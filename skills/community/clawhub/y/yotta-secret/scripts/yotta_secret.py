#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yotta-secret（元钥）—— 零依赖自研密钥 / 凭据泄露源头扫描引擎
================================================================

跨智能体的密钥泄露源头扫描：用「正则 + 熵 + 格式校验」离线扫描源代码 / 配置文件 /
.env / 文本中的疑似密钥与凭据，覆盖 云厂商 API Key、私钥、通用口令赋值、
URL 内嵌凭据、高熵长 token 五类。

特性
----
- 五类规则：cloud（云厂商 / SaaS API Key）、private_key（PEM / OpenSSH / PuTTY 私钥）、
  credential（password / secret / token 等赋值）、url_userinfo（URL 内嵌账号密码）、
  generic（高熵长 token）
- 正则 + 熵 + 格式校验三重判定，占位符 / 示例值过滤，误报可控
- 输出默认打码（--show-secret 才明文），text / JSON / CSV 三种格式
- 子命令：scan（文件 / 目录 / stdin / git 历史）、verify（单值判定）、mask（脱敏）、
  entropy（信息熵）
- 与元史 yotta-logs 脱敏共享词库：mask 输出与元史 redact 行为一致（本引擎规则为超集）
- 纯本地离线：不联网查询、不发送任何数据（红线）

用法
----
  python3 scripts/yotta_secret.py scan --path src/
  python3 scripts/yotta_secret.py scan --stdin --format json
  python3 scripts/yotta_secret.py scan --git --path repo/ --format json --output report.json
  python3 scripts/yotta_secret.py scan --path . --types cloud,private_key --show-secret
  python3 scripts/yotta_secret.py verify --value ghp_xxxxxxxxxxxxxxxx
  python3 scripts/yotta_secret.py entropy --value abc123
  python3 scripts/yotta_secret.py mask --path notes.txt --output safe.txt
  python3 scripts/yotta_secret.py --version

退出码：scan 0 = 未发现；1 = 发现疑似密钥；4 = 用法 / 读取 / git 不可用错误。
verify：0 = 未命中规则；1 = 命中规则；4 = 用法错误。mask / entropy：0 = 成功；4 = 错误。
Windows 下用 python 代替 python3。
"""

import argparse
import csv
import fnmatch
import io
import json
import math
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone

try:
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VERSION = "0.2.4"
TOOL = "yotta-secret"
TOOL_CN = "元钥"

EXIT_CLEAN = 0
EXIT_FOUND = 1
EXIT_ERROR = 4

CATEGORY_ORDER = ("cloud", "private_key", "credential", "url_userinfo", "generic")
CATEGORY_LABELS = {
    "cloud": "云厂商 / SaaS 密钥",
    "private_key": "私钥",
    "credential": "凭据赋值",
    "url_userinfo": "URL 内嵌凭据",
    "generic": "高熵长 Token",
}
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


# ── 工具函数 ──────────────────────────────────────────────────────────────

def shannon_entropy(s):
    """Shannon 信息熵（bit / char）。"""
    if not s:
        return 0.0
    n = len(s)
    if n == 0:
        return 0.0
    cnt = Counter(s)
    return -sum((c / n) * math.log2(c / n) for c in cnt.values())


_PLACEHOLDER_RE = re.compile(
    r"^(?i:"
    r"<[^>]*>"
    r"|(?:your|my|our)[_-]?[a-z]+"
    r"|xxx+|\*+|\?+"
    r"|change[_-]?me|replace[_-]?me|changeme|todo"
    r"|example[_-]?[a-z0-9]*|sample|dummy|fake|demo|test[a-z0-9]*"
    r"|null|none|n/a|true|false|yes|no|undefined|nil"
    r"|\d{1,4}"
    r"|(?:password|passwd|pwd|secret|token|api[_-]?key|apikey|"
    r"access[_-]?key|auth[_-]?token|client[_-]?secret|private[_-]?key)"
    r"|(?:\$\{?[a-z0-9_]+}?|env\([^)]*\)|os\.environ(?:\[[^\]]*\])?|"
    r"process\.env(?:\.\w+)?|getenv\([^)]*\)|config\([^)]*\)|settings\([^)]*\))"
    r")$")


def is_placeholder(value):
    """判断值是否为占位符 / 示例 / 环境变量引用（不当作真密钥）。"""
    v = value.strip().strip("'\"")
    return bool(_PLACEHOLDER_RE.match(v))


# 可安全保留的类型前缀（ghp_ / sk- / AKIA? 不保留无分隔符前缀）
_SECRET_PREFIX_RE = re.compile(r"^([A-Za-z][A-Za-z0-9]{1,7}[_-])")


def mask_secret(value):
    """打码：只保留可识别的类型前缀（如 ghp_ / sk-），其余全部遮蔽。

    v0.2.1：旧行为保留首尾各 4 个字符，长密钥仍会露出 8 个字符明文；
    现在默认全遮，只有 --show-secret 才输出原文。
    """
    v = value.strip()
    if not v:
        return "****"
    m = _SECRET_PREFIX_RE.match(v)
    prefix = m.group(1) if m else ""
    if len(prefix) > 8:
        prefix = prefix[:8]
    return prefix + "****"


def masked_snippet(text, span, display):
    """用打码后的值替换命中片段，生成可安全展示的上下文。"""
    try:
        masked = text[:span[0]] + display + text[span[1]:]
    except (IndexError, TypeError):
        return display
    return masked.strip()[:200]


# ── 规则 ──────────────────────────────────────────────────────────────────

class Rule:
    __slots__ = ("id", "name", "category", "severity", "re", "group", "mask", "multi")

    def __init__(self, rid, name, category, severity, pattern, group=1, mask=True, multi=False):
        self.id = rid
        self.name = name
        self.category = category
        self.severity = severity
        self.re = re.compile(pattern, re.S if multi else 0)
        self.group = group
        self.mask = mask
        self.multi = multi


# 行级规则（逐行扫描，能给出准确行号）
LINE_RULES = [
    # ── cloud：云厂商 / SaaS API Key ──
    Rule("aws_access_key", "AWS 访问密钥 ID", "cloud", "high",
         r"\b(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[0-9A-Z]{16}\b"),
    Rule("aws_secret", "AWS 秘密访问密钥", "cloud", "critical",
         r"(?i)\baws[_-]?secret[_-]?access[_-]?key\b\s*[=:]\s*[\"']?([A-Za-z0-9/+=]{40})[\"']?"),
    Rule("google_api", "Google API Key", "cloud", "high",
         r"\bAIza[0-9A-Za-z\-_]{35}\b"),
    Rule("openai", "OpenAI API Key", "cloud", "high",
         r"\bsk-(?!(?:ant-))[A-Za-z0-9_-]{20,}\b"),
    Rule("anthropic", "Anthropic API Key", "cloud", "high",
         r"\bsk-ant-[A-Za-z0-9_-]{20,}\b"),
    Rule("stripe", "Stripe API Key", "cloud", "high",
         r"\b(?:sk|rk|pk)_(?:live|test)_[0-9A-Za-z]{16,}\b"),
    Rule("slack", "Slack Token", "cloud", "high",
         r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b"),
    Rule("github", "GitHub Token", "cloud", "critical",
         r"\bgh[pousr]_[0-9A-Za-z]{36,}\b|\bgithub_pat_[0-9A-Za-z_]{20,}\b"),
    Rule("gitlab", "GitLab Token", "cloud", "high",
         r"\bglpat-[0-9A-Za-z\-_]{20,}\b"),
    Rule("npm_token", "npm Token", "cloud", "high",
         r"\bnpm_[0-9A-Za-z]{36}\b"),
    Rule("pypi_token", "PyPI Token", "cloud", "high",
         r"\bpypi-AgEIcHlwaS5vcmc[A-Za-z0-9\-_]{50,}\b"),
    Rule("telegram_bot", "Telegram Bot Token", "cloud", "high",
         r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b"),
    Rule("jwt", "JWT", "cloud", "high",
         r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    Rule("huggingface", "HuggingFace Token", "cloud", "high",
         r"\bhf_[A-Za-z0-9]{30,}\b"),
    Rule("notion", "Notion Token", "cloud", "high",
         r"\b(?:secret_[A-Za-z0-9]{40,}|ntn_[0-9A-Za-z]{24,})\b"),
    Rule("shopify", "Shopify Token", "cloud", "high",
         r"\bshpat_[0-9a-fA-F]{32}\b"),
    Rule("sendgrid", "SendGrid API Key", "cloud", "high",
         r"\bSG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}\b"),
    Rule("twilio", "Twilio API Key", "cloud", "high",
         r"\bSK[0-9a-fA-F]{32}\b"),
    Rule("mailgun", "Mailgun API Key", "cloud", "high",
         r"\bkey-[0-9a-zA-Z]{32}\b"),
    Rule("sendinblue", "Sendinblue API Key", "cloud", "high",
         r"\bxkeysib-[0-9a-fA-F]{64}-[A-Za-z0-9_-]{16}\b"),
    Rule("digitalocean", "DigitalOcean Token", "cloud", "high",
         r"\bdop_v1_[0-9a-fA-F]{64}\b"),
    Rule("pagerduty", "PagerDuty Token", "cloud", "high",
         r"\bpdus_[A-Za-z0-9_-]{20,}\b"),
    Rule("azure_storage", "Azure 存储账户密钥", "cloud", "critical",
         r"(?i)\bAccountKey\s*=\s*[\"']?([A-Za-z0-9+/=]{80,})[\"']?"),
    Rule("bearer", "Bearer Token", "cloud", "high",
         r"(?i)\bbearer\s+([a-z0-9._~+/=-]{20,})\b"),
    Rule("basic_auth", "HTTP Basic 认证", "cloud", "medium",
         r"(?i)\bbasic\s+([a-z0-9+/]{16,}={0,2})"),

    # ── credential：通用口令赋值（key = value）──
    Rule("credential", "凭据赋值", "credential", "high",
         r"(?i)(?:\b(?P<key>password|passwd|pwd|secret|api[_-]?key|apikey|"
         r"access[_-]?key|accesskey|auth[_-]?token|client[_-]?secret|client[_-]?key|"
         r"private[_-]?key|consumer[_-]?(?:key|secret)|refresh[_-]?token|"
         r"app[_-]?secret|secret[_-]?key|signing[_-]?key|session[_-]?token|"
         r"db[_-]?password|root[_-]?password|admin[_-]?password|user[_-]?password|"
         r"smtp[_-]?(?:password|pass)|ftp[_-]?password|redis[_-]?password|"
         r"mysql[_-]?password|pg[_-]?password|mongo[_-]?password|proxy[_-]?password|"
         r"encryption[_-]?key|master[_-]?key|webhook[_-]?(?:secret|token)|"
         r"oauth[_-]?client[_-]?secret|id[_-]?token|access[_-]?token|"
         r"_authToken|_password|auth_token|token)\b|"
         r"[A-Za-z0-9._-]+[_-](?P<key2>password|passwd|pwd|secret|token|pass|key|"
         r"api[_-]?key|access[_-]?key|auth[_-]?token|client[_-]?secret|"
         r"private[_-]?key|refresh[_-]?token))"
         r"\s*[:=]\s*[\"']?(?P<val>[^\"'\s,;]{4,})",
         group="val"),

    # ── url_userinfo：URL 内嵌账号密码 ──
    Rule("url_userinfo", "URL 内嵌账号密码", "url_userinfo", "high",
         r"\b(?:https?|ftp|smtp|imaps?|pop3s?|ldaps?|mongodb(?:\+srv)?|redis|rediss|"
         r"mysql|postgres(?:ql)?|mssql|amqp|amqps|jdbc:[a-z0-9]+)://"
         r"([^/\s:@]+):([^/\s@]+)@",
         group=2),

    # ── generic：高熵长 token（代码内再校验）──
    Rule("generic", "高熵长 Token", "generic", "medium",
         r"\b[A-Za-z0-9+/=_-]{32,}\b"),
]

# 块级规则（跨行匹配，如 PEM 私钥）
BLOCK_RULES = [
    Rule("pem_private", "PEM 私钥块", "private_key", "critical",
         r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----",
         group=0, multi=True),
    Rule("pgp_private", "PGP 私钥块", "private_key", "critical",
         r"-----BEGIN PGP PRIVATE KEY BLOCK-----.*?-----END PGP PRIVATE KEY BLOCK-----",
         group=0, multi=True),
    Rule("putty_ppk", "PuTTY 私钥", "private_key", "critical",
         r"PuTTY-User-Key-File-[23][^\n]*\n(?:[^\n]*\n){0,20}?Private-Lines:\s*\d+",
         group=0, multi=True),
]


def _generic_ok(value):
    """generic 规则的值级校验：排除纯哈希 / UUID / 低熵。"""
    v = value.strip().strip("=")
    if len(v) < 32:
        return False
    if re.fullmatch(r"[0-9a-fA-F]{32}|[0-9a-fA-F]{40}|[0-9a-fA-F]{64}|[0-9a-fA-F]{128}", v):
        return False
    if re.fullmatch(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", v):
        return False
    return shannon_entropy(v) >= 4.0


# ── 脱敏（mask 子命令；与元史 yotta-logs redact 同源，规则为超集）────────

_URL_RE = re.compile(r"(https?://[^\s\"'<>]+)", re.I)
_URL_USERPASS_RE = re.compile(r"(https?://)([^/\s:@]+):([^/\s@]+)@", re.I)


def _inside_url(line, pos):
    """pos 是否落在 URL（https?://...）区间内（URL 路径/查询串不算密钥）。"""
    for um in _URL_RE.finditer(line):
        if um.start() <= pos < um.end():
            return True
    return False


def redact_text(text):
    """把疑似密钥打码（默认动作；与元史脱敏词库保持一致）。"""
    if not text:
        return text
    # 块级：私钥整块替换
    for r in BLOCK_RULES:
        if r.mask:
            text = r.re.sub("[PRIVATE KEY REDACTED]", text)
    # URL 内嵌口令
    text = _URL_USERPASS_RE.sub(r"\1\2:***@", text)
    chunks = _URL_RE.split(text)
    out = []
    for i, chunk in enumerate(chunks):
        if i % 2 == 1:
            out.append(chunk)  # URL 原文保留（路径不算密钥）
            continue
        for r in LINE_RULES:
            if not r.mask:
                continue
            def _rep(m, _r=r):
                if _r.id == "credential":
                    off = m.start("val") - m.start(0)
                    return m.group(0)[:off] + "***"
                if _r.id == "generic" and not _generic_ok(m.group(1)):
                    return m.group(0)
                return "***"
            chunk = r.re.sub(_rep, chunk)
        out.append(chunk)
    return "".join(out)


# ── 读取 ──────────────────────────────────────────────────────────────────

DEFAULT_SKIP_DIRS = frozenset({
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env", "dist", "build",
    ".tox", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".next", ".nuxt", ".cache",
    ".idea", "target", ".tmp", ".gitlab", "coverage", ".DS_Store",
})

