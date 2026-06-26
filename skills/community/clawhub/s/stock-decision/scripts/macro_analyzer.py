#!/usr/bin/env python3
"""
宏观环境自动化分析器 - 改进版 v2.4
使用真实网页搜索查询行业周期、公司治理、宏观经济环境
改进: 优化搜索结果解析，避免误报，只分析搜索结果摘要
"""

import sys
import json
import time
import subprocess
import requests
import re
from urllib.parse import quote

def search_web(query, max_results=10):
    """使用Bing搜索查询网页内容"""
    encoded_query = quote(query)
    url = f"https://www.bing.com/search?q={encoded_query}&count={max_results}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"    ⚠️ 搜索失败: {e}")
        return None

def extract_search_summaries(html_content):
    """提取搜索结果的摘要内容，避免误报"""
    # 提取<li class="b_algo">标签内的内容，这些是主要的搜索结果
    # 使用正则表达式提取搜索结果卡片
    pattern = r'<li class="b_algo"[^>]*>.*?</li>'
    results = re.findall(pattern, html_content, re.DOTALL)
    
    # 进一步提取摘要部分（通常是<cite>标签或<p>标签）
    summaries = []
    for result in results:
        # 提取包含摘要的部分，通常在<p>标签中
        summary_match = re.search(r'<p[^>]*>(.*?)</p>', result, re.DOTALL | re.IGNORECASE)
        if summary_match:
            summary = summary_match.group(1)
            # 移除HTML标签
            summary = re.sub(r'<[^>]+>', '', summary)
            summaries.append(summary)
        
        # 也提取<h2>标签下的标题（通常包含搜索结果的标题）
        title_match = re.search(r'<h2[^>]*><a[^>]*>(.*?)</a></h2>', result, re.DOTALL | re.IGNORECASE)
        if title_match:
            title = title_match.group(1)
            # 移除HTML标签
            title = re.sub(r'<[^>]+>', '', title)
            summaries.append(title)
    
    # 如果没有找到，尝试其他方式提取
    if not summaries:
        # 提取所有<p>标签内容
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html_content, re.DOTALL | re.IGNORECASE)
        summaries = [re.sub(r'<[^>]+>', '', p) for p in paragraphs[:10]]
    
    return summaries

def analyze_industry_cycle_industry(industry):
    """查询行业周期 - 针对美股（使用英文关键词）"""
    print(f"🔍 查询行业周期: {industry}")
    
    # 优化关键词，包含更多维度
    keywords_list = [
        f"{industry} industry 2026 trend outlook cycle",
        f"{industry} sector performance 2026",
        f"{industry} market forecast 2026",
        f"{industry} growth cycle analysis 2026"
    ]
    
    all_summaries = []
    for keywords in keywords_list:
        print(f"    搜索关键词: {keywords}")
        content = search_web(keywords, max_results=5)
        if content:
            summaries = extract_search_summaries(content)
            all_summaries.extend(summaries)
        time.sleep(1)  # 避免请求过快
    
    if not all_summaries:
        print("    ⚠️ 搜索失败，采用保守估计")
        return {
            'status': 'stable',
            'coefficient': 0.9,
            'risk_coefficient': 1.0,
            'reason': '搜索失败，采用保守估计'
        }
    
    combined_text = ' '.join(all_summaries).lower()
    
    # 分析判断
    bull_keywords = ['bullish', 'upward', 'growth', 'expanding', 'boom', 'rally', 'strong', 'positive', 'outperformance', 'recover']
    bear_keywords = ['bearish', 'downward', 'declining', 'recession', 'slowdown', 'weak', 'negative', 'underperformance', 'contraction']
    neutral_keywords = ['stable', 'steady', 'neutral', 'moderate', 'mixed', 'cautious', 'uncertain']
    
    bull_count = sum(combined_text.count(k) for k in bull_keywords)
    bear_count = sum(combined_text.count(k) for k in bear_keywords)
    neutral_count = sum(combined_text.count(k) for k in neutral_keywords)
    
    print(f"    多头关键词: {bull_count}")
    print(f"    空头关键词: {bear_count}")
    print(f"    中性关键词: {neutral_count}")
    
    if bull_count > bear_count + 2:
        return {
            'status': 'up',
            'coefficient': 1.1,
            'risk_coefficient': 0.9,
            'reason': f'行业处于上行期，市场预期积极，找到{bull_count}个多头信号'
        }
    elif bear_count > bull_count + 2:
        return {
            'status': 'down',
            'coefficient': 0.8,
            'risk_coefficient': 1.2,
            'reason': f'行业处于下行期，市场预期悲观，找到{bear_count}个空头信号'
        }
    else:
        return {
            'status': 'stable',
            'coefficient': 0.9,
            'risk_coefficient': 1.0,
            'reason': f'行业处于平稳期，市场预期中性，找到{neutral_count}个中性信号'
        }

def analyze_company_governance(company, stock_code):
    """查询公司治理风险 - 针对美股（使用英文关键词）"""
    print(f"🔍 查询公司治理: {company} ({stock_code})")
    
    # 大幅优化关键词，覆盖更多风险类型
    keywords_list = [
        f"{company} {stock_code} fraud investigation SEC FBI",
        f"{company} {stock_code} management arrest criminal",
        f"{company} {stock_code} accounting scandal lawsuit",
        f"{company} {stock_code} delisting risk regulatory",
        f"{company} {stock_code} governance risk corruption",
        f"{company} {stock_code} CEO CFO arrest indictment"
    ]
    
    all_summaries = []
    for keywords in keywords_list:
        print(f"    搜索关键词: {keywords}")
        content = search_web(keywords, max_results=5)
        if content:
            summaries = extract_search_summaries(content)
            all_summaries.extend(summaries)
        time.sleep(1)
    
    if not all_summaries:
        print("    ⚠️ 搜索失败，采用保守估计")
        return {
            'status': 'none',
            'coefficient': 1.0,
            'risk_coefficient': 1.0,
            'reason': '搜索失败，无法判断治理风险'
        }
    
    combined_text = ' '.join(all_summaries).lower()
    
    # 更全面的风险关键词
    severe_keywords = ['fraud', 'arrest', 'criminal', 'indictment', 'fbi', 'delisting', 'fake news', 'accounting scandal', 'major violation']
    moderate_keywords = ['sec investigation', 'lawsuit', 'regulatory', 'warning', 'investigation', 'class action', 'violation']
    mild_keywords = ['ceo change', 'management change', 'director', 'resignation', 'controversy', 'dispute']
    
    severe_count = sum(combined_text.count(k) for k in severe_keywords)
    moderate_count = sum(combined_text.count(k) for k in moderate_keywords)
    mild_count = sum(combined_text.count(k) for k in mild_keywords)
    
    print(f"    严重风险关键词: {severe_count}")
    print(f"    中等风险关键词: {moderate_count}")
    print(f"    轻微风险关键词: {mild_count}")
    
    # 调整判断阈值，避免误报
    if severe_count >= 5:
        return {
            'status': 'severe',
            'coefficient': 0.5,
            'risk_coefficient': 2.0,
            'reason': f'公司存在严重治理风险（欺诈、刑事调查等），找到{severe_count}个严重风险信号，强烈不建议买入'
        }
    elif moderate_count >= 5:
        return {
            'status': 'moderate',
            'coefficient': 0.7,
            'risk_coefficient': 1.3,
            'reason': f'公司存在中等治理风险（监管处罚、诉讼等），找到{moderate_count}个中等风险信号，不建议买入'
        }
    elif mild_count >= 5:
        return {
            'status': 'mild',
            'coefficient': 0.9,
            'risk_coefficient': 1.1,
            'reason': f'公司存在轻微治理风险（高管变动等），找到{mild_count}个轻微风险信号，建议谨慎'
        }
    else:
        return {
            'status': 'none',
            'coefficient': 1.0,
            'risk_coefficient': 1.0,
            'reason': '公司治理良好，无明显问题'
        }

def analyze_macro_economy_us():
    """查询美国宏观经济环境"""
    print(f"🔍 查询美国宏观经济环境")
    
    keywords_list = [
        "2026 US economy outlook stock market",
        "2026 Federal Reserve interest rate inflation",
        "2026 US economic growth GDP forecast",
        "2026 US stock market trend analysis"
    ]
    
    all_summaries = []
    for keywords in keywords_list:
        print(f"    搜索关键词: {keywords}")
        content = search_web(keywords, max_results=5)
        if content:
            summaries = extract_search_summaries(content)
            all_summaries.extend(summaries)
        time.sleep(1)
    
    if not all_summaries:
        print("    ⚠️ 搜索失败，采用保守估计")
        return {
            'status': 'neutral',
            'coefficient': 1.0,
            'risk_coefficient': 1.0,
            'reason': '搜索失败，采用保守估计'
        }
    
    combined_text = ' '.join(all_summaries).lower()
    
    # 分析判断
    bull_keywords = ['rate cut', 'stimulus', 'liquidity', 'bull market', 'recovery', 'growth', 'expansion', 'positive']
    bear_keywords = ['rate hike', 'tightening', 'inflation', 'bear market', 'recession', 'contraction', 'negative']
    neutral_keywords = ['stable', 'neutral', 'steady', 'moderate', 'cautious']
    
    bull_count = sum(combined_text.count(k) for k in bull_keywords)
    bear_count = sum(combined_text.count(k) for k in bear_keywords)
    neutral_count = sum(combined_text.count(k) for k in neutral_keywords)
    
    print(f"    利好关键词: {bull_count}")
    print(f"    利空关键词: {bear_count}")
    print(f"    中性关键词: {neutral_count}")
    
    if bull_count > bear_count + 2:
        return {
            'status': 'bull',
            'coefficient': 1.1,
            'risk_coefficient': 0.9,
            'reason': f'宏观经济利好环境（降息、宽松等），找到{bull_count}个利好信号'
        }
    elif bear_count > bull_count + 2:
        return {
            'status': 'bear',
            'coefficient': 0.8,
            'risk_coefficient': 1.2,
            'reason': f'宏观经济利空环境（加息、紧缩等），找到{bear_count}个利空信号'
        }
    else:
        return {
            'status': 'neutral',
            'coefficient': 1.0,
            'risk_coefficient': 1.0,
            'reason': f'宏观经济环境中性，政策稳健，找到{neutral_count}个中性信号'
        }

def main():
    if len(sys.argv) < 3:
        print("使用方法: python macro_analyzer.py <公司名称> <股票代码> [行业]")
        print("示例: python macro_analyzer.py 超微电脑 usSMCI.OQ 计算机")
        return
    
    company = sys.argv[1]
    stock_code = sys.argv[2]
    industry = sys.argv[3] if len(sys.argv) > 3 else "未知"
    
    print("="*60)
    print(f"宏观环境分析: {company} ({stock_code})")
    print("="*60)
    print()
    
    # 分析行业周期
    industry_result = analyze_industry_cycle_industry(industry)
    print()
    print(f"📈 行业周期分析:")
    print(f"   状态: {industry_result['status']}")
    print(f"   调整系数: {industry_result['coefficient']}")
    print(f"   风险系数: {industry_result['risk_coefficient']}")
    print(f"   理由: {industry_result['reason']}")
    print()
    
    # 分析公司治理
    governance_result = analyze_company_governance(company, stock_code)
    print()
    print(f"🏢 公司治理分析:")
    print(f"   状态: {governance_result['status']}")
    print(f"   调整系数: {governance_result['coefficient']}")
    print(f"   风险系数: {governance_result['risk_coefficient']}")
    print(f"   理由: {governance_result['reason']}")
    print()
    
    # 分析宏观经济
    macro_result = analyze_macro_economy_us()
    print()
    print(f"🌍 宏观经济分析:")
    print(f"   状态: {macro_result['status']}")
    print(f"   调整系数: {macro_result['coefficient']}")
    print(f"   风险系数: {macro_result['risk_coefficient']}")
    print(f"   理由: {macro_result['reason']}")
    print()
    
    # 计算综合调整系数
    total_coefficient = (
        industry_result['coefficient'] * 
        governance_result['coefficient'] * 
        macro_result['coefficient']
    )
    
    total_risk = (
        industry_result['risk_coefficient'] * 
        governance_result['risk_coefficient'] * 
        macro_result['risk_coefficient']
    )
    
    print("="*60)
    print(f"🎯 综合调整系数: {total_coefficient:.3f}")
    print(f"🎯 综合风险系数: {total_risk:.3f}")
    print("="*60)
    print()
    
    # 风险提示
    if governance_result['status'] == 'severe':
        print("🚨🚨🚨 严重风险警告 🚨🚨🚨")
        print("该公司存在严重治理风险，强烈不建议买入！")
        print("风险系数: 2.0 (严重)")
        print()
    elif governance_result['status'] == 'moderate':
        print("⚠️ 风险警告")
        print("该公司存在中等治理风险，不建议买入！")
        print("风险系数: 1.3 (中等)")
        print()

if __name__ == "__main__":
    main()
