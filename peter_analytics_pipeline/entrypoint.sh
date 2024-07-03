#!/bin/bash

# Run the Python script
# python /peter_analytics_pipeline/analytics/pipeline.py

# Open DuckDB CLI
/peter_analytics_pipeline/duckdb online_retail_output.duckdb

# Keep the container running
tail -f /dev/null