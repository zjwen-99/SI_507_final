
from bs4 import BeautifulSoup
import requests
import time
import json
import numpy

BASE_URL = 'https://www.nyc.com'
COURSES_PATH = '/restaurants'
CACHE_FILE_NAME = 'cacheSI_Scrape.json'
CACHE_DICT = {}

headers = {'User-Agent': 'UMSI 507 Course Project - Python Web Scraping','From': 'youremail@domain.com','web-Info': 'https://www.si.umich.edu/programs/courses/507'}

##### Make Soup for courses page



def load_cache():
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache


def save_cache(cache):
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()


def make_url_request_using_cache(url, cache):
    if (url in cache.keys()): # the url is our unique key
        print("Using cache")
        return cache[url]
    else:
        print("Fetching")
        time.sleep(1)
        response = requests.get(url, headers=headers)
        cache[url] = response.text
        save_cache(cache)
        return cache[url]


# Load the cache, save in global variable
CACHE_DICT = load_cache()

courses_page_url = BASE_URL + COURSES_PATH
url_text = make_url_request_using_cache(courses_page_url, CACHE_DICT)
response = requests.get(courses_page_url)

soup = BeautifulSoup(response.text, 'html.parser')



def searchCuisine():
    #chose_cuisine = input("Select Cuisine: ")
    list_parent = soup.find('div', class_='categories')
    #print('1')
    manual_list = list_parent.find_all('div', class_ = 'row searchoption-cat hidden') 
    #print(manual_list[1]) # print all cuisine

    cuisine_list = manual_list[1]
    cuisine_tags = cuisine_list.find_all('a')

    i=len(cuisine_tags)
    m=0

    cuisine_store = []
    cuisine_name_store = []
    for k in range(int(i)):
        cuisine_store.append(cuisine_tags[k]['href'])
        cuisine_name_store.append(cuisine_tags[k].contents[0])
    
    resturant_name = []
    address_list = []

    for link in cuisine_store:
        #link = cuisine_store[4]
        courses_page_url = BASE_URL + link
        response = make_url_request_using_cache(courses_page_url,CACHE_DICT)#requests.get(courses_page_url)
        soup_resturant = BeautifulSoup(response, 'html.parser')
        list_parent = soup_resturant.find('div', class_='col-md-9 col-md-push-3 col-sm-12 records')
        #print(list_parent)
        resturant_list = list_parent.find_all('li')

        resturant_link = resturant_list[0].find_all('a')[1]
        resturant_name_store = resturant_link.find_all('h3')[0].text
        resturant_name.append(resturant_name_store)
        #print(resturant_name_store)
        x=resturant_list[0].findAll('div')[0].text
        list1 = x.split('.')
        if len(list1)>3:
            street = list1[2]
            zip = list1[3]
        
        else:
            if len(list1)==3:
                street = list1[2]
                zip = list1[1]            

            elif len(list1)==2:
                street = list1[0]
                zip = list1[1]
            
            else:
                street = list1[0]
                zip = None


        address = street + zip
        address_list.append(address)
        #print(address)

    print(address_list)
    ###



def searchParking():
    BASE_URL = 'https://spothero.com/'
    COURSES_PATH = '/city/nyc-parking'
    CACHE_FILE_NAME = 'cacheSI_Scrape.json'

    CACHE_DICT = {}
    headers = {'User-Agent': 'UMSI 507 Course Project - Python Web Scraping','From': 'youremail@domain.com','Course-Info': 'https://www.si.umich.edu/programs/courses/507'}
    #list_parents =   
    
    #print(cuisine_name_store)



    print('3')
    print('4')




























if __name__=="__main__": 
    searchCuisine()