"""
股票分析统一工具库
封装API调用、数据获取等通用功能，供所有策略脚本使用

数据来源：Tushare Pro（https://tushare.pro）
  - 使用前需在 config.json 中填入个人 token，或设置环境变量 TUSHARE_TOKEN
  - 官方文档：https://tushare.pro/document/2

更新记录：
  2026-04-01 初始版本
  2026-04-02 优化：添加重试机制、缓存支持、get_daily_basic函数、错误日志级别控制
  2026-04-12 安全修复：改为直连 Tushare 官方 API（http://api.tushare.pro）
"""

import os
import requests
import json
import pandas as pd
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from functools import lru_cache

# ── Tushare 官方 API 端点（唯一外部请求地址）──────────────────────────────
TUSHARE_API_URL = "http://api.tushare.pro"
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 2
RETRY_DELAY = 0.5

# 日志配置（可通过 set_log_level 调整）
logger = logging.getLogger("stock_utils")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s [%(name)s] %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)  # 默认仅显示警告及以上


def set_log_level(level: str = "WARNING"):
    """设置日志级别，可选 DEBUG/INFO/WARNING/ERROR"""
    logger.setLevel(getattr(logging, level.upper(), logging.WARNING))


def _get_token() -> str:
    """
    按优先级读取 Tushare Token：
      1. 环境变量 TUSHARE_TOKEN
      2. 当前目录 config.json 中的 token 字段
    """
    token = os.environ.get("TUSHARE_TOKEN", "")
    if not token or token == "YOUR_TUSHARE_TOKEN_HERE":
        cfg_path = os.path.join(os.path.dirname(__file__), "config.json")
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            token = cfg.get("token", "")
        except Exception:
            pass
    if not token or token == "YOUR_TUSHARE_TOKEN_HERE":
        raise RuntimeError(
            "Tushare token 未配置。请在 config.json 中填入 token，"
            "或设置环境变量 TUSHARE_TOKEN。\n"
            "注册免费 token：https://tushare.pro/register"
        )
    return token


def call_api(api_name: str, params: Dict[str, Any], fields: str = "",
             retries: int = MAX_RETRIES) -> Optional[Dict[str, Any]]:
    """
    直连 Tushare Pro 官方 API（http://api.tushare.pro）
    
    Args:
        api_name: API名称（如'fina_indicator', 'daily'等）
        params:   API参数字典
        fields:   可选字段筛选（逗号分隔）
        retries:  失败重试次数
    
    Returns:
        返回 API 响应的 data 字段，失败返回 None
    
    请求格式（Tushare 标准）：
        POST http://api.tushare.pro
        Body: {"api_name": ..., "token": ..., "params": ..., "fields": ...}
    """
    try:
        token = _get_token()
    except RuntimeError as e:
        logger.error(str(e))
        return None

    payload: Dict[str, Any] = {
        "api_name": api_name,
        "token": token,
        "params": params,
    }
    if fields:
        payload["fields"] = fields

    headers = {"Content-Type": "application/json"}

    for attempt in range(retries + 1):
        try:
            response = requests.post(
                TUSHARE_API_URL,
                json=payload,
                headers=headers,
                timeout=DEFAULT_TIMEOUT,
            )
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    return result.get("data", {})
                else:
                    logger.debug(
                        f"API返回错误 [{api_name}]: "
                        f"code={result.get('code')}, msg={result.get('msg')}"
                    )
            else:
                logger.debug(f"HTTP错误 [{api_name}]: status={response.status_code}")
        except requests.exceptions.Timeout:
            logger.debug(f"API超时 [{api_name}] (attempt {attempt+1}/{retries+1})")
        except Exception as e:
            logger.debug(f"API调用异常 [{api_name}]: {e}")

        if attempt < retries:
            time.sleep(RETRY_DELAY * (attempt + 1))

    return None


