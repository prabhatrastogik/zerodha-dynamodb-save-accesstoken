from logging import getLogger, DEBUG
import os
from src.access_operations import (
    is_request_token_call, get_request_token, get_session
)
from src.table_operations import write_to_store

logger = getLogger("AccessHandler")
logger.setLevel(DEBUG)


def get_env_vars():
    all_keys = dict(
        api_key=os.getenv('ZAPI'),
        api_secret=os.getenv('ZSECRET'),
        api_auth=os.getenv('ZAPI_AUTH'),
        user_id=os.getenv('ZUSER'),
        pw=os.getenv('ZPASS'),
        twofa_key=os.getenv('ZTFA'),
    )
    return all_keys


def handler(event, context):
    all_keys = get_env_vars()
    if is_request_token_call(event, all_keys['api_auth']):
        request_token = get_request_token(event)
        access_token = get_session(
            all_keys['api_key'], all_keys['api_secret'], request_token)
        response = write_to_store(access_token)
        return "Session written to store"
    raise Exception("Malformed Request")


if __name__ == "__main__":
    all_keys = get_env_vars()
    event = {
        'requestContext': {
            'http': {
                'method': 'GET'
            }
        },
        'rawPath': '/default/save_access',
        'queryStringParameters': {
            'api_auth': all_keys['api_auth'],
            'status': 200,
            'type': 'hard',
            'action': 'abc',
            'request_token': 'sample_token'
        }
    }
    handler(event, {})
