#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests


# In[5]:


requ = requests.get("https://en.wikipedia.org/wiki/Harvard_University")


# In[6]:


type(requ)


# In[7]:


dir(requ)


# In[8]:


page = requ.text


# In[9]:


page


# In[10]:


from bs4 import BeautifulSoup


# In[11]:


soup = BeautifulSoup(page, 'html.parser')


# In[12]:


soup


# In[13]:


soup.title


# In[15]:


soup.table["class"]


# In[16]:


[t["class"] for t in soup.find_all("table") if t.get("class")]


# In[17]:


table_html = str(soup.find_all("table", "wikitable")[2])


# In[18]:


from IPython.core.display import HTML
HTML(table_html)


# In[19]:


rows = [row for row in soup.find_all("table", "wikitable")[2].find_all("tr")]


# In[20]:


rows


# In[21]:


rem_nl = lambda s: s.replace("\n", "")


# In[22]:


columns = [rem_nl(col.get_text()) for col in rows[0].find_all("th") if col.get_text()]
columns


# In[23]:


indexes = [rem_nl(row.find("th").get_text()) for row in rows[1:]]

indexes


# In[24]:


to_num = lambda s: s[-1] =="%" and int(s[:-1]) or None 


# In[25]:


values = [to_num(rem_nl(value.get_text())) for row in rows[1:] for value in row.find_all("td")]
values


# In[26]:


stacked_values = zip(*[values[i::3] for i in range(len(columns))])
list(stacked_values)


# In[27]:


import pandas as pd


# In[28]:


stacked_values = zip(*[values[i::3] for i in range(len(columns))])
df = pd.DataFrame(stacked_values, columns=columns, index=indexes)
df


# In[29]:


columns = [rem_nl(col.get_text()) for col in rows[0].find_all("th") if col.get_text()] 
stacked_values = zip(*[values[i::3] for i in range(len(columns))])
data_dicts = [{col: val for col, val in zip(columns,col_values)} for col_values in stacked_values]
data_dicts


# In[30]:


df.dtypes


# In[31]:


df.dropna()


# In[32]:


dfnew = df.fillna(0).astype(int)
dfnew


# In[33]:


dfnew.describe()


# In[34]:


import numpy as np


# In[35]:


dfnew.values


# In[36]:


type(dfnew.values)


# In[37]:


np.mean(dfnew.Undergrad)


# In[38]:


dfnew['Undergrad']


# In[39]:


dfnew.loc["Asian/Pacific Islander"]


# In[40]:


dfnew.loc["Asian/Pacific Islander","Graduate"]


# In[41]:


seq_table = dfnew.stack().reset_index()
seq_table.columns = ["race", "source", "percentage"]
seq_table


# In[42]:


grouped_data = seq_table.groupby("race")
grouped_data.groups


# In[43]:


type(grouped_data)


# In[44]:


mean_table = grouped_data.mean()
mean_table


# In[45]:


for name, group in seq_table.groupby("source", sort=True):
  print(name)
  print(group)


# In[46]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[47]:


mean_table.plot(kind="bar")


# In[ ]:




