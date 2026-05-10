#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
df = pd.read_csv('customer_shopping_behavior.csv')


# In[5]:


df.head()


# In[6]:


df.info()


# In[7]:


df.describe(include = 'all')


# In[8]:


df.isnull().sum()


# In[9]:


df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))


# In[10]:


df.isnull().sum()


# In[11]:


df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
df = df.rename(columns = {'purchase_amount_(usd)':'purchase_amount'})


# In[12]:


df.info()


# In[13]:


# create a new column age_group
df.columns = df.columns.str.strip()
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels = labels)


# In[14]:


df[['age','age_group']].head(10)


# In[15]:


# create column purchase frequency days
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)


# In[16]:


df[['purchase_frequency_days','frequency_of_purchases']].head(10)


# In[17]:


df[['discount_applied','promo_code_used']].head(10)


# In[18]:


(df['discount_applied'] == df['promo_code_used']).all()


# In[19]:


df = df.drop('promo_code_used', axis = 1)


# In[20]:


df.info()


# In[21]:


pip install sqlalchemy mysql-connector-python pandas


# In[25]:


get_ipython().system('pip install pymysql sqlalchemy')
get_ipython().system('pip install pymysql')
get_ipython().system('pip install cryptography pymysql')


# In[27]:


from sqlalchemy import create_engine

# MySQL connection
username = "root"
password = "password"
host = "localhost"
port = "3306"
database = "customer_behavior"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}",
    connect_args={"charset": "utf8mb4"}
)

# Write DataFrame to MySQL
table_name = "customer"   # choose any table name
df.to_sql(table_name, engine, if_exists="replace", index=False)

# Read back sample
pd.read_sql("SELECT * FROM customer LIMIT 5;", engine)


# In[ ]:




