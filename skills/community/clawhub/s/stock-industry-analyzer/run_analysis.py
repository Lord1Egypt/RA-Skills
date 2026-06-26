# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'C:\Users\l31408\.agents\skills\stock-industry-analyzer')

from src.fetcher import fetch_news
from src.analyzer import analyze_industry, analyze_stock
from src.reporter import generate_report

# 获取新闻
news = fetch_news()
print(f"Got {len(news)} news")

# 分析行业
trends = analyze_industry(news)
print(f"Analyzed {len(trends)} industries")

# 获取股票数据
stocks = []
for trend in trends[:3]:
    industry = trend.get('industry')
    codes = ['300750', '002594', '002230', '600036', '600519', '688981', '600276']
    for code in codes:
        s = analyze_stock(code, news)
        if s.get('industry') == industry and s not in stocks:
            stocks.append(s)
            if len(stocks) >= 6:
                break

# 生成报告
report = generate_report(news, trends, stocks)

# 保存报告
with open(r'C:\Users\l31408\.agents\skills\stock-industry-analyzer\data\reports\latest_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print("Report saved!")
print(report[:2000])