BINARY_EXT = frozenset({
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".bmp", ".pdf",
    ".zip", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".rar", ".tar", ".jar", ".war",
    ".class", ".so", ".dll", ".exe", ".dylib", ".o", ".a", ".lib", ".pyc", ".pyo",
    ".woff", ".woff2", ".ttf", ".otf", ".eot", ".mp3", ".mp4", ".avi", ".mov",
    ".mkv", ".wav", ".flac", ".db", ".sqlite", ".sqlite3", ".mdb", ".accdb",
    ".iso", ".img", ".dmg", ".apk", ".deb", ".rpm", ".msi", ".crx", ".lockb",
    ".parquet", ".avro", ".orc", ".min.js", ".min.css",
})


def read_text(path, max_size):
    """读取文本文件；二进制 / 超大文件返回 None。"""
    try:
        with open(path, "rb") as f:
            head = f.read(8192)
            if b"\x00" in head:
                return None
            f.seek(0)
            data = f.read()
    except OSError:
        return None
    if len(data) > max_size:
        return None
    for enc in ("utf-8-sig", "utf-8", "gb18030", "latin-1"):
        try:
            return data.decode(enc)
        except (UnicodeDecodeError, ValueError):
            continue
    return data.decode("latin-1", errors="replace")


def _match_excludes(rel_path, basename, patterns):
    for pat in patterns:
        if "/" not in pat:
            if fnmatch.fnmatch(basename, pat) or fnmatch.fnmatch(rel_path, pat):
                return True
        elif fnmatch.fnmatch(rel_path, pat) or fnmatch.fnmatch(rel_path.replace("\\", "/"), pat):
            return True
    return False


# ── 扫描 ──────────────────────────────────────────────────────────────────

def _line_no(text, pos):
    return text.count("\n", 0, pos) + 1


