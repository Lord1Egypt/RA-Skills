#!/usr/bin/env python3
"""vuln_scan.py — 服务器漏洞扫描（只读）

用法:
    python vuln_scan.py --target <local|ssh://user@host[:port]> [--scope all|config|service|port|patch|ssh] [--output scan-result.json]

输出: JSON（漏洞清单 + 严重度 + 证据）到 stdout 或 --output 文件。
所有检测均为只读，不修改目标系统。
"""

import argparse
import json
import os
import re
import shlex
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common
from _common import run_cmd, read_file, emit_json, log, parse_target


def finding(fid, title, severity, scope, evidence, auto_fixable=True, remediation="", **extra):
    f = {
        "id": fid, "title": title, "severity": severity, "scope": scope,
        "evidence": evidence, "auto_fixable": auto_fixable,
        "remediation_ref": f"fix-playbook.md#{fid.lower()}", "remediation": remediation,
    }
    f.update(extra)
    return f


# ---------- config scope ----------
def scan_ssh_config(target):
    out = []
    cfg = read_file(target, "/etc/ssh/sshd_config")
    if cfg is None:
        log("无法读取 /etc/ssh/sshd_config，跳过 SSH 配置检查", "WARN")
        return out
    lines = cfg.splitlines()
    def get_directive(name):
        for i, ln in enumerate(lines, 1):
            s = ln.strip()
            if s.startswith(name) and not s.startswith("#"):
                return s, i
        return None, None

    val, ln = get_directive("PermitRootLogin")
    if val and re.search(r'PermitRootLogin\s+yes', val, re.I):
        out.append(finding("CFG-01", "SSH PermitRootLogin 已启用", "HIGH", "config",
                           f"/etc/ssh/sshd_config 第 {ln} 行: {val}"))
    val, ln = get_directive("PasswordAuthentication")
    if val and re.search(r'PasswordAuthentication\s+yes', val, re.I):
        out.append(finding("CFG-02", "SSH 允许密码登录", "MEDIUM", "config",
                           f"/etc/ssh/sshd_config 第 {ln} 行: {val}"))
    val, ln = get_directive("PermitEmptyPasswords")
    if val and re.search(r'PermitEmptyPasswords\s+yes', val, re.I):
        out.append(finding("CFG-03", "SSH 允许空口令", "CRITICAL", "config",
                           f"/etc/ssh/sshd_config 第 {ln} 行: {val}"))
    val, ln = get_directive("Protocol")
    if val and re.search(r'Protocol\s+1\b', val):
        out.append(finding("CFG-04", "SSH 使用不安全的协议版本 1", "CRITICAL", "config",
                           f"/etc/ssh/sshd_config 第 {ln} 行: {val}"))
    val, ln = get_directive("MaxAuthTries")
    if val:
        m = re.search(r'MaxAuthTries\s+(\d+)', val)
        if m and int(m.group(1)) > 6:
            out.append(finding("CFG-05", "SSH MaxAuthTries 过高", "LOW", "config",
                               f"/etc/ssh/sshd_config 第 {ln} 行: {val}"))
    return out


def scan_file_perms(target):
    out = []
    r = run_cmd(target, "find / -xdev \\( -name 'id_rsa' -o -name '*.pem' -o -name 'id_dsa' \\) 2>/dev/null | head -50", timeout=20)
    if r["rc"] == 0:
        for kf in r["stdout"].split():
            kf = kf.strip()
            if not kf:
                continue
            pr = run_cmd(target, f"stat -c '%a %n' {shlex.quote(kf)}", timeout=5)
            if pr["rc"] == 0:
                parts = pr["stdout"].split()
                if parts and int(parts[0], 8) > 0o600:
                    # 只有用户主目录下的密钥才自动收紧；系统路径（/usr、/etc 等）
                    # 改权限可能影响服务，必须人工确认
                    user_scope = kf.startswith("/home/") or kf.startswith("/root/")
                    out.append(finding(
                        "CFG-06", f"私钥/证书文件权限过宽: {kf}", "HIGH", "config",
                        f"stat: {pr['stdout'].strip()}",
                        auto_fixable=user_scope,
                        remediation="" if user_scope else "系统路径文件，收紧权限前需确认是否有服务依赖",
                        keyfile=kf, user_scoped=user_scope))
    sh = run_cmd(target, "stat -c '%a %n' /etc/shadow", timeout=5)
    if sh["rc"] == 0:
        parts = sh["stdout"].split()
        if parts and parts[0] not in ("640", "000", "600"):
            out.append(finding("CFG-09", "/etc/shadow 权限异常", "HIGH", "config",
                               f"stat: {sh['stdout'].strip()}"))
    return out


