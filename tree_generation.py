
from bs4 import BeautifulSoup
import requests
import time
import json
import numpy

BASE_URL = 'https://www.nyc.com'
COURSES_PATH = '/restaurants'
CACHE_FILE_NAME = 'cacheSI_Scrape.json'
CACHE_DICT = {}


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
        #print("Using cache")
        return cache[url]
    else:
        print("Fetching")
        time.sleep(1)
        response = requests.get(url)
        cache[url] = response.text
        save_cache(cache)
        return cache[url]


# Load the cache, save in global variable
CACHE_DICT = load_cache()

courses_page_url = BASE_URL + COURSES_PATH
url_text = make_url_request_using_cache(courses_page_url, CACHE_DICT)
response = requests.get(courses_page_url)

soup = BeautifulSoup(response.text, 'html.parser')

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None
    
    def add_child(self, child):
        child.parent = self
        self.children.append(child)
    
    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level+=1
            p=p.parent
        return level

    def print_tree(self):
        spaces='   '*self.get_level()

        print(spaces + self.data)
        if self.children:
            for child in self.children:
                child.print_tree()
    
    def to_dict(self):
        result = {str(self.data): {}}
        for child in self.children:
            result[str(self.data)].update(child.to_dict())
        return result


def searchCuisine():

    #chose_cuisine = input("Select Cuisine: ")
    list_parent = soup.find('div', class_='categories')

    
    manual_list = list_parent.find_all('div', class_ = 'row searchoption-cat hidden') 
    #print(manual_list[1]) # print all cuisine

    #########Cuisine based
    cuisine_list_tot = manual_list[1]
    cuisine_tags = cuisine_list_tot.find_all('a')

    i=len(cuisine_tags)
    m=0
    root = TreeNode("cuisine")
    cuisine_store = []
    cuisine_name_store = []
    cuisine_link_name_dict={}
    cuisine_rest_dict = {}
    for k in range(int(i)):
        cuisine_store.append(cuisine_tags[k]['href'])
        cuisine_name_store.append(cuisine_tags[k].contents[0])
        #cuisine_link_name_dict[cuisine_name_store[k]] = cuisine_store[k]
        #print(root.add_child(TreeNode(cuisine_tags[k].contents[0])))
    

    

    
    resturant_name = []
    address_list = []
    restname_address_dict={}
    
    num=0
    for link in cuisine_store:
        courses_page_url = BASE_URL + link
        response = make_url_request_using_cache(courses_page_url,CACHE_DICT)#requests.get(courses_page_url)
        soup_resturant = BeautifulSoup(response, 'html.parser')
        list_parent = soup_resturant.find('div', class_='col-md-9 col-md-push-3 col-sm-12 records')
        #print(list_parent)
        resturant_list = list_parent.find_all('li')
        #print(resturant_list)
        collect_resturant=[]
        
        for y in range(len(resturant_list)):
            resturant_link = resturant_list[y].find_all('a')[1]
            resturant_url = resturant_link['href']   ##resturant url
            resturant_name_store = resturant_link.find_all('h3')[0].text
            collect_resturant.append(resturant_name_store)
            #print(collect_resturant)
            resturant_tree=root.add_child
            try:
                cuisine_rest_list = cuisine_rest_dict[cuisine_name_store[num]]
                #print(cuisine_rest_list)
            except:
                cuisine_rest_list = []
                #print(cuisine_rest_list)
            cuisine_rest_list.append(resturant_name_store)
            #print(cuisine_rest_list)
            cuisine_rest_dict[cuisine_name_store[num]] = cuisine_rest_list
            x=resturant_list[y].findAll('div')[0].text
            list1 = x.split('.')
            for i in range(len(list1)):
                list1[i] = list1[i].strip("\n   ")
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
            restname_address_dict[resturant_name_store] = address

        num=num+1
    #print(cuisine_rest_dict)
    root=TreeNode("cuisine")
    resturant_keys = list(cuisine_rest_dict.keys())
    for tree_sets in range(len(resturant_keys)):
        cuisine_tree = TreeNode(resturant_keys[tree_sets]) #corresponding to type of cuisine
        for resturants in cuisine_rest_dict[resturant_keys[tree_sets]]:
            #cuisine_tree.add_child(TreeNode(resturants)) #corresponding to all of resturants in this cuisine
            n2= TreeNode(resturants)
            node = TreeNode(restname_address_dict[resturants])
            n2.add_child(node)
            cuisine_tree.add_child(n2)
        root.add_child(cuisine_tree)
    
    cache_file = open('H:\course_materials\graduate\SI_507\SI507\Final_project\cuisine.json', 'w')
    contents_to_write = json.dumps(root.to_dict(),indent=4)
    #print(contents_to_write)
    cache_file.write(contents_to_write)

    
