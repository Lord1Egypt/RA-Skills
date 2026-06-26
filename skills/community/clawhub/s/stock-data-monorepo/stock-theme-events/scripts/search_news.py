#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻搜索脚本 - akshare + browser 混合方案
优先使用 akshare 财经新闻接口，缺失时用 browser 工具从金十数据搜索
"""

import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
import time


def search_akshare(theme: str, days: int = 15, limit: int = 5) -> List[Dict]:
    """
    使用 akshare 搜索财经新闻
    
    Args:
        theme: 题材关键词
        days: 搜索天数范围
        limit: 返回新闻数量
    
    Returns:
        新闻列表
    """
    try:
        import akshare as ak
        
        # 获取财经新闻
        # akshare 的新闻接口有限，主要尝试几个可用的
        news_list = []
        
        # 尝试获取个股新闻（如果 theme 是股票相关）
        try:
            # 东方财富财经新闻
            news_df = ak.stock_news_em(symbol=theme)
            if news_df is not None and len(news_df) > 0:
                for _, row in news_df.head(limit).iterrows():
                    news_list.append({
                        "title": row.get("标题", ""),
                        "content": row.get("内容", ""),
                        "source": "东方财富",
                        "publish_time": row.get("发布时间", ""),
                        "url": row.get("网址", "")
                    })
        except Exception as e:
            pass
        
        # 尝试获取宏观新闻
        try:
            news_df = ak.macro_news_em()
            if news_df is not None and len(news_df) > 0:
                for _, row in news_df.head(limit).iterrows():
                    if theme in row.get("内容", "") or theme in row.get("标题", ""):
                        news_list.append({
                            "title": row.get("标题", ""),
                            "content": row.get("内容", ""),
                            "source": "东方财富",
                            "publish_time": row.get("发布时间", ""),
                            "url": row.get("网址", "")
                        })
        except Exception as e:
            pass
        
        return news_list[:limit]
    
    except ImportError:
        print("akshare 未安装，将使用 browser 工具搜索")
        return []
    except Exception as e:
        print(f"akshare 搜索失败：{e}")
        return []


def search_jin10_browser(theme: str, days: int = 15, limit: int = 5) -> List[Dict]:
    """
    使用 browser 工具从金十数据搜索新闻
    
    注意：这个函数需要配合 browser 工具使用，返回搜索指令
    实际搜索由调用方执行
    
    Args:
        theme: 题材关键词
        days: 搜索天数范围
        limit: 返回新闻数量
    
    Returns:
        搜索指令和预期结果格式
    """
    search_url = f"https://xnews.jin10.com/search?keyword={theme}"
    
    # 返回搜索指令，由调用方使用 browser 工具执行
    return {
        "action": "browser_search",
        "url": search_url,
        "theme": theme,
        "days": days,
        "limit": limit,
        "extract_fields": ["title", "publish_time", "summary", "url", "source"]
    }


def filter_by_date(news_list: List[Dict], days: int) -> List[Dict]:
    """筛选近 N 天的新闻"""
    cutoff_date = datetime.now() - timedelta(days=days)
    filtered = []
    
    for news in news_list:
        try:
            publish_time = news.get("publish_time", "")
            if publish_time:
                # 尝试解析多种时间格式
                for fmt in ["%Y-%m-%d %H:%M", "%Y-%m-%d", "%m-%d %H:%M", "%Y/%m/%d"]:
                    try:
                        pub_date = datetime.strptime(publish_time, fmt)
                        if pub_date >= cutoff_date:
                            filtered.append(news)
                        break
                    except ValueError:
                        continue
        except Exception:
            # 无法解析时间的新闻也保留
            filtered.append(news)
    
    return filtered


def deduplicate_news(news_list: List[Dict]) -> List[Dict]:
    """去重新闻（基于标题）"""
    seen = set()
    unique = []
    
    for news in news_list:
        title = news.get("title", "").strip()
        if title and title not in seen:
            seen.add(title)
            unique.append(news)
    
    return unique


def search_news(theme: str, days: int = 15, limit: int = 5, 
                use_browser: bool = False) -> Dict:
    """
    搜索新闻（混合方案）
    
    Args:
        theme: 题材关键词
        days: 搜索天数范围
        limit: 返回新闻数量
        use_browser: 是否强制使用 browser
    
    Returns:
        搜索结果
    """
    result = {
        "theme": theme,
        "news": [],
        "source": "unknown",
        "search_time": datetime.now().isoformat()
    }
    
    # 优先尝试 akshare
    if not use_browser:
        news_list = search_akshare(theme, days, limit * 2)  # 多获取一些用于筛选
        
        if news_list:
            # 筛选和去重
            news_list = filter_by_date(news_list, days)
            news_list = deduplicate_news(news_list)
            
            result["news"] = news_list[:limit]
            result["source"] = "akshare"
    
    # 如果 akshare 结果不足或失败，返回 browser 搜索指令
    if len(result["news"]) < limit // 2:
        browser_result = search_jin10_browser(theme, days, limit)
        result["browser_search"] = browser_result
        if not result["news"]:
            result["source"] = "browser_required"
        else:
            result["source"] = "akshare_partial"
    
    return result


def search_multiple_themes(themes: List[str], days: int = 15, 
                          limit: int = 5, output_path: str = None) -> Dict:
    """
    批量搜索多个题材的新闻
    
    Args:
        themes: 题材列表
        days: 搜索天数范围
        limit: 每题材返回新闻数量
        output_path: 输出 JSON 文件路径
    
    Returns:
        搜索结果
    """
    results = {
        "search_time": datetime.now().isoformat(),
        "themes": {}
    }
    
    for i, theme in enumerate(themes):
        print(f"[{i+1}/{len(themes)}] 搜索：{theme}")
        result = search_news(theme, days, limit)
        results["themes"][theme] = result
        
        # 避免请求过快
        time.sleep(0.5)
    
    # 保存结果
    if output_path:
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到：{output_path}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description='新闻搜索脚本')
    parser.add_argument('--theme', help='题材关键词')
    parser.add_argument('--themes', help='题材列表 JSON 文件')
    parser.add_argument('--days', type=int, default=15, help='搜索天数范围')
    parser.add_argument('--limit', type=int, default=5, help='返回新闻数量')
    parser.add_argument('--output', help='输出 JSON 文件路径')
    parser.add_argument('--browser', action='store_true', help='强制使用 browser')
    
    args = parser.parse_args()
    
    if args.theme:
        result = search_news(args.theme, args.days, args.limit, args.browser)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.themes:
        with open(args.themes, 'r', encoding='utf-8') as f:
            themes_data = json.load(f)
        
        # 从聚类结果中提取题材列表
        if "top_themes" in themes_data:
            themes = [t["theme"] for t in themes_data["top_themes"]]
        else:
            themes = list(themes_data.keys())
        
        search_multiple_themes(themes, args.days, args.limit, args.output)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
