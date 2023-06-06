import numpy as np
import pandas as pd
import requests

params = {
  'access_key': '701faa54c5d092bd4e2f9b31d601a2c7'                         
}
                            
ticker_dict = []
watch_list = ['MSFT','AMD','NVDA','AMZN','TSLA','CRSR']
stock_data = []
yest_data = []
week_data = []
month_data = []

def create_ticker_list():
    
    
    while True:
        ticker = input("Enter ticker - ").upper()
        if ticker.isspace():
            break
        elif ticker == '':
            cont = input('Are you finished? Enter Y/N').upper()
            if cont == 'Y':
                break
            elif cont =='N':
                break
            else:
                continue
        elif ticker == 'WATCHLIST':
            for i in watch_list:
                if i in ticker_dict:
                    pass
                else:
                    ticker_dict.append(i)
            break
            
        elif ticker in ticker_dict:
            print('Stock already added! /n Add another ')
            continue
        else:
            ticker_dict.append(ticker)
            continue
        
def percentage_change(today,previous):
    return (((today-previous)/today)*100)

def change_highlight(stock_df):
    lower_limit = -3
    upper_limit = 3

    for i in range(len(stock_df.index)):
        if stock_df['day change'][i] <= lower_limit:
            print(f'{stock_df.index[i]} large drop of '+str(stock_df['day change'][i]),'%')
        elif stock_df['day change'][i] >= upper_limit:
            print(f'{stock_df.index[i]} large gain of '+str(stock_df['day change'][i]),'%')
        else:
            continue

create_ticker_list()

for ticker in ticker_dict:
    try:
        
      api_result = requests.get(f'http://api.marketstack.com/v1/tickers/{ticker}/eod',params)
      api_response = api_result.json()
      stock_data.append(api_response['data']['eod'][0])
      yest_data.append(api_response['data']['eod'][1])
      week_data.append(api_response['data']['eod'][6])
      month_data.append(api_response['data']['eod'][29])
    except:
        continue

fin_dat_frame = pd.DataFrame(stock_data)
yest_df = pd.DataFrame(yest_data)
week_df = pd.DataFrame(week_data)
month_df = pd.DataFrame(month_data)

fin_dat_frame.set_index('symbol',inplace=True)
yest_df.set_index('symbol',inplace=True)
week_df.set_index('symbol',inplace=True)
month_df.set_index('symbol',inplace=True)

fin_dat_frame['day change'] = np.vectorize(percentage_change)(fin_dat_frame['close'],yest_df['close']).round(2)

fin_dat_frame['week change'] = np.vectorize(percentage_change)(fin_dat_frame['close'],week_df['close']).round(2)

fin_dat_frame['Month Change'] =np.vectorize(percentage_change)(fin_dat_frame['close'],month_df['close']).round(2)


not_interested = ['date','split_factor','adj_high','adj_low','adj_close','adj_open','adj_volume','volume','exchange','dividend','open','high','low']
stock_df = fin_dat_frame
for i in not_interested:
    try:
        stock_df.pop(i)
       
    except:
        continue
        

print(stock_df)
change_highlight(stock_df)




