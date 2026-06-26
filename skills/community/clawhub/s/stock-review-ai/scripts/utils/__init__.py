import logging
from typing import Dict, Any, Optional, Union, List
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

# 从各个模块导入公开的函数和类
from .logger import (
    setup_logger,
    get_logger,
    LoggerManager
)

# 定义包的公开接口
__all__ = [
    # 日志相关
    "setup_logger",
    "get_logger",
    "LoggerManager",
    
    # 数值格式化
    "format_value",
    "format_volume",
    "format_percentage",
    "format_market_cap",
    
    # 文件操作
    "ensure_dir",
    "safe_filename",
    "load_csv_with_retry",
    "save_csv_with_backup",
    
    # DataFrame处理
    "df_to_markdown",
    "reorder_dataframe",
    "rename_zt_values",
    
    # 日期处理
    "parse_date",
    "get_trading_dates",
    "is_trading_day",
    "get_latest_trading_day",
    
    # 网络请求
    "fetch_with_retry",
    "make_request",
    
    # 股票代码处理
    "normalize_stock_code",
    "add_market_prefix",
    
    # 其他工具
    "chunk_list",
    "merge_dicts",
    "safe_get"
]

# 包版本
__version__ = "1.0.0"

# 包级别的默认日志配置
_default_logger = None

def get_default_logger():
    """获取默认日志记录器"""
    global _default_logger
    if _default_logger is None:
        _default_logger = setup_logger("stock_review.utils")
    return _default_logger

# 包初始化时的日志
logger = get_default_logger()
logger.debug(f"Utils package initialized (v{__version__})")

# 便捷函数：一次性格式化多个数值列
def format_dataframe_columns(df: pd.DataFrame, 
                            volume_cols: Optional[List[str]] = None,
                            percent_cols: Optional[List[str]] = None) -> pd.DataFrame:
    """
    批量格式化DataFrame中的数值列
    
    Args:
        df: 输入DataFrame
        volume_cols: 需要格式化为成交额/市值的列名列表
        percent_cols: 需要格式化为百分比的列名列表
    
    Returns:
        格式化后的DataFrame
    """
    result = df.copy()
    
    if volume_cols:
        for col in volume_cols:
            if col in result.columns:
                result[col] = result[col].apply(format_value)
    
    if percent_cols:
        for col in percent_cols:
            if col in result.columns:
                result[col] = result[col].apply(format_percentage)
    
    return result

# 添加到公开接口
__all__.extend(["format_dataframe_columns"])

# 包级别的上下文管理器（可选）
class WorkingDirectory:
    """临时工作目录上下文管理器"""
    
    def __init__(self, path: Union[str, Path]):
        self.path = Path(path)
        self.original_cwd = None
    
    def __enter__(self):
        self.original_cwd = Path.cwd()
        os.chdir(self.path)
        logger.debug(f"Changed working directory to: {self.path}")
        return self.path
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.original_cwd)
        logger.debug(f"Restored working directory to: {self.original_cwd}")

__all__.append("WorkingDirectory")