def _apply_rule_line(rule, line, fname, lineno, opts, findings, key_cache, line_values):
    for m in rule.re.finditer(line):
        try:
            value = m.group(rule.group)
        except IndexError:
            value = m.group(0)
        value = value.strip()
        if not value:
            continue
        if rule.id == "generic":
            if not _generic_ok(value):
                continue
            # URL 路径/查询串不算密钥（与 mask 的 URL 原文保留口径一致）
            if _inside_url(line, m.start()):
                continue
            # 与同行已命中的更具体规则重叠（如 JWT 各段 / ghp_ 前缀）则跳过
            if any(v in value or value in v for v in line_values):
                continue
        if rule.category == "credential":
            if is_placeholder(value):
                continue
            try:
                key = m.group("key") or m.group("key2") or ""
            except IndexError:
                key = m.group(1) or ""
            if key.strip().lower() in ("token", "auth_token"):
                # 中等置信 key：要求更长或更高熵，降低噪音
                if len(value) < 16 and shannon_entropy(value) < 3.5:
                    continue
            elif len(value) < opts.min_length:
                continue
        if rule.category == "url_userinfo":
            user = m.group(1)
            if is_placeholder(value) or user.strip().lower() in ("user", "username", "login"):
                continue
        if rule.category == "cloud" and rule.id == "basic_auth":
            try:
                import base64
                decoded = base64.b64decode(value + "=" * (-len(value) % 4), validate=True)
                if b":" not in decoded:
                    continue
            except Exception:
                continue
        # 通用去重：同文件同行的同规则同值只报一次
        dedupe_key = (rule.id, value, fname, lineno)
        if dedupe_key in key_cache:
            continue
        key_cache.add(dedupe_key)
        try:
            span = m.span(rule.group)
        except IndexError:
            span = m.span(0)
        line_values.add(value)
        display = value if opts.show_secret else mask_secret(value)
        snippet = masked_snippet(line, span, display)
        findings.append({
            "rule_id": rule.id,
            "rule_name": rule.name,
            "category": rule.category,
            "severity": rule.severity,
            "file": fname,
            "line": lineno,
            "secret": display,
            "length": len(value),
            "entropy": round(shannon_entropy(value), 3),
            "snippet": snippet[:200],
            "commit": "",
            "path_in_commit": "",
        })


def _apply_rule_block(rule, text, fname, opts, findings, key_cache):
    for m in rule.re.finditer(text):
        value = m.group(rule.group)
        if not value:
            continue
        lineno = _line_no(text, m.start())
        dedupe_key = (rule.id, value[:60], fname, lineno)
        if dedupe_key in key_cache:
            continue
        key_cache.add(dedupe_key)
        display = "[PRIVATE KEY REDACTED]"
        if opts.show_secret:
            display = value[:12] + "...(%d chars)" % len(value)
        # v0.2.1：默认上下文只给打码标记 —— 旧行为把私钥正文前 200 字符原样写进
        # findings.snippet（报告默认打印），等于泄露密钥本体。
        snippet = display
        findings.append({
            "rule_id": rule.id,
            "rule_name": rule.name,
            "category": rule.category,
            "severity": rule.severity,
            "file": fname,
            "line": lineno,
            "secret": display,
            "length": len(value),
            "entropy": round(shannon_entropy(value), 3),
            "snippet": snippet,
            "commit": "",
            "path_in_commit": "",
        })


def scan_text(text, fname, opts, commit="", path_in_commit=""):
    findings = []
    key_cache = set()
    for rule in BLOCK_RULES:
        _apply_rule_block(rule, text, fname, opts, findings, key_cache)
    for lineno, line in enumerate(text.splitlines(), start=1):
        line_values = set()
        for rule in LINE_RULES:
            _apply_rule_line(rule, line, fname, lineno, opts, findings, key_cache,
                             line_values)
    # 去重：同一文件同一行同一 secret 只保留一条（严重度优先）
    findings = _dedupe_findings(findings)
    for f in findings:
        if commit:
            f["commit"] = commit
        if path_in_commit:
            f["path_in_commit"] = path_in_commit
    return findings


def walk_files(paths, opts):
    """遍历文件 / 目录，产出 (path, rel_path, basename)。"""
    out = []
    for p in paths:
        if os.path.isfile(p):
            out.append((p, os.path.basename(p), os.path.basename(p)))
            continue
        if not os.path.isdir(p):
            sys.stderr.write("[warn] 路径不存在: %s\n" % p)
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in DEFAULT_SKIP_DIRS]
            for fn in files:
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, p)
                out.append((full, rel, fn))
    return out


