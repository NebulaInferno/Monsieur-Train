import csv

# with open("Fleetlist.csv", 'r') as file:
#     reader = csv.reader(file)
#     last_row = None
#     for row in reader:
#         last_row = row
#     log_number = int(last_row[0]) + 1
#     print(log_number)

with open("quicklogs.csv", 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

token = "MTQ1MTA1MTM3MzkzNTMyOTM5Mg.G4ReO0.5YEx9WPRFkvhZwKYoSx02KBJH7H3Vyflon4FlQ"