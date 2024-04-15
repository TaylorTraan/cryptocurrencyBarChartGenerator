from pycoingecko import CoinGeckoAPI
import pandas as pd
import plotly.graph_objects as go


cg = CoinGeckoAPI()

crypto = input('Enter crypto: ')
day = input('days to go back: ')

crypto_data = cg.get_coin_market_chart_by_id(id=crypto, vs_currency='usd', days=day)

crypto_price_data = crypto_data['prices']

data = pd.DataFrame(crypto_price_data, columns = ['Timestamp', 'Price'])

data['Date'] = pd.to_datetime(data['Timestamp'], unit='ms')

candlestick_data = data.groupby(data.Date.dt.date).agg({'Price':
    ['min', 'max', 'first', 'last']})

fig = go.Figure(data=[go.Candlestick(x= candlestick_data.index, 
                                     open=candlestick_data['Price']['first'],
                                     high=candlestick_data['Price']['max'],
                                     low=candlestick_data['Price']['min'],
                                     close=candlestick_data['Price']['last'],)
                      ])

fig.update_layout(xaxis_rangeslider_visible=False, xaxis_title='Date',
                  yaxis_title='Price (USD$)', title=f'{crypto.upper()} Candlestick Chart Over Past 30 Days' )

fig.show()