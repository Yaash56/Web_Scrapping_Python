#!/usr/bin/env python
# coding: utf-8

# # Scraping Top Repositories for Topics on GitHub 
# 
# TODO :
#  1> Intro About The Web Scrapping
#  2> Intro about GitHub and Problem Statement
#  3> Tools Used(Python, requests,BeautifulSoup,Pandas)

# # Here are the steps which we followed:
# 
# 1> We're going to Scrape "https://github.com/topics"
# 2> We'll get list of topics For each topic we will get topic title , topic url ,topic discription
# 3> for each individual topic we will get its repo name , user name , stars and repo URL
# 4> For each topic we will create a CSV file 
# 
# # Scape the list of topics from GitHub
# - use requests to download the page
# - use BS4 to parse and extract information
# - convert to pandas dataframe
# 
# # Lets Write The Function To Download the page 

# In[127]:


import requests
from bs4 import BeautifulSoup
def get_topics_page():
    topics_url = 'https://github.com/topics'
    response = requests.get(topics_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    doc = BeautifulSoup(response.text, 'html.parser')
    return doc


# In[128]:


doc = get_topics_page()


# In[129]:


doc.find('a')


# # Lets create some helper function to parse information from the page
# 
# To get topic titles, we can pick 'p' tags with the 'class = f3 lh-condensed mb-0 mt-1 Link--primary'
# 
# ![](https://imgur.com/a/fpTKCcr.png)
# 

# In[131]:


def get_topic_titles(doc):
    selection_class ="f3 lh-condensed mb-0 mt-1 Link--primary"
    topic_title_tags = doc.find_all('p',{'class': selection_class})
    topic_titles =[]
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    return topic_titles



# - get_topic_titles Can be used to get the list of titles

# In[133]:


titles = get_topic_titles(doc)


# In[134]:


len(titles)


# In[135]:


titles[:5]


# Similarly we have defined function for description and URL

# In[137]:


def get_topic_desc(doc):
    
    desc_selector = 'f5 color-fg-muted mb-0 mt-1'
    topic_desc_tags = doc.find_all('p',{'class': desc_selector})
    topic_desc =[]
    for tag in topic_desc_tags:
        topic_desc.append(tag.text.strip())
    return topic_desc



# In[138]:


def get_topic_url(doc):
    topic_link_tags = doc.find_all('a' , {'class': 'no-underline flex-1 d-flex flex-column'})
    topic_url =[]
    base_url ='https://github.com'
    for tag in topic_link_tags:
        topic_url.append(base_url + tag['href'].strip())
    return topic_url


# In[ ]:





# Lets pull this all together into the single function 

# In[140]:


def scrape_topics():
    topics_url = 'https://github.com/topics'
    response = requests.get(topics_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    doc = BeautifulSoup(response.text, 'html.parser')
    topics_dict = {
        'title' : get_topic_titles(doc),
        'description' : get_topic_desc(doc),
        'url' :get_topic_url(doc)
    }
    return pd.DataFrame(topics_dict)


# In[141]:


base_url = 'https://github.com/'


# # Get the top 25 repositories from a topic page

# In[143]:


def get_topic_page(topic_url):
    response = requests.get(topic_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    return BeautifulSoup(response.text, 'html.parser')


# In[144]:


doc = get_topic_page('https://github.com/topics/3d')


# In[145]:


def get_repo_info(h3_tag, star_tag):
    # Returns required information about a repository
    a_tags = h3_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = base_url + a_tags[1]['href']
    stars = star_tag.text.strip()  # Remove any extra whitespace
    return username, repo_name, repo_url, stars


# In[146]:


import pandas as pd
def get_topic_repos(topic_doc):
    repo_tags = topic_doc.find_all('h3', {'class': 'f3 color-fg-muted text-normal lh-condensed'})
    star_tags = topic_doc.find_all('span', {'class': 'Counter js-social-count'})

    if len(repo_tags) < 20 or len(star_tags) < 20:
        raise Exception("Not enough repositories found on the page.")

    topic_repos_dict = {
        'username': [],
        'repo_name': [],
        'repo_url': [],
        'stars': []
    }
    for i in range(20):  # Fetch only the first 20 repositories
        info = get_repo_info(repo_tags[i], star_tags[i])
        topic_repos_dict['username'].append(info[0])
        topic_repos_dict['repo_name'].append(info[1])
        topic_repos_dict['repo_url'].append(info[2])
        topic_repos_dict['stars'].append(info[3])

    return pd.DataFrame(topic_repos_dict)


# In[147]:


def scrape_topic(topic_url ,path):
    topic_df = get_topic_repos(get_topic_page(topic_url))
    topic_df.to_csv(path + '.csv', index =None)
    


# In[ ]:





# # Putting It Together
# - We have the function to get list of topics
# - We have function to create a CSV File for scapped from topic page
# - lets create a function to put them together

# In[149]:


import os
def scrape_topics_repos():
    print('Scrapping list of topics ')
    topics_df = scrape_topics()
    os.makedirs('Data', exist_ok=True)
    for index, row in topics_df.iterrows():
        print('scrapping top repositories for"{}"'.format(row['title']))
        scrape_topic(row['url'],'Data/{}.csv'.format(row['title']))
        


# Lets run it to scrape the top repos for all the topics on the first page of 
# 'https://github.com/topics'

# In[151]:


scrape_topics_repos()


# # Thank You and here I conclude my short Web Scrapping Live Project 

# In[ ]:




