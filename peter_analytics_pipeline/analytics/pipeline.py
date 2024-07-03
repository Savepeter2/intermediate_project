#Importing the required libraries
import pandas as pd
import polars as pl 
import re
import numpy as np
import duckdb as db

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

# I created a pandas dataframe, because for some weird reasons, polars dataframe can't recognize the invoicedtae column as a datetime datatype
df_1 = pd.read_csv("/peter_analytics_pipeline/analytics/data/Online_Retail.csv")

#change the InvoiceDate column to datetime
df_1['InvoiceDate'] = pd.to_datetime(df_1['InvoiceDate'])

pl_invoicedate_col = pl.Series('InvoiceDate', np.array(df_1['InvoiceDate']))

schema = {
    'InvoiceNo': pl.Utf8
}

df = pl.read_excel("/peter_analytics_pipeline/analytics/data/Online_Retail1.xlsx",
                   schema_overrides=schema)

df_copy = df.clone()
df_copy = df_copy.with_columns([pl_invoicedate_col])
df_copy.with_columns(pl.col("InvoiceNo").cast(pl.Categorical))

def check_invalid_entries(df_column):
    filtered_column = df_copy.filter(pl.col(df_column).str.contains(r"[a-zA-Z]")).select(df_column).unique()
    return filtered_column

alpha_invoice = check_invalid_entries('InvoiceNo')
alpha_invoice_list = alpha_invoice['InvoiceNo'].to_list()

def get_non_c_entries(alpha_invoice_list):
    pattern = r"^(?!C).+"
    pattern = re.compile(pattern)
    non_alpha_invoice = []
    c_entries = []
    for entry in alpha_invoice_list:
        c_codes = pattern.match(entry)
        if c_codes:
            non_alpha_invoice.append(entry)
    return non_alpha_invoice

non_alpha_invoice = get_non_c_entries(alpha_invoice_list)
df_copy = df_copy.with_columns(pl.col('InvoiceNo').str.replace_all("A", ""))
cancelled_invoices =  df_copy.filter(pl.col('InvoiceNo').str.contains(r"[a-zA-Z]"))

def remove_letters_stocks(df):
    filtered_df = df.filter(pl.col("StockCode").str.contains(r"[a-zA-Z]"))
    filtered_df = filtered_df.with_columns(pl.col("StockCode").str.replace_all(r"[a-zA-Z]", ""))
    return filtered_df

filtered_df = remove_letters_stocks(df_copy)

filtered_df = filtered_df.filter(pl.col("StockCode") != "")

filtered_df = filtered_df.filter(pl.col("StockCode").str.len_chars() == 5)

# check if the Invoice column has entries that are not equal to 6 and do not contain "C"
filtered_df.filter(
    (pl.col("InvoiceNo").str.len_chars() != 6) & (~pl.col("InvoiceNo").str.contains(r"[C]"))
)

customer_ids = filtered_df['CustomerID'].unique().to_list()

invalid_ids = []
for id in customer_ids:
    id = str(id)
    if len(id) != 5:
        invalid_ids.append(id)

# drop duplicates
filtered_df = filtered_df.filter(filtered_df.is_duplicated() == False)

filtered_df = filtered_df.with_columns(pl.col("Quantity").abs())

filtered = filtered_df.with_columns(pl.col("UnitPrice").abs())

filtered_df.write_excel("/peter_analytics_pipeline/analytics/data/Online_Retail_cleaned.xlsx")

cleaned_df = filtered_df

agg_df = cleaned_df.with_columns((pl.col("UnitPrice") * pl.col("Quantity")).alias("TotalSales")) \
            .select(["StockCode", "TotalSales"])

agg_df = agg_df.group_by("StockCode").agg([
    pl.sum("TotalSales").alias("Total_Cost_Stock_Sold"
),
    pl.mean("TotalSales").alias("Average_Sales"),
    pl.min("TotalSales").alias("Min_Sales"),
    pl.max("TotalSales").alias("Max_Sales"),
]
).sort("StockCode")

agg_df = agg_df.with_columns(pl.Series("id", np.arange(1, len(agg_df) + 1)))

agg_df = agg_df.with_columns(pl.col("id").cast(pl.Int64)) \
    .with_columns(pl.col("StockCode").cast(pl.Utf8)) \
            .with_columns(pl.col("Total_Cost_Stock_Sold").round(2).cast(pl.Float64)) \
            .with_columns(pl.col("Average_Sales").round(2).cast(pl.Float64)) \
            .with_columns(pl.col("Min_Sales").round(2).cast(pl.Float64)) \
            .with_columns(pl.col("Max_Sales").round(2).cast(pl.Float64))

agg_df = agg_df.select(["id"] + agg_df.columns[:-1])


# save the aggregated data to a new excel file
agg_df.write_excel("/peter_analytics_pipeline/analytics/data/Online_Retail_aggregated.xlsx")

# create a path for the new duckdb database file
db_path = "online_retail_output.duckdb"

Base = declarative_base()

class  OnlineRetailOutput(Base):
    __tablename__ = 'finance_data'
    
    id = Column(Integer, primary_key=True, autoincrement=False)
    StockCode = Column(String)
    Total_Cost_Stock_Sold = Column(Float)
    Average_Sales = Column(Float)
    Min_Sales = Column(Float)
    Max_Sales = Column(Float)


def save_to_duckdb(df, db_path):
    engine = create_engine(f"duckdb:///{db_path}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(autocommit = False, autoflush=False, bind=engine)
    db = Session()
    
    new_df_dict = {}
    df_columns = df.columns

    try:
        for row in df.iter_rows():
            new_df_dict = {col: row[df_columns.index(col)] for col in df_columns}
            online_retail_data = OnlineRetailOutput(**new_df_dict)
            db.add(online_retail_data)

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
        raise
    finally:
        db.close()

    return f"Data saved to {db_path} successfully"

save_to_duckdb(agg_df, db_path)

