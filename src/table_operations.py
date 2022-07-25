import boto3
from datetime import datetime
from logging import getLogger

logger = getLogger("AccessHandler")

dynamodb = boto3.resource('dynamodb')
access_store = dynamodb.Table('access_store')


def write_to_store(access_token):
    dynamodb = boto3.resource('dynamodb')
    access_store = dynamodb.Table('access_store')

    response = access_store.put_item(
        Item={
            'date': datetime.utcnow().date().strftime('%Y-%m-%d'),
            'datetime': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'access_token': access_token
        }
    )
    return response