def git_scan(path, opts):
    """扫描 git 历史：git log -p --all，只扫新增行。"""
    repo = path or "."
    try:
        r = subprocess.run(
            ["git", "-C", repo, "log", "-p", "--all", "--"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if r.returncode != 0:
        return None
    text = r.stdout.decode("utf-8", errors="replace")
    findings = []
    commit = ""
    cur_path = ""
    for raw in text.splitlines():
        line = raw
        if line.startswith("commit ") and len(line) > 7:
            commit = line.split()[1][:12]
            cur_path = ""
            continue
        if line.startswith("+++ b/") and len(line) > 6:
            cur_path = line[6:]
            continue
        if line.startswith("+") and not line.startswith("+++"):
            content = line[1:]
            for rule in LINE_RULES:
                for m in rule.re.finditer(content):
                    try:
                        value = m.group(rule.group).strip()
                    except IndexError:
                        value = m.group(0).strip()
                    if not value:
                        continue
                    if rule.id == "generic" and not _generic_ok(value):
                        continue
                    if rule.category == "credential":
                        if is_placeholder(value):
                            continue
                    if rule.category == "url_userinfo":
                        user = m.group(1)
                        if is_placeholder(value) or user.strip().lower() in ("user", "username", "login"):
                            continue
                    display = value if opts.show_secret else mask_secret(value)
                    try:
                        span = m.span(rule.group)
                    except IndexError:
                        span = m.span(0)
                    findings.append({
                        "rule_id": rule.id,
                        "rule_name": rule.name,
                        "category": rule.category,
                        "severity": rule.severity,
                        "file": cur_path,
                        "line": 0,
                        "secret": display,
                        "length": len(value),
                        "entropy": round(shannon_entropy(value), 3),
                        "snippet": masked_snippet(content, span, display),
                        "commit": commit,
                        "path_in_commit": cur_path,
                    })
    return findings


# ── 输出 ──────────────────────────────────────────────────────────────────

def _dedupe_findings(findings):
    """同一文件同一行同一 secret 只保留一条：按严重度优先，同严重度保留非 generic。"""
    best = {}
    for f in findings:
        key = (f["file"], f["line"], f["secret"])
        if key not in best:
            best[key] = f
            continue
        cur = best[key]
        if SEVERITY_ORDER.get(f["severity"], 9) < SEVERITY_ORDER.get(cur["severity"], 9):
            best[key] = f
        elif (SEVERITY_ORDER.get(f["severity"], 9) == SEVERITY_ORDER.get(cur["severity"], 9)
              and f["rule_id"] != "generic" and cur["rule_id"] == "generic"):
            best[key] = f
    return list(best.values())


def _sort_findings(findings):
    return sorted(
        findings,
        key=lambda f: (f["file"], f["line"], SEVERITY_ORDER.get(f["severity"], 9),
                       f["rule_id"], f["secret"]))


def _summary(findings):
    s = {"total": len(findings)}
    for sev in ("critical", "high", "medium", "low"):
        s[sev] = sum(1 for f in findings if f["severity"] == sev)
    return s


def render_text(findings, sources):
    lines = []
    lines.append("%s %s %s — 密钥扫描结果" % (TOOL_CN, TOOL, VERSION))
    lines.append("来源: %s" % (", ".join(sources) if sources else "-"))
    sm = _summary(findings)
    lines.append("共 %d 处疑似密钥（critical %d / high %d / medium %d / low %d）"
                 % (sm["total"], sm["critical"], sm["high"], sm["medium"], sm["low"]))
    lines.append("")
    if not findings:
        lines.append("未发现疑似密钥。")
        return "\n".join(lines)
    for cat in CATEGORY_ORDER:
        cat_findings = [f for f in _sort_findings(findings) if f["category"] == cat]
        if not cat_findings:
            continue
        lines.append("[%s]" % CATEGORY_LABELS[cat])
        for f in cat_findings:
            loc = f["file"] if f["file"] else f["path_in_commit"]
            if f["line"]:
                loc = "%s:%d" % (loc, f["line"])
            if f["commit"]:
                loc = "%s @ %s" % (loc, f["commit"])
            lines.append("  [%s] %s  %s" % (f["severity"], f["rule_name"], loc))
            lines.append("    密钥: %s" % f["secret"])
            lines.append("    熵: %.3f | 长度: %d" % (f["entropy"], f["length"]))
            if f["snippet"]:
                lines.append("    上下文: %s" % f["snippet"])
        lines.append("")
    return "\n".join(lines)


def render_json(findings, sources):
    hit_rules = []
    seen = set()
    for f in _sort_findings(findings):
        if f["rule_id"] not in seen:
            seen.add(f["rule_id"])
            hit_rules.append({
                "id": f["rule_id"],
                "name": f["rule_name"],
                "category": f["category"],
                "severity": f["severity"],
            })
    return {
        "tool": TOOL,
        "version": VERSION,
        "generated": datetime.now(timezone.utc).isoformat(),
        "source": sources,
        "summary": _summary(findings),
        "findings": _sort_findings(findings),
        "rules": hit_rules,
    }


def render_csv(findings):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["rule_id", "rule_name", "category", "severity", "file", "line",
                "secret", "entropy", "length", "snippet", "commit", "path_in_commit"])
    for f in _sort_findings(findings):
        w.writerow([f["rule_id"], f["rule_name"], f["category"], f["severity"],
                    f["file"], f["line"], f["secret"], f["entropy"], f["length"],
                    f["snippet"], f["commit"], f["path_in_commit"]])
    return buf.getvalue()


def _emit(text, output):
    if output:
        with open(output, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")


# ── 子命令 ────────────────────────────────────────────────────────────────

CATEGORY_ALIASES = {
    "cloud": "cloud", "云": "cloud", "云厂商": "cloud",
    "private_key": "private_key", "私钥": "private_key", "key": "private_key",
    "credential": "credential", "凭据": "credential", "口令": "credential",
    "url_userinfo": "url_userinfo", "url": "url_userinfo", "url凭据": "url_userinfo",
    "generic": "generic", "高熵": "generic", "长token": "generic",
}


def _parse_types(types_str):
    if not types_str:
        return None
    out = []
    for t in types_str.split(","):
        t = t.strip().lower()
        if t in CATEGORY_ALIASES:
            out.append(CATEGORY_ALIASES[t])
    return set(out) if out else None


def _types_enabled(rule, enabled):
    return enabled is None or rule.category in enabled


def cmd_scan(args):
    if not args.path and not args.stdin and not args.git:
        sys.stderr.write("用法错误: scan 需要 --path / --stdin / --git 之一\n")
        return EXIT_ERROR
    enabled = _parse_types(args.types)
    max_bytes = args.max_size * 1024 * 1024
    findings = []
    sources = []

    if args.stdin:
        text = sys.stdin.read()
        sources.append("<stdin>")
        findings.extend(scan_text(text, "<stdin>", args))
    if args.path:
        for full, rel, base in walk_files(args.path, args):
            if _match_excludes(rel, base, args.exclude):
                continue
            if os.path.splitext(base)[1].lower() in BINARY_EXT:
                continue
            text = read_text(full, max_bytes)
            if text is None:
                continue
            sources.append(full)
            findings.extend(scan_text(text, full, args))
    if args.git:
        gf = git_scan(args.path[0] if args.path else ".", args)
        if gf is None:
            sys.stderr.write("错误: git 不可用或不是 git 仓库（--git 需要已安装 git）\n")
            return EXIT_ERROR
        findings.extend(gf)
        sources.append("git history")

    # --types 过滤（scan_text 按全局规则集扫描，这里按类别收窄）
    if enabled:
        findings = [f for f in findings if f["category"] in enabled]
    # 汇总后统一去重（覆盖 git 模式）+ 排序
    findings = _dedupe_findings(findings)
    findings = _sort_findings(findings)
    if args.format == "json":
        data = render_json(findings, sources)
        _emit(json.dumps(data, ensure_ascii=False, indent=2), args.output)
    elif args.format == "csv":
        _emit(render_csv(findings), args.output)
    else:
        _emit(render_text(findings, sources), args.output)
    return EXIT_FOUND if findings else EXIT_CLEAN


def cmd_verify(args):
    values = []
    if args.value:
        values.append(args.value)
    if args.stdin:
        values.extend(line.rstrip("\r\n") for line in sys.stdin if line.strip())
    if not values:
        sys.stderr.write("用法错误: verify 需要 --value 或 --stdin\n")
        return EXIT_ERROR
    results = []
    hit = False
    for v in values:
        found = []
        for rule in LINE_RULES:
            for m in rule.re.finditer(v):
                try:
                    value = m.group(rule.group)
                except IndexError:
                    value = m.group(0)
                if not value:
                    continue
                if rule.id == "generic" and not _generic_ok(value):
                    continue
                if rule.category == "credential" and is_placeholder(value):
                    continue
                found.append({"rule_id": rule.id, "rule_name": rule.name,
                              "category": rule.category, "severity": rule.severity})
        ent = round(shannon_entropy(v), 3)
        verdict = "likely_secret" if found else ("high_entropy" if (ent >= 4.0 and len(v) >= 32) else "no_match")
        if found:
            hit = True
        results.append({"value": v if args.show_secret else mask_secret(v),
                        "length": len(v), "entropy": ent, "verdict": verdict,
                        "matches": found})
    if args.format == "json":
        _emit(json.dumps({"tool": TOOL, "version": VERSION, "results": results},
                         ensure_ascii=False, indent=2), args.output)
    else:
        lines = []
        for r in results:
            tags = ",".join(x["rule_id"] for x in r["matches"]) or "-"
            lines.append("%s\tverdict=%s\tentropy=%.3f\tmatches=%s"
                         % (r["value"], r["verdict"], r["entropy"], tags))
        _emit("\n".join(lines) + "\n", args.output)
    return EXIT_FOUND if hit else EXIT_CLEAN


def cmd_mask(args):
    if not args.path and not args.stdin:
        sys.stderr.write("用法错误: mask 需要 --path 或 --stdin\n")
        return EXIT_ERROR
    chunks = []
    if args.stdin:
        chunks.append(redact_text(sys.stdin.read()))
    if args.path:
        for full, rel, base in walk_files(args.path, args):
            text = read_text(full, 10 * 1024 * 1024)
            if text is not None:
                chunks.append(redact_text(text))
    _emit("".join(chunks), args.output)
    return EXIT_CLEAN


def cmd_entropy(args):
    values = []
    if args.value:
        values.append(args.value)
    if args.stdin:
        values.extend(line.rstrip("\r\n") for line in sys.stdin if line.strip())
    if not values:
        sys.stderr.write("用法错误: entropy 需要 --value 或 --stdin\n")
        return EXIT_ERROR
    for v in values:
        sys.stdout.write("%.4f\n" % shannon_entropy(v))
    return EXIT_CLEAN


# ── 入口 ──────────────────────────────────────────────────────────────────

def build_parser():
    p = argparse.ArgumentParser(
        prog=TOOL,
        description="%s（%s）—— 零依赖密钥 / 凭据泄露源头扫描引擎" % (TOOL_CN, TOOL))
    p.add_argument("--version", action="store_true", help="显示版本")
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("scan", help="扫描文件 / 目录 / stdin / git 历史中的疑似密钥")
    sp.add_argument("--path", action="append", default=[], metavar="PATH")
    sp.add_argument("--stdin", action="store_true", help="从标准输入读取")
    sp.add_argument("--git", action="store_true", help="扫描 git 历史（需要 git 命令）")
    sp.add_argument("--types", default="", metavar="a,b",
                    help="只检测指定类别: cloud,private_key,credential,url_userinfo,generic")
    sp.add_argument("--format", choices=("text", "json", "csv"), default="text")
    sp.add_argument("--output", default="", metavar="FILE", help="写入文件（默认打印）")
    sp.add_argument("--show-secret", action="store_true", help="明文显示密钥（默认打码）")
    sp.add_argument("--min-entropy", type=float, default=3.5, metavar="N",
                    help="凭据赋值检测最低熵（默认 3.5）")
    sp.add_argument("--min-length", type=int, default=8, metavar="N",
                    help="凭据赋值检测最短值长度（默认 8）")
    sp.add_argument("--exclude", action="append", default=[], metavar="GLOB",
                    help="排除路径模式（可多次，fnmatch）")
    sp.add_argument("--max-size", type=int, default=5, metavar="MB",
                    help="跳过超过此大小的文件（默认 5MB）")

    vp = sub.add_parser("verify", help="判定单个值是否为疑似密钥")
    vp.add_argument("--value", default="", metavar="VALUE")
    vp.add_argument("--stdin", action="store_true", help="每行一个值")
    vp.add_argument("--format", choices=("text", "json"), default="text")
    vp.add_argument("--output", default="", metavar="FILE")
    vp.add_argument("--show-secret", action="store_true")

    mp = sub.add_parser("mask", help="把文本中疑似密钥打码（与元史脱敏同源）")
    mp.add_argument("--path", action="append", default=[], metavar="PATH")
    mp.add_argument("--stdin", action="store_true")
    mp.add_argument("--output", default="", metavar="FILE")

    ep = sub.add_parser("entropy", help="计算文本的 Shannon 信息熵")
    ep.add_argument("--value", default="", metavar="VALUE")
    ep.add_argument("--stdin", action="store_true", help="每行一个值")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.version:
        sys.stdout.write("%s %s\n" % (TOOL, VERSION))
        return EXIT_CLEAN
    if not getattr(args, "cmd", None):
        build_parser().print_help(sys.stderr)
        return EXIT_ERROR
    if args.cmd == "scan":
        return cmd_scan(args)
    if args.cmd == "verify":
        return cmd_verify(args)
    if args.cmd == "mask":
        return cmd_mask(args)
    if args.cmd == "entropy":
        return cmd_entropy(args)
    build_parser().print_help(sys.stderr)
    return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
