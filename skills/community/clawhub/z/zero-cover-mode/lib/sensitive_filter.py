"""零稀泥模式 — 敏感数据过滤 sensitive_filter.py

Usage:
    python sensitive_filter.py check <file_path>
    python sensitive_filter.py filter <file_path> [output_path]
"""

import re, sys, os, logging

log = logging.getLogger("sensitive")


def _redact_users(match):
    """替换 Windows 用户路径中的用户名（反斜杠/正斜杠兼容，保留原始分隔符风格）

    P0-E: 检测原始路径的分隔符风格（/ 或 \），脱敏后保持一致。
    """
    path = match.group(0)
    # 检测原始分隔符风格
    has_forward = '/' in path
    # 标准化为正斜杠再分割
    normalized = path.replace('\\', '/')
    parts = normalized.split('/')
    for i, part in enumerate(parts):
        if part.lower() == 'users' and i + 1 < len(parts):
            username = parts[i + 1]
            # P2-4: 跳过已知的非用户名系统目录（黑名单模式，其余一律脱敏）
            SYSTEM_SUBDIRS = {'public', 'default', 'default user', 'all users'}
            if username.lower() in SYSTEM_SUBDIRS:
                continue
            parts[i + 1] = '[REDACTED]'
            break
    # 保留原始分隔符（P0-E）
    separator = '/' if has_forward else '\\'
    return separator.join(parts)


def _redact_value(match):
    """替换敏感值，只保留 key+分隔符"""
    try:
        return match.group(1) + "[REDACTED]"
    except IndexError:
        log.warning("_redact_value 触发了意外的 IndexError: match=%s", match.group(0))
        return "[REDACTED]"


def _redact_url(match):
    """替换 URL 中的凭证"""
    url = match.group(0)
    # 用 **** 替换 user:password@ 部分
    return re.sub(r'://[^:]+:[^@]+@', '://[REDACTED]:[REDACTED]@', url)


# P4-1: 扩展敏感模式列表
SENSITIVE_PATTERNS = [
    # 通用 key/secret/token/password 变体（驼峰/下划线）
    (r'(?i)(\b(?:[-a-z_]+(?:key|secret|token|password|pwd|credential|auth))'
     r'\s*[=:]\s*)(?:"[^"]{4,}"|\'[^\']{4,}\'|\S{8,})', _redact_value),

    # 带空格的 key = value 格式
    (r'(?i)(\b(?:api_?key|secret|password|access_key|client_secret|app_secret'
     r'|private_key|secret_key)\s*[:=]\s*)(?:"[^"]*"|\'[^\']*\'|\S+)',
     _redact_value),

    # token 单独处理（排除 token_count 等）
    (r'(?i)(\btoken\s*[=:]\s*)(?:"[^"]*"|\'[^\']*\'|\S+)', _redact_value),

    # auth 前缀
    (r'(?i)(\bauth(?:_key|_token|_secret)?\s*[=:]\s*)'
     r'(?:"[^"]*"|\'[^\']*\'|\S+)', _redact_value),

    # Windows 用户路径（反斜杠 + 正斜杠兼容）
    (r'(?i)[a-z]:[\\/]users[\\/][^\\/]+(?:[\\/][^\s"\'<>|:]+)*', _redact_users),
    # P5: Linux /home/username 路径
    (r'(?i)/home/[^/\s"\'<>|:]+(?:/[^\s"\'<>|:]+)*', '[REDACTED-HOME-PATH]'),
    # P5: macOS /Users/username 路径
    (r'(?i)/Users/[^/\s"\'<>|:]+(?:/[^\s"\'<>|:]+)*', '[REDACTED-USERS-PATH]'),
    # P5: Linux /root/ 路径
    (r'(?i)/root(?:/[^\s"\'<>|:]+)*', '[REDACTED-ROOT-PATH]'),

    # AWS Access Key
    (r'(?i)AKIA[0-9A-Z]{16}', '[REDACTED-AWS-KEY]'),

    # SSH 私钥头部
    (r'-----BEGIN\s+(?:RSA|DSA|EC|OPENSSH|SSH2)\s+PRIVATE\s+KEY-----',
     '[REDACTED-SSH-KEY-HEADER]'),

    # 密码环境变量
    (r'(?i)((?:DB_|MYSQL_|POSTGRES_|REDIS_)?'
     r'(?:PASSWORD|PWD)|SECRET_KEY)\s*[=:]\s*'
     r'(?:"[^"]*"|\'[^\']*\'|\S+)', _redact_value),

    # 带密码的 URL（非贪婪匹配，防止吞掉后续标点）
    (r'https?://[^:]+:[^@]+@\S+?', _redact_url),

    # 连接串（P1-F: 排除函数调用值）
    (r'(?i)((?:connection_string|conn_str|dsn'
     r'|database_url|DATABASE_URL)\s*[:=])\s*'
     r'(?!\w+\()(?:"[^"]*"|\'[^\']*\'|\S+)', _redact_value),

    # URI 方案中包含凭据（通用）
    (r'(?i)((?:mongodb|mysql|postgres|redis|rabbitmq|amqp)://)'
     r'[^:]+:[^@]+@', '[REDACTED-CREDENTIALS]://'),

    # OpenAI / API key
    (r'(?i)sk-[a-zA-Z0-9]{20,}', "[REDACTED-API-KEY]"),

    # JWT（要求 eyJ header 前缀，避免 base64 三段误报）
    (r'(?i)eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.|[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]+',
     "[REDACTED-JWT]"),

    # GitHub PAT（ghp_/ghu_/ghs_ + github_pat_ 新格式）
    (r'(?i)(?:gh[psu]_|github_pat_)[a-zA-Z0-9]{36,}', "[REDACTED-GH-TOKEN]"),
]


def filter_sensitive(text):
    for pattern, replacement in SENSITIVE_PATTERNS:
        try:
            if callable(replacement):
                text = re.sub(pattern, replacement, text)
            else:
                text = re.sub(pattern, replacement, text)
        except Exception as e:
            log.warning("敏感过滤正则失败 %s: %s", pattern, e)
    return text


def check_file(filepath):
    """扫描文件中的敏感数据"""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    matches = []
    for i, line in enumerate(lines, 1):
        for pattern, _ in SENSITIVE_PATTERNS:
            try:
                if re.search(pattern, line):
                    matches.append((i, line.strip()[:80]))
                    break
            except Exception:
                continue
    return matches


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="敏感数据过滤器")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("check", help="扫描敏感数据")
    p.add_argument("file_path")

    p = sub.add_parser("filter", help="过滤敏感数据")
    p.add_argument("file_path")
    p.add_argument("output_path", nargs="?")

    args = parser.parse_args()

    try:
        if args.command == "check":
            matches = check_file(args.file_path)
            if matches:
                print(f"发现 {len(matches)} 处潜在敏感数据:")
                for lineno, snippet in matches:
                    print(f"  第{lineno}行: {snippet}")
            else:
                print("OK: 未发现敏感数据")
        elif args.command == "filter":
            with open(args.file_path, "r", encoding="utf-8",
                      errors="replace") as f:
                content = f.read()
            filtered = filter_sensitive(content)
            out = args.output_path or args.file_path
            with open(out, "w", encoding="utf-8") as f:
                f.write(filtered)
            print(f"OK: 已过滤 -> {out}")
    except Exception as e:
        log.error("执行失败: %s", e)
        sys.exit(1)
