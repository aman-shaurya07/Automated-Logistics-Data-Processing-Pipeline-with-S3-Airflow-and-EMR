from airflow import DAG
from airflow.providers.amazon.aws.sensors.sqs import SqsSensor
from airflow.providers.amazon.aws.operators.emr import EmrAddStepsOperator
from airflow.providers.amazon.aws.transfers.s3_to_s3 import S3ToS3Operator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'aws_logistics_pipeline',
    default_args=default_args,
    description='AWS-based Logistics Data Pipeline',
    schedule_interval='*/5 * * * *',  # Every 5 minutes
    start_date=datetime(2023, 12, 22),
    catchup=False,
)

# Wait for SQS message
# Note: When you create the queue using the aws sqs create-queue command, 
# it immediately returns the QueueUrl in the output
wait_for_file = SqsSensor(
    task_id='wait_for_file',
    sqs_queue_url='<SQS_QUEUE_URL>',  # Replace with your SQS Queue URL
    aws_conn_id='aws_default',
    dag=dag,
)

# Submit Hive Steps to EMR
hive_steps = EmrAddStepsOperator(
    task_id='hive_steps',
    job_flow_id='<EMR_CLUSTER_ID>',  # Replace with your EMR Cluster ID
    aws_conn_id='aws_default',
    steps=[
        {
            'Name': 'Create Database',
            'ActionOnFailure': 'CONTINUE',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': ['hive-script', '--run-hive-script', '--args', '-e', 'CREATE DATABASE IF NOT EXISTS logistics_db;']
            }
        },
        # Add additional steps for creating tables and loading data
    ],
    dag=dag,
)

# Move processed file to archive bucket
archive_file = S3ToS3Operator(
    task_id='archive_file',
    source_bucket_name='logistics-raw',
    source_bucket_key='input_data/logistics_*.csv',
    dest_bucket_name='logistics-archive',
    dest_bucket_key='archived_data/',
    aws_conn_id='aws_default',
    dag=dag,
)

wait_for_file >> hive_steps >> archive_file
