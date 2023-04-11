#!/usr/bin/env python
# coding: utf-8

# # Data Visualizations Project - Stock Market Notifications System (Email, SMS and Telegram)
# 
# 
# The world is changing and while the world economies keep on growing. People epsecially youths and students struggle to pay their bills. As students we wanted to have at least a passive income and because we are working towards our goal to become data scientists we thought it would be much better to invest in stock market mainly tech stocks. Is there any problem with that? Definitely no but this game requires time and so we came out with a notification system which will help us to only focus on the investing/trading strategy.
# 
# Project developed by:
# 
# - Johnas Chami, number: 20220723
# 
# - Mbagwu Ozichi, number: 20220725
# 
# - Seyram Nkulenu, number: 20221380 
# 
# - Wai Kong Ng, number: 20221384

# <div class="alert alert-block alert-info">
# 
# # Index
#     
# [1. Imports](#1)<br>
#     
# - [1.1 Import the needed Libraries](#1.1)<br>
# 
# - [1.2 Import the Dataset](#1.2)<br>
# 
# [2. Exploratory Data Analysis](#2)<br>
#     
# - [2.1 Data Exploration](#2.1)<br>
#     
# - [2.2 Data Pre-processing](#2.2)<br>
#    
# - [2.3 Data Visualization](#2.2)<br>
# 
# [3. Create the APP and the Notifications System](#3)<br>
# 
# - [3.1 Email and SMS Notifications](#3.1)<br>
#     
# - [3.2 Telegram Notifications](#3.2)<br>
#     
# 
# </div>

# <a class="anchor" id="1">
# 
# # 1. Imports
# 
#  </a> 

# <a class="anchor" id="1.1">
# 
# ## 1.1 Import the needed Libraries
# 
#  </a> 

# In[1]:


import os 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
    
from fmp_python.fmp import FMP                                   # for financial API:  pip install fmp-python
import smtplib                                                   # for sending emails
from email.message import EmailMessage                           # for sending emails

from dash import Dash, dcc, html, Output, Input, State           # pip install dash
import plotly.express as px                               
from datetime import datetime
import plotly.graph_objects as go
import plotly.io as pio

import telepot                                               
import requests 
from datetime import datetime
from timeloop import Timeloop
from datetime import timedelta


# <a class="anchor" id="1.2">
# 
# ## 1.2 Import the Dataset
#     
# </a>

# In[2]:


# Import the dataset and check it

ticker_list = pd.read_csv('project.csv')
ticker_list


# <a class="anchor" id="2">
# 
# # 2. Exploratory Data Analysis
#     
# </a>

# <a class="anchor" id="2.1">
# 
# ## 2.1. Data Exploration
#     
# </a>

# In[3]:


# Check the shape of the dataset
ticker_list.shape


# In[4]:


# Checking if there are only unique values in "Industry"
ticker_list['Industry'].unique()


# In[5]:


# Checking if there are only unique values in "Sector"
ticker_list['Sector'].unique()


# In[6]:


# Check the information about the dataframe and its features

ticker_list.info()


# In[7]:


# Checking the descriptive statistics of the categorical features
ticker_list.describe(include="object").T


# In[8]:


# Checking the top and the meast Country

ticker_list["Country"].value_counts() 


# In[9]:


ticker_list['Last Sale'].dtype


# <a class="anchor" id="2.2">
# 
# ## 2.2 Data Pre-processing 
#     
# </a>

# In[10]:


# Rename a column 
ticker_list = ticker_list.rename(columns={'Last Sale': 'Last Sale($)'})
ticker_list


# In[11]:


# Remove the '$' sign from the 'Last Sale($)' column
ticker_list['Last Sale($)'] = ticker_list['Last Sale($)'].str.replace('$', '')

# Remove the '%' sign from the '% Change' column
ticker_list['% Change'] = ticker_list['% Change'].str.replace('%', '')

ticker_list


# In[12]:


# Convert the '% Change' column to a numeric data type
ticker_list['% Change'] = pd.to_numeric(ticker_list['% Change'], errors='coerce')


# <a class="anchor" id="2.3">
# 
# ## 2.3 Data Visualization
#     
# </a>

# In[13]:


data_choropleth = dict(type='choropleth',
                       locations=ticker_list['Country'],  #There are three ways to 'merge' your data with the data pre embedded in the map
                       locationmode='country names',
                       z=np.log(ticker_list['Volume']),
                       text=ticker_list['Country'],
                       colorscale='inferno'
                      )

layout_choropleth = dict(geo=dict(scope='world',  #default
                                  projection=dict(type='orthographic'
                                                 ),
                                  #showland=True,   # default = True
                                  landcolor='black',
                                  lakecolor='white',
                                  showocean=True,   # default = False
                                  oceancolor='azure'
                                 ),
                         
                         title=dict(text='World Stock Trade Map',
                                    x=.5 # Title relative position according to the xaxis, range (0,1)
                                   )
                         
                        )


