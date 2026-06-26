#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAUSG 自动计算脚本
用于自动运行 SAUSG 软件进行结构分析

支持功能：
- 自动搜索计算机中的 SAUSG 安装目录
- 优先使用最新版本的软件
- 支持指定软件安装目录
- 防止同时启动多个计算程序
- 支持 cmd 和 PowerShell 环境
- 自动读取并显示计算结果
"""

import subprocess
import sys
import os
import time
import re
import locale
from typing import Optional, List, Tuple
import ntpath
import posixpath

# 导入结果读取模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sausg_result import read_main_results as read_results, format_results as format_results

# 设置编码以支持 cmd 和 PowerShell
if sys.platform == 'win32':
    try:
        # 尝试设置控制台编码
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 默认安装目录
DEFAULT_SAUSG_DIR = r"D:\SAUSG2026.2"

# 计算程序列表（按优先级排序）
CALC_PROGRAMS = [
    r"FeaCalc64S.exe",   # 多线程版本（推荐）
    r"FeaCalcOMP64.exe", # OpenMP版本
    r"FeaCalc64.exe"     # 单线程版本
]

# 用于检测的计算程序名
CHECK_PROGRAMS = ["FeaCalc64.exe", "FeaCalc64S.exe", "FeaCalcOMP64.exe"]


def run_command(cmd: str) -> tuple:
    """
    运行命令，兼容 cmd 和 PowerShell

    Returns:
        tuple: (returncode, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        # 备用方案：使用系统默认编码
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True
            )
            stdout = result.stdout.decode('utf-8', errors='replace') if result.stdout else ""
            stderr = result.stderr.decode('utf-8', errors='replace') if result.stderr else ""
            return result.returncode, stdout, stderr
        except Exception:
            return -1, "", str(e)


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
        # 列出 D 盘根目录下的文件夹 (兼容 cmd 和 PowerShell)
        returncode, stdout, _ = run_command('dir /ad /b D:\\SAUSG* 2>nul')

        if returncode == 0:
            for line in stdout.strip().split('\n'):
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
                    returncode, stdout, _ = run_command(f'dir /ad /b {drive}\\SAUSG* 2>nul')
                    if returncode == 0:
                        for line in stdout.strip().split('\n'):
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
            if os.path.exists(os.path.join(user_specified, "SAUSAGE.exe")):
                return user_specified
            else:
                print(f"警告: 指定目录 {user_specified} 中未找到 SAUSAGE.exe")

    # 自动搜索
    auto_dir = search_sausg_installer()
    if auto_dir:
        return auto_dir

    # 使用默认目录
    if os.path.exists(os.path.join(DEFAULT_SAUSG_DIR, "SAUSAGE.exe")):
        return DEFAULT_SAUSG_DIR

    # 都没找到，返回默认目录（让用户知道问题）
    return DEFAULT_SAUSG_DIR


def is_calc_running() -> bool:
    """检查是否有计算程序正在运行"""
    try:
        returncode, stdout, _ = run_command(
            'tasklist /FI "IMAGENAME eq FeaCalc64.exe" /FI "IMAGENAME eq FeaCalc64S.exe" /FI "IMAGENAME eq FeaCalcOMP64.exe"'
        )
        for prog in CHECK_PROGRAMS:
            if prog in stdout:
                return True
        return False
    except Exception:
        return False


def check_calc_success(model_path: str) -> bool:
    """
    检查计算是否成功（通过 MSG 文件）

    Args:
        model_path: 模型文件路径

    Returns:
        bool: 计算是否成功
    """
    # 获取 MSG 文件路径（与模型同目录，大写文件名）
    model_dir = os.path.dirname(model_path)
    model_name = os.path.splitext(os.path.basename(model_path))[0].upper()
    msg_path = os.path.join(model_dir, f"{model_name}.MSG")

    if not os.path.exists(msg_path):
        return False

    try:
        # 尝试用 UTF-8 和 GBK 两种编码读取
        content = ""
        for encoding in ['utf-8', 'gbk', 'gb2312']:
            try:
                with open(msg_path, 'r', encoding=encoding, errors='replace') as f:
                    content = f.read()
                break
            except Exception:
                continue

        # 检查是否有计算完成的标志
        success_keywords = [
            "计算完成",
            "计算成功",
            "动力弹塑性计算完成",
            "Analysis completed"
        ]

        for keyword in success_keywords:
            if keyword in content:
                return True

        # 检查是否有失败的标志
        error_keywords = [
            "计算失败",
            "Error",
            "error",
            "失败"
        ]

        for keyword in error_keywords:
            if keyword in content:
                return False

    except Exception:
        pass

    return False


