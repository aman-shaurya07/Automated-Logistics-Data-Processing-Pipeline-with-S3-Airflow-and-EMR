#!/bin/bash

aws s3 mb s3://logistics-mwaa-dags
aws s3 cp ../dags/aws_logistics_pipeline_dag.py s3://logistics-mwaa-dags/dags/
