#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


data = pd.read_csv("Sssss.csv")


# In[3]:


data.head()


# In[4]:


data['Slot_Time'] = pd.to_datetime(data['Slot_Time'])
data.head()


# In[5]:


# data['Slot_Time'].dt.day
df1=data[data['Slot_Status']=='BOOKED']
# df1=df1[df1['Entity_ID']=='H0001']
df1


# In[6]:


df1 = df1[['Slot_Time','Slot_Status']]
df1


# df2

# In[7]:


df2=df1.groupby([df1['Slot_Time'].dt.year, df1['Slot_Time'].dt.month, df1['Slot_Time'].dt.day] ).count()


# In[ ]:





# In[8]:


df2.reset_index(drop=True)


# In[9]:


df2.reset_index(level='Slot_Time', col_level=1)



# In[10]:


df1['S_m'] = df1['Slot_Time'].dt.month


# In[11]:


df1['S_y'] = df1['Slot_Time'].dt.year


# In[12]:


df1['S_d'] = df1['Slot_Time'].dt.day


# In[13]:


df4 = df1[['Slot_Status','S_m','S_y','S_d']]


# In[14]:


df4


# In[15]:


df2=df4.groupby([df4['S_y'], df4['S_m'], df4['S_d']] ).count()
df2


# In[16]:


df3=df2.reset_index()
type(df3)
df3


# In[17]:


df3['Slot_time'] = df3['S_y'].astype(str).str.cat(df3['S_m'].astype(str), sep='-')


# In[18]:


df3['Slot_time'] = df3['Slot_time'].astype(str).str.cat(df3['S_d'].astype(str), sep='-')


# In[19]:


df3['Slot_time'] = pd.to_datetime(df3['Slot_time'])
df3


# In[20]:


df4 = df3[['Slot_time','Slot_Status']]


# In[21]:


df5=df4.set_index(['Slot_time'])
df5


# In[22]:


plt.plot(df5)


# In[23]:


roll_mean=df5.rolling(window=7).mean()


# In[24]:


roll_mean


# In[25]:


roll_std=df5.rolling(window=7).std()


# In[26]:


roll_std


# In[27]:


# fig = fig(fig)
orig = plt.plot(df5,color='blue',label='orginal')
mean = plt.plot(roll_mean,color='red',label='orginal')
std = plt.plot(roll_std,color='black',label='orginal')


# In[28]:


df5_log = np.log(df5)


# In[29]:


plt.plot(df5_log)


# In[30]:


roll_mean_log=df5_log.rolling(window=7).mean()


# In[31]:


roll_std_log=df5_log.rolling(window=7).std()


# In[32]:


orig = plt.plot(df5_log,color='blue',label='orginal')
mean = plt.plot(roll_mean_log,color='red',label='orginal')
std = plt.plot(roll_std_log,color='black',label='orginal')


# In[33]:


df5_log_minus_movAvg = df5_log - roll_mean_log


# In[34]:


df5_log_minus_movAvg.dropna(inplace=True)


# In[35]:


mean=df5_log_minus_movAvg.rolling(window=7).mean()
std=df5_log_minus_movAvg.rolling(window=7).std()


# In[36]:


orig = plt.plot(df5_log_minus_movAvg,color='blue',label='orginal')
mean = plt.plot(mean,color='red',label='orginal')
std = plt.plot(std,color='black',label='orginal')


# In[ ]:





# In[37]:


import statsmodels.tsa.stattools as adfuller


# In[38]:


# result = adfuller(X


# In[39]:


X=df5_log_minus_movAvg['Slot_Status']


# In[40]:


class StationarityTests:
    def __init__(self, significance=.05):
        self.SignificanceLevel = significance
        self.pValue = None
        self.isStationary = None
    def ADF_Stationarity_Test(self, timeseries, printResults = True):

        #Dickey-Fuller test:
        adfTest = adfuller(timeseries, autolag='AIC')
        
        self.pValue = adfTest[1]
        
        if (self.pValue<self.SignificanceLevel):
            self.isStationary = True
        else:
            self.isStationary = False
        
        if printResults:
            dfResults = pd.Series(adfTest[0:4], index=['ADF Test Statistic','P-Value','# Lags Used','# Observations Used'])

            #Add Critical Values
            for key,value in adfTest[4].items():
                dfResults['Critical Value (%s)'%key] = value

            print('Augmented Dickey-Fuller Test Results:')
            print(dfResults)


# In[41]:


sTest = StationarityTests()

print("Is the time series stationary? {0}".format(sTest.isStationary))


# In[42]:


type(X)


# In[58]:


sTest.ADF_Stationarity_Test(X, printResults = True)


# In[47]:


import statsmodels.tsa.stattools as acf,pacf_yw


# In[48]:


from statsmodels.graphics.tsaplots import plot_pacf


# In[49]:


from statsmodels.graphics.tsaplots import plot_acf


# In[50]:


plot_pacf(X)


# In[52]:


plot_acf(X)


# In[54]:


acf1 = stattools.acf(X)


# In[57]:


sc = acf()


# In[60]:


from statsmodels.tsa.arima_model import ARIMA


# In[61]:


model = ARIMA(X,order=(2,1,2))
result_AR = model.fit(disp=-1)


# In[63]:


plt.plot(X)
plt.plot(result_AR.fittedvalues,color='red')


# In[66]:


rss = sum((result_AR.fittedvalues)**2)


# In[67]:


rss


# In[68]:


from statsmodels.tsa.stattools import acf, pacf


# In[69]:


acf_l = acf(df5_log_minus_movAvg,nlags = 20) 


# In[70]:


pacf_l = pacf(df5_log_minus_movAvg,nlags = 20) 


# In[71]:


plt.plot(acf_l)


# In[72]:


plt.plot(pacf_l)


# In[109]:


model = ARIMA(df5,order=(2,1,2))
result = model.fit(disp=1)


# In[117]:


plt.plot(df5_log_minus_movAvg)
# plt.plot(result.fittedvalues,color='red')


# In[111]:


rss = sum((result.fittedvalues-df5_log_minus_movAvg)**2)


# In[125]:


t=(result.fittedvalues-df5_log_minus_movAvg['Slot_Status'])**2
c=sum(t.dropna())
c 


# In[115]:


df5_log_minus_movAvg


# In[142]:


result.plot_predict(1,330)


# In[136]:


result.forecast(steps=1)


# In[ ]:




