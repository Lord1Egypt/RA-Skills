import numpy as np
import pandas as pd
from scipy import stats
from sklearn import preprocessing
from functools import *
from functools import *
def alpha001(data, dependencies=['closePrice','openPrice','turnoverVol'], max_window=7):
    # (-1*CORR(RANK(DELTA(LOG(VOLUME),1)),RANK(((CLOSE-OPEN)/OPEN)),6)
    rank_sizenl = np.log(data['turnoverVol']).diff(1).rank(axis=0, pct=True)
    rank_ret = (data['closePrice'] / data['openPrice']) .rank(axis=0, pct=True)
    rel = rank_sizenl.rolling(window=6,min_periods=6).corr(rank_ret).iloc[-1] * (-1)
    return rel
    
def alpha002(data, dependencies=['closePrice','lowestPrice','highestPrice'], max_window=2):
    # -1*delta(((close-low)-(high-close))/(high-low),1)
    win_ratio = (2*data['closePrice']-data['lowestPrice']-data['highestPrice'])/(data['highestPrice']-data['lowestPrice'])
    return win_ratio.diff(1).iloc[-1] * (-1)

def alpha003(data, dependencies=['closePrice','lowestPrice','highestPrice'], max_window=6):
    # -1*SUM((CLOSE=DELAY(CLOSE,1)?0:CLOSE-(CLOSE>DELAY(CLOSE,1)?MIN(LOW,DELAY(CLOSE,1)):MAX(HIGH,DELAY(CLOSE,1)))),6)
    # \u8fd9\u91ccSUM\u5e94\u8be5\u4e3aTSSUM
    alpha = data['closePrice']
    condition2 = data['closePrice'].diff(periods=1) > 0.0
    condition3 = data['closePrice'].diff(periods=1) < 0.0
    alpha[condition2] = data['closePrice'][condition2] - np.minimum(data['closePrice'][condition2].shift(1).replace(np.NaN,10000), data['lowestPrice'][condition2])
    alpha[condition3] = data['closePrice'][condition3] - np.maximum(data['closePrice'][condition3].shift(1).replace(np.NaN,0), data['highestPrice'][condition3])
    return alpha.sum(axis=0) * (-1)

def alpha004(data, dependencies=['closePrice','turnoverVol'], max_window=20):
    # (((SUM(CLOSE,8)/8)+STD(CLOSE,8))<(SUM(CLOSE,2)/2))
    # ?-1:(SUM(CLOSE,2)/2<(SUM(CLOSE,8)/8-STD(CLOSE,8))
    #     ?1:(1<=(VOLUME/MEAN(VOLUME,20))
    #       ?1:-1))
#STD(CLOSE,8)：过去8天的收盘价的标准差；VOLUME：成交量；MEAN(VOLUME,20);过去20天的均值
    if MEAN(data['closePrice'],8)+STD(data['closePrice'],8)<MEAN(data['closePrice'],2):return -1
    elif MEAN(data['closePrice'],2)<MEAN(data['closePrice'],8)-STD(data['closePrice'],8):return 1
    elif 1<=data['turnoverVol'].iloc[19]/MEAN(data['turnoverVol'],20):return 1
    else: return -1

def alpha005(data, dependencies=['turnoverVol', 'highestPrice'], max_window=13):
    # -1*TSMAX(CORR(TSRANK(VOLUME,5),TSRANK(HIGH,5),5),3)
    ts_volume = data['turnoverVol'].rolling(window=5,min_periods=5).apply(lambda x: stats.rankdata(x)[-1]/5.0)
    ts_high = data['highestPrice'].rolling(window=5,min_periods=5).apply(lambda x: stats.rankdata(x)[-1]/5.0)
    corr_ts = ts_volume.rolling(window=5, min_periods=5).corr(ts_high)
    alpha = corr_ts.iloc[-3:].max(axis=0) * (-1)
    return alpha

def alpha006(data, dependencies=['openPrice', 'highestPrice'], max_window=5):
    # -1*RANK(SIGN(DELTA(OPEN*0.85+HIGH*0.15,4)))
    # \u6ce8:\u53d6\u503c\u6392\u5e8f\u6709\u968f\u673a\u6027
    return sorted(np.sign(DELTA(data['openPrice']*0.85+data['highestPrice']*0.15,4)))[0]*-1


def alpha007(data, dependencies=['turnoverVol', 'turnoverValue', 'closePrice'], max_window=4):
    # (RANK(MAX(VWAP-CLOSE,3))+RANK(MIN(VWAP-CLOSE,3)))*RANK(DELTA(VOLUME,3))
    # \u611f\u89c9MAX\u5e94\u8be5\u4e3aTSMAX
    vwap = data['turnoverValue'] / data['turnoverVol']
    part1 = (vwap - data['closePrice']).rolling(window=3,min_periods=3).max().rank(axis=0, pct=True)
    part2 = (vwap - data['closePrice']).rolling(window=3,min_periods=3).min().rank(axis=0, pct=True)
    part3 = data['turnoverVol'].diff(3).rank(axis=0, pct=True).iloc[-1]
    alpha = (part1 + part2) * part3
    return alpha.iloc[-1]

def alpha008(data, dependencies=['turnoverVol', 'turnoverValue', 'highestPrice', 'lowestPrice'], max_window=5):
    # -1*RANK(DELTA((HIGH+LOW)/10+VWAP*0.8,4))
    # \u53d7\u80a1\u4ef7\u5355\u4ef7\u5f71\u54cd,\u53cd\u8f6c
    vwap = data['turnoverValue'] / data['turnoverVol']
    ma_price = data['highestPrice']*0.1 + data['lowestPrice']*0.1 + vwap*0.8
    alpha = ma_price.diff(4).iloc[-1] * (-1)
    return alpha

def alpha009(data, dependencies=['highestPrice', 'lowestPrice', 'turnoverVol'], max_window=8):
    # SMA(((HIGH+LOW)/2-(DELAY(HIGH,1)+DELAY(LOW,1))/2)*(HIGH-LOW)/VOLUME,7,2)
    part1 = (data['highestPrice']+data['lowestPrice'])*0.5-(data['highestPrice'].shift(1)+data['lowestPrice'].shift(1))*0.5
    part2 = part1 * (data['highestPrice']-data['lowestPrice']) / data['turnoverVol']
    alpha = part2.ewm(adjust=False, alpha=float(2)/7, min_periods=0, ignore_na=False).mean().iloc[-1]
    return alpha

def alpha010(data, dependencies=['closePrice'], max_window=25):
    # RANK(MAX(((RET<0)?STD(RET,20):CLOSE)^2,5))
    # \u6ca1\u6cd5\u89e3\u91ca,\u611f\u89c9MAX\u5e94\u8be5\u4e3aTSMAX
    ret = data['closePrice'].pct_change(periods=1)
    part1 = ret.rolling(window=20, min_periods=20).std()
    condition = ret >= 0.0
    part1[condition] = data['closePrice'][condition]
    alpha = (part1 ** 2).rolling(window=5,min_periods=5).max().rank(axis=0, pct=True)
    return alpha.iloc[-1]
    
def alpha011(data, dependencies=['closePrice','lowestPrice','highestPrice','turnoverVol'], max_window=6):
    # SUM(((CLOSE-LOW)-(HIGH-CLOSE))./(HIGH-LOW).*VOLUME,6)
    # \u8fd16\u5929\u83b7\u5229\u76d8\u6bd4\u4f8b
    return ((2*data['closePrice']-data['lowestPrice']-data['highestPrice'])/(data['highestPrice']-data['lowestPrice'])*data['turnoverVol']).sum(axis=0) * (-1)

def alpha012(data, dependencies=['openPrice','closePrice','turnoverVol', 'turnoverValue'], max_window=10):
    # RANK(OPEN-MA(VWAP,10))*RANK(ABS(CLOSE-VWAP))*(-1)
    vwap = data['turnoverValue'] / data['turnoverVol']
    part1 = (data['openPrice']-vwap.rolling(window=10,center=False).mean()).rank(axis=0, pct=True).iloc[-1]
    part2 = abs(data['closePrice']-vwap).rank(axis=0, pct=True).iloc[-1]
    alpha = part1 * part2 * (-1)
    return alpha

def alpha013(data, dependencies=['highestPrice','lowestPrice','turnoverVol', 'turnoverValue'], max_window=1):
    # ((HIGH*LOW)^0.5)-VWAP
    # \u8981\u6ce8\u610fVWAP/price\u662f\u5426\u590d\u6743
    vwap = data['turnoverValue'] / data['turnoverVol']
    alpha = np.sqrt(data['highestPrice'] * data['lowestPrice']) - vwap
    return alpha.iloc[-1]

def alpha014(data, dependencies=['closePrice'], max_window=6):
    # CLOSE-DELAY(CLOSE,5)
    # \u4e0e\u80a1\u4ef7\u76f8\u5173\uff0c\u5229\u597d\u8305\u53f0
    return data['closePrice'].diff(5).iloc[-1]

def alpha015(data, dependencies=['openPrice', 'closePrice'], max_window=2):
    # OPEN/DELAY(CLOSE,1)-1
    # \u8df3\u7a7a\u9ad8\u5f00/\u4f4e\u5f00
    return (data['openPrice']/data['closePrice'].shift(1)-1.0).iloc[-1]

def alpha016(data, dependencies=['turnoverVol', 'turnoverValue'], max_window=10):
    # (-1*TSMAX(RANK(CORR(RANK(VOLUME),RANK(VWAP),5)),5))
    # \u611f\u89c9\u5176\u4e2d\u6709\u4e2aTSRANK
    vwap = data['turnoverValue'] / data['turnoverVol']
    corr_vol_vwap = data['turnoverVol'].rank(axis=0, pct=True).rolling(window=5,min_periods=5).corr(vwap.rank(axis=0, pct=True))
    alpha = corr_vol_vwap.rolling(window=5,min_periods=5).apply(lambda x: stats.rankdata(x)[-1]/5.0)
    alpha = alpha.iloc[-5:].max(axis=0) * (-1)
    return alpha

def alpha017(data, dependencies=['closePrice', 'turnoverVol', 'turnoverValue'], max_window=16):
    # RANK(VWAP-MAX(VWAP,15))^DELTA(CLOSE,5)
    vwap = data['turnoverValue'] / data['turnoverVol']
    delta_price = data['closePrice'].diff(5).iloc[-1]
    alpha = (vwap-vwap.rolling(window=15,min_periods=15).max()).rank(axis=0, pct=True).iloc[-1] ** delta_price
    return alpha

def alpha018(data, dependencies=['closePrice'], max_window=6):
    # CLOSE/DELAY(CLOSE,5)
    # \u8fd15\u65e5\u6da8\u5e45, REVS5
    return (data['closePrice'] / data['closePrice'].shift(5)).iloc[-1]

def alpha019(data, dependencies=['closePrice'], max_window=6):
    # (CLOSE<DELAY(CLOSE,5)?(CLOSE/DELAY(CLOSE,5)-1):(CLOSE=DELAY(CLOSE,5)?0:(1-DELAY(CLOSE,5)/CLOSE)))
    # \u7c7b\u4f3c\u4e8e\u8fd1\u4e94\u65e5\u6da8\u5e45
    condition1 = data['closePrice'] <= data['closePrice'].shift(5)
    alpha = data['closePrice']
    alpha[condition1] = data['closePrice'].pct_change(periods=5)[condition1]
    alpha[~condition1] = -data['closePrice'].pct_change(periods=5)[~condition1]
    return alpha.iloc[-1]

def alpha020(data, dependencies=['closePrice'], max_window=7):
    # (CLOSE/DELAY(CLOSE,6)-1)*100
    # \u8fd16\u65e5\u6da8\u5e45
    return (data['closePrice'].pct_change(periods=6) * 100.0).iloc[-1]

def alpha021(data, dependencies=['closePrice'], max_window=12):
    # REGBETA(MEAN(CLOSE,6),SEQUENCE(6))
    a=[MEAN(list(data['closePrice'])[:-x],6) for x in range(1,7)]
    return REGBETA(a,SEQUENCE(6),6)

def alpha022(data, dependencies=['closePrice'], max_window=21):
    # SMEAN((CLOSE/MEAN(CLOSE,6)-1-DELAY(CLOSE/MEAN(CLOSE,6)-1,3)),12,1)
    # \u731cSMEAN\u662fSMA
    ratio = data['closePrice'] / data['closePrice'].rolling(window=6,min_periods=6).mean() - 1.0
    alpha = ratio.diff(3).ewm(adjust=False, alpha=float(1)/12, min_periods=12, ignore_na=False).mean().iloc[-1]
    return alpha
    
def alpha023(data, dependencies=['closePrice'], max_window=40):
    # SMA((CLOSE>DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1) /
    # (SMA((CLOSE>DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1)+SMA((CLOSE<=DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1))
    # *100
    prc_std = data['closePrice'].rolling(window=20, min_periods=20).std()
    condition1 = data['closePrice'] > data['closePrice'].shift(1)
    part1 = prc_std.copy(deep=True)
    part2 = prc_std.copy(deep=True)
    part1[~condition1] = 0.0
    part2[condition1] = 0.0
    alpha = part1.ewm(adjust=False, alpha=float(1)/20, min_periods=20, ignore_na=False).mean() / (part1.ewm(adjust=False, alpha=float(1)/20, min_periods=20, ignore_na=False).mean() + part2.ewm(adjust=False, alpha=float(1)/20, min_periods=20, ignore_na=False).mean()) * 100
    return alpha.iloc[-1]

def alpha024(data, dependencies=['closePrice'], max_window=10):
    # SMA(CLOSE-DELAY(CLOSE,5),5,1)
    return data['closePrice'].diff(5).ewm(adjust=False, alpha=float(1)/5, min_periods=5, ignore_na=False).mean().iloc[-1]

def alpha025(data, dependencies=['closePrice', 'turnoverVol'], max_window=251):
    # (-1*RANK(DELTA(CLOSE,7)*(1-RANK(DECAYLINEAR(VOLUME/MEAN(VOLUME,20),9)))))*(1+RANK(SUM(RET,250)))
    w = np.array(range(1, 10))
    ret = data['closePrice'].pct_change(periods=1)
    part1 = data['closePrice'].diff(7)
    part2 = data['turnoverVol']/(data['turnoverVol'].rolling(window=20,min_periods=20).mean())
    part2 = 1.0 - part2.rolling(window=9, min_periods=9).apply(lambda x: np.dot(x, w)).rank(axis=0, pct=True)
    part3 = 1.0 + ret.rolling(window=250, min_periods=250).sum().rank(axis=0, pct=True)
    alpha = (-1.0) * (part1 * part2).rank(axis=0, pct=True) * part3
    return alpha.iloc[-1]

def alpha026(data, dependencies=['closePrice', 'turnoverValue', 'turnoverVol'], max_window=235):
    # (SUM(CLOSE,7)/7-CLOSE+CORR(VWAP,DELAY(CLOSE,5),230))
    vwap = data['turnoverValue'] / data['turnoverVol']
    part1 = data['closePrice'].rolling(window=7, min_periods=7).mean() - data['closePrice']
    part2 = vwap.rolling(window=230, min_periods=230).corr(data['closePrice'].shift(5))
    return (part1 + part2).iloc[-1]

def alpha027(data, dependencies=['closePrice'], max_window=18):
    # WMA((CLOSE-DELTA(CLOSE,3))/DELAY(CLOSE,3)*100+(CLOSE-DELAY(CLOSE,6))/DELAY(CLOSE,6)*100,12)
    part1 = data['closePrice'].pct_change(periods=3) * 100.0 + data['closePrice'].pct_change(periods=6) * 100.0
    # w = preprocessing.normalize(np.array([i for i in range(1, 13)]),norm='l1',axis=1).reshape(-1)
    w=np.array(range(1,13))
    alpha = part1.rolling(window=12, min_periods=12).apply(lambda x: np.dot(x, w))
    return alpha.iloc[-1]

def alpha028(data, dependencies=['KDJ_J'], max_window=13):
    # 3*SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1)
    # -2*SMA(SMA((CLOSE-TSMIN(LOW,9))/( TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1),3,1)
    # \u5c31\u662fKDJ_J
    part1 =data['closePrice']- data['closePrice'].rolling(window=9, min_periods=9).min()
    part2=data['highestPrice'].rolling(window=9, min_periods=9).max()-data['lowestPrice'].rolling(window=9, min_periods=9).min()
    part3= 3*SMA(list(part1/part2*100)[-3:],3,1)
    part4=[SMA(list(part1/part2*100)[-5:-2],3,1),SMA(list(part1/part2*100)[-4:-1],3,1),SMA(list(part1/part2*100)[-3:],3,1)]
    part5=part3-2*SMA(part4,3,1)
    return part5

def alpha029(data, dependencies=['closePrice', 'turnoverVol'], max_window=7):
    # (CLOSE-DELAY(CLOSE,6))/DELAY(CLOSE,6)*VOLUME
    # \u83b7\u5229\u6210\u4ea4\u91cf
    return (data['closePrice'].pct_change(periods=6)*data['turnoverVol']).iloc[-1]

def alpha030(data, dependencies=['closePrice', 'PB', 'MktValue'], max_window=81):
    # WMA((REGRESI(RET,MKT,SMB,HML,60))^2,20)
    # \u5373\u7279\u8d28\u6027\u6536\u76ca
    # MKT \u4e3a\u5e02\u503c\u52a0\u6743\u7684\u5e02\u573a\u5e73\u5747\u6536\u76ca\u7387\uff0c
    # SMB \u4e3a\u5e02\u503c\u6700\u5c0f\u768430%\u7684\u80a1\u7968\u7684\u5e73\u5747\u6536\u76ca\u51cf\u53bb\u5e02\u503c\u6700\u5927\u768430%\u7684\u80a1\u7968\u7684\u5e73\u5747\u6536\u76ca\uff0c
    # HML \u4e3aPB\u6700\u9ad8\u768430%\u7684\u80a1\u7968\u7684\u5e73\u5747\u6536\u76ca\u51cf\u53bbPB\u6700\u4f4e\u768430%\u7684\u80a1\u7968\u7684\u5e73\u5747\u6536\u76ca
    ret = data['closePrice'].pct_change(periods=1).fillna(0.0)
    mkt_ret = (ret * data['MktValue']).sum(axis=1) / data['MktValue'].sum(axis=1)
    me30 = (data['MktValue'].T <= data['MktValue'].quantile(0.3, axis=1)).T
    me70 = (data['MktValue'].T >= data['MktValue'].quantile(0.7, axis=1)).T
    pb30 = (data['PB'].T <= data['PB'].quantile(0.3, axis=1)).T
    pb70 = (data['PB'].T >= data['PB'].quantile(0.7, axis=1)).T
    smb_ret = ret[me30].mean(axis=1, skipna=True) - ret[me70].mean(axis=1, skipna=True)
    hml_ret = ret[pb70].mean(axis=1, skipna=True) - ret[pb30].mean(axis=1, skipna=True)
    xs = pd.concat([mkt_ret, smb_ret, hml_ret], axis=1)
    idxs = pd.Series(data=range(len(data['closePrice'].index)), index=data['closePrice'].index)

    def multi_var_linregress(idx, y, xs):
        X = xs.iloc[idx]
        Y = y.iloc[idx]
        X = sm.add_constant(X)
        try:
            res = np.array(sm.OLS(Y, X).fit().resid)
        except Exception as e:
            return np.nan
        return res[-1]

    # print(xs.tail(5), ret.tail(5))
    residual = [idxs.rolling(window=60, min_periods=60).apply(lambda x: multi_var_linregress(x, ret[col], xs)) for col in ret.columns]
    residual = pd.concat(residual, axis=1)
    residual.columns = ret.columns

    w = preprocessing.normalize(np.array([i for i in range(1, 21)]), norm='l1', axis=1).reshape(-1)
    alpha = (residual ** 2).rolling(window=20, min_periods=20).apply(lambda x: np.dot(x, w))
    return alpha.iloc[-1]

def alpha031(data, dependencies=['closePrice'], max_window=12):
    # (CLOSE-MEAN(CLOSE,12))/MEAN(CLOSE,12)*100
    return ((data['closePrice']/data['closePrice'].rolling(window=12,min_periods=12).mean()-1.0)*100).iloc[-1]

def alpha032(data, dependencies=['highestPrice', 'turnoverVol'], max_window=6):
    # (-1*SUM(RANK(CORR(RANK(HIGH),RANK(VOLUME),3)),3))
    # \u91cf\u4ef7\u9f50\u5347/\u53cd\u8f6c
    part1 = data['highestPrice'].rank(axis=0, pct=True).rolling(window=3, min_periods=3).corr(data['turnoverVol'].rank(axis=0, pct=True))
    alpha = part1.rank(axis=0, pct=True).iloc[-3:].sum(axis=0) * (-1)
    return alpha

def alpha033(data, dependencies=['lowestPrice', 'closePrice', 'turnoverVol'], max_window=241):
    # (-1*TSMIN(LOW,5)+DELAY(TSMIN(LOW,5),5))*RANK((SUM(RET,240)-SUM(RET,20))/220)*TSRANK(VOLUME,5)
    part1 = data['lowestPrice'].rolling(window=5, min_periods=5).min().diff(5) * (-1)
    ret = data['closePrice'].pct_change(periods=1)
    part2 = ((ret.rolling(window=240, min_periods=240).sum() - ret.rolling(window=20, min_periods=20).sum()) / 220).rank(axis=0, pct=True)
    part3 = data['turnoverVol'].iloc[-5:].rank(axis=0, pct=True)
    alpha = part1.iloc[-1] * part2.iloc[-1] * part3.iloc[-1]
    return alpha

def alpha034(data, dependencies=['closePrice'], max_window=12):
    # MEAN(CLOSE,12)/CLOSE
    return (data['closePrice'].rolling(window=12, min_periods=12).mean() / data['closePrice']).iloc[-1]

def alpha035(data, dependencies=['openPrice', 'closePrice', 'turnoverVol'], max_window=24):
    # (MIN(RANK(DECAYLINEAR(DELTA(OPEN,1),15)),RANK(DECAYLINEAR(CORR(VOLUME,OPEN*0.65+CLOSE*0.35,17),7)))*-1)
    # \u731c\u540e\u4e00\u9879OPEN\u4e3aCLOSE
    w7 =np.array(range(1, 8)).reshape(-1)
    w15 = np.array(range(1, 16)).reshape(-1)
    part1 = data['openPrice'].diff(periods=1).rolling(window=15, min_periods=15).apply(lambda x: np.dot(x, w15)).rank(axis=0, pct=True)
    part2 = (data['openPrice']*0.65+data['closePrice']*0.35).rolling(window=17, min_periods=17).corr(data['turnoverVol']).rolling(window=7, min_periods=7).apply(lambda x: np.dot(x, w7)).rank(axis=0, pct=True)
    alpha = np.minimum(part1, part2).iloc[-1] * (-1)
    return alpha

def alpha036(data, dependencies=['turnoverValue', 'turnoverVol'], max_window=9):
    # RANK(SUM(CORR(RANK(VOLUME),RANK(VWAP),6),2))
    # \u91cf\u4ef7\u9f50\u5347, TSSUM
    vwap = data['turnoverValue'] / data['turnoverVol']
    part1 = data['turnoverVol'].rank(axis=0, pct=True).rolling(window=6,min_periods=6).corr(vwap.rank(axis=0, pct=True))
    alpha = part1.rolling(window=2, min_periods=2).sum().rank(axis=0, pct=True).iloc[-1]
    return alpha

def alpha037(data, dependencies=['openPrice', 'closePrice'], max_window=16):
    # (-1*RANK(SUM(OPEN,5)*SUM(RET,5)-DELAY(SUM(OPEN,5)*SUM(RET,5),10)))
    part1 = data['openPrice'].rolling(window=5, min_periods=5).sum() * (data['closePrice'].pct_change(periods=1).rolling(window=5, min_periods=5).sum())
    alpha = part1.diff(periods=10).iloc[-1] * (-1)
    return alpha
    
def alpha038(data, dependencies=['highestPrice'], max_window=20):
    # ((SUM(HIGH,20)/20)<HIGH)?(-1*DELTA(HIGH,2)):0
    # \u4e0e\u80a1\u4ef7\u76f8\u5173\uff0c\u5229\u597d\u8305\u53f0
    condition = data['highestPrice'].rolling(window=20, min_periods=20).mean() < data['highestPrice']
    alpha = data['highestPrice'].diff(periods=2) * (-1)
    alpha[~condition] = 0.0
    return alpha.iloc[-1]

def alpha039(data, dependencies=['closePrice', 'openPrice', 'turnoverValue', 'turnoverVol'], max_window=243):
    # (RANK(DECAYLINEAR(DELTA(CLOSE,2),8))-RANK(DECAYLINEAR(CORR(VWAP*0.3+OPEN*0.7,SUM(MEAN(VOLUME,180),37),14),12)))*-1
    w8 =np.array(range(1, 9)).reshape(-1)
    w12 = np.array(range(1, 13)).reshape(-1)
    parta = data['turnoverValue'] / data['turnoverVol'] * 0.3 + data['openPrice'] * 0.7
    partb = data['turnoverVol'].rolling(window=180, min_periods=180).mean().rolling(window=37, min_periods=37).sum()
    part1 = data['closePrice'].diff(periods=2).rolling(window=8, min_periods=8).apply(lambda x: np.dot(x, w8)).rank(axis=0,pct=True)
    part2 = parta.rolling(window=14, min_periods=14).corr(partb).rolling(window=12, min_periods=12).apply(lambda x: np.dot(x, w12)).rank(axis=0, pct=True)
    return (part1 - part2).iloc[-1] * (-1)

def alpha040(data, dependencies=['VR','turnoverVol'], max_window=27):
    # SUM(CLOSE>DELAY(CLOSE,1)?VOLUME:0,26)/SUM(CLOSE<=DELAY(CLOSE,1)?VOLUME:0,26)*100
    # \u5373VR\u6280\u672f\u6307\u6807
    part1=((data['closePrice'].diff(periods=1)>0)*data['turnoverVol']).sum()
    part2=((data['closePrice'].diff(periods=1)<=0)*data['turnoverVol']).sum()
    return part1/part2*100


def alpha041(data, dependencies=['turnoverValue', 'turnoverVol'], max_window=9):
    # RANK(MAX(DELTA(VWAP,3),5))*-1
    return (data['turnoverValue'] / data['turnoverVol']).diff(periods=3).rolling(window=5, min_periods=5).max().rank(axis=0, pct=True).iloc[-1] * (-1)

def alpha042(data, dependencies=['highestPrice', 'turnoverVol'], max_window=10):
    # (-1*RANK(STD(HIGH,10)))*CORR(HIGH,VOLUME,10)
    # \u4ef7\u7a33/\u91cf\u4ef7\u9f50\u5347
    part1 = data['highestPrice'].rolling(window=10,min_periods=10).std().rank(axis=0,pct=True) * (-1)
    part2 = data['highestPrice'].rolling(window=10,min_periods=10).corr(data['turnoverVol'])
    return (part1 * part2).iloc[-1]

def alpha043(data, dependencies=['OBV6'], max_window=7):
    # (SUM(CLOSE>DELAY(CLOSE,1)?VOLUME:(CLOSE<DELAY(CLOSE,1)?-VOLUME:0),6))
    # \u5373OBV6\u6307\u6807
    part1=((data['closePrice'].diff(periods=1)>0)*data['turnoverVol']).sum()
    part2=((data['closePrice'].diff(periods=1)<0)*-data['turnoverVol']).sum()
    return part1+part2

def alpha044(data, dependencies=['turnoverValue', 'turnoverVol', 'lowestPrice'], max_window=29):
    # (TSRANK(DECAYLINEAR(CORR(LOW,MEAN(VOLUME,10),7),6),4)+TSRANK(DECAYLINEAR(DELTA(VWAP,3),10),15))
    w10 = np.array(range(1, 11)).reshape(-1)
    w6 = np.array(range(1, 7)).reshape(-1)
    part1 = (data['turnoverVol'].rolling(window=10,min_periods=10).mean().rolling(window=7, min_periods=7).corr(data['lowestPrice'])).rolling(window=6,min_periods=6).apply(lambda x: np.dot(x, w6))
    part1 = part1.iloc[-4:].rank(axis=0, pct=True)
    part2 = (data['turnoverValue'] / data['turnoverVol']).diff(periods=3).rolling(window=10,min_periods=10).apply(lambda x: np.dot(x, w10))
    part2 = part2.iloc[-15:].rank(axis=0, pct=True)
    return (part1 + part2).iloc[-1]

def alpha045(data, dependencies=['openPrice', 'closePrice', 'turnoverValue', 'turnoverVol'], max_window=165):
    # (RANK(DELTA(CLOSE*0.6+OPEN*0.4,1))*RANK(CORR(VWAP,MEAN(VOLUME,150),15)))
    part1 = (data['closePrice'] * 0.6 + data['openPrice'] * 0.4).diff(periods=1).rank(axis=0,pct=True)
    part2 = ((data['turnoverValue']/data['turnoverVol']).rolling(window=15,min_periods=15).corr(data['turnoverVol'].rolling(window=150,min_periods=150).mean())).rank(axis=0,pct=True)
    return (part1 * part2).iloc[-1]

def alpha046(data, dependencies=['BBIC'], max_window=24):
    # (MEAN(CLOSE,3)+MEAN(CLOSE,6)+MEAN(CLOSE,12)+MEAN(CLOSE,24))/(4*CLOSE)
    # \u5373BBIC\u6280\u672f\u6307\u6807
    part1=[3,6,12,24]
    part2=[data['closePrice'].rolling(window=x,min_periods=x).mean().iloc[-1] for x in part1]
    return sum(part2)/data['closePrice'].iloc[-1]*4

def alpha047(data, dependencies=['closePrice', 'lowestPrice', 'highestPrice'], max_window=15):
    # SMA((TSMAX(HIGH,6)-CLOSE)/(TSMAX(HIGH,6)-TSMIN(LOW,6))*100,9,1)
    # RSV\u6280\u672f\u6307\u6807\u53d8\u79cd
    part1 = (data['highestPrice'].rolling(window=6,min_periods=6).max()-data['closePrice']) /  (data['highestPrice'].rolling(window=6,min_periods=6).max()- data['lowestPrice'].rolling(window=6,min_periods=6).min()) * 100
    alpha = part1.ewm(adjust=False, alpha=float(1)/9, min_periods=0, ignore_na=False).mean().iloc[-1]
    return alpha

def alpha048(data, dependencies=['closePrice', 'turnoverVol'], max_window=20):
    # -1*RANK(SIGN(CLOSE-DELAY(CLOSE,1))+SIGN(DELAY(CLOSE,1)-DELAY(CLOSE,2))+SIGN(DELAY(CLOSE,2)-DELAY(CLOSE,3)))*SUM(VOLUME,5)/SUM(VOLUME,20)
    # \u4e0b\u8dcc\u7f29\u91cf
    diff1 = data['closePrice'].diff(1)
    part1 = (np.sign(diff1) + np.sign(diff1.shift(1)) + np.sign(diff1.shift(2))).rank(axis=0, pct=True)
    part2 = data['turnoverVol'].rolling(window=5, min_periods=5).sum() / data['turnoverVol'].rolling(window=20, min_periods=20).sum()
    return (part1 * part2).iloc[-1] * (-1)

def alpha049(data, dependencies=['highestPrice', 'lowestPrice'], max_window=13):
    # SUM(HIGH+LOW>=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)/
    # (SUM(HIGH+LOW>=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)+
    # SUM(HIGH+LOW<=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12))
    condition1 = (data['highestPrice'] + data['lowestPrice']) >= (data['highestPrice'] + data['lowestPrice']).shift(1)
    condition2 = (data['highestPrice'] + data['lowestPrice']) <= (data['highestPrice'] + data['lowestPrice']).shift(1)
    part1 = data['highestPrice']
    part2 = data['highestPrice']
    part1[~condition1] = np.maximum(abs(data['highestPrice'].diff(1)[~condition1]), abs(data['lowestPrice'].diff(1)[~condition1]))
    part2[~condition2] = np.maximum(abs(data['highestPrice'].diff(1)[~condition2]), abs(data['lowestPrice'].diff(1)[~condition2]))
    alpha = part1.rolling(window=12,min_periods=12).sum() / (part1.rolling(window=12,min_periods=12).sum() + part2.rolling(window=12,min_periods=12).sum())
    return alpha.iloc[-1]

def alpha050(data, dependencies=['highestPrice', 'lowestPrice'], max_window=13):
    # SUM(HIGH+LOW<=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)/
    # (SUM(HIGH+LOW<=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)
    # +SUM(HIGH+LOW>=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12))
    # -SUM(HIGH+LOW>=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)/
    # (SUM(HIGH+LOW>=DELAY(HIGH,1)+DELAY(LOW,1)?0: MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)
    # +SUM(HIGH+LOW<=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12))
    condition1 = (data['highestPrice'] + data['lowestPrice']) >= (data['highestPrice'] + data['lowestPrice']).shift(1)
    condition2 = (data['highestPrice'] + data['lowestPrice']) <= (data['highestPrice'] + data['lowestPrice']).shift(1)
    part = np.maximum(abs(data['highestPrice'].diff(1)), abs(data['lowestPrice'].diff(1)))
    a=(part*condition2).sum()
    b=(part*condition1).sum()
    return a/(a+b)-b/(a+b)

def alpha051(data, dependencies=['highestPrice', 'lowestPrice'], max_window=13):
    # SUM(((HIGH+LOW)<=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1)))),12)/
    # (SUM(((HIGH+LOW)<=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1)))),12)
    # +SUM(((HIGH+LOW)>=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1)))),12))
    condition1 = (data['highestPrice'] + data['lowestPrice']) <= (data['highestPrice'] + data['lowestPrice']).shift(1)
    condition2 = (data['highestPrice'] + data['lowestPrice']) >= (data['highestPrice'] + data['lowestPrice']).shift(1)
    part1 = data['highestPrice']
    part2 = data['highestPrice']
    part1[~condition1] = np.maximum(abs(data['highestPrice'].diff(1)[~condition1]), abs(data['lowestPrice'].diff(1)[~condition1]))
    part2[~condition2] = np.maximum(abs(data['highestPrice'].diff(1)[~condition2]), abs(data['lowestPrice'].diff(1)[~condition2]))
    alpha = part1.rolling(window=12,min_periods=12).sum() / (part1.rolling(window=12,min_periods=12).sum() + part2.rolling(window=12,min_periods=12).sum())
    return alpha.iloc[-1]

def alpha052(data, dependencies=['highestPrice', 'lowestPrice', 'closePrice'], max_window=27):
    # SUM(MAX(0,HIGH-DELAY((HIGH+LOW+CLOSE)/3,1)),26)/SUM(MAX(0,DELAY((HIGH+LOW+CLOSE)/3,1)-L),26)*100
    ma = (data['highestPrice'] + data['lowestPrice'] + data['closePrice']) / 3.0
    part1 = (np.maximum(0.0, (data['highestPrice'] - ma.shift(1)))).rolling(window=26, min_periods=26).sum()
    part2 = (np.maximum(0.0, (ma.shift(1) - data['lowestPrice']))).rolling(window=26, min_periods=26).sum()
    return (part1 / part2 * 100.0).iloc[-1]

def alpha053(data, dependencies=['closePrice'], max_window=13):
    # COUNT(CLOSE>DELAY(CLOSE,1),12)/12*100
    return ((data['closePrice'].diff(1) > 0.0).rolling(window=12, min_periods=12).sum() / 12.0 * 100).iloc[-1]

def alpha054(data, dependencies=['closePrice', 'openPrice'], max_window=10):
    # (-1*RANK(STD(ABS(CLOSE-OPEN))+CLOSE-OPEN+CORR(CLOSE,OPEN,10)))
    # \u6ce8\uff0c\u8fd9\u91ccSTD\u6ca1\u6709\u6307\u660e\u5468\u671f
    part1 = abs(data['closePrice']-data['openPrice']).rolling(window=10, min_periods=10).std() + data['closePrice'] - data['openPrice'] + data['closePrice'].rolling(window=10, min_periods=10).corr(data['openPrice'])
    return part1.rank(axis=0, pct=True).iloc[-1] * (-1)

def alpha055(data, dependencies=['openPrice', 'lowestPrice', 'closePrice', 'highestPrice'], max_window=21):
    # SUM(16*(CLOSE+(CLOSE-OPEN)/2-DELAY(OPEN,1))/
    # ((ABS(HIGH-DELAY(CLOSE,1))>ABS(LOW-DELAY(CLOSE,1)) & ABS(HIGH-DELAY(CLOSE,1))>ABS(HIGH-DELAY(LOW,1)) ? 
    # ABS(HIGH-DELAY(CLOSE,1))+ABS(LOW-DELAY(CLOSE,1))/2+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4:
    # (ABS(LOW-DELAY(CLOSE,1))>ABS(HIGH-DELAY(LOW,1)) & ABS(LOW-DELAY(CLOSE,1))>ABS(HIGH-DELAY(CLOSE,1)) ?
    # ABS(LOW-DELAY(CLOSE,1))+ABS(HIGH-DELAY(CLOSE,1))/2+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4:
    # ABS(HIGH-DELAY(LOW,1))+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4)))
    # *MAX(ABS(HIGH-DELAY(CLOSE,1)),ABS(LOW-DELAY(CLOSE,1))),20)
    part1 = data['closePrice'] * 1.5 - data['openPrice'] * 0.5 - data['openPrice'].shift(1)
    part2 = abs(data['highestPrice']-data['closePrice'].shift(1)) + abs(data['lowestPrice']-data['closePrice'].shift(1)) / 2.0 + abs(data['closePrice']-data['openPrice']).shift(1) / 4.0
    condition1 = np.logical_and(abs(data['highestPrice']-data['closePrice'].shift(1)) > abs(data['lowestPrice']-data['closePrice'].shift(1)), 
                               abs(data['highestPrice']-data['closePrice'].shift(1)) > abs(data['highestPrice']-data['lowestPrice'].shift(1)))
    condition2 = np.logical_and(abs(data['lowestPrice']-data['closePrice'].shift(1)) > abs(data['highestPrice']-data['lowestPrice'].shift(1)), 
                               abs(data['lowestPrice']-data['closePrice'].shift(1)) > abs(data['highestPrice']-data['closePrice'].shift(1)))
    part2[~condition1 & condition2] = abs(data['lowestPrice']-data['closePrice'].shift(1)) + abs(data['highestPrice']-data['closePrice'].shift(1)) / 2.0 + abs(data['closePrice']-data['openPrice']).shift(1) / 4.0
    part2[~condition1 & ~condition2] = abs(data['highestPrice']-data['lowestPrice'].shift(1)) + abs(data['closePrice']-data['openPrice']).shift(1) / 4.0
    part3 = np.maximum(abs(data['highestPrice']-data['closePrice'].shift(1)), abs(data['lowestPrice']-data['closePrice'].shift(1)))
    alpha = (part1 / part2 * part3 * 16.0).rolling(window=20, min_periods=20).sum().iloc[-1]
    return alpha

def alpha056(data, dependencies=['openPrice', 'highestPrice', 'lowestPrice', 'turnoverVol'], max_window=73):
    # RANK(OPEN-TSMIN(OPEN,12))<RANK(RANK(CORR(SUM((HIGH +LOW)/2,19),SUM(MEAN(VOLUME,40),19),13))^5)
    # \u8fd9\u91cc\u5c31\u4f1a\u6709\u968f\u673a\u6027,0/1
    part1 = (data['openPrice'] - data['openPrice'].rolling(window=12, min_periods=12).min()).rank(axis=0, pct=True)
    t1 = (data['highestPrice']*0.5+data['lowestPrice']*0.5).rolling(window=19, min_periods=19).sum()
    t2 = data['turnoverVol'].rolling(window=40,min_periods=40).mean().rolling(window=19, min_periods=19).sum()
    part2 = ((t1.rolling(window=13, min_periods=13).corr(t2).rank(axis=0, pct=True)) ** 5).rank(axis=0, pct=True)
    return (part2-part1).iloc[-1]

def alpha057(data, dependencies=['KDJ_K'], max_window=11):
    # SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1)
    # KDJ_K
    part1 =data['closePrice']- data['closePrice'].rolling(window=9, min_periods=9).min()
    part2=data['highestPrice'].rolling(window=9, min_periods=9).max()-data['lowestPrice'].rolling(window=9, min_periods=9).min()
    return SMA(list(part1/part2*100)[-3:],3,1)

def alpha058(data, dependencies=['closePrice'], max_window=20):
    # COUNT(CLOSE>DELAY(CLOSE,1),20)/20*100
    return ((data['closePrice'].diff(1) > 0.0).rolling(window=20, min_periods=20).sum() / 20.0 * 100).iloc[-1]

def alpha059(data, dependencies=['closePrice', 'lowestPrice', 'highestPrice'], max_window=21):
    # SUM((CLOSE=DELAY(CLOSE,1)?0:CLOSE-(CLOSE>DELAY(CLOSE,1)?MIN(LOW,DELAY(CLOSE,1)):MAX(HIGH,DELAY(CLOSE,1)))),20)
    # \u53d7\u4ef7\u683c\u5c3a\u5ea6\u5f71\u54cd
    alpha =data['closePrice']
    condition1 = data['closePrice'].diff(1) > 0.0
    condition2 = data['closePrice'].diff(1) < 0.0
    alpha[condition1] = data['closePrice'][condition1] - np.minimum(data['lowestPrice'][condition1], data['closePrice'].shift(1)[condition1])
    alpha[condition2] = data['closePrice'][condition2] - np.maximum(data['highestPrice'][condition2], data['closePrice'].shift(1)[condition2])
    alpha = alpha.rolling(window=20, min_periods=20).sum().iloc[-1]
    return alpha

def alpha060(data, dependencies=['closePrice', 'openPrice', 'lowestPrice', 'highestPrice', 'turnoverVol'], max_window=21):
    # SUM((2*CLOSE-LOW-HIGH)./(HIGH-LOW).*VOLUME,20)
    part1 = (2*data['closePrice']-data['lowestPrice']-data['highestPrice']) / (data['highestPrice']-data['lowestPrice']) * data['turnoverVol']
    return part1.rolling(window=20, min_periods=20).sum().iloc[-1]

def alpha061(data, dependencies=['lowestPrice', 'turnoverValue', 'turnoverVol'], max_window=106):
    # MAX(RANK(DECAYLINEAR(DELTA(VWAP,1),12)),RANK(DECAYLINEAR(RANK(CORR(LOW,MEAN(VOLUME,80),8)),17)))*-1
    w12 = np.array(range(1, 13)).reshape(-1)
    w17 = np.array(range(1, 18)).reshape(-1)
    turnover_ma = data['turnoverVol'].rolling(window=80, min_periods=80).mean()
    part1 = (data['turnoverValue']/data['turnoverVol']).diff(periods=1).rolling(window=12, min_periods=12).apply(lambda x: np.dot(x, w12)).rank(axis=0, pct=True)
    part2 = (turnover_ma.rolling(window=8, min_periods=8).corr(data['lowestPrice']).rank(axis=0,pct=True)).rolling(window=17, min_periods=17).apply(lambda x: np.dot(x, w17)).rank(axis=0, pct=True)
    alpha = np.maximum(part1, part2).iloc[-1] * (-1)
    return alpha

def alpha062(data, dependencies=['turnoverVol', 'highestPrice'], max_window=5):
    # -1*CORR(HIGH,RANK(VOLUME),5)
    return data['turnoverVol'].rank(axis=0, pct=True).rolling(window=5, min_periods=5).corr(data['highestPrice']).iloc[-1] * (-1)

def alpha063(data, dependencies=['closePrice'], max_window=7):
    # SMA(MAX(CLOSE-DELAY(CLOSE,1),0),6,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),6,1)*100
    part1 = (np.maximum(data['closePrice'].diff(1), 0.0)).ewm(adjust=False, alpha=float(1)/6, min_periods=0, ignore_na=False).mean()
    part2 = abs(data['closePrice']).diff(1).ewm(adjust=False, alpha=float(1)/6, min_periods=0, ignore_na=False).mean()
    return (part1/part2*100.0).iloc[-1]
    
def alpha064(data, dependencies=['closePrice', 'turnoverValue', 'turnoverVol'], max_window=93):
    # (MAX(RANK(DECAYLINEAR(CORR(RANK(VWAP),RANK(VOLUME),4),4)),RANK(DECAYLINEAR(MAX(CORR(RANK(CLOSE),RANK(MEAN(VOLUME,60)),4),13),14)))*-1)
    # \u770b\u4e0a\u53bb\u662fTSMAX
    vwap = data['turnoverValue'] / data['turnoverVol']
    w4 = np.array(range(1, 5)).reshape(-1)
    w14 = np.array(range(1, 15)).reshape(-1)
    part1 = (vwap.rank(axis=0, pct=True).rolling(window=4, min_periods=4).corr(data['turnoverVol'].rank(axis=0, pct=True))).rolling(window=4, min_periods=4).apply(lambda x: np.dot(x, w4)).rank(axis=0, pct=True)
    part2 = (data['turnoverVol'].rolling(window=60, min_periods=60).mean().rank(axis=0, pct=True)).rolling(window=4, min_periods=4).corr(data['closePrice'].rank(axis=0, pct=True))
    part2 = (part2.rolling(window=13, min_periods=13).max()).rolling(window=14, min_periods=14).apply(lambda x: np.dot(x, w14)).rank(axis=0,pct=True)
    alpha = np.maximum(part1, part2).iloc[-1] * (-1)
    return alpha

def alpha065(data, dependencies=['closePrice'], max_window=6):
    # MEAN(CLOSE,6)/CLOSE
    return (data['closePrice'].rolling(window=6, min_periods=6).mean() / data['closePrice']).iloc[-1]

def alpha066(data, dependencies=['BIAS5'], max_window=6):
    # (CLOSE-MEAN(CLOSE,6))/MEAN(CLOSE,6)*100
    # BIAS6\uff0c\u7528BIAS5\u7b80\u5355\u66ff\u6362\u4e0b
    part1=data['closePrice'].iloc[-1]-data['closePrice'].mean()
    return part1/data['closePrice'].mean()*100

def alpha067(data, dependencies=['closePrice'], max_window=25):
    # SMA(MAX(CLOSE-DELAY(CLOSE,1),0),24,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),24,1)*100
    # RSI24
    part1 = (np.maximum(data['closePrice'].diff(1), 0.0)).ewm(adjust=False, alpha=float(1)/24, min_periods=0, ignore_na=False).mean()
    part2 = (abs(data['closePrice'].diff(1))).ewm(adjust=False, alpha=float(1)/24, min_periods=0, ignore_na=False).mean()
    return (part1 / part2 * 100).iloc[-1]

def alpha068(data, dependencies=['highestPrice', 'lowestPrice', 'turnoverVol'], max_window=16):
    # SMA(((HIGH+LOW)/2-(DELAY(HIGH,1)+DELAY(LOW,1))/2)*(HIGH-LOW)/VOLUME,15,2)
    part1 = (data['highestPrice'].diff(1) * 0.5 + data['lowestPrice'].diff(1) * 0.5) * (data['highestPrice'] - data['lowestPrice']) / data['turnoverVol']
    return part1.ewm(adjust=False, alpha=float(2)/15, min_periods=0, ignore_na=False).mean().iloc[-1]

def alpha069(data, dependencies=['openPrice', 'highestPrice', 'lowestPrice'], max_window=21):
    # (SUM(DTM,20)>SUM(DBM,20)?
        #(SUM(DTM,20)-SUM(DBM,20))/SUM(DTM,20):
        #(SUM(DTM,20)=SUM(DBM,20)?0:
            #(SUM(DTM,20)-SUM(DBM,20))/SUM(DBM,20)))
    # DTM: (OPEN<=DELAY(OPEN,1)?0:MAX((HIGH-OPEN),(OPEN-DELAY(OPEN,1))))
    # DBM: (OPEN>=DELAY(OPEN,1)?0:MAX((OPEN-LOW),(OPEN-DELAY(OPEN,1))))
    dtm=(data['openPrice'].diff(1) <= 0) * np.maximum(data['highestPrice']-data['openPrice'],data['openPrice'].diff(1))
    dbm=(data['openPrice'].diff(1) >= 0) * np.maximum(data['openPrice']-data['lowestPrice'],data['openPrice'].diff(1))
    dtm_sum = dtm.rolling(window=20, min_periods=20).sum().iloc[-1]
    dbm_sum = dbm.rolling(window=20, min_periods=20).sum().iloc[-1]
    if dtm_sum>dbm_sum:
        return (dtm_sum-dbm_sum)/dtm_sum
    elif dtm_sum==dbm_sum:return 0
    else:return (dtm_sum-dbm_sum)/dbm_sum


def alpha070(data, dependencies=['turnoverValue'], max_window=6):
    # STD(AMOUNT,6)
    return data['turnoverValue'].rolling(window=6, min_periods=6).std().iloc[-1]

def alpha071(data, dependencies=['closePrice'], max_window=25):
    # (CLOSE-MEAN(CLOSE,24))/MEAN(CLOSE,24)*100
    # BIAS24
    close_ma = data['closePrice'].rolling(window=24, min_periods=24).mean()
    return ((data['closePrice'] - close_ma) / close_ma * 100).iloc[-1]

def alpha072(data, dependencies=['highestPrice', 'lowestPrice', 'closePrice'], max_window=22):
    # SMA((TSMAX(HIGH,6)-CLOSE)/(TSMAX(HIGH,6)-TSMIN(LOW,6))*100,15,1)
    part1 = (data['highestPrice'].rolling(window=6, min_periods=6).max() - data['closePrice']) / (data['highestPrice'].rolling(window=6, min_periods=6).max() - data['lowestPrice'].rolling(window=6,min_periods=6).min()) * 100.0
    return part1.ewm(adjust=False, alpha=float(1)/15, min_periods=0, ignore_na=False).mean().iloc[-1]

def alpha073(data, dependencies=['turnoverValue', 'turnoverVol', 'closePrice'], max_window=38):
    # ((TSRANK(DECAYLINEAR(DECAYLINEAR(CORR(CLOSE,VOLUME,10),16),4),5)-RANK(DECAYLINEAR(CORR(VWAP,MEAN(VOLUME,30),4),3)))*-1)
    vwap = data['turnoverValue'] / data['turnoverVol']
    w16 =np.array(range(1, 17)).reshape(-1)
    w4 =np.array(range(1, 5)).reshape(-1)
    w3 =np.array(range(1, 4)).reshape(-1)
    part1 = (data['closePrice'].rolling(window=10, min_periods=10).corr(data['turnoverVol'])).rolling(window=16, min_periods=16).apply(lambda x: np.dot(x, w16))
    part1 = (part1.rolling(window=4, min_periods=4).apply(lambda x: np.dot(x, w4))).rolling(window=5, min_periods=5).apply(lambda x: stats.rankdata(x)[-1]/5.0)
    part2 = data['turnoverVol'].rolling(window=30, min_periods=30).mean().rolling(window=4, min_periods=4).corr(vwap)
    part2 = part2.rolling(window=3, min_periods=3).apply(lambda x: np.dot(x, w3)).rank(axis=0, pct=True)
    return (part1 - part2).iloc[-1] * (-1)

def alpha074(data, dependencies=['lowestPrice', 'turnoverValue', 'turnoverVol'], max_window=68):
    # RANK(CORR(SUM(LOW*0.35+VWAP*0.65,20),SUM(MEAN(VOLUME,40),20),7))+RANK(CORR(RANK(VWAP),RANK(VOLUME),6))
    vwap = data['turnoverValue'] / data['turnoverVol']
    part1 = ((data['lowestPrice'] * 0.35 + vwap * 0.65).rolling(window=20, min_periods=20).sum()).rolling(window=7, min_periods=7).corr((data['turnoverVol'].rolling(window=40,min_periods=40).mean()).rolling(window=20, min_periods=20).sum()).rank(axis=0, pct=True)
    part2 = (vwap.rank(axis=0,pct=True).rolling(window=6, min_periods=6).corr(data['turnoverVol'].rank(axis=0, pct=True))).rank(axis=0, pct=True)
    return (part1 + part2).iloc[-1]

def alpha075(data, dependencies=['closePrice', 'openPrice'], max_window=51):
    # COUNT(CLOSE>OPEN & BANCHMARK_INDEX_CLOSE<BANCHMARK_INDEX_OPEN,50)/COUNT(BANCHMARK_INDEX_CLOSE<BANCHMARK_INDEX_OPEN,50)
    # 简化为等权benchmark
    bm = (data['closePrice'].mean(axis=0) < data['openPrice'].mean(axis=0))
    print(bm)
    bm_den = pd.DataFrame(data=np.repeat(bm.reshape(len(bm),1), len(data['closePrice']), axis=0), index=data['closePrice'].index)
    alpha = np.logical_and(data['closePrice'] > data['openPrice'], bm_den).rolling(window=50, min_periods=50).sum() / bm_den.rolling(window=50, min_periods=50).sum()
    return alpha.iloc[-1]

def alpha076(data, dependencies=['closePrice', 'turnoverVol'], max_window=21):
    # STD(ABS(CLOSE/DELAY(CLOSE,1)-1)/VOLUME,20)/MEAN(ABS(CLOSE/DELAY(CLOSE,1)-1)/VOLUME,20)
    ret_vol = abs(data['closePrice'].pct_change(periods=1))/data['turnoverVol']
    return (ret_vol.rolling(window=20, min_periods=20).std() / ret_vol.rolling(window=20, min_periods=20).mean()).iloc[-1]

def alpha077(data, dependencies=['lowestPrice', 'highestPrice', 'turnoverValue', 'turnoverVol'], max_window=50):
    # MIN(RANK(DECAYLINEAR(HIGH*0.5+LOW*0.5-VWAP,20)),RANK(DECAYLINEAR(CORR(HIGH*0.5+LOW*0.5,MEAN(VOLUME,40),3),6)))
    w6 = np.array(range(1, 7)).reshape(-1)
    w20 = np.array(range(1, 21)).reshape(-1)
    part1 = (data['highestPrice'] * 0.5 + data['lowestPrice'] * 0.5 - data['turnoverValue'] / data['turnoverVol']).rolling(window=20, min_periods=20).apply(lambda x: np.dot(x, w20)).rank(axis=0, pct=True)
    part2 = ((data['highestPrice'] * 0.5 + data['lowestPrice'] * 0.5).rolling(window=3, min_periods=3).corr(data['turnoverVol'].rolling(window=40, min_periods=40).mean())).rolling(window=6, min_periods=6).apply(lambda x: np.dot(x, w6)).rank(axis=0, pct=True)
    return np.minimum(part1, part2).iloc[-1]
    
def alpha078(data, dependencies=['CCI10'], max_window=12):
    # ((HIGH+LOW+CLOSE)/3-MA((HIGH+LOW+CLOSE)/3,12))
    #/(0.015*MEAN(ABS(CLOSE-MEAN((HIGH+LOW+CLOSE)/3,12)),12))
    # \u76f8\u5f53\u4e8e\u662fCCI12, \u7528CCI10\u66ff\u4ee3
    part1=(data['highestPrice']+data['lowestPrice']+data['closePrice'])/3
    part2=part1.iloc[-1]-part1.rolling(window=12, min_periods=12).mean().iloc[-1]
    part3=(data['closePrice']-part1.rolling(window=12, min_periods=12).mean()).abs().mean()*0.015
    return part2/part3

def alpha079(data, dependencies=['closePrice', 'openPrice'], max_window=13):
    # SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100
    # \u5c31\u662fRSI12
    part1 = (np.maximum(data['closePrice'].diff(1), 0.0)).ewm(adjust=False, alpha=float(1)/12, min_periods=0, ignore_na=False).mean()
    part2 = (abs(data['closePrice'].diff(1))).ewm(adjust=False, alpha=float(1)/12, min_periods=0, ignore_na=False).mean()
    return (part1 / part2 * 100).iloc[-1]

def alpha080(data, dependencies=['turnoverVol'], max_window=6):
    # (VOLUME-DELAY(VOLUME,5))/DELAY(VOLUME,5)*100
    return (data['turnoverVol'].pct_change(periods=5) * 100.0).iloc[-1]

def alpha081(data, dependencies=['turnoverVol'], max_window=21):
    # SMA(VOLUME,21,2)
    return data['turnoverVol'].ewm(adjust=False, alpha=float(2)/21, min_periods=0, ignore_na=False).mean().iloc[-1]

def alpha082(data, dependencies=['lowestPrice', 'highestPrice', 'closePrice'], max_window=26):
    # SMA((TSMAX(HIGH,6)-CLOSE)/(TSMAX(HIGH,6)-TSMIN(LOW,6))*100,20,1)
    # RSV\u6280\u672f\u6307\u6807\u53d8\u79cd
    part1 = (data['highestPrice'].rolling(window=6,min_periods=6).max()-data['closePrice']) / (data['highestPrice'].rolling(window=6,min_periods=6).max()-data['lowestPrice'].rolling(window=6,min_periods=6).min()) * 100
    alpha = part1.ewm(adjust=False, alpha=float(1)/20, min_periods=0, ignore_na=False).mean().iloc[-1]
    return alpha

def alpha083(data, dependencies=['highestPrice', 'turnoverVol'], max_window=5):
    # (-1*RANK(COVIANCE(RANK(HIGH),RANK(VOLUME),5)))
    alpha = COVIANCE(sorted(data['highestPrice']),sorted(data['turnoverVol']),5)*-1
    return alpha

def alpha084(data, dependencies=['closePrice', 'turnoverVol'], max_window=21):
    # SUM((CLOSE>DELAY(CLOSE,1)?VOLUME:(CLOSE<DELAY(CLOSE,1)?-VOLUME:0)),20)
    part1 = np.sign(data['closePrice'].diff(1)) * data['turnoverVol']
    return part1.rolling(window=20, min_periods=20).sum().iloc[-1]

def alpha085(data, dependencies=['closePrice', 'turnoverVol'], max_window=40):
    # TSRANK(VOLUME/MEAN(VOLUME,20),20)*TSRANK(a-1*DELTA(CLOSE,7),8)
    part1 = (data['turnoverVol'] / data['turnoverVol'].rolling(window=20,min_periods=20).mean()).iloc[-20:].rank(axis=0, pct=True)
    part2 = (data['closePrice'].diff(7) * (-1)).iloc[-8:].rank(axis=0, pct=True)
    return (part1 * part2).iloc[-1]

def alpha086(data, dependencies=['closePrice'], max_window=21):
    # ((0.25<((DELAY(CLOSE,20)-DELAY(CLOSE,10))/10-(DELAY(CLOSE,10)-CLOSE)/10))?-1:((((DELAY(CLOSE,20)-DELAY(CLOSE,10))/10-(DELAY(CLOSE,10)-CLOSE)/10)<0)?1:(DELAY(CLOSE,1)-CLOSE)))
    condition1 = (data['closePrice'].shift(20) * 0.1 + data['closePrice'] * 0.1 - data['closePrice'].shift(10) * 0.2) > 0.25
    condition2 = (data['closePrice'].shift(20) * 0.1 + data['closePrice'] * 0.1 - data['closePrice'].shift(10) * 0.2) < 0.0
    alpha = data['closePrice']*-1
    alpha[~condition1 & condition2] = 1.0
    alpha[~condition1 & ~condition2] = data['closePrice'].diff(1)[~condition1 & ~condition2] * (-1)
    return alpha.iloc[-1]

def alpha087(data, dependencies=['turnoverValue', 'turnoverVol', 'lowestPrice', 'highestPrice', 'openPrice'], max_window=18):
    # (RANK(DECAYLINEAR(DELTA(VWAP,4),7))+TSRANK(DECAYLINEAR((LOW-VWAP)/(OPEN-(HIGH+LOW)/2),11),7))*-1
    vwap = data['turnoverValue'] / data['turnoverVol']
    w7 = np.array(range(1, 8)).reshape(-1)
    w11 = np.array(range(1, 12)).reshape(-1)
    part1 = (vwap.diff(4).rolling(window=7, min_periods=7).apply(lambda x: np.dot(x, w7))).rank(axis=0, pct=True)
    part2 = (data['lowestPrice']-vwap)/(data['openPrice']-data['highestPrice']*0.5-data['lowestPrice']*0.5)
    part2 = (part2.rolling(window=11, min_periods=11).apply(lambda x: np.dot(x, w11))).iloc[-7:].rank(axis=0, pct=True)
    return (part1 + part2).iloc[-1] * (-1)

def alpha088(data, dependencies=['REVS20'], max_window=20):
    # (CLOSE-DELAY(CLOSE,20))/DELAY(CLOSE,20)*100
    # \u5c31\u662fREVS20
    return (data['closePrice'].iloc[-1]-data['closePrice'].iloc[-20])/data['closePrice'].iloc[-20]*100

def alpha089(data, dependencies=['closePrice'], max_window=37):
    # 2*(SMA(CLOSE,13,2)-SMA(CLOSE,27,2)-SMA(SMA(CLOSE,13,2)-SMA(CLOSE,27,2),10,2))
    part1 = data['closePrice'].ewm(adjust=False, alpha=float(2)/13, min_periods=0, ignore_na=False).mean() - data['closePrice'].ewm(adjust=False, alpha=float(2)/27, min_periods=0, ignore_na=False).mean()
    alpha = (part1 - part1.ewm(adjust=False, alpha=float(2)/10, min_periods=0, ignore_na=False).mean()) * 2.0
    return alpha.iloc[-1]

def alpha090(data, dependencies=['turnoverValue', 'turnoverVol'], max_window=5):
    # (RANK(CORR(RANK(VWAP),RANK(VOLUME),5))*-1)
    return CORR(sorted(data['highestPrice']),sorted(data['turnoverVol']),5)*-1
    

def alpha091(data, dependencies=['closePrice', 'turnoverVol', 'lowestPrice'], max_window=45):
    # ((RANK(CLOSE-MAX(CLOSE,5))*RANK(CORR(MEAN(VOLUME,40),LOW,5)))*-1)
    # \u611f\u89c9\u662fTSMAX
    part1 = (data['closePrice'] - data['closePrice'].rolling(window=5, min_periods=5).max()).rank(axis=0, pct=True)
    part2 = (data['turnoverVol'].rolling(window=40, min_periods=40).mean()).rolling(window=5, min_periods=5).corr(data['lowestPrice']).rank(axis=0, pct=True)
    return (part1 * part2).iloc[-1] * (-1)

def alpha092(data, dependencies=['closePrice', 'turnoverValue', 'turnoverVol'], max_window=209):
    # (MAX(RANK(DECAYLINEAR(DELTA(CLOSE*0.35+VWAP*0.65,2),3)),TSRANK(DECAYLINEAR(ABS(CORR((MEAN(VOLUME,180)),CLOSE,13)),5),15))*-1)
    w3 = np.array(range(1, 4)).reshape(-1)
    w5 = np.array(range(1, 6)).reshape(-1)
    part1 = ((data['closePrice'] * 0.35 + data['turnoverValue'] / data['turnoverVol'] * 0.65).diff(2)).rolling(window=3, min_periods=3).apply(lambda x: np.dot(x, w3)).rank(axis=0, pct=True)
    part2 = abs((data['turnoverVol'].rolling(window=180, min_periods=180).mean()).rolling(window=13, min_periods=13).corr(data['closePrice']))
    part2 = (part2.rolling(window=5, min_periods=5).apply(lambda x: np.dot(x, w5))).iloc[-15:].rank(axis=0, pct=True)
    return np.maximum(part1.iloc[-1], part2.iloc[-1]) * (-1)

def alpha093(data, dependencies=['openPrice', 'lowestPrice'], max_window=21):
    # SUM(OPEN>=DELAY(OPEN,1)?0:MAX(OPEN-LOW,OPEN-DELAY(OPEN,1)),20)
    condition = data['openPrice'].diff(1) >= 0.0
    alpha= data['openPrice']
    alpha[~condition] = np.maximum(data['openPrice'] - data['lowestPrice'], data['openPrice'].diff(1))[~condition]
    return alpha.rolling(window=20, min_periods=20).sum().iloc[-1]

def alpha094(data, dependencies=['closePrice', 'turnoverVol'], max_window=31):
    # SUM((CLOSE>DELAY(CLOSE,1)?VOLUME:(CLOSE<DELAY(CLOSE,1)?-VOLUME:0)),30)
    part1 = np.sign(data['closePrice'].diff(1)) * data['turnoverVol']
    return part1.rolling(window=30, min_periods=30).sum().iloc[-1]

def alpha095(data, dependencies=['turnoverValue'], max_window=20):
    # STD(AMOUNT,20), \u8fd9\u91cc\u5e94\u8be5\u6ca1\u6709\u590d\u6743
    return data['turnoverValue'].rolling(window=20, min_periods=20).std().iloc[-1]

def alpha096(data, dependencies=['KDJ_D'], max_window=13):
    # SMA(SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1),3,1)
    # \u5c31\u662fKDJ_D
    part1 =data['closePrice']- data['closePrice'].rolling(window=9, min_periods=9).min()
    part2=data['highestPrice'].rolling(window=9, min_periods=9).max()-data['lowestPrice'].rolling(window=9, min_periods=9).min()
    part4=[SMA(list(part1/part2*100)[-5:-2],3,1),SMA(list(part1/part2*100)[-4:-1],3,1),SMA(list(part1/part2*100)[-3:],3,1)]
    part5=SMA(part4,3,1)
    return part5

def alpha097(data, dependencies=['VSTD10'], max_window=10):
    # STD(VOLUME,10)
    # \u5c31\u662fVSTD10
    return STD(data['turnoverVol'],10)

def alpha098(data, dependencies=['closePrice'], max_window=201):
    # (DELTA(SUM(CLOSE,100)/100,100)/DELAY(CLOSE,100)<=0.05)?(-1*(CLOSE-TSMIN(CLOSE,100))):(-1*DELTA(CLOSE,3))
    condition1 = (data['closePrice'].rolling(window=100, min_periods=100).sum() / 100).diff(periods=100) / data['closePrice'].shift(100) <= 0.05
    alpha = (data['closePrice'] - data['closePrice'].rolling(window=100, min_periods=100).min()) * (-1)
    alpha[~condition1] = data['closePrice'].diff(3)[~condition1] * (-1)
    return alpha.iloc[-1]

def alpha099(data, dependencies=['closePrice', 'turnoverVol'], max_window=5):
    # (-1*RANK(COVIANCE(RANK(CLOSE),RANK(VOLUME),5)))
    return COVIANCE(sorted(data['closePrice']),sorted(data['turnoverVol']),5)*-1


def alpha100(data, dependencies=['VSTD20'], max_window=20):
    # STD(VOLUME,20), \u5c31\u662fVSTD20
    return STD(data['turnoverVol'],20)

def alpha101(data, dependencies=['turnoverValue', 'turnoverVol', 'highestPrice', 'closePrice'], max_window=82):
    # (RANK(CORR(CLOSE,SUM(MEAN(VOLUME,30),37),15)) < RANK(CORR(RANK(HIGH*0.1+VWAP*0.9),RANK(VOLUME),11)))*-1
    part1 = (data['turnoverVol'].rolling(window=30, min_periods=30).mean()).rolling(window=37, min_periods=37).sum()
    part1 = (part1.rolling(window=15, min_periods=15).corr(data['closePrice'])).rank(axis=0, pct=True)
    part2 = (data['highestPrice'] * 0.1 + data['turnoverValue'] / data['turnoverVol'] * 0.9).rank(axis=0, pct=True)
    part2 = (part2.rolling(window=11, min_periods=11).corr(data['turnoverVol'].rank(axis=0, pct=True))).rank(axis=0, pct=True)
    return (part2 - part1).iloc[-1] * (-1)

def alpha102(data, dependencies=['turnoverVol'], max_window=7):
    # SMA(MAX(VOLUME-DELAY(VOLUME,1),0),6,1)/SMA(ABS(VOLUME-DELAY(VOLUME,1)),6,1)*100
    part1 = (np.maximum(data['turnoverVol'].diff(1), 0.0)).ewm(adjust=False, alpha=float(1)/6, min_periods=0, ignore_na=False).mean()
    part2 = abs(data['turnoverVol'].diff(1)).ewm(adjust=False, alpha=float(1)/6, min_periods=0, ignore_na=False).mean()
    return (part1 / part2).iloc[-1] * 100

def alpha103(data, dependencies=['lowestPrice'], max_window=20):
    # ((20-LOWDAY(LOW,20))/20)*100
    return (20 - data['lowestPrice'].rolling(window=20, min_periods=20).apply(lambda x: 19-x.argmin(axis=0))).iloc[-1] * 5.0

def alpha104(data, dependencies=['highestPrice', 'turnoverVol', 'closePrice'], max_window=20):
    # -1*(DELTA(CORR(HIGH,VOLUME,5),5)*RANK(STD(CLOSE,20)))
    part1 = (data['highestPrice'].rolling(window=5, min_periods=5).corr(data['turnoverVol'])).diff(5)
    part2 = (data['closePrice'].rolling(window=20, min_periods=20).std()).rank(axis=0, pct=True)
    return (part1 * part2).iloc[-1] * (-1)

def alpha105(data, dependencies=['openPrice', 'turnoverVol'], max_window=10):
    # -1*CORR(RANK(OPEN),RANK(VOLUME),10)
    alpha = (data['openPrice'].rank(axis=0, pct=True)).rolling(window=10, min_periods=10).corr(data['turnoverVol'].rank(axis=0, pct=True))
    return alpha.iloc[-1] * (-1)

def alpha106(data, dependencies=['closePrice'], max_window=21):
    # CLOSE-DELAY(CLOSE,20)
    return data['closePrice'].diff(20).iloc[-1]

def alpha107(data, dependencies=['openPrice', 'closePrice', 'highestPrice', 'lowestPrice'], max_window=2):
    # (-1*RANK(OPEN-DELAY(HIGH,1)))*RANK(OPEN-DELAY(CLOSE,1))*RANK(OPEN-DELAY(LOW,1))
    part1 = data['openPrice'] - data['highestPrice'].shift(1)
    part2 = data['openPrice'] - data['closePrice'].shift(1)
    part3 = data['openPrice'] - data['lowestPrice'].shift(1)
    return (part1 * part2 * part3).iloc[-1] * (-1)

def alpha108(data, dependencies=['highestPrice', 'turnoverValue', 'turnoverVol'], max_window=126):
    # (RANK(HIGH-MIN(HIGH,2))^RANK(CORR(VWAP,MEAN(VOLUME,120),6)))*-1
    part1 = (data['highestPrice'] - data['highestPrice'].rolling(window=2,min_periods=2).min()).rank(axis=0, pct=True)
    part2 = ((data['turnoverVol'].rolling(window=120, min_periods=120).mean()).rolling(window=6, min_periods=6).corr(data['turnoverValue']/data['turnoverVol'])).rank(axis=0, pct=True)
    return (part1 ** part2).iloc[-1] * (-1)

def alpha109(data, dependencies=['highestPrice', 'lowestPrice'], max_window=20):
    # SMA(HIGH-LOW,10,2)/SMA(SMA(HIGH-LOW,10,2),10,2)
    part1 = (data['highestPrice']-data['lowestPrice']).ewm(adjust=False, alpha=float(2)/10, min_periods=0, ignore_na=False).mean()
    return (part1 / part1.ewm(adjust=False, alpha=float(2)/10, min_periods=0, ignore_na=False).mean()).iloc[-1]

def alpha110(data, dependencies=['closePrice', 'highestPrice', 'lowestPrice'], max_window=21):
    # SUM(MAX(0,HIGH-DELAY(CLOSE,1)),20)/SUM(MAX(0,DELAY(CLOSE,1)-LOW),20)*100
    part1 = (np.maximum(data['highestPrice']-data['closePrice'].shift(1), 0.0)).rolling(window=20,min_periods=20).sum()
    part2 = (np.maximum(data['closePrice'].shift(1)-data['lowestPrice'], 0.0)).rolling(window=20,min_periods=20).sum()
    return (part1 / part2).iloc[-1] * 100.0

def alpha111(data, dependencies=['lowestPrice', 'highestPrice', 'closePrice', 'turnoverVol'], max_window=11):
    # SMA(VOL*(2*CLOSE-LOW-HIGH)/(HIGH-LOW),11,2)-SMA(VOL*(2*CLOSE-LOW-HIGH)/(HIGH-LOW),4,2)
    win_vol = data['turnoverVol'] * (data['closePrice']*2-data['lowestPrice']-data['highestPrice']) / (data['highestPrice']-data['lowestPrice'])
    alpha = win_vol.ewm(adjust=False, alpha=float(2)/11, min_periods=0, ignore_na=False).mean() - win_vol.ewm(adjust=False, alpha=float(2)/4, min_periods=0, ignore_na=False).mean()
    return alpha.iloc[-1]

def alpha112(data, dependencies=['closePrice'], max_window=13):
    # (SUM((CLOSE-DELAY(CLOSE,1)>0?CLOSE-DELAY(CLOSE,1):0),12)-SUM((CLOSE-DELAY(CLOSE,1)<0?ABS(CLOSE-DELAY(CLOSE,1)):0),12))
    # /(SUM((CLOSE-DELAY(CLOSE,1)>0?CLOSE-DELAY(CLOSE,1):0),12)+SUM((CLOSE-DELAY(CLOSE,1)<0?ABS(CLOSE-DELAY(CLOSE,1)):0),12))*100
    part1 = (np.maximum(data['closePrice'].diff(1), 0.0)).rolling(window=12, min_periods=12).sum()
    part2 = abs(np.minimum(data['closePrice'].diff(1), 0.0)).rolling(window=12, min_periods=12).sum()
    return ((part1-part2) / (part1+part2)).iloc[-1] * 100

def alpha113(data, dependencies=['closePrice', 'turnoverVol'], max_window=28):
    # -1*RANK(SUM(DELAY(CLOSE,5),20)/20)*CORR(CLOSE,VOLUME,2)*RANK(CORR(SUM(CLOSE,5),SUM(CLOSE,20),2))
    part1 = (data['closePrice'].shift(5).rolling(window=20, min_periods=20).mean()).rank(axis=0, pct=True)
    part2 = data['closePrice'].rolling(window=2, min_periods=2).corr(data['turnoverVol'])
    part3 = ((data['closePrice'].rolling(window=5, min_periods=5).sum()).rolling(window=2, min_periods=2).corr(data['closePrice'].rolling(window=20, min_periods=20).sum())).rank(axis=0, pct=True)
    return (part1 * part2 * part3).iloc[-1] * (-1)

def alpha114(data, dependencies=['highestPrice', 'lowestPrice', 'closePrice', 'turnoverValue', 'turnoverVol'], max_window=8):
    # RANK(DELAY((HIGH-LOW)/(SUM(CLOSE,5)/5),2))*RANK(RANK(VOLUME))/((HIGH-LOW)/(SUM(CLOSE,5)/5)/(VWAP-CLOSE))
    # RANK/RANK\u8c8c\u4f3c\u6ca1\u5fc5\u8981
    part1 = ((data['highestPrice']-data['lowestPrice'])/(data['closePrice'].rolling(window=5,min_periods=5).mean())).shift(2).rank(axis=0,pct=True)
    part2 = data['turnoverVol'].rank(axis=0, pct=True).rank(axis=0, pct=True)
    part3 = (data['highestPrice']-data['lowestPrice'])/(data['closePrice'].rolling(window=5,min_periods=5).mean())/(data['turnoverValue']/data['turnoverVol']-data['closePrice'])
    return (part1*part2*part3).iloc[-1]

def alpha115(data, dependencies=['highestPrice', 'lowestPrice', 'turnoverVol', 'closePrice'], max_window=40):
    # (RANK(CORR(HIGH*0.9+CLOSE*0.1,MEAN(VOLUME,30),10))^RANK(CORR(TSRANK((HIGH+LOW)/2,4),TSRANK(VOLUME,10),7)))
    part1 = ((data['highestPrice'] * 0.9 + data['closePrice'] * 0.1).rolling(window=10, min_periods=10).corr(
        data['turnoverVol'].rolling(window=30, min_periods=30).mean())).rank(axis=0, pct=True)
    part2 = (((data['highestPrice'] * 0.5 + data['lowestPrice'] * 0.5).rolling(window=4, min_periods=4).apply(lambda x: stats.rankdata(x)[-1]/4.0)).rolling(window=7, min_periods=7) .corr(data['turnoverVol'].rolling(window=10, min_periods=10).apply(lambda x: stats.rankdata(x)[-1]/10.0))).rank(axis=0,pct=True)
    return (part1 ** part2).iloc[-1]
    
def alpha116(data, dependencies=['closePrice'], max_window=20):
    # REGBETA(CLOSE,SEQUENCE,20)
    alpha = REGBETA(data['closePrice'],list(range(1,21)),20)
    return alpha

def alpha117(data, dependencies=['turnoverVol', 'closePrice', 'highestPrice', 'lowestPrice'], max_window=32):
    # TSRANK(VOLUME,32)*(1-TSRANK(CLOSE+HIGH-LOW,16))*(1-TSRANK(RET,32))
    part1 = data['turnoverVol'].iloc[-32:].rank(axis=0, pct=True)
    part2 = 1.0 - (data['closePrice']+data['highestPrice']-data['lowestPrice']).iloc[-16:].rank(axis=0, pct=True)
    part3 = 1.0 - data['closePrice'].pct_change(periods=1).iloc[-32:].rank(axis=0, pct=True)
    return (part1 * part2 * part3).iloc[-1]

def alpha118(data, dependencies=['highestPrice', 'openPrice', 'lowestPrice'], max_window=20):
    # SUM(HIGH-OPEN,20)/SUM(OPEN-LOW,20)*100
    alpha = (data['highestPrice']-data['openPrice']).rolling(window=20,min_periods=20).sum() / (data['openPrice']-data['lowestPrice']).rolling(window=20,min_periods=20).sum() * 100.0
    return alpha.iloc[-1]

def alpha119(data, dependencies=['turnoverValue', 'turnoverVol', 'openPrice'], max_window=62):
    # RANK(DECAYLINEAR(CORR(VWAP,SUM(MEAN(VOLUME,5),26),5),7))-RANK(DECAYLINEAR(TSRANK(MIN(CORR(RANK(OPEN),RANK(MEAN(VOLUME,15)),21),9),7),8))
    # \u611f\u89c9\u6709\u4e2aTSMIN
    w7 = np.array(range(1, 8))
    w8 = np.array(range(1, 9))
    part1 = ((data['turnoverVol'].rolling(window=5,min_periods=5).mean()).rolling(window=26, min_periods=26).sum()).rolling(window=5, min_periods=5).corr(data['turnoverValue']/data['turnoverVol'])
    part1 = (part1.rolling(window=7,min_periods=7).apply(lambda x:np.dot(x,w7))).rank(axis=0,pct=True)
    part2 = ((data['turnoverVol'].rolling(window=15, min_periods=15).mean()).rank(axis=0,pct=True)).rolling(window=21,min_periods=21).corr(data['openPrice'].rank(axis=0,pct=True))
    part2 = (((part2.rolling(window=9, min_periods=9).min()).rolling(window=7,min_periods=7).apply(lambda x: stats.rankdata(x)[-1]/7.0)).rolling(window=8,min_periods=8).apply(lambda x:np.dot(x,w8))).rank(axis=0, pct=True)
    return (part1-part2).iloc[-1]

def alpha120(data, dependencies=['turnoverValue', 'turnoverVol', 'closePrice'], max_window=1):
    # RANK(VWAP-CLOSE)/RANK(VWAP+CLOSE)
    vwap = data['turnoverValue'] / data['turnoverVol']
    return ((vwap-data['closePrice']) / (vwap+data['closePrice'])).iloc[-1]

def alpha121(data, dependencies=['turnoverValue', 'turnoverVol'], max_window=83):
    # (RANK(VWAP-MIN(VWAP,12))^TSRANK(CORR(TSRANK(VWAP,20),TSRANK(MEAN(VOLUME,60),2),18),3))*-1
    vwap = data['turnoverValue'] / data['turnoverVol']
    part1 = (vwap - vwap.rolling(window=12, min_periods=12).min()).rank(axis=0, pct=True)
    part2 = (data['turnoverVol'].rolling(window=60, min_periods=60).mean()).rolling(window=2, min_periods=2).apply(lambda x: stats.rankdata(x)[-1]/2.0)
    part2 = ((vwap.rolling(window=20, min_periods=20).apply(lambda x: stats.rankdata(x)[-1]/20.0)).rolling(window=18, min_periods=18).corr(part2)) .rolling(window=3, min_periods=3).apply(lambda x: stats.rankdata(x)[-1]/3.0)
    return (part1 ** part2).iloc[-1] * (-1)

def alpha122(data, dependencies=['closePrice'], max_window=40):
    # (SMA(SMA(SMA(LOG(CLOSE),13,2),13,2),13,2)-DELAY(SMA(SMA(SMA(LOG(CLOSE),13,2),13,2),13,2),1))/DELAY(SMA(SMA(SMA(LOG(CLOSE),13,2),13,2),13,2),1)
    part1 = (np.log(data['closePrice'])).ewm(adjust=False, alpha=float(2)/13, min_periods=0, ignore_na=False).mean()
    part1 = (part1.ewm(adjust=False, alpha=float(2)/13, min_periods=0, ignore_na=False).mean()).ewm(adjust=False, alpha=float(2)/13, min_periods=0, ignore_na=False).mean()
    return part1.pct_change(periods=1).iloc[-1]

def alpha123(data, dependencies=['highestPrice', 'lowestPrice', 'turnoverVol'], max_window=89):
    # (RANK(CORR(SUM((HIGH+LOW)/2,20),SUM(MEAN(VOLUME,60),20),9)) < RANK(CORR(LOW,VOLUME,6)))*-1
    part1 = (data['highestPrice']*0.5+data['lowestPrice']*0.5).rolling(window=20, min_periods=20).sum()
    part1 = ((data['turnoverVol'].rolling(window=60,min_periods=60).mean()).rolling(window=20,min_periods=20).sum()).rolling(window=9,min_periods=9).corr(part1).rank(axis=0, pct=True)
    part2 = (data['lowestPrice'].rolling(window=6,min_periods=6).corr(data['turnoverVol'])).rank(axis=0, pct=True)
    return (part2 - part1).iloc[-1] * (-1)

def alpha124(data, dependencies=['closePrice', 'turnoverValue', 'turnoverVol'], max_window=32):
    # (CLOSE-VWAP)/DECAYLINEAR(RANK(TSMAX(CLOSE,30)),2)
    vwap = data['turnoverValue'] / data['turnoverVol']
    w2 = np.array(range(1, 3))
    part1 = data['closePrice'] - vwap
    part2 = ((data['closePrice'].rolling(window=30,min_periods=30).max()).rank(axis=0,pct=True)).rolling(window=2,min_periods=2).apply(lambda x:np.dot(x,w2))
    return (part1 / part2).iloc[-1]

def alpha125(data, dependencies=['closePrice', 'turnoverValue', 'turnoverVol'], max_window=117):
    # RANK(DECAYLINEAR(CORR(VWAP,MEAN(VOLUME,80),17),20))/RANK(DECAYLINEAR(DELTA(CLOSE*0.5+VWAP*0.5,3),16))
    vwap = data['turnoverValue'] / data['turnoverVol']
    w20 = np.array(range(1, 21))
    w16 = np.array(range(1, 17))
    part1 = (data['turnoverVol'].rolling(window=80,min_periods=80).mean()).rolling(window=17,min_periods=17).corr(vwap)
    part1 = (part1.rolling(window=20,min_periods=20).apply(lambda x:np.dot(x,w20))).rank(axis=0, pct=True)
    part2 = ((data['closePrice']*0.5+vwap*0.5).diff(periods=3)).rolling(window=16,min_periods=16).apply(lambda x:np.dot(x,w16)).rank(axis=0,pct=True)
    return (part1 / part2).iloc[-1]

def alpha126(data, dependencies=['highestPrice', 'lowestPrice', 'closePrice'], max_window=1):
    # (CLOSE+HIGH+LOW)/3
    return (data['closePrice'] + data['highestPrice'] + data['lowestPrice']).iloc[-1] / 3.0

def alpha127(data, dependencies=['closePrice'], max_window=24):
    # MEAN((100*(CLOSE-MAX(CLOSE,12))/MAX(CLOSE,12))^2)^(1/2)
    # \u8fd9\u91cc\u8c8c\u4f3c\u662fTSMAX,MEAN\u5c11\u4e00\u4e2a\u53c2\u6570
    alpha = (data['closePrice'] - data['closePrice'].rolling(window=12,min_periods=12).max()) / data['closePrice'].rolling(window=12,min_periods=12).max() * 100
    alpha = (alpha ** 2).rolling(window=12, min_periods=12).mean().iloc[-1] ** 0.5
    return alpha

def alpha128(data, dependencies=['highestPrice', 'lowestPrice', 'closePrice', 'turnoverVol'], max_window=14):
    # 100-(100/(1+SUM(((HIGH+LOW+CLOSE)/3>DELAY((HIGH+LOW+CLOSE)/3,1)?(HIGH+LOW+CLOSE)/3*VOLUME:0),14)/
    # SUM(((HIGH+LOW+CLOSE)/3<DELAY((HIGH+LOW+CLOSE)/3,1)?(HIGH+LOW+CLOSE)/3*VOLUME:0),14)))
    condition1 = ((data['highestPrice']+data['lowestPrice']+data['closePrice'])/3.0).diff(1) > 0.0
    condition2 = ((data['highestPrice']+data['lowestPrice']+data['closePrice'])/3.0).diff(1) < 0.0
    part1 = (data['highestPrice']+data['lowestPrice']+data['closePrice'])/3.0*data['turnoverVol']
    part2 = part1.copy(deep=True)
    part1[~condition1] = 0.0
    part1 = part1.rolling(window=14, min_periods=14).sum()
    part2[~condition2] = 0.0
    part2 = part2.rolling(window=14, min_periods=14).sum()
    return (100.0-(100.0/(1+part1/part2))).iloc[-1]

def alpha129(data, dependencies=['closePrice'], max_window=13):
    # SUM((CLOSE-DELAY(CLOSE,1)<0?ABS(CLOSE-DELAY(CLOSE,1)):0),12)
    return (abs(np.minimum(data['closePrice'].diff(1), 0.0))).rolling(window=12, min_periods=12).sum().iloc[-1]

def alpha130(data, dependencies=['lowestPrice', 'highestPrice', 'turnoverVol', 'turnoverValue'], max_window=59):
    # (RANK(DECAYLINEAR(CORR((HIGH+LOW)/2,MEAN(VOLUME,40),9),10))/RANK(DECAYLINEAR(CORR(RANK(VWAP),RANK(VOLUME),7),3)))
    vwap = data['turnoverValue'] / data['turnoverVol']
    w10 = np.array(range(1, 11))
    w3 = np.array(range(1, 4))
    part1 = (data['turnoverVol'].rolling(window=40,min_periods=40).mean()).rolling(window=9,min_periods=9).corr(data['highestPrice']*0.5+data['lowestPrice']*0.5)
    part1 = part1.rolling(window=10,min_periods=10).apply(lambda x: np.dot(x, w10)).rank(axis=0, pct=True)
    part2 = (data['turnoverVol'].rank(axis=0, pct=True)).rolling(window=7,min_periods=7).corr(vwap.rank(axis=0, pct=True))
    part2 = part2.rolling(window=3,min_periods=3).apply(lambda x: np.dot(x, w3)).rank(axis=0, pct=True)
    return (part1 / part2).iloc[-1]

def alpha131(data, dependencies=['turnoverValue', 'turnoverVol', 'closePrice'], max_window=86):
    # (RANK(DELAT(VWAP,1))^TSRANK(CORR(CLOSE,MEAN(VOLUME,50),18),18))
    part1 = (data['turnoverValue'] / data['turnoverVol']).diff(1).rank(axis=0, pct=True).iloc[-1:]
    part2 = (data['turnoverVol'].rolling(window=50, min_periods=50).mean()).rolling(window=18, min_periods=18).corr(data['closePrice'])
    part2 = part2.iloc[-18:].rank(axis=0, pct=True)
    return (part1 ** part2).iloc[-1]

def alpha132(data, dependencies=['turnoverValue'], max_window=20):
    # MEAN(AMOUNT,20)
    return data['turnoverValue'].rolling(window=20, min_periods=20).mean().iloc[-1]

def alpha133(data, dependencies=['lowestPrice', 'highestPrice'], max_window=20):
    # ((20-HIGHDAY(HIGH,20))/20)*100-((20-LOWDAY(LOW,20))/20)*100
    part1 = (20 - data['highestPrice'].rolling(window=20, min_periods=20).apply(lambda x: 19-x.argmax(axis=0))) * 5.0
    part2 = (20 - data['lowestPrice'].rolling(window=20, min_periods=20).apply(lambda x: 19-x.argmin(axis=0))) * 5.0
    return (part1 -part2).iloc[-1]

def alpha134(data, dependencies=['closePrice', 'turnoverVol'], max_window=13):
    # (CLOSE-DELAY(CLOSE,12))/DELAY(CLOSE,12)*VOLUME
    return (data['closePrice'].pct_change(periods=12) * data['turnoverVol']).iloc[-1]

def alpha135(data, dependencies=['closePrice'], max_window=42):
    # SMA(DELAY(CLOSE/DELAY(CLOSE,20),1),20,1)
    alpha = (data['closePrice']/data['closePrice'].shift(20)).shift(1)
    return alpha.ewm(adjust=False, alpha=float(1)/20, min_periods=0, ignore_na=False).mean().iloc[-1]

def alpha136(data, dependencies=['closePrice', 'openPrice', 'turnoverVol'], max_window=10):
    # -1*RANK(DELTA(RET,3))*CORR(OPEN,VOLUME,10)
    part1 = data['closePrice'].pct_change(periods=1).diff(3).rank(axis=0,pct=True)
    part2 = data['openPrice'].rolling(window=10, min_periods=10).corr(data['turnoverVol'])
    return (part1 * part2).iloc[-1] * (-1)

def alpha137(data, dependencies=['openPrice', 'lowestPrice', 'closePrice', 'highestPrice'], max_window=2):
    # 16*(CLOSE+(CLOSE-OPEN)/2-DELAY(OPEN,1))/
    # ((ABS(HIGH-DELAY(CLOSE,1))>ABS(LOW-DELAY(CLOSE,1))&ABS(HIGH-DELAY(CLOSE,1))>ABS(HIGH-DELAY(LOW,1))?ABS(HIGH-DELAY(CLOSE,1))+ABS(LOW-DELAY(CLOSE,1))/2+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4:
    # (ABS(LOW-DELAY(CLOSE,1))>ABS(HIGH-DELAY(LOW,1)) & ABS(LOW-DELAY(CLOSE,1))>ABS(HIGH-DELAY(CLOSE,1))?ABS(LOW-DELAY(CLOSE,1))+ABS(HIGH-DELAY(CLOSE,1))/2+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4:ABS(HIGH-DELAY(LOW,1))+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4)))
    # *MAX(ABS(HIGH-DELAY(CLOSE,1)),ABS(LOW-DELAY(CLOSE,1)))
    part1 = data['closePrice'] * 1.5 - data['openPrice'] * 0.5 - data['openPrice'].shift(1)
    part2 = abs(data['highestPrice']-data['closePrice'].shift(1)) + abs(data['lowestPrice']-data['closePrice'].shift(1)) / 2.0 + abs(data['closePrice']-data['openPrice']).shift(1) / 4.0
    condition1 = np.logical_and(abs(data['highestPrice']-data['closePrice'].shift(1)) > abs(data['lowestPrice']-data['closePrice'].shift(1)), 
                               abs(data['highestPrice']-data['closePrice'].shift(1)) > abs(data['highestPrice']-data['lowestPrice'].shift(1)))
    condition2 = np.logical_and(abs(data['lowestPrice']-data['closePrice'].shift(1)) > abs(data['highestPrice']-data['lowestPrice'].shift(1)), 
                               abs(data['lowestPrice']-data['closePrice'].shift(1)) > abs(data['highestPrice']-data['closePrice'].shift(1)))
    part2[~condition1 & condition2] = abs(data['lowestPrice']-data['closePrice'].shift(1)) + abs(data['highestPrice']-data['closePrice'].shift(1)) / 2.0 + abs(data['closePrice']-data['openPrice']).shift(1) / 4.0
    part2[~condition1 & ~condition2] = abs(data['highestPrice']-data['lowestPrice'].shift(1)) + abs(data['closePrice']-data['openPrice']).shift(1) / 4.0
    part3 = np.maximum(abs(data['highestPrice']-data['closePrice'].shift(1)), abs(data['lowestPrice']-data['closePrice'].shift(1)))
    alpha = (part1 / part2 * part3 * 16.0).iloc[-1]
    return alpha

def alpha138(data, dependencies=['lowestPrice','turnoverValue','turnoverVol'], max_window=126):
    # ((RANK(DECAYLINEAR(DELTA(LOW*0.7+VWAP*0.3,3),20))
    # -TSRANK(DECAYLINEAR(TSRANK(
        # CORR(TSRANK(LOW,8),TSRANK(MEAN(VOLUME,60),17),5)
        # ,19),16),7))* -1)
    w20 = np.array(range(1, 21))
    w16 = np.array(range(1, 17))
    part1 = ((data['lowestPrice']*0.7+data['turnoverValue']/data['turnoverVol']*0.3).diff(3)).rolling(window=20,min_periods=20).apply(lambda x: np.dot(x,w20)).rank(axis=0, pct=True)
    part2 = (data['turnoverVol'].rolling(window=60, min_periods=60).mean()).rolling(window=17,min_periods=17).apply(lambda x: stats.rankdata(x)[-1]/17.0)
    part2 = part2.rolling(window=5,min_periods=5).corr(data['lowestPrice'].rolling(window=8,min_periods=8).apply(lambda x: stats.rankdata(x)[-1]/8.0))
    part2 = ((part2.rolling(window=19,min_periods=19).apply(lambda x: stats.rankdata(x)[-1]/19.0)).rolling(window=16,min_periods=16).apply(lambda x:np.dot(x,w16))).rolling(window=7,min_periods=7).apply(lambda x: stats.rankdata(x)[-1]/7.0)
    return (part1-part2).iloc[-1] * (-1)

def alpha139(data, dependencies=['openPrice', 'turnoverVol'], max_window=10):
    # (-1*CORR(OPEN,VOLUME,10))
    return data['openPrice'].rolling(window=10,min_periods=10).corr(data['turnoverVol']).iloc[-1] * (-1)

def alpha140(data, dependencies=['openPrice', 'lowestPrice', 'highestPrice', 'closePrice', 'turnoverVol'], max_window=99):
    # MIN(RANK(DECAYLINEAR(RANK(OPEN)+RANK(LOW)-RANK(HIGH)-RANK(CLOSE),8)),TSRANK(DECAYLINEAR(CORR(TSRANK(CLOSE,8),TSRANK(MEAN(VOLUME,60),20),8),7),3))
    w8 = np.array(range(1, 9))
    w7 = np.array(range(1, 8))
    part1 = data['openPrice'].rank(axis=0,pct=True)+data['lowestPrice'].rank(axis=0,pct=True)-data['highestPrice'].rank(axis=0,pct=True)-data['closePrice'].rank(axis=0,pct=True)
    part1 = part1.rolling(window=8,min_periods=8).apply(lambda x:np.dot(x,w8)).rank(axis=0,pct=True)
    part2 = (data['turnoverVol'].rolling(window=60, min_periods=60).mean()).rolling(window=20,min_periods=20).apply(lambda x: stats.rankdata(x)[-1]/20.0)
    part2 = part2.rolling(window=8,min_periods=8).corr(data['closePrice'].rolling(window=8,min_periods=8).apply(lambda x: stats.rankdata(x)[-1]/8.0))
    part2 = (part2.rolling(window=7,min_periods=7).apply(lambda x:np.dot(x,w7))).rolling(window=3,min_periods=3).apply(lambda x: stats.rankdata(x)[-1]/3.0)  
    return np.minimum(part1,part2).iloc[-1]

def alpha141(data, dependencies=['highestPrice', 'turnoverVol'], max_window=25):
    # (RANK(CORR(RANK(HIGH),RANK(MEAN(VOLUME,15)),9))*-1)
    alpha = ((data['turnoverVol'].rolling(window=15,min_periods=15).mean().rank(axis=0,pct=True)).rolling(window=9,min_periods=9).corr(data['highestPrice'].rank(axis=0,pct=True))).rank(axis=0,pct=True)
    return alpha.iloc[-1] * (-1)

def alpha142(data, dependencies=['closePrice', 'turnoverVol'], max_window=25):
    # -1*RANK(TSRANK(CLOSE,10))*RANK(DELTA(DELTA(CLOSE,1),1))*RANK(TSRANK(VOLUME/MEAN(VOLUME,20),5))
    part1 = (data['closePrice'].rolling(window=10,min_periods=10).apply(lambda x: stats.rankdata(x)[-1]/10.0)).rank(axis=0,pct=True)
    part2 = (data['closePrice'].diff(1)).diff(1).rank(axis=0,pct=True)
    part3 = (data['turnoverVol']/data['turnoverVol'].rolling(window=20,min_periods=20).mean()).rolling(window=5,min_periods=5).apply(lambda x: stats.rankdata(x)[-1]/5.0).rank(axis=0,pct=True)
    return (part1 * part2 * part3).iloc[-1] * (-1)

def alpha143():
    # CLOSE>DELAY(CLOSE,1)?(CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1)*SELF:SELF
    # \u8868\u793a t-1 \u65e5\u7684 Alpha143 \u56e0\u5b50\u8ba1\u7b97\u7ed3\u679c
    return

def alpha144(data, dependencies=['closePrice','turnoverValue'], max_window=21):
    # SUMIF(ABS(CLOSE/DELAY(CLOSE,1)-1)/AMOUNT,20,CLOSE<DELAY(CLOSE,1))/COUNT(CLOSE<DELAY(CLOSE,1),20)
    part1 = abs(data['closePrice'].pct_change(periods=1)) / data['turnoverValue']
    part1[data['closePrice'].diff(1)>=0] = 0.0
    part1 = part1.rolling(window=20, min_periods=20).sum()
    part2 = (data['closePrice'].diff(1)<0.0).rolling(window=20,min_periods=20).sum()
    return (part1 / part2).iloc[-1]

def alpha145(data, dependencies=['turnoverVol'], max_window=26):
    # (MEAN(VOLUME,9)-MEAN(VOLUME,26))/MEAN(VOLUME,12)*100
    alpha = (data['turnoverVol'].rolling(window=9,min_periods=9).mean() - data['turnoverVol'].rolling(window=26,min_periods=26).mean()) / data['turnoverVol'].rolling(window=12,min_periods=12).mean() * 100.0
    return alpha.iloc[-1]

def alpha146(data, dependencies=['closePrice'], max_window=121):
    # MEAN(RET-SMA(RET,61,2),20)*(RET-SMA(RET,61,2))/SMA(SMA(RET,61,2)^2,60)
    # \u5047\u8bbe\u6700\u540e\u4e00\u4e2aSMA(X,60,1)
    sma = (data['closePrice'].pct_change(1)).ewm(adjust=False, alpha=float(2)/61, min_periods=0, ignore_na=False).mean()
    ret_excess = data['closePrice'].pct_change(1) - sma
    part1 = ret_excess.rolling(window=20, min_periods=20).mean() * ret_excess
    part2 = (sma ** 2).ewm(adjust=False, alpha=float(1)/60, min_periods=0, ignore_na=False).mean()
    return (part1 / part2).iloc[-1]

def alpha147(data, dependencies=['closePrice'], max_window=24):
    # REGBETA(MEAN(CLOSE,12),SEQUENCE(12))
    ma_price = data['closePrice'].rolling(window=12, min_periods=12).mean()
    alpha = REGBETA(ma_price,list(range(1,13)),12)
    return alpha

def alpha148(data, dependencies=['openPrice', 'turnoverVol'], max_window=75):
    # (RANK(CORR(OPEN,SUM(MEAN(VOLUME,60),9),6))<RANK(OPEN-TSMIN(OPEN,14)))*-1
    part1 = (data['turnoverVol'].rolling(window=60,min_periods=60).mean()).rolling(window=9,min_periods=9).sum()
    part1 = part1.rolling(window=6,min_periods=6).corr(data['openPrice']).rank(axis=0,pct=True)
    part2 = (data['openPrice'] - data['openPrice'].rolling(window=14,min_periods=14).min()).rank(axis=0, pct=True)
    return (part2-part1).iloc[-1] * (-1)

def alpha149(data, dependencies=['closePrice'], max_window=253):
    # REGBETA(FILTER(RET,BANCHMARK_INDEX_CLOSE<DELAY(BANCHMARK_INDEX_CLOSE,1)),
    # FILTER(BANCHMARK_INDEX_CLOSE/DELAY(BANCHMARK_INDEX_CLOSE,1)-1,BANCHMARK_INDEX_CLOSE<DELAY(BANCHMARK_INDEX_CLOSE,1)),252)
    bm = (data['closePrice'].mean(axis=0).diff(1) < 0.0)
    part1 = data['closePrice'].pct_change(periods=1).iloc[-252:][bm]
    part2 = data['closePrice'].mean(axis=0).pct_change(periods=1).iloc[-252:][bm]
    alpha = pd.DataFrame([[stats.linregress(part1[col].values, part2.values)[0] for col in data['closePrice'].columns]], 
                 index=data['closePrice'].index[-1:], columns=data['closePrice'].columns)
    return alpha.iloc[-1]

def alpha150(data, dependencies=['closePrice', 'highestPrice', 'lowestPrice', 'turnoverVol'], max_window=1):
    # (CLOSE+HIGH+LOW)/3*VOLUME
    return ((data['closePrice'] + data['highestPrice'] + data['lowestPrice']) / 3.0 * data['turnoverVol']).iloc[-1]

def alpha151(data, dependencies=['closePrice'], max_window=41):
    # SMA(CLOSE-DELAY(CLOSE,20),20,1)
    return (data['closePrice'].diff(20)).ewm(adjust=False, alpha=float(1)/20, min_periods=0, ignore_na=False).mean().iloc[-1]

def alpha152(data, dependencies=['closePrice'], max_window=59):
    # A=DELAY(SMA(DELAY(CLOSE/DELAY(CLOSE,9),1),9,1),1)
    # SMA(MEAN(A,12)-MEAN(A,26),9,1)
    part1 = ((data['closePrice'] / data['closePrice'].shift(9)).shift(1)).ewm(adjust=False, alpha=float(1)/9, min_periods=0, ignore_na=False).mean().shift(1)
    alpha = (part1.rolling(window=12,min_periods=12).mean()-part1.rolling(window=26,min_periods=26).mean()).ewm(adjust=False, alpha=float(1)/9, min_periods=0, ignore_na=False).mean()
    return alpha.iloc[-1]

def alpha153(data, dependencies=['BBI'], max_window=24):
    # (MEAN(CLOSE,3)+MEAN(CLOSE,6)+MEAN(CLOSE,12)+MEAN(CLOSE,24))/4
    # \u5c31\u662fBBI
    part1=[3,6,12,24]
    part2=[data['closePrice'].rolling(window=x,min_periods=x).mean().iloc[-1] for x in part1]
    return sum(part2)/4

def alpha154(data, dependencies=['turnoverValue', 'turnoverVol'], max_window=198):
    # VWAP-MIN(VWAP,16)<CORR(VWAP,MEAN(VOLUME,180),18)
    # \u611f\u89c9\u662fTSMIN
    vwap = data['turnoverValue'] / data['turnoverVol']
    part1 = vwap - vwap.rolling(window=16, min_periods=16).min()
    part2 = (data['turnoverVol'].rolling(window=180, min_periods=180).mean()).rolling(window=18, min_periods=18).corr(vwap)
    return (part2-part1).iloc[-1]

def alpha155(data, dependencies=['turnoverVol'], max_window=37):
    # SMA(VOLUME,13,2)-SMA(VOLUME,27,2)-SMA(SMA(VOLUME,13,2)-SMA(VOLUME,27,2),10,2)
    sma13 = data['turnoverVol'].ewm(adjust=False, alpha=float(2)/13, min_periods=0, ignore_na=False).mean()
    sma27 = data['turnoverVol'].ewm(adjust=False, alpha=float(2)/27, min_periods=0, ignore_na=False).mean()
    ssma = (sma13-sma27).ewm(adjust=False, alpha=float(2)/10, min_periods=0, ignore_na=False).mean()
    return (sma13 - sma27 - ssma).iloc[-1]

def alpha156(data, dependencies=['turnoverValue', 'turnoverVol', 'openPrice', 'lowestPrice'], max_window=9):
    # MAX(RANK(DECAYLINEAR(DELTA(VWAP,5),3)),RANK(DECAYLINEAR((DELTA(OPEN*0.15+LOW*0.85,2)/(OPEN*0.15+LOW*0.85)) * -1,3))) * -1
    w3 = np.array(range(1, 4))
    den = data['openPrice']*0.15+data['lowestPrice']*0.85
    part1 = ((data['turnoverValue']/data['turnoverVol']).diff(5)).rolling(window=3,min_periods=3).apply(lambda x:np.dot(x,w3))
    part2 = (den.diff(2)/den*(-1)).rolling(window=3,min_periods=3).apply(lambda x:np.dot(x,w3))
    return np.maximum(part1, part2).iloc[-1] * (-1)

def alpha157(data, dependencies=['closePrice'], max_window=12):
    # MIN(PROD(RANK(LOG(SUM(TSMIN(RANK(-1*RANK(DELTA(CLOSE-1,5))),2),1))),1),5) +TSRANK(DELAY(-1*RET,6),5)
    part1 = np.log((((data['closePrice']-1.0).diff(5).rank(axis=0,pct=True) * (-1)).rank(axis=0, pct=True)).rolling(window=2, min_periods=2).min())
    part1 = (part1.rank(axis=0, pct=True)).rolling(window=5,min_periods=5).min().iloc[-1:]
    part2 = ((data['closePrice'].pct_change(periods=1) * (-1)).shift(6)).iloc[-5:].rank(axis=0, pct=True)
    return (part1 + part2) .iloc[-1]

def alpha158(data, dependencies=['lowestPrice', 'highestPrice', 'closePrice'], max_window=1):
    # (HIGH-LOW)/CLOSE
    return ((data['highestPrice'] - data['lowestPrice']) / data['closePrice']).iloc[-1]

def alpha159(data, dependencies=['closePrice', 'lowestPrice', 'highestPrice'], max_window=25):
    # ((CLOSE-SUM(MIN(LOW,DELAY(CLOSE,1)),6))/SUM(MAX(HGIH,DELAY(CLOSE,1))-MIN(LOW,DELAY(CLOSE,1)),6)*12*24
    # +(CLOSE-SUM(MIN(LOW,DELAY(CLOSE,1)),12))/SUM(MAX(HGIH,DELAY(CLOSE,1))-MIN(LOW,DELAY(CLOSE,1)),12)*6*24
    # +(CLOSE-SUM(MIN(LOW,DELAY(CLOSE,1)),24))/SUM(MAX(HGIH,DELAY(CLOSE,1))-MIN(LOW,DELAY(CLOSE,1)),24)*6*24)*100/(6*12+6*24+12*24)
    min_low_close = np.minimum(data['lowestPrice'], data['closePrice'].shift(1))
    max_high_close = np.maximum(data['highestPrice'], data['closePrice'].shift(1))
    part1 = (data['closePrice'] - min_low_close.rolling(window=6,min_periods=6).sum()) / (max_high_close-min_low_close).rolling(window=6,min_periods=6).sum() * 12 * 24
    part2 = (data['closePrice'] - min_low_close.rolling(window=12,min_periods=12).sum()) / (max_high_close-min_low_close).rolling(window=12,min_periods=12).sum() * 6 * 24
    part3 = (data['closePrice'] - min_low_close.rolling(window=24,min_periods=24).sum()) / (max_high_close-min_low_close).rolling(window=24,min_periods=24).sum() * 6 * 12
    return (part1+part2+part3).iloc[-1]*100.0/(12*6+6*24+12*24)
    
def alpha160(data, dependencies=['closePrice'], max_window=41):
    # SMA((CLOSE<=DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1)
    part1 = data['closePrice'].rolling(window=20,min_periods=20).std()
    part1[data['closePrice'].diff(1)>0] = 0.0
    return part1.ewm(adjust=False, alpha=float(1)/20, min_periods=0, ignore_na=False).mean().iloc[-1]

def alpha161(data, dependencies=['closePrice', 'lowestPrice', 'highestPrice'], max_window=13):
    # MEAN(MAX(MAX(HIGH-LOW,ABS(DELAY(CLOSE,1)-HIGH)),ABS(DELAY(CLOSE,1)-LOW)),12)
    part1 = np.maximum(data['highestPrice']-data['lowestPrice'], abs(data['closePrice'].shift(1)-data['highestPrice']))
    part1 = np.maximum(part1, abs(data['closePrice'].shift(1)-data['lowestPrice']))
    return part1.rolling(window=12,min_periods=12).mean().iloc[-1]

def alpha162(data, dependencies=['closePrice'], max_window=25):
    # (SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100
    # -MIN(SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100,12))
    # /(MAX(SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100,12)
    # -MIN(SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100,12))
    den = (np.maximum(data['closePrice'].diff(1), 0.0)).ewm(adjust=False, alpha=float(1)/12, min_periods=0, ignore_na=False).mean() /(abs(data['closePrice'].diff(1))).ewm(adjust=False, alpha=float(1)/12, min_periods=0, ignore_na=False).mean() * 100.0
    alpha = (den - den.rolling(window=12,min_periods=12).min()) / (den.rolling(window=12,min_periods=12).max() - den.rolling(window=12,min_periods=12).min())
    return alpha.iloc[-1]

def alpha163(data, dependencies=['turnoverValue', 'turnoverVol', 'closePrice', 'highestPrice'], max_window=20):
    # RANK((-1*RET)*MEAN(VOLUME,20)*VWAP*(HIGH-CLOSE))
    alpha = data['closePrice'].pct_change(periods=1) * (data['turnoverVol'].rolling(window=20, min_periods=20).mean()) * (data['turnoverValue'] / data['turnoverVol']) * (data['highestPrice'] - data['closePrice']) * (-1)
    return alpha.iloc[-1]

def alpha164(data, dependencies=['closePrice', 'highestPrice', 'lowestPrice'], max_window=26):
    # SMA(((CLOSE>DELAY(CLOSE,1)?1/(CLOSE-DELAY(CLOSE,1)):1)-MIN(CLOSE>DELAY(CLOSE,1)?1/(CLOSE-DELAY(CLOSE,1)):1,12))/(HIGH-LOW)*100,13,2)
    part1 = 1.0 / data['closePrice'].diff(1)
    part1[data['closePrice'].diff(1)<=0] = 1.0
    part2 = part1.rolling(window=12, min_periods=12).min()
    alpha = (part1-part2)/(data['highestPrice']-data['lowestPrice'])*100.0
    return alpha.ewm(adjust=False, alpha=float(2)/13, min_periods=0, ignore_na=False).mean().iloc[-1]

def alpha165(data, dependencies=['closePrice'], max_window=144):
    # MAX(SUMAC(CLOSE-MEAN(CLOSE,48)))-MIN(SUMAC(CLOSE-MEAN(CLOSE,48)))/STD(CLOSE,48)
    # SUMAC\u5c11\u4e86\u524dN\u9879\u548c,TSMAX/TSMIN
    part1 = ((data['closePrice']-data['closePrice'].rolling(window=48,min_periods=48).mean()).rolling(window=48,min_periods=48).sum()).rolling(window=48,min_periods=48).max()
    part2 = ((data['closePrice']-data['closePrice'].rolling(window=48,min_periods=48).mean()).rolling(window=48,min_periods=48).sum()).rolling(window=48,min_periods=48).min()
    part3 = data['closePrice'].rolling(window=48,min_periods=48).std()
    return (part1-part2/part3).iloc[-1]

def alpha166(data, dependencies=['closePrice'], max_window=41):
    # -20*(20-1)^1.5*SUM(CLOSE/DELAY(CLOSE,1)-1-MEAN(CLOSE/DELAY(CLOSE,1)-1,20),20)/((20-1)*(20-2)*(SUM((CLOSE/DELAY(CLOSE,1))^2,20))^1.5)
    part1 = data['closePrice'].pct_change(periods=1)-(data['closePrice'].pct_change(periods=1).rolling(window=20,min_periods=20).mean())
    part1 = part1.rolling(window=20,min_periods=20).sum() * ((-20) * 19 ** 1.5)
    part2 = (((data['closePrice']/data['closePrice'].shift(1)) ** 2).rolling(window=20,min_periods=20).sum() ** 1.5) * 19 * 18
    return (part1 / part2).iloc[-1]

def alpha167(data, dependencies=['closePrice'], max_window=13):
    # SUM(CLOSE-DELAY(CLOSE,1)>0?CLOSE-DELAY(CLOSE,1):0,12)
    return (np.maximum(data['closePrice'].diff(1), 0.0)).rolling(window=12, min_periods=12).sum().iloc[-1]

