#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from arctic import Arctic
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import pandas as pd


# In[2]:


store = Arctic('localhost',27017)

# Create the library - defaults to VersionStore
store.initialize_library('NASDAQ')

# Access the library
library = store['NASDAQ']


# In[8]:


access_token = "baddfdfbbc5590fca2c248e4582f4b2a-c8632d39abd3e0b8b28002eb54e1598e"

client = oandapyV20.API(access_token=access_token)

params ={"count": 5000,"granularity": "M5"}


# In[9]:


r = instruments.InstrumentsCandles(instrument="DE30_EUR",params=params)
client.request(r)


# In[10]:


out=[]
out=pd.DataFrame(r.response['candles'])
df=pd.DataFrame(out)
print(df['mid'])


# In[11]:


objs = [df['mid'], pd.DataFrame(df['mid'].tolist()).iloc[:, :4]]
df2 = pd.concat(objs, axis=1).drop('mid', axis=1)
df2['time'] = df['time']
df2['volume'] = df['volume']
df2.columns=['Open','High','Low','Close','Timestamp','volume']


# In[12]:


print(df2)


# In[13]:


# Load some data - maybe from Quandl
aapl = df2
# Store the data in the library
library.write('Forex', aapl, metadata={'source': 'OANDA'})


# In[20]:


# Reading the data
item = library.read('Forex')
print(item)


# In[21]:


aapl = item.data
print(aapl)
metadata = item.metadata


# In[22]:


ohlc = []
ohlc=pd.DataFrame(aapl)
print(ohlc)


# In[29]:


ohlc.describe()


# In[31]:


import matplotlib.pyplot as plt
ohlc['Open']=ohlc['Open'].astype(float)


# In[32]:


ohlc['Open'].plot(grid=True)
plt.show()


# In[34]:


low = 50
high = 120
sign = pd.DataFrame(index=ohlc.index)


# In[35]:


sign['signal'] = 0.0


# In[36]:


sign['short'] = ohlc['Open'].rolling(window=low, min_periods=1,center=False).mean() 


# In[37]:


sign['long'] = ohlc['Open'].rolling(window=high, min_periods=1,center=False).mean()


# In[38]:


sign['signal'][low:]= np.where(sign['short'][low:]>sign['long'][low:],1.0,0.0)


# In[39]:


sign.fillna(0, inplace=True)
print(sign)


# In[40]:


sign['positions'] = sign['signal'].diff()
sign[sign['positions'] == -1.0]


# In[41]:


fig=plt.figure(figsize=(20,15))
ax1=fig.add_subplot(111)
ohlc['Open'].plot(ax=ax1,color='black', lw=2.)
sign[['short','long']].plot(ax=ax1, lw=2.)
ax1.plot(sign.loc[sign.positions==1.0].index,sign.short[sign.positions == 1.0],'^', markersize=20, color='g')
ax1.plot(sign.loc[sign.positions==-1.0].index,sign.short[sign.positions == -1.0],'v', markersize=20, color='r')
plt.show()


# In[ ]:




