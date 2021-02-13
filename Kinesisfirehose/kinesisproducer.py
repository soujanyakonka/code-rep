import json
import boto3
import random
import datetime
import pandas as pd

# define our Kinesis service using the us-west-2 region
kinesis = boto3.client('kinesis', region_name='us-east-1')
def start_process(format_flag):
    begin_streaming(format_flag)
    
# function to produce our streaming data
def produceData():
    data = {}
    time_now = datetime.datetime.now()
    time_now_string = time_now.isoformat()
    data['event_time'] = time_now_string
    data['item'] = random.choice(['Longboard', 'Onewheel', 'Surfboard', 'Snowboard', 'Paddleboard'])
    price = random.random() * 100
    data['price'] = round(price, 2)
    return data

#define csv data
def produceCSVData():
        data = pd.read_csv("Surveillance.csv")
        return data
    
def begin_streaming(format_flag):
# define the number of data stream elements we wish to create
        number_of_records = 30
        record_count = 0
        
        
        if format_flag=='transform':
           #create the streaming data and send it to our kinesis
           data = produceCSVData()
           for _, row in data.iterrows():
                  values = ','.join(str(value) for value in row)
                  encodedValues = bytes(values, 'utf-8') 
                  print(encodedValues)
                  Kinesis.put record(
                          StreamName="sparkstreamsource",
                          Data=data,
                          PartitionKey="partitionkey")
                  record_count +=1
        elif format_flag == 'format':
                data = produceData()
                while record_count < number_of_records:
                        data = json.dumps(produceData())
                        print(data)
                        kinesis.put_record(
                                StreamName="kinesis-firehose-demo",
                                Data=data,
                                PartitionKey="partitionkey")
                        record_count += 1
                        
if __name__ == "__main__":
    format_flag = sys.argv[1]
    start_process(format_flag)
# create the streaming data and send it to our Kinesis Data Stream called kinesis-firehose-demo
#while record_count < number_of_records:
#        data = json.dumps(produceData()) + 'record # ' + str(record_count)
#        print(data)
#        kinesis.put_record(
#                StreamName="kinesis-firehose-demo",
#                Data=data,
#                PartitionKey="partitionkey")
#        record_count += 1
