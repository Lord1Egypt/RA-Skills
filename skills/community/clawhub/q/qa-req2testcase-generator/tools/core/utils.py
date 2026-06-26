#!/usr/bin/env python3
"""
core/utils.py — 工具函数
"""

import os
import json
import hashlib
import glob

from .constants import DOMAIN_KEYWORDS


def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def _write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _file_exists(path):
    return os.path.exists(path) and os.path.getsize(path) > 10


def _sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _detect_domain(text, default="trade"):
    text_lower = text.lower()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return domain
    return default


def _write_text(path, content):
    """写入文本文件，UTF-8编码"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _read_file_safe(path, max_chars=8000):
    """安全读取文件，不存在返回空字符串"""
    if not os.path.exists(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()[:max_chars]
    except Exception:
        return ""


def _get_nested(data, key_path):
    """获取嵌套字段值，支持多候选路径（用|分隔）

    示例:
      _get_nested(data, "blocks.modules")  # 单路径
      _get_nested(data, "blocks.operations|blocks.pages")  # 多候选，返回第一个非空的
    """
    candidates = key_path.split("|")
    for candidate in candidates:
        keys = candidate.strip().split(".")
        current = data
        for k in keys:
            if isinstance(current, dict):
                current = current.get(k)
            else:
                current = None
                break
        if current is not None:
            return current
    return None


def _get_case_field(case, field, default=""):
    """兼容fields嵌套结构和顶层字段的取值"""
    # 优先顶层
    val = case.get(field)
    if val is not None:
        return val
    # 其次fields嵌套
    fields = case.get("fields", {})
    if isinstance(fields, dict):
        val = fields.get(field)
        if val is not None:
            return val
    return default


def _is_smoke(value):
    """判断is_smoke字段值是否为True（兼容多种格式）"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "是", "yes", "1")
    if isinstance(value, (int, float)):
        return value == 1
    return False
