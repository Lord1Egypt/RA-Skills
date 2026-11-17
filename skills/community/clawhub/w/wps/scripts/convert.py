#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""convert.py — 封装 LibreOffice headless 的格式转换工具。

功能：将 .doc/.docx/.xls/.xlsx/.ppt/.pptx/.wps/.et/.dps 等格式转换为
PDF，或在 docx/xlsx/pptx 等常见格式之间互转。支持单文件、目录和 glob 批量。

用法示例：
    python scripts/convert.py 报告.docx --to pdf
    python scripts/convert.py ./docs --to pdf -o ./out
    python scripts/convert.py "*.pptx" --to pdf
    python scripts/convert.py 数据.xlsx --to xlsx -o ./out

依赖：本机需安装 LibreOffice（命令行可执行 soffice / libreoffice）。
"""

import argparse
import glob
import os
import subprocess
import sys

# 支持的源文件扩展名（小写）
SUPPORTED_EXTS = {
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".wps", ".et", ".dps", ".odt", ".ods", ".odp", ".pdf",
}

# 支持的目标格式
TARGET_FORMATS = ["pdf", "docx", "xlsx", "pptx"]

# Windows 下常见的 LibreOffice 安装路径
WINDOWS_CANDIDATES = [
    r"C:/Program Files/LibreOffice/program/soffice.exe",
    r"C:/Program Files (x86)/LibreOffice/program/soffice.exe",
]


def find_soffice():
    """按顺序探测 soffice / libreoffice，返回可执行文件完整路径；找不到返回 None。"""
    # 1) 先在 PATH 中查找
    exes = ["soffice", "libreoffice"]
    if sys.platform.startswith("win"):
        exes = ["soffice.exe", "soffice", "libreoffice.exe", "libreoffice"]
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)
    for directory in path_dirs:
        if not directory:
            continue
        for exe in exes:
            candidate = os.path.join(directory, exe)
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return candidate
    # 2) Windows 下检查常见安装路径
    if sys.platform.startswith("win"):
        for candidate in WINDOWS_CANDIDATES:
            if os.path.isfile(candidate):
                return candidate
    return None


def collect_inputs(patterns):
    """根据传入的参数收集待转换文件列表。

    支持：普通文件路径、目录（取其中受支持的文件）、glob 通配符。
    返回去重后的文件绝对路径列表。
    """
    files = []
    for item in patterns:
        if os.path.isdir(item):
            # 目录：收集其中受支持的文件（不递归）
            for name in sorted(os.listdir(item)):
                full = os.path.join(item, name)
                if os.path.isfile(full) and os.path.splitext(name)[1].lower() in SUPPORTED_EXTS:
                    files.append(full)
        elif glob.has_magic(item):
            # glob 模式
            for match in sorted(glob.glob(item)):
                if os.path.isfile(match):
                    files.append(match)
        elif os.path.isfile(item):
            files.append(item)
        else:
            print(f"[警告] 找不到文件或目录，已跳过：{item}")
    # 去重并转为绝对路径
    seen = set()
    result = []
    for f in files:
        abspath = os.path.abspath(f)
        if abspath not in seen:
            seen.add(abspath)
            result.append(abspath)
    return result


def main():
    parser = argparse.ArgumentParser(
        description="封装 LibreOffice headless，将 Office/WPS 文档批量转换为 PDF 或互转常见格式。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例：\n"
            "  python scripts/convert.py 报告.docx --to pdf\n"
            "  python scripts/convert.py ./docs --to pdf -o ./out\n"
            "  python scripts/convert.py \"*.pptx\" --to pdf\n"
            "  python scripts/convert.py 旧表.xls --to xlsx"
        ),
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="待转换的文件、目录或 glob 模式（可多个，注意 glob 模式在 Windows 下需加引号）",
    )
    parser.add_argument(
        "--to",
        required=True,
        choices=TARGET_FORMATS,
        help="目标格式：pdf / docx / xlsx / pptx",
    )
    parser.add_argument(
        "-o", "--outdir",
        default=".",
        help="输出目录（默认当前目录）",
    )
    args = parser.parse_args()

    # 探测 LibreOffice
    soffice = find_soffice()
    if soffice is None:
        print("[错误] 未在系统中找到 LibreOffice（soffice / libreoffice）。")
        print("       可前往 LibreOffice 官网（https://www.libreoffice.org/download/）下载安装；")
        print("       如果机器上已装有 WPS Office，也可以改用 WPS 图形界面手动导出 PDF。")
        sys.exit(2)

    # 收集输入文件
    files = collect_inputs(args.inputs)
    if not files:
        print("[错误] 没有可转换的文件。请检查输入路径、扩展名是否受支持。")
        print("       支持的扩展名：" + ", ".join(sorted(SUPPORTED_EXTS)))
        sys.exit(1)

    outdir = os.path.abspath(args.outdir)
    os.makedirs(outdir, exist_ok=True)

    print(f"[信息] 使用 LibreOffice：{soffice}")
    print(f"[信息] 共 {len(files)} 个文件待转换，目标格式：{args.to}，输出目录：{outdir}")

    success = 0
    failure = 0
    for f in files:
        cmd = [
            soffice,
            "--headless",
            "--convert-to", args.to,
            "--outdir", outdir,
            f,
        ]
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=300,
            )
            if result.returncode == 0:
                success += 1
                print(f"[成功] {f}")
            else:
                failure += 1
                err = result.stderr.decode("utf-8", errors="replace").strip()
                print(f"[失败] {f}")
                if err:
                    print(f"       原因：{err}")
        except subprocess.TimeoutExpired:
            failure += 1
            print(f"[失败] {f}（转换超时，超过 300 秒）")
        except OSError as exc:
            failure += 1
            print(f"[失败] {f}（无法启动 LibreOffice：{exc}）")

    print(f"[汇总] 成功 {success} 个，失败 {failure} 个。")
    sys.exit(0 if failure == 0 else 1)


if __name__ == "__main__":
    main()
