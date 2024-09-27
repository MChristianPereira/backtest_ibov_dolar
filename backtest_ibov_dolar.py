import yfinance as yf
from bcb import currency as bcb
import matplotlib.pyplot as plt
import mplcyberpunk
from matplotlib.ticker import PercentFormatter

plt.style.use('cyberpunk')

ibov = yf.download('^BVSP', start = '2010-01-01')['Adj Close']

dolar = bcb.get(['USD'], start = '2010-01-01', end = '2024-09-25', side = 'ask')

dataframe = dolar.merge(ibov, left_index = True, right_index = True)
dataframe.columns = ['Dolar', 'IBOV']

dataframe['Media_Movel_IBOV'] = dataframe['IBOV'].rolling(window = 252).mean()

dataframe['Comprar_IBOV'] = dataframe['IBOV'] > dataframe ['Media_Movel_IBOV']
dataframe['Comprar_Dolar'] = dataframe['IBOV'] < dataframe ['Media_Movel_IBOV']

dataframe['Retorno_IBOV'] = ibov.pct_change().dropna()
dataframe['Retorno_Dolar'] = dolar.pct_change().dropna()

dataframe.loc[dataframe['Comprar_Dolar'] == True, 'Retorno_Final'] =dataframe['Retorno_Dolar']
dataframe.loc[dataframe['Comprar_IBOV'] == True, 'Retorno_Final'] = dataframe['Retorno_IBOV']

returns = dataframe[['Retorno_Dolar', 'Retorno_IBOV', 'Retorno_Final']].dropna()

acum_returns = ((1 + returns).cumprod() -1) * 100
print(acum_returns)

acum_returns.plot()

plt.title('Retornos Acumulados (%)', fontsize = 15)
plt.xlabel('')
plt.ylabel('')
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.legend(fontsize = 15)
plt.grid(False)
plt.gca().yaxis.set_major_formatter(PercentFormatter())
plt.show()