from xg_tdx_func.xg_tdx_func import *
import empyrical as ep
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import json
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from scipy import stats
import statsmodels.api as sm
import math
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pandas")

class xg_factor:
    '''
    小果因子库计算系统
    '''
    def __init__(self,
                df='',
                index_df='',):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.df = df.copy() if df is not None and not isinstance(df, str) and hasattr(df, 'copy') else df
        self.index_df = index_df.copy() if index_df is not None and not isinstance(index_df, str) and hasattr(index_df, 'copy') else index_df
        
        # 数据重命名（一次性完成）
        if isinstance(self.df, pd.DataFrame) and not self.df.empty:
            rename_dict = {
                "close": "closePrice",
                "open": "openPrice",
                "low": "lowestPrice",
                "high": "highestPrice",
                "volume": "turnoverVol",
                "amount": "turnoverValue"
            }
            # 只重命名存在的列
            self.df.rename(columns={k: v for k, v in rename_dict.items() if k in self.df.columns}, inplace=True)
            
            # 提取核心数据列（使用重命名后的列名）
            self.closePrice = self.df['closePrice'] if 'closePrice' in self.df.columns else pd.Series()
            self.openPrice = self.df['openPrice'] if 'openPrice' in self.df.columns else pd.Series()
            self.lowestPrice = self.df['lowestPrice'] if 'lowestPrice' in self.df.columns else pd.Series()
            self.highestPrice = self.df['highestPrice'] if 'highestPrice' in self.df.columns else pd.Series()
            self.turnoverVol = self.df['turnoverVol'] if 'turnoverVol' in self.df.columns else pd.Series()
            self.turnoverValue = self.df['turnoverValue'] if 'turnoverValue' in self.df.columns else pd.Series()
            
            # 统一简写命名（方便调用）
            self.C = self.closePrice
            self.H = self.highestPrice
            self.L = self.lowestPrice
            self.O = self.openPrice
            self.V = self.turnoverVol
            self.AMOUNT = self.turnoverValue
            
            # 保留原始简写（兼容旧代码）
            self.close = self.closePrice
            self.high = self.highestPrice
            self.low = self.lowestPrice
            self.open = self.openPrice
            self.volume = self.turnoverVol
            self.amount = self.turnoverValue
        else:
            # 空数据时的默认值
            self.closePrice = pd.Series()
            self.openPrice = pd.Series()
            self.lowestPrice = pd.Series()
            self.highestPrice = pd.Series()
            self.turnoverVol = pd.Series()
            self.turnoverValue = pd.Series()
            self.C = pd.Series()
            self.H = pd.Series()
            self.L = pd.Series()
            self.O = pd.Series()
            self.V = pd.Series()
            self.AMOUNT = pd.Series()
            self.close = pd.Series()
            self.high = pd.Series()
            self.low = pd.Series()
            self.open = pd.Series()
            self.volume = pd.Series()
            self.amount = pd.Series()

    # ========== 辅助函数 ==========
    def _sma(self, series, n, m):
        """SMA: 移动平均，alpha = m/n"""
        return series.ewm(adjust=False, alpha=m/n, min_periods=0, ignore_na=False).mean()
    
    def _tsrank(self, series, n):
        """TSRANK: 时间序列排名"""
        def rank_last(x):
            return stats.rankdata(x)[-1] / len(x) if len(x) > 0 else np.nan
        return series.rolling(window=n, min_periods=n).apply(rank_last)
    
    def _tsrank_fixed(self, series, n):
        """改进的TSRANK函数"""
        result = pd.Series(index=series.index, dtype=float)
        for i in range(len(series)):
            start = max(0, i - n + 1)
            window_data = series.iloc[start:i+1]
            valid_data = window_data.dropna()
            if len(valid_data) >= max(2, n // 2):
                current_val = series.iloc[i]
                rank = (valid_data < current_val).sum() + 1
                result.iloc[i] = rank / len(valid_data)
            else:
                result.iloc[i] = np.nan
        return result.fillna(method='ffill').fillna(method='bfill')
    
    def _decaylinear(self, series, n):
        """DECAYLINEAR: 线性衰减加权和"""
        w = np.arange(1, n + 1)
        return series.rolling(window=n, min_periods=n).apply(lambda x: np.dot(x, w))
    
    def _regbeta(self, y, x):
        """REGBETA: 回归beta"""
        y_vals = y.values
        x_vals = x.values if isinstance(x, pd.Series) else np.array(x)
        x_vals = sm.add_constant(x_vals)
        try:
            result = sm.OLS(y_vals, x_vals).fit()
            return result.params[1]
        except:
            return np.nan
    def six_pulse_excalibur_hist(self):
        '''
        六脉神剑
        '''
        
        markers=0
        signal=0
        #df=self.data.get_hist_data_em(stock=stock)
        CLOSE=self.C
        LOW=self.L
        HIGH=self.H
        DIFF=EMA(CLOSE,8)-EMA(CLOSE,13)
        DEA=EMA(DIFF,5)
        #如果满足DIFF>DEA 在1的位置标记1的图标
        #DRAWICON(DIFF>DEA,1,1);
        markers+=IF(DIFF>DEA,1,0)
        #如果满足DIFF<DEA 在1的位置标记2的图标
        #DRAWICON(DIFF<DEA,1,2);
        markers+=IF(DIFF<DEA,1,0)
        #DRAWTEXT(ISLASTBAR=1,1,'. MACD'),COLORFFFFFF;{微信公众号:尊重市场}
        ABC1=DIFF>DEA
        signal+=IF(ABC1,1,0)
        尊重市场1=(CLOSE-LLV(LOW,8))/(HHV(HIGH,8)-LLV(LOW,8))*100
        K=SMA(尊重市场1,3,1)
        D=SMA(K,3,1)
        #如果满足k>d 在2的位置标记1的图标
        markers+=IF(K>D,1,0)
        #DRAWICON(K>D,2,1);
        markers+=IF(K<D,1,0)
        #DRAWICON(K<D,2,2);
        #DRAWTEXT(ISLASTBAR=1,2,'. KDJ'),COLORFFFFFF;
        ABC2=K>D
        signal+=IF(ABC2,1,0)
        指标营地=REF(CLOSE,1)
        RSI1=(SMA(MAX(CLOSE-指标营地,0),5,1))/(SMA(ABS(CLOSE-指标营地),5,1))*100
        RSI2=(SMA(MAX(CLOSE-指标营地,0),13,1))/(SMA(ABS(CLOSE-指标营地),13,1))*100
        markers+=IF(RSI1>RSI2,1,0)
        #DRAWICON(RSI1>RSI2,3,1);
        markers+=IF(RSI1<RSI2,1,0)
        #DRAWICON(RSI1<RSI2,3,2);
        #DRAWTEXT(ISLASTBAR=1,3,'. RSI'),COLORFFFFFF;
        ABC3=RSI1>RSI2
        signal+=IF(ABC3,1,0)
        尊重市场=-(HHV(HIGH,13)-CLOSE)/(HHV(HIGH,13)-LLV(LOW,13))*100
        LWR1=SMA(尊重市场,3,1)
        LWR2=SMA(LWR1,3,1)
        #DRAWICON(LWR1>LWR2,4,1);
        markers+=IF(LWR1>LWR2,1,0)
        #DRAWICON(LWR1<LWR2,4,2);
        markers+=IF(LWR1<LWR2,1,0)
        #DRAWTEXT(ISLASTBAR=1,4,'. LWR'),COLORFFFFFF;
        ABC4=LWR1>LWR2
        signal+=IF(ABC4,1,0)
        BBI=(MA(CLOSE,3)+MA(CLOSE,5)+MA(CLOSE,8)+MA(CLOSE,13))/4
        #DRAWICON(CLOSE>BBI,5,1);
        markers+=IF(CLOSE>BBI,1,0)
        #DRAWICON(CLOSE<BBI,5,2);
        markers+=IF(CLOSE<BBI,1,0)
        #DRAWTEXT(ISLASTBAR=1,5,'. BBI'),COLORFFFFFF;
        ABC10=7
        ABC5=CLOSE>BBI
        signal+=IF(ABC5,1,0)
        MTM=CLOSE-REF(CLOSE,1)
        MMS=100*EMA(EMA(MTM,5),3)/EMA(EMA(ABS(MTM),5),3)
        MMM=100*EMA(EMA(MTM,13),8)/EMA(EMA(ABS(MTM),13),8)
        markers+=IF(MMS>MMM,1,0)
        #DRAWICON(MMS>MMM,6,1);
        markers+=IF(MMS<MMM,1,0)
        #DRAWICON(MMS<MMM,6,2);
        #DRAWTEXT(ISLASTBAR=1,6,'. ZLMM'),COLORFFFFFF;
        ABC6=MMS>MMM
        signal+=IF(ABC6,1,0)
        return signal
    def small_fruit_band_trading_1(self):
        '''
        小波段交易
        '''
        df=self.df
        CLOSE=self.C
        C=self.C
        LOW=self.L
        L=self.L
        HIGH=self.H
        H=self.H
        OPEN=self.O
        O=self.O
        volume=self.V
        V=self.V
        N1=7
        N2=5
        N3=3
        ABC1=(((HIGH + LOW)+(CLOSE*2)) / 4)
        ABC3=EMA(ABC1,N1)
        ABC4=STD(ABC1,N1)
        ABC5=((ABC1 - ABC3)*100) / ABC4
        ABC6=EMA(ABC5,N2)
        RK7=EMA(ABC6,N1)
        UP=(EMA(ABC6,10)+(100 / 2)) - 5
        DOWN=EMA(UP,N3)
        ACB1=EMA(DOWN,N3)
        ACB2=EMA(ACB1,N3)
        ACB3=EMA(ACB2,N3)
        ACB4=EMA(ACB3,N3)
        #STICKLINE(UP < REF(UP,1),UP,MA(UP,3),5,0),COLORBLUE;
        #STICKLINE(UP > REF(UP,1),UP,EMA(UP,3),5,0),COLORMAGENTA;
        df['柱子']=IF(UP > REF(UP,1),'红色','蓝色')
        df['买']=IF(AND(UP > REF(UP,1),REF(UP,1) < REF(UP,2)),'买',None)
        df['卖']=IF(AND(UP < REF(UP,1),REF(UP,1) > REF(UP,2)),'卖',None)
        #DRAWTEXT(UP > REF(UP,1)  AND  REF(UP,1) < REF(UP,2) ,UP,'买'),COLORRED;
        #DRAWTEXT(UP < REF(UP,1)  AND  REF(UP,1) > REF(UP,2) ,UP,'卖'),COLORGREEN;
        stats_list=[]
        for buy,sell in zip(df['买'].tolist(),df['卖'].tolist()):
            if buy=='买':
                stats_list.append(True)
            elif sell=='卖':
                stats_list.append(False)
            else:
                stats_list.append(None)
        df['stats']=stats_list
        df['stats']=df['stats'].fillna(method='ffill')
        return df['stats']
    def small_fruit_band_trading_2(self):
        '''
        大波段交易
        '''
        df=self.df
        CLOSE=self.C
        C=self.C
        LOW=self.L
        L=self.L
        HIGH=self.H
        H=self.H
        OPEN=self.O
        O=self.O
        volume=self.V
        V=self.V
        N1=18
        N2=15
        N3=12
        ABC1=(((HIGH + LOW)+(CLOSE*2)) / 4)
        ABC3=EMA(ABC1,N1)
        ABC4=STD(ABC1,N1)
        ABC5=((ABC1 - ABC3)*100) / ABC4
        ABC6=EMA(ABC5,N2)
        RK7=EMA(ABC6,N1)
        UP=(EMA(ABC6,10)+(100 / 2)) - 5
        DOWN=EMA(UP,N3)
        ACB1=EMA(DOWN,N3)
        ACB2=EMA(ACB1,N3)
        ACB3=EMA(ACB2,N3)
        ACB4=EMA(ACB3,N3)
        #STICKLINE(UP < REF(UP,1),UP,MA(UP,3),5,0),COLORBLUE;
        #STICKLINE(UP > REF(UP,1),UP,EMA(UP,3),5,0),COLORMAGENTA;
        df['柱子']=IF(UP > REF(UP,1),'红色','蓝色')
        df['买']=IF(AND(UP > REF(UP,1),REF(UP,1) < REF(UP,2)),'买',None)
        df['卖']=IF(AND(UP < REF(UP,1),REF(UP,1) > REF(UP,2)),'卖',None)
        #DRAWTEXT(UP > REF(UP,1)  AND  REF(UP,1) < REF(UP,2) ,UP,'买'),COLORRED;
        #DRAWTEXT(UP < REF(UP,1)  AND  REF(UP,1) > REF(UP,2) ,UP,'卖'),COLORGREEN;
        stats_list=[]
        for buy,sell in zip(df['买'].tolist(),df['卖'].tolist()):
            if buy=='买':
                stats_list.append(True)
            elif sell=='卖':
                stats_list.append(False)
            else:
                stats_list.append(None)
        df['stats']=stats_list
        df['stats']=df['stats'].fillna(method='ffill')
        return df['stats']
    def band_supe_buy_sell(self):
        '''
        波段超级买卖
        尊重市场1赋值:收盘价的6.5日[1日权重]移动平均
        尊重市场2赋值:收盘价的13.5日[1日权重]移动平均
        尊重市场11赋值:收盘价的3日[1日权重]移动平均
        尊重市场21赋值:收盘价的8日[1日权重]移动平均
        当满足条件尊重市场1>尊重市场2时,在尊重市场1和尊重市场2位置之间画柱状线,宽度为2.5,0不为0则画空心柱.,画红色,线宽为2
        当满足条件尊重市场2>尊重市场1时,在尊重市场1和尊重市场2位置之间画柱状线,宽度为2.5,0不为0则画空心柱.,画蓝色,线宽为2
        当满足条件尊重市场1上穿尊重市场2时,在最低价*0.98位置画5号图标
        当满足条件尊重市场21上穿尊重市场11时,在最高价*1.02位置书写文字,画黄色
        BBI赋值:(收盘价的3日简单移动平均+收盘价的6日简单移动平均+收盘价的12日简单移动平均+收盘价的24日简单移动平均)/4
        UPR赋值:BBI+3*BBI的13日估算标准差,线宽为2
        DWN赋值:BBI-3*BBI的13日估算标准差
        安全赋值:收盘价的60日简单移动平均,线宽为2
        LC赋值:1日前的收盘价
        RSI赋值:收盘价-LC和0的较大值的6日[1日权重]移动平均/收盘价-LC的绝对值的6日[1日权重]移动平均*100
        A7赋值:(2*收盘价+最高价+最低价)/4
        输出操作线:A7的5日简单移动平均,线宽为1
        操作线1赋值:A7的5日简单移动平均*1.03,线宽为2
        操作线2赋值:A7的5日简单移动平均*0.97,线宽为2
        输出ABC1:21日内A7的最低值
        输出ABC2:21日内A7的最高值
        SK赋值:(A7-ABC1)/(ABC2-ABC1)*100的7日指数移动平均
        SD赋值:0.667*1日前的SK+0.333*SK的5日指数移动平均
        当满足条件如果统计8日中满足收盘价<1日前的收盘价的天数/8>6/10ANDVOL>=1.5*成交量(手)的5日简单移动平均ANDCOUNT(SK>=SD,3)ANDREF(最低价,1)=120日内最低价的最低值,返回1,否则返回0时,在最低价*0.98位置画9号图标
        当满足条件如果统计13日中满足收盘价<1日前的收盘价的天数/13>6/10ANDCOUNT(SK>SD,6)ANDREF(最低价,5)=120日内最低价的最低值ANDREF(收盘价>=开盘价,4)ANDREF(收阳线,3)ANDREF(收阳线,2)ANDREF(开盘价>CLOS,返回?,否则返回?时,在,1)ANDOPEN>1日前的收盘价,1,0)位置书写文字 ,画黄色
        当满足条件如果统计13日中满足收盘价<1日前的收盘价的天数/13>6/10ANDCOUNT(SK>SD,6)ANDREF(最低价,5)=120日内最低价的最低值ANDREF(收盘价>=开盘价,4)ANDREF(收阳线,3)ANDREF(收阳线,2)ANDREF(开盘价>CLOS,返回?,否则返回?时,在,1)ANDOPEN>1日前的收盘价,1,0)位置画最低价*0.98号图标
        '''
        df=self.df
        CLOSE=self.C
        C=self.C
        LOW=self.L
        L=self.L
        HIGH=self.H
        H=self.H
        OPEN=self.O
        O=self.O
        volume=self.V
        V=self.V
        尊重市场1=SMA(C,6.5,1)
        尊重市场2=SMA(C,13.5,1)
        尊重市场11=SMA(C,3,1)
        尊重市场21=SMA(C,8,1)
        '''
        STICKLINE(尊重市场1>尊重市场2 , 尊重市场1,尊重市场2 ,2.5, 0),COLORRED,LINETHICK2;
        STICKLINE(尊重市场2>尊重市场1,尊重市场1,尊重市场2,2.5,0),COLORBLUE,LINETHICK2;
        '''
        df['柱子']=IF(尊重市场1>尊重市场2,'红色','蓝色')
        #DRAWICON( CROSS(尊重市场1,尊重市场2),L*0.98,5);
        df['笑脸']=CROSS(尊重市场1,尊重市场2)
        #DRAWTEXT(CROSS(尊重市场21,尊重市场11),H*1.02,''),COLORYELLOW;
        df['标记文字']=CROSS(尊重市场21,尊重市场11)
        BBI=(MA(CLOSE,3)+MA(CLOSE,6)+MA(CLOSE,12)+MA(CLOSE,24))/4
        UPR=BBI+3*STD(BBI,13)
        DWN=BBI-3*STD(BBI,13)
        安全=MA(CLOSE,60)
        LC=REF(CLOSE,1)
        RSI=SMA(MAX(CLOSE-LC,0),6,1)/SMA(ABS(CLOSE-LC),6,1)*100
        A7=(2*C+H+L)/4
        操作线=MA(A7,5)
        df['操作线']=操作线
        操作线1=MA(A7,5)*1.03
        df['操作线1']=操作线1
        操作线2=MA(A7,5)*0.97
        df['操作线2']=操作线2
        ABC1=LLV(A7,21)
        ABC2=HHV(A7,21)
        SK=EMA((A7-ABC1)/(ABC2-ABC1)*100,7)
        SD=EMA(0.667*REF(SK,1)+0.333*SK,5)
        '''
        DRAWICON(IF(COUNT(CLOSE<REF(CLOSE,1),8)/8>6/10 AND VOL>=1.5*MA(VOL,5) AND
        COUNT(SK>=SD,3) AND REF(LOW,1)=LLV(LOW,120),1,0),L*0.98,9);
        {DRAWTEXT(IF(COUNT(CLOSE<REF(CLOSE,1),8)/8>6/10 AND VOL>=1.5*MA(VOL,5) AND
        COUNT(SK>=SD,3) AND REF(LOW,1)=LLV(LOW,120),1,0),LOW*0.98,'底买') ,COLOR0099FF;}
        DRAWTEXT(IF(COUNT(CLOSE<REF(CLOSE,1),13)/13>6/10 AND
        COUNT(SK>SD,6) AND REF(LOW,5)=LLV(LOW,120) AND REF(CLOSE>=OPEN,4) AND
        REF(CLOSE>OPEN,3) AND REF(CLOSE>OPEN,2) AND REF(OPEN>CLOSE,1) AND
        OPEN>REF(CLOSE,1),1,0),LOW*0.98,'底买') ,COLORYELLOW;
        DRAWICON(IF(COUNT(CLOSE<REF(CLOSE,1),13)/13>6/10 AND
        COUNT(SK>SD,6) AND REF(LOW,5)=LLV(LOW,120) AND REF(CLOSE>=OPEN,4) AND
        REF(CLOSE>OPEN,3) AND REF(CLOSE>OPEN,2) AND REF(OPEN>CLOSE,1) AND
        OPEN>REF(CLOSE,1),1,0),L*0.98,9);
        '''
        趋势=CLOSE>=操作线
        df['趋势']=CLOSE>=操作线
        df['stats']=IF(AND(趋势,尊重市场1>尊重市场2),True,False)
        return df['stats']
    def KDJ_KD金叉(self):
        '''
        KDJ_KD金叉 的 Docstring
        '''
        K,D,J=KDJ(CLOSE=self.C,HIGH=self.H,LOW=self.L)
        result=CROSS(K,D)
        #result=IF(result==True,0,1)
        return result
    def KDJ_KD死叉(self):
        '''
        KDJ_KD金叉 的 Docstring
        '''
        K,D,J=KDJ(CLOSE=self.C,HIGH=self.H,LOW=self.L)
        result=CROSS(D,K)
        #result=IF(result==True,0,1)
        return result
    def RSI_金叉(self):
        '''
        RSI_金叉 的 Docstring
        '''
        RSI1,RSI2,RSI3=RSI(CLOSE=self.C)
        result=CROSS(RSI1,RSI2)
        #result=IF(result==True,0,1)
        return result
    def RSI_死叉(self):
        '''
        RSI_金叉 的 Docstring
        '''
        RSI1,RSI2,RSI3=RSI(CLOSE=self.C)
        result=CROSS(RSI2,RSI1)
        #result=IF(result==True,0,1)
        return result

    def WR_金叉(self):
        '''
        WR_金叉 的 Docstring
        '''
        WR1,WR2=WR(CLOSE=self.C,LOW=self.L,HIGH=self.H)
        result=CROSS(WR1,WR2)
        #result=IF(result==True,0,1)
        return result
    def WR_金叉(self):
        '''
        WR_金叉 的 Docstring
        '''
        WR1,WR2=WR(CLOSE=self.C,LOW=self.L,HIGH=self.H)
        result=CROSS(WR1,WR2)
        #result=IF(result==True,0,1)
        return result
    def MACD_金叉(self):
        '''
        MACD_金叉 的 Docstring
        '''
        DIF,DEA,MACD_1=MACD(CLOSE=self.C)
        result=CROSS(DIF,DEA)
        #result=IF(result==True,0,1)
        return result
    def MACD_死叉(self):
        '''
        MACD_金叉 的 Docstring
        '''
        DIF,DEA,MACD_1=MACD(CLOSE=self.C)
        result=CROSS(DEA,DIF)
        #result=IF(result==True,0,1)
        return result
    def PSY_金叉(self):
        '''
        PSY_金叉 的 Docstring
        '''
        PSY_1,PSYMA=PSY(CLOSE=self.C)
        result=CROSS(PSY_1,PSYMA)
        #result=IF(result==True,0,1)
        return result
    def PSY_死叉(self):
        '''
        PSY_金叉 的 Docstring
        '''
        PSY_1,PSYMA=PSY(CLOSE=self.C)
        result=CROSS(PSYMA,PSY_1)
        #result=IF(result==True,0,1)  
        return result
    def roll_alpha(self,n=5):
        '''
        5日alpha
        '''
        result=ep.roll_alpha(self.C.pct_change(),self.index_df['close'].pct_change(),window=n)
        return result
    def roll_beta(self,n=5):
        '''
        5日beta
        '''
        result=ep.roll_beta(self.C.pct_change(),self.index_df['close'].pct_change(),window=n)
        return result
    def roll_sharpe_ratio(self,n=5):
        '''
        5日夏普
        '''
        result=ep.roll_sharpe_ratio(self.C.pct_change(),window=n)
        return result
    def roll_annual_volatility(self,n=5):
        '''
        5日年华波动率
        '''
        result=ep.roll_annual_volatility(self.C.pct_change(),window=n)
        return result
    def roll_max_drawdown(self,n=5):
        '''
        5日最大回撤
        '''
        result=ep.roll_max_drawdown(self.C.pct_change(),window=n)
        return result
    def roll_up_capture(self,n=5):
        '''
        5日上涨捕获率
        '''
    
        result=ep.roll_up_capture(self.C.pct_change(),self.index_df['close'].pct_change(),window=n)
        return result
    def roll_down_capture(self,n=5):
        '''
        5日下跌捕获率
        '''
        result=ep.roll_down_capture(self.C.pct_change(),self.index_df['close'].pct_change(),window=n)
        return result
    
    
    




    






    # ========== 因子方法 ==========
    def SMA(self, period=5):
        """
        SMA
        """
        return MA(self.C, N=period)
    
    def CROSS_UP(self, n1=5, n2=10):
        """
        金叉判断
        """
        result = CROSS(MA(self.C, n1), MA(self.C, n2))
        return result
    
    def CROSS_DOWN(self, n1=10, n2=5):
        """
        死叉判断
        """
        result = CROSS(MA(self.C, n1), MA(self.C, n2))
        return result
    
    def BARSLASTCOUNT_UP(self):
        """
        连续上涨
        """
        return BARSLASTCOUNT(self.C > self.O)
    
    def BARSLASTCOUNT_DOWN(self):
        """
        连续下跌
        """
        return BARSLASTCOUNT(self.C < self.O)
    
    def PRICE_MA_LINE_ANAL(self, n=5):
        """
        价格在5均线上
        """
        #IF(self.C >= MA(self.C, n), 0, 1)
        return self.C >= MA(self.C, n)
    
    def MA_LINE_ANAL(self, n1=5, n2=10):
        """
        5均线在10均线上
        """
        #IF(MA(self.C, n1) >= MA(self.C, n2), 0, 1)
        return MA(self.C, n1) >= MA(self.C, n2)
    
    def HHVBARS(self, n=5):
        """
        5日最高值到当前周期
        """
        return HHVBARS(self.C, n)
    
    def LLVBARS(self, n=5):
        """
        5日最低值到当前周期
        """
        return LLVBARS(self.C, n)
    
    def cacal_zdf(self, n=5):
        """
        5日涨跌幅
        """
        return (self.C / REF(self.C, n) - 1) * 100
    def cacal_price_line_zdf(self, n=5):
        """
        价格距离5日均线涨跌幅
        """
        result=((self.C-MA(self.C,n))/MA(self.C,n))*100
        return result
    def cacal_line_line_zdf(self, n1=5,n2=10):
        """
        5日均线距离10日均线涨跌幅
        """
        result=((MA(self.C,n1)-MA(self.C,n2))/MA(self.C,n2))*100
        return result
    def cacal_skew(self,n=5):
        '''
        5日偏度
        '''
        result=self.C.rolling(window=n).skew()
        return result
    def cacal_kurt(self,n=5):
        '''
        5日峰度
        '''
        result=self.C.rolling(window=n).kurt()
        return result
    
    def calculate_momentum_score(self, n=3):
        """
        n日回归动量 - 返回时间序列
        """
        df = self.df.copy()
        mom_daily = n
        
        # 创建与df相同索引的Series，初始全部为NaN
        result = pd.Series(index=df.index, dtype=float)
        
        # 从 n-1 开始，因为需要至少 n 个数据点来计算
        for i in range(mom_daily - 1, len(df)):
            # 获取从 i-n+1 到 i 的窗口数据 (共 n 个数据点)
            start_idx = i - mom_daily + 1
            df_sub = df.iloc[start_idx:i+1].copy()
            
            # 检查数据是否足够
            if len(df_sub) < mom_daily:
                continue
            
            # 检查价格数据是否有效
            close_data = df_sub['closePrice'].values
            if np.any(np.isnan(close_data)) or np.any(np.isinf(close_data)) or np.any(close_data <= 0):
                continue
            
            try:
                y = np.log(close_data)
                y_len = len(y)
                weights = np.linspace(1, 2, y_len)
                x = np.arange(y_len)
                slope, intercept = np.polyfit(x, y, 1, w=weights)
                annualized_returns = math.pow(math.exp(slope), 250) - 1
                residuals = y - (slope * x + intercept)
                weighted_residuals = weights * residuals**2
                y_mean = np.mean(y)
                r_squared = 1 - (np.sum(weighted_residuals) / np.sum(weights * (y - y_mean)**2))
                score = annualized_returns * r_squared
                result.iloc[i] = score
            except Exception as e:
                continue
        
        return result
    
    def SLOPE(self, n=5):
        '''
        5日回归斜率
        '''
        result = SLOPE(self.close, N=n)
        return result
    
    def STD(self, n=5):
        '''
        5日标准差
        '''
        result = STD(self.close, N=n)
        return result

    # ===== 超卖超买类 =====

    def CCI(self):
        '''
        CCI商品路径指标
        '''
        TYP = (self.H + self.L + self.C) / 3
        result = (TYP - MA(TYP, 14)) * 1000 / (15 * AVEDEV(TYP, 14))
        return result

    def MFI(self):
        '''
        最近流量指标
        '''
        return MFI(CLOSE=self.C, HIGH=self.H, LOW=self.L, VOL=self.V, N=14)

    def MTM_MTM(self):
        '''动量线 - MTM值'''
        mtm_val, mtmma_val = MTM(CLOSE=self.C, N=12, M=6)
        return mtm_val

    def MTM_MTMMA(self):
        '''动量线 - MTMMA值'''
        mtm_val, mtmma_val = MTM(CLOSE=self.C, N=12, M=6)
        return mtmma_val


    def RSI1(self):
        '''相对强弱指标 - RSI1'''
        rsi1_val, rsi2_val, rsi3_val = RSI(CLOSE=self.C, N1=6, N2=12, N3=24)
        return rsi1_val

    def RSI2(self):
        '''相对强弱指标 - RSI2'''
        rsi1_val, rsi2_val, rsi3_val = RSI(CLOSE=self.C, N1=6, N2=12, N3=24)
        return rsi2_val

    def RSI3(self):
        '''相对强弱指标 - RSI3'''
        rsi1_val, rsi2_val, rsi3_val = RSI(CLOSE=self.C, N1=6, N2=12, N3=24)
        return rsi3_val

    def KDJ_K(self):
        '''KDJ指标 - K值'''
        k_val, d_val, j_val = KDJ(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=9, M1=3, M2=3)
        return k_val

    def KDJ_D(self):
        '''KDJ指标 - D值'''
        k_val, d_val, j_val = KDJ(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=9, M1=3, M2=3)
        return d_val

    def KDJ_J(self):
        '''KDJ指标 - J值'''
        k_val, d_val, j_val = KDJ(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=9, M1=3, M2=3)
        return j_val

    def SKDJ_K(self):
        '''慢速随机指标 - K值'''
        k_val, d_val = SKDJ(CLOSE=self.C, LOW=self.L, HIGH=self.H, N=9, M=3)
        return k_val

    def SKDJ_D(self):
        '''慢速随机指标 - D值'''
        k_val, d_val = SKDJ(CLOSE=self.C, LOW=self.L, HIGH=self.H, N=9, M=3)
        return d_val

    def UDL_UDL(self):
        '''引力线 - UDL值'''
        udl_val, maudl_val = UDL(CLOSE=self.C, N1=3, N2=5, N3=10, N4=20, M=6)
        return udl_val

    def UDL_MAUDL(self):
        '''引力线 - MAUDL值'''
        udl_val, maudl_val = UDL(CLOSE=self.C, N1=3, N2=5, N3=10, N4=20, M=6)
        return maudl_val

    def WR1(self):
        '''威廉指标 - WR1'''
        wr1_val, wr2_val = WR(CLOSE=self.C, LOW=self.L, HIGH=self.H, N=10, N1=6)
        return wr1_val

    def WR2(self):
        '''威廉指标 - WR2'''
        wr1_val, wr2_val = WR(CLOSE=self.C, LOW=self.L, HIGH=self.H, N=10, N1=6)
        return wr2_val

    def LWR1(self):
        '''LWR指标 - LWR1'''
        lwr1_val, lwr2_val = LWR(CLOSE=self.C, LOW=self.L, HIGH=self.H, N=9, M1=3, M2=3)
        return lwr1_val

    def LWR2(self):
        '''LWR指标 - LWR2'''
        lwr1_val, lwr2_val = LWR(CLOSE=self.C, LOW=self.L, HIGH=self.H, N=9, M1=3, M2=3)
        return lwr2_val

    def MARSI1(self):
        '''相对强弱平均线 - RSI1'''
        rsi1_val, rsi2_val = MARSI(CLOSE=self.C, M1=10, M2=6)
        return rsi1_val

    def MARSI2(self):
        '''相对强弱平均线 - RSI2'''
        rsi1_val, rsi2_val = MARSI(CLOSE=self.C, M1=10, M2=6)
        return rsi2_val

    def BIAS1(self):
        '''乖离率 - BIAS1(6日)'''
        bias1_val, bias2_val, bias3_val = BIAS(CLOSE=self.C, N1=6, N2=12, N3=24)
        return bias1_val

    def BIAS2(self):
        '''乖离率 - BIAS2(12日)'''
        bias1_val, bias2_val, bias3_val = BIAS(CLOSE=self.C, N1=6, N2=12, N3=24)
        return bias2_val

    def BIAS3(self):
        '''乖离率 - BIAS3(24日)'''
        bias1_val, bias2_val, bias3_val = BIAS(CLOSE=self.C, N1=6, N2=12, N3=24)
        return bias3_val

    def BIAS_QL_BIAS(self):
        '''乖离率-传统版 - BIAS值'''
        bias_val, biasma_val = BIAS_QL(CLOSE=self.C, N=6, M=6)
        return bias_val

    def BIAS_QL_BIASMA(self):
        '''乖离率-传统版 - BIASMA值'''
        bias_val, biasma_val = BIAS_QL(CLOSE=self.C, N=6, M=6)
        return biasma_val

    def BIAS36_BIAS36(self):
        '''三六乖离 - BIAS36'''
        bias36_val, bias612_val, mabias_val = BIAS36(CLOSE=self.C, M=6)
        return bias36_val

    def BIAS36_BIAS612(self):
        '''三六乖离 - BIAS612'''
        bias36_val, bias612_val, mabias_val = BIAS36(CLOSE=self.C, M=6)
        return bias612_val

    def BIAS36_MABIAS(self):
        '''三六乖离 - MABIAS'''
        bias36_val, bias612_val, mabias_val = BIAS36(CLOSE=self.C, M=6)
        return mabias_val

    def ACCER(self):
        '''幅度涨速'''
        return ACCER(CLOSE=self.C, N=8)

    # ===== 趋势类型 =====

    def ASI_ASI(self):
        '''振动升降指标 - ASI'''
        asi_val, asit_val = ASI(OPEN=self.O, CLOSE=self.C, HIGH=self.H, LOW=self.L, M1=26, M2=10)
        return asi_val

    def ASI_ASIT(self):
        '''振动升降指标 - ASIT'''
        asi_val, asit_val = ASI(OPEN=self.O, CLOSE=self.C, HIGH=self.H, LOW=self.L, M1=26, M2=10)
        return asit_val

    def CHO_CHO(self):
        '''佳庆指标 - CHO'''
        cho_val, macho_val = CHO(CLOSE=self.C, OPEN=self.O, LOW=self.L, HIGH=self.H, VOL=self.V, N1=10, N2=20, M=6)
        return cho_val

    def CHO_MACHO(self):
        '''佳庆指标 - MACHO'''
        cho_val, macho_val = CHO(CLOSE=self.C, OPEN=self.O, LOW=self.L, HIGH=self.H, VOL=self.V, N1=10, N2=20, M=6)
        return macho_val

    def DMA_XT_DIF(self):
        '''平均差 - DIF'''
        dif_val, difma_val = DMA_XT(CLOSE=self.C, N1=10, N2=50, M=10)
        return dif_val

    def DMA_XT_DIFMA(self):
        '''平均差 - DIFMA'''
        dif_val, difma_val = DMA_XT(CLOSE=self.C, N1=10, N2=50, M=10)
        return difma_val

    def DMI_PDI(self):
        '''趋向指标 - PDI'''
        pdi_val, mdi_val, adx_val, adxr_val = DMI(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=14, M=6)
        return pdi_val

    def DMI_MDI(self):
        '''趋向指标 - MDI'''
        pdi_val, mdi_val, adx_val, adxr_val = DMI(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=14, M=6)
        return mdi_val

    def DMI_ADX(self):
        '''趋向指标 - ADX'''
        pdi_val, mdi_val, adx_val, adxr_val = DMI(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=14, M=6)
        return adx_val

    def DMI_ADXR(self):
        '''趋向指标 - ADXR'''
        pdi_val, mdi_val, adx_val, adxr_val = DMI(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=14, M=6)
        return adxr_val

    def DPO_DPO(self):
        '''区间震荡线 - DPO'''
        dpo_val, madpo_val = DPO(CLOSE=self.C, N=21, M=6)
        return dpo_val

    def DPO_MADPO(self):
        '''区间震荡线 - MADPO'''
        dpo_val, madpo_val = DPO(CLOSE=self.C, N=21, M=6)
        return madpo_val

    def EMV_EMV(self):
        '''简易波动指标 - EMV'''
        emv_val, maemv_val = EMV(HIGH=self.H, LOW=self.L, VOL=self.V, N=14, M=9)
        return emv_val

    def EMV_MAEMV(self):
        '''简易波动指标 - MAEMV'''
        emv_val, maemv_val = EMV(HIGH=self.H, LOW=self.L, VOL=self.V, N=14, M=9)
        return maemv_val

    def MACD_DIF(self):
        '''平滑异同平均线 - DIF'''
        dif_val, dea_val, macd_val = MACD(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return dif_val

    def MACD_DEA(self):
        '''平滑异同平均线 - DEA'''
        dif_val, dea_val, macd_val = MACD(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return dea_val

    def MACD_MACD(self):
        '''平滑异同平均线 - MACD'''
        dif_val, dea_val, macd_val = MACD(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return macd_val

    def VMACD_DIF(self):
        '''量平滑异同平均线 - DIF'''
        dif_val, dea_val, macd_val = VMACD(VOL=self.V, SHORT=12, LONG=26, MID=9)
        return dif_val

    def VMACD_DEA(self):
        '''量平滑异同平均线 - DEA'''
        dif_val, dea_val, macd_val = VMACD(VOL=self.V, SHORT=12, LONG=26, MID=9)
        return dea_val

    def VMACD_MACD(self):
        '''量平滑异同平均线 - MACD'''
        dif_val, dea_val, macd_val = VMACD(VOL=self.V, SHORT=12, LONG=26, MID=9)
        return macd_val

    def SMACD_DEA(self):
        '''单线平滑异同平均线 - DEA'''
        dea_val, macd_val = SMACD(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return dea_val

    def SMACD_MACD(self):
        '''单线平滑异同平均线 - MACD'''
        dea_val, macd_val = SMACD(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return macd_val

    def QACD_DIF(self):
        '''快速异同平均线 - DIF'''
        dif_val, macd_val, ddif_val = QACD(CLOSE=self.C, N1=12, N2=12, M=9)
        return dif_val

    def QACD_MACD(self):
        '''快速异同平均线 - MACD'''
        dif_val, macd_val, ddif_val = QACD(CLOSE=self.C, N1=12, N2=12, M=9)
        return macd_val

    def QACD_DDIF(self):
        '''快速异同平均线 - DDIF'''
        dif_val, macd_val, ddif_val = QACD(CLOSE=self.C, N1=12, N2=12, M=9)
        return ddif_val

    def TRIX_TRIX(self):
        '''三重指数平均线 - TRIX'''
        trix_val, matrix_val = TRIX(CLOSE=self.C, N=12, M=9)
        return trix_val

    def TRIX_MATRIX(self):
        '''三重指数平均线 - MATRIX'''
        trix_val, matrix_val = TRIX(CLOSE=self.C, N=12, M=9)
        return matrix_val

    def UOS_UOS(self):
        '''终极指标 - UOS'''
        uos_val, mauos_val = UOS(CLOSE=self.C, HIGH=self.H, LOW=self.L, N1=7, N2=14, N3=28, M=6)
        return uos_val

    def UOS_MAUOS(self):
        '''终极指标 - MAUOS'''
        uos_val, mauos_val = UOS(CLOSE=self.C, HIGH=self.H, LOW=self.L, N1=7, N2=14, N3=28, M=6)
        return mauos_val

    def VTP_VPT(self):
        '''量价曲线 - VPT'''
        vpt_val, mavp_val = VTP(CLOSE=self.C, VOL=self.V, N=51, M=6)
        return vpt_val

    def VTP_MAVP(self):
        '''量价曲线 - MAVP'''
        vpt_val, mavp_val = VTP(CLOSE=self.C, VOL=self.V, N=51, M=6)
        return mavp_val

    def WVAD_WVAD(self):
        '''威廉变异离散量 - WVAD'''
        wvad_val, mawvad_val = WVAD(CLOSE=self.C, OPEN=self.O, HIGH=self.H, LOW=self.L, VOL=self.V, N=24, M=6)
        return wvad_val

    def WVAD_MAWVAD(self):
        '''威廉变异离散量 - MAWVAD'''
        wvad_val, mawvad_val = WVAD(CLOSE=self.C, OPEN=self.O, HIGH=self.H, LOW=self.L, VOL=self.V, N=24, M=6)
        return mawvad_val

    def JS_JS(self):
        '''加数线 - JS'''
        js_val, majs1_val, majs2_val, majs3_val = JS(CLOSE=self.C, N=5, M1=5, M2=10, M3=20)
        return js_val

    def JS_MAJS1(self):
        '''加数线 - MAJS1'''
        js_val, majs1_val, majs2_val, majs3_val = JS(CLOSE=self.C, N=5, M1=5, M2=10, M3=20)
        return majs1_val

    def JS_MAJS2(self):
        '''加数线 - MAJS2'''
        js_val, majs1_val, majs2_val, majs3_val = JS(CLOSE=self.C, N=5, M1=5, M2=10, M3=20)
        return majs2_val

    def JS_MAJS3(self):
        '''加数线 - MAJS3'''
        js_val, majs1_val, majs2_val, majs3_val = JS(CLOSE=self.C, N=5, M1=5, M2=10, M3=20)
        return majs3_val

    def CYE_CYEL(self):
        '''市场趋势 - CYEL'''
        cyel_val, cyes_val = CYE(CLOSE=self.C)
        return cyel_val

    def CYE_CYES(self):
        '''市场趋势 - CYES'''
        cyel_val, cyes_val = CYE(CLOSE=self.C)
        return cyes_val

    def GDX_轨道(self):
        '''轨道线 - 轨道'''
        轨道_val, 压力线_val, 支撑线_val = GDX(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=30, M=9)
        return 轨道_val

    def GDX_压力线(self):
        '''轨道线 - 压力线'''
        轨道_val, 压力线_val, 支撑线_val = GDX(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=30, M=9)
        return 压力线_val

    def GDX_支撑线(self):
        '''轨道线 - 支撑线'''
        轨道_val, 压力线_val, 支撑线_val = GDX(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=30, M=9)
        return 支撑线_val

    def JLHB_B(self):
        '''绝路航标 - B'''
        b_val, var2_val, 绝路航标_val = JLHB(CLOSE=self.C, LOW=self.L,HIGH=self.H, N=7, M=5)
        return b_val

    def JLHB_VAR2(self):
        '''绝路航标 - VAR2'''
        b_val, var2_val, 绝路航标_val = JLHB(CLOSE=self.C, LOW=self.L,HIGH=self.H, N=7, M=5)
        return var2_val

    def JLHB_绝路航标(self):
        '''绝路航标 - 绝路航标'''
        b_val, var2_val, 绝路航标_val = JLHB(CLOSE=self.C, LOW=self.L,HIGH=self.H, N=7, M=5)
        return 绝路航标_val

    # ===== 能量类型 =====

    def BRAR_BR(self):
        '''情绪指标 - BR'''
        br_val, ar_val = BRAR(OPEN=self.O, HIGH=self.H, LOW=self.L,CLOSE=self.C, N=26)
        return br_val

    def BRAR_AR(self):
        '''情绪指标 - AR'''
        br_val, ar_val = BRAR(OPEN=self.O, HIGH=self.H, LOW=self.L,CLOSE=self.C, N=26)
        return ar_val

    def CR_CR(self):
        '''带状能量线 - CR'''
        cr_val, ma1_val, ma2_val, ma3_val, ma4_val = CR(HIGH=self.H, LOW=self.L, N=26, M1=10, M2=20, M3=40, M4=60)
        return cr_val

    def CR_MA1(self):
        '''带状能量线 - MA1'''
        cr_val, ma1_val, ma2_val, ma3_val, ma4_val = CR(HIGH=self.H, LOW=self.L, N=26, M1=10, M2=20, M3=40, M4=60)
        return ma1_val

    def CR_MA2(self):
        '''带状能量线 - MA2'''
        cr_val, ma1_val, ma2_val, ma3_val, ma4_val = CR(HIGH=self.H, LOW=self.L, N=26, M1=10, M2=20, M3=40, M4=60)
        return ma2_val

    def CR_MA3(self):
        '''带状能量线 - MA3'''
        cr_val, ma1_val, ma2_val, ma3_val, ma4_val = CR(HIGH=self.H, LOW=self.L, N=26, M1=10, M2=20, M3=40, M4=60)
        return ma3_val

    def CR_MA4(self):
        '''带状能量线 - MA4'''
        cr_val, ma1_val, ma2_val, ma3_val, ma4_val = CR(HIGH=self.H, LOW=self.L, N=26, M1=10, M2=20, M3=40, M4=60)
        return ma4_val

    def MASS_MASS(self):
        '''梅斯线 - MASS'''
        mass_val, mamass_val = MASS(HIGH=self.H, LOW=self.L, N1=9, N2=25, M=6)
        return mass_val

    def MASS_MAMASS(self):
        '''梅斯线 - MAMASS'''
        mass_val, mamass_val = MASS(HIGH=self.H, LOW=self.L, N1=9, N2=25, M=6)
        return mamass_val

    def PSY_PSY(self):
        '''心理线 - PSY'''
        psy_val, psyma_val = PSY(CLOSE=self.C, N=12, M=6)
        return psy_val

    def PSY_PSYMA(self):
        '''心理线 - PSYMA'''
        psy_val, psyma_val = PSY(CLOSE=self.C, N=12, M=6)
        return psyma_val

    def VR_VR(self):
        '''成交量变异率 - VR'''
        vr_val, mavr_val = VR(CLOSE=self.C,VOL=self.V, N=26, M=6)
        return vr_val

    def VR_MAVR(self):
        '''成交量变异率 - MAVR'''
        vr_val, mavr_val = VR(CLOSE=self.C,VOL=self.V, N=26, M=6)
        return mavr_val

    def WAD_WAD(self):
        '''威廉多空力度线 - WAD'''
        wad_val, mawad_val = WAD(CLOSE=self.C, LOW=self.L,HIGH=self.H, M=30)
        return wad_val

    def WAD_MAWAD(self):
        '''威廉多空力度线 - MAWAD'''
        wad_val, mawad_val = WAD(CLOSE=self.C, LOW=self.L,HIGH=self.H, M=30)
        return mawad_val

    def PCNT_PCNT(self):
        '''幅度比 - PCNT'''
        pcnt_val, mapcnt_val = PCNT(CLOSE=self.C, M=5)
        return pcnt_val

    def PCNT_MAPCNT(self):
        '''幅度比 - MAPCNT'''
        pcnt_val, mapcnt_val = PCNT(CLOSE=self.C, M=5)
        return mapcnt_val

    def CYR_CYR(self):
        '''市场强弱 - CYR'''
        cyr_val, macyr_val = CYR(AMOUNT=self.AMOUNT,VOL=self.V, N=13, M=5)
        return cyr_val

    def CYR_MACYR(self):
        '''市场强弱 - MACYR'''
        cyr_val, macyr_val = CYR(AMOUNT=self.AMOUNT,VOL=self.V, N=13, M=5)
        return macyr_val

    # ===== 能量型 =====

    def AMO_AMOW(self):
        '''成交金额 - AMOW'''
        amow_val, amo1_val, amo2_val = AMO(AMOUNT=self.AMOUNT, M1=5, M2=10)
        return amow_val

    def AMO_AMO1(self):
        '''成交金额 - AMO1'''
        amow_val, amo1_val, amo2_val = AMO(AMOUNT=self.AMOUNT, M1=5, M2=10)
        return amo1_val

    def AMO_AMO2(self):
        '''成交金额 - AMO2'''
        amow_val, amo1_val, amo2_val = AMO(AMOUNT=self.AMOUNT, M1=5, M2=10)
        return amo2_val

    def OBV_OBV(self):
        '''累积能量线 - OBV'''
        obv_val, maobv_val = OBV(VOL=self.V, CLOSE=self.C, M=30)
        return obv_val

    def OBV_MAOBV(self):
        '''累积能量线 - MAOBV'''
        obv_val, maobv_val = OBV(VOL=self.V, CLOSE=self.C, M=30)
        return maobv_val

    def VOL_XT_MAVOL1(self):
        '''成交量 - MAVOL1'''
        mavol1_val, mavol2_val = VOL_XT(VOL=self.V, M1=5, M2=10)
        return mavol1_val

    def VOL_XT_MAVOL2(self):
        '''成交量 - MAVOL2'''
        mavol1_val, mavol2_val = VOL_XT(VOL=self.V, M1=5, M2=10)
        return mavol2_val

    def VRSI1(self):
        '''相对强弱量 - RSI1'''
        rsi1_val, rsi2_val, rsi3_val = VRSI(VOL=self.V, N1=6, N2=12, N3=24)
        return rsi1_val

    def VRSI2(self):
        '''相对强弱量 - RSI2'''
        rsi1_val, rsi2_val, rsi3_val = VRSI(VOL=self.V, N1=6, N2=12, N3=24)
        return rsi2_val

    def VRSI3(self):
        '''相对强弱量 - RSI3'''
        rsi1_val, rsi2_val, rsi3_val = VRSI(VOL=self.V, N1=6, N2=12, N3=24)
        return rsi3_val

    def HSL_HSL(self):
        '''换手线 - HSL'''
        hsl_val, mahsl_val = HSL(HSL=self.V, N=5)
        return hsl_val

    def HSL_MAHSL(self):
        '''换手线 - MAHSL'''
        hsl_val, mahsl_val = HSL(HSL=self.V, N=5)
        return mahsl_val

    # ===== 均线系统 =====

    def MA_XT_MA1(self):
        '''均线 - MA1(5日)'''
        ma1_val, ma2_val, ma3_val, ma4_val = MA_XT(CLOSE=self.C, M1=5, M2=10, M3=20, M4=60)
        return ma1_val

    def MA_XT_MA2(self):
        '''均线 - MA2(10日)'''
        ma1_val, ma2_val, ma3_val, ma4_val = MA_XT(CLOSE=self.C, M1=5, M2=10, M3=20, M4=60)
        return ma2_val

    def MA_XT_MA3(self):
        '''均线 - MA3(20日)'''
        ma1_val, ma2_val, ma3_val, ma4_val = MA_XT(CLOSE=self.C, M1=5, M2=10, M3=20, M4=60)
        return ma3_val

    def MA_XT_MA4(self):
        '''均线 - MA4(60日)'''
        ma1_val, ma2_val, ma3_val, ma4_val = MA_XT(CLOSE=self.C, M1=5, M2=10, M3=20, M4=60)
        return ma4_val

    def ACD_ACD(self):
        '''升降线 - ACD'''
        acd_val, maacd_val = ACD(CLOSE=self.C, HIGH=self.H, LOW=self.L, M=20)
        return acd_val

    def ACD_MAACD(self):
        '''升降线 - MAACD'''
        acd_val, maacd_val = ACD(CLOSE=self.C, HIGH=self.H, LOW=self.L, M=20)
        return maacd_val

    def BBI(self):
        '''多空均线'''
        return BBI(CLOSE=self.C, M1=3, M2=6, M3=12, M4=24)

    def EXPMA_EXP1(self):
        '''指数平均线 - EXP1(12日)'''
        exp1_val, exp2_val = EXPMA(CLOSE=self.C, M1=12, M2=50)
        return exp1_val

    def EXPMA_EXP2(self):
        '''指数平均线 - EXP2(50日)'''
        exp1_val, exp2_val = EXPMA(CLOSE=self.C, M1=12, M2=50)
        return exp2_val

    def HMA_HMA1(self):
        '''高价平均线 - HMA1'''
        hma1_val, hma2_val, hma3_val, hma4_val, hma5_val = HMA(HIGH=self.H, M1=6, M2=12, M3=30, M4=70, M5=90)
        return hma1_val

    def HMA_HMA2(self):
        '''高价平均线 - HMA2'''
        hma1_val, hma2_val, hma3_val, hma4_val, hma5_val = HMA(HIGH=self.H, M1=6, M2=12, M3=30, M4=70, M5=90)
        return hma2_val

    def HMA_HMA3(self):
        '''高价平均线 - HMA3'''
        hma1_val, hma2_val, hma3_val, hma4_val, hma5_val = HMA(HIGH=self.H, M1=6, M2=12, M3=30, M4=70, M5=90)
        return hma3_val

    def HMA_HMA4(self):
        '''高价平均线 - HMA4'''
        hma1_val, hma2_val, hma3_val, hma4_val, hma5_val = HMA(HIGH=self.H, M1=6, M2=12, M3=30, M4=70, M5=90)
        return hma4_val

    def HMA_HMA5(self):
        '''高价平均线 - HMA5'''
        hma1_val, hma2_val, hma3_val, hma4_val, hma5_val = HMA(HIGH=self.H, M1=6, M2=12, M3=30, M4=70, M5=90)
        return hma5_val

    def LMA_LMA1(self):
        '''低价平均线 - LMA1'''
        lma1_val, lma2_val, lma3_val, lma4_val, lma5_val = LMA(LOW=self.L, M1=6, M2=12, M3=30, M4=70, M5=90)
        return lma1_val

    def LMA_LMA2(self):
        '''低价平均线 - LMA2'''
        lma1_val, lma2_val, lma3_val, lma4_val, lma5_val = LMA(LOW=self.L, M1=6, M2=12, M3=30, M4=70, M5=90)
        return lma2_val

    def LMA_LMA3(self):
        '''低价平均线 - LMA3'''
        lma1_val, lma2_val, lma3_val, lma4_val, lma5_val = LMA(LOW=self.L, M1=6, M2=12, M3=30, M4=70, M5=90)
        return lma3_val

    def LMA_LMA4(self):
        '''低价平均线 - LMA4'''
        lma1_val, lma2_val, lma3_val, lma4_val, lma5_val = LMA(LOW=self.L, M1=6, M2=12, M3=30, M4=70, M5=90)
        return lma4_val

    def LMA_LMA5(self):
        '''低价平均线 - LMA5'''
        lma1_val, lma2_val, lma3_val, lma4_val, lma5_val = LMA(LOW=self.L, M1=6, M2=12, M3=30, M4=70, M5=90)
        return lma5_val

    def VMA_VMA1(self):
        '''变异平均线 - VMA1'''
        vma1_val, vma2_val, vma3_val, vma4_val, vma5_val = VMA(HIGH=self.H, OPEN=self.O, LOW=self.L, CLOSE=self.C, M1=6, M2=12, M3=30, M4=70, M5=90)
        return vma1_val

    def VMA_VMA2(self):
        '''变异平均线 - VMA2'''
        vma1_val, vma2_val, vma3_val, vma4_val, vma5_val = VMA(HIGH=self.H, OPEN=self.O, LOW=self.L, CLOSE=self.C, M1=6, M2=12, M3=30, M4=70, M5=90)
        return vma2_val

    def VMA_VMA3(self):
        '''变异平均线 - VMA3'''
        vma1_val, vma2_val, vma3_val, vma4_val, vma5_val = VMA(HIGH=self.H, OPEN=self.O, LOW=self.L, CLOSE=self.C, M1=6, M2=12, M3=30, M4=70, M5=90)
        return vma3_val

    def VMA_VMA4(self):
        '''变异平均线 - VMA4'''
        vma1_val, vma2_val, vma3_val, vma4_val, vma5_val = VMA(HIGH=self.H, OPEN=self.O, LOW=self.L, CLOSE=self.C, M1=6, M2=12, M3=30, M4=70, M5=90)
        return vma4_val

    def VMA_VMA5(self):
        '''变异平均线 - VMA5'''
        vma1_val, vma2_val, vma3_val, vma4_val, vma5_val = VMA(HIGH=self.H, OPEN=self.O, LOW=self.L, CLOSE=self.C, M1=6, M2=12, M3=30, M4=70, M5=90)
        return vma5_val

    def AMV_AMV1(self):
        '''成本均线 - AMV1(5日)'''
        amv1_val, amv2_val, amv3_val, amv4_val = AMV(OPEN=self.O, CLOSE=self.C, VOL=self.V, M1=5, M2=13, M3=34, M4=60)
        return amv1_val

    def AMV_AMV2(self):
        '''成本均线 - AMV2(13日)'''
        amv1_val, amv2_val, amv3_val, amv4_val = AMV(OPEN=self.O, CLOSE=self.C, VOL=self.V, M1=5, M2=13, M3=34, M4=60)
        return amv2_val

    def AMV_AMV3(self):
        '''成本均线 - AMV3(34日)'''
        amv1_val, amv2_val, amv3_val, amv4_val = AMV(OPEN=self.O, CLOSE=self.C, VOL=self.V, M1=5, M2=13, M3=34, M4=60)
        return amv3_val

    def AMV_AMV4(self):
        '''成本均线 - AMV4(60日)'''
        amv1_val, amv2_val, amv3_val, amv4_val = AMV(OPEN=self.O, CLOSE=self.C, VOL=self.V, M1=5, M2=13, M3=34, M4=60)
        return amv4_val

    def BBIBOLL_BBIBOLL(self):
        '''多空布林线 - BBIBOLL'''
        bbiboll_val, upr_val, dwn_val = BBIBOLL(CLOSE=self.C, N=11, M=6)
        return bbiboll_val

    def BBIBOLL_UPR(self):
        '''多空布林线 - UPR'''
        bbiboll_val, upr_val, dwn_val = BBIBOLL(CLOSE=self.C, N=11, M=6)
        return upr_val

    def BBIBOLL_DWN(self):
        '''多空布林线 - DWN'''
        bbiboll_val, upr_val, dwn_val = BBIBOLL(CLOSE=self.C, N=11, M=6)
        return dwn_val

    def ALLIGAT_上唇(self):
        '''鳄鱼线 - 上唇'''
        上唇_val, 牙齿_val, 下颚_val = ALLIGAT(HIGH=self.H, LOW=self.L)
        return 上唇_val

    def ALLIGAT_牙齿(self):
        '''鳄鱼线 - 牙齿'''
        上唇_val, 牙齿_val, 下颚_val = ALLIGAT(HIGH=self.H, LOW=self.L)
        return 牙齿_val

    def ALLIGAT_下颚(self):
        '''鳄鱼线 - 下颚'''
        上唇_val, 牙齿_val, 下颚_val = ALLIGAT(HIGH=self.H, LOW=self.L)
        return 下颚_val

    def GMMA_MA3(self):
        '''顾比均线 - MA3'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma3_val

    def GMMA_MA5(self):
        '''顾比均线 - MA5'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma5_val

    def GMMA_MA8(self):
        '''顾比均线 - MA8'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma8_val

    def GMMA_MA10(self):
        '''顾比均线 - MA10'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma10_val

    def GMMA_MA12(self):
        '''顾比均线 - MA12'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma12_val

    def GMMA_MA15(self):
        '''顾比均线 - MA15'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma15_val

    def GMMA_MA30(self):
        '''顾比均线 - MA30'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma30_val

    def GMMA_MA35(self):
        '''顾比均线 - MA35'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma35_val

    def GMMA_MA40(self):
        '''顾比均线 - MA40'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma40_val

    def GMMA_MA45(self):
        '''顾比均线 - MA45'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma45_val

    def GMMA_MA50(self):
        '''顾比均线 - MA50'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma50_val

    def GMMA_MA60(self):
        '''顾比均线 - MA60'''
        ma3_val, ma5_val, ma8_val, ma10_val, ma12_val, ma15_val, ma30_val, ma35_val, ma40_val, ma45_val, ma50_val, ma60_val = GMMA(CLOSE=self.C)
        return ma60_val

    # ===== 路径类 =====

    def BOLL_BOLL(self):
        '''布林线 - BOLL'''
        boll_val, ub_val, lb_val = BOLL(CLOSE=self.C, M=20)
        return boll_val

    def BOLL_UB(self):
        '''布林线 - UB'''
        boll_val, ub_val, lb_val = BOLL(CLOSE=self.C, M=20)
        return ub_val

    def BOLL_LB(self):
        '''布林线 - LB'''
        boll_val, ub_val, lb_val = BOLL(CLOSE=self.C, M=20)
        return lb_val

    def PBX_PBX1(self):
        '''瀑布线 - PBX1'''
        pbx1_val, pbx2_val, pbx3_val, pbx4_val, pbx5_val, pbx6_val = PBX(CLOSE=self.C, M1=4, M2=6, M3=9, M4=13, M5=18, M6=24)
        return pbx1_val

    def PBX_PBX2(self):
        '''瀑布线 - PBX2'''
        pbx1_val, pbx2_val, pbx3_val, pbx4_val, pbx5_val, pbx6_val = PBX(CLOSE=self.C, M1=4, M2=6, M3=9, M4=13, M5=18, M6=24)
        return pbx2_val

    def PBX_PBX3(self):
        '''瀑布线 - PBX3'''
        pbx1_val, pbx2_val, pbx3_val, pbx4_val, pbx5_val, pbx6_val = PBX(CLOSE=self.C, M1=4, M2=6, M3=9, M4=13, M5=18, M6=24)
        return pbx3_val

    def PBX_PBX4(self):
        '''瀑布线 - PBX4'''
        pbx1_val, pbx2_val, pbx3_val, pbx4_val, pbx5_val, pbx6_val = PBX(CLOSE=self.C, M1=4, M2=6, M3=9, M4=13, M5=18, M6=24)
        return pbx4_val

    def PBX_PBX5(self):
        '''瀑布线 - PBX5'''
        pbx1_val, pbx2_val, pbx3_val, pbx4_val, pbx5_val, pbx6_val = PBX(CLOSE=self.C, M1=4, M2=6, M3=9, M4=13, M5=18, M6=24)
        return pbx5_val

    def PBX_PBX6(self):
        '''瀑布线 - PBX6'''
        pbx1_val, pbx2_val, pbx3_val, pbx4_val, pbx5_val, pbx6_val = PBX(CLOSE=self.C, M1=4, M2=6, M3=9, M4=13, M5=18, M6=24)
        return pbx6_val

    def ENE_UPPER(self):
        '''轨道线 - UPPER'''
        upper_val, lower_val, ene_val = ENE(CLOSE=self.C, N=25, M1=6, M2=6)
        return upper_val

    def ENE_LOWER(self):
        '''轨道线 - LOWER'''
        upper_val, lower_val, ene_val = ENE(CLOSE=self.C, N=25, M1=6, M2=6)
        return lower_val

    def ENE_ENE(self):
        '''轨道线 - ENE'''
        upper_val, lower_val, ene_val = ENE(CLOSE=self.C, N=25, M1=6, M2=6)
        return ene_val

    def MIKE_STOR(self):
        '''麦克支撑压力 - STOR'''
        stor_val, midr_val, wekr_val, weks_val, mids_val, stos_val = MIKE(HIGH=self.H, LOW=self.L, CLOSE=self.C, N=10)
        return stor_val

    def MIKE_MIDR(self):
        '''麦克支撑压力 - MIDR'''
        stor_val, midr_val, wekr_val, weks_val, mids_val, stos_val = MIKE(HIGH=self.H, LOW=self.L, CLOSE=self.C, N=10)
        return midr_val

    def MIKE_WEKR(self):
        '''麦克支撑压力 - WEKR'''
        stor_val, midr_val, wekr_val, weks_val, mids_val, stos_val = MIKE(HIGH=self.H, LOW=self.L, CLOSE=self.C, N=10)
        return wekr_val

    def MIKE_WEKS(self):
        '''麦克支撑压力 - WEKS'''
        stor_val, midr_val, wekr_val, weks_val, mids_val, stos_val = MIKE(HIGH=self.H, LOW=self.L, CLOSE=self.C, N=10)
        return weks_val

    def MIKE_MIDS(self):
        '''麦克支撑压力 - MIDS'''
        stor_val, midr_val, wekr_val, weks_val, mids_val, stos_val = MIKE(HIGH=self.H, LOW=self.L, CLOSE=self.C, N=10)
        return mids_val

    def MIKE_STOS(self):
        '''麦克支撑压力 - STOS'''
        stor_val, midr_val, wekr_val, weks_val, mids_val, stos_val = MIKE(HIGH=self.H, LOW=self.L, CLOSE=self.C, N=10)
        return stos_val

    def XS_SUP(self):
        '''薛斯通道 - SUP'''
        sup_val, sdn_val, lup_val, ldn_val = XS(CLOSE=self.C, VOL=self.V, N=13)
        return sup_val

    def XS_SDN(self):
        '''薛斯通道 - SDN'''
        sup_val, sdn_val, lup_val, ldn_val = XS(CLOSE=self.C, VOL=self.V, N=13)
        return sdn_val

    def XS_LUP(self):
        '''薛斯通道 - LUP'''
        sup_val, sdn_val, lup_val, ldn_val = XS(CLOSE=self.C, VOL=self.V, N=13)
        return lup_val

    def XS_LDN(self):
        '''薛斯通道 - LDN'''
        sup_val, sdn_val, lup_val, ldn_val = XS(CLOSE=self.C, VOL=self.V, N=13)
        return ldn_val

    def TQN_周期高点(self):
        '''唐奇安通道 - 周期高点'''
        周期高点_val, 周期低点_val, 平空开多_val, 平多开空_val = TQN(HIGH=self.H, LOW=self.L, X1=20, X2=20)
        return 周期高点_val

    def TQN_周期低点(self):
        '''唐奇安通道 - 周期低点'''
        周期高点_val, 周期低点_val, 平空开多_val, 平多开空_val = TQN(HIGH=self.H, LOW=self.L, X1=20, X2=20)
        return 周期低点_val

    def TQN_平空开多(self):
        '''唐奇安通道 - 平空开多信号'''
        周期高点_val, 周期低点_val, 平空开多_val, 平多开空_val = TQN(HIGH=self.H, LOW=self.L, X1=20, X2=20)
        return 平空开多_val

    def TQN_平多开空(self):
        '''唐奇安通道 - 平多开空信号'''
        周期高点_val, 周期低点_val, 平空开多_val, 平多开空_val = TQN(HIGH=self.H, LOW=self.L, X1=20, X2=20)
        return 平多开空_val

    # ===== 停损 =====

    def SAR(self):
        '''抛物线指标'''
        return SAR(HIGH=self.H, LOW=self.L, M=10, af=2, amax=20)

    # ===== 交易类型 =====

    def MA_交易_MA1(self):
        '''MA交易 - MA1(短期均线)'''
        ma1_val, ma2_val, 平空开多_val, 平多开空_val = MA_交易(CLOSE=self.C, SHORT=5, LONG=20)
        return ma1_val

    def MA_交易_MA2(self):
        '''MA交易 - MA2(长期均线)'''
        ma1_val, ma2_val, 平空开多_val, 平多开空_val = MA_交易(CLOSE=self.C, SHORT=5, LONG=20)
        return ma2_val

    def MA_交易_平空开多(self):
        '''MA交易 - 平空开多信号'''
        ma1_val, ma2_val, 平空开多_val, 平多开空_val = MA_交易(CLOSE=self.C, SHORT=5, LONG=20)
        return 平空开多_val

    def MA_交易_平多开空(self):
        '''MA交易 - 平多开空信号'''
        ma1_val, ma2_val, 平空开多_val, 平多开空_val = MA_交易(CLOSE=self.C, SHORT=5, LONG=20)
        return 平多开空_val

    def MACD_交易_DIFF(self):
        '''MACD交易 - DIFF'''
        diff_val, dea_val, macd_val, 平空开多_val, 平多开空_val = MACD_交易(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return diff_val

    def MACD_交易_DEA(self):
        '''MACD交易 - DEA'''
        diff_val, dea_val, macd_val, 平空开多_val, 平多开空_val = MACD_交易(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return dea_val

    def MACD_交易_MACD(self):
        '''MACD交易 - MACD'''
        diff_val, dea_val, macd_val, 平空开多_val, 平多开空_val = MACD_交易(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return macd_val

    def MACD_交易_平空开多(self):
        '''MACD交易 - 平空开多信号'''
        diff_val, dea_val, macd_val, 平空开多_val, 平多开空_val = MACD_交易(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return 平空开多_val

    def MACD_交易_平多开空(self):
        '''MACD交易 - 平多开空信号'''
        diff_val, dea_val, macd_val, 平空开多_val, 平多开空_val = MACD_交易(CLOSE=self.C, SHORT=12, LONG=26, MID=9)
        return 平多开空_val

    def KDJ_交易_K(self):
        '''KDJ交易 - K值'''
        k_val, d_val, j_val, 平空开多_val, 平多开空_val = KDJ_交易(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=9, M1=3)
        return k_val

    def KDJ_交易_D(self):
        '''KDJ交易 - D值'''
        k_val, d_val, j_val, 平空开多_val, 平多开空_val = KDJ_交易(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=9, M1=3)
        return d_val

    def KDJ_交易_J(self):
        '''KDJ交易 - J值'''
        k_val, d_val, j_val, 平空开多_val, 平多开空_val = KDJ_交易(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=9, M1=3)
        return j_val

    def KDJ_交易_平空开多(self):
        '''KDJ交易 - 平空开多信号'''
        k_val, d_val, j_val, 平空开多_val, 平多开空_val = KDJ_交易(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=9, M1=3)
        return 平空开多_val

    def KDJ_交易_平多开空(self):
        '''KDJ交易 - 平多开空信号'''
        k_val, d_val, j_val, 平空开多_val, 平多开空_val = KDJ_交易(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=9, M1=3)
        return 平多开空_val

    # ===== 神系 =====

    def SG_XDT_QR(self):
        '''心电图 - QR强弱指标'''
        qr_val, mqr1_val, mqr2_val = SG_XDT(CLOSE=self.C, INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series())
        return qr_val

    def SG_XDT_MQR1(self):
        '''心电图 - MQR1(5日均线)'''
        qr_val, mqr1_val, mqr2_val = SG_XDT(CLOSE=self.C, INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series())
        return mqr1_val

    def SG_XDT_MQR2(self):
        '''心电图 - MQR2(10日均线)'''
        qr_val, mqr1_val, mqr2_val = SG_XDT(CLOSE=self.C, INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series())
        return mqr2_val

    def SG_NDB_DK(self):
        '''脑电波 - DK'''
        dk_val, mdk1_val, mdk2_val = SG_NDB(CLOSE=self.C, HIGH=self.H, LOW=self.L, P1=5, P2=10)
        return dk_val

    def SG_NDB_MDK1(self):
        '''脑电波 - MDK1'''
        dk_val, mdk1_val, mdk2_val = SG_NDB(CLOSE=self.C, HIGH=self.H, LOW=self.L, P1=5, P2=10)
        return mdk1_val

    def SG_NDB_MDK2(self):
        '''脑电波 - MDK2'''
        dk_val, mdk1_val, mdk2_val = SG_NDB(CLOSE=self.C, HIGH=self.H, LOW=self.L, P1=5, P2=10)
        return mdk2_val

    def SG_SMX_ZY1(self):
        '''生命线 - ZY1(3日EMA)'''
        zy1_val, zy2_val, zy3_val = SG_SMX(CLOSE=self.C, HIGH=self.H, LOW=self.L, 
                                INDEXH=self.index_df['high'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                INDEXL=self.index_df['low'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                N=50)
        return zy1_val

    def SG_SMX_ZY2(self):
        '''生命线 - ZY2(17日EMA)'''
        zy1_val, zy2_val, zy3_val = SG_SMX(CLOSE=self.C, HIGH=self.H, LOW=self.L, 
                                INDEXH=self.index_df['high'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                INDEXL=self.index_df['low'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                N=50)
        return zy2_val

    def SG_SMX_ZY3(self):
        '''生命线 - ZY3(34日EMA)'''
        zy1_val, zy2_val, zy3_val = SG_SMX(CLOSE=self.C, HIGH=self.H, LOW=self.L, 
                                INDEXH=self.index_df['high'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                INDEXL=self.index_df['low'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                                N=50)
        return zy3_val

    def SG_LB_量比(self):
        '''量比'''
        量比_val, ma5_val, ma10_val = SG_LB(VOL=self.V, INDEXV=self.index_df['volume'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series())
        return 量比_val

    def SG_LB_MA5(self):
        '''量比 - MA5'''
        量比_val, ma5_val, ma10_val = SG_LB(VOL=self.V, INDEXV=self.index_df['volume'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series())
        return ma5_val

    def SG_LB_MA10(self):
        '''量比 - MA10'''
        量比_val, ma5_val, ma10_val = SG_LB(VOL=self.V, INDEXV=self.index_df['volume'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series())
        return ma10_val

    def SG_PF(self):
        '''强势股评分'''
        return SG_PF(CLOSE=self.C, INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series())

    # ===== 龙系 =====

    def RAD_RADER1(self):
        '''威力雷达 - RADER1'''
        rader1_val, rader_ma_val = RAD(OPEN=self.O, HIGH=self.H, CLOSE=self.C, LOW=self.L,
                            INDEXO=self.index_df['open'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                            INDEXH=self.index_df['high'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                            INDEXL=self.index_df['low'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                            INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                            D=3, S=30, M=30)
        return rader1_val

    def RAD_RADERMA(self):
        '''威力雷达 - RADERMA'''
        rader1_val, rader_ma_val = RAD(OPEN=self.O, HIGH=self.H, CLOSE=self.C, LOW=self.L,
                            INDEXO=self.index_df['open'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                            INDEXH=self.index_df['high'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                            INDEXL=self.index_df['low'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                            INDEXC=self.index_df['close'] if hasattr(self, 'index_df') and not self.index_df.empty else pd.Series(),
                            D=3, S=30, M=30)
        return rader_ma_val

    def LON_LON(self):
        '''龙系长线 - LON'''
        lon_val, lonma_val, lont_val = LON(CLOSE=self.C, HIGH=self.H, LOW=self.L, VOL=self.V, N=10)
        return lon_val

    def LON_LONMA(self):
        '''龙系长线 - LONMA'''
        lon_val, lonma_val, lont_val = LON(CLOSE=self.C, HIGH=self.H, LOW=self.L, VOL=self.V, N=10)
        return lonma_val

    def LON_LONT(self):
        '''龙系长线 - LONT'''
        lon_val, lonma_val, lont_val = LON(CLOSE=self.C, HIGH=self.H, LOW=self.L, VOL=self.V, N=10)
        return lont_val

    def SHT_SHT(self):
        '''龙系短线 - SHT'''
        sht_val, shtma_val = SHT(CLOSE=self.C, VOL=self.V, N=5)
        return sht_val

    def SHT_SHTMA(self):
        '''龙系短线 - SHTMA'''
        sht_val, shtma_val = SHT(CLOSE=self.C, VOL=self.V, N=5)
        return shtma_val

    def ZLJC_JCS(self):
        '''主力进出 - JCS'''
        jcs_val, jcm_val, jcl_val = ZLJC(CLOSE=self.C, LOW=self.L, HIGH=self.H,VOL=self.V)
        return jcs_val

    def ZLJC_JCM(self):
        '''主力进出 - JCM'''
        jcs_val, jcm_val, jcl_val = ZLJC(CLOSE=self.C, LOW=self.L, HIGH=self.H,VOL=self.V)
        return jcm_val

    def ZLJC_JCL(self):
        '''主力进出 - JCL'''
        jcs_val, jcm_val, jcl_val = ZLJC(CLOSE=self.C, LOW=self.L, HIGH=self.H,VOL=self.V)
        return jcl_val

    def ZLMM_MMS(self):
        '''主力买卖 - MMS'''
        mms_val, mmm_val, mml_val = ZLMM(CLOSE=self.C)
        return mms_val

    def ZLMM_MMM(self):
        '''主力买卖 - MMM'''
        mms_val, mmm_val, mml_val = ZLMM(CLOSE=self.C)
        return mmm_val

    def ZLMM_MML(self):
        '''主力买卖 - MML'''
        mms_val, mmm_val, mml_val = ZLMM(CLOSE=self.C)
        return mml_val

    def SLZT_白龙(self):
        '''神龙在天 - 白龙'''
        白龙_val, 黄龙_val, 紫龙_val, 青龙_val, 红龙_val, 蓝龙_val = SLZT(CLOSE=self.C, LOW=self.L,HIGH=self.H)
        return 白龙_val

    def SLZT_黄龙(self):
        '''神龙在天 - 黄龙'''
        白龙_val, 黄龙_val, 紫龙_val, 青龙_val, 红龙_val, 蓝龙_val = SLZT(CLOSE=self.C, LOW=self.L,HIGH=self.H)
        return 黄龙_val

    def SLZT_紫龙(self):
        '''神龙在天 - 紫龙'''
        白龙_val, 黄龙_val, 紫龙_val, 青龙_val, 红龙_val, 蓝龙_val = SLZT(CLOSE=self.C, LOW=self.L,HIGH=self.H)
        return 紫龙_val

    def SLZT_青龙(self):
        '''神龙在天 - 青龙'''
        白龙_val, 黄龙_val, 紫龙_val, 青龙_val, 红龙_val, 蓝龙_val = SLZT(CLOSE=self.C, LOW=self.L,HIGH=self.H)
        return 青龙_val

    def SLZT_红龙(self):
        '''神龙在天 - 红龙'''
        白龙_val, 黄龙_val, 紫龙_val, 青龙_val, 红龙_val, 蓝龙_val = SLZT(CLOSE=self.C, LOW=self.L,HIGH=self.H)
        return 红龙_val

    def SLZT_蓝龙(self):
        '''神龙在天 - 蓝龙'''
        白龙_val, 黄龙_val, 紫龙_val, 青龙_val, 红龙_val, 蓝龙_val = SLZT(CLOSE=self.C, LOW=self.L,HIGH=self.H)
        return 蓝龙_val

    def ADVOL_ADVOL(self):
        '''龙系离散量 - ADVOL'''
        advol_val, ma1_val, ma2_val = ADVOL(CLOSE=self.C, HIGH=self.H, LOW=self.L, VOL=self.V)
        return advol_val

    def ADVOL_MA1(self):
        '''龙系离散量 - MA1'''
        advol_val, ma1_val, ma2_val = ADVOL(CLOSE=self.C, HIGH=self.H, LOW=self.L, VOL=self.V)
        return ma1_val

    def ADVOL_MA2(self):
        '''龙系离散量 - MA2'''
        advol_val, ma1_val, ma2_val = ADVOL(CLOSE=self.C, HIGH=self.H, LOW=self.L, VOL=self.V)
        return ma2_val

    # ===== 鬼系 =====

    def CYS(self):
        '''市场盈亏'''
        return CYS(CLOSE=self.C, AMOUNT=self.AMOUNT, VOL=self.V)

    

    def CYW(self):
        '''主力控盘'''
        return CYW(CLOSE=self.C, HIGH=self.H, LOW=self.L, VOL=self.V)

    # ===== 其他系 =====

    def JAX_J(self):
        '''济安线 - J'''
        j_val, a_val, x_val = JAX(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=30)
        return j_val

    def JAX_A(self):
        '''济安线 - A'''
        j_val, a_val, x_val = JAX(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=30)
        return a_val

    def JAX_X(self):
        '''济安线 - X'''
        j_val, a_val, x_val = JAX(CLOSE=self.C, HIGH=self.H, LOW=self.L, N=30)
        return x_val

    def XJDX_J(self):
        '''超级短线 - J'''
        j_val, d_val, k_val = XJDX(CLOSE=self.C, HIGH=self.H, LOW=self.L)
        return j_val

    def XJDX_D(self):
        '''超级短线 - D'''
        j_val, d_val, k_val = XJDX(CLOSE=self.C, HIGH=self.H, LOW=self.L)
        return d_val

    def XJDX_K(self):
        '''超级短线 - K'''
        j_val, d_val, k_val = XJDX(CLOSE=self.C, HIGH=self.H, LOW=self.L)
        return k_val

    def ZJTJ_无庄控盘(self):
        '''庄家抬轿 - 无庄控盘'''
        无庄控盘_val, 开始控盘_val, 有庄控盘_val, 主力出货_val = ZJTJ(CLOSE=self.C)
        return 无庄控盘_val

    def ZJTJ_开始控盘(self):
        '''庄家抬轿 - 开始控盘'''
        无庄控盘_val, 开始控盘_val, 有庄控盘_val, 主力出货_val = ZJTJ(CLOSE=self.C)
        return 开始控盘_val

    def ZJTJ_有庄控盘(self):
        '''庄家抬轿 - 有庄控盘'''
        无庄控盘_val, 开始控盘_val, 有庄控盘_val, 主力出货_val = ZJTJ(CLOSE=self.C)
        return 有庄控盘_val

    def ZJTJ_主力出货(self):
        '''庄家抬轿 - 主力出货'''
        无庄控盘_val, 开始控盘_val, 有庄控盘_val, 主力出货_val = ZJTJ(CLOSE=self.C)
        return 主力出货_val

    
    def BDZX_AK(self):
        '''波段之星 - AK'''
        ak_val, ad1_val, aj_val, aa_val, bb_val, cc_val, 买进_val, 卖出_val = BDZX(HIGH=self.H, LOW=self.L, CLOSE=self.C)
        return ak_val

    def BDZX_AD1(self):
        '''波段之星 - AD1'''
        ak_val, ad1_val, aj_val, aa_val, bb_val, cc_val, 买进_val, 卖出_val = BDZX(HIGH=self.H, LOW=self.L, CLOSE=self.C)
        return ad1_val

    def BDZX_AJ(self):
        '''波段之星 - AJ'''
        ak_val, ad1_val, aj_val, aa_val, bb_val, cc_val, 买进_val, 卖出_val = BDZX(HIGH=self.H, LOW=self.L, CLOSE=self.C)
        return aj_val

    def BDZX_买进(self):
        '''波段之星 - 买进信号'''
        ak_val, ad1_val, aj_val, aa_val, bb_val, cc_val, 买进_val, 卖出_val = BDZX(HIGH=self.H, LOW=self.L, CLOSE=self.C)
        return 买进_val

    def BDZX_卖出(self):
        '''波段之星 - 卖出信号'''
        ak_val, ad1_val, aj_val, aa_val, bb_val, cc_val, 买进_val, 卖出_val = BDZX(HIGH=self.H, LOW=self.L, CLOSE=self.C)
        return 卖出_val

    def LHXJ_主力弃盘(self):
        '''猎狐先觉 - 主力弃盘'''
        主力弃盘_val, 主力控盘_val = LHXJ(HIGH=self.H, LOW=self.L, CLOSE=self.C)
        return 主力弃盘_val

    def LHXJ_主力控盘(self):
        '''猎狐先觉 - 主力控盘'''
        主力弃盘_val, 主力控盘_val = LHXJ(HIGH=self.H, LOW=self.L, CLOSE=self.C)
        return 主力控盘_val

    def LYJH_机构做空能量线(self):
        '''猎鹰歼狐 - 机构做空能量线'''
        机构做空能量线_val, 机构做多能量线_val, lh_val, lh1_val = LYJH(CLOSE=self.C, HIGH=self.H, LOW=self.L, M=80, M1=50)
        return 机构做空能量线_val

    def LYJH_机构做多能量线(self):
        '''猎鹰歼狐 - 机构做多能量线'''
        机构做空能量线_val, 机构做多能量线_val, lh_val, lh1_val = LYJH(CLOSE=self.C, HIGH=self.H, LOW=self.L, M=80, M1=50)
        return 机构做多能量线_val

    def JFZX_多头力量(self):
        '''飓风智能中线 - 多头力量'''
        多头力量_val, 空头力量_val, 多空平衡_val = JFZX(OPEN=self.O, CLOSE=self.C, VOL=self.V, N=30)
        return 多头力量_val

    def JFZX_空头力量(self):
        '''飓风智能中线 - 空头力量'''
        多头力量_val, 空头力量_val, 多空平衡_val = JFZX(OPEN=self.O, CLOSE=self.C, VOL=self.V, N=30)
        return 空头力量_val

    def CYHT_SK(self):
        '''财运亨通 - SK'''
        高抛_val, sk_val, sd_val, 低吸_val, 强弱分界_val, 卖出_val, 买进_val = CYHT(CLOSE=self.C, HIGH=self.H, LOW=self.L, OPEN=self.O)
        return sk_val

    def CYHT_SD(self):
        '''财运亨通 - SD'''
        高抛_val, sk_val, sd_val, 低吸_val, 强弱分界_val, 卖出_val, 买进_val = CYHT(CLOSE=self.C, HIGH=self.H, LOW=self.L, OPEN=self.O)
        return sd_val

    def CYHT_卖出(self):
        '''财运亨通 - 卖出信号'''
        高抛_val, sk_val, sd_val, 低吸_val, 强弱分界_val, 卖出_val, 买进_val = CYHT(CLOSE=self.C, HIGH=self.H, LOW=self.L, OPEN=self.O)
        return 卖出_val

    def CYHT_买进(self):
        '''财运亨通 - 买进信号'''
        高抛_val, sk_val, sd_val, 低吸_val, 强弱分界_val, 卖出_val, 买进_val = CYHT(CLOSE=self.C, HIGH=self.H, LOW=self.L, OPEN=self.O)
        return 买进_val

    def BSQJ_B买(self):
        '''买卖区间 - B买信号'''
        b买_val, 持仓_val, s卖_val, 空仓_val = BSQJ(CLOSE=self.C)
        return b买_val

    def BSQJ_持仓(self):
        '''买卖区间 - 持仓信号'''
        b买_val, 持仓_val, s卖_val, 空仓_val = BSQJ(CLOSE=self.C)
        return 持仓_val

    def BSQJ_S卖(self):
        '''买卖区间 - S卖信号'''
        b买_val, 持仓_val, s卖_val, 空仓_val = BSQJ(CLOSE=self.C)
        return s卖_val

    def BSQJ_空仓(self):
        '''买卖区间 - 空仓信号'''
        b买_val, 持仓_val, s卖_val, 空仓_val = BSQJ(CLOSE=self.C)
        return 空仓_val

    def CDP_STD_CDP(self):
        '''逆势操作 - CDP'''
        cdp_val, ah_val, nh_val, nl_val, al_val = CDP_STD(CLOSE=self.C, HIGH=self.H, LOW=self.L)
        return cdp_val

    def CDP_STD_AH(self):
        '''逆势操作 - AH'''
        cdp_val, ah_val, nh_val, nl_val, al_val = CDP_STD(CLOSE=self.C, HIGH=self.H, LOW=self.L)
        return ah_val

    def CDP_STD_NH(self):
        '''逆势操作 - NH'''
        cdp_val, ah_val, nh_val, nl_val, al_val = CDP_STD(CLOSE=self.C, HIGH=self.H, LOW=self.L)
        return nh_val

    def CDP_STD_NL(self):
        '''逆势操作 - NL'''
        cdp_val, ah_val, nh_val, nl_val, al_val = CDP_STD(CLOSE=self.C, HIGH=self.H, LOW=self.L)
        return nl_val

    def CDP_STD_AL(self):
        '''逆势操作 - AL'''
        cdp_val, ah_val, nh_val, nl_val, al_val = CDP_STD(CLOSE=self.C, HIGH=self.H, LOW=self.L)
        return al_val








































    # ===== Alpha因子 =====

    def alpha001(self, max_window=6):
        """
        (-1 * CORR(RANK(DELTA(LOG(VOLUME),1)), RANK((CLOSE-OPEN)/OPEN), 6))
        """
        rank_sizenl = np.log(self.V).diff(1).rank(axis=0, pct=True)
        rank_ret = ((self.C - self.O) / self.O).rank(axis=0, pct=True)
        return -1 * rank_sizenl.rolling(window=max_window, min_periods=max_window).corr(rank_ret)
    
    def alpha002(self, max_window=2):
        """
        -1*delta(((close-low)-(high-close))/(high-low),1)
        """
        win_ratio = (max_window * self.C - self.L - self.H) / (self.H - self.L)
        return -1 * win_ratio.diff(1)
    
    def alpha003(self):
        """
        -1*SUM((CLOSE=DELAY(CLOSE,1)?0:CLOSE-(CLOSE>DELAY(CLOSE,1)?MIN(LOW,DELAY(CLOSE,1)):MAX(HIGH,DELAY(CLOSE,1)))),6)
        """
        alpha = self.C.copy()
        condition2 = self.C.diff(periods=1) > 0.0
        condition3 = self.C.diff(periods=1) < 0.0
        alpha[condition2] = self.C[condition2] - np.minimum(self.C[condition2].shift(1).replace(np.NaN, 10000), self.L[condition2])
        alpha[condition3] = self.C[condition3] - np.maximum(self.C[condition3].shift(1).replace(np.NaN, 0), self.H[condition3])
        return -1 * alpha.sum(axis=0)

    def alpha004(self, max_window=20):
        """
        (((SUM(CLOSE,8)/8)+STD(CLOSE,8))<(SUM(CLOSE,2)/2))
        ?-1:(SUM(CLOSE,2)/2<(SUM(CLOSE,8)/8-STD(CLOSE,8))
            ?1:(1<=(VOLUME/MEAN(VOLUME,20))
                ?1:-1))
        """
        ma8 = self.C.rolling(window=8, min_periods=8).mean()
        std8 = self.C.rolling(window=8, min_periods=8).std()
        ma2 = self.C.rolling(window=2, min_periods=2).mean()
        ma20_vol = self.V.rolling(window=max_window, min_periods=max_window).mean()
        
        result = np.where(
            (ma8 + std8) < ma2,
            -1,
            np.where(
                ma2 < (ma8 - std8),
                1,
                np.where(1 <= (self.V / ma20_vol), 1, -1)
            )
        )
        return pd.Series(result, index=self.df.index, name='alpha004')

    # ... 继续 alpha005 到 alpha191（保持原有代码不变）
    def alpha005(self):
        """
        -1*TSMAX(CORR(TSRANK(VOLUME,5),TSRANK(HIGH,5),5),3)
        """
        ts_volume = self.V.rolling(window=5, min_periods=5).apply(lambda x: stats.rankdata(x)[-1] / 5.0)
        ts_high = self.H.rolling(window=5, min_periods=5).apply(lambda x: stats.rankdata(x)[-1] / 5.0)
        corr_ts = ts_volume.rolling(window=5, min_periods=5).corr(ts_high)
        return -1 * corr_ts.rolling(window=3, min_periods=3).max()
    
    def alpha006(self):
        """
        -1*RANK(SIGN(DELTA(OPEN*0.85+HIGH*0.15,4)))
        """
        weighted_price = self.O * 0.85 + self.H * 0.15
        delta = weighted_price.diff(periods=4)
        sign_val = np.sign(delta)
        rank_val = sign_val.rank(axis=0, pct=True)
        return -1 * rank_val
    
    def alpha007(self):
        """
        (RANK(MAX(VWAP-CLOSE,3))+RANK(MIN(VWAP-CLOSE,3)))*RANK(DELTA(VOLUME,3))
        """
        vwap = self.AMOUNT / self.V
        part1 = (vwap - self.C).rolling(window=3, min_periods=3).max().rank(axis=0, pct=True)
        part2 = (vwap - self.C).rolling(window=3, min_periods=3).min().rank(axis=0, pct=True)
        part3 = self.V.diff(3).rank(axis=0, pct=True)
        return (part1 + part2) * part3
    
    def alpha008(self):
        """
        -1*RANK(DELTA((HIGH+LOW)/10+VWAP*0.8,4))
        """
        vwap = self.AMOUNT / self.V
        ma_price = (self.H + self.L) / 10 + vwap * 0.8
        return -1 * ma_price.diff(4).rank(axis=0, pct=True)
    
    def alpha009(self):
        """
        SMA(((HIGH+LOW)/2-(DELAY(HIGH,1)+DELAY(LOW,1))/2)*(HIGH-LOW)/VOLUME,7,2)
        """
        part1 = (self.H + self.L) * 0.5 - (self.H.shift(1) + self.L.shift(1)) * 0.5
        part2 = part1 * (self.H - self.L) / self.V
        return part2.ewm(adjust=False, alpha=float(2) / 7, min_periods=7).mean()
    
    def alpha010(self):
        """
        RANK(MAX(((RET<0)?STD(RET,20):CLOSE)^2,5))
        """
        ret = self.C.pct_change(periods=1)
        std_ret = ret.rolling(window=20, min_periods=20).std()
        part1 = np.where(ret < 0, std_ret, self.C)
        part1 = pd.Series(part1, index=self.df.index)
        return (part1 ** 2).rolling(window=5, min_periods=5).max().rank(axis=0, pct=True)
    
    def alpha011(self):
        """
        SUM(((CLOSE-LOW)-(HIGH-CLOSE))/(HIGH-LOW)*VOLUME,6)
        """
        raw = ((2 * self.C - self.L - self.H) / (self.H - self.L)) * self.V
        return raw.rolling(window=6, min_periods=6).sum()
    
    def alpha012(self):
        """
        RANK(OPEN-MA(VWAP,10))*RANK(ABS(CLOSE-VWAP))*(-1)
        """
        vwap = self.AMOUNT / self.V
        part1 = (self.O - vwap.rolling(window=10, min_periods=10).mean()).rank(axis=0, pct=True)
        part2 = abs(self.C - vwap).rank(axis=0, pct=True)
        return -1 * part1 * part2
    
    def alpha013(self):
        """
        ((HIGH*LOW)^0.5)-VWAP
        """
        vwap = self.AMOUNT / self.V
        return np.sqrt(self.H * self.L) - vwap
    
    def alpha014(self):
        """
        CLOSE-DELAY(CLOSE,5)
        """
        return self.C.diff(5)
    
    def alpha015(self):
        """
        OPEN/DELAY(CLOSE,1)-1
        """
        return self.O / self.C.shift(1) - 1.0
    
    def alpha016(self):
        """
        (-1*TSMAX(RANK(CORR(RANK(VOLUME),RANK(VWAP),5)),5))
        """
        vwap = self.AMOUNT / self.V
        rank_vol = self.V.rank(axis=0, pct=True)
        rank_vwap = vwap.rank(axis=0, pct=True)
        corr_vol_vwap = rank_vol.rolling(window=5, min_periods=5).corr(rank_vwap)
        rank_corr = corr_vol_vwap.rank(axis=0, pct=True)
        return -1 * rank_corr.rolling(window=5, min_periods=5).max()
    
    def alpha017(self):
        """
        RANK(VWAP-MAX(VWAP,15))^DELTA(CLOSE,5)
        """
        vwap = self.AMOUNT / self.V
        delta_price = self.C.diff(5)
        base = (vwap - vwap.rolling(window=15, min_periods=15).max()).rank(axis=0, pct=True)
        return base ** delta_price
    
    def alpha018(self):
        """
        CLOSE/DELAY(CLOSE,5)
        """
        return self.C / self.C.shift(5)
    
    def alpha019(self):
        """
        (CLOSE<DELAY(CLOSE,5)?(CLOSE/DELAY(CLOSE,5)-1):(CLOSE=DELAY(CLOSE,5)?0:(1-DELAY(CLOSE,5)/CLOSE)))
        """
        condition1 = self.C <= self.C.shift(5)
        alpha = self.C.copy()
        alpha[condition1] = self.C.pct_change(periods=5)[condition1]
        alpha[~condition1] = -self.C.pct_change(periods=5)[~condition1]
        return alpha
    
    def alpha020(self):
        """
        (CLOSE/DELAY(CLOSE,6)-1)*100
        """
        return self.C.pct_change(periods=6) * 100.0
    
    def alpha021(self):
        """
        REGBETA(MEAN(CLOSE,6),SEQUENCE(6))
        """
        close_ma = self.C.rolling(window=6, min_periods=6).mean()
        result = pd.Series(index=self.df.index, dtype=float)
        for i in range(6, len(self.df)):
            y = close_ma.iloc[i-6:i]
            x = np.arange(1, 7)
            result.iloc[i] = self._regbeta(y, x)
        return result.fillna(0)
    
    def alpha022(self):
        """
        SMEAN((CLOSE/MEAN(CLOSE,6)-1-DELAY(CLOSE/MEAN(CLOSE,6)-1,3)),12,1)
        """
        ratio = self.C / self.C.rolling(window=6, min_periods=6).mean() - 1.0
        alpha = ratio.diff(3)
        return self._sma(alpha, 12, 1)
    
    def alpha023(self):
        """
        SMA((CLOSE>DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1) / 
        (SMA((CLOSE>DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1)+SMA((CLOSE<=DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1))*100
        """
        prc_std = self.C.rolling(window=20, min_periods=20).std()
        condition1 = self.C > self.C.shift(1)
        part1 = prc_std.copy()
        part2 = prc_std.copy()
        part1[~condition1] = 0.0
        part2[condition1] = 0.0
        sma1 = self._sma(part1, 20, 1)
        sma2 = self._sma(part2, 20, 1)
        return sma1 / (sma1 + sma2) * 100
    
    def alpha024(self):
        """
        SMA(CLOSE-DELAY(CLOSE,5),5,1)
        """
        return self._sma(self.C.diff(5), 5, 1)
    
    def alpha025(self):
        """
        (-1*RANK(DELTA(CLOSE,7)*(1-RANK(DECAYLINEAR(VOLUME/MEAN(VOLUME,20),9)))))*(1+RANK(SUM(RET,250)))
        """
        n_rows = len(self.df)
        if n_rows < 50:
            return pd.Series(index=self.df.index, dtype=float)
        
        if n_rows < 260:
            ret_window = min(250, n_rows - 10)
        else:
            ret_window = 250
        
        w = np.arange(1, 10)
        ret = self.C.pct_change().fillna(0)
        
        part1 = self.C.diff(7).fillna(0)
        vol_ma = self.V.rolling(window=20, min_periods=5).mean().fillna(method='ffill').fillna(method='bfill')
        volume_ratio = (self.V / vol_ma).fillna(method='ffill').fillna(method='bfill')
        
        decay_linear = volume_ratio.rolling(window=9, min_periods=4).apply(
            lambda x: np.dot(x, w[:len(x)]) if len(x) >= 4 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        
        rank_decay = decay_linear.rank(method='min', pct=True).fillna(method='ffill').fillna(method='bfill')
        part2 = 1.0 - rank_decay
        
        sum_ret = ret.rolling(window=ret_window, min_periods=max(10, ret_window//5)).sum().fillna(method='ffill').fillna(method='bfill')
        rank_sum_ret = sum_ret.rank(method='min', pct=True).fillna(method='ffill').fillna(method='bfill')
        part3 = 1.0 + rank_sum_ret
        
        part1_part2 = (part1 * part2).fillna(method='ffill').fillna(method='bfill')
        rank_part1_part2 = part1_part2.rank(method='min', pct=True).fillna(method='ffill').fillna(method='bfill')
        
        alpha = -1.0 * rank_part1_part2 * part3
        return alpha.fillna(method='ffill').fillna(method='bfill')
    
    def alpha026(self):
        """
        (SUM(CLOSE,7)/7-CLOSE+CORR(VWAP,DELAY(CLOSE,5),230))
        """
        n_rows = len(self.df)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        
        part1 = (self.C.rolling(window=7, min_periods=3).mean() - self.C).fillna(method='ffill').fillna(method='bfill')
        
        if n_rows < 230:
            corr_window = max(30, n_rows // 2)
        else:
            corr_window = 230
        
        close_lag5 = self.C.shift(5)
        part2 = vwap.rolling(window=corr_window, min_periods=max(10, corr_window//5)).corr(close_lag5).fillna(method='ffill').fillna(method='bfill')
        
        alpha = (part1 + part2).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha027(self):
        """
        WMA((CLOSE-DELTA(CLOSE,3))/DELAY(CLOSE,3)*100+(CLOSE-DELAY(CLOSE,6))/DELAY(CLOSE,6)*100,12)
        """
        part1 = self.C.pct_change(periods=3) * 100.0 + self.C.pct_change(periods=6) * 100.0
        w = np.arange(1, 13)
        return part1.rolling(window=12, min_periods=12).apply(lambda x: np.dot(x, w))
    
    def alpha028(self):
        """
        3*SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1)
        -2*SMA(SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1),3,1)
        """
        part1 = self.C - self.C.rolling(window=9, min_periods=9).min()
        part2 = self.H.rolling(window=9, min_periods=9).max() - self.L.rolling(window=9, min_periods=9).min()
        rsv = part1 / part2 * 100
        sma1 = self._sma(rsv, 3, 1)
        sma2 = self._sma(sma1, 3, 1)
        return 3 * sma1 - 2 * sma2
    
    def alpha029(self):
        """
        (CLOSE-DELAY(CLOSE,6))/DELAY(CLOSE,6)*VOLUME
        """
        return self.C.pct_change(periods=6) * self.V
    
    def alpha030(self):
        """
        WMA((REGRESI(RET,MKT,SMB,HML,60))^2,20)
        单只股票版本：使用市场指数作为基准
        """
        ret = self.C.pct_change().fillna(0.0)
        if 'index_close' in self.df.columns:
            mkt_ret = self.df['index_close'].pct_change().fillna(0.0)
        else:
            mkt_ret = ret.rolling(window=20, min_periods=20).mean().fillna(0.0)
        
        smb_ret = pd.Series(0, index=ret.index)
        hml_ret = pd.Series(0, index=ret.index)
        
        result = pd.Series(index=self.df.index, dtype=float)
        for i in range(60, len(self.df)):
            y = ret.iloc[i-60:i]
            X = pd.DataFrame({
                'const': 1,
                'mkt': mkt_ret.iloc[i-60:i],
                'smb': smb_ret.iloc[i-60:i],
                'hml': hml_ret.iloc[i-60:i]
            }).dropna()
            y = y.loc[X.index]
            if len(y) >= 20:
                try:
                    result.iloc[i] = sm.OLS(y, X).fit().resid.iloc[-1]
                except:
                    result.iloc[i] = np.nan
            else:
                result.iloc[i] = np.nan
        
        w = np.arange(1, 21) / np.arange(1, 21).sum()
        return (result ** 2).rolling(window=20, min_periods=20).apply(lambda x: np.dot(x, w))
    
    def alpha031(self):
        """
        (CLOSE-MEAN(CLOSE,12))/MEAN(CLOSE,12)*100
        """
        ma = self.C.rolling(window=12, min_periods=12).mean()
        return (self.C / ma - 1.0) * 100
    
    def alpha032(self):
        """
        (-1*SUM(RANK(CORR(RANK(HIGH),RANK(VOLUME),3)),3))
        """
        part1 = self.H.rank(pct=True).rolling(window=3, min_periods=3).corr(self.V.rank(pct=True))
        return -1 * part1.rank(pct=True).rolling(window=3, min_periods=3).sum()
    
    def alpha033(self):
        """
        (-1*TSMIN(LOW,5)+DELAY(TSMIN(LOW,5),5))*RANK((SUM(RET,240)-SUM(RET,20))/220)*TSRANK(VOLUME,5)
        """
        n_rows = len(self.df)
        if n_rows < 10:
            return pd.Series(0, index=self.df.index)
        
        self.V = self.V.replace(0, np.nan).fillna(method='ffill').fillna(method='bfill')
        
        low_min5 = self.L.rolling(window=5, min_periods=3).min().fillna(method='ffill').fillna(method='bfill')
        part1 = -1 * low_min5.diff(5).fillna(0)
        
        if n_rows < 240:
            sum_window1 = min(240, n_rows - 5)
            sum_window2 = min(20, n_rows // 3)
        else:
            sum_window1 = 240
            sum_window2 = 20
        
        ret = self.C.pct_change().fillna(0)
        sum_ret1 = ret.rolling(window=sum_window1, min_periods=max(5, sum_window1//10)).sum().fillna(method='ffill').fillna(method='bfill')
        sum_ret2 = ret.rolling(window=sum_window2, min_periods=max(3, sum_window2//5)).sum().fillna(method='ffill').fillna(method='bfill')
        
        part2_series = ((sum_ret1 - sum_ret2) / 220).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_series.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        part3 = self._tsrank_fixed(self.V, 5).fillna(method='ffill').fillna(method='bfill')
        
        alpha = (part1 * part2 * part3).fillna(0)
        return alpha
    
    def alpha034(self):
        """
        MEAN(CLOSE,12)/CLOSE
        """
        return self.C.rolling(window=12, min_periods=12).mean() / self.C
    
    def alpha035(self):
        """
        (MIN(RANK(DECAYLINEAR(DELTA(OPEN,1),15)),RANK(DECAYLINEAR(CORR(VOLUME,OPEN*0.65+CLOSE*0.35,17),7)))*-1)
        """
        w7 = np.arange(1, 8)
        w15 = np.arange(1, 16)
        part1 = self.O.diff().rolling(window=15, min_periods=15).apply(lambda x: np.dot(x, w15)).rank(pct=True)
        part2 = (self.O * 0.65 + self.C * 0.35).rolling(window=17, min_periods=17).corr(self.V)
        part2 = part2.rolling(window=7, min_periods=7).apply(lambda x: np.dot(x, w7)).rank(pct=True)
        return np.minimum(part1, part2) * (-1)
    
    def alpha036(self):
        """
        RANK(SUM(CORR(RANK(VOLUME),RANK(VWAP),6),2))
        """
        self.V = self.V.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill')
        vol_rank = self.V.rank(pct=True, method='min')
        vwap_rank = vwap.rank(pct=True, method='min')
        part1 = vol_rank.rolling(window=6, min_periods=3).corr(vwap_rank)
        return part1.rolling(window=2, min_periods=1).sum().rank(pct=True, method='min')
    
    def alpha037(self):
        """
        (-1*RANK(SUM(OPEN,5)*SUM(RET,5)-DELAY(SUM(OPEN,5)*SUM(RET,5),10)))
        """
        part1 = self.O.rolling(window=5, min_periods=5).sum() * self.C.pct_change().rolling(window=5, min_periods=5).sum()
        return -1 * part1.diff(10)
    
    def alpha038(self):
        """
        ((SUM(HIGH,20)/20)<HIGH)?(-1*DELTA(HIGH,2)):0
        """
        condition = self.H.rolling(window=20, min_periods=20).mean() < self.H
        alpha = -1 * self.H.diff(2)
        alpha[~condition] = 0.0
        return alpha
    
    def alpha039(self):
        """
        (RANK(DECAYLINEAR(DELTA(CLOSE,2),8))-RANK(DECAYLINEAR(CORR(VWAP*0.3+OPEN*0.7,SUM(MEAN(VOLUME,180),37),14),12)))*-1
        使用填充版本
        """
        n_rows = len(self.df)
        if n_rows < 200:
            return self._alpha039_small_data()
        
        w8 = np.arange(1, 9)
        w12 = np.arange(1, 13)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        
        parta = vwap * 0.3 + self.O * 0.7
        V_filled = self.V.fillna(method='ffill').fillna(method='bfill')
        
        vol_window = min(180, n_rows // 2)
        vol_min_periods = min(vol_window, max(10, vol_window // 10))
        vol_ma = V_filled.rolling(window=vol_window, min_periods=vol_min_periods).mean().fillna(method='ffill').fillna(method='bfill')
        
        sum_window = min(37, n_rows // 4)
        sum_min_periods = min(sum_window, max(5, sum_window // 4))
        partb = vol_ma.rolling(window=sum_window, min_periods=sum_min_periods).sum().fillna(method='ffill').fillna(method='bfill')
        
        part1 = self.C.diff(2).fillna(0)
        decay_window1 = 8
        decay_min_periods1 = min(decay_window1, max(3, decay_window1 // 2))
        part1_decay = part1.rolling(window=decay_window1, min_periods=decay_min_periods1).apply(
            lambda x: np.dot(x, w8[:len(x)]) if len(x) >= decay_min_periods1 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min')
        
        corr_window = min(14, n_rows // 8)
        corr_min_periods = min(corr_window, max(3, corr_window // 2))
        part2_corr = parta.rolling(window=corr_window, min_periods=corr_min_periods).corr(partb).fillna(0)
        
        decay_window2 = min(12, n_rows // 8)
        decay_min_periods2 = min(decay_window2, max(3, decay_window2 // 2))
        part2_decay = part2_corr.rolling(window=decay_window2, min_periods=decay_min_periods2).apply(
            lambda x: np.dot(x, w12[:len(x)]) if len(x) >= decay_min_periods2 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min')
        
        return -1 * (part1 - part2).fillna(method='ffill').fillna(method='bfill')
    
    def _alpha039_small_data(self):
        """
        小数据量版本
        """
        n_rows = len(self.df)
        w8 = np.arange(1, 9)
        w12 = np.arange(1, 13)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        
        parta = vwap * 0.3 + self.O * 0.7
        V_filled = self.V.fillna(method='ffill').fillna(method='bfill')
        
        vol_window = min(30, n_rows // 2)
        vol_min_periods = min(vol_window, max(3, vol_window // 3))
        vol_ma = V_filled.rolling(window=vol_window, min_periods=vol_min_periods).mean().fillna(method='ffill').fillna(method='bfill')
        
        sum_window = min(10, n_rows // 3)
        sum_min_periods = min(sum_window, max(3, sum_window // 2))
        partb = vol_ma.rolling(window=sum_window, min_periods=sum_min_periods).sum().fillna(method='ffill').fillna(method='bfill')
        
        part1 = self.C.diff(2).fillna(0)
        decay_window1 = min(8, n_rows // 3)
        decay_min_periods1 = min(decay_window1, max(2, decay_window1 // 2))
        part1_decay = part1.rolling(window=decay_window1, min_periods=decay_min_periods1).apply(
            lambda x: np.dot(x, w8[:len(x)]) if len(x) >= decay_min_periods1 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min')
        
        corr_window = min(8, n_rows // 4)
        corr_min_periods = min(corr_window, max(2, corr_window // 2))
        part2_corr = parta.rolling(window=corr_window, min_periods=corr_min_periods).corr(partb).fillna(0)
        
        decay_window2 = min(8, n_rows // 4)
        decay_min_periods2 = min(decay_window2, max(2, decay_window2 // 2))
        part2_decay = part2_corr.rolling(window=decay_window2, min_periods=decay_min_periods2).apply(
            lambda x: np.dot(x, w12[:len(x)]) if len(x) >= decay_min_periods2 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min')
        
        return -1 * (part1 - part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha040(self):
        """
        SUM(CLOSE>DELAY(CLOSE,1)?VOLUME:0,26)/SUM(CLOSE<=DELAY(CLOSE,1)?VOLUME:0,26)*100
        """
        diff = self.C.diff()
        part1 = ((diff > 0) * self.V).rolling(window=26, min_periods=26).sum()
        part2 = ((diff <= 0) * self.V).rolling(window=26, min_periods=26).sum()
        return part1 / part2 * 100
    
    def alpha041(self):
        """
        RANK(MAX(DELTA(VWAP,3),5))*-1
        """
        self.V = self.V.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        vwap_diff = vwap.diff(3)
        vwap_max = vwap_diff.rolling(window=5, min_periods=3).max()
        return -1 * vwap_max.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
    
    def alpha042(self):
        """
        (-1*RANK(STD(HIGH,10)))*CORR(HIGH,VOLUME,10)
        """
        part1 = -1 * self.H.rolling(window=10, min_periods=10).std().rank(pct=True)
        part2 = self.H.rolling(window=10, min_periods=10).corr(self.V)
        return part1 * part2
    
    def alpha043(self):
        """
        (SUM(CLOSE>DELAY(CLOSE,1)?VOLUME:(CLOSE<DELAY(CLOSE,1)?-VOLUME:0),6))
        """
        diff = self.C.diff()
        part1 = ((diff > 0) * self.V).rolling(window=6, min_periods=6).sum()
        part2 = ((diff < 0) * -self.V).rolling(window=6, min_periods=6).sum()
        return part1 + part2
    
    def alpha044(self):
        """
        (TSRANK(DECAYLINEAR(CORR(LOW,MEAN(VOLUME,10),7),6),4)+TSRANK(DECAYLINEAR(DELTA(VWAP,3),10),15))
        """
        w6 = np.arange(1, 7)
        w10 = np.arange(1, 11)
        self.V = self.V.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        
        vol_ma = self.V.rolling(window=10, min_periods=5).mean().fillna(method='ffill').fillna(method='bfill')
        part1_corr = vol_ma.rolling(window=7, min_periods=4).corr(self.L).fillna(method='ffill').fillna(method='bfill')
        part1_decay = part1_corr.rolling(window=6, min_periods=3).apply(
            lambda x: np.dot(x, w6[:len(x)]) if len(x) >= 3 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = self._tsrank_fixed(part1_decay, 4)
        
        vwap_diff = vwap.diff(3).fillna(0)
        part2_decay = vwap_diff.rolling(window=10, min_periods=5).apply(
            lambda x: np.dot(x, w10[:len(x)]) if len(x) >= 5 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = self._tsrank_fixed(part2_decay, 15)
        
        return part1 + part2
    
    def alpha045(self):
        """
        (RANK(DELTA(CLOSE*0.6+OPEN*0.4,1))*RANK(CORR(VWAP,MEAN(VOLUME,150),15)))
        调整版本：根据数据量动态调整窗口
        """
        n_rows = len(self.df)
        vol_window = max(20, n_rows // 3) if n_rows < 150 else 150
        
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        
        weighted_price = self.C * 0.6 + self.O * 0.4
        part1 = weighted_price.diff().fillna(0).rank(pct=True, method='min')
        
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(5, vol_window//10)).mean().fillna(method='ffill').fillna(method='bfill')
        part2_corr = vwap.rolling(window=15, min_periods=5).corr(vol_ma).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_corr.rank(pct=True, method='min')
        
        return (part1 * part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha046(self):
        """
        (MEAN(CLOSE,3)+MEAN(CLOSE,6)+MEAN(CLOSE,12)+MEAN(CLOSE,24))/(4*CLOSE)
        """
        ma3 = self.C.rolling(window=3, min_periods=3).mean()
        ma6 = self.C.rolling(window=6, min_periods=6).mean()
        ma12 = self.C.rolling(window=12, min_periods=12).mean()
        ma24 = self.C.rolling(window=24, min_periods=24).mean()
        return (ma3 + ma6 + ma12 + ma24) / (4 * self.C)
    
    def alpha047(self):
        """
        SMA((TSMAX(HIGH,6)-CLOSE)/(TSMAX(HIGH,6)-TSMIN(LOW,6))*100,9,1)
        """
        high_max = self.H.rolling(window=6, min_periods=6).max()
        low_min = self.L.rolling(window=6, min_periods=6).min()
        part1 = (high_max - self.C) / (high_max - low_min) * 100
        return self._sma(part1, 9, 1)
    
    def alpha048(self):
        """
        -1*RANK(SIGN(CLOSE-DELAY(CLOSE,1))+SIGN(DELAY(CLOSE,1)-DELAY(CLOSE,2))+SIGN(DELAY(CLOSE,2)-DELAY(CLOSE,3)))*SUM(VOLUME,5)/SUM(VOLUME,20)
        """
        diff1 = self.C.diff()
        part1 = (np.sign(diff1) + np.sign(diff1.shift(1)) + np.sign(diff1.shift(2))).rank(pct=True)
        part2 = self.V.rolling(window=5, min_periods=5).sum() / self.V.rolling(window=20, min_periods=20).sum()
        return -1 * part1 * part2
    
    def alpha049(self):
        """
        SUM(HIGH+LOW>=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)/
        (SUM(HIGH+LOW>=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)+
        SUM(HIGH+LOW<=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12))
        """
        hl_sum = self.H + self.L
        condition1 = hl_sum >= hl_sum.shift(1)
        condition2 = hl_sum <= hl_sum.shift(1)
        max_abs = np.maximum(abs(self.H.diff()), abs(self.L.diff()))
        
        part1 = max_abs.copy()
        part2 = max_abs.copy()
        part1[condition1] = 0.0
        part2[condition2] = 0.0
        
        sum1 = part1.rolling(window=12, min_periods=12).sum()
        sum2 = part2.rolling(window=12, min_periods=12).sum()
        return sum1 / (sum1 + sum2)
    
    def alpha050(self):
        """
        SUM(HIGH+LOW<=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)/
        (SUM(HIGH+LOW<=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)
        +SUM(HIGH+LOW>=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12))
        -SUM(HIGH+LOW>=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)/
        (SUM(HIGH+LOW>=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12)
        +SUM(HIGH+LOW<=DELAY(HIGH,1)+DELAY(LOW,1)?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1))),12))
        """
        hl_sum = self.H + self.L
        condition1 = hl_sum >= hl_sum.shift(1)
        condition2 = hl_sum <= hl_sum.shift(1)
        max_abs = np.maximum(abs(self.H.diff()), abs(self.L.diff()))
        
        part1 = max_abs.copy()
        part2 = max_abs.copy()
        part1[condition2] = 0.0
        part2[condition1] = 0.0
        
        sum1 = part1.rolling(window=12, min_periods=12).sum()
        sum2 = part2.rolling(window=12, min_periods=12).sum()
        return sum1 / (sum1 + sum2) - sum2 / (sum1 + sum2)
    
    def alpha051(self):
        """
        SUM(((HIGH+LOW)<=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1)))),12)/
        (SUM(((HIGH+LOW)<=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1)))),12)
        +SUM(((HIGH+LOW)>=(DELAY(HIGH,1)+DELAY(LOW,1))?0:MAX(ABS(HIGH-DELAY(HIGH,1)),ABS(LOW-DELAY(LOW,1)))),12))
        """
        hl_sum = self.H + self.L
        condition1 = hl_sum <= hl_sum.shift(1)
        condition2 = hl_sum >= hl_sum.shift(1)
        max_abs = np.maximum(abs(self.H.diff()), abs(self.L.diff()))
        
        part1 = max_abs.copy()
        part2 = max_abs.copy()
        part1[condition1] = 0.0
        part2[condition2] = 0.0
        
        sum1 = part1.rolling(window=12, min_periods=12).sum()
        sum2 = part2.rolling(window=12, min_periods=12).sum()
        return sum1 / (sum1 + sum2)
    
    def alpha052(self):
        """
        SUM(MAX(0,HIGH-DELAY((HIGH+LOW+CLOSE)/3,1)),26)/SUM(MAX(0,DELAY((HIGH+LOW+CLOSE)/3,1)-L),26)*100
        """
        ma = (self.H + self.L + self.C) / 3.0
        part1 = np.maximum(0.0, self.H - ma.shift(1)).rolling(window=26, min_periods=26).sum()
        part2 = np.maximum(0.0, ma.shift(1) - self.L).rolling(window=26, min_periods=26).sum()
        return part1 / part2 * 100.0
    
    def alpha053(self):
        """
        COUNT(CLOSE>DELAY(CLOSE,1),12)/12*100
        """
        return (self.C.diff() > 0.0).rolling(window=12, min_periods=12).sum() / 12.0 * 100
    
    def alpha054(self):
        """
        (-1*RANK(STD(ABS(CLOSE-OPEN))+CLOSE-OPEN+CORR(CLOSE,OPEN,10)))
        """
        part1 = abs(self.C - self.O).rolling(window=10, min_periods=10).std() + self.C - self.O + self.C.rolling(window=10, min_periods=10).corr(self.O)
        return -1 * part1.rank(pct=True)
    
    def alpha055(self):
        """
        SUM(16*(CLOSE+(CLOSE-OPEN)/2-DELAY(OPEN,1))/
        ((ABS(HIGH-DELAY(CLOSE,1))>ABS(LOW-DELAY(CLOSE,1)) & ABS(HIGH-DELAY(CLOSE,1))>ABS(HIGH-DELAY(LOW,1)) ? 
        ABS(HIGH-DELAY(CLOSE,1))+ABS(LOW-DELAY(CLOSE,1))/2+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4:
        (ABS(LOW-DELAY(CLOSE,1))>ABS(HIGH-DELAY(LOW,1)) & ABS(LOW-DELAY(CLOSE,1))>ABS(HIGH-DELAY(CLOSE,1)) ?
        ABS(LOW-DELAY(CLOSE,1))+ABS(HIGH-DELAY(CLOSE,1))/2+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4:
        ABS(HIGH-DELAY(LOW,1))+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4)))
        *MAX(ABS(HIGH-DELAY(CLOSE,1)),ABS(LOW-DELAY(CLOSE,1))),20)
        """
        part1 = self.C * 1.5 - self.O * 0.5 - self.O.shift(1)
        part2 = abs(self.H - self.C.shift(1)) + abs(self.L - self.C.shift(1)) / 2.0 + abs(self.C - self.O).shift(1) / 4.0
        
        condition1 = np.logical_and(
            abs(self.H - self.C.shift(1)) > abs(self.L - self.C.shift(1)),
            abs(self.H - self.C.shift(1)) > abs(self.H - self.L.shift(1))
        )
        condition2 = np.logical_and(
            abs(self.L - self.C.shift(1)) > abs(self.H - self.L.shift(1)),
            abs(self.L - self.C.shift(1)) > abs(self.H - self.C.shift(1))
        )
        
        part2[~condition1 & condition2] = abs(self.L - self.C.shift(1)) + abs(self.H - self.C.shift(1)) / 2.0 + abs(self.C - self.O).shift(1) / 4.0
        part2[~condition1 & ~condition2] = abs(self.H - self.L.shift(1)) + abs(self.C - self.O).shift(1) / 4.0
        
        part3 = np.maximum(abs(self.H - self.C.shift(1)), abs(self.L - self.C.shift(1)))
        alpha = (part1 / part2 * part3 * 16.0).rolling(window=20, min_periods=20).sum()
        return alpha
    
    def alpha056(self):
        """
        RANK(OPEN-TSMIN(OPEN,12))<RANK(RANK(CORR(SUM((HIGH +LOW)/2,19),SUM(MEAN(VOLUME,40),19),13))^5)
        """
        part1 = (self.O - self.O.rolling(window=12, min_periods=12).min()).rank(pct=True)
        t1 = (self.H * 0.5 + self.L * 0.5).rolling(window=19, min_periods=19).sum()
        t2 = self.V.rolling(window=40, min_periods=40).mean().rolling(window=19, min_periods=19).sum()
        part2 = (t1.rolling(window=13, min_periods=13).corr(t2).rank(pct=True) ** 5).rank(pct=True)
        return part2 - part1
    
    def alpha057(self):
        """
        SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1)
        """
        part1 = self.C - self.C.rolling(window=9, min_periods=9).min()
        part2 = self.H.rolling(window=9, min_periods=9).max() - self.L.rolling(window=9, min_periods=9).min()
        rsv = part1 / part2 * 100
        return self._sma(rsv, 3, 1)
    
    def alpha058(self):
        """
        COUNT(CLOSE>DELAY(CLOSE,1),20)/20*100
        """
        return (self.C.diff() > 0.0).rolling(window=20, min_periods=20).sum() / 20.0 * 100
    
    def alpha059(self):
        """
        SUM((CLOSE=DELAY(CLOSE,1)?0:CLOSE-(CLOSE>DELAY(CLOSE,1)?MIN(LOW,DELAY(CLOSE,1)):MAX(HIGH,DELAY(CLOSE,1)))),20)
        """
        alpha = self.C.copy()
        diff = self.C.diff()
        condition1 = diff > 0.0
        condition2 = diff < 0.0
        
        alpha[condition1] = self.C[condition1] - np.minimum(self.L[condition1], self.C.shift(1)[condition1])
        alpha[condition2] = self.C[condition2] - np.maximum(self.H[condition2], self.C.shift(1)[condition2])
        alpha[diff == 0] = 0.0
        
        return alpha.rolling(window=20, min_periods=20).sum()
    
    def alpha060(self):
        """
        SUM((2*CLOSE-LOW-HIGH)/(HIGH-LOW)*VOLUME,20)
        """
        price_range = (self.H - self.L).replace(0, 1e-10)
        numerator = 2 * self.C - self.L - self.H
        ratio = numerator / price_range
        part1 = (ratio * self.V).fillna(method='ffill').fillna(method='bfill')
        alpha = part1.rolling(window=20, min_periods=10).sum().fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha061(self):
        """
        MAX(RANK(DECAYLINEAR(DELTA(VWAP,1),12)),RANK(DECAYLINEAR(RANK(CORR(LOW,MEAN(VOLUME,80),8)),17)))*-1
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        
        w12 = np.arange(1, 13)
        vwap_diff = vwap.diff().fillna(0)
        part1_decay = vwap_diff.rolling(window=12, min_periods=6).apply(
            lambda x: np.dot(x, w12[:len(x)]) if len(x) >= 6 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min')
        
        vol_window = min(80, len(self.df) // 2)
        turnover_ma = self.V.rolling(window=vol_window, min_periods=max(5, vol_window//10)).mean().fillna(method='ffill').fillna(method='bfill')
        part2_corr = turnover_ma.rolling(window=8, min_periods=4).corr(self.L).fillna(method='ffill').fillna(method='bfill')
        part2_rank = part2_corr.rank(pct=True, method='min')
        
        w17 = np.arange(1, 18)
        part2_decay = part2_rank.rolling(window=17, min_periods=8).apply(
            lambda x: np.dot(x, w17[:len(x)]) if len(x) >= 8 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min')
        
        return -1 * np.maximum(part1, part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha062(self):
        """
        -1*CORR(HIGH,RANK(VOLUME),5)
        """
        return -1 * self.V.rank(pct=True).rolling(window=5, min_periods=5).corr(self.H)
    
    def alpha063(self):
        """
        SMA(MAX(CLOSE-DELAY(CLOSE,1),0),6,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),6,1)*100
        """
        diff = self.C.diff()
        part1 = np.maximum(diff, 0.0)
        part2 = abs(diff)
        sma1 = self._sma(part1, 6, 1)
        sma2 = self._sma(part2, 6, 1)
        return sma1 / sma2 * 100.0
    
    def alpha064(self):
        """
        (MAX(RANK(DECAYLINEAR(CORR(RANK(VWAP),RANK(VOLUME),4),4)),RANK(DECAYLINEAR(MAX(CORR(RANK(CLOSE),RANK(MEAN(VOLUME,60)),4),13),14)))*-1)
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w4 = np.arange(1, 5)
        w14 = np.arange(1, 15)
        
        vwap_rank = vwap.rank(pct=True, method='min')
        vol_rank = self.V.rank(pct=True, method='min')
        
        part1_corr = vwap_rank.rolling(window=4, min_periods=3).corr(vol_rank).fillna(method='ffill').fillna(method='bfill')
        part1_decay = part1_corr.rolling(window=4, min_periods=3).apply(
            lambda x: np.dot(x, w4[:len(x)]) if len(x) >= 3 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min')
        
        vol_window = min(60, len(self.df) // 2)
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(5, vol_window//10)).mean().fillna(method='ffill').fillna(method='bfill')
        vol_ma_rank = vol_ma.rank(pct=True, method='min')
        close_rank = self.C.rank(pct=True, method='min')
        
        part2_corr = close_rank.rolling(window=4, min_periods=3).corr(vol_ma_rank).fillna(method='ffill').fillna(method='bfill')
        part2_max = part2_corr.rolling(window=13, min_periods=7).max().fillna(method='ffill').fillna(method='bfill')
        part2_decay = part2_max.rolling(window=14, min_periods=7).apply(
            lambda x: np.dot(x, w14[:len(x)]) if len(x) >= 7 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min')
        
        return -1 * np.maximum(part1, part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha065(self):
        """
        MEAN(CLOSE,6)/CLOSE
        """
        return self.C.rolling(window=6, min_periods=6).mean() / self.C
    
    def alpha066(self):
        """
        (CLOSE-MEAN(CLOSE,6))/MEAN(CLOSE,6)*100
        """
        ma = self.C.rolling(window=6, min_periods=6).mean()
        return (self.C - ma) / ma * 100
    
    def alpha067(self):
        """
        SMA(MAX(CLOSE-DELAY(CLOSE,1),0),24,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),24,1)*100
        """
        diff = self.C.diff()
        part1 = np.maximum(diff, 0.0)
        part2 = abs(diff)
        sma1 = self._sma(part1, 24, 1)
        sma2 = self._sma(part2, 24, 1)
        return sma1 / sma2 * 100
    
    def alpha068(self):
        """
        SMA(((HIGH+LOW)/2-(DELAY(HIGH,1)+DELAY(LOW,1))/2)*(HIGH-LOW)/VOLUME,15,2)
        """
        part1 = (self.H.diff() * 0.5 + self.L.diff() * 0.5) * (self.H - self.L) / self.V
        return self._sma(part1, 15, 2)
    
    def alpha069(self):
        """
        (SUM(DTM,20)>SUM(DBM,20)?(SUM(DTM,20)-SUM(DBM,20))/SUM(DTM,20):
        (SUM(DTM,20)=SUM(DBM,20)?0:(SUM(DTM,20)-SUM(DBM,20))/SUM(DBM,20)))
        """
        dtm = (self.O.diff() <= 0) * np.maximum(self.H - self.O, self.O.diff())
        dbm = (self.O.diff() >= 0) * np.maximum(self.O - self.L, self.O.diff())
        
        dtm_sum = dtm.rolling(window=20, min_periods=20).sum()
        dbm_sum = dbm.rolling(window=20, min_periods=20).sum()
        
        result = pd.Series(index=self.df.index, dtype=float)
        mask_gt = dtm_sum > dbm_sum
        mask_eq = dtm_sum == dbm_sum
        mask_lt = dtm_sum < dbm_sum
        
        result[mask_gt] = (dtm_sum[mask_gt] - dbm_sum[mask_gt]) / dtm_sum[mask_gt]
        result[mask_eq] = 0.0
        result[mask_lt] = (dtm_sum[mask_lt] - dbm_sum[mask_lt]) / dbm_sum[mask_lt]
        
        return result
    
    def alpha070(self):
        """
        STD(AMOUNT,6)
        """
        return self.AMOUNT.rolling(window=6, min_periods=6).std()
    
    def alpha071(self):
        """
        (CLOSE-MEAN(CLOSE,24))/MEAN(CLOSE,24)*100
        """
        ma = self.C.rolling(window=24, min_periods=24).mean()
        return (self.C - ma) / ma * 100
    
    def alpha072(self):
        """
        SMA((TSMAX(HIGH,6)-CLOSE)/(TSMAX(HIGH,6)-TSMIN(LOW,6))*100,15,1)
        """
        high_max = self.H.rolling(window=6, min_periods=6).max()
        low_min = self.L.rolling(window=6, min_periods=6).min()
        part1 = (high_max - self.C) / (high_max - low_min) * 100.0
        return self._sma(part1, 15, 1)
    
    def alpha073(self):
        """
        ((TSRANK(DECAYLINEAR(DECAYLINEAR(CORR(CLOSE,VOLUME,10),16),4),5)-RANK(DECAYLINEAR(CORR(VWAP,MEAN(VOLUME,30),4),3)))*-1)
        ETF专用版本
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        def normalize(series):
            return (series - series.min()) / (series.max() - series.min() + 1e-10)
        
        part1_corr = self.C.rolling(window=10, min_periods=5).corr(self.V).fillna(method='ffill').fillna(method='bfill')
        part1_ema1 = part1_corr.ewm(span=16, adjust=False, min_periods=5).mean()
        part1_ema2 = part1_ema1.ewm(span=4, adjust=False, min_periods=3).mean()
        part1 = normalize(part1_ema2)
        
        vol_window = min(30, len(self.df) // 2)
        vol_ma = self.V.rolling(window=vol_window, min_periods=5).mean().fillna(method='ffill').fillna(method='bfill')
        part2_corr = vwap.rolling(window=4, min_periods=3).corr(vol_ma).fillna(method='ffill').fillna(method='bfill')
        
        w3 = np.arange(1, 4) / np.arange(1, 4).sum()
        part2 = part2_corr.rolling(window=3, min_periods=2).apply(
            lambda x: np.sum(x * w3[:len(x)]) if len(x) >= 2 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = normalize(part2)
        
        return -1 * (part1 - part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha074(self):
        """
        RANK(CORR(SUM(LOW*0.35+VWAP*0.65,20),SUM(MEAN(VOLUME,40),20),7))+RANK(CORR(RANK(VWAP),RANK(VOLUME),6))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        weighted_price = self.L * 0.35 + vwap * 0.65
        sum1 = weighted_price.rolling(window=20, min_periods=10).sum().fillna(method='ffill').fillna(method='bfill')
        
        vol_window = min(40, len(self.df) // 2)
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(5, vol_window//8)).mean().fillna(method='ffill').fillna(method='bfill')
        sum2 = vol_ma.rolling(window=20, min_periods=10).sum().fillna(method='ffill').fillna(method='bfill')
        
        part1_corr = sum1.rolling(window=7, min_periods=4).corr(sum2).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_corr.rank(pct=True, method='min')
        
        vwap_rank = vwap.rank(pct=True, method='min')
        vol_rank = self.V.rank(pct=True, method='min')
        part2_corr = vwap_rank.rolling(window=6, min_periods=4).corr(vol_rank).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_corr.rank(pct=True, method='min')
        
        return (part1 + part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha075(self):
        """
        COUNT(CLOSE>OPEN & BANCHMARK_INDEX_CLOSE<BANCHMARK_INDEX_OPEN,50)/COUNT(BANCHMARK_INDEX_CLOSE<BANCHMARK_INDEX_OPEN,50)
        使用指数数据
        """
        n_rows = len(self.df)
        
        if hasattr(self, 'index_df') and self.index_df is not None:
            index_data = self.index_df.copy()
            if 'close' in index_data.columns:
                index_close = index_data['close']
            else:
                index_close = index_data.iloc[:, 0]
            
            if 'open' in index_data.columns:
                index_open = index_data['open']
            else:
                index_open = index_close.shift(1).fillna(index_close)
            
            if 'date' in self.df.columns and 'date' in index_data.columns:
                self.df['date'] = pd.to_datetime(self.df['date'])
                index_data['date'] = pd.to_datetime(index_data['date'])
                close_map = dict(zip(index_data['date'], index_close))
                open_map = dict(zip(index_data['date'], index_open))
                bm_close = self.df['date'].map(close_map).fillna(method='ffill').fillna(method='bfill')
                bm_open = self.df['date'].map(open_map).fillna(method='ffill').fillna(method='bfill')
            else:
                bm_close = index_close.reindex(self.df.index, method='ffill')
                bm_open = index_open.reindex(self.df.index, method='ffill')
        else:
            bm_close = self.C.rolling(window=20, min_periods=5).mean().fillna(method='ffill').fillna(method='bfill')
            bm_open = self.O.rolling(window=20, min_periods=5).mean().fillna(method='ffill').fillna(method='bfill')
        
        bm_down = bm_close < bm_open
        stock_up = self.C > self.O
        condition = stock_up & bm_down
        
        if condition.sum() == 0:
            bm_ret = bm_close.pct_change().fillna(0)
            bm_down_ret = bm_ret < 0
            condition = stock_up & bm_down_ret
            bm_down = bm_down_ret
        
        window = min(50, n_rows // 2)
        min_periods = max(5, window // 3)
        
        numerator = condition.rolling(window=window, min_periods=min_periods).sum()
        denominator = bm_down.rolling(window=window, min_periods=min_periods).sum().replace(0, np.nan)
        alpha = (numerator / denominator).fillna(method='ffill').fillna(method='bfill').fillna(0)
        
        return alpha
    
    def alpha076(self):
        """
        STD(ABS(CLOSE/DELAY(CLOSE,1)-1)/VOLUME,20)/MEAN(ABS(CLOSE/DELAY(CLOSE,1)-1)/VOLUME,20)
        """
        self.V = self.V.replace(0, np.nan).fillna(method='ffill').fillna(method='bfill')
        ret = self.C.pct_change().fillna(0).replace([np.inf, -np.inf], 0)
        ret_vol = (abs(ret) / self.V).fillna(method='ffill').fillna(method='bfill')
        std = ret_vol.rolling(window=20, min_periods=10).std()
        mean = ret_vol.rolling(window=20, min_periods=10).mean().replace(0, np.nan)
        alpha = (std / mean).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha077(self):
        """
        MIN(RANK(DECAYLINEAR(HIGH*0.5+LOW*0.5-VWAP,20)),RANK(DECAYLINEAR(CORR(HIGH*0.5+LOW*0.5,MEAN(VOLUME,40),3),6)))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w6 = np.arange(1, 7)
        w20 = np.arange(1, 21)
        
        hl_avg = self.H * 0.5 + self.L * 0.5
        part1_series = hl_avg - vwap
        part1_decay = part1_series.rolling(window=20, min_periods=10).apply(
            lambda x: np.dot(x, w20[:len(x)]) if len(x) >= 10 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min')
        
        vol_window = min(40, len(self.df) // 2)
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(5, vol_window//8)).mean().fillna(method='ffill').fillna(method='bfill')
        part2_corr = hl_avg.rolling(window=3, min_periods=2).corr(vol_ma).fillna(method='ffill').fillna(method='bfill')
        part2_decay = part2_corr.rolling(window=6, min_periods=3).apply(
            lambda x: np.dot(x, w6[:len(x)]) if len(x) >= 3 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min')
        
        return np.minimum(part1, part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha078(self):
        """
        ((HIGH+LOW+CLOSE)/3-MA((HIGH+LOW+CLOSE)/3,12))/(0.015*MEAN(ABS(CLOSE-MEAN((HIGH+LOW+CLOSE)/3,12)),12))
        """
        tp = (self.H + self.L + self.C) / 3
        tp_ma = tp.rolling(window=12, min_periods=12).mean()
        part1 = tp - tp_ma
        part2 = abs(self.C - tp_ma).rolling(window=12, min_periods=12).mean() * 0.015
        return part1 / part2
    
    def alpha079(self):
        """
        SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100
        """
        diff = self.C.diff()
        part1 = np.maximum(diff, 0.0)
        part2 = abs(diff)
        sma1 = self._sma(part1, 12, 1)
        sma2 = self._sma(part2, 12, 1)
        return sma1 / sma2 * 100
    
    def alpha080(self):
        """
        (VOLUME-DELAY(VOLUME,5))/DELAY(VOLUME,5)*100
        """
        return self.V.pct_change(periods=5) * 100.0
    
    def alpha081(self):
        """
        SMA(VOLUME,21,2)
        """
        return self._sma(self.V, 21, 2)
    
    def alpha082(self):
        """
        SMA((TSMAX(HIGH,6)-CLOSE)/(TSMAX(HIGH,6)-TSMIN(LOW,6))*100,20,1)
        """
        high_max = self.H.rolling(window=6, min_periods=6).max()
        low_min = self.L.rolling(window=6, min_periods=6).min()
        part1 = (high_max - self.C) / (high_max - low_min) * 100
        return self._sma(part1, 20, 1)
    
    def alpha083(self):
        """
        (-1*RANK(COVIANCE(RANK(HIGH),RANK(VOLUME),5)))
        """
        alpha = self.H.rank(pct=True).rolling(window=5, min_periods=5).cov(self.V.rank(pct=True))
        return -1 * alpha.rank(pct=True)
    
    def alpha084(self):
        """
        SUM((CLOSE>DELAY(CLOSE,1)?VOLUME:(CLOSE<DELAY(CLOSE,1)?-VOLUME:0)),20)
        """
        part1 = np.sign(self.C.diff()) * self.V
        return part1.rolling(window=20, min_periods=20).sum()
    
    def alpha085(self):
        """
        TSRANK(VOLUME/MEAN(VOLUME,20),20)*TSRANK(-1*DELTA(CLOSE,7),8)
        """
        part1 = self.V / self.V.rolling(window=20, min_periods=20).mean()
        part1 = self._tsrank(part1, 20)
        part2 = -1 * self.C.diff(7)
        part2 = self._tsrank(part2, 8)
        return part1 * part2
    
    def alpha086(self):
        """
        ((0.25<((DELAY(CLOSE,20)-DELAY(CLOSE,10))/10-(DELAY(CLOSE,10)-CLOSE)/10))?-1:((((DELAY(CLOSE,20)-DELAY(CLOSE,10))/10-(DELAY(CLOSE,10)-CLOSE)/10)<0)?1:(DELAY(CLOSE,1)-CLOSE)))
        """
        part = (self.C.shift(20) - self.C.shift(10)) / 10 - (self.C.shift(10) - self.C) / 10
        condition1 = part > 0.25
        condition2 = part < 0.0
        
        alpha = pd.Series(index=self.df.index, dtype=float)
        alpha[condition1] = -1.0
        alpha[~condition1 & condition2] = 1.0
        alpha[~condition1 & ~condition2] = self.C.shift(1) - self.C
        
        return alpha
    
    def alpha087(self):
        """
        (RANK(DECAYLINEAR(DELTA(VWAP,4),7))+TSRANK(DECAYLINEAR((LOW-VWAP)/(OPEN-(HIGH+LOW)/2),11),7))*-1
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w7 = np.arange(1, 8)
        w11 = np.arange(1, 12)
        
        vwap_diff = vwap.diff(4).fillna(0)
        part1_decay = vwap_diff.rolling(window=7, min_periods=4).apply(
            lambda x: np.dot(x, w7[:len(x)]) if len(x) >= 4 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min')
        
        hl_avg = (self.H + self.L) / 2
        denominator = self.O - hl_avg
        denominator = denominator.replace(0, 1e-10)
        mask_small = abs(denominator) < 1e-8
        denominator[mask_small] = 1e-10 * np.sign(denominator[mask_small])
        
        part2_series = (self.L - vwap) / denominator
        part2_series = part2_series.replace([np.inf, -np.inf], np.nan).fillna(method='ffill').fillna(method='bfill').clip(-100, 100)
        
        part2_decay = part2_series.rolling(window=11, min_periods=6).apply(
            lambda x: np.dot(x, w11[:len(x)]) if len(x) >= 6 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = self._tsrank_fixed(part2_decay, 7)
        
        return -1 * (part1 + part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha088(self):
        """
        (CLOSE-DELAY(CLOSE,20))/DELAY(CLOSE,20)*100
        """
        return self.C.pct_change(periods=20) * 100
    
    def alpha089(self):
        """
        2*(SMA(CLOSE,13,2)-SMA(CLOSE,27,2)-SMA(SMA(CLOSE,13,2)-SMA(CLOSE,27,2),10,2))
        """
        sma13 = self._sma(self.C, 13, 2)
        sma27 = self._sma(self.C, 27, 2)
        part = sma13 - sma27
        return 2.0 * (part - self._sma(part, 10, 2))
    
    def alpha090(self):
        """
        (RANK(CORR(RANK(VWAP),RANK(VOLUME),5))*-1)
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        vwap_rank = vwap.rank(pct=True, method='min')
        vol_rank = self.V.rank(pct=True, method='min')
        corr = vwap_rank.rolling(window=5, min_periods=3).corr(vol_rank).fillna(method='ffill').fillna(method='bfill')
        alpha = -1 * corr.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        return alpha
    
    def alpha091(self):
        """
        ((RANK(CLOSE-MAX(CLOSE,5))*RANK(CORR(MEAN(VOLUME,40),LOW,5)))*-1)
        """
        part1 = (self.C - self.C.rolling(window=5, min_periods=5).max()).rank(pct=True)
        part2 = self.V.rolling(window=40, min_periods=40).mean().rolling(window=5, min_periods=5).corr(self.L).rank(pct=True)
        return -1 * part1 * part2
    
    def alpha092(self):
        """
        (MAX(RANK(DECAYLINEAR(DELTA(CLOSE*0.35+VWAP*0.65,2),3)),TSRANK(DECAYLINEAR(ABS(CORR((MEAN(VOLUME,180)),CLOSE,13)),5),15))*-1)
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w3 = np.arange(1, 4)
        w5 = np.arange(1, 6)
        
        weighted_price = self.C * 0.35 + vwap * 0.65
        weighted_diff = weighted_price.diff(2).fillna(0)
        part1_decay = weighted_diff.rolling(window=3, min_periods=2).apply(
            lambda x: np.dot(x, w3[:len(x)]) if len(x) >= 2 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min')
        
        vol_window = min(180, len(self.df) // 2)
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//10)).mean().fillna(method='ffill').fillna(method='bfill')
        part2_corr = vol_ma.rolling(window=13, min_periods=7).corr(self.C).fillna(method='ffill').fillna(method='bfill')
        part2_abs = abs(part2_corr)
        part2_decay = part2_abs.rolling(window=5, min_periods=3).apply(
            lambda x: np.dot(x, w5[:len(x)]) if len(x) >= 3 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = self._tsrank_fixed(part2_decay, 15)
        
        return -1 * np.maximum(part1, part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha093(self):
        """
        SUM(OPEN>=DELAY(OPEN,1)?0:MAX(OPEN-LOW,OPEN-DELAY(OPEN,1)),20)
        """
        condition = self.O.diff() >= 0.0
        alpha = np.maximum(self.O - self.L, self.O.diff())
        alpha[condition] = 0.0
        return alpha.rolling(window=20, min_periods=20).sum()
    
    def alpha094(self):
        """
        SUM((CLOSE>DELAY(CLOSE,1)?VOLUME:(CLOSE<DELAY(CLOSE,1)?-VOLUME:0)),30)
        """
        part1 = np.sign(self.C.diff()) * self.V
        return part1.rolling(window=30, min_periods=30).sum()
    
    def alpha095(self):
        """
        STD(AMOUNT,20)
        """
        return self.AMOUNT.rolling(window=20, min_periods=20).std()
    
    def alpha096(self):
        """
        SMA(SMA((CLOSE-TSMIN(LOW,9))/(TSMAX(HIGH,9)-TSMIN(LOW,9))*100,3,1),3,1)
        """
        part1 = self.C - self.C.rolling(window=9, min_periods=9).min()
        part2 = self.H.rolling(window=9, min_periods=9).max() - self.L.rolling(window=9, min_periods=9).min()
        rsv = part1 / part2 * 100
        sma1 = self._sma(rsv, 3, 1)
        return self._sma(sma1, 3, 1)
    
    def alpha097(self):
        """
        STD(VOLUME,10)
        """
        return self.V.rolling(window=10, min_periods=10).std()
    
    def alpha098(self):
        """
        (DELTA(SUM(CLOSE,100)/100,100)/DELAY(CLOSE,100)<=0.05)?(-1*(CLOSE-TSMIN(CLOSE,100))):(-1*DELTA(CLOSE,3))
        """
        condition1 = self.C.rolling(window=100, min_periods=100).mean().diff(100) / self.C.shift(100) <= 0.05
        alpha = pd.Series(index=self.df.index, dtype=float)
        alpha[condition1] = -1 * (self.C - self.C.rolling(window=100, min_periods=100).min())
        alpha[~condition1] = -1 * self.C.diff(3)
        return alpha
    
    def alpha099(self):
        """
        (-1*RANK(COVIANCE(RANK(CLOSE),RANK(VOLUME),5)))
        """
        alpha = self.C.rank(pct=True).rolling(window=5, min_periods=5).cov(self.V.rank(pct=True))
        return -1 * alpha.rank(pct=True)
    
    def alpha100(self):
        """
        STD(VOLUME,20)
        """
        return self.V.rolling(window=20, min_periods=20).std()
    
    def alpha101(self):
        """
        (RANK(CORR(CLOSE,SUM(MEAN(VOLUME,30),37),15)) < RANK(CORR(RANK(HIGH*0.1+VWAP*0.9),RANK(VOLUME),11)))*-1
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        vol_window = min(30, len(self.df) // 3)
        sum_window = min(37, len(self.df) // 3)
        corr_window = min(15, len(self.df) // 4)
        
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(5, vol_window//6)).mean().fillna(method='ffill').fillna(method='bfill')
        vol_sum = vol_ma.rolling(window=sum_window, min_periods=max(5, sum_window//6)).sum().fillna(method='ffill').fillna(method='bfill')
        part1_corr = vol_sum.rolling(window=corr_window, min_periods=max(5, corr_window//3)).corr(self.C).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_corr.rank(pct=True, method='min')
        
        weighted_price = self.H * 0.1 + vwap * 0.9
        weighted_rank = weighted_price.rank(pct=True, method='min')
        vol_rank = self.V.rank(pct=True, method='min')
        corr_window2 = min(11, len(self.df) // 4)
        part2_corr = weighted_rank.rolling(window=corr_window2, min_periods=max(4, corr_window2//3)).corr(vol_rank).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_corr.rank(pct=True, method='min')
        
        return -1 * (part2 - part1).fillna(method='ffill').fillna(method='bfill')
    
    def alpha102(self):
        """
        SMA(MAX(VOLUME-DELAY(VOLUME,1),0),6,1)/SMA(ABS(VOLUME-DELAY(VOLUME,1)),6,1)*100
        """
        diff = self.V.diff()
        part1 = np.maximum(diff, 0.0)
        part2 = abs(diff)
        sma1 = self._sma(part1, 6, 1)
        sma2 = self._sma(part2, 6, 1)
        return sma1 / sma2 * 100
    
    def alpha103(self):
        """
        ((20-LOWDAY(LOW,20))/20)*100
        """
        def lowday(x):
            return 19 - x.argmin() if len(x) == 20 else np.nan
        return (20 - self.L.rolling(window=20, min_periods=20).apply(lowday)) / 20 * 100
    
    def alpha104(self):
        """
        -1*(DELTA(CORR(HIGH,VOLUME,5),5)*RANK(STD(CLOSE,20)))
        """
        part1 = self.H.rolling(window=5, min_periods=5).corr(self.V).diff(5)
        part2 = self.C.rolling(window=20, min_periods=20).std().rank(pct=True)
        return -1 * part1 * part2
    
    def alpha105(self):
        """
        -1*CORR(RANK(OPEN),RANK(VOLUME),10)
        """
        return -1 * self.O.rank(pct=True).rolling(window=10, min_periods=10).corr(self.V.rank(pct=True))
    
    def alpha106(self):
        """
        CLOSE-DELAY(CLOSE,20)
        """
        return self.C.diff(20)
    
    def alpha107(self):
        """
        (-1*RANK(OPEN-DELAY(HIGH,1)))*RANK(OPEN-DELAY(CLOSE,1))*RANK(OPEN-DELAY(LOW,1))
        """
        part1 = -1 * (self.O - self.H.shift(1)).rank(pct=True)
        part2 = (self.O - self.C.shift(1)).rank(pct=True)
        part3 = (self.O - self.L.shift(1)).rank(pct=True)
        return part1 * part2 * part3
    
    def alpha108(self):
        """
        (RANK(HIGH-MIN(HIGH,2))^RANK(CORR(VWAP,MEAN(VOLUME,120),6)))*-1
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        high_min = self.H.rolling(window=2, min_periods=1).min()
        part1 = (self.H - high_min).rank(pct=True, method='min')
        
        vol_window = min(120, len(self.df) // 2)
        corr_window = min(6, len(self.df) // 6)
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//10)).mean().fillna(method='ffill').fillna(method='bfill')
        part2_corr = vwap.rolling(window=corr_window, min_periods=max(3, corr_window//2)).corr(vol_ma).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_corr.rank(pct=True, method='min')
        
        alpha = pd.Series(index=self.df.index, dtype=float)
        for i in range(len(self.df)):
            p1 = part1.iloc[i]
            p2 = part2.iloc[i]
            if pd.notna(p1) and pd.notna(p2):
                p1 = max(0.001, min(p1, 0.999))
                try:
                    alpha.iloc[i] = -(p1 ** p2)
                except:
                    alpha.iloc[i] = np.nan
            else:
                alpha.iloc[i] = np.nan
        
        return alpha.fillna(method='ffill').fillna(method='bfill')
    
    def alpha109(self):
        """
        SMA(HIGH-LOW,10,2)/SMA(SMA(HIGH-LOW,10,2),10,2)
        """
        hl = self.H - self.L
        sma = self._sma(hl, 10, 2)
        return sma / self._sma(sma, 10, 2)
    
    def alpha110(self):
        """
        SUM(MAX(0,HIGH-DELAY(CLOSE,1)),20)/SUM(MAX(0,DELAY(CLOSE,1)-LOW),20)*100
        """
        part1 = np.maximum(self.H - self.C.shift(1), 0.0).rolling(window=20, min_periods=20).sum()
        part2 = np.maximum(self.C.shift(1) - self.L, 0.0).rolling(window=20, min_periods=20).sum()
        return part1 / part2 * 100.0
    
    def alpha111(self):
        """
        SMA(VOL*(2*CLOSE-LOW-HIGH)/(HIGH-LOW),11,2)-SMA(VOL*(2*CLOSE-LOW-HIGH)/(HIGH-LOW),4,2)
        """
        win_vol = self.V * (2 * self.C - self.L - self.H) / (self.H - self.L)
        return self._sma(win_vol, 11, 2) - self._sma(win_vol, 4, 2)
    
    def alpha112(self):
        """
        (SUM((CLOSE-DELAY(CLOSE,1)>0?CLOSE-DELAY(CLOSE,1):0),12)-SUM((CLOSE-DELAY(CLOSE,1)<0?ABS(CLOSE-DELAY(CLOSE,1)):0),12))
        /(SUM((CLOSE-DELAY(CLOSE,1)>0?CLOSE-DELAY(CLOSE,1):0),12)+SUM((CLOSE-DELAY(CLOSE,1)<0?ABS(CLOSE-DELAY(CLOSE,1)):0),12))*100
        """
        diff = self.C.diff()
        part1 = np.maximum(diff, 0.0).rolling(window=12, min_periods=12).sum()
        part2 = abs(np.minimum(diff, 0.0)).rolling(window=12, min_periods=12).sum()
        return (part1 - part2) / (part1 + part2) * 100
    
    def alpha113(self):
        """
        -1*RANK(SUM(DELAY(CLOSE,5),20)/20)*CORR(CLOSE,VOLUME,2)*RANK(CORR(SUM(CLOSE,5),SUM(CLOSE,20),2))
        """
        self.V = self.V.replace(0, np.nan).fillna(method='ffill').fillna(method='bfill')
        
        part1_series = self.C.shift(5).rolling(window=20, min_periods=10).mean().fillna(method='ffill').fillna(method='bfill')
        part1 = part1_series.rank(pct=True, method='min')
        
        part2 = self.C.rolling(window=2, min_periods=2).corr(self.V).fillna(method='ffill').fillna(method='bfill').clip(-1, 1)
        
        sum5 = self.C.rolling(window=5, min_periods=3).sum().fillna(method='ffill').fillna(method='bfill')
        sum20 = self.C.rolling(window=20, min_periods=10).sum().fillna(method='ffill').fillna(method='bfill')
        part3_corr = sum5.rolling(window=2, min_periods=2).corr(sum20).fillna(method='ffill').fillna(method='bfill').clip(-1, 1)
        part3 = part3_corr.rank(pct=True, method='min')
        
        return -1 * part1 * part2 * part3
    
    def alpha114(self):
        """
        RANK(DELAY((HIGH-LOW)/(SUM(CLOSE,5)/5),2))*RANK(RANK(VOLUME))/((HIGH-LOW)/(SUM(CLOSE,5)/5)/(VWAP-CLOSE))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        hl = self.H - self.L
        close_ma5 = self.C.rolling(window=5, min_periods=3).mean().fillna(method='ffill').fillna(method='bfill')
        hl_ma = (hl / close_ma5).fillna(method='ffill').fillna(method='bfill')
        
        part1 = hl_ma.shift(2).rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        vol_rank1 = self.V.rank(pct=True, method='min')
        part2 = vol_rank1.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        vwap_close_diff = vwap - self.C
        threshold = 0.0001
        mask_small = abs(vwap_close_diff) < threshold
        vwap_close_diff[mask_small] = threshold * np.sign(vwap_close_diff[mask_small])
        vwap_close_diff = vwap_close_diff.replace(0, threshold)
        part3 = (hl_ma / vwap_close_diff).fillna(method='ffill').fillna(method='bfill')
        part3 = part3.clip(lower=part3.quantile(0.01), upper=part3.quantile(0.99))
        
        alpha = (part1 * part2 / part3).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha115(self):
        """
        (RANK(CORR(HIGH*0.9+CLOSE*0.1,MEAN(VOLUME,30),10))^RANK(CORR(TSRANK((HIGH+LOW)/2,4),TSRANK(VOLUME,10),7)))
        """
        part1 = (self.H * 0.9 + self.C * 0.1).rolling(window=10, min_periods=10).corr(
            self.V.rolling(window=30, min_periods=30).mean()
        ).rank(pct=True)
        part2 = self._tsrank((self.H + self.L) / 2, 4)
        part2 = part2.rolling(window=7, min_periods=7).corr(self._tsrank(self.V, 10)).rank(pct=True)
        return part1 ** part2
    
    def alpha116(self):
        """
        REGBETA(CLOSE,SEQUENCE,20)
        """
        result = pd.Series(index=self.df.index, dtype=float)
        for i in range(20, len(self.df)):
            y = self.C.iloc[i-20:i]
            x = np.arange(1, 21)
            result.iloc[i] = self._regbeta(y, x)
        return result.fillna(0)
    
    def alpha117(self):
        """
        TSRANK(VOLUME,32)*(1-TSRANK(CLOSE+HIGH-LOW,16))*(1-TSRANK(RET,32))
        """
        part1 = self._tsrank(self.V, 32)
        part2 = 1.0 - self._tsrank(self.C + self.H - self.L, 16)
        part3 = 1.0 - self._tsrank(self.C.pct_change(), 32)
        return part1 * part2 * part3
    
    def alpha118(self):
        """
        SUM(HIGH-OPEN,20)/SUM(OPEN-LOW,20)*100
        """
        part1 = (self.H - self.O).rolling(window=20, min_periods=20).sum()
        part2 = (self.O - self.L).rolling(window=20, min_periods=20).sum()
        return part1 / part2 * 100.0
    
    def alpha119(self):
        """
        RANK(DECAYLINEAR(CORR(VWAP,SUM(MEAN(VOLUME,5),26),5),7))-RANK(DECAYLINEAR(TSRANK(MIN(CORR(RANK(OPEN),RANK(MEAN(VOLUME,15)),21),9),7),8))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w7 = np.arange(1, 8)
        w8 = np.arange(1, 9)
        
        vol_ma5 = self.V.rolling(window=5, min_periods=3).mean().fillna(method='ffill').fillna(method='bfill')
        sum_window = min(26, len(self.df) // 3)
        corr_window1 = min(5, len(self.df) // 10)
        decay_window1 = min(7, len(self.df) // 10)
        
        vol_sum = vol_ma5.rolling(window=sum_window, min_periods=max(5, sum_window//5)).sum().fillna(method='ffill').fillna(method='bfill')
        part1_corr = vol_sum.rolling(window=corr_window1, min_periods=max(3, corr_window1//2)).corr(vwap).fillna(method='ffill').fillna(method='bfill')
        part1_decay = part1_corr.rolling(window=decay_window1, min_periods=max(3, decay_window1//2)).apply(
            lambda x: np.dot(x, w7[:len(x)]) if len(x) >= 3 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min')
        
        vol_window = min(15, len(self.df) // 3)
        corr_window2 = min(21, len(self.df) // 3)
        min_window = min(9, len(self.df) // 5)
        decay_window2 = min(8, len(self.df) // 5)
        
        vol_ma15 = self.V.rolling(window=vol_window, min_periods=max(5, vol_window//3)).mean().fillna(method='ffill').fillna(method='bfill')
        vol_ma15_rank = vol_ma15.rank(pct=True, method='min')
        open_rank = self.O.rank(pct=True, method='min')
        part2_corr = vol_ma15_rank.rolling(window=corr_window2, min_periods=max(5, corr_window2//4)).corr(open_rank).fillna(method='ffill').fillna(method='bfill')
        part2_min = part2_corr.rolling(window=min_window, min_periods=max(3, min_window//3)).min().fillna(method='ffill').fillna(method='bfill')
        part2_tsrank = self._tsrank_fixed(part2_min, 7)
        part2_decay = part2_tsrank.rolling(window=decay_window2, min_periods=max(3, decay_window2//2)).apply(
            lambda x: np.dot(x, w8[:len(x)]) if len(x) >= 3 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min')
        
        return (part1 - part2).fillna(method='ffill').fillna(method='bfill')
    
    def alpha120(self):
        """
        RANK(VWAP-CLOSE)/RANK(VWAP+CLOSE)
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        denominator = vwap + self.C
        denominator = denominator.replace(0, 1e-10)
        alpha = ((vwap - self.C) / denominator).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha121(self):
        """
        (RANK(VWAP-MIN(VWAP,12))^TSRANK(CORR(TSRANK(VWAP,20),TSRANK(MEAN(VOLUME,60),2),18),3))*-1
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        vwap_min = vwap.rolling(window=12, min_periods=6).min().fillna(method='ffill').fillna(method='bfill')
        part1 = (vwap - vwap_min).rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill').clip(0.001, 0.999)
        
        vol_window = min(60, len(self.df) // 2)
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//6)).mean().fillna(method='ffill').fillna(method='bfill')
        tsrank_vwap = self._tsrank_fixed(vwap, 20)
        tsrank_vol = self._tsrank_fixed(vol_ma, 2)
        corr_window = min(18, len(self.df) // 3)
        part2_corr = tsrank_vwap.rolling(window=corr_window, min_periods=max(5, corr_window//3)).corr(tsrank_vol).fillna(method='ffill').fillna(method='bfill')
        part2 = self._tsrank_fixed(part2_corr, 3).fillna(method='ffill').fillna(method='bfill').clip(0.001, 0.999)
        
        alpha = pd.Series(index=self.df.index, dtype=float)
        for i in range(len(self.df)):
            p1 = part1.iloc[i]
            p2 = part2.iloc[i]
            if pd.notna(p1) and pd.notna(p2):
                try:
                    alpha.iloc[i] = -(p1 ** p2)
                except:
                    alpha.iloc[i] = np.nan
            else:
                alpha.iloc[i] = np.nan
        
        return alpha.fillna(method='ffill').fillna(method='bfill')
    
    def alpha122(self):
        """
        (SMA(SMA(SMA(LOG(CLOSE),13,2),13,2),13,2)-DELAY(SMA(SMA(SMA(LOG(CLOSE),13,2),13,2),13,2),1))/DELAY(SMA(SMA(SMA(LOG(CLOSE),13,2),13,2),13,2),1)
        """
        part1 = np.log(self.C)
        part1 = self._sma(part1, 13, 2)
        part1 = self._sma(part1, 13, 2)
        part1 = self._sma(part1, 13, 2)
        return part1.pct_change()
    
    def alpha123(self):
        """
        (RANK(CORR(SUM((HIGH+LOW)/2,20),SUM(MEAN(VOLUME,60),20),9)) < RANK(CORR(LOW,VOLUME,6)))*-1
        """
        part1 = (self.H * 0.5 + self.L * 0.5).rolling(window=20, min_periods=20).sum()
        part1 = self.V.rolling(window=60, min_periods=60).mean().rolling(window=20, min_periods=20).sum().rolling(window=9, min_periods=9).corr(part1).rank(pct=True)
        part2 = self.L.rolling(window=6, min_periods=6).corr(self.V).rank(pct=True)
        return -1 * (part2 - part1)
    
    def alpha124(self):
        """
        (CLOSE-VWAP)/DECAYLINEAR(RANK(TSMAX(CLOSE,30)),2)
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        
        part1 = self.C - vwap
        close_max = self.C.rolling(window=30, min_periods=15).max().fillna(method='ffill').fillna(method='bfill')
        part2_rank = close_max.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        w2 = np.arange(1, 3)
        part2 = part2_rank.rolling(window=2, min_periods=1).apply(
            lambda x: np.dot(x, w2[:len(x)]) if len(x) >= 1 else np.nan
        ).fillna(method='ffill').fillna(method='bfill').replace(0, 1e-10)
        
        alpha = (part1 / part2).fillna(method='ffill').fillna(method='bfill')
        alpha = alpha.clip(lower=alpha.quantile(0.01), upper=alpha.quantile(0.99))
        return alpha
    
    def alpha125(self):
        """
        RANK(DECAYLINEAR(CORR(VWAP,MEAN(VOLUME,80),17),20))/RANK(DECAYLINEAR(DELTA(CLOSE*0.5+VWAP*0.5,3),16))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w20 = np.arange(1, 21)
        w16 = np.arange(1, 17)
        
        vol_window = min(80, len(self.df) // 2)
        corr_window = min(17, len(self.df) // 3)
        decay_window1 = min(20, len(self.df) // 3)
        
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//8)).mean().fillna(method='ffill').fillna(method='bfill')
        part1_corr = vol_ma.rolling(window=corr_window, min_periods=max(5, corr_window//3)).corr(vwap).fillna(method='ffill').fillna(method='bfill')
        part1_decay = part1_corr.rolling(window=decay_window1, min_periods=max(5, decay_window1//4)).apply(
            lambda x: np.dot(x, w20[:len(x)]) if len(x) >= 5 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        decay_window2 = min(16, len(self.df) // 3)
        weighted_price = self.C * 0.5 + vwap * 0.5
        part2_diff = weighted_price.diff(3).fillna(0)
        part2_decay = part2_diff.rolling(window=decay_window2, min_periods=max(5, decay_window2//3)).apply(
            lambda x: np.dot(x, w16[:len(x)]) if len(x) >= 5 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill').replace(0, 1e-10)
        
        alpha = (part1 / part2).fillna(method='ffill').fillna(method='bfill')
        alpha = alpha.clip(lower=alpha.quantile(0.01), upper=alpha.quantile(0.99))
        return alpha
    
    def alpha126(self):
        """
        (CLOSE+HIGH+LOW)/3
        """
        return (self.C + self.H + self.L) / 3.0
    
    def alpha127(self):
        """
        MEAN((100*(CLOSE-MAX(CLOSE,12))/MAX(CLOSE,12))^2)^(1/2)
        """
        close_max = self.C.rolling(window=12, min_periods=12).max()
        alpha = (self.C - close_max) / close_max * 100
        return (alpha ** 2).rolling(window=12, min_periods=12).mean() ** 0.5
    
    def alpha128(self):
        """
        100-(100/(1+SUM(((HIGH+LOW+CLOSE)/3>DELAY((HIGH+LOW+CLOSE)/3,1)?(HIGH+LOW+CLOSE)/3*VOLUME:0),14)/
        SUM(((HIGH+LOW+CLOSE)/3<DELAY((HIGH+LOW+CLOSE)/3,1)?(HIGH+LOW+CLOSE)/3*VOLUME:0),14)))
        """
        tp = (self.H + self.L + self.C) / 3.0
        condition1 = tp.diff() > 0.0
        condition2 = tp.diff() < 0.0
        
        part1 = tp * self.V
        part1[~condition1] = 0.0
        part1 = part1.rolling(window=14, min_periods=14).sum()
        
        part2 = tp * self.V
        part2[~condition2] = 0.0
        part2 = part2.rolling(window=14, min_periods=14).sum()
        
        return 100.0 - 100.0 / (1 + part1 / part2)
    
    def alpha129(self):
        """
        SUM((CLOSE-DELAY(CLOSE,1)<0?ABS(CLOSE-DELAY(CLOSE,1)):0),12)
        """
        return abs(np.minimum(self.C.diff(), 0.0)).rolling(window=12, min_periods=12).sum()
    
    def alpha130(self):
        """
        (RANK(DECAYLINEAR(CORR((HIGH+LOW)/2,MEAN(VOLUME,40),9),10))/RANK(DECAYLINEAR(CORR(RANK(VWAP),RANK(VOLUME),7),3)))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w10 = np.arange(1, 11)
        w3 = np.arange(1, 4)
        
        vol_window = min(40, len(self.df) // 2)
        corr_window1 = min(9, len(self.df) // 4)
        decay_window1 = min(10, len(self.df) // 4)
        
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//4)).mean().fillna(method='ffill').fillna(method='bfill')
        hl_avg = self.H * 0.5 + self.L * 0.5
        part1_corr = vol_ma.rolling(window=corr_window1, min_periods=max(5, corr_window1//2)).corr(hl_avg).fillna(method='ffill').fillna(method='bfill')
        part1_decay = part1_corr.rolling(window=decay_window1, min_periods=max(5, decay_window1//2)).apply(
            lambda x: np.dot(x, w10[:len(x)]) if len(x) >= 5 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        corr_window2 = min(7, len(self.df) // 5)
        decay_window2 = min(3, len(self.df) // 10)
        vwap_rank = vwap.rank(pct=True, method='min')
        vol_rank = self.V.rank(pct=True, method='min')
        part2_corr = vwap_rank.rolling(window=corr_window2, min_periods=max(4, corr_window2//2)).corr(vol_rank).fillna(method='ffill').fillna(method='bfill')
        part2_decay = part2_corr.rolling(window=decay_window2, min_periods=2).apply(
            lambda x: np.dot(x, w3[:len(x)]) if len(x) >= 2 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill').replace(0, 1e-10)
        
        alpha = (part1 / part2).fillna(method='ffill').fillna(method='bfill')
        alpha = alpha.clip(lower=alpha.quantile(0.01), upper=alpha.quantile(0.99))
        return alpha
    
    def alpha131(self):
        """
        (RANK(DELTA(VWAP,1))^TSRANK(CORR(CLOSE,MEAN(VOLUME,50),18),18))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        vwap_diff = vwap.diff().fillna(0)
        part1 = vwap_diff.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill').clip(0.001, 0.999)
        
        vol_window = min(50, len(self.df) // 2)
        corr_window = min(18, len(self.df) // 3)
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//5)).mean().fillna(method='ffill').fillna(method='bfill')
        part2_corr = vol_ma.rolling(window=corr_window, min_periods=max(5, corr_window//3)).corr(self.C).fillna(method='ffill').fillna(method='bfill')
        part2 = self._tsrank_fixed(part2_corr, 18).fillna(method='ffill').fillna(method='bfill').clip(0.001, 0.999)
        
        alpha = np.exp(np.log(part1 + 1e-10) * part2)
        alpha = alpha.fillna(method='ffill').fillna(method='bfill').clip(0, 100)
        return alpha
    
    def alpha132(self):
        """
        MEAN(AMOUNT,20)
        """
        return self.AMOUNT.rolling(window=20, min_periods=20).mean()
    
    def alpha133(self):
        """
        ((20-HIGHDAY(HIGH,20))/20)*100-((20-LOWDAY(LOW,20))/20)*100
        """
        def highday(x):
            return 19 - x.argmax() if len(x) == 20 else np.nan
        def lowday(x):
            return 19 - x.argmin() if len(x) == 20 else np.nan
        
        part1 = (20 - self.H.rolling(window=20, min_periods=20).apply(highday)) / 20 * 100
        part2 = (20 - self.L.rolling(window=20, min_periods=20).apply(lowday)) / 20 * 100
        return part1 - part2
    
    def alpha134(self):
        """
        (CLOSE-DELAY(CLOSE,12))/DELAY(CLOSE,12)*VOLUME
        """
        return self.C.pct_change(periods=12) * self.V
    
    def alpha135(self):
        """
        SMA(DELAY(CLOSE/DELAY(CLOSE,20),1),20,1)
        """
        alpha = (self.C / self.C.shift(20)).shift(1)
        return self._sma(alpha, 20, 1)
    
    def alpha136(self):
        """
        -1*RANK(DELTA(RET,3))*CORR(OPEN,VOLUME,10)
        """
        ret = self.C.pct_change()
        part1 = ret.diff(3).rank(pct=True)
        part2 = self.O.rolling(window=10, min_periods=10).corr(self.V)
        return -1 * part1 * part2
    
    def alpha137(self):
        """
        16*(CLOSE+(CLOSE-OPEN)/2-DELAY(OPEN,1))/
        ((ABS(HIGH-DELAY(CLOSE,1))>ABS(LOW-DELAY(CLOSE,1))&ABS(HIGH-DELAY(CLOSE,1))>ABS(HIGH-DELAY(LOW,1))?ABS(HIGH-DELAY(CLOSE,1))+ABS(LOW-DELAY(CLOSE,1))/2+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4:
        (ABS(LOW-DELAY(CLOSE,1))>ABS(HIGH-DELAY(LOW,1)) & ABS(LOW-DELAY(CLOSE,1))>ABS(HIGH-DELAY(CLOSE,1))?ABS(LOW-DELAY(CLOSE,1))+ABS(HIGH-DELAY(CLOSE,1))/2+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4:ABS(HIGH-DELAY(LOW,1))+ABS(DELAY(CLOSE,1)-DELAY(OPEN,1))/4)))
        *MAX(ABS(HIGH-DELAY(CLOSE,1)),ABS(LOW-DELAY(CLOSE,1)))
        """
        part1 = self.C * 1.5 - self.O * 0.5 - self.O.shift(1)
        part2 = abs(self.H - self.C.shift(1)) + abs(self.L - self.C.shift(1)) / 2.0 + abs(self.C - self.O).shift(1) / 4.0
        
        condition1 = np.logical_and(
            abs(self.H - self.C.shift(1)) > abs(self.L - self.C.shift(1)),
            abs(self.H - self.C.shift(1)) > abs(self.H - self.L.shift(1))
        )
        condition2 = np.logical_and(
            abs(self.L - self.C.shift(1)) > abs(self.H - self.L.shift(1)),
            abs(self.L - self.C.shift(1)) > abs(self.H - self.C.shift(1))
        )
        
        part2[~condition1 & condition2] = abs(self.L - self.C.shift(1)) + abs(self.H - self.C.shift(1)) / 2.0 + abs(self.C - self.O).shift(1) / 4.0
        part2[~condition1 & ~condition2] = abs(self.H - self.L.shift(1)) + abs(self.C - self.O).shift(1) / 4.0
        
        part3 = np.maximum(abs(self.H - self.C.shift(1)), abs(self.L - self.C.shift(1)))
        alpha = part1 / part2 * part3 * 16.0
        return alpha
    
    def alpha138(self):
        """
        ((RANK(DECAYLINEAR(DELTA(LOW*0.7+VWAP*0.3,3),20))
        -TSRANK(DECAYLINEAR(TSRANK(
            CORR(TSRANK(LOW,8),TSRANK(MEAN(VOLUME,60),17),5)
            ,19),16),7))* -1)
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w20 = np.arange(1, 21)
        w16 = np.arange(1, 17)
        
        decay_window1 = min(20, len(self.df) // 3)
        weighted_price = self.L * 0.7 + vwap * 0.3
        part1_diff = weighted_price.diff(3).fillna(0)
        part1_decay = part1_diff.rolling(window=decay_window1, min_periods=max(5, decay_window1//4)).apply(
            lambda x: np.dot(x, w20[:len(x)]) if len(x) >= 5 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        vol_window = min(60, len(self.df) // 2)
        tsrank_window1 = min(17, len(self.df) // 3)
        corr_window = min(5, len(self.df) // 6)
        tsrank_window2 = min(19, len(self.df) // 3)
        decay_window2 = min(16, len(self.df) // 3)
        tsrank_window3 = min(7, len(self.df) // 5)
        
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//6)).mean().fillna(method='ffill').fillna(method='bfill')
        tsrank_vol = self._tsrank_fixed(vol_ma, tsrank_window1).fillna(method='ffill').fillna(method='bfill')
        tsrank_low = self._tsrank_fixed(self.L, 8).fillna(method='ffill').fillna(method='bfill')
        part2_corr = tsrank_low.rolling(window=corr_window, min_periods=max(3, corr_window//2)).corr(tsrank_vol).fillna(method='ffill').fillna(method='bfill')
        part2_tsrank = self._tsrank_fixed(part2_corr, tsrank_window2).fillna(method='ffill').fillna(method='bfill')
        part2_decay = part2_tsrank.rolling(window=decay_window2, min_periods=max(5, decay_window2//3)).apply(
            lambda x: np.dot(x, w16[:len(x)]) if len(x) >= 5 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = self._tsrank_fixed(part2_decay, tsrank_window3).fillna(method='ffill').fillna(method='bfill')
        
        alpha = -1 * (part1 - part2).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha139(self):
        """
        (-1*CORR(OPEN,VOLUME,10))
        """
        return -1 * self.O.rolling(window=10, min_periods=10).corr(self.V)
    
    def alpha140(self):
        """
        MIN(RANK(DECAYLINEAR(RANK(OPEN)+RANK(LOW)-RANK(HIGH)-RANK(CLOSE),8)),TSRANK(DECAYLINEAR(CORR(TSRANK(CLOSE,8),TSRANK(MEAN(VOLUME,60),20),8),7),3))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        w8 = np.arange(1, 9)
        w7 = np.arange(1, 8)
        
        decay_window1 = min(8, len(self.df) // 4)
        open_rank = self.O.rank(pct=True, method='min')
        low_rank = self.L.rank(pct=True, method='min')
        high_rank = self.H.rank(pct=True, method='min')
        close_rank = self.C.rank(pct=True, method='min')
        
        part1_series = open_rank + low_rank - high_rank - close_rank
        part1_series = part1_series.fillna(method='ffill').fillna(method='bfill')
        part1_decay = part1_series.rolling(window=decay_window1, min_periods=max(4, decay_window1//2)).apply(
            lambda x: np.dot(x, w8[:len(x)]) if len(x) >= 4 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        vol_window = min(60, len(self.df) // 2)
        tsrank_window1 = min(20, len(self.df) // 3)
        corr_window = min(8, len(self.df) // 4)
        decay_window2 = min(7, len(self.df) // 5)
        tsrank_window2 = min(3, len(self.df) // 10)
        
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//6)).mean().fillna(method='ffill').fillna(method='bfill')
        tsrank_vol = self._tsrank_fixed(vol_ma, tsrank_window1).fillna(method='ffill').fillna(method='bfill')
        tsrank_close = self._tsrank_fixed(self.C, 8).fillna(method='ffill').fillna(method='bfill')
        part2_corr = tsrank_close.rolling(window=corr_window, min_periods=max(4, corr_window//2)).corr(tsrank_vol).fillna(method='ffill').fillna(method='bfill')
        part2_decay = part2_corr.rolling(window=decay_window2, min_periods=max(3, decay_window2//2)).apply(
            lambda x: np.dot(x, w7[:len(x)]) if len(x) >= 3 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = self._tsrank_fixed(part2_decay, tsrank_window2).fillna(method='ffill').fillna(method='bfill')
        
        alpha = np.minimum(part1, part2).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha141(self):
        """
        (RANK(CORR(RANK(HIGH),RANK(MEAN(VOLUME,15)),9))*-1)
        """
        alpha = self.V.rolling(window=15, min_periods=15).mean().rank(pct=True)
        alpha = alpha.rolling(window=9, min_periods=9).corr(self.H.rank(pct=True)).rank(pct=True)
        return -1 * alpha
    
    def alpha142(self):
        """
        -1*RANK(TSRANK(CLOSE,10))*RANK(DELTA(DELTA(CLOSE,1),1))*RANK(TSRANK(VOLUME/MEAN(VOLUME,20),5))
        """
        part1 = self._tsrank(self.C, 10).rank(pct=True)
        part2 = self.C.diff().diff().rank(pct=True)
        part3 = self._tsrank(self.V / self.V.rolling(window=20, min_periods=20).mean(), 5).rank(pct=True)
        return -1 * part1 * part2 * part3
    
    def alpha143(self):
        """
        CLOSE>DELAY(CLOSE,1)?(CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1)*SELF:SELF
        """
        condition = self.C > self.C.shift(1)
        alpha = self.C.pct_change()
        alpha[~condition] = alpha.shift(1)[~condition]
        return alpha
    
    def alpha144(self):
        """
        SUMIF(ABS(CLOSE/DELAY(CLOSE,1)-1)/AMOUNT,20,CLOSE<DELAY(CLOSE,1))/COUNT(CLOSE<DELAY(CLOSE,1),20)
        """
        part1 = abs(self.C.pct_change()) / self.AMOUNT
        part1[self.C.diff() >= 0] = 0.0
        part1 = part1.rolling(window=20, min_periods=20).sum()
        part2 = (self.C.diff() < 0.0).rolling(window=20, min_periods=20).sum()
        return part1 / part2
    
    def alpha145(self):
        """
        (MEAN(VOLUME,9)-MEAN(VOLUME,26))/MEAN(VOLUME,12)*100
        """
        ma9 = self.V.rolling(window=9, min_periods=9).mean()
        ma26 = self.V.rolling(window=26, min_periods=26).mean()
        ma12 = self.V.rolling(window=12, min_periods=12).mean()
        return (ma9 - ma26) / ma12 * 100.0
    
    def alpha146(self):
        """
        MEAN(RET-SMA(RET,61,2),20)*(RET-SMA(RET,61,2))/SMA(SMA(RET,61,2)^2,60)
        """
        ret = self.C.pct_change()
        sma = self._sma(ret, 61, 2)
        ret_excess = ret - sma
        part1 = ret_excess.rolling(window=20, min_periods=20).mean() * ret_excess
        part2 = self._sma(sma ** 2, 60, 1)
        return part1 / part2
    
    def alpha147(self):
        """
        REGBETA(MEAN(CLOSE,12),SEQUENCE(12))
        """
        ma_price = self.C.rolling(window=12, min_periods=12).mean()
        result = pd.Series(index=self.df.index, dtype=float)
        for i in range(12, len(self.df)):
            y = ma_price.iloc[i-12:i]
            x = np.arange(1, 13)
            result.iloc[i] = self._regbeta(y, x)
        return result.fillna(0)
    
    def alpha148(self):
        """
        (RANK(CORR(OPEN,SUM(MEAN(VOLUME,60),9),6))<RANK(OPEN-TSMIN(OPEN,14)))*-1
        """
        part1 = self.V.rolling(window=60, min_periods=60).mean().rolling(window=9, min_periods=9).sum()
        part1 = part1.rolling(window=6, min_periods=6).corr(self.O).rank(pct=True)
        part2 = (self.O - self.O.rolling(window=14, min_periods=14).min()).rank(pct=True)
        return -1 * (part2 - part1)
    
    def alpha149(self):
        """
        REGBETA(FILTER(RET,BANCHMARK_INDEX_CLOSE<DELAY(BANCHMARK_INDEX_CLOSE,1)),
        FILTER(BANCHMARK_INDEX_CLOSE/DELAY(BANCHMARK_INDEX_CLOSE,1)-1,BANCHMARK_INDEX_CLOSE<DELAY(BANCHMARK_INDEX_CLOSE,1)),252)
        调整窗口期以适应数据量
        """
        n_rows = len(self.df)
        if n_rows < 252:
            window = max(60, n_rows // 2)
        else:
            window = 252
        
        if hasattr(self, 'index_df') and self.index_df is not None:
            index_data = self.index_df.copy()
            if 'close' in index_data.columns:
                index_close = index_data['close']
            elif 'closePrice' in index_data.columns:
                index_close = index_data['closePrice']
            else:
                index_close = index_data.iloc[:, 0]
            
            if 'date' in self.df.columns and 'date' in index_data.columns:
                self.df['date'] = pd.to_datetime(self.df['date'])
                index_data['date'] = pd.to_datetime(index_data['date'])
                date_to_index = dict(zip(index_data['date'], index_close))
                bm_close = self.df['date'].map(date_to_index).fillna(method='ffill').fillna(method='bfill')
            else:
                bm_close = index_close.reindex(self.df.index, method='ffill')
        else:
            bm_close = self.C.rolling(window=20, min_periods=5).mean()
        
        bm_ret = bm_close.pct_change().fillna(0)
        bm_down = bm_ret < 0.0
        stock_ret = self.C.pct_change().fillna(0)
        
        result = pd.Series(index=self.df.index, dtype=float)
        if n_rows < window:
            return pd.Series(0, index=self.df.index)
        
        for i in range(window, n_rows):
            start_idx = i - window
            bm_down_window = bm_down.iloc[start_idx:i]
            valid_indices = bm_down_window[bm_down_window].index
            if len(valid_indices) < 5:
                result.iloc[i] = np.nan
                continue
            y = stock_ret.loc[valid_indices]
            x = bm_ret.loc[valid_indices]
            valid_mask = ~(y.isna() | x.isna())
            y_clean = y[valid_mask]
            x_clean = x[valid_mask]
            if len(y_clean) > 3:
                try:
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x_clean, y_clean)
                    result.iloc[i] = slope
                except:
                    result.iloc[i] = np.nan
            else:
                result.iloc[i] = np.nan
        
        result = result.fillna(method='ffill').fillna(method='bfill').fillna(0)
        return result
    
    def alpha150(self):
        """
        (CLOSE+HIGH+LOW)/3*VOLUME
        """
        return (self.C + self.H + self.L) / 3.0 * self.V
    
    def alpha151(self):
        """
        SMA(CLOSE-DELAY(CLOSE,20),20,1)
        """
        return self._sma(self.C.diff(20), 20, 1)
    
    def alpha152(self):
        """
        A=DELAY(SMA(DELAY(CLOSE/DELAY(CLOSE,9),1),9,1),1)
        SMA(MEAN(A,12)-MEAN(A,26),9,1)
        """
        a = (self.C / self.C.shift(9)).shift(1)
        a = self._sma(a, 9, 1).shift(1)
        alpha = (a.rolling(window=12, min_periods=12).mean() - a.rolling(window=26, min_periods=26).mean())
        alpha = self._sma(alpha, 9, 1)
        return alpha
    
    def alpha153(self):
        """
        (MEAN(CLOSE,3)+MEAN(CLOSE,6)+MEAN(CLOSE,12)+MEAN(CLOSE,24))/4
        """
        ma3 = self.C.rolling(window=3, min_periods=3).mean()
        ma6 = self.C.rolling(window=6, min_periods=6).mean()
        ma12 = self.C.rolling(window=12, min_periods=12).mean()
        ma24 = self.C.rolling(window=24, min_periods=24).mean()
        return (ma3 + ma6 + ma12 + ma24) / 4
    
    def alpha154(self):
        """
        VWAP-MIN(VWAP,16)<CORR(VWAP,MEAN(VOLUME,180),18)
        """
        n_rows = len(self.df)
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        vwap_min = vwap.rolling(window=16, min_periods=8).min().fillna(method='ffill').fillna(method='bfill')
        part1 = vwap - vwap_min
        
        if n_rows < 180:
            vol_window = max(60, n_rows // 2)
            corr_window = max(10, min(18, n_rows // 5))
        else:
            vol_window = 180
            corr_window = 18
        
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(10, vol_window//10)).mean().fillna(method='ffill').fillna(method='bfill')
        part2_corr = vol_ma.rolling(window=corr_window, min_periods=max(5, corr_window//3)).corr(vwap).fillna(method='ffill').fillna(method='bfill')
        
        alpha = (part2_corr - part1).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha155(self):
        """
        SMA(VOLUME,13,2)-SMA(VOLUME,27,2)-SMA(SMA(VOLUME,13,2)-SMA(VOLUME,27,2),10,2)
        """
        sma13 = self._sma(self.V, 13, 2)
        sma27 = self._sma(self.V, 27, 2)
        diff = sma13 - sma27
        return sma13 - sma27 - self._sma(diff, 10, 2)
    
    def alpha156(self):
        """
        MAX(RANK(DECAYLINEAR(DELTA(VWAP,5),3)),RANK(DECAYLINEAR((DELTA(OPEN*0.15+LOW*0.85,2)/(OPEN*0.15+LOW*0.85)) * -1,3))) * -1
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        
        w3 = np.arange(1, 4)
        den = self.O * 0.15 + self.L * 0.85
        
        vwap_diff = vwap.diff(5).fillna(0)
        part1_decay = vwap_diff.rolling(window=3, min_periods=2).apply(
            lambda x: np.dot(x, w3[:len(x)]) if len(x) >= 2 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_decay.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        den = den.replace(0, 1e-10)
        den_diff = den.diff(2).fillna(0)
        den_ratio = (den_diff / den) * (-1)
        den_ratio = den_ratio.replace([np.inf, -np.inf], np.nan).fillna(method='ffill').fillna(method='bfill').clip(-100, 100)
        part2_decay = den_ratio.rolling(window=3, min_periods=2).apply(
            lambda x: np.dot(x, w3[:len(x)]) if len(x) >= 2 else np.nan
        ).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_decay.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        alpha = -1 * np.maximum(part1, part2).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha157(self):
        """
        MIN(PROD(RANK(LOG(SUM(TSMIN(RANK(-1*RANK(DELTA(CLOSE-1,5))),2),1))),1),5)+TSRANK(DELAY(-1*RET,6),5)
        """
        part1 = (self.C - 1.0).diff(5).rank(pct=True) * (-1)
        part1 = part1.rank(pct=True).rolling(window=2, min_periods=2).min()
        part1 = np.log(part1.rolling(window=1, min_periods=1).sum()).rank(pct=True)
        part1 = part1.rolling(window=5, min_periods=5).min()
        
        part2 = self._tsrank((-1 * self.C.pct_change()).shift(6), 5)
        
        return part1 + part2
    
    def alpha158(self):
        """
        (HIGH-LOW)/CLOSE
        """
        return (self.H - self.L) / self.C
    
    def alpha159(self):
        """
        ((CLOSE-SUM(MIN(LOW,DELAY(CLOSE,1)),6))/SUM(MAX(HIGH,DELAY(CLOSE,1))-MIN(LOW,DELAY(CLOSE,1)),6)*12*24
        +(CLOSE-SUM(MIN(LOW,DELAY(CLOSE,1)),12))/SUM(MAX(HIGH,DELAY(CLOSE,1))-MIN(LOW,DELAY(CLOSE,1)),12)*6*24
        +(CLOSE-SUM(MIN(LOW,DELAY(CLOSE,1)),24))/SUM(MAX(HIGH,DELAY(CLOSE,1))-MIN(LOW,DELAY(CLOSE,1)),24)*6*12)*100/(6*12+6*24+12*24)
        """
        min_low_close = np.minimum(self.L, self.C.shift(1))
        max_high_close = np.maximum(self.H, self.C.shift(1))
        diff = max_high_close - min_low_close
        
        part1 = (self.C - min_low_close.rolling(window=6, min_periods=6).sum()) / diff.rolling(window=6, min_periods=6).sum() * 12 * 24
        part2 = (self.C - min_low_close.rolling(window=12, min_periods=12).sum()) / diff.rolling(window=12, min_periods=12).sum() * 6 * 24
        part3 = (self.C - min_low_close.rolling(window=24, min_periods=24).sum()) / diff.rolling(window=24, min_periods=24).sum() * 6 * 12
        
        return (part1 + part2 + part3) * 100.0 / (12 * 6 + 6 * 24 + 12 * 24)
    
    def alpha160(self):
        """
        SMA((CLOSE<=DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1)
        """
        part1 = self.C.rolling(window=20, min_periods=20).std()
        part1[self.C.diff() > 0] = 0.0
        return self._sma(part1, 20, 1)
    
    def alpha161(self):
        """
        MEAN(MAX(MAX(HIGH-LOW,ABS(DELAY(CLOSE,1)-HIGH)),ABS(DELAY(CLOSE,1)-LOW)),12)
        """
        part1 = np.maximum(self.H - self.L, abs(self.C.shift(1) - self.H))
        part1 = np.maximum(part1, abs(self.C.shift(1) - self.L))
        return part1.rolling(window=12, min_periods=12).mean()
    
    def alpha162(self):
        """
        (SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100
        -MIN(SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100,12))
        /(MAX(SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100,12)
        -MIN(SMA(MAX(CLOSE-DELAY(CLOSE,1),0),12,1)/SMA(ABS(CLOSE-DELAY(CLOSE,1)),12,1)*100,12))
        """
        diff = self.C.diff()
        den = np.maximum(diff, 0.0).ewm(adjust=False, alpha=1/12, min_periods=0).mean() / abs(diff).ewm(adjust=False, alpha=1/12, min_periods=0).mean() * 100.0
        
        alpha = (den - den.rolling(window=12, min_periods=12).min()) / (den.rolling(window=12, min_periods=12).max() - den.rolling(window=12, min_periods=12).min())
        return alpha
    
    def alpha163(self):
        """
        RANK((-1*RET)*MEAN(VOLUME,20)*VWAP*(HIGH-CLOSE))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        ret = self.C.pct_change().fillna(0)
        vol_ma = self.V.rolling(window=20, min_periods=10).mean().fillna(method='ffill').fillna(method='bfill')
        high_minus_close = self.H - self.C
        
        alpha = (-1 * ret) * vol_ma * vwap * high_minus_close
        alpha = alpha.fillna(method='ffill').fillna(method='bfill')
        alpha_rank = alpha.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        return alpha_rank
    
    def alpha164(self):
        """
        SMA(((CLOSE>DELAY(CLOSE,1)?1/(CLOSE-DELAY(CLOSE,1)):1)-MIN(CLOSE>DELAY(CLOSE,1)?1/(CLOSE-DELAY(CLOSE,1)):1,12))/(HIGH-LOW)*100,13,2)
        """
        diff = self.C.diff()
        part1 = 1.0 / diff
        part1[diff <= 0] = 1.0
        part2 = part1.rolling(window=12, min_periods=12).min()
        alpha = (part1 - part2) / (self.H - self.L) * 100.0
        return self._sma(alpha, 13, 2)
    
    def alpha165(self):
        """
        MAX(SUMAC(CLOSE-MEAN(CLOSE,48)))-MIN(SUMAC(CLOSE-MEAN(CLOSE,48)))/STD(CLOSE,48)
        """
        part = self.C - self.C.rolling(window=48, min_periods=48).mean()
        part = part.rolling(window=48, min_periods=48).sum()
        
        part1 = part.rolling(window=48, min_periods=48).max()
        part2 = part.rolling(window=48, min_periods=48).min()
        part3 = self.C.rolling(window=48, min_periods=48).std()
        
        return part1 - part2 / part3
    
    def alpha166(self):
        """
        -20*(20-1)^1.5*SUM(CLOSE/DELAY(CLOSE,1)-1-MEAN(CLOSE/DELAY(CLOSE,1)-1,20),20)/((20-1)*(20-2)*(SUM((CLOSE/DELAY(CLOSE,1))^2,20))^1.5)
        """
        ret = self.C.pct_change()
        ret_mean = ret.rolling(window=20, min_periods=20).mean()
        part1 = (ret - ret_mean).rolling(window=20, min_periods=20).sum() * (-20 * 19 ** 1.5)
        part2 = ((self.C / self.C.shift(1)) ** 2).rolling(window=20, min_periods=20).sum() ** 1.5 * 19 * 18
        return part1 / part2
    
    def alpha167(self):
        """
        SUM(CLOSE-DELAY(CLOSE,1)>0?CLOSE-DELAY(CLOSE,1):0,12)
        """
        return np.maximum(self.C.diff(), 0.0).rolling(window=12, min_periods=12).sum()
    
    def alpha168(self):
        """
        -1*VOLUME/MEAN(VOLUME,20)
        """
        return -1 * self.V / self.V.rolling(window=20, min_periods=20).mean()
    
    def alpha169(self):
        """
        SMA(MEAN(DELAY(SMA(CLOSE-DELAY(CLOSE,1),9,1),1),12)-MEAN(DELAY(SMA(CLOSE-DELAY(CLOSE,1),9,1),1),26),10,1)
        """
        part1 = self._sma(self.C.diff(), 9, 1).shift(1)
        part2 = part1.rolling(window=12, min_periods=12).mean() - part1.rolling(window=26, min_periods=26).mean()
        return self._sma(part2, 10, 1)
    
    def alpha170(self):
        """
        ((RANK(1/CLOSE)*VOLUME)/MEAN(VOLUME,20))*(HIGH*RANK(HIGH-CLOSE)/(SUM(HIGH,5)/5))-RANK(VWAP-DELAY(VWAP,5))
        """
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        inv_close_rank = (1.0 / self.C).rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        vol_ma = self.V.rolling(window=20, min_periods=10).mean().fillna(method='ffill').fillna(method='bfill').replace(0, 1e-10)
        part1 = (inv_close_rank * self.V) / vol_ma
        
        high_minus_close_rank = (self.H - self.C).rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        high_ma5 = self.H.rolling(window=5, min_periods=3).sum() / 5.0
        high_ma5 = high_ma5.fillna(method='ffill').fillna(method='bfill').replace(0, 1e-10)
        part2 = (self.H * high_minus_close_rank) / high_ma5
        
        vwap_diff = vwap.diff(5).fillna(0)
        part3 = vwap_diff.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        alpha = (part1 * part2 - part3).fillna(method='ffill').fillna(method='bfill').clip(-10, 10)
        return alpha
    
    def alpha171(self):
        """
        (-1*(LOW-CLOSE)*(OPEN^5))/((CLOSE-HIGH)*(CLOSE^5))
        """
        self.C = self.C.clip(lower=1e-10)
        self.O = self.O.clip(lower=1e-10)
        self.H = self.H.clip(lower=1e-10)
        self.L = self.L.clip(lower=1e-10)
        
        part1 = (self.C - self.L) * (self.O ** 5)
        part2 = (self.C - self.H) * (self.C ** 5)
        part2 = part2.replace(0, 1e-10)
        mask_small = abs(part2) < 1e-10
        part2[mask_small] = 1e-10 * np.sign(part2[mask_small])
        
        alpha = part1 / part2
        alpha = alpha.replace([np.inf, -np.inf], np.nan).fillna(method='ffill').fillna(method='bfill').clip(-100, 100)
        return alpha
    
    def alpha172(self):
        """
        ADX指标
        """
        hd = self.H.diff()
        ld = -self.L.diff()
        tr = np.maximum(
            np.maximum(self.H - self.L, abs(self.H - self.C.shift(1))),
            abs(self.L - self.C.shift(1))
        )
        
        plus_dm = ((hd > 0) & (hd > ld)) * hd
        minus_dm = ((ld > 0) & (ld > hd)) * ld
        
        plus_di = plus_dm.rolling(window=14, min_periods=14).sum() * 100 / tr.rolling(window=14, min_periods=14).sum()
        minus_di = minus_dm.rolling(window=14, min_periods=14).sum() * 100 / tr.rolling(window=14, min_periods=14).sum()
        
        dx = abs(plus_di - minus_di) / (plus_di + minus_di) * 100
        return dx.rolling(window=6, min_periods=6).mean()
    
    def alpha173(self):
        """
        3*SMA(CLOSE,13,2)-2*SMA(SMA(CLOSE,13,2),13,2)+SMA(SMA(SMA(LOG(CLOSE),13,2),13,2),13,2)
        """
        sma = self._sma(self.C, 13, 2)
        sma2 = self._sma(sma, 13, 2)
        log_sma = self._sma(np.log(self.C), 13, 2)
        log_sma2 = self._sma(log_sma, 13, 2)
        log_sma3 = self._sma(log_sma2, 13, 2)
        
        return 3 * sma - 2 * sma2 + log_sma3
    
    def alpha174(self):
        """
        SMA((CLOSE>DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1)
        """
        part1 = self.C.rolling(window=20, min_periods=20).std()
        part1[self.C.diff() <= 0] = 0.0
        return self._sma(part1, 20, 1)
    
    def alpha175(self):
        """
        MEAN(MAX(MAX(HIGH-LOW,ABS(DELAY(CLOSE,1)-HIGH)),ABS(DELAY(CLOSE,1)-LOW)),6)
        """
        part1 = np.maximum(self.H - self.L, abs(self.C.shift(1) - self.H))
        part1 = np.maximum(part1, abs(self.C.shift(1) - self.L))
        return part1.rolling(window=6, min_periods=6).mean()
    
    def alpha176(self):
        """
        CORR(RANK((CLOSE-TSMIN(LOW,12))/(TSMAX(HIGH,12)-TSMIN(LOW,12))),RANK(VOLUME),6)
        """
        high_max = self.H.rolling(window=12, min_periods=12).max()
        low_min = self.L.rolling(window=12, min_periods=12).min()
        part1 = (self.C - low_min) / (high_max - low_min)
        part1 = part1.rank(pct=True)
        part2 = self.V.rank(pct=True)
        return part1.rolling(window=6, min_periods=6).corr(part2)
    
    def alpha177(self):
        """
        ((20-HIGHDAY(HIGH,20))/20)*100
        """
        def highday(x):
            return 19 - x.argmax() if len(x) == 20 else np.nan
        return (20 - self.H.rolling(window=20, min_periods=20).apply(highday)) / 20 * 100
    
    def alpha178(self):
        """
        (CLOSE-DELAY(CLOSE,1))/DELAY(CLOSE,1)*VOLUME
        """
        return self.C.pct_change() * self.V
    
    def alpha179(self):
        """
        RANK(CORR(VWAP,VOLUME,4))*RANK(CORR(RANK(LOW),RANK(MEAN(VOLUME,50)),12))
        """
        n_rows = len(self.df)
        self.V = self.V.replace(0, np.nan)
        self.AMOUNT = self.AMOUNT.replace(0, np.nan)
        vwap = (self.AMOUNT / self.V).fillna(method='ffill').fillna(method='bfill')
        self.V = self.V.fillna(method='ffill').fillna(method='bfill')
        
        part1_corr = vwap.rolling(window=4, min_periods=3).corr(self.V).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_corr.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        if n_rows < 50:
            vol_window = max(20, n_rows // 2)
            corr_window = max(5, min(12, n_rows // 4))
        else:
            vol_window = 50
            corr_window = 12
        
        vol_ma = self.V.rolling(window=vol_window, min_periods=max(5, vol_window//5)).mean().fillna(method='ffill').fillna(method='bfill')
        low_rank = self.L.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        vol_ma_rank = vol_ma.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        part2_corr = low_rank.rolling(window=corr_window, min_periods=max(3, corr_window//2)).corr(vol_ma_rank).fillna(method='ffill').fillna(method='bfill')
        part2 = part2_corr.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        alpha = (part1 * part2).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha180(self):
        """
        (MEAN(VOLUME,20)<VOLUME)?((-1*TSRANK(ABS(DELTA(CLOSE,7)),60))*SIGN(DELTA(CLOSE,7)):(-1*VOLUME))
        """
        condition = self.V.rolling(window=20, min_periods=20).mean() < self.V
        alpha = pd.Series(index=self.df.index, dtype=float)
        alpha[condition] = self._tsrank(abs(self.C.diff(7)), 60) * np.sign(self.C.diff(7)) * (-1)
        alpha[~condition] = -1 * self.V
        return alpha
    
    def alpha181(self):
        """
        SUM(RET-MEAN(RET,20)-(BANCHMARK_INDEX_CLOSE-MEAN(BANCHMARK_INDEX_CLOSE,20))^2,20)/SUM((BANCHMARK_INDEX_CLOSE-MEAN(BANCHMARK_INDEX_CLOSE,20))^3)
        """
        n_rows = len(self.df)
        
        if hasattr(self, 'index_df') and self.index_df is not None:
            index_data = self.index_df.copy()
            if 'close' in index_data.columns:
                index_close = index_data['close']
            elif 'closePrice' in index_data.columns:
                index_close = index_data['closePrice']
            else:
                index_close = index_data.iloc[:, 0]
            
            if 'date' in self.df.columns and 'date' in index_data.columns:
                self.df['date'] = pd.to_datetime(self.df['date'])
                index_data['date'] = pd.to_datetime(index_data['date'])
                date_to_index = dict(zip(index_data['date'], index_close))
                bm_close = self.df['date'].map(date_to_index).fillna(method='ffill').fillna(method='bfill')
            else:
                bm_close = index_close.reindex(self.df.index, method='ffill')
        else:
            bm_close = self.C.rolling(window=20, min_periods=10).mean()
        
        bm_mean = bm_close - bm_close.rolling(window=20, min_periods=10).mean().fillna(0)
        ret = self.C.pct_change().fillna(0)
        ret_mean = ret.rolling(window=20, min_periods=10).mean().fillna(0)
        
        part1 = (ret - ret_mean - bm_mean ** 2).rolling(window=20, min_periods=10).sum().fillna(method='ffill').fillna(method='bfill')
        part2 = (bm_mean ** 3).rolling(window=20, min_periods=10).sum().fillna(method='ffill').fillna(method='bfill').replace(0, 1e-10)
        
        alpha = (part1 / part2).fillna(method='ffill').fillna(method='bfill').clip(-100, 100)
        return alpha
    
    def alpha182(self):
        """
        COUNT((CLOSE>OPEN & BANCHMARK_INDEX_CLOSE>BANCHMARK_INDEX_OPEN) OR (CLOSE<OPEN &BANCHMARK_INDEX_CLOSE<BANCHMARK_INDEX_OPEN),20)/20
        """
        n_rows = len(self.df)
        
        if hasattr(self, 'index_df') and self.index_df is not None:
            index_data = self.index_df.copy()
            if 'close' in index_data.columns:
                index_close = index_data['close']
            elif 'closePrice' in index_data.columns:
                index_close = index_data['closePrice']
            else:
                index_close = index_data.iloc[:, 0]
            
            if 'open' in index_data.columns:
                index_open = index_data['open']
            elif 'openPrice' in index_data.columns:
                index_open = index_data['openPrice']
            else:
                index_open = index_close.shift(1).fillna(index_close)
            
            if 'date' in self.df.columns and 'date' in index_data.columns:
                self.df['date'] = pd.to_datetime(self.df['date'])
                index_data['date'] = pd.to_datetime(index_data['date'])
                date_to_close = dict(zip(index_data['date'], index_close))
                date_to_open = dict(zip(index_data['date'], index_open))
                bm_close = self.df['date'].map(date_to_close).fillna(method='ffill').fillna(method='bfill')
                bm_open = self.df['date'].map(date_to_open).fillna(method='ffill').fillna(method='bfill')
            else:
                bm_close = index_close.reindex(self.df.index, method='ffill')
                bm_open = index_open.reindex(self.df.index, method='ffill')
        else:
            bm_close = self.C.rolling(window=20, min_periods=5).mean()
            bm_open = self.O.rolling(window=20, min_periods=5).mean()
        
        bm_up = bm_close > bm_open
        stock_up = self.C > self.O
        stock_down = self.C < self.O
        
        condition1 = stock_up & bm_up
        condition2 = stock_down & ~bm_up
        condition = condition1 | condition2
        
        min_periods = max(5, min(10, n_rows // 4))
        alpha = condition.rolling(window=20, min_periods=min_periods).mean().fillna(method='ffill').fillna(method='bfill')
        
        return alpha
    
    def alpha183(self):
        """
        MAX(SUMAC(CLOSE-MEAN(CLOSE,24)))-MIN(SUMAC(CLOSE-MEAN(CLOSE,24)))/STD(CLOSE,24)
        """
        part = self.C - self.C.rolling(window=24, min_periods=24).mean()
        part = part.rolling(window=24, min_periods=24).sum()
        
        part1 = part.rolling(window=24, min_periods=24).max()
        part2 = part.rolling(window=24, min_periods=24).min()
        part3 = self.C.rolling(window=24, min_periods=24).std()
        
        return part1 - part2 / part3
    
    def alpha184(self):
        """
        RANK(CORR(DELAY(OPEN-CLOSE,1),CLOSE,200))+RANK(OPEN-CLOSE)
        """
        n_rows = len(self.df)
        if n_rows < 200:
            window = max(20, int(n_rows * 0.6))
        else:
            window = 200
        
        oc = self.O - self.C
        min_periods = max(10, min(50, window // 4))
        part1_corr = oc.shift(1).rolling(window=window, min_periods=min_periods).corr(self.C).fillna(method='ffill').fillna(method='bfill')
        part1 = part1_corr.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        part2 = oc.rank(pct=True, method='min').fillna(method='ffill').fillna(method='bfill')
        
        alpha = ((part1 + part2) / 2.0).fillna(method='ffill').fillna(method='bfill')
        return alpha
    
    def alpha185(self):
        """
        RANK(-1*(1-OPEN/CLOSE)^2)
        """
        return -1 * (1.0 - self.O / self.C) ** 2
    
    def alpha186(self):
        """
        ADXR指标
        """
        hd = self.H.diff()
        ld = -self.L.diff()
        tr = np.maximum(
            np.maximum(self.H - self.L, abs(self.H - self.C.shift(1))),
            abs(self.L - self.C.shift(1))
        )
        
        plus_dm = ((hd > 0) & (hd > ld)) * hd
        minus_dm = ((ld > 0) & (ld > hd)) * ld
        
        plus_di = plus_dm.rolling(window=14, min_periods=14).sum() * 100 / tr.rolling(window=14, min_periods=14).sum()
        minus_di = minus_dm.rolling(window=14, min_periods=14).sum() * 100 / tr.rolling(window=14, min_periods=14).sum()
        
        dx = abs(plus_di - minus_di) / (plus_di + minus_di) * 100
        adx = dx.rolling(window=6, min_periods=6).mean()
        adxr = (adx + adx.shift(6)) / 2
        
        return adxr
    
    def alpha187(self):
        """
        SUM(OPEN<=DELAY(OPEN,1)?0:MAX(HIGH-OPEN,OPEN-DELAY(OPEN,1)),20)
        """
        part1 = np.maximum(self.H - self.O, self.O.diff())
        part1[self.O.diff() <= 0] = 0.0
        return part1.rolling(window=20, min_periods=20).sum()
    
    def alpha188(self):
        """
        ((HIGH-LOW-SMA(HIGH-LOW,11,2))/SMA(HIGH-LOW,11,2))*100
        """
        hl = self.H - self.L
        sma = self._sma(hl, 11, 2)
        return (hl - sma) / sma * 100
    
    def alpha189(self):
        """
        MEAN(ABS(CLOSE-MEAN(CLOSE,6)),6)
        """
        ma = self.C.rolling(window=6, min_periods=6).mean()
        return abs(self.C - ma).rolling(window=6, min_periods=6).mean()
    
    def alpha190(self):
        """
        LOG((COUNT(RET>((CLOSE/DELAY(CLOSE,19))^(1/20)-1),20)-1)
        *SUMIF((RET-(CLOSE/DELAY(CLOSE,19))^(1/20)-1)^2,20,RET<(CLOSE/DELAY(CLOSE,19))^(1/20)-1)
        /(COUNT(RET<(CLOSE/DELAY(CLOSE,19))^(1/20)-1,20)
        *SUMIF((RET-((CLOSE/DELAY(CLOSE,19))^(1/20)-1))^2,20,RET>(CLOSE/DELAY(CLOSE,19))^(1/20)-1)))
        """
        ret = self.C.pct_change()
        ret_19 = (self.C / self.C.shift(19)) ** 0.05 - 1.0
        
        part1 = (ret > ret_19).rolling(window=20, min_periods=20).sum() - 1.0
        part2 = (np.minimum(ret - ret_19, 0.0) ** 2).rolling(window=20, min_periods=20).sum()
        part3 = (ret < ret_19).rolling(window=20, min_periods=20).sum()
        part4 = (np.maximum(ret - ret_19, 0.0) ** 2).rolling(window=20, min_periods=20).sum()
        
        return np.log(part1 * part2 / part3 / part4)
    
    def alpha191(self):
        """
        CORR(MEAN(VOLUME,20),LOW,5)+(HIGH+LOW)/2-CLOSE
        """
        part1 = self.V.rolling(window=20, min_periods=20).mean().rolling(window=5, min_periods=5).corr(self.L)
        return part1 + (self.H + self.L) / 2 - self.C


if __name__ == '__main__':
    api = xg_factor()
    result = api.CROSS_DOWN()
    # print(result)