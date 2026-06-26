# -*- coding: utf-8 -*-
import sys
import traceback
sys.path.insert(0, r'C:\Users\l31408\.agents\skills\stock-industry-analyzer')

try:
    from src.fetcher import fetch_news
    from src.analyzer import analyze_industry, analyze_stock
    from src.reporter import generate_report, INDUSTRY_GRAPH

    # 获取新闻
    news = fetch_news()
    print(f"Got {len(news)} news")

    # 分析行业
    trends = analyze_industry(news)
    print(f"Analyzed {len(trends)} industries")

    # 获取股票数据
    stocks = []
    codes_to_check = ['300750', '002594', '002230', '600036', '600519', '688981', '600276', '600438']
    for code in codes_to_check:
        s = analyze_stock(code, news)
        if s not in stocks:
            stocks.append(s)
        if len(stocks) >= 6:
            break

    # 生成报告
    report = generate_report(news, trends, stocks)
    print("Report generated!")

    # 保存报告
    out_path = r'C:\Users\l31408\.agents\skills\stock-industry-analyzer\data\reports\report.txt'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Report saved to {out_path}")
    
    # 打印报告
    print("\n" + "="*75)
    print(report)
    
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()