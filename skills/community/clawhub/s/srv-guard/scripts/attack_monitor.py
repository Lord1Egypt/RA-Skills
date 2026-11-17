#!/usr/bin/env python3
"""attack_monitor.py — 攻击感知（只读日志分析）

用法:
    python attack_monitor.py --target <local|ssh://user@host[:port]> --window 24h [--rules brute-force,scan,anomaly] [--output monitor-result.json]

只读取日志，不修改系统。
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common
from _common import run_cmd, emit_json, log, parse_target

AUTH_LOGS = ["/var/log/auth.log", "/var/log/secure"]
WEB_LOGS = ["/var/log/nginx/access.log", "/var/log/apache2/access.log"]
WEB_SCAN_PATTERNS = [r'\.env\b', r'\.git/', r'wp-admin', r'phpmyadmin', r'%3Cscript', r'/etc/passwd',
                     r'sqlmap', r'nikto', r'nmap', r'masscan', r'dirbuster', r'gobuster']

_SYSLOG_TS = re.compile(r'^([A-Z][a-z]{2})\s+(\d{1,2})\s+(\d{2}):(\d{2}):(\d{2})')
_ISO_TS = re.compile(r'^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})')
_MONTHS = {m: i + 1 for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}


def parse_window(window):
    """解析 '24h'/'10m'/'7d' 为 timedelta。"""
    m = re.match(r'^(\d+)([smhd])$', window)
    if not m:
        raise ValueError(f"无法解析 window: {window}（格式如 24h, 10m, 7d）")
    n, unit = int(m.group(1)), m.group(2)
    return timedelta(seconds={"s": 1, "m": 60, "h": 3600, "d": 86400}[unit] * n)


def fmt_window(td):
    """timedelta → 可读字符串。"""
    s = int(td.total_seconds())
    if s % 86400 == 0:
        return f"{s // 86400}d"
    if s % 3600 == 0:
        return f"{s // 3600}h"
    if s % 60 == 0:
        return f"{s // 60}m"
    return f"{s}s"


def _parse_ts(line, year_hint):
    """尽力解析行首时间戳，返回 datetime 或 None。"""
    m = _ISO_TS.match(line)
    if m:
        return datetime(int(m[1]), int(m[2]), int(m[3]),
                        int(m[4]), int(m[5]), int(m[6]), tzinfo=timezone.utc)
    m = _SYSLOG_TS.match(line)
    if m:
        mon = _MONTHS.get(m[1])
        if mon:
            return datetime(year_hint, mon, int(m[2]),
                            int(m[3]), int(m[4]), int(m[5]), tzinfo=timezone.utc)
    return None


def read_log(target, path, since):
    """读取日志中 since 之后的行。返回 list[str]。

    策略：tail -5000 取尾部，Python 侧按时间戳过滤。
    无法解析时间戳的行保留（保守策略，宁多不漏）。
    """
    r = run_cmd(target, f"tail -5000 {path} 2>/dev/null", timeout=30)
    if r["rc"] != 0 or not r["stdout"]:
        return []
    lines = r["stdout"].splitlines()
    year_hint = since.year
    result = []
    for ln in lines:
        ts = _parse_ts(ln, year_hint)
        if ts is None or ts >= since:
            result.append(ln)
    return result


def detect_brute_force(target, since, window):
    """检测 SSH 暴力破解。"""
    events = []
    logs_used = []
    for lp in AUTH_LOGS:
        lines = read_log(target, lp, since)
        if not lines:
            continue
        logs_used.append(lp)
        fails = {}
        for ln in lines:
            m = re.search(r'Failed password for (?:invalid user )?(\S+) from (\S+) port', ln)
            if m:
                user, ip = m.group(1), m.group(2)
                fails.setdefault(ip, {"count": 0, "users": set(), "lines": []})
                fails[ip]["count"] += 1
                fails[ip]["users"].add(user)
                if len(fails[ip]["lines"]) < 5:
                    fails[ip]["lines"].append(f"{lp}:{ln.strip()[:200]}")
        for ip, info in fails.items():
            if info["count"] >= 5:
                events.append({
                    "type": "brute_force", "source_ip": ip,
                    "target_users": sorted(info["users"])[:5],
                    "failed_count": info["count"], "window": fmt_window(window),
                    "evidence": info["lines"], "severity": "HIGH",
                })
    return events, logs_used


def detect_scan(target, since, window):
    """检测端口/Web 扫描。"""
    events = []
    logs_used = []
    for lp in WEB_LOGS:
        lines = read_log(target, lp, since)
        if not lines:
            continue
        logs_used.append(lp)
        hits = {}
        for ln in lines:
            m = re.match(r'^(\S+) \S+ \S+ \[.*?\] "(\S+) (\S+)', ln)
            if not m:
                continue
            ip, path = m.group(1), m.group(2)
            for pat in WEB_SCAN_PATTERNS:
                if re.search(pat, ln, re.I):
                    hits.setdefault(ip, {"count": 0, "patterns": set(), "lines": []})
                    hits[ip]["count"] += 1
                    hits[ip]["patterns"].add(pat)
                    if len(hits[ip]["lines"]) < 5:
                        hits[ip]["lines"].append(f"{lp}:{ln.strip()[:200]}")
                    break
        for ip, info in hits.items():
            sev = "HIGH" if any(p in str(info["patterns"]) for p in ["sqlmap", "nikto", "/etc/passwd", "%3Cscript"]) else "MEDIUM"
            events.append({
                "type": "web_scan", "source_ip": ip, "hit_count": info["count"],
                "patterns_matched": sorted(info["patterns"])[:5], "evidence": info["lines"],
                "severity": sev,
            })
    return events, logs_used


def detect_anomaly(target, since, window):
    """检测异常登录。"""
    events = []
    logs_used = []
    for lp in AUTH_LOGS:
        lines = read_log(target, lp, since)
        if not lines:
            continue
        logs_used.append(lp)
        for ln in lines:
            m = re.search(r'Accepted (?:password|publickey) for (\S+) from (\S+) port', ln)
            if m:
                user, ip = m.group(1), m.group(2)
                if user == "root":
                    events.append({
                        "type": "root_login", "source_ip": ip, "target_user": "root",
                        "evidence": [f"{lp}:{ln.strip()[:200]}"], "severity": "HIGH",
                    })
    return events, logs_used


def detect_login(target, since, window):
    """汇总成功登录事件（INFO）。"""
    events = []
    logs_used = []
    for lp in AUTH_LOGS:
        lines = read_log(target, lp, since)
        if not lines:
            continue
        logs_used.append(lp)
        for ln in lines:
            m = re.search(r'Accepted (?:password|publickey) for (\S+) from (\S+) port', ln)
            if m:
                events.append({
                    "type": "login_success", "source_ip": m.group(2),
                    "target_user": m.group(1), "evidence": [f"{lp}:{ln.strip()[:200]}"],
                    "severity": "INFO",
                })
    return events, logs_used


RULES = {
    "brute-force": detect_brute_force,
    "scan": detect_scan,
    "anomaly": detect_anomaly,
    "login": detect_login,
}


def main():
    parser = argparse.ArgumentParser(description="攻击感知（只读日志分析）")
    parser.add_argument("--target", required=True, help="local 或 ssh://user@host[:port]")
    parser.add_argument("--window", default="24h", help="时间窗口（如 24h, 10m, 7d）")
    parser.add_argument("--rules", default="brute-force,scan,anomaly",
                        help="检测规则（逗号分隔）")
    parser.add_argument("--output", help="输出 JSON 文件路径")
    args = parser.parse_args()

    try:
        parse_target(args.target)
        td = parse_window(args.window)
    except ValueError as e:
        log(str(e), "ERROR")
        sys.exit(2)

    now = datetime.now(timezone.utc)
    since = now - td
    rules = [r.strip() for r in args.rules.split(",") if r.strip() in RULES]

    all_events = []
    logs_used = []
    logs_unavail = []
    for rule in rules:
        try:
            evs, used = RULES[rule](args.target, since, td)
            all_events.extend(evs)
            for u in used:
                if u not in logs_used:
                    logs_used.append(u)
        except Exception as e:
            log(f"规则 {rule} 异常: {e}", "WARN")

    for lp in AUTH_LOGS + WEB_LOGS:
        if lp not in logs_used:
            logs_unavail.append(lp)

    sev = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
    for e in all_events:
        sev[e["severity"]] = sev.get(e["severity"], 0) + 1

    out = {
        "target": args.target, "window": args.window,
        "from": since.isoformat(), "to": now.isoformat(),
        "rules_run": rules, "logs_analyzed": logs_used,
        "logs_unavailable": logs_unavail, "events": all_events,
        "summary": {"total": len(all_events), **sev},
    }
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        log(f"结果已写入 {args.output}")
    emit_json(out)
    log(f"感知完成: {len(all_events)} 事件")


if __name__ == "__main__":
    main()
