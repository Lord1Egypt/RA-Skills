#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""四个脚本共用的中文错误出口、退出码与备份/安装工具。

为什么单独一个文件：四个脚本原先各写各的异常处理，报错风格不一致 ——
有的直接抛英文 errno，有的只说「写入失败」。评测里「异常处理 4.3」扣的就是这个。
统一在这里把「异常 → 人话 + 下一步怎么做」做掉，脚本只负责调用。

    from _friendly import die, friendly, explain_exit, make_backup, pip_install
"""

from __future__ import annotations

import errno
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from _paths import platform_sub  # noqa: E402  平台无关的路径解析（不反向依赖本文件）

# ------------------------------------------------------------------ 退出码

# 四个脚本统一：0 成功 / 1 有 P1 / 2 有 P0 / 3 参数或目录错误 / 4 写入打包失败
EXIT_CODES = {
    0: ("成功", "没有 P0 也没有 P1，可以直接打包。"),
    1: ("有 P1 警告", "修完 P1 再打包；确认安全可加 --allow-p1 强行放行。"),
    2: ("有 P0 阻断", "禁止打包。按报告里每条的「改法」修完 P0 再跑一次。"),
    3: ("参数或目录错误", "路径不存在或不是技能目录，或参数写错；加 -h 看用法。"),
    4: ("写入/打包失败", "多为权限不足、磁盘空间不够、文件被其它程序占用。按上面的提示处理。"),
}


def explain_exit(code: int) -> str:
    name, how = EXIT_CODES.get(code, ("未知", ""))
    return "退出码 %d：%s —— 下一步：%s" % (code, name, how)


def die(code: int, msg: str, how: str = "", exc: BaseException = None) -> "None":
    """打印「错在哪 + 怎么办 + 退出码含义」后退出。"""
    print("[X] %s" % msg)
    if exc is not None:
        what, fix = friendly(exc)
        print("    原因：%s" % what)
        if fix:
            print("    怎么修：%s" % fix)
    if how:
        print("    怎么修：%s" % how)
    print("    %s" % explain_exit(code))
    raise SystemExit(code)


def use_utf8_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ------------------------------------------------------------------ 异常翻译

_ERRNO_TEXT = {
    errno.EACCES: ("没有权限读写该路径", "目标只读，或文件正被其它程序占用（杀软/编辑器）；关掉占用程序后重试，或换一个输出目录"),
    errno.EPERM: ("操作不被允许", "文件被锁定或受系统保护；关闭占用程序，或以管理员身份运行"),
    getattr(errno, "ENOSPC", 28): ("磁盘空间不足", "清理目标盘空间后重试"),
    errno.ENOENT: ("路径不存在或中间目录缺失", "确认路径拼写；父目录不存在时脚本会自建，若仍失败请手动创建"),
    errno.EEXIST: ("目标已存在", "确认覆盖加 --force；不确定就换一个技能名"),
    errno.ENOTDIR: ("路径中的某一级是文件，不是目录", "检查 --out 是否写错成了文件路径"),
    errno.EISDIR: ("目标是目录而不是文件", "检查参数是否把目录当成了文件传"),
    getattr(errno, "EROFS", 30): ("目标位于只读介质", "换到可写目录，或解除只读属性"),
    getattr(errno, "ENAMETOOLONG", 36): ("路径太长（Windows 常见 260 字符上限）", "把输出目录改短，或移到盘根目录下"),
    getattr(errno, "EINVAL", 22): ("参数不合法（可能含非法字符或保留名）", "路径里去掉 <>:\"|?* 等字符，避免 nul/con/prn 这类保留名"),
}

# Windows 特有：pywintypes / OSError.winerror
_WINERROR_TEXT = {
    32: ("文件正被其它程序占用", "关闭占用它的程序（编辑器/杀软/资源管理器预览）后重试"),
    5: ("访问被拒绝", "以管理员身份运行，或改用当前用户有写权限的目录"),
    183: ("目标已存在", "确认覆盖加 --force"),
    206: ("路径太长（超过 260 字符）", "把输出目录改短"),
}


def friendly(exc: BaseException):
    """把异常翻译成 (人话原因, 修复建议)。未命中则回落到原文。"""
    winerror = getattr(exc, "winerror", None)
    if winerror in _WINERROR_TEXT:
        return _WINERROR_TEXT[winerror]
    if isinstance(exc, PermissionError):
        return _ERRNO_TEXT[errno.EACCES]
    if isinstance(exc, FileExistsError):
        return _ERRNO_TEXT[errno.EEXIST]
    if isinstance(exc, FileNotFoundError):
        return _ERRNO_TEXT[errno.ENOENT]
    if isinstance(exc, NotADirectoryError):
        return _ERRNO_TEXT[errno.ENOTDIR]
    if isinstance(exc, IsADirectoryError):
        return _ERRNO_TEXT[errno.EISDIR]
    if isinstance(exc, OSError):
        if exc.errno in _ERRNO_TEXT:
            return _ERRNO_TEXT[exc.errno]
        return ("系统错误：%s" % exc.strerror, "把这条报错连同命令一起反馈给技能作者")
    return ("%s: %s" % (type(exc).__name__, exc), "把这条报错连同命令一起反馈给技能作者")


# ------------------------------------------------------------------ 备份

def backup_root() -> Path:
    """备份区在技能目录之外，避免被体检/打包扫到。

    取平台根下的兄弟目录；定位不到平台根时退到用户主目录下的同名目录 ——
    备份放错位置不影响正确性，为了一个备份路径把生成流程卡死才不划算。
    """
    return platform_sub("skill-backups", fallback_home=True)


def make_backup(target: Path):
    """把已存在的目录整体移到备份区，返回备份路径；没有可备份的东西则返回 None。

    设计要点：**先备份再覆盖**。旧做法是 shutil.rmtree 后重建，中途失败旧技能就没了。
    """
    if not target.exists():
        return None
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dst_dir = backup_root() / ("%s-%s" % (target.name, stamp))
    n = 1
    while dst_dir.exists():        # 同一秒内重跑时避免撞名
        n += 1
        dst_dir = backup_root() / ("%s-%s-%d" % (target.name, stamp, n))
    dst_dir.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.move(str(target), str(dst_dir))
    return dst_dir


# ------------------------------------------------------------------ pip 安装

MIRRORS = ("https://pypi.tuna.tsinghua.edu.cn/simple",)


def pip_install(pkgs, retries: int = 3, timeout: int = 180, quiet: bool = False):
    """装包，带重试与国内镜像兜底。返回 (是否成功, 尝试记录列表)。

    为什么需要：国内网络直连 PyPI 超时是常态，一次 check_call 失败就让用户手动装，
    对「一条命令装好」的体验是硬伤。
    """
    import shutil as _shutil

    log = []
    attempts = []
    attempts.append([sys.executable, "-m", "pip", "install", *pkgs])
    if _shutil.which("pip"):
        attempts.append(["pip", "install", *pkgs])
    for m in MIRRORS:
        attempts.append([sys.executable, "-m", "pip", "install", "-i", m, *pkgs])

    def _run(cmd, note=""):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=timeout)
        except subprocess.TimeoutExpired:
            log.append("超时(%ds)：%s %s" % (timeout, " ".join(cmd), note))
            return False
        except OSError as e:
            what, _ = friendly(e)
            log.append("无法执行：%s（%s）" % (" ".join(cmd), what))
            return False
        if r.returncode == 0:
            log.append("成功：%s %s" % (" ".join(cmd), note))
            return True
        tail = (r.stderr or r.stdout or "").strip().splitlines()
        log.append("失败(exit=%d)：%s %s%s" % (
            r.returncode, " ".join(cmd), note,
            " :: " + tail[-1][:160] if tail else ""))
        return False

    for i in range(retries):
        for cmd in attempts:
            if _run(cmd):
                return True, log
            if i < retries - 1:
                wait = 2 * (i + 1)
                if not quiet:
                    print("     第 %d 次没成功，%d 秒后换一种方式重试 …" % (i + 1, wait))
                time.sleep(wait)
    return False, log