def alpha168(data, dependencies=['turnoverVol'], max_window=20):
    # -1*VOLUME/MEAN(VOLUME,20)
    return (data['turnoverVol']/(data['turnoverVol'].rolling(window=20,min_periods=20).mean())).iloc[-1] * (-1)

def alpha169(data, dependencies=['closePrice'], max_window=48):
    # SMA(MEAN(DELAY(SMA(CLOSE-DELAY(CLOSE,1),9,1),1),12)-MEAN(DELAY(SMA(CLOSE-DELAY(CLOSE,1),9,1),1),26),10,1)
    part1 = (data['closePrice'].diff(1).ewm(adjust=False, alpha=float(1)/9, min_periods=0, ignore_na=False).mean()).shift(1)
    part2 = (part1.rolling(window=12, min_periods=12).mean() - part1.rolling(window=26, min_periods=26).mean()).ewm(adjust=False, alpha=float(1)/10, min_periods=0, ignore_na=False).mean()
    return part2.iloc[-1]

def alpha170(data, dependencies=['closePrice','turnoverVol','highestPrice', 'turnoverValue'], max_window=20):
    # ((RANK(1/CLOSE)*VOLUME)/MEAN(VOLUME,20))*(HIGH*RANK(HIGH-CLOSE)/(SUM(HIGH,5)/5))-RANK(VWAP-DELAY(VWAP,5))
    vwap = data['turnoverValue']/data['turnoverVol']
    part1 = (1.0/data['closePrice']).rank(axis=0,pct=True) * data['turnoverVol'] / (data['turnoverVol'].rolling(window=20,min_periods=20).mean())
    part2 = ((data['highestPrice']-data['closePrice']).rank(axis=0,pct=True) * data['highestPrice']) / (data['highestPrice'].rolling(window=5,min_periods=5).sum()/5.0)
    part3 = (vwap.diff(5)).rank(axis=0,pct=True)
    return (part1*part2-part3).iloc[-1]
    
def alpha171(data, dependencies=['lowestPrice', 'closePrice', 'openPrice', 'highestPrice'], max_window=1):
    # (-1*(LOW-CLOSE)*(OPEN^5))/((CLOSE-HIGH)*(CLOSE^5))
    part1 = (data['lowestPrice']-data['closePrice']) * (data['openPrice'] ** 5) * (-1)
    part2 = (data['closePrice']-data['highestPrice']) * (data['closePrice'] ** 5)
    return (part1 / part2).iloc[-1]

def alpha172(data, dependencies=['ADX'], max_window=20):
    # 就是DMI-ADX
    # HD  HIGH-DELAY(HIGH,1)
    # LD  DELAY(LOW,1)-LOW
    # TR  MAX(MAX(HIGH-LOW,ABS(HIGH-DELAY(CLOSE,1))),ABS(LOW-DELAY(CLOSE,1)))

    # MEAN(ABS(
    #     SUM((LD>0&LD>HD)?LD:0,14)*100/SUM(TR,14)
    #     -SUM((HD>0&HD>LD)?HD:0,14)*100/SUM(TR,14))
    # /(SUM((LD>0&LD>HD)?LD:0,14)*100/SUM(TR,14)
    #     +SUM((HD>0&HD>LD)?HD:0,14)*100/SUM(TR,14))
    # *100,6)
    hd=data['highestPrice'].diff(1)
    ld=-data['lowestPrice'].diff(1)
    tr=np.maximum(np.maximum(data['highestPrice']-data['lowestPrice'],(data['highestPrice']-data['closePrice'].shift(1)).abs()),(data['lowestPrice']-data['closePrice'].shift(1)).abs())
    part1=(((ld>0)&(ld>hd))*ld).rolling(window=14, min_periods=14).sum()*100/tr.rolling(window=14, min_periods=14).sum()-(((hd>0)&(hd>ld))*hd).rolling(window=14, min_periods=14).sum()*100/tr.rolling(window=14, min_periods=14).sum()
    part2=(((ld>0)&(ld>hd))*ld).rolling(window=14, min_periods=14).sum()*100/tr.rolling(window=14, min_periods=14).sum()+(((hd>0)&(hd>ld))*hd).rolling(window=14, min_periods=14).sum()*100/tr.rolling(window=14, min_periods=14).sum()
    return (part1/part2).abs().mean()*100

def alpha173(data, dependencies=['closePrice'], max_window=39):
    # 3*SMA(CLOSE,13,2)-2*SMA(SMA(CLOSE,13,2),13,2)+SMA(SMA(SMA(LOG(CLOSE),13,2),13,2),13,2)
    den = data['closePrice'].ewm(adjust=False, alpha=float(2)/13, min_periods=0, ignore_na=False).mean()
    part1 = 3 * den
    part2 = 2 * (den.ewm(adjust=False, alpha=float(2)/13, min_periods=0, ignore_na=False).mean())
    part3 = ((np.log(data['closePrice']).ewm(adjust=False, alpha=float(2)/13, min_periods=0, ignore_na=False).mean()) .ewm(adjust=False, alpha=float(2)/13, min_periods=0, ignore_na=False).mean()) .ewm(adjust=False, alpha=float(2)/13, min_periods=0, ignore_na=False).mean()
    return (part1 -part2 + part3).iloc[-1]

def alpha174(data, dependencies=['closePrice'], max_window=41):
    # SMA((CLOSE>DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1)
    part1 = data['closePrice'].rolling(window=20,min_periods=20).std()
    part1[data['closePrice'].diff(1)<=0] = 0.0
    return part1.ewm(adjust=False, alpha=float(1)/20, min_periods=0, ignore_na=False).mean().iloc[-1]

def alpha175(data, dependencies=['lowestPrice','highestPrice','closePrice'], max_window=7):
    # MEAN(MAX(MAX(HIGH-LOW,ABS(DELAY(CLOSE,1)-HIGH)),ABS(DELAY(CLOSE,1)-LOW)),6)
    alpha = np.maximum(data['highestPrice']-data['lowestPrice'], abs(data['closePrice'].shift(1)-data['highestPrice']))
    alpha = np.maximum(alpha, abs(data['closePrice'].shift(1)-data['lowestPrice']))
    return alpha.rolling(window=6,min_periods=6).mean().iloc[-1]

def alpha176(data, dependencies=['closePrice','highestPrice','lowestPrice','turnoverVol'], max_window=18):
    # CORR(RANK((CLOSE-TSMIN(LOW,12))/(TSMAX(HIGH,12)-TSMIN(LOW,12))),RANK(VOLUME),6)
    part1 = ((data['closePrice'] - data['lowestPrice'].rolling(window=12,min_periods=12).min()) / (data['highestPrice'].rolling(window=12,min_periods=12).max()-data['lowestPrice'].rolling(window=12,min_periods=12).min())).rank(axis=0, pct=True)
    part2 = data['turnoverVol'].rank(axis=0, pct=True)
    return part1.rolling(window=6,min_periods=6).corr(part2).iloc[-1]

def alpha177(data, dependencies=['highestPrice'], max_window=20):
    # ((20-HIGHDAY(HIGH,20))/20)*100
    return (20 - data['highestPrice'].rolling(window=20, min_periods=20).apply(lambda x: 19-x.argmax(axis=0))).iloc[-1] * 5.0

def alpha178(data, dependencies=['closePrice', 'turnoverVol'], max_window=2):
    # (CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1)*VOLUME
    return (data['closePrice'].pct_change(periods=1) * data['turnoverVol']).iloc[-1]

def alpha179(data, dependencies=['lowestPrice','turnoverValue','turnoverVol'], max_window=62):
    # RANK(CORR(VWAP,VOLUME,4))*RANK(CORR(RANK(LOW),RANK(MEAN(VOLUME,50)),12))
    part1 = ((data['turnoverValue']/data['turnoverVol']).rolling(window=4,min_periods=4).corr(data['turnoverVol'])).rank(axis=0,pct=True)
    part2 = (((data['turnoverVol'].rolling(window=50,min_periods=50).mean()).rank(axis=0,pct=True)).rolling(window=12,min_periods=12).corr(data['lowestPrice'].rank(axis=0,pct=True))).rank(axis=0,pct=True)
    return (part1 * part2).iloc[-1]

def alpha180(data, dependencies=['turnoverVol', 'closePrice'], max_window=68):
    # (MEAN(VOLUME,20)<VOLUME)?((-1*TSRANK(ABS(DELTA(CLOSE,7)),60))*SIGN(DELTA(CLOSE,7)):(-1*VOLUME))
    condition = data['turnoverVol'].rolling(window=20, min_periods=20).mean() < data['turnoverVol']
    alpha = abs(data['closePrice'].diff(7)).rolling(window=60, min_periods=60).apply(lambda x: stats.rankdata(x)[-1]/60.0) * np.sign(data['closePrice'].diff(7)) * (-1)
    alpha[~condition] = -1 * data['turnoverVol'][~condition]
    return alpha.iloc[-1]

def alpha181(data, dependencies=['closePrice'], max_window=40):
    # SUM(RET-MEAN(RET,20)-(BANCHMARK_INDEX_CLOSE-MEAN(BANCHMARK_INDEX_CLOSE,20))^2,20)/SUM((BANCHMARK_INDEX_CLOSE-MEAN(BANCHMARK_INDEX_CLOSE,20))^3)
    bm = data['closePrice'].mean()
    bm_mean = bm - bm.rolling(window=20, min_periods=20).mean()
    bm_mean = pd.DataFrame(data=np.repeat(bm_mean.values.reshape(len(bm_mean.values),1), len(data['closePrice'].columns), axis=1), index=data['closePrice'].index, columns=data['closePrice'].columns)
    ret = data['closePrice'].pct_change(periods=1)
    part1 = (ret-ret.rolling(window=20,min_periods=20).mean()-bm_mean**2).rolling(window=20,min_periods=20).sum()
    part2 = (bm_mean ** 3).rolling(window=20,min_periods=20).sum()
    return (part1 / part2).iloc[-1]

def alpha182(data, dependencies=['closePrice','openPrice'], max_window=20):
    # COUNT((CLOSE>OPEN & BANCHMARK_INDEX_CLOSE>BANCHMARK_INDEX_OPEN) OR (CLOSE<OPEN &BANCHMARK_INDEX_CLOSE<BANCHMARK_INDEX_OPEN),20)/20
    bm = data['closePrice'].mean(axis=1) > data['openPrice'].mean(axis=1)
    bm = pd.DataFrame(data=np.repeat(bm.values.reshape(len(bm.values),1), len(data['closePrice'].columns), axis=1), index=data['closePrice'].index, columns=data['closePrice'].columns)
    condition1 = np.logical_and(data['closePrice']>data['openPrice'], bm)
    condition2 = np.logical_and(data['closePrice']<data['openPrice'], ~bm)
    return np.logical_or(condition1, condition2).rolling(window=20, min_periods=20).mean().iloc[-1]
    
def alpha183(data, dependencies=['closePrice'], max_window=72):
    # MAX(SUMAC(CLOSE-MEAN(CLOSE,24)))-MIN(SUMAC(CLOSE-MEAN(CLOSE,24)))/STD(CLOSE,24)
    part1 = ((data['closePrice']-data['closePrice'].rolling(window=24,min_periods=24).mean()).rolling(window=24,min_periods=24).sum()).rolling(window=24,min_periods=24).max()
    part2 = ((data['closePrice']-data['closePrice'].rolling(window=24,min_periods=24).mean()).rolling(window=24,min_periods=24).sum()).rolling(window=24,min_periods=24).min()
    part3 = data['closePrice'].rolling(window=24,min_periods=24).std()
    return (part1-part2/part3).iloc[-1]

def alpha184(data, dependencies=['closePrice','openPrice'], max_window=201):
    # RANK(CORR(DELAY(OPEN-CLOSE,1),CLOSE,200))+RANK(OPEN-CLOSE)
    part1 = (((data['openPrice']-data['closePrice']).shift(1)).rolling(window=200,min_periods=200).corr(data['closePrice'])).rank(axis=0,pct=True)
    part2 = (data['openPrice']-data['closePrice']).rank(axis=0,pct=True)
    return (part1+part2).iloc[-1]

def alpha185(data, dependencies=['closePrice', 'openPrice'], max_window=1):
    # RANK(-1*(1-OPEN/CLOSE)^2)
    return ((1.0-data['openPrice']/data['closePrice']).iloc[-1] ** 2) * (-1)

def alpha186(data, dependencies=['ADXR'], max_window=1):
    # \u5c31\u662fADXR
#     (MEAN(ABS(SUM((LD>0  &  LD>HD)?LD:0,14)*100/SUM(TR,14)-SUM((HD>0  &
# HD>LD)?HD:0,14)*100/SUM(TR,14))/(SUM((LD>0  &  LD>HD)?LD:0,14)*100/SUM(TR,14)+SUM((HD>0  &
# HD>LD)?HD:0,14)*100/SUM(TR,14))*100,6)+DELAY(MEAN(ABS(SUM((LD>0  &
# LD>HD)?LD:0,14)*100/SUM(TR,14)-SUM((HD>0  &  HD>LD)?HD:0,14)*100/SUM(TR,14))/(SUM((LD>0  &
# LD>HD)?LD:0,14)*100/SUM(TR,14)+SUM((HD>0 & HD>LD)?HD:0,14)*100/SUM(TR,14))*100,6),6))/2
    return data['ADXR'].iloc[-1]

def alpha187(data, dependencies=['openPrice', 'highestPrice'], max_window=21):
    # SUM(OPEN<=DELAY(OPEN,1)?0:MAX(HIGH-OPEN,OPEN-DELAY(OPEN,1)),20)
    part1 = np.maximum(data['highestPrice']-data['openPrice'], data['openPrice'].diff(1))
    part1[data['openPrice'].diff(1)<=0] = 0.0
    return part1.rolling(window=20, min_periods=20).sum().iloc[-1]

def alpha188(data, dependencies=['lowestPrice', 'highestPrice'], max_window=11):
    # ((HIGH-LOW\u2013SMA(HIGH-LOW,11,2))/SMA(HIGH-LOW,11,2))*100
    sma = (data['highestPrice']-data['lowestPrice']).ewm(adjust=False, alpha=float(2)/11, min_periods=0, ignore_na=False).mean()
    return ((data['highestPrice']-data['lowestPrice']-sma)/sma).iloc[-1] * 100

def alpha189(data, dependencies=['closePrice'], max_window=12):
    # MEAN(ABS(CLOSE-MEAN(CLOSE,6)),6)
    return abs(data['closePrice']-data['closePrice'].rolling(window=6,min_periods=6).mean()).rolling(window=6,min_periods=6).mean().iloc[-1]

def alpha190(data, dependencies=['closePrice'], max_window=40):
    # LOG((COUNT(RET>((CLOSE/DELAY(CLOSE,19))^(1/20)-1),20)-1)
    # *SUMIF((RET-(CLOSE/DELAY(CLOSE,19))^(1/20)-1)^2,20,RET<(CLOSE/DELAY(CLOSE,19))^(1/20)-1)
    # /(COUNT(RET<(CLOSE/DELAY(CLOSE,19))^(1/20)-1,20)
    # *SUMIF((RET-((CLOSE/DELAY(CLOSE,19))^(1/20)-1))^2,20,RET>(CLOSE/DELAY(CLOSE,19))^(1/20)-1)))
    ret = data['closePrice'].pct_change(periods=1)
    ret_19 = (data['closePrice']/data['closePrice'].shift(19))**0.05-1.0
    part1 = (ret>ret_19).rolling(window=20, min_periods=20).sum()-1.0
    part2 = (np.minimum(ret-ret_19, 0.0) ** 2).rolling(window=20,min_periods=20).sum()
    part3 = (ret<ret_19).rolling(window=20, min_periods=20).sum()
    part4 = (np.maximum(ret-ret_19, 0.0) ** 2).rolling(window=20,min_periods=20).sum()
    return np.log(part1*part2/part3/part4).iloc[-1]

def alpha191(data, dependencies=['turnoverVol', 'lowestPrice', 'closePrice', 'highestPrice'], max_window=25):
    # CORR(MEAN(VOLUME,20),LOW,5)+(HIGH+LOW)/2-CLOSE
    part1 = (data['turnoverVol'].rolling(window=20,min_periods=20).mean()).rolling(window=5,min_periods=5).corr(data['lowestPrice'])
    return (part1 + data['highestPrice']*0.5+data['lowestPrice']*0.5-data['closePrice']).iloc[-1]
