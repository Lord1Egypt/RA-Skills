#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yotta-logwatch（元察）—— 零依赖自研安全日志分析检测引擎
============================================================

跨智能体的安全日志分析能力：对本地日志文件做只读、离线、非入侵式分析，检测常见的
登录爆破 / Web 攻击扫描 / 可疑 PowerShell 脚本块，输出带中文教学说明的时间线与报告。

特性
----
- 四类日志解析：auth/secure（sshd、login、sudo…）、Web 访问日志（common/combined）、
  PowerShell 脚本块日志（Event 4104/4103、CommandInvocation、ScriptBlockText 等）、
  Windows 事件日志（Security/System，key=value / wevtutil 文本 / XML 单行导出）
- 检测规则（启发式，教学向）：
  * auth：失败登录聚合 / 同源爆破 / 时间窗内多账号撞库 / 异常登录 / sudo 提权
  * web：404 洪峰 / 扫描器特征 / webshell 上传轨迹 / 路径遍历 / SQL 注入 / 可疑 UA
  * powershell：编码命令 / 下载执行 / 反射加载 / AMSI 绕过 / 混淆启发式
- 时间线排序 + 命中规则中文说明 + 文本 / JSON / Markdown 报告
- 只读本地日志文件；不联网、不主动扫描、不修改任何其内容（红线）

用法
----
  python3 scripts/yotta_logwatch.py scan --path /var/log/auth.log
  python3 scripts/yotta_logwatch.py scan --path /var/log/nginx/access.log --recursive
  python3 scripts/yotta_logwatch.py scan --path . --format markdown --output report.md
  type access.log | python3 scripts/yotta_logwatch.py scan --stdin
  python3 scripts/yotta_logwatch.py scan --path auth.log --min-severity medium
  python3 scripts/yotta_logwatch.py --version

退出码：0 = 无命中；1 = 有命中；4 = 用法或读取错误。
Windows 下用 python 代替 python3。
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from urllib.parse import unquote

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

VERSION = "0.3.3"
TOOL = "yotta-logwatch"
TOOL_CN = "元察"

# 严重度级别：从低到高。findings 用它排序，--min-severity 用它过滤。
SEVERITY_ORDER = ["info", "low", "medium", "high", "critical"]
SEVERITY_RANK = {name: i for i, name in enumerate(SEVERITY_ORDER)}

# 事件类别
KIND_AUTH = "auth"
KIND_WEB = "web"
KIND_POWERSHELL = "powershell"
KIND_WINEVT = "winevt"        # Windows 事件日志（Security/System）

# ---------------------------------------------------------------------------
# 常量（检测阈值，均可由 CLI 覆盖）
# ---------------------------------------------------------------------------
DEFAULT_WINDOW = 300          # 聚合时间窗（秒）
DEFAULT_MAX_FAIL = 5          # 同源失败登录多少次算爆破
DEFAULT_404_THRESHOLD = 20    # 同源 404 多少次算洪峰

# 扫描器 / 自动化工具 UA 特征（小写匹配）
SCANNER_UA = [
    "sqlmap", "nuclei", "nikto", "masscan", "zgrab", "nmap", "dirbuster",
    "gobuster", "ffuf", "wfuzz", "wpscan", "joomscan", "acunetix", "nessus",
    "openvas", "python-requests", "go-http-client", "python-urllib", "curl",
    "wget", "libwww-perl", "scrapy", "httpclient", "aiohttp", "httpie",
    "lwp", "jbrofuzz", "fuzzdb", "censys", "shodan", "cobalt",
]

# 扫描 / 探测常见路径片段（小写、子串匹配）
SCANNER_PATH = [
    "/wp-login.php", "/wp-admin", "/wp-content", "/administrator",
    "/phpmyadmin", "/pma", "/mysql", "/admin", "/login", "/manager",
    "/cgi-bin", "/.git", "/.env", "/.svn", "/.htaccess", "/phpinfo.php",
    "/phpunit", "/actuator", "/console", "/backup", "/dump", "/test",
    "/explorer", "/vendor", "/config", "/server-status", "/server-info",
    "/xmlrpc.php", "/.well-known", "/robots.txt", "/webdav", "/shell",
    "/shell.php", "/cmd", "/debug", "/xdebug", "/phpmyadmin",
]

# 可疑 webshell 相关路径片段（上传 / 执行）
WEBSHELL_PATH = [
    "/shell.php", "/cmd.php", "/eval", "/webshell", "/backdoor",
    "/c99.php", "/r57.php", "/wso", "/b374k", "/uploads/shell",
    "/hack.php", "/shell.asp", "/shell.jsp", "/jsp/cmd", "/marco",
]

# 路径遍历特征
TRAVERSAL = ["../", "..%2f", "..%5c", "%2e%2e%2f", "%2e%2e%5c", "%252e%252e",
             "..%2F", "..%252f", "%c0%ae%c0%ae", "%c0%ae", "dotdot"]

# SQL 注入特征（小写、子串匹配）
SQLI = ["union select", "or 1=1", "or 1=1--", "1=1", "sleep(", "benchmark(",
        "information_schema", "@@version", "concat(", "group_concat",
        "' or '", "or '1'='1", "union all select", "procedure analyse",
        "and 1=1", "waitfor delay", "pg_sleep", "0x3a", "load_file(",
        "into outfile", "=1 or", "=1 and", "cast(", "char(", "convert(",
        "xp_cmdshell", "%27", "'%20or%20", "1%27"]

# PowerShell 脚本块日志的特征标记（出现任一即视为 PowerShell 类）
POWERSHELL_MARKERS = [
    "scriptblock", "commandinvocation", "eventid=4104", "eventid 4104",
    "eventid=4103", "eventid 4103", "powershell", "scriptblocktext",
    "create scriptblock", "hostapplication=consolehost", "scopeid=",
]

# PowerShell 常见命令 / 算子（用于 OPS 语义判断）
PS_CMDS = [
    "invoke-expression", "iex", "invoke-webrequest", "iwr", "downloadstring",
    "start-bitstransfer", "bitsadmin", "certutil", "add-type", "new-object",
    "invoke-command", "register-scheduledtask", "set-content", "out-file",
    "net.webclient", "system.net.webclient", "activation",
]

# Windows 事件日志记录的特征标记（key=value / wevtutil 文本 / XML 单行等导出形态）
# 强标记：单独出现即高度疑似事件记录；弱标记：需与其它标记组合，避免误判普通文本。
WINEVT_STRONG_MARKERS = [
    "microsoft-windows-security-auditing",   # Security 审计提供方
    "<event",                                # XML 事件记录
    "eventrecordid=",
    "eventrecordid:",
    "security id:",                          # 事件正文 Subject 字段
    "subjectusersid",
    "targetusername",
]
WINEVT_WEAK_MARKERS = [
    "eventid=",
    "<eventid",
    "event id:",
    "providername=",
    "provider name=",
    "log name:",
    "logname=",
    "channel=",
    "task category:",
    "keywords:",
    "logon type:",
    "ipaddress:",
    "new process name:",
    "computer:",
]
# 出现这些标记的行优先按 PowerShell 脚本块处理（Event 4104/4103 记录仍走 powershell 检测）
WINEVT_EXCLUDE_MARKERS = ["scriptblocktext", "commandinvocation", "scriptblock"]