def get_weekly_data(ts_code: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """
    获取周线数据
    
    Args:
        ts_code: 股票代码（如'000001.SZ'）
        start_date: 开始日期（YYYYMMDD）
        end_date: 结束日期（YYYYMMDD）
    
    Returns:
        DataFrame包含周线数据，失败返回None
    """
    params = {
        "ts_code": ts_code,
        "start_date": start_date,
        "end_date": end_date,
        "freq": "week"
    }
    
    data = call_api("stk_weekly_monthly", params)
    if data and "items" in data and len(data["items"]) > 0:
        df = pd.DataFrame(data["items"], columns=data["fields"])
        if "trade_date" in df.columns:
            df["trade_date"] = pd.to_datetime(df["trade_date"])
            return df.sort_values("trade_date").reset_index(drop=True)
    return None


def get_daily_data(ts_code: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """
    获取日线数据
    
    Args:
        ts_code: 股票代码
        start_date: 开始日期（YYYYMMDD）
        end_date: 结束日期（YYYYMMDD）
    
    Returns:
        DataFrame包含日线数据，失败返回None
    """
    params = {
        "ts_code": ts_code,
        "start_date": start_date,
        "end_date": end_date
    }
    
    data = call_api("daily", params)
    if data and "items" in data and len(data["items"]) > 0:
        df = pd.DataFrame(data["items"], columns=data["fields"])
        if "trade_date" in df.columns:
            df["trade_date"] = pd.to_datetime(df["trade_date"])
            return df.sort_values("trade_date").reset_index(drop=True)
    return None


def get_stock_list(list_status: str = "L", exclude_st: bool = True) -> List[Dict[str, Any]]:
    """
    获取股票列表
    
    Args:
        list_status: 上市状态（L-上市，D-退市，P-暂停）
        exclude_st: 是否排除ST/退市风险股票（默认True）
    
    Returns:
        股票列表，每个元素包含ts_code, name, industry, market等字段
    """
    params = {"list_status": list_status}
    fields = "ts_code,name,industry,market,area"
    
    data = call_api("stock_basic", params, fields)
    if data and "items" in data:
        items = data["items"]
        if exclude_st:
            # 过滤ST/*ST股票（name字段在index=1）
            items = [s for s in items if len(s) > 1 and "ST" not in str(s[1]).upper()]
        return items
    return []
def get_daily_basic(ts_code: str, start_date: str = None, end_date: str = None,
                    latest_only: bool = False) -> Optional[pd.DataFrame]:
    """
    获取每日指标数据（PE、PB、股息率、市值等）
    
    Args:
        ts_code: 股票代码
        start_date: 开始日期（YYYYMMDD），为空则取当月
        end_date: 结束日期（YYYYMMDD），为空则取今日
        latest_only: 是否只返回最新一条（返回dict）
    
    Returns:
        DataFrame 或最新一行 dict，失败返回None
    """
    if end_date is None:
        end_date = datetime.now().strftime("%Y%m%d")
    if start_date is None:
        start_date = datetime.now().replace(day=1).strftime("%Y%m%d")
    
    params = {"ts_code": ts_code, "start_date": start_date, "end_date": end_date}
    data = call_api("daily_basic", params)
    
    if data and "items" in data and len(data["items"]) > 0:
        df = pd.DataFrame(data["items"], columns=data["fields"])
        df = df.sort_values("trade_date", ascending=False).reset_index(drop=True)
        
        if latest_only:
            return df.iloc[0].to_dict()
        return df
    return None

def get_fina_indicator(ts_code: str, limit: int = 4, period: Optional[str] = None) -> Optional[pd.DataFrame]:
    """
    获取财务指标数据
    
    Args:
        ts_code: 股票代码
        limit: 获取最近几个季度/年度数据
        period: 特定期次（如'20240930'），如果指定则忽略limit
    
    Returns:
        DataFrame包含财务指标，失败返回None
    """
    params = {"ts_code": ts_code}
    
    if period:
        params["period"] = period
    else:
        params["limit"] = limit
    
    data = call_api("fina_indicator", params)
    if data and "items" in data and len(data["items"]) > 0:
        df = pd.DataFrame(data["items"], columns=data["fields"])
        if "end_date" in df.columns:
            df["end_date"] = pd.to_datetime(df["end_date"])
            return df.sort_values("end_date", ascending=False).reset_index(drop=True)
    return None


def get_income_data(ts_code: str, period: Optional[str] = None, limit: int = 4) -> Optional[pd.DataFrame]:
    """
    获取利润表数据
    
    Args:
        ts_code: 股票代码
        period: 特定期次（如'20240930'）
        limit: 获取最近几个季度数据
    
    Returns:
        DataFrame包含利润表数据，失败返回None
    """
    params = {"ts_code": ts_code}
    
    if period:
        params["period"] = period
    else:
        params["limit"] = limit
    
    data = call_api("income", params)
    if data and "items" in data and len(data["items"]) > 0:
        df = pd.DataFrame(data["items"], columns=data["fields"])
        if "end_date" in df.columns:
            df["end_date"] = pd.to_datetime(df["end_date"])
            return df.sort_values("end_date", ascending=False).reset_index(drop=True)
    return None


def get_date_before_days(days: int, date_format: str = "%Y%m%d") -> str:
    """
    获取N天前的日期字符串
    
    Args:
        days: 天数
        date_format: 日期格式
    
    Returns:
        格式化后的日期字符串
    """
    date = datetime.now() - timedelta(days=days)
    return date.strftime(date_format)


def get_date_before_years(years: int, date_format: str = "%Y%m%d") -> str:
    """
    获取N年前的日期字符串
    
    Args:
        years: 年数
        date_format: 日期格式
    
    Returns:
        格式化后的日期字符串
    """
    date = datetime.now() - timedelta(days=years * 365)
    return date.strftime(date_format)


def get_cashflow_data(ts_code: str, start_date: str = None, end_date: str = None,
                      period: str = None) -> Optional[pd.DataFrame]:
    """
    获取现金流量表数据
    
    Args:
        ts_code: 股票代码（含后缀）
        start_date: 开始日期（YYYYMMDD），默认3年前
        end_date: 结束日期（YYYYMMDD），默认昨天
        period: 财报期次（如20231231），空则取全部
    
    Returns:
        DataFrame 或 None
    """
    if start_date is None:
        start_date = get_date_before_years(3)
    if end_date is None:
        end_date = get_date_before_days(1)
    
    params = {
        "ts_code": ts_code,
        "start_date": start_date,
        "end_date": end_date,
    }
    if period:
        params["period"] = period
    
    data = call_api("cashflow", params)
    if not data or "items" not in data or len(data["items"]) < 1:
        return None
    
    df = pd.DataFrame(data["items"], columns=data["fields"])
    for date_col in ("period", "end_date", "report_date"):
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            df = df.sort_values(date_col, ascending=False).reset_index(drop=True)
            break
    return df


def get_holder_number(ts_code: str, limit: int = 8) -> Optional[pd.DataFrame]:
    """
    获取股东户数数据
    
    Args:
        ts_code: 股票代码（含后缀）
        limit: 最大期数
    
    Returns:
        DataFrame（end_date升序，含holdernumber列）或 None
    """
    params = {"ts_code": ts_code, "limit": limit}
    data = call_api("stk_holdernumber", params)
    if not data or "items" not in data or len(data["items"]) < 2:
        return None
    
    df = pd.DataFrame(data["items"], columns=data["fields"])
    if "holdernumber" not in df.columns or "end_date" not in df.columns:
        return None
    df = df.dropna(subset=["holdernumber", "end_date"])
    df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")
    df = df.sort_values("end_date", ascending=True).reset_index(drop=True)
    return df


def save_json_data(data: Any, filename: str, ensure_ascii: bool = False, indent: int = 2) -> bool:
    """
    保存数据到JSON文件
    
    Args:
        data: 要保存的数据
        filename: 文件名
        ensure_ascii: 是否确保ASCII编码
        indent: 缩进空格数
    
    Returns:
        成功返回True，失败返回False
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=ensure_ascii, indent=indent)
        print(f"数据已保存到: {filename}")
        return True
    except Exception as e:
        print(f"保存文件失败: {e}")
        return False


def load_json_data(filename: str) -> Any:
    """
    从JSON文件加载数据
    
    Args:
        filename: 文件名
    
    Returns:
        加载的数据，失败返回None
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"加载文件失败: {e}")
        return None


if __name__ == "__main__":
    # 测试函数
    print("测试统一工具库...")
    set_log_level("INFO")
    
    # 测试API调用
    print("\n1. 测试API调用:")
    data = call_api("stock_basic", {"list_status": "L"}, "ts_code,name")
    if data and "items" in data:
        print(f"   成功获取 {len(data['items'])} 只股票")
    else:
        print("   API调用失败")
    
    # 测试获取单只股票数据
    print("\n2. 测试获取财务指标:")
    df = get_fina_indicator("000001.SZ", limit=2)
    if df is not None and not df.empty:
        print(f"   成功获取数据，字段: {', '.join(df.columns[:5])}...")
        print(f"   最新ROE: {df.iloc[0].get('roe', 'N/A')}")
    else:
        print("   获取数据失败")
    
    # 测试每日指标
    print("\n3. 测试每日指标:")
    daily = get_daily_basic("000001.SZ", latest_only=True)
    if daily:
        print(f"   PE(TTM): {daily.get('pe_ttm', 'N/A')}")
        print(f"   PB: {daily.get('pb', 'N/A')}")
    else:
        print("   获取数据失败")
