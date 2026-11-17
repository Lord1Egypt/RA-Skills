#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autologin.py —— QQ 群作业登录态自动恢复（QQ 浏览器 skill 原生点击）

适用：qun.qq.com 的 ptlogin 会话过期（bkn 仍能取到、但 day --refresh 报
`ptlogin-ex verify fail`），而**本机 QQ 客户端已登录**时，自动点击快捷登录
头像完成网页登录，省去人工重登。

前提：
  - Windows + QQ 浏览器 + qqbrowser-skill / x5use 1.6.3+
  - 本机 QQ 客户端已登录（快捷登录列表 #qlogin_list 才会渲染）
  - QQB_CLI 指向 qqbrowser-skill.exe（隔离 venv 安装时必填）
  - 浏览器命令需在沙箱外运行（dangerouslyDisableSandbox: true）

用法：
  python scripts/autologin.py                       # 自动登录 + 页面重定向验证
  python scripts/autologin.py --probe               # 只探测快捷登录列表，不点击
  python scripts/autologin.py --gid <群号>          # 额外用 bkn 验证登录态
  python scripts/autologin.py --gid <群号> --verify-day --date <日期>
                                                   # 完整闭环：再跑 day --refresh

环境变量（全部可选，除 QQB_CLI）：
  QQB_CLI                qqbrowser-skill.exe 绝对路径
  QQB_BROWSER_EXE        QQBrowser.exe 绝对路径（默认查注册表/常见安装位置）
  QQB_AUTOLOGIN_PROFILE  独立 profile 目录（默认 %LOCALAPPDATA%/qqbrowser-skill/autologin-profile）

实现要点（踩过的坑，别改回去）：
  1. 必须在**单次调用内**跑完全链路：daemon 跨调用会被平台清理，扩展不会重连新 daemon。
  2. 直接再启动带 `--x5use-automatic-in-tab` 的浏览器会被**单实例转发**，flag 不生效；
     必须用独立 `--user-data-dir` 起一个真正独立的实例，且不强杀用户现有窗口。
  3. `#qlogin_list` 在跨域 iframe（xui.ptlogin2.qq.com）里，CLI 的 snapshot /
     find_and_act 只看顶层 frame —— 必须把 xlogin URL **在顶层打开**，列表才进入主 DOM。
  4. 选择器必须是 `#qlogin_list a`：写 `#qlogin a` 会点到「QQ手机版」下载链接。
  5. 浏览器禁止 `document.cookie`（CLI 报 forbidden API）；bkn 用 performance 资源条目。

⛔ 全程不强杀任何现有浏览器窗口；所有新拉起的进程经 FocusGuard 无焦点启动，
   不改变用户桌面当前焦点（全屏游戏 / 办公场景尤其重要）。
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from focusless import FocusGuard  # noqa: E402

CLI = (os.environ.get("QQB_CLI") or shutil.which("qqbrowser-skill") or "").strip()
PY = sys.executable
QQ_HW = str(HERE / "qq_hw.py")

_la = Path(os.environ.get("LOCALAPPDATA") or Path.home())
QB_LOG_DIR = _la / "qqbrowser-skill" / "logs"
DAEMON_LOG = QB_LOG_DIR / "daemon.log"
QB_LOG = QB_LOG_DIR / "qb_autologin.log"
PROFILE = Path(os.environ.get("QQB_AUTOLOGIN_PROFILE")
               or (_la / "qqbrowser-skill" / "autologin-profile"))

# qun.qq.com 登录页嵌入的 ptlogin iframe 地址（appid 为站点固定值，非账号信息）
PT_URL = ("https://xui.ptlogin2.qq.com/cgi-bin/xlogin?pt_disable_pwd=1"
          "&appid=715030901&hide_close_icon=1&daid=73&pt_no_auth=1"
          "&s_url=https%3A%2F%2Fqun.qq.com%2F")
LOGIN_URL = "https://qun.qq.com/#/login"

# 注意：探测 JS 里绝不能用 document.cookie（CLI 安全策略会拒）
STATE = r"""JSON.stringify({url:location.href,
  txt:document.body.innerText.replace(/\s+/g,' ').slice(0,200),
  qloginA:document.querySelectorAll('#qlogin_list a').length})"""


def browser_exe():
    """定位 QQBrowser.exe：环境变量 > 注册表 > 常见安装位置。"""
    env = os.environ.get("QQB_BROWSER_EXE", "").strip()
    if env and Path(env).is_file():
        return env
    try:
        import winreg
        probes = [
            (winreg.HKEY_CURRENT_USER,
             r"Software\Tencent\QQBrowser\CurrentVersion\App Paths\QQBrowser.exe", ""),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Tencent\QQBrowser", "InstallPath"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Tencent\QQBrowser", "InstallPath"),
        ]
        for hive, key, value_name in probes:
            try:
                with winreg.OpenKey(hive, key) as k:
                    val, _ = winreg.QueryValueEx(k, value_name)
                p = Path(val) if value_name == "" else Path(val) / "QQBrowser.exe"
                if p.is_file():
                    return str(p)
            except OSError:
                continue
    except Exception:
        pass
    roots = [os.environ.get("ProgramFiles", ""), os.environ.get("ProgramFiles(x86)", ""),
             os.environ.get("LOCALAPPDATA", "")]
    for root in roots:
        if not root:
            continue
        for rel in ("Tencent/QQBrowser/QQBrowser.exe", "QQBrowser/QQBrowser.exe"):
            p = Path(root) / rel
            if p.is_file():
                return str(p)
    return ""


def run(args, timeout=90):
    if not CLI:
        return "[ERROR] QQB_CLI 未设置，请先指向 qqbrowser-skill.exe"
    try:
        p = subprocess.run([CLI] + args, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return "[TIMEOUT] " + " ".join(args)
    except Exception as e:
        return "[ERROR] %r" % e


def text(raw):
    m = re.search(r"\[RESULT\]\s*(\{.*\})\s*$", raw, re.DOTALL)
    if m:
        try:
            t = json.loads(m.group(1)).get("text", "")
            if isinstance(t, str) and t.strip():
                return t
        except Exception:
            pass
    return raw


def ev(js, sid, timeout=60):
    return text(run(["browser_eval_content_js", "--script", js,
                     "--sessionId", sid], timeout))


def log_lines():
    try:
        return DAEMON_LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return []


def qq_hw(args, timeout=180):
    env = dict(os.environ, QQB_CLI=CLI)
    try:
        p = subprocess.run([PY, QQ_HW] + args, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=env, timeout=timeout)
        return (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return "[TIMEOUT] qq_hw.py " + " ".join(args)
    except Exception as e:
        return "[ERROR] %r" % e


def main():
    ap = argparse.ArgumentParser(description="QQ 群作业登录态自动恢复（原生点击快捷登录）")
    ap.add_argument("--probe", action="store_true", help="只探测快捷登录列表，不点击、不验证")
    ap.add_argument("--gid", default="", help="群号；给出时用 bkn 追加验证登录态")
    ap.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="--verify-day 使用的日期")
    ap.add_argument("--verify-day", action="store_true", help="完整闭环：额外跑 day --refresh")
    ap.add_argument("--wait", type=int, default=9, help="等待快捷登录列表渲染的秒数（默认 9）")
    args = ap.parse_args()

    if not CLI or not Path(CLI).is_file():
        print("!! 找不到 qqbrowser-skill.exe，请设置 QQB_CLI")
        return 2
    qb = browser_exe()
    if not qb:
        print("!! 找不到 QQBrowser.exe，请设置 QQB_BROWSER_EXE")
        return 2

    PROFILE.mkdir(parents=True, exist_ok=True)
    QB_LOG_DIR.mkdir(parents=True, exist_ok=True)
    guard = FocusGuard("autologin")
    print("[0] 拉起进程前的桌面前台窗口：", guard.origin_title or "<无标题>")
    base = len(log_lines())

    m = re.search(r"T-\d{10}-\d", run(["get_session_id"], 30))
    if not m:
        print("!! 无法获取 session id"); return 2
    sid = m.group(0)
    print("[1] SID =", sid)

    print("[2] 后台起 daemon（无焦点启动）")
    p = guard.launch([CLI, "browser_start_session", "--sessionId", sid],
                     no_window=False,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                     text=True, encoding="utf-8", errors="replace")
    time.sleep(5)

    print("[3] 独立 profile + 自动化 flag 拉起 QQ 浏览器（不抢焦点）")
    flags = ["--display-invisible-extension=true", "--disable-infobars",
             # ⛔ 不用 --start-maximized：最大化必然创建前台窗口抢焦点
             "--window-position=80,80", "--window-size=960,720",
             "--x5use-automatic-in-tab", "--no-first-run",
             "--no-crashed-bubble-view", "--no-modal-dialogs",
             "--no-external-protocol-dialogs", "--no-sandbox",
             # 窗口压到 Z 序底部后 Chromium 会节流渲染，禁用之
             "--disable-backgrounding-occluded-windows",
             "--disable-renderer-backgrounding",
             "--disable-background-timer-throttling",
             "--user-data-dir=" + str(PROFILE), PT_URL]
    with QB_LOG.open("a", encoding="utf-8", errors="replace") as qf:
        guard.launch([qb] + flags, no_window=False, stdout=qf, stderr=subprocess.STDOUT)

    print("[3b] 新窗口加固数 =", guard.harden_new_windows(timeout=12))
    guard.report("browser-launched")

    print("[4] 等扩展连接 daemon")
    ok = False
    deadline = time.time() + 60
    while time.time() < deadline:
        for ln in log_lines()[base:]:
            if "浏览器扩展客户端连接成功" in ln:
                print("   ✅", ln.strip()[:140]); ok = True; break
        if ok:
            break
        time.sleep(2)
    try:
        out, _ = p.communicate(timeout=65)
        print("[5] start_session ->", (out or "").strip()[:170].replace("\n", " "))
    except subprocess.TimeoutExpired:
        p.kill(); print("[5] start_session 超时")
    if not ok:
        print("!! 扩展未连上 daemon（可刷新已开的 qun.qq.com 标签页后重试）")
        return 3

    print("\n[6] 顶层打开 ptlogin 快捷登录页，等 %ds" % args.wait)
    run(["browser_go_to_url", "--url", PT_URL, "--sessionId", sid], 60)
    time.sleep(args.wait)
    state = ev(STATE, sid)
    print("   ", state[:400])
    try:
        qlogin_a = json.loads(state).get("qloginA", 0)
    except Exception:
        qlogin_a = 0
    if not qlogin_a:
        print("!! 未渲染 #qlogin_list：请确认本机 QQ 客户端已登录")
        return 4
    print("   检测到快捷登录项：", qlogin_a)
    if args.probe:
        guard.report("probe-done")
        print("\n=== 探测完成（--probe，未点击） ===")
        return 0

    print("\n[7] 原生模拟点击 #qlogin_list a")
    click = run(["browser_find_and_act", "--by", "css", "--value", "#qlogin_list a",
                 "--action", "click", "--nth", "1", "--sessionId", sid], 60)
    print("   ", click.strip()[:400])
    if "Clicked element" not in click:
        print("!! 点击未成功"); return 6
    time.sleep(8)

    print("\n[8] 登录态验证（访问登录页应被重定向）")
    run(["browser_go_to_url", "--url", LOGIN_URL, "--sessionId", sid], 60)
    time.sleep(5)
    after = ev(STATE, sid)
    print("   ", after[:350])
    login_ok = ("ptlogin" not in after and "qlogin_list" not in after
                and "/#/login" not in after)
    print("   ✅ 自动登录成功" if login_ok else "   ⚠️ 页面重定向未确认（仍会尝试后续验证）")
    guard.harden_new_windows(timeout=3)
    guard.report("after-click")

    if args.gid:
        print("\n[9] 主流程验证：qq_hw.py bkn --gid <群号>")
        b = qq_hw(["bkn", "--gid", args.gid], timeout=150)
        print("   ", b.strip()[-300:])
        if args.verify_day:
            print("\n[10] 主流程验证：qq_hw.py day %s --refresh" % args.date)
            d = qq_hw(["day", args.date, "--refresh"], timeout=200)
            print("   ", d.strip()[-400:])

    guard.harden_new_windows(timeout=3)
    kept, desc = guard.report("final")
    print("\n=== 完成（登录确认=%s，焦点保持=%s） ===" % (login_ok, kept))
    return 0


if __name__ == "__main__":
    sys.exit(main())
