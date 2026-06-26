"""
Tushare 数据接口适配器（选股系统用）
必须用自定义初始化方式，否则 token 无效
"""

import tushare as ts
import pandas as pd


TOKEN = '676658a3dc1be0f7b5b2c884777d325f133b1f6f6973d4caa61b6476f854'
_http_url = 'http://140.143.209.128:5000'


def _get_pro():
    """获取初始化好的 pro 对象"""
    pro = ts.pro_api(TOKEN)
    pro._DataApi__token = TOKEN
    pro._DataApi__http_url = _http_url
    return pro


def get_quote_history_ts(code: str, start_date: str = '20200101', end_date: str = '20500101') -> pd.DataFrame | None:
    """
    用 tushare 拉取日线数据
    code: 6位股票代码，如 '000045' 或 '600350'
    返回: DataFrame（wyckoff_engine 兼容格式）
    """
    code = str(code).strip()
    if code.startswith(('0', '3')):
        ts_code = f'{code}.SZ'
    elif code.startswith('6'):
        ts_code = f'{code}.SH'
    else:
        ts_code = f'{code}.BJ'

    try:
        pro = _get_pro()
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        if df is None or len(df) == 0:
            return None

        df = df.rename(columns={
            'trade_date': '日期',
            'ts_code': '股票代码',
            'open': '开盘',
            'high': '最高',
            'low': '最低',
            'close': '收盘',
            'vol': '成交量',
            'amount': '成交额',
        })

        df = df.sort_values('日期').reset_index(drop=True)
        for col in ['开盘', '最高', '最低', '收盘', '成交量', '成交额']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.dropna(subset=['收盘', '最高', '最低', '成交量'])
        return df

    except Exception:
        return None