# In[14]:


fig_choropleth = go.Figure(data=data_choropleth, layout=layout_choropleth)

fig_choropleth.update_layout(
    plot_bgcolor='rgb(240, 240, 240)',
    paper_bgcolor='#f5f5f7'
)

fig_choropleth.show()


# In[15]:


# Group the data by industry and calculate the mean of the '% Change' column
mean_pct_change_by_industry = ticker_list.groupby('Industry')['% Change'].mean()

# Print the result
print(mean_pct_change_by_industry)


# In[16]:


# create a bar chart
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(mean_pct_change_by_industry.index, mean_pct_change_by_industry.values)
ax.set_xlabel('Industry')
ax.set_ylabel('Average % Change')
ax.set_title('Average % Change by Industry')
plt.xticks(rotation=90)
plt.show()


# In[17]:


# Group the data by industry and calculate the mean of the 'Volume' column
mean_volume_by_industry = ticker_list.groupby('Industry')['Volume'].mean()

# Print the result
print(mean_volume_by_industry)


# In[18]:


# create a bar chart
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(mean_volume_by_industry.index, mean_volume_by_industry.values)
ax.set_xlabel('Industry')
ax.set_ylabel('Average Volume')
ax.set_title('Average Volume by Industry')
plt.xticks(rotation=90)
plt.show()


# In[19]:


#Lets focus on a particular sector

sunburst_df = ticker_list.loc[ticker_list['Sector'] == 'Technology'].dropna()
#All values to be used in the plot independent to their position in the plot itself (keep in mind their index is important)
labels = np.append(sunburst_df['Country'].unique(), sunburst_df['Name'].values)

#For each index in the labels array you should choose a parent(inner circle), when the label refers to a 'parent' itself you put an empty value
parents = np.append([ '' for _ in range(len(sunburst_df['Country'].unique()))], sunburst_df['Country'].values)

#Values to be displayed when hovered over each label (company name and the market value)
values = np.append([ticker_list.loc[ticker_list['Country'] == _ ]['Market Cap'].sum() for _ in sunburst_df['Country'].unique()] , sunburst_df['Market Cap'])

#Since the data points have a big discrepancy between them, lets apply a log to them for this particular visualization
values = np.log(values)


#Construction of this particular graph(Sunburst)
sunburst_data = dict(type='sunburst', 
                     labels=labels, 
                     parents=parents, 
                     values=values)

#As the name hints the layout_margin defines the empty space on the top, left, right and below respectively of the graphs margins

sunburst_layout = dict(title="Market Capitalization by Countries",
                       title_x=0.5,
    margin=dict(t=100, l=100, r=100, b=100))


sunburst = go.Figure(data=sunburst_data, layout=sunburst_layout)
sunburst.update_layout(
    plot_bgcolor='rgb(240, 240, 240)',
    paper_bgcolor='#f5f5f7'
)
sunburst.show()


# <a class="anchor" id="3">
# 
# # 3. Create the APP and the Notifications System
# 
#  </a>

# <a class="anchor" id="3.1">
# 
# ## 3.1 Email and SMS Notifications
# 
#  </a> 

# In[20]:


def send_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = 'johnasc96@gmail.com'                                                   # email <-- Update here
    msg['from'] = user
    password = 'wcclgjnjmbcjmydo'                                                  # password from gmail <-- Update here

      # set server parameters
    server = smtplib.SMTP ('smtp.gmail.com', 587)                                  # create server variable
    server.starttls()
    server.login(user,password)
    server.send_message(msg)

    server.quit()


# In[79]:


app = Dash(__name__)
app.layout = html.Div([
    html.H1("Stock Market Notification System (Email and SMS)", style={'textAlign': 'center'}),
    dcc.Interval(id='trigger', interval=1000*10),
    dcc.Dropdown(id='ticker-name', options=ticker_list['Symbol'], value='MSFT', clearable=False, style={'width': '50%','borderRadius': '5px', 'borderColor': 'blue', 'borderWidth': '2px', 'padding': '10px'}),
    html.Div(id='price-placeholder', children=[]),
    dcc.Graph(id='line-history', figure={}),
    html.Hr(),
    html.Div('Would you like to set up email or phone alerts for price changes?'),
    dcc.RadioItems(id='alert-permission', options=['No','Yes, email alerts', 'Yes, phone alerts'], value='No'),
    html.Div('Alert me when share price is equal or above:',) ,
    dcc.Input(id='alert-value', type='number', min=0, max=1000, value=0,     style={
        'borderRadius': '5px',  # Set the border radius to 5 pixels
        'borderColor': 'blue',  # Set the border color to blue
        'borderWidth': '2px',  # Set the border width to 2 pixels
        'padding': '10px'  # Add some padding to the input box
    }),
    dcc.Graph(id='choropleth-map', figure=fig_choropleth, style={'height': '100vh'} ),  # Add the choropleth map here
    dcc.Graph(id='sunburst-plot', figure=sunburst, style={'height': '100vh'}),  # Add the sunburst plot here

])


