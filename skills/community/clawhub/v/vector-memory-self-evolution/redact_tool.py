#!/usr/bin/env python3
"""
向量记忆 - 敏感数据脱敏工具
自动脱敏敏感信息（API密钥、密码等）
"""

import re
from datetime import datetime

# 敏感信息正则模式
SENSITIVE_PATTERNS = [
    (r'Bearer\s+[a-zA-Z0-9_-]{20,}', 'Bearer ***REDACTED***'),
    (r'api[_-]?key["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_-]{20,}', 'api_key=***REDACTED***'),
    (r'postgres://[^@]+@', 'postgres://***REDACTED***@'),
    (r'mysql://[^@]+@', 'mysql://***REDACTED***@'),
    (r'-i\s+[^\s]+/id_[a-z]+', '-i ***REDACTED***'),
    (r'-p["\']?[a-zA-Z0-9_-]{6,}', '-p ***REDACTED***'),
    (r'--password["\']?\s*[a-zA-Z0-9_-]{6,}', '--password ***REDACTED***'),
    (r'token["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_-]{20,}', 'token=***REDACTED***'),
    (r'AKIA[0-9A-Z]{16}', 'AKIA***REDACTED***'),
    (r'sk-[a-zA-Z0-9]{20,}', 'sk-***REDACTED***'),
]

def redact_sensitive(text):
    """脱敏敏感信息"""
    if not text:
        return text

    redacted = text
    for pattern, replacement in SENSITIVE_PATTERNS:
        redacted = re.sub(pattern, replacement, redacted, flags=re.IGNORECASE)

    return redacted

def redact_command(command):
    """脱敏命令中的敏感信息"""
    return redact_sensitive(command)

def redact_content(content):
    """脱敏内容中的敏感信息"""
    return redact_sensitive(content)

def log_redacted(title, content, context="", **metadata):
    """记录脱敏后的内容"""
    from memory_api import log

    redacted_content = redact_content(content)
    redacted_context = redact_sensitive(context) if context else ""

    return log(
        typ=metadata.get('type', 'info'),
        title=title,
        content=redacted_content,
        context=redacted_context,
        **{k: redact_sensitive(str(v)) for k, v in metadata.items() if k not in ['type', 'title', 'content', 'context']}
    )

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: redact_tool.py <文本>")
        sys.exit(1)

    text = sys.argv[1]
    print(f"原文: {text}")
    print(f"脱敏: {redact_sensitive(text)}")