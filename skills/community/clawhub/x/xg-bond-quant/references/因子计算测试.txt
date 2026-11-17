import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import json
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import os
from xg_factor import xg_factor
from tqdm import tqdm
class xg_factor_trader:
    def __init__(self,
            index_stock='000300.SH',
            start_date='20260101',
            end_date='20500101'):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.index_stock=index_stock
        self.start_date=start_date
        self.end_date=end_date
        self.adj_type = 'none'
    def adjust_price(self, df):
        '''
        根据复权方式调整价格
        '''
        if self.adj_type == 'none':
            return df
        
        if 'preClose' in df.columns:
            try:
                df['adj_factor'] = 1.0
                for i in range(1, len(df)):
                    if df.loc[i, 'preClose'] > 0:
                        actual_return = df.loc[i, 'close'] / df.loc[i, 'preClose']
                        df.loc[i, 'adj_factor'] = df.loc[i-1, 'adj_factor'] * actual_return
                    else:
                        df.loc[i, 'adj_factor'] = df.loc[i-1, 'adj_factor']
                
                if self.adj_type in ['front', 'front_ratio']:
                    last_factor = df['adj_factor'].iloc[-1]
                    df['adj_factor'] = df['adj_factor'] / last_factor
                
                price_cols = ['open', 'high', 'low', 'close']
                for col in price_cols:
                    if col in df.columns:
                        df[col] = df[col] * df['adj_factor']
                
                df = df.drop(columns=['adj_factor'])
            except Exception as e:
                print(f"  复权计算出错: {e}")
                return df
        else:
            print(f"  警告: 没有preClose列，使用原始价格")
        
        return df
    def _convert_to_serializable(self, obj):
        '''
        递归转换不可序列化的对象为JSON可序列化格式
        '''
        if isinstance(obj, dict):
            return {k: self._convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_serializable(item) for item in obj]
        elif isinstance(obj, pd.Timestamp):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj) if not np.isnan(obj) else None
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict('records')
        elif isinstance(obj, pd.Series):
            return obj.tolist()
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif pd.isna(obj):
            return None
        else:
            return obj
    
    def get_stock_data(self, stock_code):
        '''读取单个股票历史数据'''
        try:
            df = pd.read_parquet(r'{}/data/历史数据/{}.parquet'.format(self.path, stock_code),
                engine='pyarrow',use_threads=True)
            
            df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
            df = df[(df['date'] >= pd.to_datetime(self.start_date)) & 
                    (df['date'] <= pd.to_datetime(self.end_date))]
            df = df.sort_values('date').reset_index(drop=True)
            
            # 删除无效数据行
            df = df[df['close'] > 0]
            df = df[df['open'] > 0]
            
            # 应用复权
            df = self.adjust_price(df)
            
            # 计算涨跌幅
            df['zdf'] = df['close'].pct_change()
            
            return df
        except Exception as e:
            print(f"加载股票数据出错 {stock_code}: {e}")
            return pd.DataFrame()
    
    def _load_single_stock(self, stock):
        '''单个股票加载函数（用于多线程）'''
        try:
            df = self.get_stock_data(stock)
            if not df.empty:
                return (stock, df, True, f"数据加载成功: {len(df)} 行")
            else:
                return (stock, None, False, "数据加载失败")
        except Exception as e:
            return (stock, None, False, f"加载异常: {e}")
    
    def adjust_price(self, df):
        '''
        根据复权方式调整价格
        '''
        if self.adj_type == 'none':
            return df
        
        if 'preClose' in df.columns:
            try:
                df['adj_factor'] = 1.0
                for i in range(1, len(df)):
                    if df.loc[i, 'preClose'] > 0:
                        actual_return = df.loc[i, 'close'] / df.loc[i, 'preClose']
                        df.loc[i, 'adj_factor'] = df.loc[i-1, 'adj_factor'] * actual_return
                    else:
                        df.loc[i, 'adj_factor'] = df.loc[i-1, 'adj_factor']
                
                if self.adj_type in ['front', 'front_ratio']:
                    last_factor = df['adj_factor'].iloc[-1]
                    df['adj_factor'] = df['adj_factor'] / last_factor
                
                price_cols = ['open', 'high', 'low', 'close']
                for col in price_cols:
                    if col in df.columns:
                        df[col] = df[col] * df['adj_factor']
                
                df = df.drop(columns=['adj_factor'])
            except Exception as e:
                print(f"  复权计算出错: {e}")
                return df
        else:
            print(f"  警告: 没有preClose列，使用原始价格")
        
        return df
    def get_index_data(self):
        '''读取指数历史数据'''
        try:
        
            file_path = r'{}/data/指数数据/{}.parquet'.format(self.path, self.index_stock)
            if not os.path.exists(file_path):
                print(f"指数文件不存在: {file_path}")
                return pd.DataFrame()
            
            df = pd.read_parquet(file_path,engine='pyarrow',use_threads=True)
            df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
            df = df[(df['date'] >= pd.to_datetime(self.start_date)) & 
                    (df['date'] <= pd.to_datetime(self.end_date))]
            df = df.sort_values('date').reset_index(drop=True)
            df = df[df['close'] > 0]
            df = df[df['open'] > 0]
            
            print(f"指数数据加载成功: {len(df)} 行")
            return df
        except Exception as e:
            print(f"加载指数数据出错: {e}")
            return pd.DataFrame()
if __name__=='__main__':
    stock='513100.SH'
    api=xg_factor_trader()
    df=api.get_stock_data(stock)
    index_df=api.get_index_data()
    models=xg_factor(df=df,index_df=index_df)
    result=models.MACD_金叉()
    df['因子']=result
    df=df[['date','证券代码','证券名称','因子']]
    print(df)