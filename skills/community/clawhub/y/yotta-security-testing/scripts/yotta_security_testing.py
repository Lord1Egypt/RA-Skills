#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yotta_security_testing.py — YottaMeta 元测（yotta-security-testing）Scope Guard CLI。

「有纪律的 AI 安全测试方法论」的硬产品机制：Scope Guard 五道防线之 CLI 层。
授权以 scope.json 为准（不信任对话口头声明）；未授权目标默认拒绝；操作留痕默认开启。

子命令：
  scope init      初始化授权清单（~/.yottasec/scope.json，默认 deny）
  scope check     目标三层判定：授权白名单 → 目标类型识别 → 默认拒绝
  scope list      查看授权条目
  scope add       添加授权条目（self-owned / ctf / bug-bounty / training / explicit）
  scope remove    移除授权条目（--target 或 --id）
  report generate 由 findings.json 生成漏洞报告（Markdown / JSON，敏感凭据脱敏）
  audit log       查看 / 过滤 / 导出操作留痕（默认开启，无 --no-audit）

设计原则：
- 纯 Python 3.8+ 标准库，零依赖；Windows / Linux / macOS 通用。
- 只做判定与报告：不发起任何网络请求、不执行目标代码、不输出可执行 payload。
- 行为锚点写死为默认行为。

exit code：
  0 = ALLOW（已授权放行）
  1 = DENY（未授权拒绝：白名单未命中 / 授权过期 / 高敏域名未 explicit）
  2 = DENY（绝对禁止：云元数据 / 管理面目标，白名单也无法覆盖）
  3 = 配置 / 用法 / 输入错误
  4 = 未初始化（scope.json 不存在）

用法示例：
  python3 yotta_security_testing.py scope init --owner demo
  python3 yotta_security_testing.py scope add --type ctf --target 127.0.0.1 --note dvwa
  python3 yotta_security_testing.py scope check http://127.0.0.1/dvwa
  python3 yotta_security_testing.py scope check example.com --json
  python3 yotta_security_testing.py report generate findings.json --out report.md
  python3 yotta_security_testing.py audit log --result deny --export audit-deny.jsonl
"""
import argparse
import getpass
import ipaddress
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

VERSION = "0.3.4"
TOOL_NAME = "yotta-security-testing"
CN_NAME = "元测"

AUTHORIZATION_TYPES = ("self-owned", "ctf", "bug-bounty", "training", "explicit")
SEVERITIES = ("critical", "high", "medium", "low", "info")

# ── exit code（行为锚点：未授权默认拒绝；云元数据绝对禁止）───────────────
EXIT_ALLOW = 0
EXIT_DENY_UNAUTHORIZED = 1
EXIT_DENY_FORBIDDEN = 2
EXIT_ERROR = 3
EXIT_NOT_INITIALIZED = 4

DEFAULT_CONFIG_DIR_NAME = ".yottasec"
SCOPE_FILENAME = "scope.json"
AUDIT_FILENAME = "audit.log"

# 设计 §4.2：明确禁止的云元数据 / 管理面目标 —— 白名单也无法覆盖
ABSOLUTE_DENY_HOSTS = (
    "169.254.169.254",  # AWS / GCP / Azure 云元数据
    "100.100.100.200",  # 阿里云 ECS 元数据
    "metadata.google.internal",
)

# 设计 §4.2：高敏域名后缀（.gov / .mil 等）需 --type explicit 显式授权
HIGH_SENSITIVITY_SECOND_LEVEL = ("gov", "mil")

# 防线 2：默认合法靶场 / 本地靶机特征名（仍需先授权才放行）
LAB_HOSTNAMES = {
    "dvwa", "juice-shop", "juiceshop", "juice_shop", "hackthebox", "htb",
    "vulnhub", "metasploitable", "metasploitable2", "metasploitable3",
    "bwapp", "webgoat", "mutillidae", "damn-vulnerable-web-app",
}
LOCALHOST_NAMES = {"localhost", "127.0.0.1", "127.0.0.2", "::1"}


class ScopeError(Exception):
    """带退出码的业务错误（配置 / 用法 / 输入）。"""

    def __init__(self, message, exit_code=EXIT_ERROR):
        super().__init__(message)
        self.exit_code = exit_code


# ── 配置与授权清单（~/.yottasec/scope.json）─────────────────────────────

def resolve_config_dir(config_dir=None):
    """解析配置目录：--config-dir > $YOTTASEC_DIR > ~/.yottasec。"""
    if config_dir:
        return Path(config_dir)
    env_dir = os.environ.get("YOTTASEC_DIR")
    if env_dir:
        return Path(env_dir)
    return Path.home() / DEFAULT_CONFIG_DIR_NAME


def scope_path(cfg_dir):
    return Path(cfg_dir) / SCOPE_FILENAME


def audit_path(cfg_dir):
    return Path(cfg_dir) / AUDIT_FILENAME


def load_scope(cfg_dir):
    """读取并校验授权清单；不存在 → exit 4（未初始化）。"""
    p = scope_path(cfg_dir)
    if not p.exists():
        raise ScopeError(
            "未初始化：缺少 %s\n请先运行：scope init --owner <你的名字>\n"
            "完整示例：python scripts/yotta_security_testing.py scope init --owner <你的名字>"
            % p, EXIT_NOT_INITIALIZED)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        raise ScopeError("scope.json 无法解析：%s" % e, EXIT_ERROR)
    if not isinstance(data, dict):
        raise ScopeError("scope.json 格式错误：应为 JSON 对象", EXIT_ERROR)
    if "version" in data and data["version"] != 1:
        raise ScopeError(
            "scope.json 版本不支持：%r（当前仅支持 version 1）" % data["version"],
            EXIT_ERROR)
    auth = data.get("authorization")
    if auth is None:
        auth = []
        data["authorization"] = auth
    if not isinstance(auth, list):
        raise ScopeError("scope.json 格式错误：authorization 应为数组", EXIT_ERROR)
    for i, entry in enumerate(auth):
        if not isinstance(entry, dict):
            raise ScopeError(
                "scope.json 格式错误：authorization[%d] 应为对象" % i, EXIT_ERROR)
        t = entry.get("type")
        if t not in AUTHORIZATION_TYPES:
            raise ScopeError(
                "scope.json 格式错误：authorization[%d] type=%r 非法" % (i, t),
                EXIT_ERROR)
        if not entry.get("target"):
            raise ScopeError(
                "scope.json 格式错误：authorization[%d] 缺 target" % i, EXIT_ERROR)
    return data


def save_scope(cfg_dir, scope):
    Path(cfg_dir).mkdir(parents=True, exist_ok=True)
    p = scope_path(cfg_dir)
    p.write_text(json.dumps(scope, ensure_ascii=False, indent=2) + "\n",
                 encoding="utf-8")


# ── 操作留痕（防线 5：默认开启，不可静默关闭）──────────────────────────

def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def audit(cfg_dir, action, **fields):
    """追加一条 JSONL 留痕（ts / tool / version / action + 业务字段）。"""
    Path(cfg_dir).mkdir(parents=True, exist_ok=True)
    entry = {"ts": now_iso(), "tool": TOOL_NAME, "version": VERSION,
             "action": action}
    entry.update(fields)
    with open(audit_path(cfg_dir), "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry

# ── 目标解析与分类（设计 §4.1 目标三层判定之类型识别）────────────────────

def split_target(raw):
    """归一化目标 → (host, port, path, scheme)；非法返回 None。

    支持：bare 域名 / IPv4 / IPv6（[::1]:8080）/ URL（含 scheme / userinfo / 端口 / 路径）。
    """
    if raw is None:
        return None
    raw = raw.strip()
    if not raw:
        return None
    scheme = ""
    rest = raw
    if "://" in raw:
        scheme, _, rest = raw.partition("://")
        if not rest:
            return None
    hostport = rest
    path = ""
    if "/" in rest:
        hostport, _, path = rest.partition("/")
        path = "/" + path
    if "@" in hostport:
        # 剥离 userinfo（user:pass@host）
        _, _, hostport = hostport.rpartition("@")
    hostport = hostport.strip()
    if not hostport:
        return None
    host = hostport
    port = ""
    if hostport.startswith("["):
        m = re.match(r"^\[([^\]]+)\](?::(\d+))?$", hostport)
        if not m:
            return None
        host = m.group(1)
        port = m.group(2) or ""
    elif hostport.count(":") == 1:
        h, _, maybe_port = hostport.partition(":")
        if maybe_port.isdigit():
            host = h
            port = maybe_port
    host = host.lower().rstrip(".")
    if not host:
        return None
    return host, port, path, scheme


def classify_target(host):
    """返回 (类型, 高敏标识)。

    类型：local-lab / private-network / link-local / public-domain /
          public-ip / cloud-metadata / reserved / unknown。
    """
    if host in ABSOLUTE_DENY_HOSTS:
        return "cloud-metadata", False
    if host in LOCALHOST_NAMES or host in LAB_HOSTNAMES:
        return "local-lab", False
    ip = None
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        ip = None
    if ip is not None:
        if ip.is_loopback:
            return "local-lab", False
        if ip.version == 4 and ip in ipaddress.ip_network("169.254.0.0/16"):
            return "link-local", False
        if ip.is_private:
            return "private-network", False
        if ip.is_link_local:
            return "link-local", False
        if ip.is_reserved or ip.is_multicast or ip.is_unspecified:
            return "reserved", False
        return "public-ip", False
    labels = host.split(".")
    if len(labels) < 2:
        return "unknown", False
    if host.endswith(".local") or host.endswith(".lan"):
        return "private-network", False
    high = (labels[-1] in HIGH_SENSITIVITY_SECOND_LEVEL
            or labels[-2] in HIGH_SENSITIVITY_SECOND_LEVEL)
    return "public-domain", high


def is_high_sensitivity(host):
    """目标是否为高敏域名（.gov / .mil 及其国家后缀，如 .gov.cn）。"""
    try:
        ipaddress.ip_address(host)
        return False
    except ValueError:
        pass
    labels = host.split(".")
    return (len(labels) >= 2
            and (labels[-1] in HIGH_SENSITIVITY_SECOND_LEVEL
                 or labels[-2] in HIGH_SENSITIVITY_SECOND_LEVEL))


# ── 授权白名单匹配（设计 §4.3 scope.json schema）────────────────────────

def host_matches(pattern, host):
    """域名匹配：精确 / *.example.com 通配（含主域与任意子域）。"""
    pattern = (pattern or "").strip().lower().rstrip(".")
    host = (host or "").lower().rstrip(".")
    if not pattern or not host:
        return False
    if pattern == host:
        return True
    if pattern.startswith("*."):
        base = pattern[2:]
        return host == base or host.endswith("." + base)
    return False


def ip_matches(pattern, host):
    """CIDR 匹配（10.0.0.0/24 等）；精确 IP 由 host_matches 处理。"""
    if "/" not in (pattern or ""):
        return False
    try:
        net = ipaddress.ip_network(pattern.strip(), strict=False)
    except ValueError:
        return False
    try:
        return ipaddress.ip_address(host) in net
    except ValueError:
        return False


def url_prefix_matches(pattern, raw, host, path):
    """URL / 路径前缀匹配：
    - "https://example.com/app" 匹配同前缀 URL；
    - "example.com/app" 匹配同 host 下的路径前缀。
    """
    p = (pattern or "").strip().lower().rstrip("/")
    if not p:
        return False
    if "://" in p:
        r = (raw or "").strip().lower().rstrip("/")
        if not r:
            return False
        return r == p or r.startswith(p + "/")
    if "/" in p:
        p_host, _, p_path = p.partition("/")
        p_host = p_host.lower().rstrip(".")
        if p_host != host:
            return False
        if not p_path.startswith("/"):
            p_path = "/" + p_path
        p_path = p_path.rstrip("/")
        if path == p_path:
            return True
        return path.startswith(p_path + "/")
    return False


def entry_matches(entry, host, port, path, raw):
    """授权条目（target / scope 字段任一命中）即匹配。"""
    for key in ("target", "scope"):
        p = (entry.get(key) or "").strip()
        if not p:
            continue
        if host_matches(p, host):
            return True
        if ip_matches(p, host):
            return True
        if url_prefix_matches(p, raw, host, path):
            return True
    return False


def find_match(scope, host, port, path, raw):
    """返回 (index, entry)；未命中 → (None, None)。"""
    for i, entry in enumerate(scope.get("authorization") or []):
        if entry_matches(entry, host, port, path, raw):
            return i, entry
    return None, None


def is_expired(entry, today=None):
    """expires = 最后有效日（含当日）；"never" / 缺省 = 不过期；无法解析视为过期。"""
    expires = entry.get("expires")
    if not expires or str(expires).strip().lower() == "never":
        return False
    today = today or date.today()
    try:
        exp = datetime.strptime(str(expires).strip(), "%Y-%m-%d").date()
    except ValueError:
        return True
    return today > exp


def validate_expires(expires):
    if not expires:
        return "never"
    expires = expires.strip()
    if expires.lower() == "never":
        return "never"
    try:
        d = datetime.strptime(expires, "%Y-%m-%d").date()
    except ValueError:
        raise ScopeError("expires 格式非法：应为 YYYY-MM-DD 或 never", EXIT_ERROR)
    if d < date.today():
        raise ScopeError("expires 早于今天：%s" % expires, EXIT_ERROR)
    return expires


def build_entry(args):
    """由 argparse 参数构造并校验授权条目。"""
    target = (args.target or "").strip()
    host, port, path, scheme = split_target(target)
    if host is None:
        raise ScopeError("target 非法：%r" % target, EXIT_ERROR)
    if host in ABSOLUTE_DENY_HOSTS:
        raise ScopeError(
            "禁止添加云元数据 / 管理面目标：%s" % host, EXIT_ERROR)
    if is_high_sensitivity(host) and args.type != "explicit":
        raise ScopeError(
            "高敏域名（.gov / .mil）需 --type explicit 显式授权", EXIT_ERROR)
    scope_field = (args.scope or "").strip() or target
    expires = validate_expires(args.expires)
    entry = {"type": args.type, "target": target,
             "scope": scope_field, "expires": expires}
    note = (args.note or "").strip()
    if note:
        entry["note"] = note
    return entry


def deny_hint(target_type, host):
    if target_type in ("local-lab", "private-network", "link-local"):
        return ("提示：本地靶场 / 内网目标也需先授权：scope add --type ctf|training|self-owned --target %s"
                % host)
    if target_type in ("public-domain", "public-ip"):
        return ("提示：公网目标需显式授权：scope add --type self-owned|bug-bounty|explicit --target %s"
                % host)
    return "提示：目标未识别或未授权，请确认目标并先在 scope.json 添加授权条目"


# ── 子命令：scope ────────────────────────────────────────────────────────

def cmd_scope_init(args):
    cfg_dir = resolve_config_dir(args.config_dir)
    p = scope_path(cfg_dir)
    if p.exists() and not args.force:
        raise ScopeError("scope.json 已存在：%s（使用 --force 覆盖）" % p, EXIT_ERROR)
    scope = {
        "version": 1,
        "owner": args.owner or getpass.getuser() or "unknown",
        "default_policy": "deny",
        "authorization": [],
    }
    if args.type:
        if not args.target:
            raise ScopeError("init 附带首个授权条目需 --target", EXIT_ERROR)
        scope["authorization"].append(build_entry(args))
    save_scope(cfg_dir, scope)
    audit(cfg_dir, "scope.init", owner=scope["owner"], target=args.target or "")
    print("已初始化授权清单: %s" % p)
    print("default_policy = deny（未授权目标默认拒绝）")
    return EXIT_ALLOW


def cmd_scope_add(args):
    cfg_dir = resolve_config_dir(args.config_dir)
    scope = load_scope(cfg_dir)
    entry = build_entry(args)
    auth = scope.setdefault("authorization", [])
    for e in auth:
        if (e.get("target") == entry["target"]
                and e.get("scope") == entry["scope"]
                and e.get("type") == entry["type"]):
            raise ScopeError(
                "该授权条目已存在（target=%s scope=%s type=%s）"
                % (entry["target"], entry["scope"], entry["type"]), EXIT_ERROR)
    auth.append(entry)
    save_scope(cfg_dir, scope)
    audit(cfg_dir, "scope.add", target=entry["target"], scope=entry["scope"],
          type=entry["type"], expires=entry["expires"])
    print("已添加授权条目 #%d: %s (type=%s, scope=%s, expires=%s)"
          % (len(auth), entry["target"], entry["type"],
             entry["scope"], entry["expires"]))
    return EXIT_ALLOW


def cmd_scope_remove(args):
    cfg_dir = resolve_config_dir(args.config_dir)
    scope = load_scope(cfg_dir)
    auth = scope.get("authorization") or []
    if args.id is not None:
        idx = args.id - 1
        if idx < 0 or idx >= len(auth):
            raise ScopeError("--id 越界：1-%d" % len(auth), EXIT_ERROR)
        entry = auth.pop(idx)
    else:
        target = (args.target or "").strip()
        if not target:
            raise ScopeError("需指定 --target 或 --id", EXIT_ERROR)
        matches = [i for i, e in enumerate(auth)
                   if e.get("target") == target or e.get("scope") == target]
        if not matches:
            raise ScopeError("未找到匹配条目: %s" % target, EXIT_ERROR)
        if len(matches) > 1:
            raise ScopeError(
                "多条匹配，请用 --id 指定（%s）"
                % ", ".join(str(i + 1) for i in matches), EXIT_ERROR)
        entry = auth.pop(matches[0])
    save_scope(cfg_dir, scope)
    audit(cfg_dir, "scope.remove", target=entry.get("target", ""),
          scope=entry.get("scope", ""))
    print("已移除授权条目: %s (type=%s)"
          % (entry.get("target", ""), entry.get("type", "")))
    return EXIT_ALLOW


def cmd_scope_list(args):
    cfg_dir = resolve_config_dir(args.config_dir)
    scope = load_scope(cfg_dir)
    auth = scope.get("authorization") or []
    if args.json:
        print(json.dumps({"version": scope.get("version"),
                          "owner": scope.get("owner"),
                          "default_policy": scope.get("default_policy"),
                          "authorization": auth}, ensure_ascii=False, indent=2))
        return EXIT_ALLOW
    print("owner=%s  default_policy=%s  授权条目 %d 条"
          % (scope.get("owner"), scope.get("default_policy"), len(auth)))
    if not auth:
        print("（空）用 scope add 添加授权")
        return EXIT_ALLOW
    for i, e in enumerate(auth, 1):
        note = ("  # %s" % e["note"]) if e.get("note") else ""
        print("%2d  %-11s %-30s scope=%s  expires=%s%s"
              % (i, e.get("type"), e.get("target"), e.get("scope"),
                 e.get("expires"), note))
    return EXIT_ALLOW


def cmd_scope_check(args):
    """目标三层判定（设计 §4.1）+ 内置黑名单（§4.2）+ 行为锚点（§4.4）。"""
    cfg_dir = resolve_config_dir(args.config_dir)
    scope = load_scope(cfg_dir)
    raw = args.target
    parsed = split_target(raw)
    if parsed is None:
        raise ScopeError("target 非法: %r" % raw, EXIT_ERROR)
    host, port, path, scheme = parsed
    # 绝对禁止：云元数据 / 管理面（白名单也无法覆盖）
    if host in ABSOLUTE_DENY_HOSTS:
        audit(cfg_dir, "scope.check", target=raw, host=host,
              result="deny", reason="absolute-deny")
        result = {"result": "deny", "reason": "absolute-deny",
                  "exit": EXIT_DENY_FORBIDDEN,
                  "message": "拒绝：%s 为云元数据 / 管理面目标，禁止测试（exit %d）"
                             % (host, EXIT_DENY_FORBIDDEN)}
    else:
        target_type, high = classify_target(host)
        idx, entry = find_match(scope, host, port, path, raw)
        if entry is not None and is_expired(entry):
            audit(cfg_dir, "scope.check", target=raw, host=host,
                  result="deny", reason="expired", entry_index=idx + 1)
            result = {"result": "deny", "reason": "expired",
                      "exit": EXIT_DENY_UNAUTHORIZED, "entry_index": idx + 1,
                      "message": "拒绝：命中授权条目 #%d 但已过期（expires=%s）"
                                 % (idx + 1, entry.get("expires"))}
        elif entry is not None and high and entry.get("type") != "explicit":
            audit(cfg_dir, "scope.check", target=raw, host=host,
                  result="deny", reason="high-sensitivity-needs-explicit",
                  entry_index=idx + 1, entry_type=entry.get("type"))
            result = {"result": "deny", "reason": "high-sensitivity-needs-explicit",
                      "exit": EXIT_DENY_UNAUTHORIZED, "entry_index": idx + 1,
                      "entry_type": entry.get("type"),
                      "message": "拒绝：%s 为高敏域名，授权条目 type=%s 需为 explicit"
                                 % (host, entry.get("type"))}
        elif entry is not None:
            audit(cfg_dir, "scope.check", target=raw, host=host,
                  result="allow", reason="whitelist", entry_index=idx + 1,
                  entry_type=entry.get("type"))
            result = {"result": "allow", "reason": "whitelist",
                      "exit": EXIT_ALLOW, "entry_index": idx + 1,
                      "entry_type": entry.get("type"),
                      "message": "放行：命中授权条目 #%d（type=%s, scope=%s, expires=%s）"
                                 % (idx + 1, entry.get("type"),
                                    entry.get("scope"), entry.get("expires"))}
        else:
            # 白名单未命中 → 默认拒绝（锚点：口头声明无效，授权以 scope.json 为准）
            audit(cfg_dir, "scope.check", target=raw, host=host,
                  result="deny", reason="not-authorized",
                  target_type=target_type)
            result = {"result": "deny", "reason": "not-authorized",
                      "exit": EXIT_DENY_UNAUTHORIZED, "target_type": target_type,
                      "message": "拒绝：%s（%s）未在授权清单（exit %d）"
                                 % (host, target_type, EXIT_DENY_UNAUTHORIZED),
                      "hint": deny_hint(target_type, host)}
    if args.json:
        payload = {"target": raw, "host": host}
        payload.update(result)
        print(json.dumps(payload, ensure_ascii=False))
        return result["exit"]
    print(result["message"])
    if result.get("hint"):
        print(result["hint"])
    return result["exit"]


# ── 敏感凭据脱敏（行为锚点：报告默认脱敏）────────────────────────────────

_FENCE = chr(96) * 3  # markdown 代码围栏（避免在源码中出现裸反引号）

_SECRET_KEY_RE = re.compile(
    r"(?i)\b(password|passwd|pwd|secret|token|api[_-]?key|apikey|access[_-]?token|"
    r"refresh[_-]?token|client[_-]?secret|auth[_-]?token|session[_-]?id|"
    r"private[_-]?key)\b\s*[=:]\s*(?:\"[^\"]*\"|'[^']*'|[^\s\"',;]+)")
_AUTH_HDR_RE = re.compile(r"(?i)\b(authorization|cookie)\s*[=:]\s*[^\s,;]+")
_BEARER_RE = re.compile(r"(?i)\bbearer\s+[a-z0-9._~+/=-]{6,}")
_URL_USERINFO_RE = re.compile(
    r"(?i)([a-z][a-z0-9+.-]*://[^/\s:@]+:)[^/\s@]+(@)")
_LONG_HEX_RE = re.compile(r"(?i)\b[0-9a-f]{16,}\b")
_LONG_B64_RE = re.compile(r"\b[A-Za-z0-9+/]{32,}={0,2}\b")
_REDACTED = "***REDACTED***"


def redact_text(text):
    """把文本中的口令 / token / 密钥 / 长十六进制 / 长 base64 掩码。"""
    if not isinstance(text, str):
        return text
    out = _SECRET_KEY_RE.sub(lambda m: m.group(1) + "=" + _REDACTED, text)
    out = _AUTH_HDR_RE.sub(lambda m: m.group(1) + "=" + _REDACTED, out)
    out = _BEARER_RE.sub("Bearer " + _REDACTED, out)
    out = _URL_USERINFO_RE.sub(r"\1" + _REDACTED + r"\2", out)
    out = _LONG_HEX_RE.sub(_REDACTED, out)
    out = _LONG_B64_RE.sub(_REDACTED, out)
    return out


_SENSITIVE_KEYS = frozenset((
    "password", "passwd", "pwd", "secret", "token", "api_key", "apikey",
    "access_token", "refresh_token", "client_secret", "authorization",
    "cookie", "session_id", "private_key", "set-cookie",
))


def redact_value(value):
    """递归脱敏（字符串 / 列表 / 字典 / 标量）。

    字典：键命中敏感名单（password / token / secret / cookie 等）时，
    整个值掩码，避免"password": "明文" 这类键值对泄露。
    """
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, list):
        return [redact_value(x) for x in value]
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            if str(k).lower() in _SENSITIVE_KEYS:
                out[k] = _REDACTED
            else:
                out[k] = redact_value(v)
        return out
    return value


def render_markdown(findings, target, generated_at, counts, scans=None):
    lines = []
    lines.append("# 漏洞评估与渗透测试报告")
    lines.append("")
    lines.append("- 目标：%s" % (redact_text(target) or "未指定"))
    lines.append("- 生成时间：%s" % generated_at)
    lines.append("- 生成工具：%s %s v%s（Scope Guard 已启用，敏感凭据已脱敏）"
                 % (CN_NAME, TOOL_NAME, VERSION))
    lines.append("")
    lines.append("## 摘要")
    lines.append("")
    lines.append("| 严重级 | 数量 |")
    lines.append("|---|---|")
    for sev in SEVERITIES:
        lines.append("| %s | %d |" % (sev, counts.get(sev, 0)))
    lines.append("")
    lines.append("共 %d 条发现。" % sum(counts.values()))
    lines.append("")
    if scans:
        lines.append("## 安全扫描联动")
        lines.append("")
        lines.append("| 工具 | 类型 | verdict | 关联报告 |")
        lines.append("|---|---|---|---|")
        for sc in scans:
            if not isinstance(sc, dict):
                continue
            tool = sc.get("tool") or "-"
            kind = sc.get("kind") or "-"
            verdict = sc.get("verdict") or "-"
            ref = sc.get("reference") or sc.get("report") or "-"
            lines.append("| %s | %s | %s | `%s` |" % (tool, kind, verdict, ref))
        lines.append("")
        lines.append("> 联动说明：本报告与元信（装前扫描）/ 元安（深度扫描）/ 元审（四阶段审查）"
                     "报告相互引用，形成「目标 → 扫描 → 测试 → 结论」的完整留痕链。")
        lines.append("")
    if not findings:
        lines.append("_暂无发现。_")
        return "\n".join(lines)
    for i, f in enumerate(findings, 1):
        lines.append("## 发现 %d：%s" % (i, f.get("title") or "(未命名)"))
        lines.append("")
        lines.append("- 严重级：%s" % f.get("severity"))
        lines.append("- 类别：%s" % (f.get("category") or "未指定"))
        if f.get("cwe"):
            lines.append("- CWE：%s" % f["cwe"])
        if f.get("owasp"):
            lines.append("- OWASP：%s" % f["owasp"])
        if f.get("endpoint") or f.get("url"):
            lines.append("- 端点：%s" % (f.get("endpoint") or f.get("url")))
        if f.get("target"):
            lines.append("- 目标：%s" % f["target"])
        lines.append("")
        lines.append("### 描述")
        lines.append("")
        lines.append(f.get("description") or "（无描述）")
        lines.append("")
        ev = f.get("evidence")
        if ev:
            lines.append("### 证据")
            lines.append("")
            if isinstance(ev, str):
                lines.append(ev)
            else:
                lines.append(_FENCE + "json")
                lines.append(json.dumps(ev, ensure_ascii=False, indent=2))
                lines.append(_FENCE)
            lines.append("")
        lines.append("### 修复建议")
        lines.append("")
        lines.append(f.get("remediation") or "（未提供，建议补充）")
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def cmd_report_generate(args):
    cfg_dir = resolve_config_dir(args.config_dir)
    src = Path(args.findings)
    if not src.exists():
        raise ScopeError("findings 文件不存在: %s" % src, EXIT_ERROR)
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except Exception as e:
        raise ScopeError("findings 无法解析：%s" % e, EXIT_ERROR)
    if isinstance(data, dict):
        target = data.get("target") or ""
        raw_findings = data.get("findings")
        if raw_findings is None:
            raw_findings = data.get("results") or []
        scans = data.get("scans")
        if scans is not None and not isinstance(scans, list):
            scans = None
    elif isinstance(data, list):
        target = ""
        raw_findings = data
        scans = None
    else:
        raise ScopeError("findings 应为对象或数组", EXIT_ERROR)
    if not isinstance(raw_findings, list):
        raise ScopeError("findings 字段应为数组", EXIT_ERROR)
    findings = []
    for i, f in enumerate(raw_findings):
        if not isinstance(f, dict):
            raise ScopeError("findings[%d] 应为对象" % i, EXIT_ERROR)
        sev = str(f.get("severity") or "info").lower()
        if sev not in SEVERITIES:
            raise ScopeError(
                "findings[%d] severity=%r 非法（可选：%s）"
                % (i, f.get("severity"), "/".join(SEVERITIES)), EXIT_ERROR)
        findings.append(redact_value(f))
    generated_at = now_iso()
    counts = {s: 0 for s in SEVERITIES}
    for f in findings:
        counts[str(f.get("severity") or "info").lower()] += 1
    if args.json:
        report = {
            "tool": "%s %s v%s" % (CN_NAME, TOOL_NAME, VERSION),
            "target": redact_text(target),
            "generated_at": generated_at,
            "summary": counts,
            "scans": scans or [],
            "findings": findings,
        }
        text = json.dumps(report, ensure_ascii=False, indent=2)
    else:
        text = render_markdown(findings, target, generated_at, counts, scans)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
        print("报告已写入: %s" % args.out)
    else:
        print(text)
    audit(cfg_dir, "report.generate", target=target or "", findings=len(findings),
          out=args.out or "")
    return EXIT_ALLOW


# ── 子命令：audit log ───────────────────────────────────────────────────

def cmd_audit_log(args):
    cfg_dir = resolve_config_dir(args.config_dir)
    p = audit_path(cfg_dir)
    if not p.exists():
        print("暂无操作留痕：%s" % p)
        return EXIT_ALLOW
    entries = []
    bad = 0
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except ValueError:
            bad += 1
    if args.action:
        entries = [e for e in entries
                   if args.action in (e.get("action") or "")]
    if args.target:
        entries = [e for e in entries
                   if args.target in (e.get("target") or "")]
    if args.result:
        entries = [e for e in entries if e.get("result") == args.result]
    if args.since:
        entries = [e for e in entries if (e.get("ts") or "")[:10] >= args.since]
    if args.until:
        entries = [e for e in entries if (e.get("ts") or "")[:10] <= args.until]
    if args.limit and args.limit > 0:
        entries = entries[-args.limit:]
    if args.export:
        Path(args.export).parent.mkdir(parents=True, exist_ok=True)
        Path(args.export).write_text(
            "\n".join(json.dumps(e, ensure_ascii=False) for e in entries)
            + ("\n" if entries else ""), encoding="utf-8")
        print("已导出 %d 条留痕: %s" % (len(entries), args.export))
        return EXIT_ALLOW
    if args.json:
        print(json.dumps({"total": len(entries), "entries": entries},
                         ensure_ascii=False, indent=2))
        return EXIT_ALLOW
    print("操作留痕 %d 条%s" % (len(entries),
                             "（%d 行解析失败）" % bad if bad else ""))
    for e in entries:
        print("%s  %-14s result=%-5s target=%s"
              % (e.get("ts", ""), e.get("action", ""),
                 e.get("result", "-"), e.get("target", "")))
    return EXIT_ALLOW

# ── CLI 入口 ─────────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog=TOOL_NAME,
        description="%s %s —— 有纪律的 AI 安全测试：Scope Guard 授权清单 + 目标判定 + 漏洞报告 + 操作留痕"
                    % (CN_NAME, TOOL_NAME))
    parser.add_argument("--version", action="store_true", help="显示版本")
    parser.add_argument("--config-dir",
                        help="覆盖配置目录（默认 ~/.yottasec 或 $YOTTASEC_DIR）")
    sub = parser.add_subparsers(dest="command")

    p_scope = sub.add_parser("scope", help="Scope Guard 授权清单与目标判定")
    sscope = p_scope.add_subparsers(dest="scope_command", required=True)

    p_init = sscope.add_parser("init", help="初始化授权清单（默认 deny）")
    p_init.add_argument("--owner", help="使用者标识")
    p_init.add_argument("--force", action="store_true",
                        help="覆盖已存在的 scope.json")
    p_init.add_argument("--type", choices=AUTHORIZATION_TYPES,
                        help="可选：随 init 附带首个授权条目类型")
    p_init.add_argument("--target")
    p_init.add_argument("--scope")
    p_init.add_argument("--expires", help="YYYY-MM-DD 或 never（默认 never）")
    p_init.add_argument("--note")
    p_init.set_defaults(func=cmd_scope_init)

    p_check = sscope.add_parser(
        "check", help="目标三层判定：授权白名单 → 类型识别 → 默认拒绝")
    p_check.add_argument("target")
    p_check.add_argument("--json", action="store_true")
    p_check.set_defaults(func=cmd_scope_check)

    p_list = sscope.add_parser("list", help="查看授权条目")
    p_list.add_argument("--json", action="store_true")
    p_list.set_defaults(func=cmd_scope_list)

    p_add = sscope.add_parser("add", help="添加授权条目")
    p_add.add_argument("--type", choices=AUTHORIZATION_TYPES, required=True)
    p_add.add_argument("--target", required=True)
    p_add.add_argument("--scope", help="授权范围（默认 = target）")
    p_add.add_argument("--expires", help="YYYY-MM-DD 或 never（默认 never）")
    p_add.add_argument("--note")
    p_add.set_defaults(func=cmd_scope_add)

    p_remove = sscope.add_parser("remove", help="移除授权条目（--target 或 --id）")
    p_remove.add_argument("--target")
    p_remove.add_argument("--id", type=int, help="条目序号（1 起）")
    p_remove.set_defaults(func=cmd_scope_remove)

    p_report = sub.add_parser("report", help="漏洞报告")
    sreport = p_report.add_subparsers(dest="report_command", required=True)
    p_gen = sreport.add_parser(
        "generate", help="由 findings.json 生成报告（Markdown / JSON，敏感凭据脱敏）")
    p_gen.add_argument("findings")
    p_gen.add_argument("--json", action="store_true", help="输出 JSON 报告")
    p_gen.add_argument("--out", help="写入文件")
    p_gen.set_defaults(func=cmd_report_generate)

    p_audit = sub.add_parser("audit", help="操作留痕")
    saudit = p_audit.add_subparsers(dest="audit_command", required=True)
    p_log = saudit.add_parser("log", help="查看 / 过滤 / 导出操作留痕")
    p_log.add_argument("--action", help="按动作过滤（如 scope.check）")
    p_log.add_argument("--target", help="按目标过滤（子串）")
    p_log.add_argument("--result", choices=("allow", "deny"))
    p_log.add_argument("--since", help="YYYY-MM-DD（含）")
    p_log.add_argument("--until", help="YYYY-MM-DD（含）")
    p_log.add_argument("--limit", type=int, help="最近 N 条")
    p_log.add_argument("--json", action="store_true")
    p_log.add_argument("--export", help="导出到文件（JSONL）")
    p_log.set_defaults(func=cmd_audit_log)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version:
        print("%s %s v%s" % (CN_NAME, TOOL_NAME, VERSION))
        return EXIT_ALLOW
    if not getattr(args, "command", None):
        parser.print_help()
        return EXIT_ERROR
    try:
        return args.func(args)
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else EXIT_ERROR
        # argparse 用法错误（choices / 缺参数等）统一归为用法错误
        return EXIT_ERROR if code == 2 else code
    except ScopeError as e:
        print("错误：%s" % e, file=sys.stderr)
        return e.exit_code
    except Exception as e:  # noqa: BLE001
        print("错误：%s" % e, file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
