import csv
toast = input("Train: ")

with open("trainsblahblajblah.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        if toast in row[0]:
            log = row[0]

quicklog = [log]

with open("quicklogs.csv", mode="a", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(quicklog)
