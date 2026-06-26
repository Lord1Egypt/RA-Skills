# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os
os.chdir(r'C:\Users\l31408\.openclaw\workspace\stock-analyst')
from src.fetcher import fetch_news
from src.analyzer import analyze_industry, analyze_stock

news = fetch_news()
print('=== News Check ===')
for n in news[:3]:
    print('Title:', n.get('title'))
    print('Companies:', n.get('companies'))
    print('')

print('=== Industry Trends ===')
trends = analyze_industry(news)
for t in trends[:3]:
    print('Industry:', t.get('industry'))
    print('Companies:', t.get('companies'))
    print('')
    
print('=== Stock Analysis ===')
stock = analyze_stock('300750', news)
print('Stock:', stock)