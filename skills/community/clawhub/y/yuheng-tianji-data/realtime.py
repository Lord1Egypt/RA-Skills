"""
天玑实时行情接口
数据源：腾讯 qt.gtimg.cn（无需登录，免费实时）
格式：Shenzhen/SH前缀 + 6位代码
"""
import urllib.request
from typing import Optional

def get_realtime(stock_code: str) -> Optional[dict]:
    """
    获取单只股票实时行情

    Args:
        stock_code: 股票代码，如 '000791'（自动判断交易所）
                    支持格式：sz000791, sh600938, 000001(自动判断)

    Returns:
        dict: {
            'name': str,      # 股票名称
            'price': float,   # 当前价
            'change_pct': float, # 涨跌幅%
            'change_abs': float,  # 涨跌额
            'open': float,    # 开盘价
            'high': float,    # 最高价
            'low': float,     # 最低价
            'volume': int,     # 成交量（手）
            'turnover': float, # 成交额（元）
            'time': str,       # 更新时间 HH:MM:SS
            'status': str      # 交易状态
        }
    """
    code = stock_code.strip().lower()
    if not code.startswith(('sz', 'sh')):
        # 6位数代码：0/3开头→深交所，6开头→上交所
        # 000001特殊：sz=平安银行，sh=上证指数
        if stock_code == '000001':
            code = 'sh000001'  # 上证指数
        elif stock_code.startswith(('0', '3')) and len(stock_code) == 6:
            code = 'sz' + stock_code
        else:
            code = 'sh' + stock_code

    url = f'https://qt.gtimg.cn/q={code}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            raw = r.read().decode('gbk', errors='replace').strip()
            return _parse_tencent(raw, code)
    except Exception as e:
        return None


def get_batch(stock_codes: list[str]) -> dict[str, dict]:
    """批量获取实时行情"""
    codes = []
    for sc in stock_codes:
        sc = sc.strip().lower()
        if not sc.startswith(('sz', 'sh')):
            if sc == '000001':
                sc = 'sh000001'
            elif sc.startswith(('0', '3')) and len(sc) == 6:
                sc = 'sz' + sc
            else:
                sc = 'sh' + sc
        codes.append(sc)

    codes_str = ','.join(codes)
    url = f'https://qt.gtimg.cn/q={codes_str}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    results = {}
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read().decode('gbk', errors='replace').strip()
            lines = raw.split('\n')
            for line, code in zip(lines, codes):
                d = _parse_tencent(line, code)
                if d:
                    ticker = code[2:].upper()
                    results[ticker] = d
    except Exception:
        pass

    return results


def _parse_tencent(raw: str, code: str) -> Optional[dict]:
    """解析腾讯行情数据格式"""
    try:
        # 腾讯行情格式（按 ~ 分割）
        # [3]=现价 [4]=昨收 [5]=开盘 [6]=成交量(手)
        # [31]=涨跌额 [32]=涨跌幅% [33]=最高 [34]=最低 [37]=成交额(万元)
        parts = raw.split('~')
        if len(parts) < 38:
            return None

        volume_lots = int(parts[6])
        turnover_wan = float(parts[37]) if parts[37] else 0.0
        ts = parts[30]
        time_str = f"{ts[8:10]}:{ts[10:12]}:{ts[12:14]}"

        return {
            'name': parts[1],
            'code': parts[2],
            'price': float(parts[3]),
            'prev_close': float(parts[4]),
            'open': float(parts[5]),
            'high': float(parts[33]),
            'low': float(parts[34]),
            'volume_lots': volume_lots,
            'turnover_yi': turnover_wan / 10000,
            'change_abs': float(parts[31]),
            'change_pct': float(parts[32]),
            'time': time_str,
            'raw_time': ts,
        }
    except (ValueError, IndexError):
        return None


# 常用股票代码对照
STOCK_CODES = {
    '000791': 'sz000791',  # 甘肃能源
    '600938': 'sh600938',  # 中海油
    '601857': 'sh601857',  # 中石油
    '600726': 'sh600726',  # 华电辽能
    '600887': 'sh600887',  # 伊利股份
    '000001': 'sh000001',  # 上证指数
    '399001': 'sz399001',  # 深证成指
    '399006': 'sz399006',  # 创业板指
}


if __name__ == '__main__':
    # 测试
    results = get_batch(['000791', '600938', '601857', '000001'])
    for ticker, d in results.items():
        if d:
            print(f"{d['name']}({ticker}): {d['price']}元 "
                  f"{d['change_pct']:+.2f}% "
                  f"高{d['high']} 低{d['low']} 成交{d['turnover']/1e8:.2f}亿")
        else:
            print(f"{ticker}: 获取失败")
