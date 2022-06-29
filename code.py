import requests
import time
from requests.structures import CaseInsensitiveDict
import pandas as pd
import numpy as np
import json
from os.path import exists
from pandas import json_normalize
import datetime
import csv
df_options = pd.DataFrame()
df_quote = pd.DataFrame()
#READING AS.CSV
AS = pd.read_csv('AS.csv')
#FILTERING AS with type==stock
AS = (AS[(AS['type']=='stock')])
symbols = AS['symbol']
#traversing the symbol column and for each symbol calling the API 
for symbol in symbols:
    print(symbol)
    url = "https://yfapi.net/v7/finance/options/"+symbol
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["X-API-KEY"] = "8gWOr0Pu5h8mtHMJ8l7pR6jTpKgKCriL9P6vKF2G"
    resp = requests.get(url, headers=headers) 
    resp = resp.json()
    #print(resp)
    # extracting calls puts and quote data from the entire response 
    calls = resp['optionChain']['result'][0]['options'][0]['calls'] 
    puts=resp['optionChain']['result'][0]['options'][0]['puts']
    quote = resp['optionChain']['result'][0]['quote']
    symbol
    #converting json to dataframe   
    df_calls = pd.json_normalize(calls)
    df_calls['strikeType'] = 'call'
    df_puts = pd.json_normalize(puts)
    df_puts['strikeType'] = 'put'
    df_puts['symbol'] = symbol
    df_calls['symbol'] = symbol
    df_options = pd.concat([df_options,df_calls,df_puts])
    #df_options = pd.concat([df_options,df_puts])
    
    df_curr = pd.json_normalize(quote)
    #adding a column state
    df_curr['state'] = 'current'
    #filtering out what is not required
    df_curr = df_curr.filter(['symbol','state','regularMarketTime','regularMarketPrice','regularMarketOpen','adjusted','marketCap','fiftyTwoWeekRange','twoHundredDayAverage','trailingPE','sharesOutstanding','forwardPE'])
    #renaming few columns 
    df_curr = df_curr.rename(columns = {'regularMarketTime':'dateTime','regularMarketPrice':'adjusted','regularMarketOpen':'Open'})
    df_quote = pd.concat([df_quote,df_curr])
    #doing the set up for v8 API call
    url2 = "https://yfapi.net/v8/finance/chart/"+symbol
    queryString={"range":'1mo',"interval":'1d',"events":"div,split"}
    #calling the API and getting the historical data into resp2
    resp2 = requests.get(url2, headers=headers,params=queryString)
    resp2 = resp2.json()
    resp2 = resp2['chart']['result'][0]
    #extracting meta from the response for getting the symbol value
    meta = resp2['meta']
    symbol = meta['symbol']
    #extracting the indicators data for getting 'close','open' and 'adjclose'
    indicators = resp2['indicators']
    #converting the timestamp list into a pandas series because it has to be
    #concatenated to the dataframe df_hist
    dateTime = pd.Series(resp2['timestamp'])
    #same with open data
    Open = pd.Series(indicators['quote'][0]['open'])
    #same with adjclose
    adjusted = pd.Series(indicators['adjclose'][0]['adjclose'])
    #combining all the pd series into one pandas dataframe df_hist 
    df_hist=pd.concat([dateTime,Open,adjusted], axis = 1, ignore_index = True)
    #reversing the whole dataframe so that datetime is in descending order
    df_hist=df_hist[::-1].reset_index(drop = True)
    df_hist.columns = ['dateTime','Open','adjusted']
    df_hist['symbol'] = symbol  
    #setting the state of data    
    df_hist['state'] = 'historical'
    #joining the current and historical data
    df_quote = pd.concat([df_quote,df_hist])
    
#converting the time format     
dateTime = np.vectorize(datetime.datetime.fromtimestamp, otypes=[np.ndarray])
df_options['expiration'] = dateTime(df_options['expiration'])
df_options['lastTradeDate'] = dateTime(df_options['lastTradeDate'])
df_quote['dateTime'] = dateTime(df_quote['dateTime'])
#writing the Dataframes into csv files         
df_quote.to_csv('quote.csv',mode = 'w',header = True,index = False)
df_options.to_csv('options.csv',mode = 'w',header = True,index = False)


        
