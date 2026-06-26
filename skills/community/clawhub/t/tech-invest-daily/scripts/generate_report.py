#!/usr/bin/env python3
"""科技投资日报生成脚本"""
import subprocess, re, sys
from datetime import datetime

def fetch_url(url):
    result = subprocess.run(
        ['curl', '-s', '-L', '--max-time', '10', url],
        capture_output=True
    )
    return result.stdout.decode('utf-8', errors='ignore')

def fetch_cls_news():
    """抓财联社电报"""
    content = fetch_url('https://www.cls.cn/telegraph')
    # 提取新闻条目（时间+内容格式）
    items = re.findall(r'(\d{2}:\d{2}:\d{2})【([^】]+)】([^\n]+)', content)
    return items[:20]  # 取最新20条

def extract_companies(news_items):
    """从新闻中提取公司名和股票代码映射"""
    # 常见科技公司映射表
    company_map = {
        '英伟达': 'usNVDA', 'NVIDIA': 'usNVDA',
        '苹果': 'usAAPL', 'Apple': 'usAAPL',
        '微软': 'usMSFT', 'Microsoft': 'usMSFT',
        '谷歌': 'usGOOGL', 'Google': 'usGOOGL',
        '特斯拉': 'usTSLA', 'Tesla': 'usTSLA',
        '阿里巴巴': 'usBABA', '阿里': 'usBABA',
        '腾讯': 'hk00700',
        '百度': 'usBIDU',
        '中芯国际': 'hk00981',
        '中科曙光': 'sh603019',
        '海光信息': 'sh688041',
        '科大讯飞': 'sz002230',
        '潍柴动力': 'sz000338',
        '拓邦股份': 'sz002139',
        '九安医疗': 'sz002432',
        '绿的谐波': 'sh688017',
        '水晶光电': 'sz002273',
        '歌尔股份': 'sz002241',
        '比亚迪': 'sz002594',
        '小米': 'hk01810',
        '华为': None,  # 非上市
        'OpenAI': None,  # 非上市
        '月之暗面': None,  # 非上市
    }
    found = {}
    all_text = ' '.join([t + c for _, t, c in news_items])
    for name, code in company_map.items():
        if name in all_text and code:
            found[name] = code
    return found

def get_stock_prices(codes):
    """批量获取股价"""
    if not codes:
        return {}
    query = ','.join(codes)
    raw = subprocess.run(
        ['curl', '-s', f'http://qt.gtimg.cn/q={query}'],
        capture_output=True
    ).stdout.decode('gbk', errors='ignore')
    
    result = {}
    for line in raw.split('\n'):
        m = re.search(r'v_(\w+)="([^"]+)"', line)
        if m:
            code = m.group(1)
            f = m.group(2).split('~')
            if len(f) > 34:
                result[code] = {
                    'name': f[1], 'price': f[3], 'prev': f[4],
                    'change': f[31], 'pct': f[32],
                    'high': f[33], 'low': f[34]
                }
    return result

def generate_report(news_items, companies, prices):
    """生成报告文本"""
    date = datetime.now().strftime('%Y-%m-%d')
    lines = [f'# 📊 科技投资日报 · {date}\n']
    
    # 科技相关新闻
    tech_keywords = ['AI', '芯片', '半导体', '科技', '智能', '机器人', '算力', '大模型', '融资', '投资']
    tech_news = [(t, title, content) for t, title, content in news_items 
                 if any(k in title or k in content for k in tech_keywords)]
    
    if tech_news:
        lines.append('## 今日科技热点\n')
        for time, title, content in tech_news[:8]:
            lines.append(f'**{time} 【{title}】**\n{content}\n')
    
    # 股价数据
    if prices:
        lines.append('\n## 涉及上市公司股价\n')
        lines.append('| 公司 | 现价 | 涨跌 | 涨跌幅 | 最高 | 最低 |')
        lines.append('|------|------|------|--------|------|------|')
        for code, info in prices.items():
            pct = info["pct"]
            emoji = '🔴' if float(pct) < 0 else '🟢'
            lines.append(f'| {info["name"]} | {info["price"]} | {info["change"]} | {emoji}{pct}% | {info["high"]} | {info["low"]} |')
    
    return '\n'.join(lines)

if __name__ == '__main__':
    print('抓取财联社新闻...', file=sys.stderr)
    news = fetch_cls_news()
    
    print('提取上市公司...', file=sys.stderr)
    companies = extract_companies(news)
    
    print(f'获取股价: {list(companies.values())}', file=sys.stderr)
    prices = get_stock_prices(list(companies.values())) if companies else {}
    
    report = generate_report(news, companies, prices)
    print(report)
