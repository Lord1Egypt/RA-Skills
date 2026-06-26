#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serper API Web Search 客户端
用于 OpenClaw 自定义技能，提供国内可访问的实时网络搜索能力

Serper 是一个基于 Google Search 的 API 服务，国内可直接访问。
免费额度：每月 2,500 次搜索

注册获取 API Key: https://serper.dev/
API 文档：https://serper.dev/api-key
"""

import json
import sys
import os
import urllib.request
import urllib.error

# ==================== 配置区域 ====================
# 请在此处填入你的 Serper API Key
SERPER_API_KEY = "f57857d0a19871c49ea0e2bf186dd30bcf5bb6d7"

# Serper API 端点
SERPER_ENDPOINT = "https://google.serper.dev/search"

# 默认搜索数量
DEFAULT_COUNT = 5
# ==================================================


def clean_search_result(result_text):
    """
    清洗搜索结果，提取更丰富的信息
    包括 title、snippet、url、date 等
    """
    try:
        data = json.loads(result_text)
        cleaned_results = []
        
        # Serper 返回的有机搜索结果在 'organic' 数组中
        organic_results = data.get("organic", [])
        
        for result in organic_results:
            title = result.get("title", "无标题")
            snippet = result.get("snippet", "无摘要")
            link = result.get("link", result.get("url", ""))
            date = result.get("date", "")  # 搜索结果日期
            
            cleaned_results.append({
                "title": title,
                "snippet": snippet,
                "url": link,
                "date": date
            })
        
        # 如果有天气/即时答案信息，优先返回
        answer_box = data.get("answerBox", {})
        weather_info = data.get("weather", {})
        
        return cleaned_results, answer_box, weather_info
        
    except json.JSONDecodeError as e:
        return [{"title": "JSON Parse Error", "snippet": str(e), "url": "", "date": ""}], {}, {}
    except Exception as e:
        return [{"title": "Error", "snippet": str(e), "url": "", "date": ""}], {}, {}


def format_output(cleaned_results, answer_box=None, weather_info=None):
    """
    将清洗后的结果格式化为纯文本输出
    """
    output_lines = []
    
    # 优先显示天气信息（如果有）
    if weather_info and isinstance(weather_info, dict) and weather_info.get("temperature"):
        output_lines.append("【天气信息】")
        if weather_info.get("location"):
            output_lines.append(f"地点：{weather_info.get('location', '')}")
        if weather_info.get("temperature"):
            output_lines.append(f"温度：{weather_info.get('temperature', '')}")
        if weather_info.get("condition"):
            output_lines.append(f"天气：{weather_info.get('condition', '')}")
        if weather_info.get("humidity"):
            output_lines.append(f"湿度：{weather_info.get('humidity', '')}")
        if weather_info.get("wind"):
            output_lines.append(f"风力：{weather_info.get('wind', '')}")
        output_lines.append("")
    
    # 显示答案框（如果有）
    if answer_box and isinstance(answer_box, dict) and answer_box.get("answer"):
        output_lines.append("【答案】")
        output_lines.append(answer_box.get("answer", ""))
        if answer_box.get("source"):
            output_lines.append(f"来源：{answer_box.get('source', '')}")
        output_lines.append("")
    
    # 显示搜索结果
    if not cleaned_results:
        output_lines.append("未找到更多搜索结果")
    else:
        output_lines.append("【搜索结果】")
        for i, result in enumerate(cleaned_results, 1):
            output_lines.append(f"[{i}] {result['title']}")
            output_lines.append(f"    {result['snippet']}")
            if result.get('url'):
                output_lines.append(f"    链接：{result['url']}")
            if result.get('date'):
                output_lines.append(f"    日期：{result['date']}")
            output_lines.append("")
    
    return "\n".join(output_lines)


def web_search(query, count=DEFAULT_COUNT):
    """
    执行 Web 搜索
    
    Args:
        query: 搜索关键词
        count: 返回结果数量（默认 5，最大 10）
    
    Returns:
        格式化后的搜索结果文本
    """
    # 构建 Serper API 请求
    payload = {
        "q": query,
        "num": min(max(1, count), 10)  # 限制在 1-10 之间
    }
    
    data = json.dumps(payload).encode('utf-8')
    headers = {
        "X-API-Key": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        # 发送 POST 请求（使用 urllib，不需要额外安装库）
        req = urllib.request.Request(SERPER_ENDPOINT, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=30) as response:
            result_text = response.read().decode('utf-8')
            
            # 清洗数据（返回三元组：results, answer_box, weather_info）
            cleaned_results, answer_box, weather_info = clean_search_result(result_text)
            
            # 格式化输出
            formatted_output = format_output(cleaned_results, answer_box, weather_info)
            
            # 返回 MCP 兼容的响应格式
            return json.dumps({
                "jsonrpc": "2.0",
                "id": 1,
                "result": {
                    "content": [{"type": "text", "text": formatted_output}],
                    "isError": False
                }
            }, ensure_ascii=False)
        
    except urllib.error.HTTPError as e:
        error_msg = f"HTTP Error {e.code}: {e.reason}"
        try:
            error_body = e.read().decode('utf-8')
            error_msg += f"\n{error_body}"
        except:
            pass
        return json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "content": [{"type": "text", "text": error_msg}],
                "isError": True
            }
        }, ensure_ascii=False)
    except urllib.error.URLError as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "content": [{"type": "text", "text": f"网络错误：{e.reason}"}],
                "isError": True
            }
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "content": [{"type": "text", "text": f"错误：{str(e)}"}],
                "isError": True
            }
        }, ensure_ascii=False)


def main():
    """
    主函数：从命令行参数获取搜索关键词并执行搜索
    """
    # 获取命令行参数
    if len(sys.argv) < 2:
        # 如果没有参数，尝试从标准输入读取
        query = sys.stdin.read().strip() if not sys.stdin.isatty() else ""
        if not query:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": 1,
                "result": {
                    "content": [{"type": "text", "text": "用法：python web_search.py <搜索关键词> [结果数量]"}],
                    "isError": True
                }
            }, ensure_ascii=False))
            sys.exit(1)
    else:
        query = sys.argv[1]
    
    # 获取结果数量（可选）
    count = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_COUNT
    
    # 执行搜索并输出结果
    result = web_search(query, count)
    print(result)


if __name__ == "__main__":
    main()
