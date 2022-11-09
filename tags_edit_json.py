from boto3 import client
import json

#Read and add the required data from JSON to list
f = open('jsonfiles/roles.json')
readfile = json.load(f)
list = []
for i in readfile['Roles']:
    list.append(i['RoleName'])

f.close()
print(len(list))

count = 0

iam = client('iam')
    
tags=[
        {
            "Key": "nike-department",
            "Value": "global order and logistics"
        },
        {
            "Key": "nike-owner",
            "Value": "scott.marien@nike.com"
        },
        {
            "Key": "nike-distributionlist",
            "Value": "lst-sec.opsandservices.integration@nike.com"
        },
        {
            "Key": "nike-domain",
            "Value": "order status visibility"
        },
        {
            "Key": "nike-application",
            "Value": "opsandsrvosv-test"
        },
        {
            "Key": "nike-environment",
            "Value": "test"
        }
    ]

for obj in range(2, m_row + 1):
    count += 1
    cell_obj = sheet_obj.cell(row = obj, column = 1)
    print()
    response = iam.tag_policy(
        PolicyArn=cell_obj.value,
        Tags=tags
    )       
    print(count, cell_obj.value, response)