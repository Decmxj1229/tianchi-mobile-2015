__author__ = 'yfwz100'

import random


def sample_negative_positive(df, weight=5):
    """
    Sample the given data frame.
    :param df: the data frame.
    :param weight: the weight of the negative set.
    :return: the sampled data frame.
    """
    posdf = df[df['label'] > 0]
    negdf = df[df['label'] <= 0]
    negdf = negdf.ix[random.choice(df.index.values, len(posdf) * weight)]
    return negdf.append(posdf)