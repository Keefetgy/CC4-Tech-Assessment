#!/usr/bin/env python
# coding: utf-8

# In[96]:


import pandas as pd
import numpy as np
import json
import urllib.request
from datetime import datetime

Question 1
# In[106]:


url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
with urllib.request.urlopen(url) as response:
    data = json.load(response)


# In[98]:


#Converting the country code mapping to a dictionary
country_codes_df = pd.read_excel("Country-Code.xlsx")
country_codes_dict = country_codes_df.set_index('Country Code').to_dict()['Country']


# In[113]:


#
def extract_restaurant_data(restaurant):
    res_data = restaurant['restaurant']
    return {
        'Restaurant Id': res_data['R']['res_id'],
        'Restaurant Name': res_data['name'],
        'Country Code': res_data['location']['country_id'],
        'City': res_data['location']['city'],
        'User Rating Votes': int(res_data['user_rating']['votes']),
        'User Aggregate Rating': float(res_data['user_rating']['aggregate_rating']),
        'Cuisines': res_data['cuisines']
    }

restaurants_list = [extract_restaurant_data(restaurant) for page in data for restaurant in page['restaurants']]


# In[114]:


for restaurant in restaurants_list:
    # If the country code is not found, fill it up with 'NA' values
    restaurant['Country Code'] = country_codes_dict.get(restaurant['Country Code'], 'NA')
    
restaurants_df = pd.DataFrame(restaurants_list)
restaurants_df.rename(columns={'Country Code': 'Country'}, inplace=True)
restaurants_df.to_csv('restaurants.csv', index=False)

Question 2
# In[115]:


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

Question 3
# In[102]:


rating_thresholds = {
    'Excellent': float('inf'),
    'Very Good': float('inf'),
    'Good': float('inf'),
    'Average': float('inf'),
    'Poor': float('inf')
}

for page in data:
    for restaurant in page['restaurants']:
        rating_text = restaurant['restaurant']['user_rating']['rating_text']
        aggregate_rating = float(restaurant['restaurant']['user_rating']['aggregate_rating'])
        if rating_text in rating_thresholds:
            rating_thresholds[rating_text] = min(aggregate_rating, rating_thresholds[rating_text])
print(rating_thresholds)


# In[ ]:




