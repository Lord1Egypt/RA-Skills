#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具模块：提供 HTTP 请求和输出格式化的通用函数。

包含：
- http_get: 发送 GET 请求，自动处理编码和错误
- normalize_stock_id: 股票代码转 stockid 格式（sh/sz 前缀）
- output_json / output_error / output_text: 三种输出格式
"""

import json
import re
import sys
import urllib.error
import urllib.request

from config import TIMEOUT, MARKET_PREFIX


def http_get(url, raise_on_error=True):
    """
    发送 HTTP GET 请求，返回响应文本。

    自动处理：
    - User-Agent 伪装成 Chrome 浏览器，避免被反爬
    - 响应编码自动探测（优先 utf-8，失败则回退 gbk）

    参数：
        url: 完整的请求 URL
        raise_on_error: True 时（默认）HTTP/网络异常直接输出 JSON 错误并退出进程；
                       False 时返回空字符串，由调用方决定错误处理策略

    返回：
        响应体的文本内容（str）；raise_on_error=False 且出错时返回 ""
    """
    req = urllib.request.Request(url, headers={
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            content = resp.read()
            try:
                return content.decode("utf-8")
            except UnicodeDecodeError:
                return content.decode("gbk", errors="replace")
    except urllib.error.HTTPError as e:
        if raise_on_error:
            print(json.dumps({"error": f"HTTP error: {e.code} {e.reason}", "status": "failed"}))
            sys.exit(1)
        return ""
    except urllib.error.URLError as e:
        if raise_on_error:
            print(json.dumps({"error": f"Network error: {e.reason}", "status": "failed"}))
            sys.exit(1)
        return ""


def normalize_stock_id(code):
    """
    将股票代码转换为 stockid 格式（如 sh600000、sz000001）。

    规则：
    - 已有 sh/sz 前缀 → 直接返回
    - 6 位纯数字 → 根据首位数字自动补前缀
    - 其他格式 → 返回原值（由调用方处理）

    参数：
        code: 股票代码字符串

    返回：
        stockid 格式字符串（如 "sh600000"）
    """
    code = code.strip()
    # 已有前缀
    if re.match(r'^(sh|sz)\d{6}$', code):
        return code
    # 纯 6 位数字
    if re.match(r'^\d{6}$', code):
        prefix = MARKET_PREFIX.get(code[0], "")
        if prefix:
            return f"{prefix}{code}"
    # 其他格式原样返回
    return code


def output_json(data, status="success"):
    """以 JSON 格式输出到 stdout，供 AI agent 解析使用"""
    data = {**data, "status": status}
    print(json.dumps(data, ensure_ascii=False))


def output_error(message):
    """以 JSON 格式输出错误信息"""
    print(json.dumps({"error": message, "status": "failed"}, ensure_ascii=False))


def output_text(text):
    """以纯文本格式输出到 stdout，供人类直接阅读"""
    print(text)
