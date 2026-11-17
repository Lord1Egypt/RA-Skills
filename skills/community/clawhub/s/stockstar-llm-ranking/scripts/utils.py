#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTP 工具与输出函数模块。

http_get：请求排行榜页面，支持 gzip 解压、超时与解码回退。
output_json / output_error / output_text：统一输出格式。
"""

import gzip
import io
import json
import sys
import urllib.request

from config import HEADERS, TIMEOUT


def http_get(url, timeout=TIMEOUT, headers=None):
    """
    请求 URL 并返回解码后的 HTML 文本。

    处理要点：
        1. 携带浏览器 UA 与 Accept-Encoding: gzip，减少带宽
        2. gzip 响应自动解压
        3. UTF-8 解码失败时回退 GBK
        4. 网络/HTTP 错误抛出异常，由调用方捕获

    参数：
        url: 完整 URL
        timeout: 超时秒数（默认取 config.TIMEOUT）
        headers: 额外请求头（可选）

    返回：
        HTML 文本字符串

    异常：
        OSError/HTTPError/TimeoutError：请求失败
    """
    req_headers = dict(HEADERS)
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, headers=req_headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        if resp.headers.get("Content-Encoding", "").lower() == "gzip":
            raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            return raw.decode("gbk", errors="replace")


def output_json(data):
    """输出 JSON（ensure_ascii=False，保留中文）。"""
    print(json.dumps(data, ensure_ascii=False))


def output_error(message):
    """统一异常输出格式：{"error": "...", "status": "failed"}。"""
    output_json({"error": message, "status": "failed"})


def output_text(text):
    """文本模式输出。"""
    print(text)


def output_stderr(message):
    """警告/提示信息输出到 stderr，不污染 stdout 的 JSON。"""
    print(message, file=sys.stderr)