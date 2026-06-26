
from datetime import datetime
import pandas as pd
import baostock as bs


def get_kline_data_baostock(stock_symbol, start_date, end_date, adjust="qfq"):
    """
    使用 baostock 获取 K 线数据
    
    Args:
        stock_symbol: 股票代码 (如 "600000" 或 "000927")
        start_date: 开始日期 YYYY-MM-DD 格式
        end_date: 结束日期 YYYY-MM-DD 格式
        adjust: 复权类型 qfq=前复权 hfq=后复权
    
    Returns:
        DataFrame 格式的股票数据
    """
    try:
        # 登录 baostock
        login_rs = bs.login()
        
        if login_rs.error_code != '0':
            print(f"❌ 登录失败：{login_rs.error_msg}")
            return None
        
        # 确定市场前缀
        if stock_symbol.startswith("0") or stock_symbol.startswith("3"):
            market = "sz"  # 深交所
        else:
            market = "sh"  # 上交所
        
        full_symbol = f"{market}.{stock_symbol}"
        
        # 日期使用 YYYY-MM-DD 格式 (Baostock 要求)
        # start_date_bs = start_date.replace("-", "")
        # end_date_bs = end_date.replace("-", "")
        start_date_bs = start_date
        end_date_bs = end_date
        
        # 复权标志
        adjust_flag = "3" if adjust == "qfq" else "2" if adjust == "hfq" else "1"
        
        # 获取历史 K 线数据
        fields = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg"
        rs = bs.query_history_k_data_plus(
            code=full_symbol,
            fields=fields,
            start_date=start_date_bs,
            end_date=end_date_bs,
            frequency="d",
            adjustflag=adjust_flag
        )
        
        if rs.error_code != '0':
            print(f"❌ 查询失败：{rs.error_msg}")
            bs.logout()
            return None
        
        data_list = []
        while rs.error_code == '0' and rs.next():
            data_list.append(rs.get_row_data())
        df = pd.DataFrame(data_list, columns=rs.fields)
        bs.logout()

        df = df[df['volume'].astype(str).str.strip() != '']
        type_mapping = {
            'code': 'str',
            'volume': 'int64'
        }

        df = df.astype(type_mapping)
        
        if len(df) == 0:
            return None
        
        # 处理日期列
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        
        # 确保数值列为 float
        numeric_cols = ['open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'turn', 'pctChg']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 重命名列并选择需要的列
        col_mapping = {
            'open': '开盘',
            'high': '最高', 
            'low': '最低',
            'close': '收盘',
            'volume': '成交量',
            'preclose': '昨收',
            'pctChg': '涨跌幅',
            'turn': '换手率'
        }
        df.rename(columns=col_mapping, inplace=True)
        
        # 排序并删除空值
        df.sort_index(inplace=True)
        df = df.dropna()
        
        print(f"✅ 成功通过 baostock 获取 {len(df)} 条数据")
        return df
        
    except Exception as e:
        print(f"❌ baostock 获取异常：{str(e)[:100]}")
        try:
            bs.logout()
        except:
            pass
    return None


if __name__== "__main__":
    l = get_kline_data_baostock("600249","2020-01-01","2026-04-01","")
    print(l)