# ---------------------------------------------------------------------------
# 时间解析
# ---------------------------------------------------------------------------

MONTH_ABBR = {m.lower(): i for i, m in enumerate([
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}


def _now_year():
    return datetime.now().year


def parse_syslog_time(text):
    """解析 syslog 风格 'Mon dd hh:mm:ss'，返回 datetime（年份取当前年）。

    无法解析时返回 None。
    """
    m = re.search(r"([A-Za-z]{3})\s+(\d{1,2})\s+(\d{2}):(\d{2}):(\d{2})", text)
    if not m:
        return None
    mon = MONTH_ABBR.get(m.group(1).lower())
    if not mon:
        return None
    try:
        return datetime(_now_year(), mon, int(m.group(2)),
                        int(m.group(3)), int(m.group(4)), int(m.group(5)))
    except ValueError:
        return None


def parse_web_time(text):
    """解析 Web 日志 'dd/Mon/yyyy:hh:mm:ss +zzzz'，返回 datetime。

    也兼容 'dd/Mon/yyyy:hh:mm:ss'（无时区）。无法解析时返回 None。
    """
    text = text.strip()
    m = re.search(r"(\d{1,2})/([A-Za-z]{3})/(\d{4}):(\d{2}):(\d{2}):(\d{2})",
                  text)
    if not m:
        return None
    mon = MONTH_ABBR.get(m.group(2).lower())
    if not mon:
        return None
    try:
        return datetime(int(m.group(3)), mon, int(m.group(1)),
                        int(m.group(4)), int(m.group(5)), int(m.group(6)))
    except ValueError:
        return None


def parse_iso_time(text):
    """解析 ISO 8601 / 'yyyy-mm-dd hh:mm:ss'，返回 datetime。"""
    text = text.strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(text[:len(fmt)], fmt)
        except ValueError:
            continue
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})", text)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                            int(m.group(4)), int(m.group(5)), int(m.group(6)))
        except ValueError:
            return None
    return None


def parse_time(text):
    """通用时间解析：依次尝试 web / syslog / ISO。"""
    for fn in (parse_web_time, parse_syslog_time, parse_iso_time):
        dt = fn(text)
        if dt:
            return dt
    return None


# ---------------------------------------------------------------------------
# 类型嗅探与单行解析
# ---------------------------------------------------------------------------

AUTH_MARKERS = [
    "failed password", "accepted password", "accepted publickey",
    "authentication failure", "sshd[", "pam_unix", "sudo:",
    "session opened for user", "invalid user", "systemd-logind",
    "su[", "new user", "useradd", "login[",
]

# Web access log（common/combined）正则
WEB_RE = re.compile(
    r"^(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<ts>[^\]]+)\]\s+"
    r'"(?P<req>[^"]*)"\s+(?P<status>\d{3})\s+(?P<size>\S+)'
    r'(?:\s+"(?P<referer>[^"]*)"\s+"(?P<ua>[^"]*)")?'
)

IP_RE = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3})")
# 支持带冒号源端口：from 1.2.3.4 port 1234
IP_PORT_RE = re.compile(r"(?:from|host=)\s+(\d{1,3}(?:\.\d{1,3}){3})")


def _ip_in(text):
    """从文本里提取第一个 IPv4。找不到返回 None。"""
    m = IP_PORT_RE.search(text)
    if m:
        return m.group(1)
    m = IP_RE.search(text)
    return m.group(1) if m else None


def sniff_type(line):
    """判断一行日志属于哪一类。返回 KIND_* 或 None。"""
    low = line.lower()
    if WEB_RE.match(line):
        return KIND_WEB
    # Windows 事件记录优先于 auth/powershell 关键字嗅探：防止 4688 等事件行因含
    # "powershell" 字样被误判为 PowerShell 脚本块；Event 4104 脚本块记录仍走 powershell。
    if _looks_like_winevt(line):
        return KIND_WINEVT
    for marker in AUTH_MARKERS:
        if marker in low:
            return KIND_AUTH
    for marker in POWERSHELL_MARKERS:
        if marker in low:
            return KIND_POWERSHELL
    return None


def _split_syslog(line):
    """拆 syslog 行：返回 (timestamp, hostname, rest)。失败返回 (None, None, line)。"""
    m = re.match(r"^([A-Za-z]{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(.+)$",
                 line)
    if not m:
        return None, None, line
    return m.group(1), m.group(2), m.group(3)


def parse_auth_line(line, host):
    """解析一条 auth/secure 日志。返回事件字典或 None。"""
    ts_str, _hostname, rest = _split_syslog(line)
    ts = parse_syslog_time(ts_str) if ts_str else None
    low = rest.lower()

    outcome = None
    if any(k in low for k in ("failed password", "authentication failure",
                              "failed password for invalid user",
                              "did not receive identification",
                              "connection reset by peer",
                              "maximum authentication attempts")):
        outcome = "failed"
    elif any(k in low for k in ("accepted password", "accepted publickey",
                                "accepted keyboard-interactive",
                                "session opened for user")):
        outcome = "success"
    if "sudo:" in low:
        if any(k in low for k in ("command=", "session opened for user",
                                  "not in sudoers", "authentication failure",
                                  "root")):
            outcome = outcome or "sudo"

    # 提取用户名
    user = None
    for pat in (r"for invalid user\s+([^\s]+)",
                r"for\s+([^\s]+)\s+from",
                r"for user\s+([^\s]+)",
                r"user\s+([^\s]+)\s+from",
                r"user\s+'([^']+)'"):
        m = re.search(pat, low)
        if m:
            user = m.group(1)
            break
    # sudo 常见形态
    if not user:
        m = re.search(r"\(([^)]+)\)\s+(?:RUN|COMMAND)", low)
        if m:
            user = m.group(1)
        elif "sudo:" in low:
            m = re.search(r"user\s+([a-z0-9_.-]+)", low)
            if m:
                user = m.group(1)

    source = _ip_in(rest)
    return {
        "kind": KIND_AUTH,
        "ts": ts,
        "ts_raw": ts_str,
        "line": line,
        "host": host,
        "source": source,
        "user": user,
        "outcome": outcome,
        "message": rest,
    }


def parse_web_line(line, host):
    """解析一条 Web 访问日志（common/combined）。返回事件字典或 None。"""
    m = WEB_RE.match(line)
    if not m:
        return None
    req = m.group("req")
    method = None
    uri = None
    proto = None
    if req and req != "-":
        parts = req.split(" ")
        if len(parts) >= 2:
            method = parts[0]
            uri = parts[1]
            proto = parts[2] if len(parts) >= 3 else None
    ts = parse_web_time(m.group("ts"))
    status_raw = m.group("status")
    try:
        status = int(status_raw)
    except ValueError:
        status = 0
    return {
        "kind": KIND_WEB,
        "ts": ts,
        "ts_raw": m.group("ts"),
        "line": line,
        "host": host,
        "source": m.group("ip"),
        "method": method,
        "uri": uri,
        "proto": proto,
        "status": status,
        "status_raw": status_raw,
        "size": m.group("size"),
        "referer": m.group("referer"),
        "ua": m.group("ua"),
        "message": line,
    }


def parse_powershell_line(line, host):
    """解析一行 PowerShell 脚本块 / 命令日志。返回事件字典或 None。"""
    ts = None
    ts_raw = None
    for fn, name in ((parse_syslog_time, "syslog"),
                     (parse_iso_time, "iso"),
                     (parse_web_time, "web")):
        candidate = line[:60]
        dt = fn(candidate)
        if dt:
            ts = dt
            ts_raw = candidate.strip()
            break
    return {
        "kind": KIND_POWERSHELL,
        "ts": ts,
        "ts_raw": ts_raw,
        "line": line,
        "host": host,
        "source": None,
        "user": None,
        "outcome": None,
        "message": line,
    }


WINEVT_ISO_RE = re.compile(r"((?:19|20)\d{2}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?)")


def _winevt_field(text, names):
    """从 Windows 事件行提取字段值：key=value / 'Name: value' / XML <Data Name="..">。

    在原始文本上做大小写不敏感匹配，保留字段值原始大小写；找不到返回 None。
    """
    for name in names:
        m = re.search(r"<data\s+name=\"%s\">([^<]*)</data>" % re.escape(name), text,
                      re.IGNORECASE)
        if m:
            return m.group(1).strip() or None
        # 优先取引号包裹的完整值（命令行等含空格的字段）
        m = re.search(r"%s\s*[:=]\s*\"([^\"]*)\"" % re.escape(name), text,
                      re.IGNORECASE)
        if m:
            return m.group(1).strip() or None
        m = re.search(r"%s\s*[:=]\s*'([^']*)'" % re.escape(name), text,
                      re.IGNORECASE)
        if m:
            return m.group(1).strip() or None
        m = re.search(r"%s\s*[:=]\s*\"?([^\"\s,]+)" % re.escape(name), text,
                      re.IGNORECASE)
        if m:
            return m.group(1).strip('"')
    return None


def _looks_like_winevt(line):
    """判断一行是否为 Windows 事件日志记录（排除 PowerShell 脚本块行）。"""
    low = line.lower()
    strong = sum(1 for m in WINEVT_STRONG_MARKERS if m in low)
    weak = sum(1 for m in WINEVT_WEAK_MARKERS if m in low)
    if strong + weak < 2:
        return False
    if any(m in low for m in WINEVT_EXCLUDE_MARKERS):
        return False
    return True


def parse_winevt_line(line, host):
    """解析一行 Windows 事件日志记录（key=value / wevtutil 文本 / XML 单行）。

    提取 EventID / Provider / 时间 / 账号 / 工作站 / 源 IP / 登录类型。
    """
    low = line.lower()
    evid = None
    m = re.search(r"(?:eventid=|event\s+id:\s*|<eventid>)\s*(\d+)", low)
    if m:
        evid = int(m.group(1))
    provider = None
    m = (re.search(r"providername=([^\s]+)", line, re.IGNORECASE)
         or re.search(r"<provider\s+name=\"([^\"]+)\"", line, re.IGNORECASE)
         or re.search(r"source:\s*([^\s]+)", line, re.IGNORECASE))
    if m:
        provider = m.group(1).strip('"')
    ts = None
    ts_raw = None
    m = WINEVT_ISO_RE.search(line)
    if m:
        ts_raw = m.group(1)
        ts = parse_iso_time(ts_raw)
    user = _winevt_field(line, ["targetusername", "target user name",
                                "subjectusername", "accountname", "account name"])
    workstation = _winevt_field(line, ["workstationname", "workstation name"])
    source = None
    cand = _winevt_field(line, ["ipaddress"])
    if cand and cand not in ("-", "::", "::1", "0.0.0.0"):
        source = cand
    if not source:
        m = re.search(r"source\s+network\s+address\s*:\s*([0-9a-fA-F:.]+)", line,
                      re.IGNORECASE)
        if m:
            candidate = m.group(1).strip('"')
            if candidate not in ("-", "::", "::1"):
                source = candidate
    logon_type = None
    lt_raw = _winevt_field(line, ["logontype", "logon type"])
    if lt_raw and lt_raw.isdigit():
        logon_type = int(lt_raw)
    outcome = None
    if evid == 4625:
        outcome = "failed"
    elif evid == 4624:
        outcome = "success"
    return {
        "kind": KIND_WINEVT,
        "ts": ts,
        "ts_raw": ts_raw,
        "line": line,
        "host": host,
        "event_id": evid,
        "provider": provider,
        "source": source,
        "user": user,
        "workstation": workstation,
        "logon_type": logon_type,
        "outcome": outcome,
        "message": line,
    }


def parse_line(line, host, forced_kind=None):
    """按类型解析一行日志。返回事件字典；无法解析时返回 None。

    forced_kind 为 None 时自动嗅探类型。
    """
    line = line.rstrip("\n").rstrip("\r")
    if not line.strip():
        return None
    kind = forced_kind or sniff_type(line)
    if kind == KIND_AUTH:
        return parse_auth_line(line, host)
    if kind == KIND_WEB:
        return parse_web_line(line, host)
    if kind == KIND_POWERSHELL:
        return parse_powershell_line(line, host)
    if kind == KIND_WINEVT:
        return parse_winevt_line(line, host)
    return None


# ---------------------------------------------------------------------------
# 检测
# ---------------------------------------------------------------------------

def _make_finding(category, ftype, severity, title, description,
                  evidence=None, time_value=None, source=None, count=None,
                  user=None, uri=None, ua=None, method=None, users=None,
                  event_id=None, provider=None, workstation=None, extra=None):
    """构造一条 finding 字典。"""
    f = {
        "id": "%s-%s" % (category.upper(), ftype.upper().replace("_", "-")),
        "category": category,
        "type": ftype,
        "severity": severity,
        "title": title,
        "description": description,
        "evidence": list(evidence or []),
    }
    if time_value is not None:
        f["time"] = time_value.isoformat()
    if source is not None:
        f["source"] = source
    if count is not None:
        f["count"] = count
    if user is not None:
        f["user"] = user
    if uri is not None:
        f["uri"] = uri
    if ua is not None:
        f["ua"] = ua
    if method is not None:
        f["method"] = method
    if users is not None:
        f["users"] = users
    if event_id is not None:
        f["event_id"] = event_id
    if provider is not None:
        f["provider"] = provider
    if workstation is not None:
        f["workstation"] = workstation
    if extra:
        f.update(extra)
    return f


