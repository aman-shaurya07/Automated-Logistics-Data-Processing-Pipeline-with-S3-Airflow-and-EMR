#!/bin/bash

# Create a directory for dependencies
mkdir -p ./package

# Install dependencies into the package directory
pip install -r requirements.txt -t ./package

# Add the Lambda function code to the package
cp lambda_trigger_sqs.py ./package

# Zip everything
cd package
zip -r ../lambda_trigger_sqs.zip .
cd ..
