import pandas as pd
import numpy as np
import sys
import scipy.stats as sci
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import datetime as dt

ticker = sys.argv[1]

# Setting up data extract
start = dt.datetime(2006, 1, 1)
end = dt.datetime.now()
df = web.DataReader(ticker, 'morningstar', start, end)
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)
df = df.drop("Symbol", axis=1)



### Data Manipulations
log_returns = np.log(1+df['Close'].pct_change())
u = log_returns.mean()
var = log_returns.var()
stddev = log_returns.std()
drift = u - (0.5 * var)

t_intervals = 252
iterations = 10000

Z = sci.norm.ppf(np.random.rand(t_intervals,iterations))
daily_returns = np.exp(drift + stddev * Z)
S0 = df['Close'][-1:][0]
price_list = np.zeros_like(daily_returns)
price_list[0] = S0

for t in range(1,t_intervals):
    price_list[t] = price_list[t-1] * daily_returns[t]

result = price_list[-1]

print("Last Close Price: $"+str(df['Close'][-1:][0]))
print(sci.describe(result))

plt.plot(price_list)
plt.show()
plt.hist(result,bins=50)
plt.show()
