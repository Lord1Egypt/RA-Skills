import pandas as pd
import numpy as np
import os
from datetime import datetime
import json
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor
from tqdm import tqdm
import multiprocessing
import gc
import shutil
import pickle
from functools import lru_cache
import re

warnings.filterwarnings("ignore")


# ========== 模块级函数（用于多进程） ==========
def _call_factor_function_worker(models, func_str):
    """因子函数调用工作函数（修复版 - 正确解析参数）"""
    if not func_str:
        return None
    
    # 提取函数名
    func_name = func_str.split('(')[0].strip() if '(' in func_str else func_str.strip()
    
    if not hasattr(models, func_name):
        return None
    
    method = getattr(models, func_name)
    if not callable(method):
        return None
    
    # 如果没有参数，直接调用
    if '(' not in func_str or func_str.endswith('()'):
        try:
            return method()
        except Exception as e:
            return None
    
    # 解析参数
    try:
        start = func_str.index('(') + 1
        end = func_str.rindex(')')
        params_str = func_str[start:end].strip()
        
        if not params_str:
            return method()
        
        # 解析参数 - 处理带括号的复杂参数
        args = {}
        # 按逗号分割，但跳过括号内的逗号
        params = re.split(r',(?![^()]*\))', params_str)
        
        for param in params:
            param = param.strip()
            if not param:
                continue
                
            if '=' in param:
                key, value = param.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # 尝试转换为数值
                try:
                    if value.lower() == 'true':
                        args[key] = True
                    elif value.lower() == 'false':
                        args[key] = False
                    elif value.lower() == 'none':
                        args[key] = None
                    elif '.' in value:
                        args[key] = float(value)
                    else:
                        args[key] = int(value)
                except:
                    # 尝试去除引号
                    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                        args[key] = value[1:-1]
                    else:
                        args[key] = value
            else:
                # 位置参数 - 尝试转换为数值
                try:
                    if '.' in param:
                        args['arg'] = float(param)
                    else:
                        args['arg'] = int(param)
                except:
                    args['arg'] = param
        
        # 调用方法
        try:
            return method(**args)
        except TypeError as e:
            # 如果参数不匹配，尝试不带参数调用
            try:
                return method()
            except:
                return None
    except Exception as e:
        return None


def calculate_single_stock_worker_optimized(stock_code, path, index_stock, start_date, end_date, text, adj_type='none'):
    """多进程工作函数：计算单只股票的所有因子（优化版 - 修复数据对齐）"""
    try:
        from xg_factor import xg_factor
        
        file_path = r'{}/data/历史数据/{}.parquet'.format(path, stock_code)
        if not os.path.exists(file_path):
            return (stock_code, False, "数据文件不存在")
        
        # 只读取需要的列，减少内存
        use_cols = ['date','证券代码','证券名称' ,'open', 'high', 'low', 'close', 'volume', 'amount']
        if adj_type != 'none':
            use_cols.append('preClose')
        
        df = pd.read_parquet(file_path, columns=use_cols, engine='pyarrow', use_threads=True)
        df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
        
        # 使用query过滤，速度更快
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        df = df[(df['date'] >= start_dt) & (df['date'] <= end_dt)]
        df = df.sort_values('date').reset_index(drop=True)
        
        # 过滤无效数据
        df = df[(df['close'] > 0) & (df['open'] > 0)]
        
        if df.empty:
            return (stock_code, False, "无有效数据")
        
        # 获取指数数据
        index_file = r'{}/data/指数数据/{}.parquet'.format(path, index_stock)
        index_df = pd.DataFrame()
        if os.path.exists(index_file):
            try:
                index_df = pd.read_parquet(index_file, columns=['date', 'open', 'close'], 
                                          engine='pyarrow', use_threads=True)
                index_df['date'] = pd.to_datetime(index_df['date'].astype(str), format='%Y%m%d')
                index_df = index_df[(index_df['date'] >= start_dt) & (index_df['date'] <= end_dt)]
                index_df = index_df.sort_values('date').reset_index(drop=True)
            except:
                index_df = pd.DataFrame()
        
        # 创建因子计算实例
        models = xg_factor(df=df, index_df=index_df)
        
        # 预分配结果列
        for name in text.keys():
            df[name] = np.nan
        
        # 批量计算因子
        for name, func_str in text.items():
            try:
                result = _call_factor_function_worker(models, func_str)
                
                if result is None:
                    continue
                elif isinstance(result, pd.Series):
                    # 对齐长度 - 确保与df长度一致
                    if len(result) == len(df):
                        df[name] = result.values
                    elif len(result) < len(df):
                        # 前面填充NaN
                        temp = pd.Series([np.nan] * (len(df) - len(result)) + list(result))
                        df[name] = temp.values
                    else:
                        # 截取前len(df)个
                        df[name] = result.iloc[:len(df)].values
                elif isinstance(result, (int, float, np.number)):
                    # 标量值，整列赋值
                    df[name] = result
                elif isinstance(result, (list, tuple, np.ndarray)):
                    if len(result) == len(df):
                        df[name] = result
                    elif len(result) < len(df):
                        temp = [np.nan] * (len(df) - len(result)) + list(result)
                        df[name] = temp
                    else:
                        df[name] = result[:len(df)]
                else:
                    try:
                        if hasattr(result, '__len__') and len(result) == len(df):
                            df[name] = result
                    except:
                        pass
            except Exception as e:
                continue
        
        if df.shape[0] > 0:
            save_path = r'{}/data/全部因子数据/{}.parquet'.format(path, stock_code)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            df.to_parquet(save_path, compression='zstd')
            return (stock_code, True, "成功")
        else:
            return (stock_code, False, "数据为空")
            
    except Exception as e:
        return (stock_code, False, str(e))


