from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
from datetime import *

search_1 = "monitor"

url = "https://seattle.craigslist.org/search/sss?query={}&sort=rel".format(search_1)
# request to server to let us retrieve data from the web page
src = requests.get(url)
# get HTML of the page
results = src.content
# converting HTML to more readable format
soup = BeautifulSoup(results,'lxml')
# finding all classes that match "result-info" to get information on all posts in the page
front_page_results = soup.find_all(class_='result-info')

# lists that store post data
title_list = []
price_list = []
date_list = []
location_list = []
href_list = []


# get title, price, date, and location of the post and save to their respective lists
post_num = 0
for post in range(len(front_page_results)):
    try: # retrieving title data
        title = front_page_results[post].find(class_='result-title hdrlnk').get_text()
        title_list.append(title)
    except:
        title_list.append("could not get title {}".format(post_num))
    try: # retrieving price data
        price = front_page_results[post].find(class_='result-price').get_text()
        price_list.append(price)
    except:
        price_list.append("could not get price {}".format(post_num))
    try: # retrieving date data
        date = front_page_results[post].find(class_='result-date')
        first_split = str(date).split("datetime=", 1)[1]
        second_split = first_split.split("title", 1)[0][1:-2]
        date_object = datetime.strptime(second_split, '%Y-%m-%d %H:%M')
        date_list.append(date_object)
    except:
        date_list.append("could not get date {}".format(post_num))
    try: # retrieving location data
        location = front_page_results[post].find(class_='result-hood').get_text()
        location_list.append(location)
    except:
        location_list.append("could not get location {}".format(post_num))
    try: # retrieving post url
        href = front_page_results[post].find('a', href = True)['href']
        href_list.append(href)
    except:
        href_list.append("could not get href {}".format(post_num))
    post_num += 1

# creating a dictionary made from the data arrays for converting to pandas DataFrame
front_page_data = {
        'Title: ' : title_list,
        'Price: ' : price_list,
        'Date: ' : date_list,
        'Location: ' : location_list,
        'href: ' : href_list
}
# creating dataframe
df = pd.DataFrame(front_page_data)
# sort by datetime column
df = df.sort_values(by="Date: ")

# convert pandas dataframe columns back to Python arrays
title = df['Title: '].tolist()
price = df['Price: '].tolist()
date = df['Date: '].tolist()
location = df['Location: '].tolist()
href = df['href: '].tolist()

# print data to prompt
for i in range(70, 120):
    print("\n" + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    if (datetime.now() - date[i]).total_seconds() <= (60*10):
        print("                                     ---10 MINUTES AGO---")
    if (60*10) < (datetime.now() - date[i]).total_seconds() <= (60*30):
        print("                                     ---30 MINUTES AGO---")
    if (60*30) < (datetime.now() - date[i]).total_seconds() <= (60*60):
        print("                                     ---WITHIN THE HOUR---")
    if (60*60*6) < (datetime.now() - date[i]).total_seconds():
        print("                                     ---6+ Hours ago---")
    if "24\"" in title[i]:
        print("                                     ***24\"***")
    if "27\"" in title[i]:
        print("                                     ***27\"***")
    if "4k" in title[i].lower():
        print("                                     ***4K***")
    if "32\"" in title[i]:
        print("                                     ***32\"***")
    if "ultra" in title[i].lower():
         print("                                     ***ULTRAWIDE***")
    if int(price[i][1:]) <= 100:
        print("                                     ***CHEAP***")
    if 300 >= int(price[i][1:]) > 100:
        print("                                     ***IN PRICE RANGE***")
    print("\n")
    print("Title:     " + title[i])
    print("Price:     " + price[i])
    print("Date:      " + str(date[i]))
    print("Location: " + location[i])
    print("href:      " + href[i]+"\n" + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + "\n")

print("Time: " + str(datetime.now().hour) + ":" + str(datetime.now().minute))
