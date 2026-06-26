"""
Tushare 数据接口适配器
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


def get_quote_history_ts(code: str, start_date: str = '20200101', end_date: str = '20500101') -> tuple[pd.DataFrame | None, str]:
    """
    用 tushare 拉取日线数据
    code: 6位股票代码，如 '000045' 或 '600350'
    返回: (DataFrame, stock_name)
    """
    code = str(code).strip()

    # tushare 代码后缀
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
            return None, code

        # tushare 返回列: ts_code, trade_date, open, high, low, close, vol, amount
        # 重命名为 wyckoff_engine 兼容的中文列名
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

        # 按日期升序排列（tushare 默认是降序）
        df = df.sort_values('日期').reset_index(drop=True)

        # 数值类型
        for col in ['开盘', '最高', '最低', '收盘', '成交量', '成交额']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df = df.dropna(subset=['收盘', '最高', '最低', '成交量'])
        return df, code

    except Exception as e:
        return None, code
