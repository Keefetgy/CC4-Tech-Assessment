#!/usr/bin/env python
# coding: utf-8

# In[85]:


import pandas as pd
import numpy as np
import json
import urllib.request
from datetime import datetime
#!pip install openpyxl


# In[14]:


url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
with urllib.request.urlopen(url) as response:
    data = json.load(response)


# In[46]:


country_codes_df = pd.read_excel("Country-Code.xlsx")
country_codes_dict = country_codes_df.set_index('Country Code').to_dict()['Country']


# In[82]:


def extract_restaurant_data(restaurant):
    return {
        'Restaurant Id': restaurant['restaurant']['R']['res_id'],
        'Restaurant Name': restaurant['restaurant']['name'],
        'Country Code': restaurant['restaurant']['location']['country_id'],
        'City': restaurant['restaurant']['location']['city'],
        'User Rating Votes': int(restaurant['restaurant']['user_rating']['votes']),
        'User Aggregate Rating': float(restaurant['restaurant']['user_rating']['aggregate_rating']),
        'Cuisines': restaurant['restaurant']['cuisines']
    }

restaurants_list = [extract_restaurant_data(restaurant) for page in data for restaurant in page['restaurants']]


# In[83]:


for restaurant in restaurants_list:
    # If the country code is not found, fill it up with 'NA' values
    restaurant['Country Code'] = country_codes_dict.get(restaurant['Country Code'], 'NA')
    
restaurants_df = pd.DataFrame(restaurants_list)
restaurants_df.rename(columns={'Country Code': 'Country'}, inplace=True)
restaurants_df.to_csv('restaurants.csv', index=False)

Task 2
# In[90]:


april_start = datetime(2019, 4, 1)
april_end = datetime(2019, 4, 30)

def is_event_in_april(event):
    start_date = datetime.strptime(event['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(event['end_date'], '%Y-%m-%d')
    return start_date <= april_end and end_date >= april_start

restaurant_events = []
for page in data:
    for restaurant in page['restaurants']:
        res_data = restaurant['restaurant']
        for z_event in res_data.get('zomato_events', []):
            event = z_event['event']
            if is_event_in_april(event):
                photo_url = event['photos'][0]['photo']['url'] if event.get('photos') else None
                restaurant_events.append({
                    'Event Id': event['event_id'],
                    'Restaurant Id': res_data['id'],
                    'Restaurant Name': res_data['name'],
                    'Photo URL': photo_url,
                    'Event Title': event['title'],
                    'Event Start Date': event['start_date'],
                    'Event End Date': event['end_date']
                })
restaurant_events = pd.DataFrame(restaurant_events)
restaurant_events.fillna("NA", inplace=True)
restaurant_events.to_csv('restaurant_events.csv', index=False)


# In[ ]:




