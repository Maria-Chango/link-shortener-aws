import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "url_shortener")

# Boto3 utilizará automáticamente el rol IAM asignado a la instancia EC2
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)

def get_url_item(short_code: str):
    try:
        response = table.get_item(Key={"short_code": short_code})
        return response.get("Item")
    except ClientError as e:
        print(f"Error al consultar DynamoDB: {e.response['Error']['Message']}")
        return None

def put_url_item(item: dict):
    try:
        table.put_item(Item=item)
        return True
    except ClientError as e:
        print(f"Error al insertar en DynamoDB: {e.response['Error']['Message']}")
        return False