# import csv

# # Define a function to read the data from the CSV file
# def read_csv(filename):
#     companies = []
#     with open(filename, newline='', encoding='utf-8') as csvfile:
#         reader = csv.reader(csvfile)
#         for row in reader:
#             # Assuming the first element (index 0) is company_name and second element (index 1) is company_url
#             if len(row) == 2:
#                 company_name = row[0].strip()
#                 company_url = row[1].strip()
#                 companies.append([company_name, company_url])
#     return companies

# # Example usage:
# companies = read_csv(filename='companies.csv')
# for company in companies:
#     company_name = company[0]
#     company_url = company[1].replace('https:', '').replace('www.', '').replace('/', '')
#     print(company_name, company_url)

import os
user = os.environ.get('USERNAME')
print(user)