#!/usr/bin/env python
# coding: utf-8

# ### Importing necessary libraries

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# ### Reading the excel file into a pandas dataframe

# In[2]:


birdstrike = pd.read_excel("Bird Strikes data.xlsx")
birdstrike.head()


# ### Checking for null values

# In[3]:


birdstrike.isnull().sum()


# ### Taking Care of null values

# In[4]:


birdstrike["Effect: Indicated Damage"].replace(to_replace=['No damage', 'Caused damage'], value=[0, 1],inplace=True)
birdstrike["Pilot warned of birds or wildlife?"].replace(to_replace=['N', 'Y'], value=[0, 1],inplace=True)
birdstrike["Effect: Impact to flight"] = birdstrike["Effect: Impact to flight"].fillna("No Impact")
birdstrike["Conditions: Precipitation"] = birdstrike["Conditions: Precipitation"].fillna("No Precipitation")


# ### Drop Remarks Column and null value rows for better analysis

# In[5]:


birdstrike = birdstrike.drop("Remarks",axis=1)
birdstrike = birdstrike.dropna()
birdstrike.describe()


# In[6]:


birdstrike.info()


# ### Add a Year column for segregation on the basis of year

# In[7]:


birdstrike["Year"] = birdstrike["FlightDate"].dt.year
birdstrike.head()


# ### Group the data Year wise

# In[8]:


yearwise_birdstrike = birdstrike.groupby("Year")["Record ID"].count().reset_index()
yearwise_birdstrike.rename(columns = {"Record ID":"No. of Birdstrikes"},inplace=True)
yearwise_birdstrike.head()


# ### Visuals depicting the number of Bird Strikes Yearly

# In[9]:


plt.bar(yearwise_birdstrike["Year"],yearwise_birdstrike["No. of Birdstrikes"])
plt.xlabel("Year")
plt.ylabel("No. of Birdstrikes")
plt.title("Year Wise distribution of Birdstrikes")
plt.show()


# ### Statewise segregation of the data

# In[10]:


statewise_birdstrike = birdstrike.groupby("Origin State")["Record ID"].count().reset_index()
statewise_birdstrike.rename(columns = {"Record ID":"No. of Birdstrikes"},inplace=True)
statewise_birdstrike.head()


# ### Bar Chart depicting number of Bird Strikes State wise

# In[11]:


plt.figure(figsize=(13,5),dpi=80)
plt.bar(statewise_birdstrike["Origin State"],statewise_birdstrike["No. of Birdstrikes"])
plt.xlabel("Origin State",fontsize=13)
plt.xticks(rotation=90)
plt.ylabel("No. of Birdstrikes",fontsize=13)
plt.title("State Wise distribution of Birdstrikes",fontsize=15)
plt.show()


# ### Top 10 US Airlines in terms of having encountered Bird Strikes

# In[12]:


airlinewise_birdstrike = birdstrike.groupby("Aircraft: Airline/Operator")["Record ID"].count().reset_index()
airlinewise_birdstrike.rename(columns = {"Record ID":"No. of Birdstrikes"},inplace=True)
airlinewise_birdstrike = airlinewise_birdstrike.sort_values("No. of Birdstrikes",ascending=False)
airlinewise_birdstrike.head(10)


# ### Airports with the most incidents of Bird Strikes - Top 50

# In[13]:


airportwise_birdstrike = birdstrike.groupby("Airport: Name")["Record ID"].count().reset_index()
airportwise_birdstrike.rename(columns = {"Record ID":"No. of Birdstrikes"},inplace=True)
airportwise_birdstrike = airportwise_birdstrike.sort_values("No. of Birdstrikes",ascending=False)
airportwise_birdstrike.head(50)


# ### Yearly Cost incurred due to Bird Strikes and Visualising it

# In[14]:


yearwise_cost = birdstrike.groupby("Year")["Cost: Total $"].sum().reset_index()
yearwise_cost.head()


# In[15]:


plt.bar(yearwise_cost["Year"],yearwise_cost["Cost: Total $"])
plt.xlabel("Year")
plt.ylabel("Total Cost (tens of millions $)")
plt.title("Year Wise Cost distribution due to Birdstrikes")
plt.show()


# ### Phase of the flight during most of the Bird Strikes

# In[16]:


flightphase_birdstrike = birdstrike.groupby("When: Phase of flight")["Record ID"].count().reset_index()
flightphase_birdstrike.rename(columns = {"Record ID":"No. of Birdstrikes"},inplace=True)
flightphase_birdstrike.sort_values("No. of Birdstrikes",ascending=False)


# ### Binary Altitude during Bird Strikes

# In[17]:


altitudebin_birdstrike = birdstrike.groupby("Altitude bin")["Record ID"].count().reset_index()
altitudebin_birdstrike.rename(columns = {"Record ID":"No. of Birdstrikes"},inplace=True)
altitudebin_birdstrike.head()


# ### Average altitude of aeroplanes in different phases at the time of the strike

# In[18]:


phase_altitude = birdstrike.groupby("When: Phase of flight")["Feet above ground"].mean().reset_index()
phase_altitude.head()


# ### Whether the Bird Strike Caused Damage and Visualising it

# In[19]:


indicated_damage = birdstrike.groupby("Effect: Indicated Damage")["Record ID"].count().reset_index()
indicated_damage.rename(columns = {"Record ID":"No. of Birdstrikes"},inplace=True)
indicated_damage.head()


# In[20]:


plt.subplot(1,2,1)
plt.pie(indicated_damage["No. of Birdstrikes"],labels=["No Damage","Caused Damage"])
plt.title("Pie Chart")
plt.subplot(1,2,2)
plt.bar(indicated_damage["Effect: Indicated Damage"],indicated_damage["No. of Birdstrikes"])
plt.xlabel("Damage Caused or Not")
plt.ylabel("Count")
plt.title("Bar Chart")
plt.tight_layout()
plt.show()


# ### Bird Strike Impact on flight and visualising it

# In[21]:


impact_birdstrike = birdstrike.groupby("Effect: Impact to flight")["Record ID"].count().reset_index()
impact_birdstrike.rename(columns = {"Record ID":"No. of Birdstrikes"},inplace=True)
impact_birdstrike.head()


# In[22]:


plt.bar(impact_birdstrike["Effect: Impact to flight"],impact_birdstrike["No. of Birdstrikes"])
plt.xticks(rotation=45)
plt.xlabel("Impact on flight")
plt.ylabel("No. of Birdstrikes")
plt.title("Impact on flight vs the No. of Birdstrikes")
plt.show()


# ### Effect of Strike at different altitudes

# In[23]:


plt.scatter(birdstrike["Effect: Impact to flight"],birdstrike["Feet above ground"])
plt.xlabel("Impact on Flight")
plt.ylabel("Altitude")
plt.xticks(rotation=60)
plt.show()


# #### We can notice from the above scatterplot that there are no engine failures and aborted flights at high altitude whereas planes on low altitude suffer all kinds of impacts

# ### Were pilots Informed and its effect on Impact ?

# In[24]:


birdstrike["Pilot warned of birds or wildlife?"].value_counts()


# In[25]:


pilots_warned = birdstrike.groupby("Effect: Impact to flight")["Pilot warned of birds or wildlife?"].sum().reset_index()
pilots_warned.head()


# In[26]:


pilots_not_warned = birdstrike.groupby("Effect: Impact to flight")["Pilot warned of birds or wildlife?"].count().reset_index()
pilots_not_warned.head()


# In[27]:


pilot_warning = pd.merge(pilots_warned,pilots_not_warned,on="Effect: Impact to flight")
pilot_warning["Not Warned"]=pilot_warning["Pilot warned of birds or wildlife?_y"]-pilot_warning["Pilot warned of birds or wildlife?_x"]
pilot_warning.rename(columns={"Pilot warned of birds or wildlife?_x":"Warned"},inplace=True)
pilot_warning.drop("Pilot warned of birds or wildlife?_y",axis=1,inplace=True)
pilot_warning


# In[28]:


width=0.40
x=np.arange(5)
plt.bar(x-0.2,pilot_warning["Warned"],width,label="Warned")
plt.bar(x+0.2,pilot_warning["Not Warned"],width,label="Not Warned")
plt.legend()
plt.title("Effect on Impact if Pilot was warned")
plt.ylabel("No. of Bird Strikes")
plt.xlabel("Pilot Warned or Not")
plt.xticks(x,labels=pilot_warning["Effect: Impact to flight"],rotation = 45)
plt.show()


# #### We can notice that there are less incidents of an Impact if the pilot was Warned.
