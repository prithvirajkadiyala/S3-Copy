# importing openpyxl module
from boto3 import client

sourceDirectory = 'input/valid/'
destinationDirectory = 'codeTrigger/'
Bucket='opsandsrvosv-asnedi-prod-us-west-2'

#Check if it is valid.
valids = []
#Count the number of records copied
count = 0
page_number = 0
#Avoid duplicates
checked = {}

with open('FailedBOL.txt') as f:
    lines = f.readlines()
    for line in lines:
        orders = line.split(",")
        BOL = orders[0].split()
        valids.append(BOL[2])

print(len(valids))

s3 = client('s3')

paginator = s3.get_paginator('list_objects_v2')

#Get all the pages from the bucket
pages = paginator.paginate(Bucket=Bucket, Prefix=sourceDirectory)

for page in pages:
    page_number += 1
    print(page_number)

    #For each document in the page
    for obj in page['Contents']:

        #Extracting the Document number from the filepath 
        Key = obj['Key'].split('/')
        item_ = Key[-1].split('-')

        #Ignoring duplicates
        if item_[0] in checked:
            continue
        else:
            #Adding the document number to the list for duplicate check
            checked[item_[0]] = True

             #If mising according to the list provided
            if item_[0] in valids:
                count += 1

                copy_source = Bucket + '/' + obj['Key']
                copyDestination = destinationDirectory + obj['Key']

                #aws cli command to copy object
                response = s3.copy_object(CopySource = copy_source, Bucket=Bucket, Key=copyDestination)  
                print(copy_source + ' - ' + Bucket + '/' + copyDestination)
                print(response)
            else:
                continue

#Printing total count after the run is complete
print(count)