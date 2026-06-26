#!/usr/bin/env python3
"""
Web Search Tool - 无需API Key的联网搜索工具
支持百度、必应(中国版)搜索引擎
通过解析搜索结果页面获取信息
"""

import argparse
import io
import json
import os
import re
import sys
import time
import random
import urllib.parse
from typing import Optional

# Windows环境下强制使用UTF-8输出
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import requests
from bs4 import BeautifulSoup


# ============================================================
# 通用配置
# ============================================================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
]

DEFAULT_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


def get_session() -> requests.Session:
    """创建带有随机UA的请求会话"""
    session = requests.Session()
    headers = DEFAULT_HEADERS.copy()
    headers["User-Agent"] = random.choice(USER_AGENTS)
    session.headers.update(headers)
    return session


# ============================================================
# 百度搜索
# ============================================================

def search_baidu(query: str, num_results: int = 8, time_range: Optional[str] = None) -> list[dict]:
    """
    百度搜索
    
    Args:
        query: 搜索关键词（支持 site:xxx filetype:xxx 等高级语法）
        num_results: 返回结果数量
        time_range: 时间范围 - day/week/month/year/None
    
    Returns:
        搜索结果列表 [{"title", "url", "snippet", "source"}]
    """
    session = get_session()
    results = []
    
    params = {
        "wd": query,
        "rn": min(num_results, 20),  # 百度每页最多20条
        "ie": "utf-8",
    }
    
    # 时间范围参数
    time_map = {
        "day": "stf=1709596800,1709683200|stftype=1",
        "week": "stf=1709164800,1709683200|stftype=1",
        "month": "stf=1707091200,1709683200|stftype=1",
        "year": "stf=1678147200,1709683200|stftype=1",
    }
    
    # 百度用gpc参数控制时间范围
    if time_range and time_range in ("day", "week", "month", "year"):
        # 使用更通用的方式：通过搜索工具参数
        stf_map = {"day": 1, "week": 2, "month": 3, "year": 4}
        params["gpc"] = f"stf={stf_map.get(time_range, 0)}"
    
    try:
        resp = session.get(
            "https://www.baidu.com/s",
            params=params,
            timeout=15,
            allow_redirects=True,
        )
        resp.raise_for_status()
        resp.encoding = "utf-8"
        
        soup = BeautifulSoup(resp.text, "lxml")
        
        # 百度搜索结果在 div.result 或 div.c-container 中
        containers = soup.select("div.result, div.c-container")
        
        for container in containers[:num_results]:
            title_tag = container.select_one("h3 a, .t a")
            if not title_tag:
                continue
            
            title = title_tag.get_text(strip=True)
            href = title_tag.get("href", "")
            
            # 百度的链接是跳转链接，尝试获取真实URL
            real_url = href  # 默认使用百度跳转链接
            
            # 获取摘要
            snippet_tag = container.select_one(
                ".c-abstract, .c-span-last, "
                "div.c-row .content-right_2s-H4, "
                "span.content-right_2s-H4, "
                ".c-font-normal"
            )
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
            
            # 如果没有摘要，尝试获取容器内所有文本
            if not snippet:
                # 排除标题后获取文本
                all_text = container.get_text(strip=True)
                title_text = title
                snippet = all_text.replace(title_text, "", 1).strip()[:200]
            
            # 获取来源
            source_tag = container.select_one(
                ".c-showurl, .source_s_3L3PB, "
                "span.c-color-gray, .c-gap-icon-right-samll"
            )
            source = source_tag.get_text(strip=True) if source_tag else ""
            
            if title:
                results.append({
                    "title": title,
                    "url": real_url,
                    "snippet": snippet[:300],
                    "source": source or "百度",
                    "engine": "baidu",
                })
        
    except requests.RequestException as e:
        print(f"[百度搜索错误] {e}", file=sys.stderr)
    
    return results


# ============================================================
# 必应搜索（中国版）
# ============================================================

