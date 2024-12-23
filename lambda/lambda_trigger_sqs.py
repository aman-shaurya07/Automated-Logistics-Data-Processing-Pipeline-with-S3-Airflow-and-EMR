import json
import boto3

def lambda_handler(event, context):
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        file_key = record['s3']['object']['key']

        sqs_client = boto3.client('sqs')
        queue_url = '<SQS_QUEUE_URL>'  # Replace with your SQS Queue URL

        message_body = {
            "bucket_name": bucket_name,
            "file_key": file_key
        }

        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message_body)
        )

        print(f"Message sent to SQS: {response['MessageId']}")

    return {
        'statusCode': 200,
        'body': json.dumps('Message successfully sent to SQS')
    }