class xg_factor_trader:
    def __init__(self,
            index_stock='000300.SH',
            start_date='20200101',
            end_date='20500101',
            max_workers=None,
            verbose=False,
            use_multiprocess=True,
            chunk_size=30,
            stage_size=200,
            use_async_io=True,
            force_recalc=False):
        """
        初始化因子计算器（超级优化版）
        
        Args:
            index_stock: 指数代码
            start_date: 开始日期
            end_date: 结束日期
            max_workers: 最大进程数
            verbose: 是否显示详细信息
            use_multiprocess: 是否使用多进程
            chunk_size: 批次处理大小
            stage_size: 阶段大小
            use_async_io: 是否使用异步IO
            force_recalc: 是否强制重新计算所有股票（True=覆盖计算全部，False=跳过已计算的）
        """
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.index_stock = index_stock
        self.start_date = start_date
        self.end_date = end_date
        self.chunk_size = chunk_size
        self.stage_size = stage_size
        self.use_async_io = use_async_io
        self.force_recalc = force_recalc
        
        if max_workers is None:
            self.max_workers = max(1, multiprocessing.cpu_count() - 1)
        else:
            self.max_workers = max_workers
        
        self.verbose = verbose
        self.use_multiprocess = use_multiprocess
        
        # 缓存指数数据
        self.index_df = self.get_index_data()
        self.adj_type = 'none'
        
        # 加载因子表
        try:
            with open(r'因子表.json', 'r+', encoding='utf-8') as f:
                com = f.read()
            self.text = json.loads(com)
        except:
            self.text = {}
            print("警告: 因子表.json 不存在，请先创建")
        
        # 统计
        self.success_count = 0
        self.fail_count = 0
        self.fail_list = []
        self.stage_results = []
        
        # 创建目录
        os.makedirs(r'{}/data/全部因子数据'.format(self.path), exist_ok=True)
        
        self.stock_list = None
        self._processed_cache = set()  # 缓存已处理的股票
        
        # 如果强制重算，清空已计算的缓存
        if self.force_recalc:
            print("⚠️  强制重算模式已开启，将重新计算所有股票并覆盖已有数据")
            # 清理已处理缓存，但保留目录
            self._processed_cache = set()

    def get_all_factor_table(self):
        """生成因子列表"""
        data = pd.DataFrame()
        text_copy = self.text.copy()
        text_copy['close'] = '默认'
        text_copy['high'] = '默认'
        text_copy['low'] = '默认'
        text_copy['open'] = '默认'
        text_copy['amount'] = '默认'
        text_copy['volume'] = '默认'
        text_copy['zdf'] = '默认'

        for name, func in text_copy.items():
            data = pd.concat([data, pd.DataFrame({'因子名称': [name], '因子函数': [func]})], ignore_index=True)
        
        os.makedirs(r'{}/data/全部因子'.format(self.path), exist_ok=True)
        data.to_excel(r'{}/data/全部因子/全部因子.xlsx'.format(self.path))
        data.to_json(r'{}/data/全部因子/全部因子.json'.format(self.path), orient='records', force_ascii=False)
        print(f"因子列表已生成，共 {len(data)} 个因子")

    @lru_cache(maxsize=128)
    def _get_stock_data_cached(self, stock_code):
        """缓存股票数据"""
        return self.get_stock_data(stock_code)

    def get_stock_data(self, stock_code):
        """获取单只股票数据（优化版）"""
        try:
            file_path = r'{}/data/历史数据/{}.parquet'.format(self.path, stock_code)
            if not os.path.exists(file_path):
                return pd.DataFrame()
            
            # 只读需要的列
            use_cols = ['date','证券代码','证券名称', 'open', 'high', 'low', 'close', 'volume', 'amount']
            if self.adj_type != 'none':
                use_cols.append('preClose')
            
            df = pd.read_parquet(file_path, columns=use_cols, engine='pyarrow', use_threads=True)
            df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
            
            start_dt = pd.to_datetime(self.start_date)
            end_dt = pd.to_datetime(self.end_date)
            df = df[(df['date'] >= start_dt) & (df['date'] <= end_dt)]
            df = df.sort_values('date').reset_index(drop=True)
            df = df[(df['close'] > 0) & (df['open'] > 0)]
            
            if df.empty:
                return df
            
            df = self.adjust_price(df)
            df['zdf'] = df['close'].pct_change() * 100
            return df
        except Exception as e:
            return pd.DataFrame()
    
    def adjust_price(self, df):
        """价格复权（优化版）"""
        if self.adj_type == 'none' or 'preClose' not in df.columns:
            return df
        
        try:
            # 使用向量化操作
            df['adj_factor'] = 1.0
            pre_close = df['preClose'].values
            close = df['close'].values
            
            # 批量计算复权因子
            for i in range(1, len(df)):
                if pre_close[i] > 0:
                    df.loc[i, 'adj_factor'] = df.loc[i-1, 'adj_factor'] * (close[i] / pre_close[i])
                else:
                    df.loc[i, 'adj_factor'] = df.loc[i-1, 'adj_factor']
            
            if self.adj_type in ['front', 'front_ratio']:
                df['adj_factor'] = df['adj_factor'] / df['adj_factor'].iloc[-1]
            
            price_cols = ['open', 'high', 'low', 'close']
            for col in price_cols:
                if col in df.columns:
                    df[col] = df[col] * df['adj_factor']
            df = df.drop(columns=['adj_factor'])
        except Exception as e:
            pass
        return df
    
    def get_index_data(self):
        """获取指数数据"""
        try:
            file_path = r'{}/data/指数数据/{}.parquet'.format(self.path, self.index_stock)
            if not os.path.exists(file_path):
                return pd.DataFrame()
            df = pd.read_parquet(file_path, columns=['date', 'open', 'close'], 
                                engine='pyarrow', use_threads=True)
            df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
            
            start_dt = pd.to_datetime(self.start_date)
            end_dt = pd.to_datetime(self.end_date)
            df = df[(df['date'] >= start_dt) & (df['date'] <= end_dt)]
            df = df.sort_values('date').reset_index(drop=True)
            df = df[(df['close'] > 0) & (df['open'] > 0)]
            return df
        except Exception as e:
            return pd.DataFrame()
    
    def _call_factor_function(self, models, func_str):
        """调用因子函数（单线程版本 - 修复参数解析）"""
        if not func_str:
            return None
        
        func_name = func_str.split('(')[0].strip() if '(' in func_str else func_str.strip()
        
        if not hasattr(models, func_name):
            return None
        
        method = getattr(models, func_name)
        if not callable(method):
            return None
        
        if '(' not in func_str or func_str.endswith('()'):
            try:
                return method()
            except:
                return None
        
        try:
            start = func_str.index('(') + 1
            end = func_str.rindex(')')
            params_str = func_str[start:end].strip()
            
            if not params_str:
                return method()
            
            # 解析参数 - 处理带括号的复杂参数
            args = {}
            params = re.split(r',(?![^()]*\))', params_str)
            
            for param in params:
                param = param.strip()
                if not param:
                    continue
                    
                if '=' in param:
                    key, value = param.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    try:
                        if value.lower() == 'true':
                            args[key] = True
                        elif value.lower() == 'false':
                            args[key] = False
                        elif value.lower() == 'none':
                            args[key] = None
                        elif '.' in value:
                            args[key] = float(value)
                        else:
                            args[key] = int(value)
                    except:
                        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                            args[key] = value[1:-1]
                        else:
                            args[key] = value
                else:
                    try:
                        if '.' in param:
                            args['arg'] = float(param)
                        else:
                            args['arg'] = int(param)
                    except:
                        args['arg'] = param
            
            try:
                return method(**args)
            except TypeError as e:
                try:
                    return method()
                except:
                    return None
        except:
            return None
    
    def cacal_stock_factor(self, stock='513100.SH'):
        """单只股票因子计算（修复版）"""
        try:
            from xg_factor import xg_factor
            df = self.get_stock_data(stock_code=stock)
            if df.empty:
                print(f"股票 {stock} 无数据")
                return False
            
            print(f"股票 {stock} 数据加载成功: {len(df)} 行")
            print(f"因子数量: {len(self.text)} 个")
            
            models = xg_factor(df=df, index_df=self.index_df)
            factor_items = list(self.text.items())
            
            for name, func_str in tqdm(factor_items, desc=f"计算 {stock}", unit="个", leave=False, disable=not self.verbose):
                try:
                    result = self._call_factor_function(models, func_str)
                    if result is None:
                        df[name] = np.nan
                        continue
                    
                    # 处理不同类型的返回值
                    if isinstance(result, pd.Series):
                        # 对齐长度
                        if len(result) < df.shape[0]:
                            # 结果长度小于df，在前面填充NaN
                            result = pd.concat([pd.Series([np.nan] * (df.shape[0] - len(result))), result], ignore_index=True)
                        elif len(result) > df.shape[0]:
                            # 结果长度大于df，截取前df.shape[0]个
                            result = result.iloc[:df.shape[0]]
                        df[name] = result.values
                        
                    elif isinstance(result, (list, tuple, np.ndarray)):
                        # 列表、元组、数组
                        if len(result) < df.shape[0]:
                            # 前面填充NaN
                            result = [np.nan] * (df.shape[0] - len(result)) + list(result)
                        elif len(result) > df.shape[0]:
                            # 截取前df.shape[0]个
                            result = result[:df.shape[0]]
                        df[name] = result
                        
                    elif isinstance(result, (int, float, np.number)):
                        # 标量值，直接赋值（整列都是同一个值）
                        df[name] = result
                        
                    else:
                        # 其他类型尝试转换
                        try:
                            if hasattr(result, '__len__') and len(result) == df.shape[0]:
                                df[name] = result
                            else:
                                df[name] = np.nan
                        except:
                            df[name] = np.nan
                            
                except Exception as e:
                    df[name] = np.nan
            
            if df.shape[0] > 0:
                save_path = r'{}/data/全部因子数据/{}.parquet'.format(self.path, stock)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                df.to_parquet(save_path, compression='zstd')
                print(f"股票 {stock} 因子计算完成，共 {df.shape[0]} 行数据")
                return True
            return False
        except Exception as e:
            print(f"股票 {stock} 计算失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _calculate_single_stock_sync(self, stock):
        """同步单线程计算单只股票（修复版）"""
        try:
            from xg_factor import xg_factor
            df = self.get_stock_data(stock_code=stock)
            if df.empty:
                return False
            
            models = xg_factor(df=df, index_df=self.index_df)
            df_len = len(df)
            
            for name, func_str in self.text.items():
                try:
                    result = self._call_factor_function(models, func_str)
                    
                    if result is None:
                        df[name] = np.nan
                    elif isinstance(result, pd.Series):
                        if len(result) == df_len:
                            df[name] = result.values
                        elif len(result) < df_len:
                            temp = pd.Series([np.nan] * (df_len - len(result)) + list(result))
                            df[name] = temp.values
                        else:
                            df[name] = result.iloc[:df_len].values
                    elif isinstance(result, (int, float, np.number)):
                        df[name] = result
                    elif isinstance(result, (list, tuple, np.ndarray)):
                        if len(result) == df_len:
                            df[name] = result
                        elif len(result) < df_len:
                            df[name] = [np.nan] * (df_len - len(result)) + list(result)
                        else:
                            df[name] = result[:df_len]
                    else:
                        try:
                            if hasattr(result, '__len__') and len(result) == df_len:
                                df[name] = result
                            else:
                                df[name] = np.nan
                        except:
                            df[name] = np.nan
                except Exception as e:
                    df[name] = np.nan
            
            if df.shape[0] > 0:
                save_path = r'{}/data/全部因子数据/{}.parquet'.format(self.path, stock)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                df.to_parquet(save_path, compression='zstd')
                return True
            return False
        except Exception as e:
            if self.verbose:
                print(f"计算 {stock} 时出错: {e}")
            return False
    def get_bond_stock(self):
        '''
        可转债代码
        '''
        df_bond = pd.read_excel(r'{}/data/可转债代码/可转债代码.xlsx'.format(self.path))
        df_bond['代码'] = df_bond['代码'].apply(lambda x: str(x)[2:] + '.' + str(x)[:2])
        df_bond.columns = ['证券代码', '证券名称']
        return df_bond
    def _get_stock_list(self):
        """获取股票列表（带缓存）- 支持强制重算模式"""
        if self.stock_list is not None:
            return self.stock_list
        
        # 如果不强制重算，加载已处理缓存
        if not self.force_recalc:
            try:
                factor_path = r'{}/data/全部因子数据'.format(self.path)
                if os.path.exists(factor_path):
                    processed = [f.replace('.parquet', '') for f in os.listdir(factor_path) 
                                if f.endswith('.parquet') and f != '失败列表.xlsx']
                    self._processed_cache = set(processed)
            except:
                self._processed_cache = set()
        else:
            # 强制重算模式：清空缓存，但保留已计算文件（后续会覆盖）
            self._processed_cache = set()
            print("🔄 强制重算模式：将重新计算所有股票并覆盖已有数据文件")
        
        try:
            # 尝试从Excel读取
            excel_path = r'{}/data/基金代码/基金代码.xlsx'.format(self.path)
            if os.path.exists(excel_path):
                df_fund = pd.read_excel(excel_path)
                df_fund=df_fund[['基金代码','基金名称']]
                df_fund.columns = ['证券代码', '证券名称']
                df_bond=self.get_bond_stock()
                df=pd.concat([df_fund,df_bond],ignore_index=True)
                if '证券代码' in df.columns:
                    self.stock_list = df['证券代码'].tolist()
                    # 如果不强制重算，过滤已处理的股票
                    if not self.force_recalc and self._processed_cache:
                        original_count = len(self.stock_list)
                        self.stock_list = [s for s in self.stock_list if s not in self._processed_cache]
                        skipped_count = original_count - len(self.stock_list)
                        if skipped_count > 0:
                            print(f"⏭️  跳过已计算的股票: {skipped_count} 只")
                    
                    print(f"📊 本次需要计算的股票数: {len(self.stock_list)} 只")
                    return self.stock_list
            
            # 尝试从parquet目录获取
            hist_path = r'{}/data/历史数据'.format(self.path)
            if os.path.exists(hist_path):
                files = [f.replace('.parquet', '') for f in os.listdir(hist_path) if f.endswith('.parquet')]
                if files:
                    self.stock_list = files
                    # 如果不强制重算，过滤已处理的
                    if not self.force_recalc and self._processed_cache:
                        original_count = len(self.stock_list)
                        self.stock_list = [s for s in self.stock_list if s not in self._processed_cache]
                        skipped_count = original_count - len(self.stock_list)
                        if skipped_count > 0:
                            print(f"⏭️  跳过已计算的股票: {skipped_count} 只")
                    
                    print(f"📊 本次需要计算的股票数: {len(self.stock_list)} 只")
                    return self.stock_list
            
            self.stock_list = []
            return self.stock_list
        except Exception as e:
            print(f"获取股票列表失败: {e}")
            self.stock_list = []
            return self.stock_list
    
    def _clear_cache(self):
        """清理缓存释放内存"""
        gc.collect()
    
    def _save_stage_checkpoint(self, stage_num, total_stages):
        """保存阶段检查点"""
        checkpoint_path = r'{}/data/全部因子数据/checkpoint.json'.format(self.path)
        checkpoint_data = {
            'stage': stage_num,
            'total_stages': total_stages,
            'success_count': self.success_count,
            'fail_count': self.fail_count,
            'force_recalc': self.force_recalc,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        try:
            with open(checkpoint_path, 'w', encoding='utf-8') as f:
                json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def cacal_all_stock_factor_single(self):
        """单线程分阶段计算所有股票因子"""
        stock_list = self._get_stock_list()
        if not stock_list:
            print("没有找到需要计算的股票数据")
            return
        
        total = len(stock_list)
        self.success_count = 0
        self.fail_count = 0
        self.fail_list = []
        self.stage_results = []
        
        total_stages = max(1, (total + self.stage_size - 1) // self.stage_size)
        
        print(f"\n{'='*60}")
        print(f"单线程分阶段计算模式")
        print(f"需要计算股票数: {total}")
        print(f"因子数量: {len(self.text)} 个")
        print(f"阶段大小: {self.stage_size} 只/阶段")
        print(f"总阶段数: {total_stages}")
        if self.force_recalc:
            print("模式: 🔄 强制重算（覆盖已有数据）")
        else:
            print("模式: 📝 增量计算（跳过已计算）")
        print(f"{'='*60}\n")
        
        start_time = datetime.now()
        
        for stage_idx in range(total_stages):
            stage_start = stage_idx * self.stage_size
            stage_end = min(stage_start + self.stage_size, total)
            stage_stocks = stock_list[stage_start:stage_end]
            
            stage_success = 0
            stage_fail = 0
            stage_start_time = datetime.now()
            
            print(f"\n阶段 {stage_idx + 1}/{total_stages} (股票 {stage_start+1}-{stage_end}/{total})")
            
            # 使用线程池进行并行IO
            if self.use_async_io and len(stage_stocks) > 10:
                with ThreadPoolExecutor(max_workers=min(8, len(stage_stocks))) as io_executor:
                    # 预加载数据
                    futures = {io_executor.submit(self.get_stock_data, stock): stock for stock in stage_stocks}
                    for future in as_completed(futures):
                        stock = futures[future]
                        try:
                            df = future.result()
                            if not df.empty:
                                self.success_count += 1
                                stage_success += 1
                                # 保存数据
                                save_path = r'{}/data/全部因子数据/{}.parquet'.format(self.path, stock)
                                df.to_parquet(save_path, compression='zstd')
                            else:
                                self.fail_count += 1
                                stage_fail += 1
                                self.fail_list.append(stock)
                        except:
                            self.fail_count += 1
                            stage_fail += 1
                            self.fail_list.append(stock)
            else:
                # 传统顺序处理
                for idx, stock in enumerate(tqdm(stage_stocks, desc=f"阶段{stage_idx+1}进度", unit="只")):
                    try:
                        success = self._calculate_single_stock_sync(stock)
                        if success:
                            self.success_count += 1
                            stage_success += 1
                        else:
                            self.fail_count += 1
                            stage_fail += 1
                            self.fail_list.append(stock)
                    except Exception as e:
                        self.fail_count += 1
                        stage_fail += 1
                        self.fail_list.append(stock)
            
            stage_elapsed = (datetime.now() - stage_start_time).total_seconds()
            self.stage_results.append({
                'stage': stage_idx + 1,
                'stocks': len(stage_stocks),
                'success': stage_success,
                'fail': stage_fail,
                'time': stage_elapsed
            })
            
            self._clear_cache()
            self._save_stage_checkpoint(stage_idx + 1, total_stages)
            
            total_elapsed = (datetime.now() - start_time).total_seconds()
            print(f"\n阶段 {stage_idx+1} 完成! 成功:{stage_success} 失败:{stage_fail} 耗时:{stage_elapsed:.1f}s")
            
            if stage_idx + 1 < total_stages:
                avg_time = total_elapsed / (stage_idx + 1)
                remaining = avg_time * (total_stages - stage_idx - 1)
                print(f"  预计剩余: {remaining:.1f}s ({remaining/60:.1f}分钟)")
        
        elapsed = (datetime.now() - start_time).total_seconds()
        self._print_summary(total, elapsed)
    
    def cacal_all_stock_factor_multiprocess(self):
        """多进程分阶段计算所有股票因子（优化版）"""
        stock_list = self._get_stock_list()
        if not stock_list:
            print("没有找到需要计算的股票数据")
            return
        
        total = len(stock_list)
        self.success_count = 0
        self.fail_count = 0
        self.fail_list = []
        self.stage_results = []
        
        total_stages = max(1, (total + self.stage_size - 1) // self.stage_size)
        
        print(f"\n{'='*60}")
        print(f"多进程分阶段计算模式（优化版）")
        print(f"需要计算股票数: {total}")
        print(f"因子数量: {len(self.text)} 个")
        print(f"进程数: {self.max_workers}")
        print(f"批次大小: {self.chunk_size}")
        print(f"阶段大小: {self.stage_size} 只/阶段")
        print(f"总阶段数: {total_stages}")
        if self.force_recalc:
            print("模式: 🔄 强制重算（覆盖已有数据）")
        else:
            print("模式: 📝 增量计算（跳过已计算）")
        print(f"{'='*60}\n")
        
        start_time = datetime.now()
        
        for stage_idx in range(total_stages):
            stage_start = stage_idx * self.stage_size
            stage_end = min(stage_start + self.stage_size, total)
            stage_stocks = stock_list[stage_start:stage_end]
            
            stage_success = 0
            stage_fail = 0
            stage_start_time = datetime.now()
            
            print(f"\n阶段 {stage_idx + 1}/{total_stages} (股票 {stage_start+1}-{stage_end}/{total})")
            
            # 批量提交任务
            with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {}
                for stock in stage_stocks:
                    future = executor.submit(
                        calculate_single_stock_worker_optimized,
                        stock,
                        self.path,
                        self.index_stock,
                        self.start_date,
                        self.end_date,
                        self.text,
                        self.adj_type
                    )
                    futures[future] = stock
                
                with tqdm(total=len(futures), desc=f"阶段{stage_idx+1}进度", unit="只") as pbar:
                    for future in as_completed(futures):
                        try:
                            stock, success, msg = future.result(timeout=600)
                            if success:
                                self.success_count += 1
                                stage_success += 1
                            else:
                                self.fail_count += 1
                                stage_fail += 1
                                self.fail_list.append(stock)
                            pbar.set_postfix_str(f"成功:{self.success_count} 失败:{self.fail_count}")
                        except Exception as e:
                            self.fail_count += 1
                            stage_fail += 1
                            stock = futures[future]
                            self.fail_list.append(stock)
                            if self.verbose:
                                print(f"股票 {stock} 计算异常: {e}")
                        pbar.update(1)
            
            stage_elapsed = (datetime.now() - stage_start_time).total_seconds()
            self.stage_results.append({
                'stage': stage_idx + 1,
                'stocks': len(stage_stocks),
                'success': stage_success,
                'fail': stage_fail,
                'time': stage_elapsed
            })
            
            self._clear_cache()
            self._save_stage_checkpoint(stage_idx + 1, total_stages)
            
            total_elapsed = (datetime.now() - start_time).total_seconds()
            print(f"\n阶段 {stage_idx+1} 完成!")
            
            if stage_idx + 1 < total_stages:
                avg_time = total_elapsed / (stage_idx + 1)
                remaining = avg_time * (total_stages - stage_idx - 1)
                print(f"  预计剩余: {remaining:.1f}s ({remaining/60:.1f}分钟)")
        
        elapsed = (datetime.now() - start_time).total_seconds()
        self._print_summary(total, elapsed)
    
    def _print_summary(self, total, elapsed):
        """打印计算摘要"""
        print(f"\n{'='*60}")
        print(f"计算完成!")
        print(f"{'='*60}")
        print(f"总股票数: {total}")
        print(f"成功: {self.success_count} 只")
        print(f"失败: {self.fail_count} 只")
        if self.fail_list:
            print(f"失败列表: {self.fail_list[:10]}{'...' if len(self.fail_list) > 10 else ''}")
        print(f"总耗时: {elapsed:.1f} 秒 ({elapsed/60:.1f} 分钟)")
        if total > 0:
            print(f"平均每只: {elapsed/total:.2f} 秒")
        print(f"{'='*60}")
        
        if self.stage_results:
            print(f"\n阶段统计:")
            print(f"{'阶段':<8} {'股票数':<8} {'成功':<8} {'失败':<8} {'耗时(s)':<10}")
            print("-" * 50)
            for r in self.stage_results:
                print(f"{r['stage']:<8} {r['stocks']:<8} {r['success']:<8} {r['fail']:<8} {r['time']:<10.1f}")
        
        if self.fail_list:
            fail_df = pd.DataFrame({'失败股票': self.fail_list})
            fail_path = r'{}/data/全部因子数据/失败列表.xlsx'.format(self.path)
            fail_df.to_excel(fail_path, index=False)
            print(f"\n失败列表已保存至: {fail_path}")
    
    def cacal_all_stock_factor(self):
        """计算所有股票因子"""
        if not self.text:
            print("因子表为空，请检查因子表.json")
            return
        
        if self.use_multiprocess and self.max_workers > 1:
            self.cacal_all_stock_factor_multiprocess()
        else:
            self.cacal_all_stock_factor_single()
    
    def get_factor_data(self, stock='513100.SH'):
        """获取已计算的因子数据"""
        try:
            file_path = r'{}/data/全部因子数据/{}.parquet'.format(self.path, stock)
            if not os.path.exists(file_path):
                return pd.DataFrame()
            return pd.read_parquet(file_path, engine='pyarrow', use_threads=True)
        except:
            return pd.DataFrame()
    
    def get_all_factor_data(self):
        """获取所有已计算的因子数据"""
        data_path = r'{}/data/全部因子数据'.format(self.path)
        if not os.path.exists(data_path):
            return pd.DataFrame()
        
        all_data = []
        for file in os.listdir(data_path):
            if file.endswith('.parquet') and file != '失败列表.xlsx':
                try:
                    stock = file.replace('.parquet', '')
                    df = self.get_factor_data(stock)
                    if not df.empty:
                        df['stock'] = stock
                        all_data.append(df)
                except:
                    continue
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        return pd.DataFrame()
    
    def run_all_func(self):
        """运行完整流程"""
        print("="*60)
        print("小果因子计算系统 (超级优化版)")
        print("="*60)
        
        print("\n[1/2] 生成因子列表...")
        self.get_all_factor_table()
        
        print("\n[2/2] 计算所有股票因子...")
        self.cacal_all_stock_factor()
        
        print("\n全部完成!")
        #下载一个因子的例子
        df=self.get_factor_data('513100.SH')[-10:]
        df['date']=pd.to_datetime(df['date'])
        df['date']=df['date'].apply(lambda x:str(x)[:10])
        df.to_json(r'{}/data/因子例子参考/因子例子参考.json'.format(self.path),orient='records',force_ascii=False)
        df.to_excel(r'{}/data/因子例子参考/因子例子参考.xlsx'.format(self.path))

if __name__ == '__main__':
    # ========== 强制重新计算所有股票（覆盖最新） ==========
    api = xg_factor_trader(
        max_workers=4,          # 进程数
        verbose=False,          # 是否显示详细信息
        use_multiprocess=True,  # 多进程模式
        chunk_size=100,         # 每批处理100只
        stage_size=100,         # 每阶段处理100只后清理缓存
        use_async_io=True,      # 使用异步IO
        start_date='20240101',
        force_recalc=True       # 🔥 强制重算模式：覆盖计算全部股票
    )
    api.run_all_func()
   
    df=api.get_factor_data('513100.SH')[-10:]
    df['date']=pd.to_datetime(df['date'])
    df['date']=df['date'].apply(lambda x:str(x)[:10])
    df.to_json(r'data/因子例子参考/因子例子参考.json',orient='records',force_ascii=False)
    df.to_excel(r'data/因子例子参考/因子例子参考.xlsx')
    


    
    
    