def search_bing(query: str, num_results: int = 8, time_range: Optional[str] = None) -> list[dict]:
    """
    必应中国版搜索
    
    Args:
        query: 搜索关键词（支持 site:xxx filetype:xxx 等高级语法）
        num_results: 返回结果数量
        time_range: 时间范围 - day/week/month/year/None
    
    Returns:
        搜索结果列表 [{"title", "url", "snippet", "source"}]
    """
    session = get_session()
    results = []
    
    params = {
        "q": query,
        "count": min(num_results, 30),
        "ensearch": 0,  # 使用中文版必应
        "FORM": "BESBTB",
    }
    
    # 必应时间范围过滤
    time_map = {
        "day": "ex1:\"ez1\"",
        "week": "ex1:\"ez2\"",
        "month": "ex1:\"ez3\"",
        "year": "ex1:\"ez5_10750_13849\"",
    }
    if time_range and time_range in time_map:
        params["filters"] = time_map[time_range]
    
    try:
        resp = session.get(
            "https://cn.bing.com/search",
            params=params,
            timeout=15,
            allow_redirects=True,
        )
        resp.raise_for_status()
        resp.encoding = "utf-8"
        
        soup = BeautifulSoup(resp.text, "lxml")
        
        # 必应结果在 li.b_algo 中
        items = soup.select("li.b_algo")
        
        for item in items[:num_results]:
            title_tag = item.select_one("h2 a")
            if not title_tag:
                continue
            
            title = title_tag.get_text(strip=True)
            url = title_tag.get("href", "")
            
            # 获取摘要
            snippet_tag = item.select_one(
                ".b_caption p, .b_algoSlug, .b_paractl, .b_dList"
            )
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
            
            if not snippet:
                caption = item.select_one(".b_caption")
                snippet = caption.get_text(strip=True) if caption else ""
                snippet = snippet.replace(title, "", 1).strip()[:200]
            
            # 获取来源/域名
            cite_tag = item.select_one("cite, .b_attribution cite")
            source = cite_tag.get_text(strip=True) if cite_tag else ""
            if not source and url:
                try:
                    source = urllib.parse.urlparse(url).netloc
                except Exception:
                    source = ""
            
            if title:
                results.append({
                    "title": title,
                    "url": url,
                    "snippet": snippet[:300],
                    "source": source or "必应",
                    "engine": "bing",
                })
        
    except requests.RequestException as e:
        print(f"[必应搜索错误] {e}", file=sys.stderr)
    
    return results


# ============================================================
# 聚合搜索
# ============================================================

def search_all(
    query: str,
    engines: list[str] | None = None,
    num_results: int = 8,
    time_range: Optional[str] = None,
) -> list[dict]:
    """
    聚合搜索 - 同时搜索多个引擎并去重
    
    Args:
        query: 搜索关键词
        engines: 使用的引擎列表，默认 ["baidu", "bing"]
        num_results: 每个引擎的结果数量
        time_range: 时间范围
    
    Returns:
        去重后的搜索结果列表
    """
    if engines is None:
        engines = ["baidu", "bing"]
    
    engine_map = {
        "baidu": search_baidu,
        "bing": search_bing,
    }
    
    all_results = []
    seen_titles = set()
    
    for engine_name in engines:
        func = engine_map.get(engine_name)
        if not func:
            print(f"[警告] 未知引擎: {engine_name}", file=sys.stderr)
            continue
        
        try:
            engine_results = func(query, num_results=num_results, time_range=time_range)
            for r in engine_results:
                # 用标题的前30个字符做简单去重
                key = re.sub(r"\s+", "", r["title"])[:30].lower()
                if key not in seen_titles:
                    seen_titles.add(key)
                    all_results.append(r)
        except Exception as e:
            print(f"[{engine_name}搜索异常] {e}", file=sys.stderr)
        
        # 引擎之间加小延迟，避免被封
        time.sleep(random.uniform(0.3, 0.8))
    
    return all_results


# ============================================================
# 输出格式化
# ============================================================

def format_text(results: list[dict], query: str) -> str:
    """格式化为简洁文本摘要"""
    if not results:
        return f"未找到与 \"{query}\" 相关的搜索结果。"
    
    lines = [f"搜索: {query}", f"共 {len(results)} 条结果", ""]
    
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['title']}")
        lines.append(f"    链接: {r['url']}")
        if r.get("snippet"):
            lines.append(f"    摘要: {r['snippet']}")
        if r.get("source"):
            lines.append(f"    来源: {r['source']} ({r['engine']})")
        lines.append("")
    
    return "\n".join(lines)


def format_json(results: list[dict], query: str) -> str:
    """格式化为JSON"""
    output = {
        "query": query,
        "total": len(results),
        "results": results,
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Web Search Tool - 无需API Key的联网搜索",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
高级搜索语法示例:
  限定站点:   python search.py "site:zhihu.com 机器学习"
  限定文件:   python search.py "filetype:pdf 深度学习教程"
  精确匹配:   python search.py '"自然语言处理"'
  排除关键词: python search.py "Python教程 -广告"
  组合搜索:   python search.py "site:github.com Python web框架"
        """,
    )
    
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument(
        "-e", "--engine",
        choices=["baidu", "bing", "all"],
        default="all",
        help="搜索引擎 (默认: all)",
    )
    parser.add_argument(
        "-n", "--num",
        type=int,
        default=8,
        help="每个引擎返回结果数 (默认: 8)",
    )
    parser.add_argument(
        "-t", "--time",
        choices=["day", "week", "month", "year"],
        default=None,
        help="时间范围过滤",
    )
    parser.add_argument(
        "-f", "--format",
        choices=["text", "json"],
        default="text",
        help="输出格式 (默认: text)",
    )
    
    args = parser.parse_args()
    
    # 确定引擎列表
    if args.engine == "all":
        engines = ["baidu", "bing"]
    else:
        engines = [args.engine]
    
    # 执行搜索
    results = search_all(
        query=args.query,
        engines=engines,
        num_results=args.num,
        time_range=args.time,
    )
    
    # 格式化输出
    if args.format == "json":
        print(format_json(results, args.query))
    else:
        print(format_text(results, args.query))


if __name__ == "__main__":
    main()
