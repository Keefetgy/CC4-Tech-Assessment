#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import numpy as np
import json
import urllib.request
get_ipython().system('pip install openpyxl')


# In[14]:


url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
with urllib.request.urlopen(url) as response:
    data = json.load(response)


# In[46]:


country_codes_df = pd.read_excel("Country-Code.xlsx")
country_codes_df
country_codes_dict = country_codes_df.set_index('Country Code').to_dict()['Country']
country_codes_dict


# In[68]:


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


# In[72]:


for restaurant in restaurants_list:
    # If the country code is not found, use the 'City' value instead (for Dummy countries)
    restaurant['Country Code'] = country_codes_dict.get(restaurant['Country Code'], restaurant['City'])
    
restaurants_df = pd.DataFrame(restaurants_list)

restaurants_df.rename(columns={'Country Code': 'Country'}, inplace=True)
restaurants_df.to_csv('restaurants.csv', index=False)


# In[ ]:




