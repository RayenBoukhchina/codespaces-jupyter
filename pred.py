#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
# Load the dataset
file_path = r"C:\Users\najar\Downloads\PV_Elec_Gas3.csv"
data = pd.read_csv(file_path)


# In[2]:


data


# In[3]:


data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y')


# In[4]:


#creating a new feature that seems useful for plotting
data['Daily Production'] = 0  # or any other initial value

data['Daily Production'] = data['Cumulative_solar_power'].diff()


# In[5]:


start_date = pd.to_datetime('01/01/2012', format='%d/%m/%Y')
end_date = pd.to_datetime('30/12/2019', format='%d/%m/%Y')
data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
plt.figure(figsize=(14, 7))
plt.stem(data['date'], data['Daily Production'], use_line_collection=True)
plt.title('Daily Solar Power Production')
plt.xlabel('date')
plt.ylabel('Daily Production (kWh)')
plt.grid(True)
# Set the correct date format on the x-axis
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d/%m/%Y'))
plt.gcf().autofmt_xdate()
plt.show()


# In[9]:


# Load the weather dataset
weather_file_path = r"C:\Users\najar\Downloads\weather_in_Antwerp.csv\weather_in_Antwerp.csv"
weather_data = pd.read_csv(weather_file_path, delimiter=';')


# In[10]:


weather_data


# In[11]:


# Extract all unique values from the 'Weather' column
unique_weather_conditions = weather_data['weather'].unique()

# Print the unique weather conditions
print(unique_weather_conditions)


# In[12]:


import re




# Function to clean weather descriptions
#deleting the rain/snow (precipitations in general) information if it exists
def clean_weather(description):
    if pd.isna(description):
        return description
    # Split at the first period
    parts = description.split('.', 1)
    if len(parts) > 1 and parts[1].strip():  # Check if the second part is non-empty
        return parts[1].strip()  # Return the part after the first period without adding a period
    else:
        return description  # Return the original description if no useful part after the period


# In[15]:


weather_data['weather'] = weather_data['weather'].apply(clean_weather)


# In[16]:


weather_data


# In[17]:


weather_data.dropna(subset=['weather'], inplace=True)


# In[18]:


# Count occurrences of each unique weather description and sort
weather_counts = weather_data['weather'].value_counts()

# Print each weather condition with its count
for condition, count in weather_counts.items():
    print(f"{condition}: {count}")


# In[19]:


weather_data = weather_data[~weather_data['weather'].isin([
    'Sandstorm.', 'Mild.', 'Quite Cool.', 'Haze.', 'Light fog', 'Frigid.', 
    'Cloudy.', 'Dense fog.', 'Cold.', 'More clouds than sun.', 'Light fog.', 'Chilly.', 'Cool.'
])]


# In[20]:


duplicated_dataset = weather_data.copy()
# Create a 'Date' column by combining 'year', 'month', and 'day'
duplicated_dataset['Date'] = pd.to_datetime(duplicated_dataset[['year', 'month', 'day']])

# Drop the original 'year', 'month', and 'day' columns
duplicated_dataset= duplicated_dataset.drop(columns=['year', 'month', 'day'])


# In[21]:


print(duplicated_dataset.columns)


# In[22]:


# Function to clean temperature and similar columns
def clean_numeric_column(column):
    return pd.to_numeric(column.str.replace(r'[^\d.]+', '', regex=True), errors='coerce')

# Clean the relevant columns
duplicated_dataset['temp'] = clean_numeric_column(duplicated_dataset['temp'])
duplicated_dataset['wind'] = clean_numeric_column(duplicated_dataset['wind'])
duplicated_dataset['visibility'] = clean_numeric_column(duplicated_dataset['visibility'])
duplicated_dataset['humidity'] = clean_numeric_column(duplicated_dataset['humidity'])


# In[23]:


# Group by date and calculate daily means
daily_weather = duplicated_dataset.groupby('Date').agg({
    'temp': 'mean',
    'wind': 'mean',
    'visibility': 'mean',
    'humidity': 'mean',
    
}).reset_index()


# In[24]:


daily_weather


# In[25]:


# Convert 'Date' column in 'daily_weather' to datetime
daily_weather.loc[:, 'Date'] = pd.to_datetime(daily_weather['Date'])
# merging both dataframes in order to have a closer look on the correlation/causality between weather features and the outputs of the solar panels
merged_data = pd.merge(daily_weather, data, left_on='Date', right_on='date', how='inner')  


# In[26]:


# Group by average temperature and calculate average production
average_production_by_temp = merged_data.groupby('temp')['Daily Production'].mean().reset_index()

# Plotting average production against temperature
plt.figure(figsize=(10, 6))
plt.plot(average_production_by_temp['temp'], average_production_by_temp['Daily Production'], marker='o', linestyle='-', color='b')

plt.title('Average Daily Production by Average Daily Temperature')
plt.xlabel('Average Temperature (°C)')
plt.ylabel('Average Production')
plt.grid()
plt.tight_layout()
plt.show()


# In[27]:


# Define a dictionary with sunny scores, thus changing categorical variables to numerical ones
sunny_order = {
    'overcast': 1,
    'ice fog': 2,
    'fog': 3,
    'low clouds': 4,
    'broken clouds': 5,
    'mostly cloudy': 6,
    'partly cloudy': 7,
    'partly sunny': 8,
    'scattered clouds': 9,
    'passing clouds': 10,
    'clear': 11,
    'sunny': 12
}


# In[ ]:
