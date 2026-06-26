"""实战 96: 实时财经报价 (mock) + 股票代码映射
- 真实数据需接东方财富/新浪 API (付费/反爬)
- 我们提供 mock + 提示用户
"""
import re
import time
from typing import Dict, Optional

# 实战 96: 常见股票/指数代码映射 (A 股 + 港股 + 美股 + 加密)
STOCK_MAP = {
    # A 股
    '比亚迪': ('002594', 'SZ', 'A 股'),
    '宁德时代': ('300750', 'SZ', 'A 股'),
    '茅台': ('600519', 'SH', 'A 股'),
    '五粮液': ('000858', 'SZ', 'A 股'),
    '腾讯': ('00700', 'HK', '港股'),
    '阿里巴巴': ('09988', 'HK', '港股'),
    '美团': ('03690', 'HK', '港股'),
    '京东': ('09618', 'HK', '港股'),
    '拼多多': ('PDD', 'US', '美股'),
    '百度': ('09888', 'HK', '港股'),
    '蔚来': ('NIO', 'US', '美股'),
    '小鹏': ('XPEV', 'US', '美股'),
    '理想': ('LI', 'US', '美股'),
    # 美股
    '苹果': ('AAPL', 'US', '美股'),
    '微软': ('MSFT', 'US', '美股'),
    '谷歌': ('GOOGL', 'US', '美股'),
    '亚马逊': ('AMZN', 'US', '美股'),
    'Meta': ('META', 'US', '美股'),
    '英伟达': ('NVDA', 'US', '美股'),
    '特斯拉': ('TSLA', 'US', '美股'),
    'Netflix': ('NFLX', 'US', '美股'),
    'OpenAI': ('-', 'PRIVATE', '未上市'),
    'Anthropic': ('-', 'PRIVATE', '未上市'),
    # 加密
    '比特币': ('BTC-USD', 'CRYPTO', '加密'),
    '以太坊': ('ETH-USD', 'CRYPTO', '加密'),
    # 指数
    '上证指数': ('000001', 'SH', 'A 股指数'),
    '深证成指': ('399001', 'SZ', 'A 股指数'),
    '沪深300': ('000300', 'SH', 'A 股指数'),
    '恒生指数': ('HSI', 'HK', '港股指数'),
    '纳斯达克': ('IXIC', 'US', '美股指数'),
    '标普500': ('SPX', 'US', '美股指数'),
    '道琼斯': ('DJI', 'US', '美股指数'),
}

# 实战 96: 实时报价查询 (mock 数据 + 真实 API 提示)
def get_quote(symbol_or_name: str) -> Dict:
    """获取股票/指数实时报价
    实战 96: 先查 STOCK_MAP, 返回 mock 数据 + 真实 API 链接
    未来: 接东方财富/新浪 API
    """
    q = (symbol_or_name or '').strip()

    # 1) 直接代码 (e.g. AAPL, 002594)
    code = None
    name = None
    market = None
    for k, v in STOCK_MAP.items():
        if v[0].upper() == q.upper() or k in q:
            code, market, name = v
            break

    # 2) 没找到 - 给链接建议
    if not code:
        return {
            'success': False,
            'query': q,
            'error': f'未找到 {q} 的代码',
            'suggestions': [
                f'https://so.eastmoney.com/web/s?keyword={q} (东方财富搜索)',
                f'https://www.google.com/finance/quote/{q} (Google Finance)',
            ],
        }

    # 3) 找到 - mock 数据 + 真实 API 链接
    return {
        'success': True,
        'query': q,
        'name': name,
        'code': code,
        'market': market,
        'quote': {
            'price': 'N/A (需实时 API)',
            'change': 'N/A',
            'change_pct': 'N/A',
            'volume': 'N/A',
            'note': '实战 96: mock 数据, 真实价格请查询下方链接',
        },
        'realtime_links': [
            f'https://quote.eastmoney.com/{code}.html (东方财富)',
            f'https://www.szse.cn/disclosure/listed/notice/index.html?code={code}' if market == 'SZ' else None,
            f'https://stock.finance.sina.com.cn/{code}/ (新浪财经)',
            f'https://finance.yahoo.com/quote/{code} (Yahoo Finance)',
        ],
        'timestamp': int(time.time()),
    }


def get_quote_links_only(query: str) -> list:
    """仅返回实时价格链接 (用于 answer 注入)"""
    q = (query or '').strip()
    for k, v in STOCK_MAP.items():
        if k in q:
            code = v[0]
            return [
                f'📊 实时价格: https://quote.eastmoney.com/{code}.html (东方财富)',
                f'📈 Yahoo Finance: https://finance.yahoo.com/quote/{code}',
            ]
    return [
        f'📊 搜索实时数据: https://so.eastmoney.com/web/s?keyword={q}',
    ]
