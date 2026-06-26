"""
baostock 数据接口适配器（选股系统用）
"""

import baostock as bs
import pandas as pd


def get_quote_history_bs(code: str, start_date: str = '2020-01-01', end_date: str = '2050-01-01') -> tuple[pd.DataFrame | None, str]:
    """返回 (DataFrame, stock_name)"""
    code = str(code).strip()
    if code.startswith(('0', '3')):
        bs_code = f'sz.{code}'
    elif code.startswith('6'):
        bs_code = f'sh.{code}'
    else:
        bs_code = f'bj.{code}'

    lg = bs.login()
    if lg.error_code != '0':
        bs.logout()
        return None, code

    rs = bs.query_history_k_data_plus(
        bs_code,
        'date,code,open,high,low,close,volume,amount',
        start_date=start_date,
        end_date=end_date,
        frequency='d'
    )
    if rs.error_code != '0':
        bs.logout()
        return None, code

    data = []
    while rs.error_code == '0' and rs.next():
        data.append(rs.get_row_data())
    bs.logout()

    if not data:
        return None, code

    df = pd.DataFrame(data, columns=rs.fields)
    df = df.rename(columns={
        'date': '日期', 'code': '股票代码',
        'open': '开盘', 'high': '最高', 'low': '最低',
        'close': '收盘', 'volume': '成交量', 'amount': '成交额',
    })
    for col in ['开盘', '最高', '最低', '收盘', '成交量', '成交额']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['收盘', '最高', '最低', '成交量'])
    df = df.reset_index(drop=True)
    return df, code
