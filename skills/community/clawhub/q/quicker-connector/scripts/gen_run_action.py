#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_run_action.py —— 生成 Quicker「运行程序或打开文件」(ActionType 11) 动作 JSON

根据「要运行的程序 / 脚本 / 命令」生成一个可直接导入 Quicker 的动作定义 JSON：
- 默认 ActionType 11（运行程序或打开文件）
- 默认不用管理员（RunAsAdmin=false）
- 默认勾选「如果已在运行，则尝试激活已打开的窗口」（ActivateWindowIfRunning=true）
- 默认最小化启动（WindowStyle=2）
- 工作目录默认取脚本/程序所在目录
- 名称智能生成（脚本 docstring 首行 / 文件名清洗）
- 脚本类（.py/.ps1/.bat/.cmd）默认「脱离 Quicker 启动」：通过 .cache/launchers/*.ps1 启动器启动
  （动作本体为 powershell.exe -File 启动器，内部用 Start-Process 让目标进程完全脱离），
  使 Quicker 动作立即结束、进程真正后台常驻。否则 Quicker 会把进程当子进程跟踪，
  依赖全局键盘钩子（如 keyboard 库）的脚本会收不到按键，直到手动终止动作才生效。
  注意：不要用 cmd.exe /c + start 方案——Quicker 启动 cmd 时接管 stdout 管道，start 在
  管道环境下会等待子进程，整条链会被拖住卡在「运行中」。powershell.exe -File 是参考
  动作（awam待办UI）验证过的可用模式，启动器文件名保持纯 ASCII。
- 支持把标准输出与错误重定向到日志文件，便于排查执行状态（--log）
  日志默认写入 <技能库>/.cache/logs/（stdout 用 .log、stderr 用 .err.log），
  启动器写入 .cache/launchers/，均已被 .gitignore 忽略，不会进 Git

典型用法：
  # 运行 Python 脚本并开启日志（自动探测解释器、脱离启动）
  python scripts/gen_run_action.py --script "G:\\Projects\\Tools\\potplayer-helper\\potplayer_clip.py" --log

  # 直接运行/打开某个程序或文件
  python scripts/gen_run_action.py --command "notepad.exe" "C:\\a.txt"

  # 运行 PowerShell 脚本
  python scripts/gen_run_action.py --script "x.ps1"

  # 自定义名称 / 工作目录 / 关闭日志 / 指定解释器 / 输出文件
  python scripts/gen_run_action.py --script a.py --name "我的动作" --workdir D:\\work --no-log --interpreter "C:\\Python312\\python.exe"
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone, timedelta

# 技能库根目录（本脚本位于 scripts/ 下）
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_LOG_DIR = os.path.join(SKILL_ROOT, ".cache", "logs")
DEFAULT_LAUNCHER_DIR = os.path.join(SKILL_ROOT, ".cache", "launchers")

SCRIPT_EXTS = (".py", ".ps1", ".bat", ".cmd")


def now_iso() -> str:
    """生成与 Quicker 导出格式一致的本地时间 ISO 字符串（带 +08:00）。"""
    tz = timezone(timedelta(hours=8))
    return datetime.now(tz).isoformat()


def shell_quote(p: str) -> str:
    """给路径加双引号（用于外壳命令行）。"""
    return '"' + p + '"'


def smart_name(script_path: str, explicit: str | None) -> str:
    """智能起名：优先用脚本 docstring 首行，否则用文件名清洗。"""
    if explicit:
        return explicit
    base = os.path.basename(script_path)
    stem = os.path.splitext(base)[0]
    try:
        with open(script_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read(4096)
        m = re.search(r'"""([\s\S]*?)"""', text)
        if m:
            for line in m.group(1).splitlines():
                s = line.strip()
                if s and not set(s) <= set("=-_#*"):
                    return s
    except OSError:
        pass
    stem = stem.replace("_", " ").replace("-", " ").strip()
    return stem or base


def top_level_imports(script_path: str) -> list[str]:
    """提取脚本顶层 import / from 的顶层模块名（用于探测解释器依赖）。"""
    mods: list[str] = []
    try:
        with open(script_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.lstrip()
                if line.startswith("import "):
                    for part in line[len("import "):].split(","):
                        name = part.strip().split()[0].split(".")[0]
                        if name and name not in mods:
                            mods.append(name)
                elif line.startswith("from "):
                    m = re.match(r"from\s+([A-Za-z0-9_.]+)", line)
                    if m:
                        name = m.group(1).split(".")[0]
                        if name and name not in mods:
                            mods.append(name)
                if line and not line.startswith(("import ", "from ")) and mods:
                    break
    except OSError:
        pass
    stdlib = {
        "os", "sys", "re", "time", "json", "math", "random", "datetime", "pathlib",
        "subprocess", "threading", "logging", "argparse", "shutil", "collections",
        "typing", "itertools", "functools", "io", "glob", "string", "textwrap",
    }
    return [m for m in mods if m not in stdlib]


def candidate_pythons() -> list[str]:
    """收集候选 Python 解释器（按可用性排序）。"""
    cands: list[str] = []
    for name in ("python", "python3"):
        p = shutil.which(name)
        if p:
            cands.append(p)
    wb = os.path.expandvars(r"C:\Users\Administrator\.workbuddy\binaries\python\versions")
    if os.path.isdir(wb):
        for d in sorted(os.listdir(wb), reverse=True):
            ep = os.path.join(wb, d, "python.exe")
            if os.path.isfile(ep):
                cands.append(ep)
    pe = os.path.expandvars(r"C:\Users\Administrator\.pyenv\pyenv-win\versions")
    if os.path.isdir(pe):
        for d in sorted(os.listdir(pe), reverse=True):
            ep = os.path.join(pe, d, "python.exe")
            if os.path.isfile(ep):
                cands.append(ep)
    seen, uniq = set(), []
    for c in cands:
        if c not in seen:
            seen.add(c)
            uniq.append(c)
    return uniq


def detect_interpreter(script_path: str, explicit: str | None) -> str:
    """为 .py 脚本挑选能成功 import 其依赖的最高版本解释器。"""
    if explicit:
        return explicit
    mods = top_level_imports(script_path)
    if not mods:
        return shutil.which("python") or "python"

    def version_of(py: str) -> tuple[int, int, int]:
        try:
            r = subprocess.run(
                [py, "-c", "import sys;print('%d.%d.%d'%sys.version_info[:3])"],
                capture_output=True, text=True, timeout=15,
            )
            if r.returncode == 0:
                return tuple(int(x) for x in r.stdout.strip().split(".")[:3])
        except (OSError, subprocess.SubprocessError, ValueError):
            pass
        return (0, 0, 0)

    ok: list[tuple[tuple[int, int, int], str]] = []
    for py in candidate_pythons():
        try:
            r = subprocess.run(
                [py, "-c", "import " + ", ".join(mods)],
                capture_output=True, text=True, timeout=15,
            )
            if r.returncode == 0:
                ok.append((version_of(py), py))
        except (OSError, subprocess.SubprocessError):
            continue
    if ok:
        ok.sort(key=lambda t: t[0], reverse=True)
        return ok[0][1]
    fallback = shutil.which("python") or "python"
    print(f"[warn] 未找到可 import {mods} 的解释器，回退为 {fallback}", file=sys.stderr)
    return fallback


def ps_quote(s: str) -> str:
    """PowerShell 单引号字符串转义（内部单引号翻倍）。"""
    return "'" + s.replace("'", "''") + "'"


def write_launcher(title: str, exe: str, base_args: list[str], work_dir: str,
                   log_path: str | None) -> str:
    """
    写一个 .ps1 启动器到 .cache/launchers/（已被 gitignore 忽略）。
    动作本体执行 powershell.exe -NoProfile -ExecutionPolicy Bypass -File <启动器>，
    与参考动作（awam待办UI）的 powershell.exe -File 模式同构，已验证可用。
    启动器内部用 Start-Process 让目标进程完全脱离 PowerShell/Quicker，可选重定向日志。
    启动器文件名保持纯 ASCII（避免 Quicker/cmd 环境下的路径解析问题）。
    返回 .ps1 的绝对路径。
    """
    os.makedirs(DEFAULT_LAUNCHER_DIR, exist_ok=True)
    safe = re.sub(r'[^A-Za-z0-9_.-]', "_", title)[:60] or "action"
    ps1 = os.path.join(DEFAULT_LAUNCHER_DIR, safe + ".ps1")
    arg_line = " ".join('"' + a + '"' for a in base_args)
    lines = [
        "# Generated by gen_run_action.py (quicker-connector skill) - do not edit",
        f"$exe = {ps_quote(exe)}",
        f"$argLine = {ps_quote(arg_line)}",
        f"$wd = {ps_quote(work_dir)}",
        "Start-Process -FilePath $exe -ArgumentList $argLine -WorkingDirectory $wd "
        "-WindowStyle Hidden",
    ]
    if log_path:
        root, ext = os.path.splitext(log_path)
        err_log = root + ".err" + ext
        lines[-1] = (
            "Start-Process -FilePath $exe -ArgumentList $argLine -WorkingDirectory $wd "
            f"-RedirectStandardOutput {ps_quote(log_path)} "
            f"-RedirectStandardError {ps_quote(err_log)}"
        )
    content = "\r\n".join(lines) + "\r\n"
    # UTF-8 带 BOM：PowerShell 5.1 无 BOM 时按 ANSI 解析，非 ASCII 内容会乱码
    with open(ps1, "w", encoding="utf-8-sig") as f:
        f.write(content)
    return ps1


def build_direct(exe: str, base_args: list[str]) -> tuple[str, str]:
    """非脱离模式：直接以 exe 运行 base_args。"""
    return exe, " ".join(shell_quote(a) for a in base_args)


def gen_action(
    *,
    file_name: str,
    arguments: str,
    title: str,
    description: str,
    work_dir: str,
    run_as_admin: bool,
    minimized: bool,
    activate: bool,
    row: int = 0,
    col: int = 3,
) -> dict:
    ts = now_iso()
    data_obj = {
        "FileName": file_name,
        "Arguments": arguments,
        "RunAsAdmin": run_as_admin,
        "WaitForExit": False,
        "WindowStyle": "2" if minimized else "1",
        "SetWorkingDir": False,
        "WorkingDir": work_dir,
        "AlternativePaths": "",
        "ActivateWindowIfRunning": activate,
        "ActivateWindowHotkey": "",
    }
    data_str = "json:" + json.dumps(data_obj, ensure_ascii=False, separators=(",", ":"))
    return {
        "Row": row,
        "Col": col,
        "ActionType": 11,
        "Title": title,
        "Description": description,
        "Icon": "https://files.getquicker.net/_system/run_program.png",
        "Path": None,
        "DelayMs": 0,
        "Data": data_str,
        "Data2": "",
        "Data3": "",
        "Children": None,
        "Id": str(uuid.uuid4()),
        "TemplateId": None,
        "TemplateRevision": 0,
        "UseTemplate": False,
        "LastEditTimeUtc": ts,
        "SharedActionId": None,
        "ShareTimeUtc": None,
        "CreateTimeUtc": ts,
        "AsSubProgram": False,
        "SkipWhenStopRunningActions": False,
        "SkipCheckUpdate": False,
        "AutoUpdate": False,
        "KeepInfoWhenUpdate": False,
        "MinQuickerVersion": None,
        "ContextMenuData": None,
        "AllowScrollTrigger": False,
        "EnableEvaluateVariable": True,
        "IsTextProcessor": False,
        "IsImageProcessor": False,
        "Association": None,
        "DoNotClosePanel": None,
        "UserLimitation": None,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="生成 Quicker 运行程序动作 JSON")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--script", help="要运行的脚本文件 (.py/.ps1/.bat/.cmd/.exe)")
    src.add_argument("--command", nargs="+", help="程序路径 + 参数")
    ap.add_argument("--name", help="动作标题（默认智能生成）")
    ap.add_argument("--description", help="动作说明（默认智能生成）")
    ap.add_argument("--workdir", help="工作目录（默认取脚本/程序所在目录）")
    ap.add_argument("--admin", action="store_true", help="以管理员身份运行")
    ap.add_argument("--no-minimized", action="store_true", help="不使用最小化窗口")
    ap.add_argument("--no-activate", action="store_true", help="关闭「已在运行则激活窗口」")
    ap.add_argument("--no-detach", action="store_true",
                    help="不脱离 Quicker 启动（脚本类默认经 ps1 启动器脱离，避免被跟踪导致钩子失效）")
    ap.add_argument("--log", action="store_true", help="重定向 stdout/stderr 到日志文件")
    ap.add_argument("--log-dir", default=DEFAULT_LOG_DIR, help="日志目录（默认 .cache/logs）")
    ap.add_argument("--interpreter", help=".py 使用的解释器（默认自动探测）")
    ap.add_argument("--out", help="输出 JSON 路径（默认打印到 stdout）")
    ap.add_argument("--row", type=int, default=0)
    ap.add_argument("--col", type=int, default=3)
    args = ap.parse_args()

    # 解析 (exe, base_args, work_dir, name, desc, is_script_type)
    if args.script:
        script = os.path.abspath(args.script)
        if not os.path.isfile(script):
            print(f"[error] 脚本不存在: {script}", file=sys.stderr)
            return 2
        ext = os.path.splitext(script)[1].lower()
        work_dir = args.workdir or os.path.dirname(script)
        name = smart_name(script, args.name)
        if ext == ".py":
            interp = detect_interpreter(script, args.interpreter)
            exe, base_args = interp, [script]
        elif ext == ".ps1":
            exe, base_args = "powershell.exe", ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script]
        elif ext in (".bat", ".cmd"):
            exe, base_args = "cmd.exe", ["/c", script]
        elif ext == ".exe":
            exe, base_args = script, []
        else:
            exe, base_args = script, []
        desc = args.description or f"后台启动 {os.path.basename(script)}"
        is_script = ext in SCRIPT_EXTS
    else:
        raw = args.command[0]
        if os.path.sep in raw or (os.altsep and os.altsep in raw) or os.path.isfile(raw):
            prog = os.path.abspath(raw)
            work_dir = args.workdir or os.path.dirname(prog)
            exe = prog
            name = args.name or os.path.splitext(os.path.basename(prog))[0]
            desc = args.description or f"运行 {os.path.basename(prog)}"
        else:
            prog = raw
            work_dir = args.workdir or os.getcwd()
            exe = raw
            name = args.name or raw
            desc = args.description or f"运行 {raw}"
        base_args = args.command[1:]
        if base_args:
            desc = (desc + " " + " ".join(base_args)).strip()
        is_script = False

    # 决定启动方式
    # 脚本类：默认脱离（detach）；显式 --no-detach 则直接运行
    # 非脚本（--command / .exe）：默认不脱离，除非 --log 需要重定向
    need_launcher = (is_script and not args.no_detach) or (args.log and not (is_script and args.no_detach))
    if args.log and is_script and args.no_detach:
        # 不脱离又要日志：只能用 cmd 包裹（不推荐，仅兜底）
        need_launcher = True

    if need_launcher:
        log_path = None
        if args.log:
            os.makedirs(args.log_dir, exist_ok=True)
            # 日志文件名必须纯 ASCII：cmd 双层引号（""）里含中文/空格会破坏重定向解析，
            # 故用脚本文件名（ASCII）或动作名的 ASCII 化版本，动作标题仍保留智能中文名
            if args.script:
                base = os.path.splitext(os.path.basename(args.script))[0]
            else:
                base = name
            safe = re.sub(r'[^A-Za-z0-9_.-]', "_", base)[:60] or "action"
            log_path = os.path.join(args.log_dir, safe + ".log")
        ps1 = write_launcher(name, exe, base_args, work_dir, log_path)
        file_name, arguments = (
            "powershell.exe",
            '-NoProfile -ExecutionPolicy Bypass -File "' + ps1 + '"',
        )
        if args.log:
            print(f"[info] 日志将写入: {log_path}")
            print(f"[info] stderr 日志: {os.path.splitext(log_path)[0]}.err.log")
        print(f"[info] 启动器: {ps1}（Start-Process 脱离，动作立即结束）")
    else:
        file_name, arguments = build_direct(exe, base_args)

    action = gen_action(
        file_name=file_name,
        arguments=arguments,
        title=name,
        description=desc,
        work_dir=work_dir,
        run_as_admin=args.admin,
        minimized=not args.no_minimized,
        activate=not args.no_activate,
        row=args.row,
        col=args.col,
    )

    text = json.dumps(action, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"[ok] 已生成: {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