def _count_within_window(events, window):
    """统计 events 中时间落在最后 window 秒内的事件数（无时间时全算）。"""
    ts_list = [e.get("ts") for e in events if e.get("ts")]
    if not ts_list or window <= 0:
        return len(events)
    latest = max(ts_list)
    cutoff = latest - timedelta(seconds=window)
    return sum(1 for e in events if e.get("ts") and e["ts"] >= cutoff)


def detect_auth(events, window=DEFAULT_WINDOW, max_fail=DEFAULT_MAX_FAIL):
    """检测 auth/secure 日志：爆破、撞库、异常登录、sudo 提权。"""
    findings = []
    failed_by_src = {}
    success_by_src = {}
    sudo_events = []

    for ev in events:
        if ev.get("kind") != KIND_AUTH:
            continue
        src = ev.get("source")
        out = ev.get("outcome")
        msg = (ev.get("message") or "").lower()
        if out == "failed":
            failed_by_src.setdefault(src, []).append(ev)
        elif out == "success":
            success_by_src.setdefault(src, []).append(ev)
        if "sudo:" in msg and any(k in msg for k in (
                "command=", "session opened for user", "not in sudoers")):
            sudo_events.append(ev)
        if "invalid user" in msg:
            findings.append(_make_finding(
                KIND_AUTH, "invalid_user", "medium",
                "尝试登录不存在的用户",
                "日志中出现 'invalid user'，说明攻击者在对一个真实系统上不存在的账户发起登录尝试，"
                "通常是撞库 / 用户名枚举的前兆。可结合同源失败登录聚合判断是否为自动化爆破。",
                evidence=[ev.get("line")], time_value=ev.get("ts"),
                source=src, user=ev.get("user")))

    # 同源失败登录聚合（爆破）
    for src, evs in failed_by_src.items():
        if not src:
            continue
        n = len(evs)
        in_window = _count_within_window(evs, window)
        count = max(n, in_window)
        if count >= max_fail:
            sev = "high" if count >= max_fail * 4 else ("medium" if count >= max_fail * 2 else "low")
            findings.append(_make_finding(
                KIND_AUTH, "brute_force", sev,
                "检测到密码爆破（同源多次失败登录）",
                "来源 %s 在时间窗 %d 秒内发生 %d 次失败登录（阈值 %d），符合暴力破解特征。建议："
                "核查来源是否合法，临时封禁该来源，并确认是否存在弱口令账户。" % (src, window, count, max_fail),
                evidence=[e.get("line") for e in evs[:5]], time_value=evs[-1].get("ts"),
                source=src, count=count))
        # 时间窗内多账号撞库
        users = {e.get("user") for e in evs if e.get("user")}
        if len(users) >= 2:
            findings.append(_make_finding(
                KIND_AUTH, "credential_stuffing", "high",
                "检测到撞库 / 多账号扫描（同源尝试多个用户名）",
                "来源 %s 在日志中尝试了 %d 个不同用户名（%s），符合撞库或用户名枚举特征。建议："
                "启用来源限速与失败锁定，并核查相关账户是否失陷。" % (
                    src, len(users), ", ".join(sorted(users))),
                evidence=[e.get("line") for e in evs[:5]], time_value=evs[-1].get("ts"),
                source=src, count=len(users), users=sorted(users)))

    # 异常登录：成功登录的来源此前有过失败；或 root 直接登录
    for src, evs in success_by_src.items():
        if not src:
            continue
        if src in failed_by_src:
            findings.append(_make_finding(
                KIND_AUTH, "abnormal_login", "high",
                "检测到异常登录（同类来源曾多次失败后成功）",
                "来源 %s 在多次失败登录后又成功登录，可能是攻击者爆破成功后接管账户。建议："
                "立即核查该来源与相关账户的会话、检查是否有未授权操作，并重置密码。" % src,
                evidence=[e.get("line") for e in evs[:3]], time_value=evs[-1].get("ts"),
                source=src))
        for e in evs:
            if e.get("user") == "root":
                findings.append(_make_finding(
                    KIND_AUTH, "root_login", "medium",
                    "检测到 root 直接登录",
                    "来源 %s 以 root 身份直接登录。root 直登风险较高，若来源非预期则应重点核查，"
                    "建议改用受限账户 + sudo 代替 root 直登。" % src,
                    evidence=[e.get("line")], time_value=e.get("ts"), source=src,
                    user="root"))

    # sudo 提权
    for e in sudo_events:
        msg = (e.get("message") or "")
        sev = "high" if "not in sudoers" in msg.lower() else "medium"
        ftype = "sudo_attempt" if "not in sudoers" in msg.lower() else "sudo_escalation"
        title = "检测到 sudo 提权尝试" if sev == "medium" else "检测到越权 sudo 尝试（不在 sudoers）"
        desc = ("日志中出现 sudo 提权 / 命令执行记录。建议：核对执行者是否授权、执行的命令是否正常，"
                "并确认 sudoers 配置最小化授权。") if sev == "medium" else (
                "日志中出现 'user NOT in sudoers'，说明有用户尝试越权执行 sudo，"
                "可能是横向移动或提权攻击的迹象。建议：核查该用户来源、检查 sudoers 配置。")
        findings.append(_make_finding(
            KIND_AUTH, ftype, sev, title, desc,
            evidence=[e.get("line")], time_value=e.get("ts"), source=e.get("source"),
            user=e.get("user")))

    return findings


def detect_web(events, window=DEFAULT_WINDOW, threshold_404=DEFAULT_404_THRESHOLD):
    """检测 Web 访问日志：404 洪峰 / 扫描 / webshell / 路径遍历 / SQLi / 可疑 UA。"""
    findings = []
    by_src = {}

    for ev in events:
        if ev.get("kind") != KIND_WEB:
            continue
        src = ev.get("source")
        by_src.setdefault(src, []).append(ev)
        uri = (ev.get("uri") or "").lower()
        decoded_uri = unquote(uri)
        ua = (ev.get("ua") or "").lower()
        method = (ev.get("method") or "")
        status = ev.get("status") or 0

        # 路径遍历
        if any(t in uri or t in decoded_uri for t in TRAVERSAL):
            findings.append(_make_finding(
                KIND_WEB, "path_traversal", "high", "检测到路径遍历",
                "请求路径包含目录穿越特征（../ 或编码变体），攻击者可能试图读取服务器任意文件。"
                "建议：核查是否成功穿越、修复路径校验与文件访问控制。",
                evidence=[ev.get("line")], time_value=ev.get("ts"), source=src,
                uri=ev.get("uri"), method=method))
        # SQL 注入
        if any(t in uri or t in decoded_uri for t in SQLI):
            findings.append(_make_finding(
                KIND_WEB, "sql_injection", "high", "检测到 SQL 注入特征",
                "请求 URI/参数包含 SQL 注入特征字符串，攻击者可能试图操纵数据库查询。"
                "建议：核查对应接口是否使用参数化查询，并检查数据库日志确认是否命中。",
                evidence=[ev.get("line")], time_value=ev.get("ts"), source=src,
                uri=ev.get("uri"), method=method))
        # webshell 上传 / 执行轨迹
        if (method.upper() == "POST" and any(p in uri for p in WEBSHELL_PATH)) or \
           (any(p in uri for p in WEBSHELL_PATH) and ("cmd=" in uri or "eval(" in uri)):
            findings.append(_make_finding(
                KIND_WEB, "webshell_upload", "critical", "检测到 webshell 上传/访问轨迹",
                "访问路径命中 webshell 特征（如 shell.php / cmd / eval 等），"
                "可能已上传或调用后门脚本。建议：立即排查文件系统、检查 web 目录写权限，"
                "并确认对应请求是否被 WAF 拦截。",
                evidence=[ev.get("line")], time_value=ev.get("ts"), source=src,
                uri=ev.get("uri"), method=method))
        # 可疑 UA（扫描器 / 自动化工具）
        if ua and any(s in ua for s in SCANNER_UA):
            findings.append(_make_finding(
                KIND_WEB, "suspicious_ua", "low", "检测到可疑 User-Agent",
                "请求的 User-Agent 命中已知扫描 / 自动化工具特征（%s）。" % ua,
                evidence=[ev.get("line")], time_value=ev.get("ts"), source=src,
                uri=ev.get("uri"), ua=ev.get("ua")))

    # 聚合：扫描特征（命中探测路径）、404 洪峰
    for src, evs in by_src.items():
        if not src:
            continue
        scans = [e for e in evs
                 if e.get("uri") and any(p in e["uri"].lower() for p in SCANNER_PATH)]
        if len(scans) >= 3:
            findings.append(_make_finding(
                KIND_WEB, "scanner_signature", "medium",
                "检测到扫描器探测行为（命中多个敏感/管理路径）",
                "来源 %s 在日志中请求了 %d 个常见管理/敏感路径（如 wp-login、phpmyadmin 等），"
                "符合自动化扫描 / 踩点特征。建议：核对来源并考虑在 WAF 层处置。" % (src, len(scans)),
                evidence=[e.get("line") for e in scans[:5]], time_value=evs[-1].get("ts"),
                source=src, count=len(scans)))
        codes = [e for e in evs if (e.get("status") or 0) == 404]
        if len(codes) >= threshold_404:
            findings.append(_make_finding(
                KIND_WEB, "flood_404", "medium",
                "检测到 404 洪峰",
                "来源 %s 在时间窗内产生 %d 个 404 响应（阈值 %d），可能是目录爆破或扫描行为。"
                "建议：核查来源、确认服务是否过载，并评估是否加防护。" % (src, len(codes), threshold_404),
                evidence=[e.get("line") for e in codes[:5]], time_value=evs[-1].get("ts"),
                source=src, count=len(codes)))

    return findings


def _base64_len(text):
    """估计行内长 base64 串长度；用于识别 PowerShell 编码命令。"""
    m = re.search(r"([A-Za-z0-9+/]{80,}={0,2})", text)
    return len(m.group(1)) if m else 0


def detect_powershell(events):
    """检测 PowerShell 脚本块日志：编码命令 / 下载执行 / 反射 / AMSI 绕过 / 混淆。"""
    findings = []
    for ev in events:
        if ev.get("kind") != KIND_POWERSHELL:
            continue
        msg = (ev.get("message") or "")
        low = msg.lower()
        evid = [ev.get("line")]

        if "encodedcommand" in low or "-enc" in low or _base64_len(msg) >= 160:
            findings.append(_make_finding(
                KIND_POWERSHELL, "encoded_command", "high",
                "检测到 PowerShell 编码命令",
                "PowerShell 脚本块中出现 -EncodedCommand / 长 base64 负载，编码命令常用于绕过静态检测"
                "执行隐蔽操作。建议：核查对应进程与命令、确认是否为恶意行为。",
                evidence=evid, time_value=ev.get("ts")))
        if any(k in low for k in ("invoke-webrequest", "downloadstring",
                                  "start-bitstransfer", "urlcache",
                                  "net.webclient")) and "http" in low:
            findings.append(_make_finding(
                KIND_POWERSHELL, "download_execute", "critical",
                "检测到下载执行（下载器 + 远程脚本）",
                "PowerShell 中出现从网络下载内容并转入执行（Invoke-WebRequest / DownloadString / "
                "certutil urlcache 等），是常见的下载器 / 木马投递手法。建议：核查下载目标与"
                "进程行为，结合上下文判断是否恶意。",
                evidence=evid, time_value=ev.get("ts")))
        if any(k in low for k in ("add-type", "[reflection.assembly]",
                                  "assembly::load", "getmethod", "activator")):
            findings.append(_make_finding(
                KIND_POWERSHELL, "reflection", "medium",
                "检测到反射加载（.NET / 内存加载）",
                "PowerShell 使用 Add-Type / Reflection.Assembly 等反射加载 .NET 程序集，"
                "常用于内存执行绕过落盘。建议：结合父进程与命令上下文判断。",
                evidence=evid, time_value=ev.get("ts")))
        if any(k in low for k in ("amsiutils", "amsiinitfailed", "0x417369",
                                  "system.management.automation.amsiutils",
                                  "amsibypass")):
            findings.append(_make_finding(
                KIND_POWERSHELL, "amsi_bypass", "critical",
                "检测到 AMSI 绕过",
                "PowerShell 中出现 AMSI 绕过相关字符串（AmsiUtils / amsiInitFailed 等），"
                "攻击者试图绕过 AMSI 检测以加载恶意内容。建议：重点核查该进程及后续行为。",
                evidence=evid, time_value=ev.get("ts")))
        if any(k in low for k in ("-enc", "iex", "frombase64string",
                                  "write-output", "-replace", "join",
                                  "powershell -no")) or \
           (("[char]" in low) or (" -f " in low and "=" in low)):
            findings.append(_make_finding(
                KIND_POWERSHELL, "obfuscation", "medium",
                "检测到 PowerShell 混淆手段",
                "PowerShell 脚本块包含混淆特征（iex / -enc / [char] / 字符串拼接 / 格式化等），"
                "可能用于规避检测。建议：尝试解码还原后人工核实。",
                evidence=evid, time_value=ev.get("ts")))

    return findings