def scan_passwd_empty(target):
    out = []
    r = run_cmd(target, "awk -F: '$2==\"\" {print $1}' /etc/passwd", timeout=5)
    if r["rc"] == 0:
        for user in r["stdout"].split():
            if user and user not in ("nobody",):
                out.append(finding("CFG-07", f"账户 {user} 无密码", "CRITICAL", "config",
                                   f"/etc/passwd: {user} 第二字段为空", user=user))
    return out


def scan_sudo_nopasswd(target):
    out = []
    r = run_cmd(target, "grep -r 'NOPASSWD' /etc/sudoers /etc/sudoers.d/ 2>/dev/null", timeout=5)
    if r["rc"] == 0 and r["stdout"].strip():
        high_risk_cmds = ("ALL", "sudo", "su", "bash", "sh", "/bin/", "vi", "vim", "nano")
        for ln in r["stdout"].strip().splitlines()[:5]:
            # 提取 NOPASSWD 后的命令列表
            m = re.search(r'NOPASSWD:\s*(.*)', ln)
            cmd_list = m.group(1).strip() if m else ""
            if any(c in cmd_list for c in high_risk_cmds):
                out.append(finding("CFG-08", "sudo NOPASSWD 高危命令", "HIGH", "config", ln.strip()))
            else:
                out.append(finding("CFG-08", "sudo NOPASSWD 配置（受限命令）", "LOW", "config",
                                   ln.strip(), auto_fixable=False, remediation="需人工确认是否合理"))
    return out


# ---------- service scope ----------
DANGEROUS_SERVICES = {"telnet", "rsh", "rlogin", "tftp"}
HIGH_RISK_SERVICES = {"ftp", "vsftpd", "proftpd"}
EXPOSED_DB_PORTS = {"3306": "MySQL", "5432": "PostgreSQL", "27017": "MongoDB"}


def scan_services(target):
    out = []
    r = run_cmd(target, "systemctl list-unit-files --type=service --state=enabled 2>/dev/null || chkconfig --list 2>/dev/null", timeout=15)
    enabled = r["stdout"] if r["rc"] == 0 else ""
    for svc in DANGEROUS_SERVICES:
        if re.search(rf'\b{svc}\b', enabled, re.I):
            out.append(finding("SVC-01", f"危险服务已启用: {svc}", "CRITICAL", "service",
                               f"systemctl: {svc} enabled", auto_fixable=True))
    for svc in HIGH_RISK_SERVICES:
        if re.search(rf'\b{svc}\b', enabled, re.I):
            out.append(finding("SVC-01", f"高风险服务已启用: {svc}", "HIGH", "service",
                               f"systemctl: {svc} enabled", auto_fixable=False,
                               remediation="需人工确认是否业务必需"))
    return out


def _parse_listening(output, tool):
    """从 ss 或 netstat 输出解析 (addr, port, line) 列表。

    ss -tlnp:   LISTEN  0  128  0.0.0.0:22  0.0.0.0:*   (地址在 LISTEN+两数字后)
    netstat:    0.0.0.0:22  0.0.0.0:*  LISTEN          (LISTEN 在行尾)
    """
    results = []
    for ln in output.splitlines():
        if tool == "ss":
            m = re.search(r'LISTEN\s+\d+\s+\d+\s+(\S+):(\d+)\s', ln)
        else:
            m = re.search(r'(\S+):(\d+)\s+\S+\s+LISTEN', ln)
        if m:
            results.append((m.group(1), m.group(2), ln))
    return results


def _is_public_addr(addr):
    return addr in ("0.0.0.0", "::", ":::", "*", "[::]", "[::]:", "[*]")


def scan_listening_ports(target):
    out = []
    r = run_cmd(target, "ss -tlnp 2>/dev/null", timeout=10)
    if r["rc"] == 0 and r["stdout"].strip():
        listeners = _parse_listening(r["stdout"], "ss")
    else:
        r = run_cmd(target, "netstat -tlnp 2>/dev/null", timeout=10)
        if r["rc"] != 0 or not r["stdout"].strip():
            log("无法获取监听端口列表（ss 和 netstat 均不可用）", "WARN")
            return out
        listeners = _parse_listening(r["stdout"], "netstat")
    for addr, port, ln in listeners:
        is_public = _is_public_addr(addr)
        if port in ("23", "21", "3389") and is_public:
            out.append(finding("SVC-02", f"高危端口对外开放: {port}", "HIGH", "service",
                               f"监听: {ln.strip()}"))
        if port == "2375" and is_public:
            out.append(finding("SVC-04", "Docker daemon 无 TLS 对外开放", "CRITICAL", "service",
                               f"监听: {ln.strip()}"))
        if port in EXPOSED_DB_PORTS and is_public:
            out.append(finding("SVC-05", f"{EXPOSED_DB_PORTS[port]} 对外暴露 ({port})", "HIGH", "service",
                               f"监听: {ln.strip()}", auto_fixable=False))
        if port == "6379" and is_public:
            rcfg = read_file(target, "/etc/redis/redis.conf") or read_file(target, "/etc/redis.conf")
            if rcfg and not re.search(r'^\s*requirepass\s+\S+', rcfg, re.M):
                out.append(finding("SVC-06", "Redis 无认证对外暴露", "CRITICAL", "service",
                                   "6379 对外监听且无 requirepass", auto_fixable=False))
        if is_public and port not in ("22", "80", "443"):
            out.append(finding("PRT-01", f"非本地监听端口: {port}", "INFO", "port",
                               f"监听: {ln.strip()}", auto_fixable=False))
    return out


# ---------- patch scope ----------
def scan_security_updates(target, refresh=False):
    out = []
    distro = _common.detect_distro(target)
    if distro == "debian":
        # 默认不刷新包索引（保持只读）；--refresh 时才 apt-get update
        upd = "apt-get update -qq 2>/dev/null; " if refresh else ""
        r = run_cmd(target, f"{upd}apt list --upgradable 2>/dev/null | grep -i security | wc -l", timeout=60)
        if r["rc"] == 0:
            n = int(r["stdout"].strip() or 0)
            if n > 0:
                out.append(finding("PCH-01", f"{n} 个安全更新可用", "HIGH", "patch",
                                   f"apt: {n} 个安全包可升级", auto_fixable=False,
                                   remediation="需人工确认升级窗口"))
    elif distro == "rhel":
        r = run_cmd(target, "yum check-update --security 2>/dev/null | grep -c '\\.el'", timeout=60)
        if r["rc"] in (0, 100):
            n = int(r["stdout"].strip() or 0)
            if n > 0:
                out.append(finding("PCH-01", f"{n} 个安全更新可用", "HIGH", "patch",
                                   f"yum: {n} 个安全包可升级", auto_fixable=False))
    else:
        log("无法确定发行版，跳过安全更新检查", "WARN")
    return out


def scan_kernel(target):
    out = []
    r = run_cmd(target, "uname -r; rpm -q kernel-default 2>/dev/null || dpkg -l linux-image-* 2>/dev/null | grep '^ii'", timeout=10)
    if r["rc"] == 0:
        lines = r["stdout"].strip().splitlines()
        if len(lines) >= 2:
            running = lines[0].strip()
            out.append(finding("PCH-02", "运行内核与已安装最新内核可能不一致", "MEDIUM", "patch",
                               f"运行: {running}; 已安装: {lines[1][:80]}", auto_fixable=False,
                               remediation="需重启以应用新内核"))
    return out


SCOPES = {
    "config": [scan_ssh_config, scan_file_perms, scan_passwd_empty, scan_sudo_nopasswd],
    "service": [scan_services, scan_listening_ports],
    "port": [scan_listening_ports],
    "patch": [scan_security_updates, scan_kernel],
    "ssh": [scan_ssh_config],
}


def main():
    parser = argparse.ArgumentParser(description="服务器漏洞扫描（只读）")
    parser.add_argument("--target", required=True, help="local 或 ssh://user@host[:port]")
    parser.add_argument("--scope", default="all",
                        choices=["all", "config", "service", "port", "patch", "ssh"])
    parser.add_argument("--output", help="输出 JSON 文件路径（默认 stdout）")
    parser.add_argument("--refresh", action="store_true",
                        help="刷新包索引（默认只读，不执行 apt-get update）")
    args = parser.parse_args()

    try:
        target = parse_target(args.target)
    except ValueError as e:
        log(str(e), "ERROR")
        sys.exit(2)

    log(f"开始扫描: target={args.target} scope={args.scope}")

    scopes = list(SCOPES.keys()) if args.scope == "all" else [args.scope]
    findings = []
    errors = []
    for sc in scopes:
        for fn in SCOPES[sc]:
            try:
                if fn is scan_security_updates:
                    findings.extend(fn(args.target, refresh=args.refresh))
                else:
                    findings.extend(fn(args.target))
            except Exception as e:
                errors.append(f"{fn.__name__}: {e}")
                log(f"扫描项 {fn.__name__} 异常: {e}", "WARN")

    sev_count = {s: 0 for s in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]}
    for f in findings:
        sev_count[f["severity"]] = sev_count.get(f["severity"], 0) + 1

    result = {
        "target": args.target, "scope": args.scope,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "findings": findings, "summary": sev_count,
        "total": len(findings), "errors": errors,
    }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        log(f"结果已写入 {args.output}")
    emit_json(result)
    log(f"扫描完成: {len(findings)} 项发现")


if __name__ == "__main__":
    main()
