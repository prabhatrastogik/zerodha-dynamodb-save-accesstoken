from logging import getLogger

from kiteconnect import KiteConnect

logger = getLogger("AccessHandler")


def is_request_token_call(event, api_auth):
    if event.get('requestContext', {}).get('http', {}).get('method', '') == "GET":
        if event.get('rawPath', '').startswith('/default/save_access'):
            logger.info(
                f"GET Call to save access; Referrer = {event.get('headers',{}).get('referrer','')}"
            )
            if event.get('queryStringParameters', {}).get('api_auth', '') == api_auth:
                logger.info(f"Auth for GET call verified")
                return True
            else:
                logger.error(f"Invalid Auth")
        else:
            logger.info(
                f"Not a request token call. rawPath={event.get('rawPath', '')}"
            )
    else:
        logger.info("Not a save GET request;")
    return False


def get_request_token(event):
    returned_params = event.get('queryStringParameters', {})
    for param in ['request_token', 'status', 'type', 'action', 'api_auth']:
        if param not in returned_params.keys():
            logger.error(
                f"""Request Not Formed Correctly - Perhaps not from Zerodha or Failed Query 
                    Params = {returned_params}
                """)
            raise Exception(
                "No request token found in the redirect - check logs for analysis"
            )
    return returned_params['request_token']


def get_session(api_key, api_secret, request_token):
    kite = KiteConnect(api_key=api_key)
    resp = kite.generate_session(
        request_token=request_token, api_secret=api_secret)
    if resp.get('access_token'):
        logger.info("Session Generated!")
        return resp.get('access_token')
    else:
        logger.error(f"Access token not created; Response = {resp}")
        raise Exception("Session Not Generated! Check logs")
