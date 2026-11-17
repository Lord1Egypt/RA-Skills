#!/usr/bin/env python3
"""环境自检：流水线开跑前先确认一切就绪。

只依赖标准库，因此在依赖缺失时也能正常运行。
用法：
    python scripts/check_env.py
退出码 0 = 全部就绪；1 = 存在阻塞项。
"""

from __future__ import annotations

import os
import shutil
import sys

MODULES = {
    "whisper": "openai-whisper",
    "edge_tts": "edge-tts",
    "pysrt": "pysrt",
    "pydub": "pydub",
}


def check_audioop() -> bool:
    """audioop：Python 3.13 起从标准库移除，但 pydub 依然依赖它。

    在 3.13+ 上不补这个包，import pydub 会直接 ModuleNotFoundError，
    而报错指向 pydub，很容易让人以为是 pydub 装坏了。
    """
    try:
        import audioop  # noqa: F401

        print("  OK    audioop（pydub 依赖）")
        return True
    except ModuleNotFoundError:
        print("  MISS  audioop      -> pip install audioop-lts")
        print("        Python 3.13 起标准库已移除 audioop，需单独补装。")
        return False


def check_torch() -> None:
    """torch 只做信息提示，不阻断。

    重点是区分 CPU 版与 CUDA 版：后者体积达数 GB，
    而本项目纯 CPU 推理即可，装错纯属浪费。
    """
    try:
        import torch
    except ImportError:
        return
    cuda = getattr(torch.version, "cuda", None)
    if cuda:
        print(f"  INFO  torch {torch.__version__}（含 CUDA {cuda}，体积大）")
        print("        若不需要 GPU，可换 CPU 版以节省数 GB：")
        print("        pip install torch --index-url https://download.pytorch.org/whl/cpu")
    else:
        print(f"  OK    torch {torch.__version__}（CPU 版）")


def check_modules() -> tuple[list[str], list[str]]:
    """区分「没装」和「装了但导入崩溃」。

    这一点很关键：SSL 初始化失败之类的环境问题会让已安装的包在
    import 阶段抛异常，症状与「没装」一模一样。若不加区分就会给出
    「请 pip install」的错误指引，让人白费力气反复重装。
    """
    import importlib

    missing: list[str] = []
    broken: list[str] = []
    for mod, pkg in MODULES.items():
        try:
            importlib.import_module(mod)
            print(f"  OK    {mod}")
        except ModuleNotFoundError:
            print(f"  MISS  {mod}        -> pip install {pkg}")
            missing.append(pkg)
        except Exception as exc:  # noqa: BLE001 - 任何异常都说明是环境而非缺包
            print(f"  BROKEN {mod}       已安装，但导入时崩溃：{type(exc).__name__}: {exc}")
            broken.append(mod)
    return missing, broken


def from_cwd(executable_path: str) -> bool:
    """判断可执行文件是否来自「当前目录」而非 PATH。

    Windows 上 shutil.which 会顺带搜索当前目录，所以即使 ffmpeg 没进 PATH，
    在这里也能被找到——脚本当下跑得通，但换个工作目录就会失效。
    这种「现在能用、以后会坏」的状态必须显式提示。
    """
    try:
        return os.path.dirname(os.path.abspath(executable_path)) == os.path.abspath(os.getcwd())
    except OSError:
        return False


def warn_cwd_only(name: str, path: str) -> None:
    if from_cwd(path):
        print(f"  WARN  {name} 是从当前目录找到的，并不在 PATH 中。")
        print("        换到其他目录运行时会失效。建议把它所在目录加入 PATH，")
        print("        或始终在该目录下工作（命令需写成 ./ffmpeg 或 .\\ffmpeg.exe）。")


def check_ffmpeg() -> str | None:
    path = shutil.which("ffmpeg")
    if path:
        print(f"  OK    ffmpeg       {path}")
        warn_cwd_only("ffmpeg", path)
        return None
    print("  MISS  ffmpeg       -> 需加入 PATH（pydub / whisper 都要调用它）")
    return "ffmpeg"


def check_ffprobe() -> str | None:
    """ffprobe 是必需的，不是可选。

    pydub 读取音频时长、解码 mp3 都依赖它。有些 ffmpeg 发行版或便携包
    只提供 ffmpeg.exe，此时 pydub 会在解码阶段失败，而报错看起来
    像是文件格式问题，很难联想到 ffprobe 缺失。
    """
    path = shutil.which("ffprobe")
    if path:
        print(f"  OK    ffprobe      {path}")
        warn_cwd_only("ffprobe", path)
        return None
    print("  MISS  ffprobe      -> pydub 解码 mp3 需要它")
    print("        部分 ffmpeg 包只有 ffmpeg.exe，需单独补一个 ffprobe.exe 放到 PATH。")
    return "ffprobe"


def check_sslkeylogfile() -> None:
    """Windows 上偶发的坑：SSLKEYLOGFILE 指向无法写入的路径。

    SSL 库初始化时会尝试写该文件，失败则报 PermissionError。
    症状极具迷惑性：pip list 看得到包、包也确实装好了，
    却 import 不进来，看起来就像没装一样。

    注意：不能用 os.access() 判断可写性，它在某些环境下会误报。
    必须真的打开一次文件。
    """
    value = os.environ.get("SSLKEYLOGFILE")
    if not value:
        print("  OK    SSLKEYLOGFILE 未设置")
        return

    try:
        with open(value, "a"):
            pass
        print(f"  OK    SSLKEYLOGFILE {value}（实测可写）")
        return
    except Exception as exc:  # noqa: BLE001
        reason = f"{type(exc).__name__}: {exc}"

    print(f"  WARN  SSLKEYLOGFILE={value}  实测无法写入（{reason}）")
    print("        这会导致 pip / edge_tts 在 SSL 初始化时崩溃，")
    print("        并伪装成“包没安装”。若上方出现 BROKEN 多半就是这个原因。")
    print("        修复：")
    print("          Git Bash/Linux/macOS : unset SSLKEYLOGFILE")
    print("          PowerShell           : Remove-Item Env:SSLKEYLOGFILE")
    print("          长久方案             : 从系统环境变量中删除它")


def main() -> int:
    print(f"Python  {sys.executable}")
    print(f"版本    {sys.version.split()[0]}\n")

    print("[ Python 依赖 ]")
    missing, broken = check_modules()
    audioop_ok = check_audioop()
    check_torch()

    print("\n[ 外部工具 ]")
    missing_bin = check_ffmpeg()
    missing_probe = check_ffprobe()

    print("\n[ 环境变量陷阱 ]")
    check_sslkeylogfile()

    if not audioop_ok:
        missing.append("audioop-lts")
    for item in (missing_bin, missing_probe):
        if item:
            missing.append(item)

    print()
    if missing:
        print("缺失依赖，请安装：")
        for item in missing:
            print(f"  - {item}")
    if broken:
        print("以下包已安装但导入失败，通常是环境问题而非缺包：")
        for item in broken:
            print(f"  - {item}")
        if sys.platform == "win32":
            print("  Windows 上若报错含 DLL / 动态库 / ImportError，多半缺 VC++ 运行库：")
            print("    pip install msvc-runtime")
        print("  请勿用重装来解决——先按上一节的提示排查环境变量与运行库。")
    if missing or broken:
        return 1
    print("结论：环境就绪，可以开始流水线。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
