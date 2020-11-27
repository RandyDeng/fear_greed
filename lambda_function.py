import json
import time
import requests
import boto3
from bs4 import BeautifulSoup

def lambda_handler(event, context):

    session = boto3.Session()
    client = session.client('timestream-write')

    page = requests.get('https://money.cnn.com/data/fear-and-greed')
    content = BeautifulSoup(page.content, 'html.parser')
    fearGreedText = content.find(id='needleChart').select('li')[0].text
    fearGreedValue = fearGreedText.split('Fear & Greed Now:')[1].split()[0]

    record = {
        'Dimensions': [{'Name': 'Name', 'Value': 'FearGreedIndex'}],
        'MeasureName': 'FearGreedIndexValue',
        'MeasureValue': fearGreedValue,
        'MeasureValueType': 'BIGINT',
        'Time': str(int(round(time.time() * 1000)))
    }

    client.write_records(DatabaseName='StockData', TableName='FearAndGreedIndex',
                         Records=[record], CommonAttributes={})

    return {
        'statusCode': 200,
        'body': json.dumps('Complete')
    }
