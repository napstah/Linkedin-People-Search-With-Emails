from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import random
from time import sleep
import math
import pandas as pd
import csv
import urllib.parse
import os


STARTING_PAGE = 1
people = []
keywords = input("Keywords: ").replace("&", '%26').replace(' ', '%20').replace('/','%2F')

user = os.environ.get('USERNAME')

def get_driver():
    options = Options()
    options.add_argument(f"user-data-dir=C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    return driver


def get_format_url(driver, company_name, company_url):
    encoded_company_name = urllib.parse.quote(company_name)
    url = f'https://www.google.com/search?q={encoded_company_name}+%40{company_url}+%22email+format%22+%22rocketreach%22'
    driver.get(url)
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')
    email_format_url = soup.find('div', class_='kvH3mc BToiNc UK95Uc').find('div', class_='yuRUbf').find('a').get('href')
    print(email_format_url)
    return email_format_url


def get_format_from_url(driver, email_format_url):
    url = email_format_url
    driver.get(url)
    sleep(10)
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')
    posible_email_format = soup.find('div', class_='headline-summary').find('div', class_='table-wpr').find('table', class_='table').find('tbody').find('tr').find('td').text.strip()
    print(posible_email_format)
    return posible_email_format


def match_posible_format(first_name, last_name, posible_email_format, company_url):
    match posible_email_format:
        case '[first]':
            return f'{first_name}@{company_url}'
        case '[last]':
            return f'{last_name}@{company_url}'
        case '[last][first]':
            return f'{last_name}{first_name}@{company_url}'
        case '[last].[first]':
            return f'{last_name}.{first_name}@{company_url}'
        case '[last]_[first]':
            return f'{last_name}_{first_name}@{company_url}'
        case '[last][first_initial]':
            return f'{last_name}{first_name[0]}@{company_url}'
        case '[last].[first_initial]':
            return f'{last_name}.{first_name[0]}@{company_url}'
        case '[last]_[first_initial]':
            return f'{last_name}_{first_name[0]}@{company_url}'
        case '[last_initial][first]':
            return f'{last_name[0]}{first_name}@{company_url}'
        case '[last_initial].[first]':
            return f'{last_name[0]}.{first_name}@{company_url}'
        case '[last_initial]_[first]':
            return f'{last_name[0]}_{first_name}@{company_url}'
        case '[first][last]':
            return f'{first_name}{last_name}@{company_url}'
        case '[first].[last]':
            return f'{first_name}.{last_name}@{company_url}'
        case '[first]_[last]':
            return f'{first_name}_{last_name}@{company_url}'
        case '[first][last_initial]':
            return f'{first_name}{last_name[0]}@{company_url}'
        case '[first].[last_initial]':
            return f'{first_name}.{last_name[0]}@{company_url}'
        case '[first]_[last_initial]':
            return f'{first_name}_{last_name[0]}@{company_url}'
        case '[first_initial][last]':
            return f'{first_name[0]}{last_name}@{company_url}'
        case '[first_initial].[last]':
            return f'{first_name[0]}.{last_name}@{company_url}'
        case '[first_initial]_[last]':
            return f'{first_name[0]}_{last_name}@{company_url}'
        case '[first_initial][last_initial]':
            return f'{first_name[0]}{last_name[0]}@{company_url}'
        case '[first_initial].[last_initial]':
            return f'{first_name[0]}.{last_name[0]}@{company_url}'
        case '[first_initial]_[last_initial]':
            return f'{first_name[0]}_{last_name[0]}@{company_url}'


def get_linkedin_url(company_name, driver):
    encoded_company_name = urllib.parse.quote(company_name)
    url = f'https://www.google.com/search?q={encoded_company_name}+linkedin'
    driver.get(url)
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')
    try:
        linkedin_url = soup.find('div', class_='yuRUbf').find('a').get('href')
        return linkedin_url
    except AttributeError:
        return None


def check_and_transform_linkedin_url(linkedin_url):
    separator = "."
    replacement = 'https://www'
    if replacement not in linkedin_url:
        url = linkedin_url.split('.')
        url[0] = replacement
        linkedin_url = separator.join(url)
        print(linkedin_url)
        return linkedin_url
    else:
        return linkedin_url
    

def transform_url(linkedin_url, driver):
    if linkedin_url:
        driver.get(linkedin_url)
        src = driver.page_source
        soup = BeautifulSoup(src, 'html.parser')
        return soup
    

def full_linkedin_url(soup):
    try:
        url = soup.find('div', class_='inline-block').find('a').get('href')
        full_linkedin_url = f'https://www.linkedin.com{url}'
        return full_linkedin_url
    except AttributeError:
        try:
            url = soup.find('a', class_='ember-view org-top-card-summary-info-list__info-item').get('href')
            full_linkedin_url = f'https://www.linkedin.com{url}'
            return full_linkedin_url
        except AttributeError:
            print("LinkedIn URL not found")
            return None
        

def get_company_name(soup):
    try:
        company_name = soup.find('span', attrs={'dir':'ltr'}).text.strip()
        return company_name
    except AttributeError: 
        try:
            company_name = soup.find('h1', class_='ember-view text-display-medium-bold org-top-card-summary__title')
            return company_name
        except AttributeError:
            print("Company Name not found")
            return None
        

def get_num_of_people(soup):
    try:
        init_result = soup.find('h2', class_='pb2 t-black--light t-14').text.strip().split()
        for element in init_result:
            try:
                number = int(element.replace(',', ''))
                return number
            except ValueError:
                pass    
        return 0
    except AttributeError:
        return 0
    

def num_of_pages(num_of_people):
    try:
        num_of_pages = math.ceil(num_of_people / 10)
        return num_of_pages
    except:
        return 0


def extract(transformed_url, page, driver, keywords):
    if transformed_url:
        #'&keywords="Demand%20Generation"'
        #'&keywords="Demand%20Generation"%20OR%20"Account-based%20Marketing"%20OR%20ABM%20Marketing%20OR%20"Competitive%20intelligence"%20OR%20"Competitive%20Market"'
        # keywords = '&keywords="Finance"%20OR%20"IT"'
        profile_url = f'{transformed_url}{keywords}&page={page}'
        driver.get(profile_url)
        sleep(3)
        src = driver.page_source
        soup = BeautifulSoup(src, 'html.parser')
        return soup
    

def transform(soup, company_name, page, posible_email_format, company_url):
    if page == 1:
        try:
            ul = soup.find_all('ul', class_='reusable-search__entity-result-list list-style-none')[1]
            lis = ul.find_all('li')
        except:
            lis = ''
    elif page > 1:
        ul = soup.find_all('ul', class_='reusable-search__entity-result-list list-style-none')[0]
        lis = ul.find_all('li')
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
            if first_name == 'Linkedin':
                matched_email = 'NA'
            else:
                matched_email = match_posible_format(first_name.lower(), last_name.lower().split(' ')[-1], posible_email_format, company_url)
            person = {
                'LinkedIn Profile URL': profile_url,
                'First Name': first_name,
                'Last Name': last_name,
                'Title': title,
                'Company': company_name,
                'Posible email': matched_email,
            }
            people.append(person)
    return


def time_to_sleep(people):
    if people <= 10:
        sleep_time = 5
    elif people > 10 and people <= 49:
        sleep_time = random.randint(8, 14)
    elif people > 50 and people <= 149:
        sleep_time = random.randint(15, 20)
    elif people >= 150 and people <= 300:
        sleep_time = random.randint(21, 24)
    else:
        sleep_time = random.randint(25, 30)
    return sleep_time


def read_csv(filename):
    companies = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 2:
                company_name = row[0].strip()
                company_url = row[1].strip()
                companies.append([company_name, company_url])
    return companies


def scrape(driver, keywords):
    
    companies = read_csv(filename='companies.csv')
    for company in companies:
        company_name = company[0]
        print(company_name)
        company_url = company[1].replace('https:', '').replace('www.', '').replace('/', '')
        print(company_url)
        email_format_url = get_format_url(driver, company_name, company_url)
        posible_email_format = get_format_from_url(driver, email_format_url)
        linkedin_url = get_linkedin_url(company_name, driver)
        checked_url = check_and_transform_linkedin_url(linkedin_url)
        sleep(2)
        soup_content = transform_url(checked_url, driver)
        transformed_url = full_linkedin_url(soup_content)
        company_name = get_company_name(soup_content)
        sleep(2)
        content = extract(transformed_url, STARTING_PAGE, driver, keywords)
        num_of_people = get_num_of_people(content)
        if num_of_people >= 1000:
            pages = 100
        else:
            pages = num_of_pages(num_of_people)
        sleep_time = time_to_sleep(num_of_people)
        print(f'Found {num_of_people} people in {company_name}, sleep time set to: {sleep_time}')
        if pages == 1:
            print(f"Getting Page 1 of {pages}", end='\r')
            transform(content, company_name, pages, posible_email_format, company_url)
            print(people)
            df = pd.DataFrame(people)
            try:
                cmpny = company_name.replace('/', '')
            except:
                cmpny = company_name
            df.to_csv(f'contacts_{cmpny}.csv', index=False)
        else:
            print(f"Getting Page 1 of {pages}", end='\r')
            transform(content, company_name, STARTING_PAGE, posible_email_format, company_url)
            for i in range(STARTING_PAGE + 1, pages + 1):
                if i <= 100:
                    sleep(sleep_time)
                    print(f"Getting Page {i} of {pages}", end='\r')
                    cont = extract(transformed_url, i, driver, keywords)
                    transform(cont, company_name, i, posible_email_format, company_url)
                else:
                    cmpny = company.replace('/', '')
                    df = pd.DataFrame(people)
                    df.to_csv(f'contacts_{cmpny}.csv', index=False)
                    break
        try:
            cmpny = company_name.replace('/', '')
        except:
            cmpny = company_name
        df = pd.DataFrame(people)
        df.to_csv(f'contacts_{cmpny}.csv', index=False)
        people.clear()
        sleep(sleep_time)
    driver.quit()


def main():
    driver = get_driver()
    scrape(driver, keywords)

if __name__ == '__main__':
    main()