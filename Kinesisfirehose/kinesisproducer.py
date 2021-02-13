import json
import boto3
import random
import datetime

# define our Kinesis service using the us-west-2 region
kinesis = boto3.client('kinesis', region_name='us-west-2')

# function to produce our streaming data
def produceData():
    data = {}
    time_now = datetime.datetime.now()
    time_now_string = time_now.isoformat()
    data['EVENT_TIME'] = time_now_string
    data['ITEM'] = random.choice(['Longboard', 'Onewheel', 'Surfboard', 'Snowboard', 'Paddleboard'])
    price = random.random() * 100
    data['PRICE'] = round(price, 2)
    return data

# define the number of data stream elements we wish to create
number_of_records = 30
record_count = 0

# create the streaming data and send it to our Kinesis Data Stream called kinesis-firehose-demo
while record_count < number_of_records:
        data = json.dumps(produceData()) + 'record # ' + str(record_count)
        print(data)
        kinesis.put_record(
                StreamName="kinesis-firehose-demo",
                Data=data,
                PartitionKey="partitionkey")
        record_count += 1
