import boto3
import json
import os

bucket_name = os.environ['BUCKET_NAME']
csv_key = os.environ['CSV_KEY_NAME'] 
# csvdynamo.csv
TABLE_NAME = os.environ['TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

          
# temprorary file to store csv downloaded from s3
tmp_csv_file = '/tmp/images.csv'

s3 = boto3.resource('s3')
#db_table = boto3.resource('dynamodb').Table(table_name)

def save_to_dynamodb(key,sender_id,label,kids):
  print('save to dynamodb')
  response1 = table.put_item(
      Item={
        'key': key,
        'sender_id': sender_id,
        'label': label,
        'kids': kids,
      })
  print('load complete')
  return

def lambda_handler(event, context):
  
#    os.remove("images.csv")

    s3.meta.client.download_file(
                  bucket_name, 
                  csv_key, 
                  tmp_csv_file)
    print('file read successful')
    with open(tmp_csv_file, 'r') as f:

      next(f) # skip header
      print('next function read')
      for line in f:
        print('data read')
        key,sender_id,label,kids = line.rstrip().split(',')
        print('data:')
        result = save_to_dynamodb(key,sender_id,label,kids)

        print(result)

    return {'statusCode': 200}
