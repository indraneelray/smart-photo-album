import json
import boto3
from botocore.vendored import requests
import time


def lambda_handler(event, context):
    print(json.dumps(event, indent=4, sort_keys=True))
    print("line1")
    s3_info = event['Records'][0]['s3']
    bucket_name = s3_info['bucket']['name']
    key_name = s3_info['object']['key']
    #print(bucket_name)
    client = boto3.client('rekognition')
    print("line1.1")
    pass_object = {'S3Object':{'Bucket':bucket_name,'Name':key_name}}
    print (pass_object)
    print("2")
    resp = client.detect_labels(Image=pass_object)
    print("3")
    print('<---------Now response object---------->')
    print(json.dumps(resp, indent=4, sort_keys=True))
    timestamp =time.time()
    labels = []
    for i in range(len(resp['Labels'])):
        labels.append(resp['Labels'][i]['Name'])
    print('<------------Now label list----------------->')
    print(labels)
    print('<------------Now required json-------------->')
    format = {'objectKey':key_name,'bucket':bucket_name,'createdTimestamp':timestamp,'labels':labels}
    url = "https://vpc-photoes-pkippvrbcck5ytoxiq7bxgxwfe.us-east-1.es.amazonaws.com/photos/0"
    headers = {"Content-Type": "application/json"}
    print("elastic")
    r = requests.post(url, data=json.dumps(format).encode("utf-8"), headers=headers)
    print('<------------------GET-------------------->')
    print(r.text)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
