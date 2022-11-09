from boto3 import client
from openpyxl import Workbook, load_workbook


sourceDirectory = 'fulfilmentretry/2022/09/29/'
inputDirectory = 'input/2022/09/27/'
destinationDirectory = 'codeTrigger/'
Bucket='opsandsrvosv-orderfulfilmentpersist-prod-us-west-2'

page_number = 0
count = 0
findinbox = []
checked = {}

s3 = client('s3')

paginator = s3.get_paginator('list_objects_v2')

#Get all the pages from the bucket
pages = paginator.paginate(Bucket=Bucket, Prefix=sourceDirectory)

for page in pages:

    #For each document in the page
    for obj in page['Contents']:
        count += 1
        #print(count, obj)

        #Extracting the Document number from the filepath 
        Key = obj['Key'].split('/')
        item_ = Key[-1].split('-')

        #print(count, item_)

        strings = item_[0].split('%')

        #print(strings)

        fulfillmentNumber = strings[4][2:].split('-')
        print(fulfillmentNumber[0])

        #print(count, fulfillmentNumber)

        findinbox.append(fulfillmentNumber[0])

print(findinbox)

count = 0
pages = paginator.paginate(Bucket=Bucket, Prefix=inputDirectory)

for page in pages:
    page_number += 1
    print(page_number)

    #For each document in the page
    for obj in page['Contents']:

        #Extracting the Document number from the filepath 
        Key = obj['Key'].split('/')
        item_ = Key[-1].split('-')


        #If mising according to the list provided
        if item_[0] in findinbox:
            count += 1
            copy_source = Bucket + '/' + obj['Key']
            copyDestination = destinationDirectory + Key[-1]

            
            #aws cli command to copy object
            response = s3.copy_object(CopySource = copy_source, Bucket=Bucket, Key=copyDestination)  
            if count%10 == 0:
                print(response)
                #print(count, copy_source + ' - ' + Bucket + '/' + copyDestination)
        else:
            continue
