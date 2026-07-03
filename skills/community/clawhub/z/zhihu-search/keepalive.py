#!/usr/bin/env python3
"""知乎登录态持久化助手

和 zhihu-search skill 配套使用,负责:
  - ab daemon 生命周期管理
  - cookie/state 文件持久化
  - z_c0 滑窗每日续期

用法:
  keepalive.py open [URL]         加载登录态 + 打开页面
  keepalive.py save               把当前 Chrome 状态写入 state 文件
  keepalive.py refresh            打开首页(触发 z_c0 续期) + save
  keepalive.py check              验证登录态是否还有效 (只读,不修改文件)
  keepalive.py inject             转 cookies-raw.txt 为 Netscape 格式 cookies.txt
  keepalive.py install-cron       安装每日 9:00 续期 cron
  keepalive.py status             看 state / daemon / cron 状态
  keepalive.py --help             显示完整帮助

环境变量 (覆盖默认路径,优先级: env > paths.py):
  ZHIHU_DATA_DIR       默认 $SKILL/data/ (自包含), 老 /tmp/zhihu/ 自动兼容
  ZHIHU_COOKIE_FILE    默认 $SKILL/data/cookies.txt
  ZHIHU_STATE          默认 $SKILL/data/state/zhihu.state.json
  ZHIHU_LOG            默认 $SKILL/data/state/cron.log
"""
import argparse
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ===== 路径 (从 paths.py 读) =====
from paths import (
    DATA_DIR, COOKIE_FILE, COOKIE_RAW, STATE_DIR, STATE_FILE, report
)

# ===== 常量 (ab daemon 进程名 + 默认目标) =====
HOME = Path.home()
LOG_FILE = Path(os.environ.get("ZHIHU_LOG", str(STATE_DIR / "cron.log")))
TARGET_DEFAULT = "https://www.zhihu.com/"
SELF_PATH = Path(__file__).resolve()
AB_PROCESS = "agent-browser-linux"

# ===== 底层工具 =====
def run(cmd: list[str], check: bool = False, capture: bool = True) -> subprocess.CompletedProcess:
    """统一运行 shell 命令"""
    return subprocess.run(cmd, capture_output=capture, text=True, check=check)

def is_daemon_running() -> bool:
    """检查 ab daemon 是否在跑 (排除自己 + 父进程)"""
    r = run(["pgrep", "-f", AB_PROCESS])
    pids = [p for p in r.stdout.split() if p not in (str(os.getpid()), str(os.getppid()))]
    return bool(pids)

def kill_daemon() -> None:
    """杀 ab daemon (排除自己 + 父进程避免自杀, 只杀 agent-browser 不杀系统 Chrome)
    不能用 pkill -f: 它的命令行参数含 AB_PROCESS, 会匹配自己.
    """
    r = run(["pgrep", "-f", AB_PROCESS])
    pids = [p for p in r.stdout.split() if p not in (str(os.getpid()), str(os.getppid()))]
    for pid in pids:
        run(["kill", "-9", pid])
    time.sleep(1)

def ab_load_and_open(url: str = TARGET_DEFAULT) -> int:
    """杀 daemon + 用 state load + open URL,返回 ab 的 returncode"""
    if not STATE_FILE.exists():
        print(f"⚠ state 文件不存在: {STATE_FILE}", file=sys.stderr)
        print("  → 首次使用,先走 setup 流程(注入 cookie + state save)", file=sys.stderr)
        return 1
    kill_daemon()
    r = run(["ab", "--state", str(STATE_FILE), "open", url], capture=False)
    return r.returncode

def is_logged_in() -> bool:
    """首页加载完后,检测 '私信' 字样 (登录后右上角才有). 仅对首页准."""
    r = run(["ab", "eval", 'document.body.innerText.includes("私信") ? "OK" : "FAIL"'])
    return "OK" in (r.stdout or "")

def wait_until(condition, timeout: float = 10.0, interval: float = 0.5) -> bool:
    """轮询 condition 直到 True 或超时. condition: callable -> bool"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if condition():
            return True
        time.sleep(interval)
    return False

# ===== 命令 =====
def cmd_open(args):
    """加载登录态 + 打开页面"""
    rc = ab_load_and_open(args.url or TARGET_DEFAULT)
    if rc == 0:
        print(f"✓ 已打开: {args.url or TARGET_DEFAULT}")
    else:
        print(f"✗ 打开失败 (ab 返回 {rc})", file=sys.stderr)
    sys.exit(rc)

def cmd_save(args):
    """把当前 Chrome 状态写入 state 文件"""
    if not STATE_FILE.exists():
        print("✗ {STATE_FILE} 不存在,先 open 一次让浏览器有登录态", file=sys.stderr)
        sys.exit(1)
    if not is_daemon_running():
        print(f"✗ ab daemon 未运行,先跑 'keepalive.py open <url>' 启动浏览器", file=sys.stderr)
        sys.exit(1)
    run(["ab", "state", "save", str(STATE_FILE)])
    st = STATE_FILE.stat()
    size_kb = st.st_size / 1024
    mtime = datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds")
    print(f"✓ 已保存 ({size_kb:.1f} KB, {mtime}) → {STATE_FILE}")

def cmd_refresh(args):
    """打开首页(触发 z_c0 续期) + save 回磁盘. cron 调用入口."""
    if not STATE_FILE.exists():
        print("⚠ state 文件不存在,无法续期", file=sys.stderr)
        print("  → 请先跑 setup (注入 cookie + save state)", file=sys.stderr)
        sys.exit(1)
    rc = ab_load_and_open(TARGET_DEFAULT)
    if rc != 0:
        print(f"✗ open 失败 (rc={rc}),跳过续期", file=sys.stderr)
        sys.exit(rc)
    # 等页面加载完,确保请求触发 z_c0 续期
    if wait_until(is_logged_in, timeout=10):
        run(["ab", "state", "save", str(STATE_FILE)])
        print(f"✓ 续期完成 ({datetime.now().isoformat(timespec='seconds')})")
    else:
        print("⚠ 页面未在 10s 内加载完成,但仍尝试 save", file=sys.stderr)
        run(["ab", "state", "save", str(STATE_FILE)])
        sys.exit(1)

def cmd_check(args):
    """验证登录态是否还有效. 只读,不修改任何文件."""
    if not STATE_FILE.exists():
        print("✗ state 文件不存在", file=sys.stderr)
        sys.exit(1)
    rc = ab_load_and_open(TARGET_DEFAULT)
    if rc != 0:
        print(f"✗ open 失败 (rc={rc})", file=sys.stderr)
        sys.exit(rc)
    if wait_until(is_logged_in, timeout=10):
        print("✓ 登录态有效")
        sys.exit(0)
    else:
        print("✗ 登录态已失效 → 重新导出 cookie 走 setup", file=sys.stderr)
        sys.exit(1)

def cmd_install_cron(args):
    """安装每日 9:00 自动续期 cron"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    # 用 shebang 路径而非 sys.executable (venv 漂移保护)
    python_bin = sys.executable if Path(sys.executable).is_absolute() else "/usr/bin/python3"
    cron_line = f'0 9 * * * {python_bin} {SELF_PATH} refresh >>{LOG_FILE} 2>&1'

    # 读现有 crontab (没有 crontab 时 crontab -l 返回非 0)
    r = run(["crontab", "-l"], check=False)
    existing = r.stdout if r.returncode == 0 and r.stdout else ""

    if "keepalive.py refresh" in existing:
        print("✓ 每日 9 点保活 cron 已存在:")
        for line in existing.splitlines():
            if "keepalive.py" in line:
                print(f"  {line}")
        return

    # 追加 (用 stdin 而非 crontab 文件,避免权限问题)
    new_content = (existing.rstrip("\n") + "\n" + cron_line + "\n") if existing.strip() else (cron_line + "\n")
    proc = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
    proc.communicate(new_content)
    if proc.returncode != 0:
        print(f"✗ crontab 安装失败 (rc={proc.returncode})", file=sys.stderr)
        sys.exit(1)
    print(f"✓ 已安装 cron: 每天 9:00 触发 z_c0 续期")
    print(f"  日志: {LOG_FILE}")

def cmd_status(args):
    """看 state / daemon / cron 状态"""
    print("=== state 文件 ===")
    if STATE_FILE.exists():
        st = STATE_FILE.stat()
        age_h = (time.time() - st.st_mtime) / 3600
        print(f"  {STATE_FILE}")
        print(f"  {st.st_size/1024:.1f} KB, 距今 {age_h:.1f} 小时")
    else:
        print("  ✗ 不存在")

    print("\n=== ab daemon 状态 ===")
    if is_daemon_running():
        r = run(["pgrep", "-f", AB_PROCESS])
        print(f"  运行中 (PID: {r.stdout.strip()})")
    else:
        print("  未运行")

    print("\n=== cron 保活 ===")
    r = run(["crontab", "-l"], check=False)
    if "keepalive.py refresh" in (r.stdout or ""):
        print("  ✓ 已启用")
        for line in (r.stdout or "").splitlines():
            if "keepalive.py" in line:
                print(f"  {line}")
    else:
        print("  ✗ 未启用,运行 'keepalive.py install-cron' 启用")

# ===== CLI =====
def main():
    p = argparse.ArgumentParser(
        prog="keepalive.py",
        description="知乎登录态持久化助手(和 zhihu-search skill 配套)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="cmd", required=True, metavar="<命令>")

    sp = sub.add_parser("open", help="加载登录态 + 打开页面")
    sp.add_argument("url", nargs="?", default=TARGET_DEFAULT, help="要打开的 URL (默认知乎首页)")
    sp.set_defaults(func=cmd_open)

    sp = sub.add_parser("save", help="把当前 Chrome 状态写入 state 文件")
    sp.set_defaults(func=cmd_save)

    sp = sub.add_parser("refresh", help="打开首页(触发 z_c0 续期) + 自动 save (cron 调用)")
    sp.set_defaults(func=cmd_refresh)

    sp = sub.add_parser("check", help="验证登录态是否还有效 (只读,退出码: 0=有效, 1=失效)")
    sp.set_defaults(func=cmd_check)

    sp = sub.add_parser("install-cron", help="安装每日 9:00 续期 cron")
    sp.set_defaults(func=cmd_install_cron)

    sp = sub.add_parser("status", help="查看 state/daemon/cron 状态")
    sp.set_defaults(func=cmd_status)

    sp = sub.add_parser("paths", help="打印当前 skill 的路径配置 (含 data 目录, cookies 路径)")
    sp.set_defaults(func=lambda a: print(report()))

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()