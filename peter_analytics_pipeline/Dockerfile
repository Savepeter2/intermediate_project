FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /peter_analytics_pipeline

#Install DuckDB
RUN apt-get update && apt-get install -y wget
RUN apt-get update && apt-get install -y unzip
RUN wget https://github.com/duckdb/duckdb/releases/download/v0.8.1/duckdb_cli-linux-amd64.zip
RUN unzip duckdb_cli-linux-amd64.zip
RUN chmod +x duckdb

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy the entire analytics directory, which includes pipeline.py
COPY analytics /peter_analytics_pipeline/analytics

# Set the working directory to where other files to run are located
WORKDIR /peter_analytics_pipeline/analytics

#install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN python pipeline.py








