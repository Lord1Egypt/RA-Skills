#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票行情查询脚本
支持 A 股、港股、美股，使用多数据源轮询负载均衡
"""

import sys
import io

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from data_sources import fetch_stock_price, DataSourceManager, get_manager


def format_output(data):
    """格式化输出"""
    if 'error' in data:
        error_msg = data['error']
        if 'details' in data:
            error_msg += f" ({', '.join(data['details'])})"
        return f"❌ {error_msg}"

    trend = "📈" if data['change'] > 0 else "📉" if data['change'] < 0 else "➖"
    source_tag = f"[{data.get('source', 'unknown')}]"

    return f"""
{trend} **{data['name']}** ({data['symbol']}) {source_tag}

| 项目 | 数值 |
|------|------|
| 当前价 | ¥{data['current']:.2f} |
| 涨跌 | {data['change']:+.2f} ({data['change_pct']:+.2f}%) |
| 今开 | ¥{data['open']:.2f} |
| 最高 | ¥{data['high']:.2f} |
| 最低 | ¥{data['low']:.2f} |
| 昨收 | ¥{data['prev_close']:.2f} |
| 成交量 | {data['volume']:,} 股 |
| 成交额 | ¥{data['turnover']/10000:.1f} 万 |
| 更新时间 | {data.get('update_time', '-')} |
""".strip()


def main():
    if len(sys.argv) < 2:
        print("用法：python stock_fetch.py <股票代码> [--json]")
        print("示例：python stock_fetch.py 600519")
        print("      python stock_fetch.py 600519 --json")
        sys.exit(1)

    symbol = sys.argv[1]
    data = fetch_stock_price(symbol)

    if '--json' in sys.argv:
        import json
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_output(data))


if __name__ == '__main__':
    main()