#############################################################
########## Crypto Factors For Medium Frequency ##############
##########        Auther Allen Wang            ##############
#############################################################

import pandas as pd
import numpy as np

def Factor_X1 (df_buyvol, df_sellvol, len):
    return (
             df_buyvol.rolling(window = len, closed = 'left').mean() /
            (df_buyvol.rolling(window = len, closed = 'left').mean() +
             df_sellvol.rolling(window = len, closed = 'left').mean())
           ).rename('MedFreqBook_X1')

def Factor_X2(df_high, df_low, df_close, len):
    _tr = pd.Series( np.maximum( df_high.shift(1) - df_low.shift(1), 
                                 abs(df_close.shift(1) - df_high.shift(1)),
                                 abs(df_close.shift(1) - df_low.shift(1))))
    return _tr.rolling(len).mean().rename('MedFreqBook_X2')

def Factor_X3(df_close, len):
    _aroon_up = df_close.shift(1).rolling(window=len).apply(lambda x:(len - x.argmax()) / len * 100)
    _aroon_down = df_close.shift(1).rolling(window=len).apply(lambda x:(len - x.argmin()) / len * 100)
    _aroon = _aroon_up - _aroon_down
    return _aroon.rename('MedFreqBook_X3')

def Factor_X4(df_close, len):
    _delta = df_close.shift(1).diff()
    _gain = _delta.where(_delta > 0, 0).rolling(window=len).mean()
    _loss = _delta.where(_delta < 0, 0).rolling(window=len).mean()
    _rsi = pd.Series(np.where(_loss != 0, _gain / _loss, 0), index = df_close.index)
    return _rsi.rename('MedFreqBook_X4')

def Factor_X5(df_close, len):
    _high = df_close.shift(1).rolling(window = len).max()
    _low = df_close.shift(1).rolling(window = len).min()
    _K = (df_close.shift(1) - _low) / (_high - _low)
    return _K.rename('MedFreqBook_X5')

def Factor_X6(df_close):
    return df_close.shift(1).pct_change().rename('MedFreqBook_X6')
                                                                                                                                                              
def Factor_X7(df_close, len):
    return df_close.shift(1).pct_change().rolling(window = len).mean().rename('MedFreqBook_X7')

def Factor_X8(df_open, df_high, df_low, df_close, len):
    # _alpha = 2.0 / (len + 1)
    _range = df_high.shift(1) - df_low.shift(1)
    _up = (df_high.shift(1).diff() + df_open.shift(1).diff() + df_close.shift(1).diff()) / 3.0
    _down = (df_low.shift(1).diff() + df_open.shift(1).diff() + df_close.shift(1).diff()) / 3.0
    _td = (_up - _down) / _range
    return _td.rename('MedFreqBook_X8').rolling(window = len).mean()

def Factor_X9(df, len):
    return df.shift(1).apply(lambda x : x['high'] - x['close'] / x['close'] - x['open'] 
                                        if x['close'] - x['open'] > 0 else 
                                        x['close'] - x['low'] / x['open'] - x['close'], 
                                        axis = 1).rename('MedFreqBook_X9').rolling(window = len).mean()

def Factor_X10(df_close, len):
    return (df_close.shift(1) / df_close.shift(1 + len)).rename('MedFreqBook_X10')
