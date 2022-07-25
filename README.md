# Zerodha Login Access DynamoDB storage Tool

## Context
This code is for a docker container that runs as a lambda function to store access_token to DynamoDB provided by Zerodha Redirect URL.

## How to productionalize
- Get Zerodha (kite.trade) account for API based access to the platform.
- Create an AWS API Gateway (type HTTP) and place that as the redirect url for Zerodha API access.
- Create a DynamoDB Table 'save_access' - with primary key as 'date' of type string and secondary key (sort key) as 'datetime' of type string
- Create a Lambda function of type container. Give it access to DynamoDB and set its trigger to be the API Gateway.
- Add ENV variables for the lambda function  - check the .env.sample file.
    ZAPI - provided by zerodha - the API key
    ZSECRET - provided by zerodha - the API secret
    ZAPI_AUTH - ZAPI_AUTH is created as a way to ensure that the api redirect is coming from Zerodha itself. Choose any complex string as this value (your choice) AND
    When logging in - send this as a redirect parameter 'api_auth'. For this, your Zerodha login URL will be
    f'https://kite.trade/connect/login?v=3&api_key={api_key}&redirect_params={quote_plus(f"api_auth={api_auth}")}'

## This repo is a sister repo with ZLOGIN tool which automates login through selenium; 
That tool creates the redirect to the API gateway. For both to work properly, please use the same  ZAPI_AUTH environment variable value in both places
