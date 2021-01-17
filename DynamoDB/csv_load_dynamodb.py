import boto3
import csv

def lambda_handler(event, context):
    region='us-east-1'
    recList=[]
    try:            
        s3=boto3.client('s3')            
        dyndb = boto3.client('dynamodb', region_name=region)
        confile= s3.get_object(Bucket='my-bucket', Key='employee.csv')
        recList = confile['Body'].read().split('\n')
        firstrecord=True
        csv_reader = csv.reader(recList, delimiter=',', quotechar='"')
        for row in csv_reader:
            if (firstrecord):
                firstrecord=False
                continue
            key = row[0]
            sender_id = row[1].replace(',','').replace('$','') if row[1] else '-'
            label = row[2].replace(',','').replace('Not sure','Apparel') if row[2] else 'Apparel'
            kids = row[3].replace(',','').replace('$','') if row[3] else 'false'
            response = dyndb.put_item(
                TableName='Images-data',
                Item={
                'key' : {'S':key},
                'sender_id': {'S':sender_id},
                'label': {'N':label},
                'kids': {'BOOL':False},
                }
            )
        print('Put succeeded:')
    except Exception, e:
        print (str(e))