# Windows 事件日志可疑进程特征：(匹配子串, 说明, 严重度)。按严重度从高到低匹配。
SUSPICIOUS_PROCESS = [
    ("mimikatz", "凭据窃取工具（Mimikatz）", "critical"),
    ("lsass", "LSASS 进程访问（凭据窃取）", "critical"),
    ("downloadstring", "下载内容并执行", "critical"),
    ("procdump", "内存转储（可能窃取凭据）", "high"),
    ("frombase64string", "Base64 解码执行", "high"),
    ("mshta", "MSHTA 脚本宿主（可加载远程内容）", "high"),
    ("certutil -urlcache", "CertUtil 下载执行", "high"),
    ("certutil -decode", "CertUtil 解码执行", "high"),
    ("regsvr32 /s", "Regsvr32 静默注册（可远程加载）", "high"),
    ("rundll32 javascript", "Rundll32 加载 JS（可疑）", "high"),
    ("bitsadmin /transfer", "BitsAdmin 下载执行", "high"),
    ("bitsadmin /download", "BitsAdmin 下载执行", "high"),
    ("wmic process call create", "WMIC 进程创建 / 远程执行", "high"),
    ("-windowstyle hidden", "PowerShell 隐藏窗口执行", "high"),
    ("-enc", "PowerShell 编码命令", "high"),
    ("iex", "Invoke-Expression 执行", "medium"),
    ("powershell", "PowerShell 执行", "medium"),
    ("pwsh", "PowerShell Core 执行", "medium"),
    ("cmd /c", "cmd 一次性命令执行", "medium"),
    ("cmd.exe", "cmd 命令行执行", "medium"),
    ("wscript", "WSH 脚本宿主", "medium"),
    ("cscript", "WSH 脚本宿主", "medium"),
    ("schtasks /create", "计划任务创建（持久化）", "medium"),
    ("sc create", "服务创建（持久化）", "medium"),
    ("sc config", "服务配置修改（持久化）", "medium"),
    ("net user", "账户管理命令", "medium"),
    ("net localgroup", "本地组管理命令", "medium"),
    ("net group", "域组管理命令", "medium"),
    ("whoami", "身份侦察命令", "low"),
    ("taskkill /f", "强制结束进程", "low"),
]


def _match_suspicious_process(text):
    """在进程映像 + 命令行中匹配可疑特征，返回 (说明, 严重度) 或 None。"""
    low = text.lower()
    for pat, desc, sev in SUSPICIOUS_PROCESS:
        if pat in low:
            return desc, sev
    return None


def detect_winevt(events, window=DEFAULT_WINDOW, max_fail=DEFAULT_MAX_FAIL):
    """检测 Windows 事件日志（Security/System）。

    覆盖：登录失败聚合（4625）/ 异常·管理员·RDP 登录（4624）/ 账户创建·删除（4720/4726）
    / 账户锁定（4740）/ 组成员添加（4732/4728）/ 安全日志清空（1102）/ 可疑进程创建（4688）
    / 新服务安装（7045）/ 计划任务创建（4698）。
    """
    findings = []
    failed_by_src = {}
    success_by_src = {}

    def _wfind(ftype, sev, title, desc, ev, **kw):
        return _make_finding(
            KIND_WINEVT, ftype, sev, title, desc,
            evidence=[ev.get("line")], time_value=ev.get("ts"),
            source=ev.get("source"), user=ev.get("user"),
            event_id=ev.get("event_id"), provider=ev.get("provider"),
            workstation=ev.get("workstation"), **kw)

    for ev in events:
        if ev.get("kind") != KIND_WINEVT:
            continue
        eid = ev.get("event_id")
        msg = ev.get("message") or ""
        low = msg.lower()

        if eid == 4625:
            failed_by_src.setdefault(ev.get("source"), []).append(ev)
            continue
        if eid == 4624:
            user = ev.get("user") or ""
            if ev.get("source"):
                success_by_src.setdefault(ev.get("source"), []).append(ev)
            if ev.get("logon_type") == 10:
                findings.append(_wfind(
                    "rdp_logon", "medium", "检测到远程桌面（RDP）登录",
                    "EventID 4624 记录 Logon Type 10（远程交互）登录。若登录来源或时间非预期，"
                    "可能是远程接管迹象。建议：核对来源 IP、账号与会话，确认是否为授权运维。",
                    ev))
            if user.lower() in ("administrator", "root"):
                findings.append(_wfind(
                    "admin_logon", "medium", "检测到管理员账号登录",
                    "EventID 4624 以 Administrator / root 等管理员账号成功登录。若来源非预期，"
                    "应重点核查该会话后续行为与账号口令安全。",
                    ev))
            continue
        if eid == 4720:
            findings.append(_wfind(
                "account_created", "high", "检测到用户账户创建",
                "Security 日志出现账户创建（EventID 4720），攻击者常创建后门账户维持访问。"
                "建议：核对创建者与用途，确认为授权操作；可疑则立即禁用并排查创建来源。",
                ev))
            continue
        if eid == 4726:
            findings.append(_wfind(
                "account_deleted", "high", "检测到用户账户删除",
                "Security 日志出现账户删除（EventID 4726），可能是清理痕迹或破坏性操作。"
                "建议：核对被删账户与删除者，确认业务合理性。",
                ev))
            continue
        if eid == 4740:
            findings.append(_wfind(
                "account_locked", "medium", "检测到用户账户被锁定",
                "EventID 4740 账户被锁定，通常由连续失败登录触发，可能是针对该账户的爆破。"
                "建议：结合 4625 失败登录记录定位来源，评估账户口令强度。",
                ev))
            continue
        if eid in (4732, 4728):
            group = _winevt_field(low, ["groupname", "group name"])
            sev = ("high" if group and "admin" in group.lower() else "medium")
            findings.append(_wfind(
                "group_member_add", sev, "检测到组成员添加",
                "EventID %d 记录将成员加入安全组（%s）。若加入的是管理员组，可能是权限维持 / "
                "提权迹象。建议：核对操作者与被加账号，确认为授权操作。" % (eid, group or "-"),
                ev))
            continue
        if eid == 1102:
            findings.append(_wfind(
                "audit_log_cleared", "critical", "检测到安全日志被清空",
                "EventID 1102 记录安全日志被清空，攻击者常在攻击后清空日志以抹除痕迹。"
                "建议：立即核查清空者与时间，检查日志转发 / 备份，评估事件响应。",
                ev))
            continue
        if eid == 4688:
            image = _winevt_field(low, ["newprocessname", "new process name"]) or ""
            cmdline = _winevt_field(low, ["commandline", "command line"]) or ""
            hit = _match_suspicious_process(image + " " + cmdline)
            if hit:
                desc, sev = hit
                findings.append(_wfind(
                    "suspicious_process", sev, "检测到可疑进程创建",
                    "EventID 4688 进程创建：%s，命中可疑特征（%s）。攻击者常通过此类进程执行"
                    "下载、编码命令、凭据窃取或持久化。建议：结合父进程与后续行为核实。" % (
                        image or "-", desc),
                    ev))
            continue
        if eid == 7045:
            svc = _winevt_field(low, ["servicename", "service name"])
            findings.append(_wfind(
                "service_installed", "medium", "检测到新服务安装",
                "System 日志 EventID 7045 记录新服务安装（%s），服务可被用于持久化。"
                "建议：核对服务名 / 可执行路径与安装者，确认为授权操作。" % (svc or "-"),
                ev))
            continue
        if eid == 4698:
            task = _winevt_field(low, ["taskname", "task name"])
            findings.append(_wfind(
                "task_created", "medium", "检测到计划任务创建",
                "Security 日志 EventID 4698 记录计划任务创建（%s），计划任务是常见持久化手段。"
                "建议：核对任务动作 / 触发条件与创建者，确认为授权操作。" % (task or "-"),
                ev))
            continue

    # 4625 聚合：同源失败登录（爆破）+ 多账号撞库
    for src, evs in failed_by_src.items():
        n = len(evs)
        in_window = _count_within_window(evs, window)
        count = max(n, in_window)
        if count >= max_fail:
            sev = "high" if count >= max_fail * 4 else ("medium" if count >= max_fail * 2 else "low")
            findings.append(_make_finding(
                KIND_WINEVT, "brute_force", sev,
                "检测到密码爆破（同源多次登录失败）",
                "来源 %s 在时间窗 %d 秒内发生 %d 次登录失败（EventID 4625，阈值 %d），符合暴力破解"
                "特征。建议：核查来源是否合法，临时封禁并确认相关账户口令强度。" % (
                    src, window, count, max_fail),
                evidence=[e.get("line") for e in evs[:5]], time_value=evs[-1].get("ts"),
                source=src, count=count))
        users = {e.get("user") for e in evs if e.get("user")}
        if len(users) >= 2:
            findings.append(_make_finding(
                KIND_WINEVT, "credential_stuffing", "high",
                "检测到撞库 / 多账号扫描（同源尝试多个用户名）",
                "来源 %s 在日志中尝试了 %d 个不同用户名（%s），符合撞库 / 用户名枚举特征。"
                "建议：启用来源限速与失败锁定，核查相关账户。" % (
                    src, len(users), ", ".join(sorted(users))),
                evidence=[e.get("line") for e in evs[:5]], time_value=evs[-1].get("ts"),
                source=src, count=len(users), users=sorted(users)))

    # 异常登录：同来源先失败（4625）后成功（4624）
    for src, evs in success_by_src.items():
        if src in failed_by_src:
            findings.append(_make_finding(
                KIND_WINEVT, "abnormal_login", "high",
                "检测到异常登录（同来源曾失败后成功）",
                "来源 %s 先出现登录失败（4625）又成功登录（4624），可能是爆破成功后接管账户。"
                "建议：立即核查该来源与相关账户的会话与后续行为，重置可疑账户口令。" % src,
                evidence=[e.get("line") for e in evs[:3]], time_value=evs[-1].get("ts"),
                source=src))

    return findings


# ---------------------------------------------------------------------------
# 管线
# ---------------------------------------------------------------------------

def parse_events(lines, host, forced_kind=None):
    """逐行解析，产出事件字典（生成器）。"""
    for line in lines:
        ev = parse_line(line, host, forced_kind)
        if ev:
            yield ev


def run_detections(events, opts):
    """对事件执行三类检测，合并去重。opts 支持 window / max_fail / threshold_404。"""
    findings = []
    findings += detect_auth(events, opts.get("window", DEFAULT_WINDOW),
                            opts.get("max_fail", DEFAULT_MAX_FAIL))
    findings += detect_web(events, opts.get("window", DEFAULT_WINDOW),
                           opts.get("threshold_404", DEFAULT_404_THRESHOLD))
    findings += detect_powershell(events)
    findings += detect_winevt(events, opts.get("window", DEFAULT_WINDOW),
                              opts.get("max_fail", DEFAULT_MAX_FAIL))
    return dedupe_findings(findings)


def dedupe_findings(findings):
    """按 (id, source, uri, user, title) 去重，保留首次出现。"""
    out = []
    seen = set()
    for f in findings:
        key = (f.get("id"), f.get("source"), f.get("uri"),
               f.get("user"), f.get("title"))
        if key in seen:
            continue
        seen.add(key)
        out.append(f)
    return out


def build_timeline(findings):
    """按时间排序命中；无时间的排最后。"""
    return sorted(findings, key=lambda f: (f.get("time") is None,
                                           f.get("time") or ""))


# ---------------------------------------------------------------------------
# 输出
# ---------------------------------------------------------------------------

def _sev_counts(findings):
    counts = {s: 0 for s in SEVERITY_ORDER}
    for f in findings:
        sev = f.get("severity")
        if sev in counts:
            counts[sev] += 1
    return counts


def _format_time(f):
    return f.get("time") or "-"


def format_text(findings, stats, meta):
    """人类可读文本报告（中文）。"""
    lines = []
    lines.append("=" * 58)
    lines.append("  %s (%s) 安全日志分析报告" % (TOOL_CN, TOOL))
    lines.append("=" * 58)
    lines.append("生成时间 : %s" % meta.get("generated_at", "-"))
    lines.append("输入文件 : %s" % (", ".join(stats.get("inputs", [])) or "-"))
    lines.append("扫描事件 : %d" % stats.get("events", 0))
    lines.append("命中数量 : %d" % len(findings))
    lines.append("")
    if not findings:
        lines.append("未发现命中。")
        lines.append("")
        return "\n".join(lines) + "\n"

    lines.append("## 命中详情")
    lines.append("")
    for f in findings:
        sev = f.get("severity", "info").upper()
        lines.append("[%s] %s" % (sev, f.get("title", "")))
        lines.append("  类型   : %s / %s" % (f.get("category", ""), f.get("type", "")))
        lines.append("  时间   : %s" % _format_time(f))
        if f.get("source"):
            lines.append("  来源   : %s" % f["source"])
        if f.get("event_id") is not None:
            lines.append("  EventID: %s" % f["event_id"])
        if f.get("provider"):
            lines.append("  提供方 : %s" % f["provider"])
        if f.get("workstation"):
            lines.append("  工作站 : %s" % f["workstation"])
        if f.get("uri"):
            lines.append("  URI    : %s" % f["uri"])
        if f.get("user"):
            lines.append("  用户   : %s" % f["user"])
        if f.get("count") is not None:
            lines.append("  计数   : %s" % f["count"])
        for ev in f.get("evidence", []):
            lines.append("    - %s" % ev)
        lines.append("  说明   : %s" % f.get("description", ""))
        lines.append("")

    lines.append("## 汇总")
    cnt = _sev_counts(findings)
    lines.append("  " + "  ".join("%s=%d" % (s, cnt[s]) for s in SEVERITY_ORDER))
    lines.append("")
    return "\n".join(lines) + "\n"


