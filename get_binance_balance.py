# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 23:48:09 2018

@author: Cruise Wong

"""

import pandas as pd
#%% get binance

from binance.client import Client
binance_api_key='03wDOZYGsshWRxAPqLpO2qTOU4FpgVgjLcd3Kwgl4PT0jdsQDvoitvWe7auVZCQB'
binance_api_secret='DRimKqRB8r8uwW6DE9nHgMSi2LhqNE6pbOgbJqE4nz77TMm4Otfgqr1bedYMnTvZ'
def get_binance_balance(currency):
    client=Client(binance_api_key,binance_api_secret)
    account = client.get_account()
    balance=pd.DataFrame(account['balances'])
    return balance[balance.asset==currency]