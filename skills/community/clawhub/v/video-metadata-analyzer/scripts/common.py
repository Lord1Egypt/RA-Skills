#!/usr/bin/env python3
"""
common.py — video-metadata-analyzer shared utilities
"""

import json
import os
import re
import ssl
import subprocess
import time
import urllib.error
import urllib.request


def http_request_with_retry(req, ctx=None, timeout=180, max_retries=3, label="API"):
    """带重试的 HTTP 请求，5xx / 连接错误时指数退避重试"""
    if ctx is None:
        ctx = ssl.create_default_context()
    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code >= 500 and attempt < max_retries:
                wait = 2 ** attempt
                print(f"WARNING: {label} returned HTTP {e.code}, retry {attempt}/{max_retries} in {wait}s...")
                time.sleep(wait)
                continue
            raise
        except (ConnectionError, TimeoutError, OSError) as e:
            if attempt < max_retries:
                wait = 2 ** attempt
                print(f"WARNING: {label} connection error ({e}), retry {attempt}/{max_retries} in {wait}s...")
                time.sleep(wait)
                continue
            raise


def get_media_duration(path: str) -> float:
    """获取音频/视频文件时长（秒）"""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed (rc={result.returncode}): {result.stderr.strip()}")
    try:
        info = json.loads(result.stdout)
    except (json.JSONDecodeError, ValueError) as e:
        raise RuntimeError(f"ffprobe returned invalid JSON: {e}")
    try:
        return float(info["format"]["duration"])
    except (KeyError, TypeError, ValueError) as e:
        raise RuntimeError(f"ffprobe output missing format.duration: {e}")


def extract_llm_content(resp_data: bytes, label: str = "LLM") -> str:
    """从 LLM API 响应中安全提取 content 字段。
    防御性校验：处理 API 返回错误格式（如 rate limit / error response）。"""
    try:
        res = json.loads(resp_data.decode())
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError) as e:
        raise RuntimeError(f"{label} returned non-JSON response: {e}")

    # 检查是否是 API 错误响应
    if "error" in res and "choices" not in res:
        err_msg = res["error"]
        if isinstance(err_msg, dict):
            err_msg = err_msg.get("message", str(err_msg))
        raise RuntimeError(f"{label} API error: {err_msg}")

    try:
        return res["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError(f"{label} unexpected response structure (missing choices[0].message.content): {e}")


def parse_json_from_llm(content: str, expect_array: bool = False):
    """从 LLM 输出中提取 JSON（支持裸 JSON 和 ```json ... ``` 包裹）。
    expect_array=True 时期望返回 list，否则期望 dict。"""
    if not content or not content.strip():
        return None
    try:
        # 尝试提取 ```json ... ``` 包裹
        if expect_array:
            m = re.search(r'```json\s*(\[.*?\])\s*```', content, re.DOTALL)
        else:
            m = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
        if m:
            return json.loads(m.group(1))
        return json.loads(content)
    except (json.JSONDecodeError, ValueError):
        return None
