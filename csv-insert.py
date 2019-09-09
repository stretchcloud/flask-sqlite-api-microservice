import csv
import uuid


### Add UUID to each row of the supplied CSV File
fin = open('titanic.csv', 'r')
fout = open('out.csv', 'w')

reader = csv.reader(fin, delimiter=',', quotechar='"')
writer = csv.writer(fout, delimiter=',', quotechar='"')

firstrow = True
for row in reader:
    if firstrow:
        row.append('UUID')
        firstrow = False
    else:
        row.append(uuid.uuid1())
    writer.writerow(row)
### end of CSV modification