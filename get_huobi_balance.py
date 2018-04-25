# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 23:56:08 2018

@author: Cruise Wong

"""

#%% get huobi
from Utils import *
def get_huobi_balance(currency,acct_id=None):
    """
    :param acct_id
    :return:
    """
    global ACCOUNT_ID

    if not acct_id:
        accounts = get_accounts()
        acct_id = accounts['data'][0]['id'];

    url = "/v1/account/accounts/{0}/balance".format(acct_id)
    params = {"account-id": acct_id}
    balance=api_key_get(params, url)
    df=pd.DataFrame(balance['data']['list'])
    df.currency=df.currency.apply(str.upper)
    return df[df.currency==currency]