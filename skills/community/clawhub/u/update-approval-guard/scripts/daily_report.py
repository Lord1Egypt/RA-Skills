#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日AI新闻+天气日报生成器
每天9:00推送深圳南山区天气 + 国内外AI新闻摘要
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import difflib

# 配置
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', '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')
WEATHER_LAT = 22.5431
WEATHER_LON = 114.0579

def get_weather() -> Dict:
    """获取深圳南山区天气数据"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': WEATHER_LAT,
            'longitude': WEATHER_LON,
            'current': 'temperature_2m,relative_humidity_2m,weather_code',
            'daily': 'temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum',
            'forecast_days': 7,
            'timezone': 'Asia/Shanghai'
        }
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"天气数据获取失败: {e}", file=sys.stderr)
        return None

def get_news(query: str, max_results: int = 5) -> List[Dict]:
    """使用Tavily搜索新闻"""
    try:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "max_results": max_results,
            "topic": "news",
            "days": 1,
            "search_depth": "basic"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except Exception as e:
        print(f"新闻搜索失败: {e}", file=sys.stderr)
        return []

def calculate_importance(item: Dict) -> float:
    """计算新闻重要性分数"""
    score = 0.0
    title = item.get('title', '').lower()
    content = item.get('content', '').lower()
    
    # 关键词权重
    keywords = {
        # 政治监管类（最高优先级）
        'government': 30, 'regulation': 30, 'ban': 25, 'law': 20, 'policy': 20,
        'pentagon': 25, 'military': 25, 'blacklist': 28,
        
        # 重要事件
        'investment': 15, 'funding': 15, 'billion': 18, 'acquisition': 18,
        'breakthrough': 18, 'launch': 12, 'release': 10,
        
        # 知名公司
        'openai': 15, 'anthropic': 15, 'google': 12, 'microsoft': 12,
        'baidu': 15, 'alibaba': 15, 'tencent': 15,
        
        # 产品
        'chatgpt': 15, 'claude': 15, 'gpt': 12, 'model': 8,
    }
    
    for keyword, weight in keywords.items():
        if keyword in title:
            score += weight
        elif keyword in content:
            score += weight * 0.5
    
    # 搜索相关性分数
    score += item.get('score', 0) * 20
    
    return score

def remove_duplicates(news_list: List[Dict], threshold: float = 0.7) -> List[Dict]:
    """去除重复新闻"""
    unique = []
    seen_contents = []
    
    for item in news_list:
        content = item.get('content', '')
        if not content:
            continue
        
        is_duplicate = False
        for seen in seen_contents:
            similarity = difflib.SequenceMatcher(None, content[:500], seen[:500]).ratio()
            if similarity > threshold:
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique.append(item)
            seen_contents.append(content)
    
    return unique

def generate_summary(item: Dict, is_domestic: bool = False) -> str:
    """生成新闻摘要（150-200字）"""
    title = item.get('title', '')
    content = item.get('content', '')
    
    lower_title = title.lower()
    lower_content = content.lower()
    
    # 清理内容
    clean_content = content.replace('#', '').replace('*', '').replace('_', '').replace('\n', ' ')
    clean_content = ' '.join(clean_content.split())
    
    # 识别主体
    entity = "AI公司"
    if 'anthropic' in lower_title and 'claude' in lower_title:
        entity = "Anthropic Claude"
    elif 'openai' in lower_title:
        entity = "OpenAI"
    elif 'claude' in lower_title:
        entity = "Claude"
    elif 'chatgpt' in lower_title:
        entity = "ChatGPT"
    elif is_domestic and ('baidu' in lower_title or 'alibaba' in lower_title or 'tencent' in lower_title):
        entity = "中国AI企业"
    
    # 提取关键事件
    summary_parts = []
    
    if 'pentagon' in lower_content and 'deal' in lower_content:
        summary_parts.append(f"{entity}与美国国防部达成军事合作协议")
        if 'classified' in lower_content:
            summary_parts.append("涉及涉密军事网络部署")
        summary_parts.append("此举引发用户信任危机")
    
    elif 'ban' in lower_content or 'blacklist' in lower_content:
        if 'hhs' in lower_content:
            summary_parts.append(f"{entity}被美国卫生与公众服务部列入黑名单")
            summary_parts.append("禁止联邦政府员工使用")
        else:
            summary_parts.append(f"{entity}被政府部门列入黑名单")
        summary_parts.append("凸显AI伦理分歧对商业格局的影响")
    
    elif 'investment' in lower_content or 'funding' in lower_content:
        import re
        amounts = re.findall(r'\$[\d.]+(?:\s*(?:billion|million))?', lower_content)
        if amounts:
            summary_parts.append(f"{entity}获得{amounts[0]}投资")
        else:
            summary_parts.append(f"{entity}获得重大投资")
        summary_parts.append("显示AI行业持续获得资本青睐")
    
    elif 'launch' in lower_content or 'release' in lower_content:
        summary_parts.append(f"{entity}发布新的AI产品或功能")
    
    # 如果没有提取到关键信息，使用前150字
    if not summary_parts:
        summary_text = clean_content[:150]
        if len(clean_content) > 150:
            summary_text += "..."
        return summary_text
    
    summary = "，".join(summary_parts)
    
    # 限制长度
    if len(summary) > 200:
        summary = summary[:197] + "..."
    
    return summary

def format_weather(weather_data: Dict) -> str:
    """格式化天气信息"""
    if not weather_data:
        return "**当前天气**：暂无数据"
    
    current = weather_data.get('current', {})
    daily = weather_data.get('daily', {})
    
    # 当前天气
    temp = current.get('temperature_2m', 0)
    humid = current.get('relative_humidity_2m', 0)
    code = current.get('weather_code', 3)
    
    # 天气图标
    if code in [0, 1]:
        icon = '☀️'
    elif code in [2, 45, 48]:
        icon = '⛅'
    elif code == 3:
        icon = '☁️'
    elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82, 95]:
        icon = '🌧️'
    else:
        icon = '⛅'
    
    lines = [
        f"**当前天气**：{icon}",
        f"**温度**：{temp:.1f}°C  |  **湿度**：{humid:.0f}%",
        "",
        "**未来7天预报**：",
        ""
    ]
    
    # 7天预报
    times = daily.get('time', [])
    max_temps = daily.get('temperature_2m_max', [])
    min_temps = daily.get('temperature_2m_min', [])
    weather_codes = daily.get('weather_code', [])
    precip = daily.get('precipitation_sum', [0]*len(times))
    
    days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    
    for i in range(min(7, len(times))):
        date_str = times[i]
        date = datetime.strptime(date_str, '%Y-%m-%d')
        weekday = days[date.weekday()]
        
        temp_max = f'{max_temps[i]:.1f}°C' if i < len(max_temps) else '--'
        temp_min = f'{min_temps[i]:.1f}°C' if i < len(min_temps) else '--'
        wc_code = weather_codes[i] if i < len(weather_codes) else 3
        
        # 天气图标
        if wc_code in [0, 1]:
            day_icon = '☀️'
        elif wc_code in [2, 45, 48]:
            day_icon = '⛅'
        elif wc_code == 3:
            day_icon = '☁️'
        elif wc_code in [51, 53, 55, 61, 63, 65, 80, 81, 82, 95]:
            day_icon = '🌧️'
        else:
            day_icon = '⛅'
        
        rain_val = precip[i] if i < len(precip) else 0
        rain_str = f' 🌧️ {rain_val:.1f}mm' if rain_val > 0 else ''
        
        lines.append(f"{weekday} ({date_str}) {day_icon} {temp_min}~{temp_max}{rain_str}")
    
    lines.extend([
        "",
        "**温馨提示**：",
        "- 🌡️ 当前温度适宜，建议穿着轻薄舒适",
        "- ☂️ 未来一周有降雨可能，请携带雨具",
        "- 🚗 早晚温差较大，注意增减衣物",
        "- 💧 空气湿度较高，注意通风防潮"
    ])
    
    return "\n".join(lines)

def format_news(news_list: List[Dict], title: str, is_domestic: bool = False) -> str:
    """格式化新闻列表"""
    if not news_list:
        return f"### {title}\n\n暂无相关新闻"
    
    lines = [f"### {title}", ""]
    
    # 去重
    unique_news = remove_duplicates(news_list)
    
    # 按重要性排序
    scored_news = [(item, calculate_importance(item)) for item in unique_news]
    scored_news.sort(key=lambda x: x[1], reverse=True)
    
    # 取前5条
    top_news = scored_news[:5]
    
    for i, (item, score) in enumerate(top_news, 1):
        news_title = item.get('title', '').strip()
        url = item.get('url', '').strip()
        published = item.get('published_date', '').strip()
        
        if not news_title or not url:
            continue
        
        # 生成中文标题
        lower_title = news_title.lower()
        if 'anthropic' in lower_title:
            cn_title = "Anthropic Claude相关动态"
        elif 'openai' in lower_title:
            cn_title = "OpenAI相关动态"
        elif 'claude' in lower_title:
            cn_title = "Claude相关动态"
        elif 'chatgpt' in lower_title:
            cn_title = "ChatGPT相关动态"
        elif is_domestic:
            cn_title = "中国AI行业动态"
        else:
            cn_title = "AI行业动态"
        
        # 生成摘要
        summary = generate_summary(item, is_domestic)
        
        # 来源信息
        source_info = f"发布时间：{published}" if published else "来源：Tavily AI Search"
        
        lines.extend([
            f"{i}. **{cn_title}**",
            f"   {summary}",
            f"   🔗 {url}",
            f"   📍 {source_info}",
            ""
        ])
    
    return "\n".join(lines)

def main():
    """主函数"""
    now = datetime.now()
    date_str = now.strftime('%Y年%m月%d日')
    
    print(f"## 📅 {date_str}")
    print("")
    print("### 🌤️ 深圳·南山天气预报")
    print("")
    
    # 获取天气
    weather_data = get_weather()
    if weather_data:
        print(format_weather(weather_data))
    else:
        print("**当前天气**：暂无数据")
    
    print("")
    print("---")
    print("")
    print("### 🤖 今日AI要闻（精选10条）")
    print("")
    
    # 获取国内新闻
    domestic_news = get_news("中国AI人工智能大模型最新新闻百度阿里巴巴腾讯字节跳动百度文心通义千问", max_results=8)
    print(format_news(domestic_news, "🇨🇳 国内AI要闻（精选5条）", is_domestic=True))
    
    print("")
    print("---")
    print("")
    
    # 获取国外新闻
    international_news = get_news("AI artificial intelligence GPT OpenAI Anthropic Claude latest news", max_results=8)
    print(format_news(international_news, "🇺🇸 国外AI要闻（精选5条）", is_domestic=False))
    
    print("")
    print("---")
    print("")
    print("**数据来源**：")
    print("- 🌤️ 天气：Open-Meteo (open-meteo.com)")
    print("- 🤖 新闻：Tavily AI Search (tavily.com)")
    print(f"- 📅 生成时间：{now.strftime('%Y年%m月%d日 %H:%M')}")

if __name__ == "__main__":
    main()
