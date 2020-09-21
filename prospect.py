import parameters
# import csv
from time import sleep
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('/Users/jacobtadesse/Documents/practice/prospect/chromedriver')
driver.get('https://www.linkedin.com')

username = driver.find_element_by_xpath('/html/body/main/section[1]/div[2]/form/div[2]/div[1]/input')
username.send_keys(parameters.linkedin_username)
sleep(1)

password = driver.find_element_by_xpath('/html/body/main/section[1]/div[2]/form/div[2]/div[2]/input')
password.send_keys(parameters.linkedin_password)
sleep(1)

sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
sign_in_button.click()
sleep(5)

driver.get('https:www.google.com')
sleep(3)

search_query = driver.find_element_by_name('q')
sleep(0.5)

search_query.send_keys(parameters.search_query)
sleep(1)

search_query.send_keys(Keys.RETURN)
sleep(3)

linkedin_urls = driver.find_elements_by_class_name('eipWBe')
linkedin_urls = [url.text for url in linkedin_urls]
print(linkedin_urls)
sleep(2)

# # defining new variable passing two parameters
# writer = csv.writer(open(parameters.file_name, 'w'))

# # writerow() method to the write to the file object
# writer.writerow(['Name','Job Title','Company','College', 'Location','URL'])

# Creating emply list objects to store results
names = []
titles = []
companies = []
colleges = []
locations = []
links = []

def validate_field(field):# if field is present pass if field:pass
# if field is not present print text else:
    field = 'No results'
    return field

# For loop to iterate over each URL in the list
for linkedin_url in linkedin_urls:
    st = linkedin_url
    res = st.split(' ')
    link = f"https://www.linkedin.com/in/{res[-1].strip()}/"

    # get the profile URL 
    try:
        driver.get(link)
    except:
        continue

    # add a 5 second pause loading each URL
    sleep(5)

    # assigning the source code for the webpage to variable sel
    sel = Selector(text=driver.page_source) 

    # xpath to extract the text from the class containing the name
    name = sel.xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[1]/li[1]').extract_first()
    if name:
        name = name.split('\n')[-2].strip()
    else:
        name = 'Not Listed'

    # xpath to extract the text from the class containing the job title
    job_title = sel.xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/h2').extract_first()

    if job_title:
        job_title = job_title.split('\n')[-2].strip()
    else:
        job_title = 'Not Listed'


    # pulling company name from job title
    company = ""
    try:
        company = job_title.split('at ')[-1]
    except: 
        company = ""

    if company:
        company = company.strip().title()
    else:
        company = 'Not Listed'

    # xpath to extract the text from the class containing the college
    college = sel.xpath("/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[2]/ul/li/a/span/text()").extract_first()

    if college:
        college = college.strip()
    else:
        college = 'Not Listed'

    # xpath to extract the text from the class containing the location
    location = sel.xpath("/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[2]/li[1]/text()").extract_first()
    if location:
        location = location.strip()
    else:
        location = 'Not Listed'

    
    # printing the output to the terminal
    print('------------Summary-----------')
    print('\n')
    print('Name: ' + name); 
    names.append(name)
    print('Job Title: ' + job_title); 
    titles.append(job_title)
    print('Company: ' + company)
    companies.append(company)
    print('College: ' + college)
    colleges.append(college)
    print('Location: ' + location)
    locations.append(location)
    print('URL: ' + link)
    links.append(link)
    print('\n')

    # # writing the corresponding values to the header
    # writer.writerow([name.encode('utf-8'),
    #                 job_title.encode('utf-8'),
    #                 company.encode('utf-8'),
    #                 college.encode('utf-8'),
    #                 location.encode('utf-8'),
    #                 linkedin_url.encode('utf-8')])

# Creating DataFrame and removing Duplicates
import pandas as pd

data = pd.DataFrame()
data['names'] = names
data['titles'] = titles
data['companies'] = companies
data['colleges'] = colleges
data['locations'] = locations
data['links'] = links
data.drop_duplicates(inplace=True)
print(data.shape)
print(data.head())
               

# Hunter.io
from pyhunter import PyHunter

emails = []
conf_scores = []
for person, company in zip(data['names'], data['companies']):
    hunter = PyHunter('cd834d6856be0e680ee1a169a34562cca4c6f791')
    try:
        res = hunter.email_finder(company= company, full_name= person)
    except:
        res = (None, None)
    print(res)
    sleep(5)
    email = res[0]
    conf = res[1]

    emails.append(email)
    conf_scores.append(conf)
    

# Viewing Results
data['emails'] = emails
data['conf_scores'] = conf_scores
print(data.shape)
print(data.head())

# Saving Results
data.to_csv(f'{parameters.job_title}(s) at {parameters.company} - Prospects.csv')