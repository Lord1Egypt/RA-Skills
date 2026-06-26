#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAUSG 模块启动器
用于用不同的 SAUSG 模块打开模型文件

支持功能：
- 自动搜索计算机中的 SAUSG 安装目录
- 优先使用最新版本的软件
- 支持指定软件安装目录
- 支持多种模块快速打开
"""

import subprocess
import sys
import os
import re
from typing import Optional, List, Tuple

# 解决 Windows 命令行输出中文乱码问题
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 默认安装目录
DEFAULT_SAUSG_DIR = "D:\\SAUSG2026.2"

# SAUSG 模块配置
# key: 模块名称（用于匹配用户输入）
# value: (可执行文件名, 模块显示名称, 模块说明)
SAUSG_MODULES = {
    # 全模块
    "opensausg": ("OpenSAUSG.exe", "OpenSAUSG", "通用结构分析与设计软件"),
    "open": ("OpenSAUSG.exe", "OpenSAUSG", "通用结构分析与设计软件"),
    "通用": ("OpenSAUSG.exe", "OpenSAUSG", "通用结构分析与设计软件"),

    # 非线性模块
    "sausage": ("SAUSAGE.exe", "SAUSAGE", "非线性结构分析与设计"),
    "非线性": ("SAUSAGE.exe", "SAUSAGE", "非线性结构分析与设计"),

    # 钢结构模块
    "delta": ("SAUSGDelta.exe", "SAUSGDelta", "钢结构分析与设计"),
    "钢结构": ("SAUSGDelta.exe", "SAUSGDelta", "钢结构分析与设计"),

    # 加固模块
    "jg": ("SAUSGJG.exe", "SAUSGJG", "结构加固分析与设计"),
    "加固": ("SAUSGJG.exe", "SAUSGJG", "结构加固分析与设计"),

    # 隔震模块
    "pi": ("SAUSGPI.exe", "SAUSGPI", "隔震结构分析与设计"),
    "隔震": ("SAUSGPI.exe", "SAUSGPI", "隔震结构分析与设计"),

    # 减震模块
    "zeta": ("SAUSGZeta.exe", "SAUSGZeta", "减震结构分析与设计"),
    "减震": ("SAUSGZeta.exe", "SAUSGZeta", "减震结构分析与设计"),
}


def search_sausg_installer() -> Optional[str]:
    """
    自动搜索计算机中的 SAUSG 安装目录

    搜索逻辑：
    1. 搜索 D 盘根目录下的 SAUSGXXXX 文件夹
    2. 提取版本号，选择最新版本
    3. 如果找到多个版本，返回最新版本的路径

    Returns:
        Optional[str]: 找到的最新版本路径，未找到返回 None
    """
    print("正在搜索 SAUSG 安装目录...")

    # 搜索 D 盘下的 SAUSG 目录
    saug_dirs: List[Tuple[str, int]] = []  # (路径, 版本号)

    try:
        # 列出 D 盘根目录下的文件夹
        result = subprocess.run(
            'dir /ad /b D:\\SAUSG* 2>nul',
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    # 提取版本号，例如 SAUSG2026 -> 2026
                    match = re.search(r'SAUSG(\d+)', line, re.IGNORECASE)
                    if match:
                        version = int(match.group(1))
                        dir_path = os.path.join("D:\\", line.strip())
                        if os.path.isdir(dir_path):
                            saug_dirs.append((dir_path, version))

        # 如果 D 盘没找到，尝试其他盘符
        if not saug_dirs:
            for drive in ['C:', 'E:', 'F:']:
                try:
                    result = subprocess.run(
                        f'dir /ad /b {drive}\\SAUSG* 2>nul',
                        shell=True,
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='replace'
                    )
                    if result.returncode == 0:
                        for line in result.stdout.strip().split('\n'):
                            if line.strip():
                                match = re.search(r'SAUSG(\d+)', line, re.IGNORECASE)
                                if match:
                                    version = int(match.group(1))
                                    dir_path = os.path.join(drive, line.strip().replace('/', '\\'))
                                    if os.path.isdir(dir_path):
                                        saug_dirs.append((dir_path, version))
                except Exception:
                    continue

    except Exception as e:
        print(f"搜索目录时出错: {e}")

    if not saug_dirs:
        return None

    # 按版本号排序，返回最新版本
    saug_dirs.sort(key=lambda x: x[1], reverse=True)
    latest_dir = saug_dirs[0][0]

    print(f"找到 SAUSG 版本: {saug_dirs[0][1]}")

    # 验证目录中是否有 SAUSAGE.exe
    if os.path.exists(os.path.join(latest_dir, "SAUSAGE.exe")):
        return latest_dir

    return None


def find_sausg_dir(user_specified: str = None) -> str:
    """
    查找 SAUSG 安装目录

    Args:
        user_specified: 用户指定的目录，如果为 None 则自动搜索

    Returns:
        str: SAUSG 安装目录路径
    """
    # 如果用户指定了目录
    if user_specified:
        if os.path.isdir(user_specified):
            # 检查是否有任意一个 GUI 程序
            for prog in ["SAUSAGE.exe", "OpenSAUSG.exe"]:
                if os.path.exists(os.path.join(user_specified, prog)):
                    return user_specified
            print(f"警告: 指定目录 {user_specified} 中未找到 SAUSG 程序")

    # 自动搜索
    auto_dir = search_sausg_installer()
    if auto_dir:
        return auto_dir

    # 使用默认目录
    for prog in ["SAUSAGE.exe", "OpenSAUSG.exe"]:
        if os.path.exists(os.path.join(DEFAULT_SAUSG_DIR, prog)):
            return DEFAULT_SAUSG_DIR

    # 都没找到，返回默认目录
    return DEFAULT_SAUSG_DIR


def find_module(module_name: str) -> tuple:
    """查找匹配的模块"""
    module_name_lower = module_name.lower().strip()

    # 精确匹配
    if module_name_lower in SAUSG_MODULES:
        return SAUSG_MODULES[module_name_lower]

    # 模糊匹配（包含关系）
    for key, value in SAUSG_MODULES.items():
        if key in module_name_lower or module_name_lower in key:
            return value

    return None


def open_sausg_model(model_path: str, module: str = None, sausg_dir: str = None) -> dict:
    """
    用指定模块打开 SAUSG 模型

    Args:
        model_path: 模型文件路径 (.ssg)
        module: 模块名称（可选，不指定则用默认模块）
        sausg_dir: SAUSG 安装目录（可选）

    Returns:
        dict: 包含状态和消息的字典
    """
    # 转换为绝对路径
    model_path = os.path.abspath(model_path)

    # 验证模型文件
    if not os.path.exists(model_path):
        return {"status": "error", "message": f"模型文件不存在: {model_path}"}

    if not model_path.lower().endswith('.ssg'):
        return {"status": "error", "message": "模型文件必须是 .ssg 格式"}

    # 查找 SAUSG 安装目录
    SAUSG_DIR = find_sausg_dir(sausg_dir)

    # 确定使用的模块
    if module is None or module.strip() == "":
        # 默认使用 OpenSAUSG
        exe_name, display_name, description = "OpenSAUSG.exe", "OpenSAUSG", "通用结构分析与设计"
    else:
        module_info = find_module(module)
        if module_info is None:
            available = ", ".join(sorted(set([k for k in SAUSG_MODULES.keys() if len(k) > 2])))
            return {
                "status": "error",
                "message": f"未找到模块: {module}\n可用模块: {available}"
            }
        exe_name, display_name, description = module_info

    # 检查可执行文件是否存在
    exe_path = os.path.join(SAUSG_DIR, exe_name)
    if not os.path.exists(exe_path):
        return {"status": "error", "message": f"模块程序不存在: {exe_path}"}

    # 构建命令行
    cmd = f'"{exe_path}" TYPE=OPEN PATH="{model_path}"'

    print(f"正在启动 {display_name} ({description})...")
    print(f"软件目录: {SAUSG_DIR}")
    print(f"模型: {model_path}")
    print(f"命令: {cmd}")

    try:
        # 启动进程
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=SAUSG_DIR
        )

        print(f"已启动，进程ID: {process.pid}")

        return {
            "status": "success",
            "message": f"{display_name} 已启动，正在打开模型",
            "exe": exe_name,
            "display_name": display_name,
            "pid": process.pid,
            "sausg_dir": SAUSG_DIR
        }

    except Exception as e:
        return {"status": "error", "message": f"启动失败: {str(e)}"}


def list_modules():
    """列出所有可用模块"""
    print("可用 SAUSG 模块:")
    print("-" * 60)

    # 按类别分组显示
    categories = {
        "通用模块": ["opensausg", "open", "通用"],
        "非线性模块": ["sausage", "非线性"],
        "钢结构模块": ["delta", "钢结构"],
        "加固模块": ["jg", "加固"],
        "隔震模块": ["pi", "隔震"],
        "减震模块": ["zeta", "减震"],
    }

    for category, keys in categories.items():
        print(f"\n{category}:")
        for key in keys:
            if key in SAUSG_MODULES:
                exe, name, desc = SAUSG_MODULES[key]
                print(f"  {key:10} -> {name:15} ({desc})")


if __name__ == "__main__":
    # 如果没有参数，显示帮助
    if len(sys.argv) < 2:
        print("SAUSG 模块启动器")
        print("=" * 60)
        print("用法:")
        print("  python saush_open.py <模型文件> [模块名称] [软件目录]")
        print()
        print("参数:")
        print("  模型文件: .ssg 格式的模型文件路径")
        print("  模块名称: 可选，指定要使用的模块")
        print("  软件目录: 可选，指定 SAUSG 安装目录")
        print()
        print("示例:")
        print('  python saush_open.py "F:\\00AI\\AutoSSG\\Test\\Example.ssg"')
        print('  python saush_open.py "F:\\00AI\\AutoSSG\\Test\\Example.ssg" 隔震')
        print('  python saush_open.py "F:\\00AI\\AutoSSG\\Test\\Example.ssg" zeta')
        print('  python saush_open.py "F:\\00AI\\AutoSSG\\Test\\Example.ssg" 非线性 "D:\\SAUSG2026"')
        print()
        list_modules()
        sys.exit(0)

    model_path = sys.argv[1]
    module = sys.argv[2] if len(sys.argv) > 2 else None
    sausg_dir = sys.argv[3] if len(sys.argv) > 3 else None

    result = open_sausg_model(model_path, module, sausg_dir)

    print(f"\n状态: {result['status']}")
    print(f"消息: {result['message']}")

    sys.exit(0 if result["status"] == "success" else 1)
