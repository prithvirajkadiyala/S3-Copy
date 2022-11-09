import json
from turtle import clear
f = open('filesjson/SG.json')
readfile = json.load(f)
list = []
for i in readfile['SecurityGroups']:
    for tag in i['Tags']:
        if tag['Key'] == "nike-department" and tag["Value"] == "sec":
            print(i['GroupName'])

f.close()
# print(len(list))