def format_md(findings, stats, meta):
    """Markdown 报告。"""
    fence = chr(96) * 3
    out = []
    out.append("# 元察（yotta-logwatch）安全日志分析报告")
    out.append("")
    out.append("- 生成时间：%s" % meta.get("generated_at", "-"))
    out.append("- 输入文件：%s" % (", ".join(stats.get("inputs", [])) or "-"))
    out.append("- 扫描事件：%d" % stats.get("events", 0))
    out.append("- 命中数量：%d" % len(findings))
    out.append("")
    if not findings:
        out.append("未发现命中。")
        out.append("")
        return "\n".join(out) + "\n"
    out.append("## 命中详情")
    out.append("")
    for f in findings:
        sev = f.get("severity", "info").upper()
        out.append("### [%s] %s" % (sev, f.get("title", "")))
        out.append("")
        out.append("- 类型：%s / %s" % (f.get("category", ""), f.get("type", "")))
        out.append("- 时间：%s" % _format_time(f))
        if f.get("source"):
            out.append("- 来源：%s" % f["source"])
        if f.get("event_id") is not None:
            out.append("- EventID：%s" % f["event_id"])
        if f.get("provider"):
            out.append("- 提供方：%s" % f["provider"])
        if f.get("workstation"):
            out.append("- 工作站：%s" % f["workstation"])
        if f.get("uri"):
            out.append("- URI：%s" % f["uri"])
        if f.get("user"):
            out.append("- 用户：%s" % f["user"])
        if f.get("count") is not None:
            out.append("- 计数：%s" % f["count"])
        if f.get("evidence"):
            out.append("- 证据：")
            for ev in f.get("evidence", []):
                out.append("  " + fence)
                out.append("  %s" % ev)
                out.append("  " + fence)
        out.append("- 说明：%s" % f.get("description", ""))
        out.append("")
    out.append("## 汇总")
    cnt = _sev_counts(findings)
    out.append("")
    out.append("| %s |" % " | ".join(SEVERITY_ORDER))
    out.append("|---%s|" % "---|" * len(SEVERITY_ORDER))
    out.append("| %s |" % " | ".join(str(cnt[s]) for s in SEVERITY_ORDER))
    out.append("")
    return "\n".join(out) + "\n"


def build_json(findings, stats, meta):
    """构造 JSON 报告对象。"""
    return {
        "tool": TOOL,
        "tool_cn": TOOL_CN,
        "version": VERSION,
        "generated_at": meta.get("generated_at"),
        "inputs": stats.get("inputs", []),
        "stats": {"events": stats.get("events", 0), "findings": len(findings)},
        "findings": findings,
    }


def write_report(text, output):
    """写出报告文件（UTF-8，LF）。"""
    with open(output, "w", encoding="utf-8", newline="") as f:
        f.write(text)


# ---------------------------------------------------------------------------
# 读取
# ---------------------------------------------------------------------------

def read_text(path):
    """读取文本文件为行列表（容错解码）。"""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.readlines()


def _looks_like_log(path):
    """判断文件是否像日志（扩展名或文件名特征）。"""
    name = os.path.basename(path).lower()
    if name.startswith("."):
        return False
    ext = os.path.splitext(path)[1].lower()
    if ext in (".log", ".txt", ".out", ".access", ".err", ".audit"):
        return True
    if any(k in name for k in ("auth", "access", "secure", "powershell",
                               "syslog", "error", "system", "event")):
        return True
    return False


def iter_log_files(path, recursive=False):
    """产出要分析的日志文件路径。

    显式传文件 -> 直接分析；传目录 -> 按日志特征筛选。
    """
    if os.path.isfile(path):
        yield path
        return
    if os.path.isdir(path):
        skip_dirs = {".git", ".svn", "__pycache__", "node_modules", ".tmp"}
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for f in files:
                p = os.path.join(root, f)
                if _looks_like_log(p):
                    yield p
        return
    raise ValueError("路径不存在或不可读：%s" % path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_scan(args):
    """scan 子命令实现。返回退出码。"""
    fmt = "json" if args.json else ("markdown" if args.report else args.format)
    opts = {
        "window": args.window,
        "max_fail": args.max_fail,
        "threshold_404": args.threshold_404,
    }
    events = []
    inputs = []
    try:
        if args.stdin:
            lines = sys.stdin.read().splitlines()
            events = list(parse_events(lines, "<stdin>", args.type))
            inputs.append("<stdin>")
        else:
            paths = []
            for p in (args.path or []):
                for f in iter_log_files(p, args.recursive):
                    paths.append(f)
            if not paths:
                raise ValueError("未找到可分析的日志文件")
            for f in paths:
                events.extend(parse_events(read_text(f), f, args.type))
                inputs.append(f)
    except (ValueError, OSError) as e:
        sys.stderr.write("错误：%s\n" % e)
        return 4

    findings = run_detections(events, opts)
    min_rank = SEVERITY_RANK.get(args.min_severity, 0)
    findings = [f for f in findings
                if SEVERITY_RANK.get(f.get("severity", "info"), 0) >= min_rank]
    findings = build_timeline(findings)
    stats = {"events": len(events), "inputs": inputs, "findings": len(findings)}
    meta = {"generated_at": datetime.now(timezone.utc).isoformat()}

    if fmt == "json":
        payload = build_json(findings, stats, meta)
        text = json.dumps(payload, ensure_ascii=False, indent=2)
    elif fmt == "markdown":
        text = format_md(findings, stats, meta)
    else:
        text = format_text(findings, stats, meta)

    if args.output:
        try:
            write_report(text, args.output)
        except OSError as e:
            sys.stderr.write("写入输出失败：%s\n" % e)
            return 4
    else:
        print(text)
    return 1 if findings else 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog=TOOL,
        description="%s（%s）：零依赖安全日志分析检测引擎（只读本地）。" % (TOOL_CN, TOOL),
    )
    parser.add_argument("--version", action="version",
                        version="%s (%s) %s" % (TOOL, TOOL_CN, VERSION))
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("scan", help="扫描本地日志文件并检测可疑活动")
    p.add_argument("--path", action="append", metavar="PATH",
                   help="日志文件或目录，可多次；目录默认只取日志特征文件")
    p.add_argument("--recursive", action="store_true", help="递归扫描目录")
    p.add_argument("--stdin", action="store_true", help="从标准输入读取日志")
    p.add_argument("--type", choices=[KIND_AUTH, KIND_WEB, KIND_POWERSHELL, KIND_WINEVT],
                   help="强制指定日志类型（默认自动嗅探）")
    p.add_argument("--format", choices=["text", "json", "markdown"],
                   default="text", help="输出格式")
    p.add_argument("--json", action="store_true", help="等价于 --format json")
    p.add_argument("--report", action="store_true", help="等价于 --format markdown")
    p.add_argument("--output", metavar="FILE", help="写入报告文件（默认打印）")
    p.add_argument("--min-severity", choices=SEVERITY_ORDER, default="info",
                   help="只显示不低于该严重度的命中")
    p.add_argument("--max-fail", type=int, default=DEFAULT_MAX_FAIL,
                   help="同源失败登录阈值（默认 %d）" % DEFAULT_MAX_FAIL)
    p.add_argument("--window", type=int, default=DEFAULT_WINDOW,
                   help="聚合时间窗（秒，默认 %d）" % DEFAULT_WINDOW)
    p.add_argument("--404-threshold", dest="threshold_404", type=int, default=DEFAULT_404_THRESHOLD,
                   help="同源 404 洪峰阈值（默认 %d）" % DEFAULT_404_THRESHOLD)

    args = parser.parse_args(argv)
    if args.command == "scan":
        return cmd_scan(args)
    parser.print_help()
    return 4


if __name__ == "__main__":
    sys.exit(main())
