import parameters
import csv
from time import sleep
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('/Users/jacobtadesse/Documents/practice/prospect/chromedriver')
driver.get('https://www.linkedin.com')

username = driver.find_element_by_xpath('/html/body/main/section[1]/div[2]/form/div[2]/div[1]/input')
username.send_keys(parameters.linkedin_username)
sleep(0.5)

password = driver.find_element_by_xpath('/html/body/main/section[1]/div[2]/form/div[2]/div[2]/input')
password.send_keys(parameters.linkedin_password)
sleep(0.5)

sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
sign_in_button.click()
sleep(0.5)

driver.get('https:www.google.com')
sleep(3)

search_query = driver.find_element_by_name('q')
search_query.send_keys(parameters.search_query)
sleep(0.5)

search_query.send_keys(Keys.RETURN)
sleep(3)

linkedin_urls = driver.find_elements_by_class_name('r')
linkedin_urls = [url.text for url in linkedin_urls]
sleep(0.5)

# defining new variable passing two parameters
writer = csv.writer(open(parameters.file_name, 'w'))

# writerow() method to the write to the file object
writer.writerow(['Name','Job Title','Company','College', 'Location','URL'])

def validate_field(field):# if field is present pass if field:pass
# if field is not present print text else:
    field = 'No results'
    return field

# For loop to iterate over each URL in the list
for linkedin_url in linkedin_urls:

    # get the profile URL 
    driver.get(linkedin_url)

    # add a 5 second pause loading each URL
    sleep(5)

    # assigning the source code for the webpage to variable sel
    sel = Selector(text=driver.page_source) 

    # xpath to extract the text from the class containing the name
    name = sel.xpath('//h1/text()').extract_first()

    if name:
        name = name.strip()


    # xpath to extract the text from the class containing the job title
    job_title = sel.xpath('//*[starts-with(@class, "pv-top-card-section__headline")]/text()').extract_first()

    if job_title:
        job_title = job_title.strip()


    # pulling company name from job title
    company = ""
    try:
        company = job_title.split('at')[-1]
    except: 
        pass

    if company:
        company = company.strip()


    # xpath to extract the text from the class containing the college
    college = sel.xpath("//*[starts-with(@class, 'text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view')]/text()").extract_first()

    if college:
        college = college.strip()


    # xpath to extract the text from the class containing the location
    location = sel.xpath("//*[starts-with(@class, 't-16 t-black t-normal inline-block')]/text()").extract_first()

    if location:
        location = location.strip()

    # terminates the application
    driver.quit()

    # printing the output to the terminal
    print('\n')
    print('Name: ' + name)
    print('Job Title: ' + job_title)
    print('Company: ' + company)
    print('College: ' + college)
    print('Location: ' + location)
    print('URL: ' + linkedin_url)
    print('\n')

    # writing the corresponding values to the header
    writer.writerow([name.encode('utf-8'),
                    job_title.encode('utf-8'),
                    company.encode('utf-8'),
                    college.encode('utf-8'),
                    location.encode('utf-8'),
                    linkedin_url.encode('utf-8')])
# terminates the application
driver.quit()                 