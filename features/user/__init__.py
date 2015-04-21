# -*- coding: utf8 -*-

__author__ = 'Administrator'
import pandas as pd
##data:dataframe输入数据集
##lessThandate：小于日期，不包括等于
#userToBuyRate(data,'2014-12-18')
def userToBuyRate(data,lessThandate):
    data=data[data.date<lessThandate]
    ##用户加入购物车、浏览、收藏到购买的转化率，用户购买的总次数/用户浏览（收藏、购物车）总次数
    cartToBuyRate=(data[data.behavior_type==4].groupby(['user_id']).size())/(data[data.behavior_type==3].groupby(['user_id']).size())
    cartToBuyRate.name='usercartToBuyRate'
    cartToBuyRateDF=pd.DataFrame(cartToBuyRate)

    collectToBuyRate=(data[data.behavior_type==4].groupby(['user_id']).size())/(data[data.behavior_type==2].groupby(['user_id']).size())
    collectToBuyRate.name='usercollectToBuyRate'
    collectToBuyRateDF=pd.DataFrame(collectToBuyRate)

    browseToBuyRate=(data[data.behavior_type==4].groupby(['user_id']).size())/(data[data.behavior_type==1].groupby(['user_id']).size())
    browseToBuyRate.name='userbrowseToBuyRate'
    browseToBuyRateDF=pd.DataFrame(browseToBuyRate)

    browseToBuyRateDF.reset_index(inplace=True)
    collectToBuyRateDF.reset_index(inplace=True)
    cartToBuyRateDF.reset_index(inplace=True)

    toBuyRate=pd.merge(browseToBuyRateDF,collectToBuyRateDF,on='user_id',how='outer')

    toBuyRate=pd.merge(toBuyRate,cartToBuyRateDF,on='user_id',how='outer')

    toBuyRate.fillna(-1,inplace=True)
    return toBuyRate

##商品购物车、浏览、收藏到购买的转化率，用户购买的总次数/用户浏览（收藏、购物车）总次数
##data:dataframe输入数据集
##lessThandate：小于日期，不包括等于
#例如：itemToBuyRate(data,'2014-12-18')
def itemToBuyRate(data,lessThandate):
    data=data[data.date<=lessThandate]
    cartToBuyRate=(data[data.behavior_type==4].groupby(['item_id']).size())/(data[data.behavior_type==3].groupby(['item_id']).size())
    cartToBuyRate.name='itemcartToBuyRate'
    cartToBuyRateDF=pd.DataFrame(cartToBuyRate)

    collectToBuyRate=(data[data.behavior_type==4].groupby(['item_id']).size())/(data[data.behavior_type==2].groupby(['item_id']).size())
    collectToBuyRate.name='itemcollectToBuyRate'
    collectToBuyRateDF=pd.DataFrame(collectToBuyRate)

    browseToBuyRate=(data[data.behavior_type==4].groupby(['item_id']).size())/(data[data.behavior_type==1].groupby(['item_id']).size())
    browseToBuyRate.name='itembrowseToBuyRate'
    browseToBuyRateDF=pd.DataFrame(browseToBuyRate)

    browseToBuyRateDF.reset_index(inplace=True)
    collectToBuyRateDF.reset_index(inplace=True)
    cartToBuyRateDF.reset_index(inplace=True)

    toBuyRate=pd.merge(browseToBuyRateDF,collectToBuyRateDF,on='item_id',how='outer')

    toBuyRate=pd.merge(toBuyRate,cartToBuyRateDF,on='item_id',how='outer')

    toBuyRate.fillna(-1,inplace=True)
    return toBuyRate

import os
print os.getcwd()