######################Search Neighberhood
def searchNeighbor():
    ########## Neighbor based
    list_parent = soup.find('div', class_='categories')
    manual_list = list_parent.find_all('div', class_ = 'row searchoption-cat hidden') 
    neighbor_list_tot = manual_list[0]
    neighbor_tags = neighbor_list_tot.find_all('a')

    l=len(neighbor_tags)
    m=0

    neighbor_store = []
    neighbor_name_store = []
    neighber_rest_address_dict={}
    for m in range(int(l)):
        neighbor_store.append(neighbor_tags[m]['href'])
        neighbor_name_store.append(neighbor_tags[m].contents[0])
    
    #print(neighbor_name_store)

    neighbor_name = []
    neighbor_address_list = []
    nei_dict = {}
    num = 0
    for nlink in neighbor_store:
        #link = cuisine_store[4]
        courses_page_url2 = BASE_URL + nlink
        response2 = make_url_request_using_cache(courses_page_url2,CACHE_DICT)
        soup_neighbor = BeautifulSoup(response2, 'html.parser')
        list_parent2 = soup_neighbor.find('div', class_='col-md-9 col-md-push-3 col-sm-12 records')
    
        neighbor_list = list_parent2.find_all('li')
        #print(neighbor_list)
        if len(neighbor_list)==0:
            nei_dict[neighbor_name_store[num]] = []
        else:

            for z in range(len(neighbor_list)):
                neighbor_resturant_link = neighbor_list[z].find_all('a')[1]
                neighbor_url = neighbor_resturant_link['href']   ##resturant url
                resturant_name_store = neighbor_resturant_link.find_all('h3')[0].text
                
                try:
                    neighber_rest_list = nei_dict[neighbor_name_store[num]]
                except:
                    neighber_rest_list = []
                neighber_rest_list.append(resturant_name_store)
                nei_dict[neighbor_name_store[num]] = neighber_rest_list
                x=neighbor_list[z].findAll('div')[0].text
                list1 = x.split('.')
                for i in range(len(list1)):
                    list1[i] = list1[i].strip("\n   ")
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
                neighbor_address_list.append(address)
                neighber_rest_address_dict[resturant_name_store] = address                
                
              
        num=num+1
    #print(nei_dict)
    root=TreeNode("neighber")
    resturant_keys = list(nei_dict.keys())
    for neighber_sets in range(len(resturant_keys)):
        neighber_tree = TreeNode(resturant_keys[neighber_sets]) #corresponding to type of cuisine
        
        for resturants in nei_dict[resturant_keys[neighber_sets]]:
            #cuisine_tree.add_child(TreeNode(resturants)) #corresponding to all of resturants in this cuisine
            n2= TreeNode(resturants)
            node = TreeNode(neighber_rest_address_dict[resturants])
            n2.add_child(node)
            neighber_tree.add_child(n2)
        root.add_child(neighber_tree)
    
    cache_file = open('H:\course_materials\graduate\SI_507\SI507\Final_project\eighber.json', 'w')
    contents_to_write = json.dumps(root.to_dict(),indent=4)
    #print(contents_to_write)
    cache_file.write(contents_to_write)
     








if __name__=="__main__": 
    searchCuisine()
    searchNeighbor()



    
