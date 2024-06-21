from polygon import RESTClient
import config
import json
import pandas as pd
import mplfinance as mpf
from typing import cast
from urllib3 import HTTPResponse

# Initialize RESTClient
client = RESTClient(config.API_KEY)

# Fetch historical data
aggs = cast(
    HTTPResponse,
    client.get_aggs(
        'AAPL',
        1,
        'day',
        '2022-05-20',
        '2022-11-11',
        raw=True
    ),
)

# Load data from response
data = json.loads(aggs.data)
results = data['results']

# Convert the data into a pandas DataFrame
df = pd.DataFrame(results)

# Convert timestamp to datetime
df['t'] = pd.to_datetime(df['t'], unit='ms')

# Set the timestamp as the DataFrame index
df.set_index('t', inplace=True)

# Rename columns to match mplfinance expectations
df.rename(columns={
    'o': 'Open',
    'h': 'High',
    'l': 'Low',
    'c': 'Close',
    'v': 'Volume'
}, inplace=True)

# Save DataFrame to a CSV file
df.to_csv('aapl_historical_data.csv')

# Plot the candlestick chart
mpf.plot(df, type='candle', volume=True, title='AAPL Historical Prices', style='yahoo')

