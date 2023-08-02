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

# import os
# user = os.environ.get('USERNAME')
# print(user)

from bs4 import BeautifulSoup
from test_html import test


soup = BeautifulSoup(test, 'html.parser')


def transform(soup, company_name):
    num_of_uls = len(soup.find_all('ul', class_='reusable-search__entity-result-list list-style-none'))
    if num_of_uls > 2:
        ul = soup.find_all('ul', class_='reusable-search__entity-result-list list-style-none')[1]
        lis = ul.find_all('li')
    elif num_of_uls <= 2:
        ul = soup.find_all('ul', class_='reusable-search__entity-result-list list-style-none')[0]
        lis = ul.find_all('li')
    # if page == 1:
    #     try:
    #         ul = soup.find_all('ul', class_='reusable-search__entity-result-list list-style-none')[1]
    #         lis = ul.find_all('li')
    #     except:
    #         lis = ''
    # elif page > 1:
    #     ul = soup.find_all('ul', class_='reusable-search__entity-result-list list-style-none')[0]
    #     lis = ul.find_all('li')
    if lis != '':
        for li in lis:
            try:
                profile_url = li.find('span', class_='entity-result__title-line').find('a', class_='app-aware-link').get('href')
            except:
                profile_url = ''
            try:
                full_name = li.find('span', class_='entity-result__title-line').find('a', class_='app-aware-link').find('span', attrs={'dir':'ltr'}).find('span', attrs={'aria-hidden':'true'}).text.strip().split()
                first_name = full_name[0]
                last_name = ' '.join(full_name[1:])
            except:
                first_name = 'Linkedin'
                last_name = 'Member'
            try:
                title = li.find('div', class_='entity-result__primary-subtitle').text.strip()
            except:
                title = ''
            try:
                location = li.find('div', class_='entity-result__secondary-subtitle').text.strip()
            except:
                location = ''
            try:
                past_current_skils = li.find('p', class_='entity-result__summary').text.strip()
            except:
                past_current_skils = 'N/A'
            print(past_current_skils, location)
            
    return


transform(soup,company_name="test")