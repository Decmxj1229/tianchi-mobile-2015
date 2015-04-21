# -*- coding: utf8 -*-

__author__ = 'yfwz100'

from Apr10 import *
import pandas as pd

from features import item, user
from util.sample import sample_negative_positive


class Cached(object):

    def __init__(self, func):
        super(Cached, self).__init__()
        self.__func = func
        self.__cache = dict()

    def __call__(self, *args, **kwargs):
        key = (args, kwargs)
        if not self.__cache.has_key(key):
            self.__cache[key] = self.__func(*args, **kwargs)
        return self.__cache[key]


def extract_user_features(df, before_date):
    ret = user.conversion.user_to_buy_rate(df, before_date).reset_index()
    print 'Extracted user features: '
    print ret.head(2)
    return ret.reset_index()


def extract_item_features(df, before_date):
    ret = pd.DataFrame(dict(
        itemBrowseToBuyRate=item.conversion.overall(df, 1, 4, before_date),
        itemCollectToBuyRate=item.conversion.overall(df, 2, 4, before_date),
        itemCartToBuyRate=item.conversion.overall(df, 3, 4, before_date)
        # itemRecentBrowseToBuyRate=item.conversion.recent(df, before_date, 1, 4),
        # itemRecentCollectToBuyRate=item.conversion.recent(df, before_date, 2, 4),
        # itemRecentCartToBuyRate=item.conversion.recent(df, before_date, 3, 4)
    )).fillna(-1)
    print 'Extracted item features: '
    print ret.head(2)
    return ret.reset_index()


def ensure_label(df):
    df['cla'] = df['label']
    del df['label']
    print 'Ensuring label:'
    print df.head(2)
    return df


if __name__ == '__main__':

    u = pd.read_csv('data/2nd/tianchi_mobile_recommend_train_user_filtered.csv')
    m = pd.read_csv('data/2nd/tianchi_mobile_recommend_train_user_filtered_merged_old.csv')

    # 训练数据
    ensure_label(
        sample_negative_positive(
            pd.merge(
                pd.merge(
                    extract_user_item_behaviors_with_label(m, '2014-12-17').reset_index(),
                    extract_user_features(m, '2014-12-18'),
                    how='left',
                    on=['user_id']
                ),
                extract_item_features(m, '2014-12-18'),
                how='left',
                on=['item_id']
            )
        , 10).set_index('user_id')
    ).fillna(-1).to_csv('data/sample/apr21_train_2014-12-18.csv')

    # 测试数据
    ensure_label(pd.merge(
        pd.merge(
            extract_user_item_behaviors_with_label(m, '2014-12-18').reset_index(),
            extract_user_features(m, '2014-12-18'),
            how='left',
            on=['user_id']
        ),
        extract_item_features(m, '2014-12-18'),
        how='left',
        on=['item_id']
    ).set_index('user_id')).fillna(-1).to_csv('data/sample/apr21_test_2014-12-18.csv')

    # 预测数据
    pd.merge(
        pd.merge(
            extract_user_item_behaviors(u, '2014-12-18').reset_index(),
            extract_user_features(m, '2014-12-19'),
            how='left',
            on=['user_id']
        ),
        extract_item_features(m, '2014-12-19'),
        how='left',
        on=['item_id']
    ).set_index('user_id').to_csv('data/sample/apr21_predict_2014-12-18.csv')
