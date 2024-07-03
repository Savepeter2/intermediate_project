# Online Retail ETL Pipeline

This project implements an ETL (Extract, Transform, Load) pipeline for Online Retail data. It leverages Polars for data ingestion, preprocessing, and analysis, with DuckDB as the target database. The entire pipeline, including data ingestion scripts and the DuckDB database, is containerized using Docker for easy deployment and scalability.

## Features

- Data extraction from Online Retail dataset
- Data transformation and analysis using Polars
- Data loading into DuckDB
- Dockerized pipeline for portability and reproducibility

## Prerequisites

- Docker and Docker Compose
- Git

## Quick Start

1. Clone the repository:
git clone https://github.com/Savepeter2/intermediate_project.git
cd intermediate_project

2. Prepare the data:
- Place both `Online_Retail.csv` and `Online_Retail.xlsx` in the `analytics/data` folder.

3. Build and start the Docker container:
docker-compose up --build

4. Access the container:
docker start -ai etl-duckdb-container

5. Query the database:
```sql
SELECT * FROM finance_data;

Input
Online_Retail.csv: Primary dataset for the ETL process

Output
An aggregated table with the following columns:

StockCode
Total_Stock_Sold
Average_Cost
Min_Sales
Max_Sales