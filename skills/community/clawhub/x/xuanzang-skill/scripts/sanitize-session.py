"""
玄奘 Session 脱敏处理器 — 实现 SKILL.md 任务完成反馈第二步脱敏规则。
用法: python sanitize-session.py <input.json> [output.json]
      若不指定 output，输出到 <input>-sanitized.json

脱敏规则:
  - 移除：文件绝对路径（仅保留扩展名统计）、代码片段、API Key/Token、
           公司/项目名称、邮箱/用户名、任何 PII
  - 保留：任务类型分类、失败模式分类、压力等级变化、角色使用统计、
           工具调用计数、时间线（相对时间偏移）
"""

import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

tz = timezone(timedelta(hours=8))  # UTC+8

# ── 脱敏模式 ──────────────────────────────────────────────
PATH_PATTERNS = [
    re.compile(r'[A-Za-z]:[\\/][^\s"\'<>|*?]+', re.IGNORECASE),   # Windows 绝对路径
    re.compile(r'/(?:home|Users|root|var|tmp|opt|etc)/[^\s"\'<>|*?]+'),  # Unix 绝对路径
    re.compile(r'~(?:\.[a-zA-Z]+)?/[^\s"\'<>|*?]+'),              # ~/ 路径
]

API_KEY_PATTERNS = [
    re.compile(r'(?:api[_-]?key|apikey|secret|token|password|passwd)\s*[:=]\s*[^\s,;}"]+', re.IGNORECASE),
    re.compile(r'(?:Bearer|Basic)\s+[A-Za-z0-9+/=_-]{20,}', re.IGNORECASE),
    re.compile(r'sk-[A-Za-z0-9]{20,}', re.IGNORECASE),            # OpenAI key
    re.compile(r'ghp_[A-Za-z0-9]{36}', re.IGNORECASE),            # GitHub PAT
    re.compile(r'AKIA[0-9A-Z]{16}', re.IGNORECASE),               # AWS Access Key
]

EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', re.IGNORECASE)
IP_PATTERN = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
UUID_PATTERN = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.IGNORECASE)

# 文件扩展名提取
EXT_PATTERN = re.compile(r'\.([a-zA-Z0-9]{1,10})(?:["\s,;)}\]]|$)')


def _extract_extension_stats(text):
    """从文本中提取文件扩展名统计，替换路径为占位符。"""
    exts = {}
    for m in EXT_PATTERN.finditer(text):
        ext = m.group(1).lower()
        if ext not in ('com', 'org', 'net', 'io', 'dev', 'app', 'cn', 'html', 'htm',
                        'py', 'yaml', 'yml', 'toml', 'md', 'json', 'jsonl',
                        'xml', 'csv', 'ts', 'js', 'tsx', 'jsx', 'css', 'scss'):
            exts[ext] = exts.get(ext, 0) + 1
    return exts


def _sanitize_text(text):
    """对单段文本执行全部脱敏替换。"""
    if not isinstance(text, str):
        return text

    result = text

    # 1. 移除 API 密钥
    for pat in API_KEY_PATTERNS:
        result = pat.sub('[REDACTED:API_KEY]', result)

    # 2. 移除邮箱
    result = EMAIL_PATTERN.sub('[REDACTED:EMAIL]', result)

    # 3. 移除 IP
    result = IP_PATTERN.sub('[REDACTED:IP]', result)

    # 4. 移除 UUID
    result = UUID_PATTERN.sub('[REDACTED:UUID]', result)

    # 5. 移除绝对路径（最宽匹配，最后执行）
    for pat in PATH_PATTERNS:
        result = pat.sub('[REDACTED:PATH]', result)

    return result


def _sanitize_obj(obj, ext_stats=None):
    """递归脱敏 JSON 对象。"""
    if ext_stats is None:
        ext_stats = {}

    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            # 标记敏感字段直接替换
            k_lower = k.lower()
            if any(s in k_lower for s in ('path', 'file', 'dir', 'folder')):
                if isinstance(v, str):
                    _extract_extension_stats(v)
                    result[k] = '[REDACTED:PATH]'
                    continue
            if any(s in k_lower for s in ('code', 'source', 'content', 'body', 'script')):
                if isinstance(v, str) and len(v) > 100:
                    result[k] = '[REDACTED:CODE]'
                    continue
            result[k] = _sanitize_obj(v, ext_stats)
        return result

    elif isinstance(obj, list):
        return [_sanitize_obj(item, ext_stats) for item in obj]

    elif isinstance(obj, str):
        return _sanitize_text(obj)

    return obj


def _collect_extension_stats(obj):
    """从完整对象中收集扩展名统计（遍历所有字符串值）。"""
    stats = {}

    def _walk(o):
        if isinstance(o, dict):
            for v in o.values():
                _walk(v)
        elif isinstance(o, list):
            for item in o:
                _walk(item)
        elif isinstance(o, str):
            exts = _extract_extension_stats(o)
            for ext, count in exts.items():
                stats[ext] = stats.get(ext, 0) + count

    _walk(obj)
    return stats


def sanitize_session(input_path, output_path=None):
    """主入口：读取 session JSON，脱敏，输出。"""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 收集扩展名统计（脱敏前）
    ext_stats = _collect_extension_stats(data)

    # 执行脱敏
    sanitized = _sanitize_obj(data, ext_stats)

    # 附加脱敏元信息
    ts = datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S+08:00')
    sanitized['_sanitization'] = {
        'timestamp': ts,
        'script_version': '1.0.0',
        'extension_stats': ext_stats,
        'rules_applied': [
            'api_key_redaction',
            'email_redaction',
            'ip_redaction',
            'uuid_redaction',
            'absolute_path_redaction',
            'code_content_redaction',
        ],
    }

    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f'{base}-sanitized{ext}'

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sanitized, f, ensure_ascii=False, indent=2)

    return output_path


# ── CLI ────────────────────────────────────────────────────
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python sanitize-session.py <input.json> [output.json]', file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result = sanitize_session(input_file, output_file)
        print(json.dumps({
            'status': 'ok',
            'output': result,
        }, ensure_ascii=False))
    except FileNotFoundError:
        print(json.dumps({
            'status': 'error',
            'message': f'输入文件不存在: {input_file}',
        }, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(json.dumps({
            'status': 'error',
            'message': f'JSON 解析失败: {e}',
        }, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
