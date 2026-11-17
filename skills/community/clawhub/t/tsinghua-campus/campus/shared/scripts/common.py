"""common.py — 技能包共享公共库

所有脚本通过 `sys.path.insert(0, <shared/scripts>)` + `import common` 引入。
提供:
- output_json(): stdout JSON 输出（UnicodeEncodeError fallback）
- log(): 进度日志 → 写 runtime/logs/campus.log（不写 stderr，避免 PowerShell 渲染成错误）
- platform 检测: detect_platform() → windows / macos / linux_wsl / linux
- 路径管理: skill 根目录、runtime（凭据/会话/profile/下载）

约定:
- stdout → JSON（供 AI 解析），进度日志 → runtime/logs/campus.log 文件
- 脚本禁止 input()/getpass() 阻塞（见 AGENTS.md 铁律）
"""
import os
import sys
import json
import time
import tempfile
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def output_json(data, indent=2):
    """stdout 输出 JSON（含中文/emoji 时用 buffer 写 UTF-8 字节）"""
    text = json.dumps(data, ensure_ascii=False, indent=indent, default=str)
    try:
        print(text, flush=True)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((text + "\n").encode("utf-8"))


def _log_file():
    d = _skill_root() / "runtime" / "logs"
    d.mkdir(parents=True, exist_ok=True)
    return d / "campus.log"


def log(msg):
    """进度日志 → 写 runtime/logs/campus.log（带时间戳，不写 stderr）。

    不写 stderr 的原因：Windows PowerShell 会把脚本的 stderr 输出渲染成
    `python.exe : ...` 错误记录，干扰 AI/用户判断。日志文件供排错追溯。
    """
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(_log_file(), "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")
    except Exception:
        pass


def detect_platform():
    """返回平台标识: windows / macos / linux_wsl / linux"""
    if sys.platform == "win32":
        return "windows"
    if sys.platform == "darwin":
        return "macos"
    # Linux: 检测 WSL
    try:
        if "microsoft" in Path("/proc/version").read_text(encoding="utf-8", errors="replace").lower():
            return "linux_wsl"
    except Exception:
        pass
    return "linux"


def _skill_root():
    """技能包根目录 = common.py 所在目录的上一级（shared/scripts/../.. = skill/campus/）"""
    return Path(__file__).resolve().parent.parent.parent


def runtime_dir(*sub):
    """运行时数据目录（skill/campus/runtime/），自动创建。

    注意：*sub 最后一个元素若是文件名（如 credentials.json），
    只创建其父目录，不把文件名当目录建。"""
    d = _skill_root() / "runtime"
    for s in sub[:-1]:
        d = d / s
        d.mkdir(parents=True, exist_ok=True)
    if sub:
        d = d / sub[-1]
    d.parent.mkdir(parents=True, exist_ok=True)
    return d


def skill_root():
    return _skill_root()


def browser_profile_dir():
    """Playwright 持久 profile（复用 CAS cookies 免 2FA）"""
    return runtime_dir("profiles", "default_profile")


def pending_dir():
    """两阶段验证码 pending 状态目录"""
    return runtime_dir("sessions", "pending")


def session_dir():
    return runtime_dir("sessions")
