#!/usr/bin/env python3
"""
tunnel_handler.py — Feishu tunnel control handler
Trigger words:
  /万重山-隧道-开启  → start tunnel
  /万重山-隧道-关闭  → stop tunnel
  /万重山-隧道-状态  → check status
"""
import subprocess, sys, time, re

CONNECT = "/root/.openclaw/skills/wcs-helper-network-skill/scripts/connect.sh"

def strip_ansi(text):
    """去除ANSI颜色码 [N或Nm 格式]"""
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

def run(cmd, timeout=30):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr

def is_running():
    c, _, _ = run("nc -z 127.0.0.1 1080 2>/dev/null")
    return c == 0

def do_start():
    if is_running():
        return "🟡 隧道已在运行，无需重复开启"
    c, out, err = run(f"bash {CONNECT} connect 2>&1", timeout=30)
    time.sleep(3)
    if is_running():
        return "✅ 隧道已开启\n\nGitHub / ClawHub / HuggingFace 等流量走隧道代理"
    out_s = strip_ansi(out + err)
    lines = [l for l in out_s.split("\n") if l.strip()]
    brief = "\n".join(lines[-5:])
    return f"❌ 开启失败\n```\n{brief}\n```"

def do_stop():
    if not is_running():
        return "🟡 隧道未运行，无需关闭"
    c, out, err = run(f"bash {CONNECT} disconnect 2>&1", timeout=20)
    time.sleep(2)
    if not is_running():
        return "🛑 隧道已关闭\n\n所有流量改走本机直连（国际站点可能无法访问）"
    out_s = strip_ansi(out + err)
    lines = [l for l in out_s.split("\n") if l.strip()]
    brief = "\n".join(lines[-3:])
    return f"❌ 关闭失败\n```\n{brief}\n```"

def do_status():
    c, out, err = run(f"bash {CONNECT} status 2>&1", timeout=15)
    out_s = strip_ansi(out + err)
    lines = [l.strip() for l in out_s.split("\n") if l.strip()]
    # 过滤有意义的关键行
    meaningful = [l for l in lines if any(k in l for k in ["autossh", "SOCKS5", "GitHub", "✅", "❌", "服务器", "用户", "端口", "OK", "信息"])]
    body = "\n".join(meaning[:6]) if (meaning := meaningful) else out_s.strip()[:200]
    banner = "🟢 隧道运行中" if is_running() else "🔴 隧道已关闭"
    return f"{banner}\n```\n{body}\n```"

def handle(text=None, command=None, commandName=None, skillName=None):
    """
    Entry point for both SOUL.md trigger words (text=) and OpenClaw tool dispatch (command=, commandName=, skillName=).
    OpenClaw calls this with: { command: "<raw args>", commandName: "<slash command>", skillName: "<skill name>" }
    """
    # Handle both calling conventions
    if command is not None:
        # Called as OpenClaw tool - command is the raw argument string after the slash command
        t = str(command).strip()
    elif text is not None:
        t = str(text).strip()
    else:
        t = ""
    
    if t in ["开启", "开"]:
        return do_start()
    elif t in ["关闭", "关"]:
        return do_stop()
    elif t in ["状态"]:
        return do_status()
    elif t in ["帮助"]:
        return """**隧道控制**

发送以下命令：

• `/万重山-隧道-开启` → 启动隧道（GitHub/ClawHub等走代理）
• `/万重山-隧道-关闭` → 停止隧道（所有流量走本机直连）
• `/万重山-隧道-状态` → 查看当前状态

**开启后**：代理生效，国际站点可访问
**关闭后**：直连生效，本机网络出口"""
    return f"未知命令：`{t}`\n\n发送 `帮助` 查看可用命令"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: tunnel_handler.py <开启|关闭|状态|帮助>", file=sys.stderr)
        sys.exit(1)
    print(handle(sys.argv[1]))
