#!/bin/bash

echo "Checking setup requirements..."

# Check if Google Cloud SDK is installed
if ! command -v gcloud &> /dev/null; then
    echo "Google Cloud SDK not found. Please install it first."
    echo "Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if BigQuery CLI (bq) is installed
if ! command -v bq &> /dev/null; then
    echo "BigQuery CLI (bq) not found. Please install Google Cloud SDK components."
    echo "Run: gcloud components install bq"
    exit 1
fi

# Check if we're authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q '^'; then
    echo "Not authenticated with Google Cloud."
    echo "Please run: gcloud auth login"
    echo "Then run: gcloud auth application-default login"
    exit 1
fi

# Set the project explicitly
echo "Setting project to shopify-dw..."
gcloud config set project shopify-dw

# Check if we have access to the project
if ! gcloud projects describe shopify-dw &> /dev/null; then
    echo "No access to shopify-dw project."
    echo "Please ensure you have the correct permissions."
    exit 1
fi

# Check Python requirements
echo "Checking Python packages..."
pip install -r requirements.txt

# Try to get dataset location
echo "Checking dataset location..."
if ! bq show --format=prettyjson shopify-dw:raw_salesloft > /dev/null 2>&1; then
    echo "Cannot access dataset shopify-dw:raw_salesloft"
    echo "Please ensure:"
    echo "1. You have proper permissions"
    echo "2. The dataset name is correct (raw_salesloft)"
    echo "3. You are in the correct project (shopify-dw)"
    exit 1
fi

echo "Setup check complete. Running search script..."

# Run the simplified search script
python simplified_search.py 