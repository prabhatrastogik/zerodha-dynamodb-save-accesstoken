FROM public.ecr.aws/lambda/python
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install kiteconnect boto3
COPY . ${LAMBDA_TASK_ROOT}
CMD ["handler.handler"]
