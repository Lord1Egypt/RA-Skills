#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具模块：提供 HTTP 请求和输出格式化的通用函数。

包含：
- http_get: 发送 GET 请求，自动处理编码和错误
- output_json / output_error / output_text: 三种输出格式
"""

import json
import sys
import unicodedata
import urllib.error
import urllib.request

from config import TIMEOUT


def http_get(url):
    """
    发送 HTTP GET 请求，返回响应文本。

    自动处理：
    - User-Agent 伪装成 Chrome 浏览器，避免被反爬
    - 响应编码自动探测（优先 utf-8，失败则回退 gbk）
    - HTTP/网络异常时直接输出 JSON 错误并退出进程

    参数：
        url: 完整的请求 URL

    返回：
        响应体的文本内容（str）

    异常：
        任何 HTTP/网络错误都会触发 sys.exit(1)，不返回
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
            # 优先 utf-8，部分国内 API 返回 gbk 编码
            try:
                return content.decode("utf-8")
            except UnicodeDecodeError:
                return content.decode("gbk", errors="replace")
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": f"HTTP error: {e.code} {e.reason}", "status": "failed"}))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": f"Network error: {e.reason}", "status": "failed"}))
        sys.exit(1)


def normalize_name(name):
    """将全角英数字归一化为半角（NFKC），如 Ａ→A、１→1"""
    return unicodedata.normalize('NFKC', name) if name else name


def output_json(data, status="success"):
    """以 JSON 格式输出到 stdout，供 AI agent 解析使用"""
    data["status"] = status
    print(json.dumps(data, ensure_ascii=False))


def output_error(message):
    """以 JSON 格式输出错误信息"""
    print(json.dumps({"error": message, "status": "failed"}, ensure_ascii=False))


def output_text(text):
    """以纯文本格式输出到 stdout，供人类直接阅读"""
    print(text)
