import csv

MyValues = [] #create an empty list
values = csv.reader(open('file.csv', 'rb'), delimiter=' ')
for row in values:
    MyValues.append(row[1])


print(MyValues)
