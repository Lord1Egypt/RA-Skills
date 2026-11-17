#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTP 请求与输出工具模块。

http_get：下载完整页面（用于构建/更新缓存）。
http_get_partial：仅下载前 10KB，用于快速检测评级日期是否变化。
output_json / output_error / output_text：统一输出格式，供 CLI 调用。
"""

import gzip
import json
import sys
import urllib.error
import urllib.request

from config import TIMEOUT


def _decode(content):
    """将 bytes 解码为 str，优先 UTF-8，回退 GBK。"""
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return content.decode("gbk", errors="replace")


def http_get(url):
    """
    下载完整页面内容。
    使用 Accept-Encoding: gzip 压缩传输，减少带宽和 IncompleteRead 风险。
    先尝试 UTF-8 解码，失败则回退到 GBK（证券之星部分页面使用 GBK 编码）。
    网络/HTTP 异常时直接打印错误 JSON 并退出。
    """
    req = urllib.request.Request(url, headers={
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Encoding": "gzip",
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            content = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                content = gzip.decompress(content)
            return _decode(content)
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": f"请求失败({e.code})，请稍后重试", "status": "failed"}))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": "网络连接失败，请检查网络后重试", "status": "failed"}))
        sys.exit(1)


def http_get_partial(url, max_bytes=10240):
    """
    仅下载页面头部（默认 10KB），用于快速检测评级日期是否变更。
    不需要完整页面，减少带宽和耗时。
    使用 Accept-Encoding: gzip 压缩传输。
    失败时返回空字符串，由调用方决定是否跳过该机构。
    """
    req = urllib.request.Request(url, headers={
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Encoding": "gzip",
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            content = resp.read(max_bytes)
            if resp.headers.get("Content-Encoding") == "gzip":
                content = gzip.decompress(content)
            return _decode(content)
    except Exception:
        return ""


def output_json(data, status="success"):
    """输出 JSON 格式（供 AI 解析），自动带上 status 字段。"""
    data["status"] = status
    print(json.dumps(data, ensure_ascii=False))


def output_error(message):
    """输出错误 JSON。"""
    print(json.dumps({"error": message, "status": "failed"}, ensure_ascii=False))


def output_text(text):
    """输出纯文本格式（供终端用户直接阅读）。"""
    print(text)