# In[80]:


@app.callback(
    Output('line-history', 'figure'),
    Output('price-placeholder', 'children'),
    Input('trigger', 'n_intervals'),
    Input('ticker-name', 'value'),
    State('alert-permission', 'value'),
    State('alert-value', 'value'),
)
def display_price(_, ticker_name, alert_permission, alert_value):
    fmp = FMP(output_format='pandas', api_key='627aaecb52f1f08e5ddda8a4490ef225')                          # <-- Update here-------------------
    stock = fmp.get_quote_short(ticker_name)
    stock_history = fmp.get_historical_chart('1hour', ticker_name)
    current_time = datetime.now().strftime("%H:%M:%S")

    if alert_permission == 'Yes, phone alerts':
        if stock.price[0] >= alert_value:
            send_alert('Alert: Buy Stock',
                        f'{ticker_name} passed your alert threshold of ${alert_value} '
                        f'and is now at ${stock.price[0]} per share.',
                        '351914172220@sms.vodafone.pt')                                                  # <-- Update here-------------------

    elif alert_permission == 'Yes, email alerts':
        if stock.price[0] >= alert_value:
            send_alert('Alert: Buy Stock',
                        f'{ticker_name} passed your alert threshold of ${alert_value} '
                        f'and is now at ${stock.price[0]} per share.',
                        'EmailToAddress@gmail.com')                                              # <-- Update here-------------------

    history_fig = px.line(stock_history, x='date', y='high')
    return history_fig, html.Pre(f"Time: {current_time}\nPrice: ${stock.price[0]}")


# In[ ]:


if __name__ == '__main__':
    app.run()


# <a class="anchor" id="3.2">
# 
# ## 3.2 Telegram Notifications
# 
#  </a> 

# In[24]:


# Define a Python function to get real time stock data
# This function will accept one input ticker as its parameter

def getStockData(ticker):
    base_url = "https://financialmodelingprep.com/api/v3/quote/"     # Split the HTTP request URL into three parts so that we can build a dynamic API request URL based on the input ticker and individual API key.
    key = "627aaecb52f1f08e5ddda8a4490ef225"
    full_url = base_url + ticker + "?apikey=" + key
    r = requests.get(full_url)                                       # Use the Python requests module to get the real time stock data via the FMP API request URL and return the data in JSON format.
    stock_data= r.json()
    return stock_data


# In[25]:


def generateMessage(data):
    symbol = data[0]['symbol']
    price = data[0]["price"]
    changesPercent = data[0]["changesPercentage"]
    timestamp = data[0]['timestamp']
    
    current = datetime.fromtimestamp(timestamp)
    message = str(current)
    message += "\n" + symbol 
    message += "\n$" + str(price)
    
    if(changesPercent < -2):
        message += "\nWarning! Price drop more than 2%!"
        
    return message


# In[26]:


def sendMessage(text):
    token = '6138788409:AAFVqj5EETnfvfqs47SPgV5ZAK-nS1cDMP8'
    receiver_id = 5817562148      #In Numeric Format
    bot = telepot.Bot(token)
    bot.sendMessage(receiver_id,text)


# In[27]:


tl = Timeloop()

# Define a list of tickers for the top 50 tech stocks
tickers = ["AAPL", "MSFT", "AMZN", "GOOG", "FB", "TSLA", "NVDA", "PYPL", "INTC", "ASML", "NFLX", "ADBE", "CRM", "CSCO", "AVGO", "ORCL", "TXN", "SHOP", "SQ", "BIDU", "SE", "JD", "VMW", "IBM", "AMD", "MU", "NOW", "UBER", "LRCX", "ADI", "SNPS", "TEL", "SAP", "QCOM", "TEAM", "KLAC", "CRWD", "SNOW", "MELI", "OKTA", "ANSS", "FTNT", "CDNS", "DDOG", "ZS", "TWLO", "PANW", "WDAY", "DOCU", "NET"]

@tl.job(interval=timedelta(seconds=60))
def run_tasks():
    for ticker in tickers:
        # Get real-time stock data using FMP API
        api_key = "627aaecb52f1f08e5ddda8a4490ef225"
        url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={api_key}"
        response = requests.get(url)
        real_time_data = response.json()

        # Generate message for the stock
        textMessage = generateMessage(real_time_data)

        # Send message using appropriate method
        sendMessage(textMessage)

tl.start(block=True)


# In[ ]:




