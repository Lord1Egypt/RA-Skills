#!/usr/bin/env python3
"""_common.py — server-security-guard 脚本共享工具

提供目标解析、命令执行（本地/SSH）、JSON 输出与资源解析。
所有脚本通过本模块执行命令，不在脚本中直接 subprocess/ssh。
"""

import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent

# Debian/Ubuntu 服务名为 ssh，RHEL/CentOS 为 sshd；按顺序回退，全部失败不致命。
RELOAD_SSHD = ("systemctl reload sshd 2>/dev/null || systemctl reload ssh 2>/dev/null "
               "|| systemctl reload openssh-server 2>/dev/null || true")


def log(msg, level="INFO"):
    """进度/错误输出到 stderr（不污染 stdout 的 JSON）。"""
    print(f"[{level}] {msg}", file=sys.stderr, flush=True)


def emit_json(data):
    """最终结果以 JSON 输出到 stdout。"""
    print(json.dumps(data, ensure_ascii=False, indent=2))


def parse_target(target):
    """解析目标字符串。

    返回 dict:
      {"mode": "local"} 或
      {"mode": "ssh", "user": ..., "host": ..., "port": 22}
    非法时抛 ValueError。
    """
    if not target:
        raise ValueError("target 为空")
    if target == "local":
        return {"mode": "local"}
    m = re.match(r'^ssh://([^@]+)@([^:]+)(?::(\d+))?$', target)
    if m:
        return {"mode": "ssh", "user": m.group(1), "host": m.group(2),
                "port": int(m.group(3)) if m.group(3) else 22}
    raise ValueError(f"无法解析 target: {target}（应为 local 或 ssh://user@host[:port]）")


def run_cmd(target, cmd, timeout=30):
    """执行 shell 命令（本地或远程 SSH）。

    返回 dict: {"rc": int, "stdout": str, "stderr": str}
    SSH 失败（连接错误）返回 rc=-1 并在 stderr 标注。
    不抛异常，由调用方判断 rc。
    """
    t = parse_target(target) if isinstance(target, str) else target
    try:
        if t["mode"] == "local":
            proc = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,
                timeout=timeout, encoding="utf-8", errors="replace")
            return {"rc": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
        else:
            ssh_cmd = ["ssh", "-p", str(t["port"]),
                       "-o", "BatchMode=yes", "-o", "ConnectTimeout=10",
                       "-o", "StrictHostKeyChecking=accept-new",
                       f"{t['user']}@{t['host']}", cmd]
            proc = subprocess.run(
                ssh_cmd, capture_output=True, text=True,
                timeout=timeout, encoding="utf-8", errors="replace")
            return {"rc": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
    except subprocess.TimeoutExpired:
        return {"rc": -1, "stdout": "", "stderr": f"命令超时（{timeout}s）: {cmd}"}
    except FileNotFoundError as e:
        return {"rc": -1, "stdout": "", "stderr": f"执行器不存在: {e}"}
    except Exception as e:
        return {"rc": -1, "stdout": "", "stderr": f"执行异常: {e}"}


def read_file(target, path, timeout=15):
    """读取目标上的文件内容（cat）。返回 str 或 None。"""
    r = run_cmd(target, f"cat {shlex.quote(path)}", timeout=timeout)
    if r["rc"] == 0:
        return r["stdout"]
    return None


def read_resource(rel_path):
    """读取 Skill 内资源（基于脚本位置，不依赖 cwd）。"""
    p = SKILL_ROOT / rel_path
    if not p.exists():
        raise FileNotFoundError(f"Skill 资源不存在: {p}")
    return p.read_text(encoding="utf-8")


def is_root(target):
    """判断当前用户是否为 root。"""
    r = run_cmd(target, "id -u", timeout=10)
    return r["rc"] == 0 and r["stdout"].strip() == "0"


def detect_distro(target):
    """检测目标发行版。返回 'debian'/'rhel'/'unknown'。"""
    r = run_cmd(target, "cat /etc/os-release", timeout=10)
    if r["rc"] == 0:
        if "debian" in r["stdout"].lower() or "ubuntu" in r["stdout"].lower():
            return "debian"
        if "rhel" in r["stdout"].lower() or "centos" in r["stdout"].lower() or "fedora" in r["stdout"].lower():
            return "rhel"
    return "unknown"


def cidr_match(ip, cidrs):
    """判断 ip 是否落在任一 CIDR/单 IP 条目内（支持 IPv4/IPv6 任意前缀长度）。

    条目非法（写错、空串）时跳过该条并继续，不抛异常。
    裸 IP（无 / 前缀）按单主机 /32 或 /128 处理。
    """
    import ipaddress

    try:
        addr = ipaddress.ip_address(str(ip).strip())
    except ValueError:
        return False
    for entry in cidrs or []:
        s = str(entry).strip()
        if not s:
            continue
        try:
            if "/" in s:
                net = ipaddress.ip_network(s, strict=False)
                if addr.version == net.version and addr in net:
                    return True
            else:
                if addr == ipaddress.ip_address(s):
                    return True
        except ValueError:
            continue
    return False


def write_audit(target, message):
    """写审计日志（尽力而为，失败不中断）。"""
    line = f"[{message}]\n"
    cmd = (f'echo {shlex.quote(line)} >> /var/log/security-guard-audit.log 2>/dev/null '
           f'|| echo {shlex.quote(line)} >> security-guard-audit.log')
    run_cmd(target, cmd, timeout=5)
