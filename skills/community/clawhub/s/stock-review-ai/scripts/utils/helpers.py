import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Union, List, Dict, Any, Callable
import re
import os
import time
import json
from datetime import datetime, timedelta
import requests
from functools import wraps

# ========== 数值格式化 ==========

def format_value(value) -> str:
    """格式化数值为亿元/万元"""
    if pd.isna(value):
        return str(value)
    try:
        num = float(value)
        if num >= 1e8:
            return f"{num / 1e8:.2f}亿"
        elif num >= 1e4:
            return f"{num / 1e4:.2f}万"
        else:
            return f"{num:.2f}"
    except:
        return str(value)

def format_volume(value) -> str:
    """格式化成交额（别名）"""
    return format_value(value)

def format_percentage(value, digits: int = 2) -> str:
    """格式化为百分比"""
    if pd.isna(value):
        return "-"
    try:
        num = float(value)
        return f"{num:+.{digits}f}%"
    except:
        return str(value)

def format_market_cap(value) -> str:
    """格式化市值"""
    return format_value(value)

# ========== 文件操作 ==========

def ensure_dir(path: Union[str, Path]) -> Path:
    """确保目录存在"""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def safe_filename(text: str, max_length: int = 200) -> str:
    """生成安全的文件名"""
    # 移除非法字符
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    # 替换空格
    text = re.sub(r'\s+', '_', text)
    # 限制长度
    return text[:max_length]

def load_csv_with_retry(file_path: Union[str, Path], 
                       retries: int = 3, 
                       delay: float = 1,
                       **kwargs) -> Optional[pd.DataFrame]:
    """带重试的CSV加载"""
    file_path = Path(file_path)
    for i in range(retries):
        try:
            if file_path.exists():
                return pd.read_csv(file_path, dtype={'代码': str}, **kwargs)
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(delay)
    return None

def save_csv_with_backup(df: pd.DataFrame, 
                        file_path: Union[str, Path],
                        backup: bool = True,
                        **kwargs) -> Path:
    """保存CSV并可选创建备份"""
    file_path = Path(file_path)
    
    if backup and file_path.exists():
        backup_path = file_path.with_suffix(f'.bak{file_path.suffix}')
        file_path.rename(backup_path)
    
    df.to_csv(file_path, index=False, encoding="utf-8-sig", **kwargs)
    return file_path

# ========== DataFrame处理 ==========

def df_to_markdown(df: pd.DataFrame, max_col_width: int = 30) -> str:
    """DataFrame转Markdown表格"""
    if df.empty:
        return "暂无数据"
    
    display_df = df.copy()
    for col in display_df.columns:
        if display_df[col].dtype == 'object':
            display_df[col] = display_df[col].astype(str).str[:max_col_width]
    
    return display_df.to_markdown(index=False, tablefmt="pipe")

def reorder_dataframe(df: pd.DataFrame, priority_cols: List[str]) -> pd.DataFrame:
    """重新排序DataFrame列"""
    df = df.copy()
    # 移除序号列
    df = df.drop(columns=['序号', 'index', 'level_0'], errors='ignore')
    
    # 获取现有列
    existing_priority = [c for c in priority_cols if c in df.columns]
    other_cols = [c for c in df.columns if c not in existing_priority]
    
    # 重新排序
    new_order = existing_priority + other_cols
    return df[new_order]

def rename_zt_values(df: pd.DataFrame) -> pd.DataFrame:
    """重命名涨停相关值"""
    if '涨停统计' in df.columns:
        for idx, row in df.iterrows():
            val = row['涨停统计']
            if pd.notna(val) and isinstance(val, str) and '/' in val:
                cal_day, cont_day = val.split('/')
                if cal_day == '1':
                    df.loc[idx, '涨停统计'] = "首板"
                else:
                    df.loc[idx, '涨停统计'] = f"{cal_day}天{cont_day}板"
    return df

# ========== 日期处理 ==========

def parse_date(date_str: str, format: str = "%Y%m%d") -> Optional[datetime]:
    """解析日期字符串"""
    try:
        return datetime.strptime(date_str, format)
    except:
        return None

def is_trading_day(date: Union[str, datetime]) -> bool:
    """判断是否为交易日（简化版）"""
    if isinstance(date, str):
        date = parse_date(date)
    if not date:
        return False
    
    # 周一至周五为交易日
    return date.weekday() < 5

def get_latest_trading_day(base_date: Optional[Union[str, datetime]] = None,
                          max_back: int = 10) -> str:
    """获取最近的交易日"""
    if base_date is None:
        base_date = datetime.now()
    elif isinstance(base_date, str):
        base_date = parse_date(base_date)
    
    for i in range(max_back):
        check_date = base_date - timedelta(days=i)
        if is_trading_day(check_date):
            return check_date.strftime("%Y%m%d")
    
    return base_date.strftime("%Y%m%d")

# ========== 网络请求 ==========

def fetch_with_retry(fetch_func: Callable, 
                    retries: int = 3, 
                    delay: float = 1,
                    backoff: float = 2,
                    **kwargs) -> Any:
    """带重试的获取函数"""
    last_error = None
    for i in range(retries):
        try:
            return fetch_func(**kwargs)
        except Exception as e:
            last_error = e
            if i < retries - 1:
                time.sleep(delay * (backoff ** i))
    raise last_error

def make_request(url: str, 
                method: str = 'GET',
                headers: Optional[Dict] = None,
                timeout: int = 30,
                **kwargs) -> Optional[requests.Response]:
    """发送HTTP请求"""
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=timeout, **kwargs)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, timeout=timeout, **kwargs)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response
    except Exception as e:
        print(f"Request failed: {e}")
        return None

# ========== 股票代码处理 ==========

def normalize_stock_code(code: str) -> str:
    """规范化股票代码（确保6位）"""
    code = str(code).strip()
    # 移除可能的前缀
    code = re.sub(r'^(sh|sz|SH|SZ)', '', code)
    # 补齐6位
    return code.zfill(6)[-6:]

def add_market_prefix(code: str) -> str:
    """添加市场前缀"""
    code = normalize_stock_code(code)
    if code.startswith('6'):
        return f"SH{code}"
    elif code.startswith(('0', '3')):
        return f"SZ{code}"
    else:
        return code

# ========== 其他工具 ==========

def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """将列表分块"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def merge_dicts(dict1: Dict, dict2: Dict, deep: bool = True) -> Dict:
    """合并字典"""
    result = dict1.copy()
    for key, value in dict2.items():
        if deep and isinstance(value, dict) and key in result and isinstance(result[key], dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result

def safe_get(obj: Any, *keys, default: Any = None) -> Any:
    """安全获取嵌套字典/对象的值"""
    for key in keys:
        if isinstance(obj, dict):
            obj = obj.get(key)
        elif hasattr(obj, key):
            obj = getattr(obj, key)
        else:
            return default
        
        if obj is None:
            return default
    return obj

# ========== 装饰器 ==========

def retry(max_retries: int = 3, delay: float = 1, backoff: float = 2):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if i < max_retries - 1:
                        time.sleep(delay * (backoff ** i))
            raise last_error
        return wrapper
    return decorator

def log_execution(logger=None):
    """日志执行装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                logger = get_default_logger()
            
            logger.debug(f"Executing {func.__name__}")
            start = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start
                logger.debug(f"Completed {func.__name__} in {elapsed:.2f}s")
                return result
            except Exception as e:
                elapsed = time.time() - start
                logger.error(f"Failed {func.__name__} after {elapsed:.2f}s: {e}")
                raise
        return wrapper
    return decorator