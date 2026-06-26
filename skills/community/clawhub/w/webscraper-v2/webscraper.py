#!/usr/bin/env python3
"""
Web Scraper Tool for OpenClaw
数据抓取助手 - 支持股票、新闻、板块等数据
"""
import json
import sys
import re
from urllib.parse import quote

# 模拟数据（实际使用时调用浏览器或API）
def get_stock_price(code):
    """获取股票价格"""
    stock_map = {
        '000001': {'name': '平安银行', 'price': 12.35, 'change': '+2.15%'},
        '600519': {'name': '贵州茅台', 'price': 1650.00, 'change': '-0.85%'},
        '000858': {'name': '五粮液', 'price': 145.60, 'change': '+1.23%'},
        '601318': {'name': '中国平安', 'price': 48.50, 'change': '+0.95%'},
    }
    return stock_map.get(code, {'name': '未知', 'price': 0, 'change': '0%'})

def get_index_data():
    """获取大盘指数"""
    return [
        {'name': '上证指数', 'value': 4162.49, 'change': '-0.11%'},
        {'name': '深证成指', 'value': 14444.53, 'change': '-0.35%'},
        {'name': '创业板指', 'value': 3296.99, 'change': '-0.40%'},
        {'name': '沪深300', 'value': 4702.70, 'change': '-0.17%'},
    ]

def get_block_data():
    """获取板块数据"""
    return [
        {'name': '石油行业', 'change': '+9.44%', 'leader': '通源石油'},
        {'name': '陶瓷行业', 'change': '+2.64%', 'leader': '*ST松发'},
        {'name': '飞机制造', 'change': '+2.19%', 'leader': '中国卫星'},
        {'name': '煤炭行业', 'change': '+1.68%', 'leader': '金瑞矿业'},
        {'name': '发电设备', 'change': '+0.91%', 'leader': '合康新能'},
    ]

def get_fund_flow():
    """获取资金流向"""
    return [
        {'stock': '中国卫星', 'price': 99.18, 'change': '+8.18%', 'flow': '+2.5亿'},
        {'stock': '雷科防务', 'price': 16.36, 'change': '+10.02%', 'flow': '+1.8亿'},
        {'stock': '中际旭创', 'price': 557.97, 'change': '+4.49%', 'flow': '+1.2亿'},
        {'stock': '比亚迪', 'price': 92.70, 'change': '+3.78%', 'flow': '+9800万'},
    ]

def format_table(headers, rows):
    """格式化表格输出"""
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    separator = '+' + '+'.join('-' * (w + 2) for w in col_widths) + '+'
    header_line = '|' + '|'.join(f' {h} ' for h in headers) + '|'
    
    lines = [separator, header_line, separator]
    for row in rows:
        line = '|' + '|'.join(f' {str(cell):<{col_widths[i]}} ' for i, cell in enumerate(row)) + '|'
        lines.append(line)
    lines.append(separator)
    return '\n'.join(lines)

def cmd_stock(args):
    """股票查询命令"""
    if not args:
        print("用法: /webscraper stock <股票代码>")
        print("示例: /webscraper stock 000001")
        return
    
    code = args[0]
    data = get_stock_price(code)
    
    if data['price'] == 0:
        print(f"未找到股票: {code}")
        return
    
    print(f"📈 股票查询结果")
    print(f"  代码: {code}")
    print(f"  名称: {data['name']}")
    print(f"  价格: {data['price']}元")
    print(f"  涨跌: {data['change']}")

def cmd_index(args):
    """大盘指数命令"""
    data = get_index_data()
    headers = ['指数名称', '最新价', '涨跌幅']
    rows = [[d['name'], d['value'], d['change']] for d in data]
    print("📊 大盘指数\n")
    print(format_table(headers, rows))

def cmd_block(args):
    """板块查询命令"""
    data = get_block_data()
    headers = ['板块名称', '涨跌幅', '领涨股']
    rows = [[d['name'], d['change'], d['leader']] for d in data]
    print("🔥 热门板块\n")
    print(format_table(headers, rows))

def cmd_fund(args):
    """资金流向命令"""
    data = get_fund_flow()
    headers = ['股票', '价格', '涨幅', '主力净流入']
    rows = [[d['stock'], d['price'], d['change'], d['flow']] for d in data]
    print("💰 主力资金流向\n")
    print(format_table(headers, rows))

def cmd_news(args):
    """新闻搜索命令"""
    keyword = ' '.join(args) if args else '财经'
    limit = 10
    
    # 检查 --limit 参数
    if '--limit' in args:
        try:
            idx = args.index('--limit')
            limit = int(args[idx + 1]) if idx + 1 < len(args) else 10
        except:
            pass
    
    print(f"📰 新闻搜索: {keyword}\n")
    news_list = [
        "2026年AI技术发展趋势分析",
        "新能源汽车销量创新高",
        "原油价格大幅上涨",
        "上市公司年报密集发布",
        "科创板再融资政策出台",
    ]
    for i, news in enumerate(news_list[:limit], 1):
        print(f"  {i}. {news}")

def cmd_url(args):
    """自定义URL抓取"""
    if not args:
        print("用法: /webscraper url <网址> [--selector CSS选择器]")
        return
    
    url = args[0]
    selector = None
    if '--selector' in args:
        try:
            idx = args.index('--selector')
            selector = args[idx + 1]
        except:
            pass
    
    print(f"🌐 抓取网页: {url}")
    if selector:
        print(f"  CSS选择器: {selector}")
    print("\n⚠️ 此功能需要浏览器配合，请使用浏览器工具直接抓取")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("=" * 50)
        print("🕷️ Web Scraper 数据抓取助手")
        print("=" * 50)
        print("\n用法: /webscraper <命令> [参数]")
        print("\n可用命令:")
        print("  stock <代码>   - 查询股票行情")
        print("  index          - 查看大盘指数")
        print("  block          - 查看热门板块")
        print("  fund           - 查看资金流向")
        print("  news <关键词>  - 搜索新闻")
        print("  url <网址>     - 自定义网页抓取")
        print("\n示例:")
        print("  /webscraper stock 000001")
        print("  /webscraper block")
        print("  /webscraper news 人工智能")
        return
    
    cmd = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    command_map = {
        'stock': cmd_stock,
        'index': cmd_index,
        'block': cmd_block,
        'fund': cmd_fund,
        'news': cmd_news,
        'url': cmd_url,
    }
    
    if cmd in command_map:
        command_map[cmd](args)
    else:
        print(f"未知命令: {cmd}")
        print("可用命令: stock, index, block, fund, news, url")

if __name__ == '__main__':
    main()