#!/usr/bin/env python3
# run-spss-internal.py — Run SPSS syntax via SPSS built-in Python (no GUI)
# Usage: "C:\Program Files\IBM\SPSS\Statistics\XX\Python3\python.exe" run-spss-internal.py <sps_file>
# Note: 动态扫描任意盘符下的 SPSS 安装目录 / Dynamic scan SPSS on any drive

import sys
import os
import re

# Output bilingual helper
def log(msg_cn, msg_en=None):
    if msg_en is None:
        msg_en = msg_cn
    print("[CN] " + msg_cn + "\n[EN] " + msg_en)


def _find_spss_home():
    """
    Auto-detect SPSS installation directory dynamically.
    动态检测 SPSS 安装目录：遍历所有盘符和已知模式。
    """
    # 收集所有可用驱动器盘符 / Collect available drive letters
    drives = ["C", "D", "E"]
    if sys.platform == "win32":
        try:
            import string
            import ctypes
            bitmask = ctypes.windll.kernel32.GetLogicalDrives()
            drives = [d for i, d in enumerate(string.ascii_uppercase) if bitmask & (1 << i)]
        except:
            pass  # fallback to default drives

    versions = ["26", "27", "28", "29", "30", "31"]
    patterns = [
        "{0}:\\Program Files\\IBM\\SPSS\\Statistics\\{1}",
        "{0}:\\Program Files (x86)\\IBM\\SPSS\\Statistics\\{1}",
        "{0}:\\SPSS\\Statistics\\{1}",
        "{0}:\\IBM\\SPSS\\Statistics\\{1}",
    ]

    for d in drives:
        for v in versions:
            for pat in patterns:
                dirpath = pat.format(d, v)
                if os.path.isdir(dirpath):
                    python_exe = os.path.join(dirpath, "Python3", "python.exe")
                    if os.path.isfile(python_exe):
                        return dirpath, python_exe
    return None, None


# Auto-detect SPSS home
spss_home, stats_python_path = _find_spss_home()
if spss_home is None:
    log("未检测到 SPSS Statistics 安装", "SPSS Statistics installation not detected")
    log("请确认 SPSS 已正确安装，路径包含 SPSS\\Statistics\\<版本号>", "Please verify SPSS is correctly installed with path SPSS\\Statistics\\<version>")
    sys.exit(1)

# Validate path security (pattern-based, not hardcoded)
lowered = spss_home.lower()
if not ("spss" in lowered and "statistics" in lowered):
    log("SPSS 路径不在预期的安装目录内", "SPSS path is not within the expected installation directory")
    sys.exit(1)

# Add SPSS Python package path
spss_pkg = os.path.join(spss_home, "Python3", "Lib", "site-packages")
if spss_pkg not in sys.path:
    sys.path.insert(0, spss_pkg)

# Add SPSS bin path (DLL dependencies)
os.environ["PATH"] = spss_home + ";" + os.environ.get("PATH", "")

log("SPSS 安装目录: " + spss_home, "SPSS install dir: " + spss_home)
log("内置 Python:   " + stats_python_path, "Built-in Python: " + stats_python_path)

try:
    import spss
    log("SPSS Python 模块加载成功", "SPSS Python module loaded successfully")
except Exception as e:
    log("无法加载 SPSS 模块: " + str(e), "Failed to load SPSS module: " + str(e))
    sys.exit(1)


def run_syntax(sps_file):
    """Run syntax file via spss.Submit() (no GUI)"""
    if not os.path.exists(sps_file):
        log("语法文件不存在: " + sps_file, "Syntax file not found: " + sps_file)
        return 1

    with open(sps_file, "r", encoding="utf-8", errors="replace") as f:
        syntax = f.read()

    log("正在运行语法文件: " + sps_file, "Running syntax file: " + sps_file)
    log("语法行数: " + str(len(syntax.splitlines())), "Syntax lines: " + str(len(syntax.splitlines())))

    try:
        spss.StartSPSS()
        log("SPSS 处理器已启动（无 GUI，无闪屏）", "SPSS processor started (no GUI, no splash)")

        spss.Submit(syntax)
        log("语法执行完成", "Syntax execution complete")

        spss.StopSPSS()
        log("SPSS 处理器已停止", "SPSS processor stopped")
        return 0

    except Exception as e:
        log("语法执行失败: " + str(e), "Syntax execution failed: " + str(e))
        import traceback
        traceback.print_exc()
        try:
            spss.StopSPSS()
        except:
            pass
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        log("用法: python.exe run-spss-internal.py <sps_file>", "Usage: python.exe run-spss-internal.py <sps_file>")
        sys.exit(1)

    sps_file = sys.argv[1]
    rc = run_syntax(sps_file)
    sys.exit(rc)
