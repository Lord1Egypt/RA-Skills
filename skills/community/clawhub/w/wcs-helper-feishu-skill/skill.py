#!/usr/bin/env python3
"""guanqi-feishu-config skill — 飞书卡片输出"""
import json, subprocess, sys
from pathlib import Path

PREFIX = "/万重山-飞书"

def md(t): return {"tag": "markdown", "content": t}
def hr(): return {"tag": "hr"}
def make_card(title, elements):
    return {
        "config": {"wide_screen_mode": True},
        "header": {"title": {"tag": "plain_text", "content": title}, "template": "purple"},
        "elements": elements
    }

def get_procs():
    try:
        r = subprocess.run(["pgrep","-f","openclaw","-c"], capture_output=True, text=True, timeout=3)
        return int(r.stdout.strip()) if r.stdout.strip().isdigit() else 0
    except: return 0

def get_streaming():
    try:
        r = subprocess.run(["openclaw","config","get","channels.feishu.streaming"], capture_output=True, text=True, timeout=5)
        v = r.stdout.strip().lower()
        return True if v=="true" else False if v=="false" else None
    except: return None

def get_require_mention():
    try:
        r = subprocess.run(["openclaw","config","get","channels.feishu.requireMention"], capture_output=True, text=True, timeout=5)
        v = r.stdout.strip().lower()
        return True if v=="true" else False if v=="false" else None
    except: return None

def cmd_status():
    p=get_procs(); st=get_streaming(); mt=get_require_mention()
    txt = (f"🤖 服务状态    {'✅ 正常' if p>0 else '❌ 未运行'}  ({p}个进程)\n"
           f"✏️ 打字效果  {'✅ 开启' if st==True else '❌ 关闭' if st==False else '⚠️ 未设置'}\n"
           f"💬 群里回复  {'✅ 只回@我的' if mt==True else '🔊 什么都回' if mt==False else '⚠️ 未设置'}")
    return make_card("🦞 飞书配置", [
        md("**当前配置：**"),
        hr(),
        md("```\n" + txt + "\n```"),
        hr(),
        md("**发送命令控制：**"),
        md(f"• `{PREFIX}`             → 查看设置\n"
           f"• `{PREFIX}-打字效果`    → 开/关打字效果\n"
           f"• `{PREFIX}-群里-A`      → 群里只回@我\n"
           f"• `{PREFIX}-群里-B`    → 群里什么都回\n"
           f"• `{PREFIX}-诊断`        → 检查状态\n"
           f"• `{PREFIX}-重启`        → 重启服务"),
    ])

def cmd_toggle():
    cur = get_streaming(); new_val = not cur if cur in (True,False) else True
    subprocess.run(["openclaw","config","set","channels.feishu.streaming",str(new_val).lower()], capture_output=True, timeout=5)
    return make_card("📡 打字效果", [
        md(f"**{'✅ 已开启' if new_val else '❌ 已关闭'}**"),
        hr(),
        md(f"打字效果已{'开启' if new_val else '关闭'}，{'有实时对话感' if new_val else '关闭打字效果'}"),
    ])

def cmd_set_mention(mode):
    val = "true" if mode.upper()=="A" else "false"
    subprocess.run(["openclaw","config","set","channels.feishu.requireMention",val], capture_output=True, timeout=5)
    label = "✅ 只回@我的" if val=="true" else "🔊 什么都回"
    return make_card("💬 群里回复", [
        md(f"**{label}**"),
        hr(),
        md(f"群里回复已设为：{label}"),
    ])

def cmd_diagnose():
    p=get_procs(); st=get_streaming(); mt=get_require_mention()
    oc = subprocess.run(["openclaw","status"], capture_output=True, text=True, timeout=15)
    txt = (f"🤖 OpenClaw    {'✅ 运行中' if p>0 else '❌ 未运行'}\n"
           f"✏️ 打字效果  {'✅ 开启' if st==True else '❌ 关闭' if st==False else '⚠️ 未设置'}\n"
           f"💬 群里回复  {'✅ 只回@我的' if mt==True else '🔊 什么都回' if mt==False else '⚠️ 未设置'}\n"
           f"🔧 status     {'✅ 正常' if oc.returncode==0 else '❌ 异常'}")
    return make_card("🔍 诊断结果", [
        md("```\n" + txt + "\n```"),
        hr(),
        md("如有问题，发送 `/万重山-飞书-重启` 重启服务"),
    ])

def cmd_restart():
    subprocess.run(["openclaw","gateway","restart"], capture_output=True, timeout=10)
    return make_card("🚀 重启中", [
        md("**重启指令已发出**"),
        hr(),
        md("服务将在几秒内重启，请稍候..."),
    ])

def cmd_help():
    return make_card("🦞 帮助", [
        md("**发送命令控制飞书插件：**"),
        hr(),
        md(f"• `{PREFIX}`             → 查看当前设置\n"
           f"• `{PREFIX}-打字效果`    → 开/关打字效果\n"
           f"• `{PREFIX}-群里-A`      → 群里只回@我的\n"
           f"• `{PREFIX}-群里-B`      → 群里什么都回\n"
           f"• `{PREFIX}-诊断`        → 检查状态\n"
           f"• `{PREFIX}-重启`         → 重启服务"),
    ])

def handle(raw):
    suffix = PREFIX + "-"
    if raw == PREFIX or raw == PREFIX.lower(): return cmd_status()
    sub = raw[len(suffix):] if raw.startswith(suffix) else (raw[len(PREFIX)+1:] if raw.startswith(PREFIX.lower()+"-") else None)
    if sub is None: return cmd_status()
    if sub in ("","状态"): return cmd_status()
    if sub == "帮助": return cmd_help()
    if sub == "打字效果": return cmd_toggle()
    if sub.startswith("群里-"): return cmd_set_mention(sub[3:])
    if sub == "诊断": return cmd_diagnose()
    if sub == "重启": return cmd_restart()
    return cmd_help()

if __name__ == "__main__":
    result = handle(sys.argv[1]) if len(sys.argv) > 1 else cmd_status()
    if result:
        print(json.dumps(result))
