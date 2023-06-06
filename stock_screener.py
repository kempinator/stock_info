import numpy as np
import pandas as pd
import requests

params = {
  'access_key': '701faa54c5d092bd4e2f9b31d601a2c7'          #appreciate this would normally not be publicized, but it's a free account and this is listed privately                      
}
                            
ticker_dict = []                                            #initialising list for user-provided stock tickers (started life as a dictionary)
watch_list = ['MSFT','AMD','NVDA','AMZN','TSLA','CRSR']     #default watchlist created, which can be used in place of user giving same companies over and over
stock_data = []                                             #set of lists to contain data from differing dates, used to calculate performance over time
yest_data = []
week_data = []
month_data = []

def create_ticker_list():
    
    
    while True:
        ticker = input("Enter ticker - ").upper()     #ask for ticker from user
                                
        if ticker == '' or ticker.isspace():                       #if no input is detected
          cont = input('Are you finished? Enter Y/N').upper()      # has the user finished input
          if cont == 'Y':
            break
          elif cont =='N':
            continue
          else:
            continue
        elif ticker == 'WATCHLIST':             #if "watchlist" is entered, add defaults
            for i in watch_list:
                if i in ticker_dict:
                    pass
                else:
                    ticker_dict.append(i)
            break
            
        elif ticker in ticker_dict:                                       #in case of duplication
            print('Stock already added! /n Add another ')                 #inform user and do not add 
            continue
        else:
            ticker_dict.append(ticker)                                    # in every other instance, add ticker to list 
            continue
        
def percentage_change(today,previous):
    return (((today-previous)/today)*100)

def change_highlight(stock_df):            
    lower_limit = -3            #setting upper and lower limits for large price changes to highlight to user
    upper_limit = 3

    for i in range(len(stock_df.index)):
        if stock_df['day change'][i] <= lower_limit:                                 #if previous day change value less than lower limit
            print(f'{stock_df.index[i]} large drop of '+str(stock_df['day change'][i]),'%')                  #highlight as large price drop
        elif stock_df['day change'][i] >= upper_limit:                               # #if previous day change value more than higher limit
            print(f'{stock_df.index[i]} large gain of '+str(stock_df['day change'][i]),'%')                 #highlight as large price gain
        else:
            continue

create_ticker_list()          

for ticker in ticker_dict:
    try:
        
      api_result = requests.get(f'http://api.marketstack.com/v1/tickers/{ticker}/eod',params)   #retrieve data from marketstack using list of tickers
      api_response = api_result.json()                      #convert each in string form
      stock_data.append(api_response['data']['eod'][0])     #pluck latest trading day data
      yest_data.append(api_response['data']['eod'][1])      #Day before above trading day data
      week_data.append(api_response['data']['eod'][6])      #week prior
      month_data.append(api_response['data']['eod'][29])    #month prior      all used for calculating %change during time periods
    except:
        continue

fin_dat_frame = pd.DataFrame(stock_data)          #convert to all data into seperate data frames
yest_df = pd.DataFrame(yest_data)                 
week_df = pd.DataFrame(week_data)
month_df = pd.DataFrame(month_data)

fin_dat_frame.set_index('symbol',inplace=True)    #convert index of all data frames to ticker symbol for readability
yest_df.set_index('symbol',inplace=True)
week_df.set_index('symbol',inplace=True)
month_df.set_index('symbol',inplace=True)

fin_dat_frame['day change'] = np.vectorize(percentage_change)(fin_dat_frame['close'],yest_df['close']).round(2)   #calculate day change based on closed data between 2 dataframes, add new column to primary dataframe

fin_dat_frame['week change'] = np.vectorize(percentage_change)(fin_dat_frame['close'],week_df['close']).round(2)  #same as above for week performance

fin_dat_frame['Month Change'] =np.vectorize(percentage_change)(fin_dat_frame['close'],month_df['close']).round(2) #same as above for month performance


not_interested = ['date','split_factor','adj_high','adj_low','adj_close','adj_open','adj_volume','volume','exchange','dividend','open','high','low']        #unneccessary data points for my needs
stock_df = fin_dat_frame      #duplicate primary data frame for visual print use only
for i in not_interested:        #for all unneccessary data points
    try:
        stock_df.pop(i)         #remove from duplicated data frame
       
    except:
        continue                
        

print(stock_df)               #show simplified data drame
change_highlight(stock_df)    #print any large price changes in my stock list