def normalize_windows_path(model_path: str) -> str:
    r"""
    将模型路径转换为Windows绝对路径格式

    处理以下格式：
    - 相对路径: Project/Example.ssg -> F:\00AI\AutoSSG\Project\Example.ssg
    - Unix风格路径: f:/00AI/AutoSSG/Project/Example.ssg -> F:\00AI\AutoSSG\Project\Example.ssg
    - Windows风格路径: F:\00AI\AutoSSG\Project\Example.ssg -> 保持不变

    Args:
        model_path: 用户传入的模型路径

    Returns:
        str: Windows绝对路径格式
    """
    # 如果已经是绝对Windows路径，直接返回
    if os.path.isabs(model_path) and (':' in model_path):
        # 确保是大写驱动器字母
        if len(model_path) >= 2 and model_path[1] == ':':
            return model_path[0].upper() + model_path[1:]
        return model_path

    # 转换Unix风格路径 (f:/ 或 f:\) 为Windows路径
    if '/' in model_path or '\\' in model_path:
        # 处理Unix风格路径
        if model_path[0].isalpha() and len(model_path) > 2 and model_path[1] == '/':
            # f:/... -> F:\...
            drive = model_path[0].upper()
            rest = model_path[2:].replace('/', '\\')
            model_path = drive + ':' + rest

    # 如果是相对路径，转换为绝对路径
    if not os.path.isabs(model_path):
        # 获取当前工作目录
        cwd = os.getcwd()
        model_path = os.path.join(cwd, model_path)

    # 规范化路径（处理..、.等）
    model_path = os.path.normpath(model_path)

    # 确保驱动器字母是大写
    if len(model_path) >= 2 and model_path[1] == ':':
        model_path = model_path[0].upper() + model_path[1:]

    return model_path


def find_calc_program(sausg_dir: str) -> str:
    """查找可用的计算程序"""
    for prog in CALC_PROGRAMS:
        prog_path = os.path.join(sausg_dir, prog)
        if os.path.exists(prog_path):
            return prog_path
    return None


def check_calc_progress(model_dir: str, model_name: str) -> dict:
    """
    检查计算进度

    进度判断依据：
    - .BCR/.BEM文件生成 → 网格划分完成
    - StaticResult文件夹 → 初始分析结果
    - .FRQ文件 → 模型基本周期
    - .MFQ文件 → 模型最大频率
    - .NSF文件 → 模型反力
    - EarthQuakeResult文件夹 → 动力结果文件夹
    - 计算报告XXXX.docx → 计算完成

    Returns:
        dict: 包含各阶段完成状态的字典
    """
    progress = {
        "mesh": False,        # 网格划分
        "static": False,      # 初始分析
        "dynamic": False,     # 动力时程分析
        "report": False       # 结果报告
    }

    # 检查网格划分完成标志：.BCR 或 .BEM 文件
    bcr_path = os.path.join(model_dir, f"{model_name}.BCR")
    bem_path = os.path.join(model_dir, f"{model_name}.BEM")
    progress["mesh"] = os.path.exists(bcr_path) or os.path.exists(bem_path)

    # 检查初始分析完成标志：StaticResult文件夹
    static_dir = os.path.join(model_dir, "StaticResult")
    if os.path.isdir(static_dir):
        # 检查FRQ文件（基本周期）
        frq_files = [f for f in os.listdir(static_dir) if f.upper().endswith('.FRQ')]
        # 检查MFQ文件（最大频率）
        mfq_files = [f for f in os.listdir(static_dir) if f.upper().endswith('.MFQ')]
        # 检查NSF文件（模型反力）
        nsf_files = [f for f in os.listdir(static_dir) if f.upper().endswith('.NSF')]

        if frq_files or mfq_files or nsf_files:
            progress["static"] = True

    # 检查动力时程分析完成标志：EarthQuakeResult文件夹
    eq_dir = os.path.join(model_dir, "EarthQuakeResult")
    if os.path.isdir(eq_dir):
        # 检查是否有工况目录
        eq_subdirs = [d for d in os.listdir(eq_dir) if os.path.isdir(os.path.join(eq_dir, d))]
        if eq_subdirs:
            progress["dynamic"] = True

    # 检查计算报告：.docx文件
    docx_files = [f for f in os.listdir(model_dir) if f.upper().endswith('.DOCX')]
    if docx_files:
        progress["report"] = True

    return progress


def get_calc_stages() -> list:
    """返回计算阶段列表"""
    return [
        {"name": "网格划分", "key": "mesh", "files": [".BCR", ".BEM"]},
        {"name": "初始分析", "key": "static", "files": ["StaticResult/", ".FRQ", ".MFQ", ".NSF"]},
        {"name": "动力时程分析", "key": "dynamic", "files": ["EarthQuakeResult/"]},
        {"name": "结果报告", "key": "report", "files": [".DOCX"]}
    ]


def format_progress(progress: dict) -> str:
    """格式化进度为可读字符串"""
    stages = get_calc_stages()
    lines = []
    for stage in stages:
        status = "完成" if progress.get(stage["key"], False) else "进行中"
        lines.append(f"  [{status}] {stage['name']}")
    return "\n".join(lines)


# 需要清理的文件扩展名和文件夹
CLEANUP_EXTENSIONS = [
    '.MSG', '.BCR', '.BLR', '.BEM', '.PAR', '.D01', '.D02', '.D03', '.D04', '.D05',
    '.EIG', '.FRQ', '.MFQ', '.MOD', '.MOF', '.NSD', '.NSF', '.DEF', '.INP', '.TXT',
    '.DAT', '.CSV', '.jpg', '.png'
]

CLEANUP_FOLDERS = [
    'StaticResult',
    'EarthQuakeResult',
    'DesignResult'
]


def cleanup_model_files(model_path: str, dry_run: bool = False) -> dict:
    """
    清理模型目录下的临时文件和结果文件

    Args:
        model_path: 模型文件路径
        dry_run: 如果为True，只显示要删除的文件但不实际删除

    Returns:
        dict: 包含清理结果的字典
    """
    model_dir = os.path.dirname(model_path)
    model_name = os.path.splitext(os.path.basename(model_path))[0].upper()

    deleted_files = []
    deleted_folders = []
    errors = []

    if not os.path.isdir(model_dir):
        return {"deleted": [], "errors": ["模型目录不存在"]}

    try:
        # 清理指定扩展名的文件
        for filename in os.listdir(model_dir):
            file_upper = filename.upper()
            # 排除模型文件本身（.ssg）
            if file_upper.endswith('.SSG'):
                continue

            # 检查是否是模型相关文件（同名文件或指定扩展名）
            is_model_file = (
                file_upper.startswith(model_name) or
                any(file_upper.endswith(ext) for ext in CLEANUP_EXTENSIONS)
            )

            if is_model_file:
                file_path = os.path.join(model_dir, filename)
                try:
                    if dry_run:
                        deleted_files.append(filename)
                    else:
                        os.remove(file_path)
                        deleted_files.append(filename)
                except Exception as e:
                    errors.append(f"删除文件失败: {filename}, 错误: {e}")

        # 清理指定文件夹
        for folder_name in CLEANUP_FOLDERS:
            folder_path = os.path.join(model_dir, folder_name)
            if os.path.isdir(folder_path):
                try:
                    if dry_run:
                        deleted_folders.append(folder_name)
                    else:
                        import shutil
                        shutil.rmtree(folder_path)
                        deleted_folders.append(folder_name)
                except Exception as e:
                    errors.append(f"删除文件夹失败: {folder_name}, 错误: {e}")

    except Exception as e:
        errors.append(f"清理过程出错: {e}")

    return {
        "deleted_files": deleted_files,
        "deleted_folders": deleted_folders,
        "errors": errors,
        "total": len(deleted_files) + len(deleted_folders)
    }


