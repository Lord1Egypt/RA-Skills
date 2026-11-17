"""
统一输入净化器 — 在系统入口处对所有输入进行消毒
────────────────────────────────────────────────────
这是系统的"免疫系统"第一道防线。
所有外部输入（用户查询、API响应、文件内容）在进入业务逻辑前
必须通过此净化器，防止注入/脏数据/XSS等攻击。
"""
from __future__ import annotations

import re
import html
from typing import Any, Optional


def sanitize_query(query: str, escape_html: bool = False) -> str:
    """
    净化用户查询字符串
    - 去除首尾空白
    - 限制长度
    - 移除控制字符
    - 可选 HTML 实体转义（默认关闭，Phase 4 修复过度净化）

    注意：HTML 转义默认关闭，因为对内部数据做 html.escape() 会
    导致二次转义问题（&amp; → &amp;amp;）。仅在最终输出到 HTML 页面
    时才启用 escape_html=True。
    """
    if not query or not isinstance(query, str):
        return ""

    # 去除控制字符（保留换行和制表符）
    query = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', query)

    # 限制最大长度
    max_len = 500
    if len(query) > max_len:
        query = query[:max_len]

    # 去除首尾空白
    query = query.strip()

    # Phase 4: HTML转义改为可选，默认关闭
    if escape_html:
        query = html.escape(query, quote=False)

    return query


def sanitize_url(url: str) -> Optional[str]:
    """
    净化并验证 URL
    - 只允许 http/https 协议
    - 移除认证信息
    - 验证基本格式
    """
    from urllib.parse import urlparse, urlunparse

    if not url or not isinstance(url, str):
        return None

    url = url.strip()

    try:
        parsed = urlparse(url)
    except Exception:
        return None

    # 只允许 http/https
    if parsed.scheme not in ("http", "https"):
        return None

    # 移除认证信息（防止 http://user:pass@evil.com 这类攻击）
    if "@" in parsed.netloc:
        parsed = parsed._replace(netloc=parsed.netloc.split("@")[-1])

    # 重建 URL
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        "",  # 移除 fragment
    ))

    # 长度限制
    if len(safe_url) > 2048:
        return None

    return safe_url


def sanitize_html_content(html_content: str) -> str:
    """
    净化 HTML 内容（爬取到的页面）
    - 移除 script 标签
    - 移除 iframe 标签
    - 移除事件处理器
    - 限制大小
    """
    if not html_content:
        return ""

    # 限制大小
    max_size = 5 * 1024 * 1024  # 5MB
    if len(html_content) > max_size:
        html_content = html_content[:max_size]

    # 移除 script 标签及其内容
    html_content = re.sub(
        r'<script[^>]*>.*?</script>',
        '',
        html_content,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # 移除 iframe 标签
    html_content = re.sub(
        r'<iframe[^>]*>.*?</iframe>',
        '',
        html_content,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # 移除 on* 事件处理器
    html_content = re.sub(
        r'\s+on\w+\s*=\s*"[^"]*"',
        '',
        html_content,
        flags=re.IGNORECASE,
    )
    html_content = re.sub(
        r"\s+on\w+\s*=\s*'[^']*'",
        '',
        html_content,
        flags=re.IGNORECASE,
    )

    return html_content


def sanitize_filename(filename: str) -> str:
    """
    净化文件名 — 移除危险字符
    """
    if not filename:
        return "untitled"

    # 移除路径分隔符
    filename = filename.replace("/", "_").replace("\\", "_")

    # 移除其他危险字符
    filename = re.sub(r'[<>:"|?*]', '_', filename)

    # 限制长度
    if len(filename) > 200:
        name, ext = filename.rsplit(".", 1) if "." in filename else (filename, "")
        if ext:
            filename = name[:195] + "." + ext
        else:
            filename = name[:200]

    return filename.strip() or "untitled"


def sanitize_dict_keys(data: dict) -> dict:
    """
    递归净化字典的所有 key 和 string value
    Phase 4 修复：不再对内部数据做 HTML 转义，只做基本净化
    （去除控制字符、限制长度、trim）
    """
    if not isinstance(data, dict):
        return data

    result = {}
    for k, v in data.items():
        safe_key = sanitize_query(str(k)) if isinstance(k, str) else str(k)
        if isinstance(v, str):
            result[safe_key] = sanitize_query(v)
        elif isinstance(v, dict):
            result[safe_key] = sanitize_dict_keys(v)
        elif isinstance(v, list):
            result[safe_key] = [
                sanitize_query(item) if isinstance(item, str) else item
                for item in v
            ]
        else:
            result[safe_key] = v
    return result


class InputSanitizer:
    """
    统一输入净化入口

    用法:
        sanitizer = InputSanitizer()
        clean_query = sanitizer.clean(query="<script>alert(1)</script>")
    """

    def clean(self, **kwargs) -> dict[str, Any]:
        """净化所有输入参数"""
        result = {}
        for key, value in kwargs.items():
            if isinstance(value, str):
                result[key] = sanitize_query(value)
            elif isinstance(value, dict):
                result[key] = sanitize_dict_keys(value)
            elif isinstance(value, list):
                result[key] = [
                    sanitize_query(item) if isinstance(item, str) else item
                    for item in value
                ]
            else:
                result[key] = value
        return result
