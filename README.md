# Automated Logistics Data Processing Pipeline with S3, Airflow, and EMR

## Overview
This project demonstrates a Big Data pipeline for logistics data processing using AWS services such as S3, SQS, Lambda, EMR, and MWAA (Managed Workflows for Apache Airflow).

## Features
- **File Storage**: Raw files are stored in Amazon S3.
- **Event-Driven**: AWS Lambda sends S3 upload events to SQS.
- **Data Processing**: Amazon EMR runs Hive queries to process the data.
- **Orchestration**: MWAA orchestrates the workflow.



## Prerequisites
1. **AWS Services**:
   - S3, Lambda, SQS, EMR, MWAA.
2. **IAM Roles**:
   - Refer to `iam/required_roles.txt`.

## Steps to Deploy

***1. Create S3 buckets:***
```bash
aws s3 mb s3://logistics-raw
aws s3 mb s3://logistics-archive
bash mwaa/create_mwaa_bucket.sh
```

***2. Create an SQS queue:***
```bash
aws sqs create-queue --queue-name logistics-processing-queue
```

***3. Deploy the Lambda function:***

Note: In "s3_trigger.json" file used in following commad, You need to replace <LAMBDA_FUNCTION_ARN> with lambda function arn you get as output lambda function creation command 
```bash
cd lambda
./install_dependencies.sh
aws lambda create-function --function-name logistics-trigger-sqs ...
aws s3api put-bucket-notification-configuration --bucket logistics-raw --notification-configuration file://../s3/s3_trigger.json
```

***4. Launch an EMR cluster:***

1. Create an EMR Cluster:
```bash
aws emr create-cluster \
    --name "Logistics-Processing-Cluster" \
    --release-label emr-6.3.0 \
    --applications Name=Hive \
    --instance-type m5.xlarge \
    --instance-count 3 \
    --use-default-roles
```

2. Add Hive Steps to the Cluster: Replace <CLUSTER_ID> with the ID returned from the previous command:
```bash
aws emr add-steps \
    --cluster-id <CLUSTER_ID> \
    --steps file://emr/hive_steps.json
```

***5. Deploy Airflow DAG:***
```bash
aws s3 cp dags/aws_logistics_pipeline_dag.py s3://logistics-mwaa-dags/dags/
```

***6. Test the Pipeline:***
```bash
aws s3 cp test_file.csv s3://logistics-raw/input_data/
```