def run_sausg(model_path: str, wait: bool = True, sausg_dir: str = None, cleanup: bool = True) -> dict:
    """
    运行 SAUSG 计算

    Args:
        model_path: 模型文件路径 (.ssg)
        wait: 是否等待计算完成
        sausg_dir: SAUSG 安装目录（可选）

    Returns:
        dict: 包含状态和消息的字典
    """
    # 转换模型路径为Windows绝对路径格式
    model_path = normalize_windows_path(model_path)

    # 验证模型文件
    if not os.path.exists(model_path):
        return {"status": "error", "message": f"模型文件不存在: {model_path}"}

    if not model_path.lower().endswith('.ssg'):
        return {"status": "error", "message": "模型文件必须是 .ssg 格式"}

    # 清理模型目录下的旧文件（可选）
    if cleanup:
        print("清理模型目录下的旧文件...")
        cleanup_result = cleanup_model_files(model_path)
        if cleanup_result["total"] > 0:
            print(f"  已清理: {cleanup_result['total']} 个文件/文件夹")
            for f in cleanup_result["deleted_files"][:5]:
                print(f"    - {f}")
            if len(cleanup_result["deleted_files"]) > 5:
                print(f"    ... 还有 {len(cleanup_result['deleted_files']) - 5} 个文件")
            for folder in cleanup_result["deleted_folders"]:
                print(f"    - {folder}/ (文件夹)")
            if cleanup_result["errors"]:
                for err in cleanup_result["errors"]:
                    print(f"  警告: {err}")
        else:
            print("  无需清理的文件")

    # 检查是否有计算程序正在运行
    if is_calc_running():
        return {"status": "error", "message": "已有计算程序正在运行，请等待计算完成后再启动新任务"}

    # 查找 SAUSG 安装目录
    SAUSG_DIR = find_sausg_dir(sausg_dir)

    # 查找可用的计算程序
    calc_program = find_calc_program(SAUSG_DIR)
    if not calc_program:
        download_url = "https://product.pkpm.cn/productDetails?productId=56"
        return {
            "status": "error",
            "message": f"未找到计算程序，请下载 SAUSG 软件\n下载链接: {download_url}"
        }

    calc_name = os.path.basename(calc_program)
    print(f"使用计算程序: {calc_name}")
    print(f"软件目录: {SAUSG_DIR}")

    # 构建命令行
    # 方式1: 使用 SAUSAGE.exe + BATCH=0 参数（打开后自动计算）
    # 方式2: 直接使用 FeaCalc64.exe（静默计算）
    # 这里使用方式1，因为 BATCH=0 可以确保模型正确加载后再计算
    cmd = f'"{SAUSG_DIR}\\SAUSAGE.exe" TYPE=OPEN BATCH=0 PATH="{model_path}"'

    print(f"正在启动 SAUSG 计算...")
    print(f"模型: {model_path}")
    print(f"命令: {cmd}")

    start_time = time.time()

    try:
        # 启动进程
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=SAUSG_DIR
        )

        print(f"计算已启动，进程ID: {process.pid}")

        if wait:
            print("等待计算完成...")
            print("=" * 50)
            print("计算阶段:")
            print("  [等待] 网格划分")
            print("  [等待] 初始分析")
            print("  [等待] 动力时程分析")
            print("  [等待] 结果报告")
            print("=" * 50)

            # 轮询检查进程状态和进度
            last_check_time = time.time()
            last_progress_check = 0
            model_dir = os.path.dirname(model_path)
            model_name = os.path.splitext(os.path.basename(model_path))[0].upper()
            prev_progress = {}

            while process.poll() is None:
                time.sleep(5)

                current_time = time.time()
                elapsed = int(current_time - start_time)
                minutes = elapsed // 60
                seconds = elapsed % 60

                # 每10秒检查一次进度
                if current_time - last_progress_check >= 10:
                    progress = check_calc_progress(model_dir, model_name)

                    # 只在进度变化时输出
                    if progress != prev_progress:
                        stages = get_calc_stages()
                        print("\n计算进度:")
                        for stage in stages:
                            status = "完成" if progress.get(stage["key"], False) else "进行中"
                            symbol = "√" if progress.get(stage["key"], False) else "○"
                            print(f"  [{symbol}] {stage['name']}")
                        prev_progress = progress.copy()

                    last_progress_check = current_time

                # 每30秒报告一次运行时间
                if current_time - last_check_time >= 30:
                    print(f"\n计算进行中... 已运行 {minutes}分{seconds}秒")
                    last_check_time = current_time
                else:
                    print(".", end="", flush=True)

            elapsed_time = int(time.time() - start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60

            stdout, stderr = process.communicate()

            # 检查进程返回码和 MSG 文件
            calc_success = False
            if process.returncode == 0:
                calc_success = True
            else:
                # 即使返回码非0，也检查 MSG 文件确认计算是否成功
                # 因为 SAUSAGE 可能在显示结果时崩溃，但计算已完成
                if check_calc_success(model_path):
                    calc_success = True

            if calc_success:
                # 计算完成后读取主要结果
                model_dir = os.path.dirname(model_path)
                model_name = os.path.splitext(os.path.basename(model_path))[0].upper()
                results = read_results(model_dir, model_name)

                print("\n" + "=" * 50)
                print("计算完成！")
                print("=" * 50)
                print("主要结果:")
                result_str = format_results(results)
                print(result_str)
                print("=" * 50)

                return {
                    "status": "success",
                    "message": f"计算完成",
                    "elapsed": f"{minutes}分{seconds}秒",
                    "sausg_dir": SAUSG_DIR,
                    "results": results
                }
            else:
                stderr_text = stderr.decode('utf-8', errors='replace') if stderr else ""
                return {
                    "status": "error",
                    "message": f"计算失败，返回码: {process.returncode}",
                    "elapsed": f"{minutes}分{seconds}秒",
                    "stderr": stderr_text
                }
        else:
            return {"status": "started", "message": "计算已启动，进程ID: " + str(process.pid), "sausg_dir": SAUSG_DIR}

    except Exception as e:
        return {"status": "error", "message": f"启动失败: {str(e)}"}


if __name__ == "__main__":
    # 解析参数
    cleanup = True  # 默认开启清理
    model_path = None
    sausg_dir = None

    for arg in sys.argv[1:]:
        if arg == '--no-cleanup':
            cleanup = False
        elif arg == '--cleanup':
            cleanup = True
        elif not arg.startswith('-'):
            if model_path is None:
                model_path = arg
            elif sausg_dir is None:
                sausg_dir = arg

    if not model_path:
        print("SAUSG 自动计算脚本")
        print("=" * 50)
        print("用法: python sausg_calc.py <模型文件路径> [软件目录] [--no-cleanup]")
        print()
        print("参数:")
        print("  模型文件路径: .ssg 格式的模型文件")
        print("  软件目录: 可选，指定 SAUSG 安装目录")
        print("  --no-cleanup: 可选，不清理模型目录下的旧文件")
        print()
        print("支持环境: cmd, PowerShell")
        print()
        print("示例:")
        print('  python .claude/skills/scripts/sausg_calc.py Test/Example.ssg')
        print(r'  python .claude/skills/scripts/sausg_calc.py Test/Example.ssg "D:\SAUSG2026"')
        print('  python .claude/skills/scripts/sausg_calc.py Test/Example.ssg --no-cleanup')
        sys.exit(1)

    result = run_sausg(model_path, True, sausg_dir, cleanup)

    print(f"\n状态: {result['status']}")
    print(f"消息: {result['message']}")

    if "elapsed" in result:
        print(f"运行时间: {result['elapsed']}")

    if result["status"] == "error" and "stderr" in result:
        print(f"错误输出: {result['stderr']}")

    sys.exit(0 if result["status"] == "success" else 1)
