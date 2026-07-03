# -*- coding: utf-8 -*-
"""
spss_helper.py — SPSS 无闪屏调用辅助脚本

调用优先级（从高到低）：
  1) stats.com 控制台版 -production silent -nologo（方案1：完全无闪屏，万无一失）
     ✅ 日常跑复杂语法首选，无功能限制
  2) SPSS 内置 Python StartSPSS() + Submit() + StopSPSS()（方案2：无闪屏）
     ⚠️ 只能跑纯分析语法，**不能包含**以下命令：
        - OUTPUT SAVE（保存输出文档）
        - OUTPUT EXPORT / OUTPUT DISPLAY（导出/显示输出）
        - HOST COMMAND（执行系统命令）
        - XDATA / XSAVE（涉及 OUTPUT 对象时）
     —— 遇到不确定是否涉及 OUTPUT/SAVE 的命令时，统一走方案1
  3) stats.exe -production silent -nologo（方案3：可能有闪屏，需用户确认）

⚠️ .spj 文件格式要求：
  - 必须用 SPSS 26+ 新格式：<output>/<syntax> 子元素（非 attributes）
  - 路径必须用正斜杠 / （反斜杠会导致 NullPointerException）
  - <output> 元素不可缺少，否则 NullPointerException
"""

import os
import sys
import re
import subprocess

# ============================================================
# 动态路径发现
# ============================================================

SPSS_ROOTS = [
    r"C:\Program Files\IBM\SPSS",
    r"C:\Program Files (x86)\IBM\SPSS",
    r"C:\Program Files\IBM\SPSS30",
    r"D:\Program Files\IBM\SPSS",
    r"D:\Program Files (x86)\IBM\SPSS",
    r"C:\SPSS",
    r"D:\SPSS",
    r"D:\IBM\SPSS",
    r"E:\SPSS",
    r"E:\IBM\SPSS",
]

SPSS_VERSIONS = ["26", "27", "28", "29", "30"]
DRIVES = ["C", "D", "E"]


def _generate_candidates(exe_name):
    """生成 SPSS 可执行文件候选路径"""
    cands = []
    for root in SPSS_ROOTS:
        for ver in SPSS_VERSIONS:
            cands.append(os.path.join(root, "Statistics", ver, exe_name))
    for d in DRIVES:
        for ver in SPSS_VERSIONS:
            cands.append(os.path.join(d + ":", "SPSS", "Statistics", ver, exe_name))
            cands.append(os.path.join(d + ":", "Program Files", "IBM", "SPSS", "Statistics", ver, exe_name))
            cands.append(os.path.join(d + ":", "Program Files", "IBM", "SPSS" + ver, "Statistics", ver, exe_name))
    return cands


def _log(msg_cn, msg_en):
    """双语输出"""
    print("[CN] " + msg_cn)
    print("[EN] " + msg_en)


def _validate_path(path, kind):
    """验证 SPSS 路径"""
    if not path:
        return None
    real = os.path.realpath(path)
    if kind == "stats_com":
        if not real.lower().endswith("stats.com"):
            return None
    elif kind == "stats":
        if not real.lower().endswith("stats.exe"):
            return None
    lowered = real.lower()
    if "spss" in lowered and "statistics" in lowered:
        m = re.search(r'statistics[/\\](\d+)[/\\]', lowered)
        if m and m.group(1) in SPSS_VERSIONS:
            return real
    return None


def _safe_wrapper_path(script_dir):
    """获取安全的包装脚本路径"""
    real_dir = os.path.realpath(script_dir)
    wrapper = os.path.join(real_dir, "_spss_runner.py")
    if not os.path.realpath(wrapper).startswith(real_dir):
        return None
    return wrapper


def _run_silent(cmd, env=None, timeout=300):
    """静默执行，返回 (returncode, stdout_str, stderr_str)"""
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        try:
            stdout, stderr = p.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            p.kill()
            stdout, stderr = p.communicate()
            print("执行超时 ({}秒)".format(timeout))
            return 1, "", "Timeout"
        out_str = stdout.decode("utf-8", errors="replace") if stdout else ""
        err_str = stderr.decode("utf-8", errors="replace") if stderr else ""
        return p.returncode, out_str, err_str
    except Exception as e:
        return 1, "", str(e)


# ============================================================
# 首选：stats.com 控制台版（无闪屏）
# ============================================================

def run_console(spj_file, stats_com=None):
    """首选：通过 stats.com 控制台版运行 .spj 文件（完全无闪屏）"""
    if not os.path.exists(spj_file):
        _log(".spj 文件不存在: " + spj_file, ".spj file not found: " + spj_file)
        return 1

    if stats_com is None:
        for c in _generate_candidates("stats.com"):
            if os.path.exists(c):
                stats_com = c
                break
        if stats_com is None:
            _log("找不到 stats.com（控制台版）", "stats.com (console version) not found")
            return 1

    validated = _validate_path(stats_com, "stats_com")
    if validated is None:
        _log("stats.com 路径未通过安全验证", "stats.com path failed security validation")
        return 1
    stats_com = validated

    _log("正在通过 stats.com（控制台版）运行 Production Facility（完全无闪屏）...",
         "Running via stats.com (console version) (NO SPLASH)...")
    cmd = [stats_com, "-production", "silent", "-nologo", spj_file]
    returncode, stdout, stderr = _run_silent(cmd, timeout=300)

    if stdout: print(stdout)
    if stderr: print("ERROR: " + stderr)
    _log("退出码: " + str(returncode), "Exit code: " + str(returncode))
    return returncode


# ============================================================
# 备用1：SPSS 内置 Python（无闪屏）
# ============================================================

def run_internal(sps_file, stats_python_path=None):
    """备用：通过 SPSS 内置 Python 运行语法（无闪屏）"""
    if not os.path.exists(sps_file):
        _log("语法文件不存在: " + sps_file, "Syntax file not found: " + sps_file)
        return 1

    if stats_python_path is None:
        for c in _generate_candidates("Python3/python.exe"):
            if os.path.exists(c):
                stats_python_path = c
                break
        if stats_python_path is None:
            _log("找不到 SPSS 内置 Python", "SPSS bundled Python not found")
            return 1

    validated = _validate_path(stats_python_path, "python")
    if validated is None:
        _log("Python 路径未通过安全验证", "Python path failed security validation")
        return 1
    stats_python_path = validated

    ver_match = re.search(r'statistics[/\\](\d+)[/\\]', stats_python_path.lower())
    spss_version = ver_match.group(1) if ver_match else "26"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    wrapper = _safe_wrapper_path(script_dir)
    if wrapper is None:
        _log("无法创建安全的包装脚本路径", "Cannot create safe wrapper script path")
        return 1

    helper_home = os.path.dirname(stats_python_path).replace("\\", "/")
    sps_file_forward = sps_file.replace("\\", "/")

    wrapper_code = '''# -*- coding: utf-8 -*-
import sys, os
spss_pkg = "{helper}/Lib/site-packages"
if spss_pkg not in sys.path: sys.path.insert(0, spss_pkg)
os.environ["PATH"] = "{helper}" + os.pathsep + os.environ.get("PATH", "")
import spss
spss.StartSPSS()
with open("{sps_file}", encoding="utf-8", errors="replace") as f:
    spss.Submit(f.read())
spss.StopSPSS()
'''.format(helper=helper_home, sps_file=sps_file_forward)

    with open(wrapper, "w", encoding="utf-8") as f:
        f.write(wrapper_code)

    _log("正在通过 SPSS 内置 Python 运行语法（无 GUI/闪屏）...",
         "Running syntax via SPSS bundled Python (NO GUI, NO SPLASH)...")
    run_env = os.environ.copy()
    spss_home = os.path.dirname(stats_python_path)
    run_env["PATH"] = spss_home + os.pathsep + run_env.get("PATH", "")

    returncode, stdout, stderr = _run_silent(
        [stats_python_path, wrapper], env=run_env, timeout=300)

    if stdout: print(stdout)
    if stderr: print("ERROR: " + stderr)
    return returncode


# ============================================================
# 备用2：stats.exe（可能有闪屏，需用户确认）
# ============================================================

def run_exe(spj_file, stats_exe=None):
    """最后备选：通过 stats.exe 运行 Production Facility（可能有闪屏）"""
    if not os.path.exists(spj_file):
        _log(".spj 文件不存在: " + spj_file, ".spj file not found: " + spj_file)
        return 1

    if stats_exe is None:
        for c in _generate_candidates("stats.exe"):
            if os.path.exists(c):
                stats_exe = c
                break
        if stats_exe is None:
            _log("找不到 stats.exe", "stats.exe not found")
            return 1

    validated = _validate_path(stats_exe, "stats")
    if validated is None:
        _log("stats.exe 路径未通过安全验证", "stats.exe path failed security validation")
        return 1
    stats_exe = validated

    _log("执行 Production Facility（stats.exe 方式，可能有闪屏）",
         "Running Production Facility (via stats.exe, may show splash screen)")
    _log("⚠️ 请确认是否继续", "⚠️ Please confirm to continue")
    cmd = [stats_exe, "-production", "silent", "-nologo", spj_file]
    returncode, stdout, stderr = _run_silent(cmd, timeout=300)

    if stdout: print(stdout)
    if stderr: print("ERROR: " + stderr)
    _log("退出码: " + str(returncode), "Exit code: " + str(returncode))
    return returncode


# ============================================================
# 工具函数
# ============================================================

def show_version(stats_python_path=None):
    """显示 SPSS 版本"""
    if stats_python_path is None:
        for c in _generate_candidates("Python3/python.exe"):
            if os.path.exists(c):
                stats_python_path = c
                break
        if stats_python_path is None:
            _log("找不到 SPSS 内置 Python", "SPSS bundled Python not found")
            return 1

    validated = _validate_path(stats_python_path, "python")
    if validated is None:
        _log("Python 路径未通过安全验证", "Python path failed security validation")
        return 1
    stats_python_path = validated

    run_env = os.environ.copy()
    run_env["PATH"] = os.path.dirname(stats_python_path) + os.pathsep + run_env.get("PATH", "")

    returncode, stdout, stderr = _run_silent(
        [stats_python_path, "-c",
         "import spss; print(getattr(spss,'__version__','unknown')); spss.StartSPSS(); spss.StopSPSS()"],
        env=run_env, timeout=30)
    if stdout: print(stdout.strip())
    return returncode


def check_sps(sps_file):
    """检查 .sps 文件是否存在并预览内容"""
    if not os.path.exists(sps_file):
        _log(".sps 文件不存在: " + sps_file, ".sps file not found: " + sps_file)
        return 1
    with open(sps_file, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    _log(".sps 文件: " + sps_file, ".sps file: " + sps_file)
    _log("行数: " + str(len(content.splitlines())), "Lines: " + str(len(content.splitlines())))
    for i, line in enumerate(content.splitlines()[:10], 1):
        print("  " + str(i) + ": " + line)
    return 0


def create_spj(sps_file, output_dir=None):
    """创建标准 .spj 文件（SPSS 26+ 新格式，正斜杠路径）"""
    sps_abs = os.path.abspath(sps_file).replace("\\", "/")
    base_name = os.path.splitext(os.path.basename(sps_file))[0]
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(sps_file))
    output_dir = os.path.abspath(output_dir).replace("\\", "/")
    spj_file = os.path.join(output_dir, base_name + ".spj").replace("\\", "/")
    spv_file = os.path.join(output_dir, base_name + ".spv").replace("\\", "/")

    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<job xmlns="http://www.ibm.com/software/analytics/spss/xml/production"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     print="false"
     syntaxErrorHandling="continue"
     syntaxFormat="interactive"
     unicode="true"
     xsi:schemaLocation="http://www.ibm.com/software/analytics/spss/xml/production 
     http://www.ibm.com/software/analytics/spss/xml/production/production-1.4.xsd">
  <locale charset="UTF-8" country="CN" language="zh"/>
  <output outputFormat="viewer" outputPath="{spv}"/>
  <syntax syntaxPath="{sps}"/>
</job>
'''.format(spv=spv_file, sps=sps_abs)

    with open(spj_file, "w", encoding="utf-8") as f:
        f.write(xml)
    print("已创建 .spj 文件: " + spj_file)
    return spj_file


# ============================================================
# 主程序入口
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("用法 / Usage:")
        print("  run-console <spj_file> [stats_com]     首选: stats.com")
        print("  run-internal <sps_file> [stats_python] 备用1: 内置 Python")
        print("  run-exe <spj_file> [stats_exe]         备用2: stats.exe (可能闪屏)")
        print("  create-spj <sps_file> [output_dir]     创建 .spj 文件")
        print("  check <sps_file>                       检查 .sps 文件")
        print("  version [stats_python]                 显示版本")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "run-console":
        spj_file = sys.argv[2] if len(sys.argv) > 2 else None
        stats_com = sys.argv[3] if len(sys.argv) > 3 else None
        if spj_file is None:
            _log("请提供 .spj 文件路径", "Please provide .spj file path")
            sys.exit(1)
        sys.exit(run_console(spj_file, stats_com))
    elif cmd == "run-internal":
        sps_file = sys.argv[2] if len(sys.argv) > 2 else None
        stats_python_path = sys.argv[3] if len(sys.argv) > 3 else None
        if sps_file is None:
            _log("请提供 .sps 文件路径", "Please provide .sps file path")
            sys.exit(1)
        sys.exit(run_internal(sps_file, stats_python_path))
    elif cmd == "run-exe":
        spj_file = sys.argv[2] if len(sys.argv) > 2 else None
        stats_exe = sys.argv[3] if len(sys.argv) > 3 else None
        if spj_file is None:
            _log("请提供 .spj 文件路径", "Please provide .spj file path")
            sys.exit(1)
        sys.exit(run_exe(spj_file, stats_exe))
    elif cmd == "create-spj":
        sps_file = sys.argv[2] if len(sys.argv) > 2 else None
        output_dir = sys.argv[3] if len(sys.argv) > 3 else None
        if sps_file is None:
            _log("请提供 .sps 文件路径", "Please provide .sps file path")
            sys.exit(1)
        spj = create_spj(sps_file, output_dir)
        sys.exit(0)
    elif cmd == "check":
        sps_file = sys.argv[2] if len(sys.argv) > 2 else None
        if sps_file is None:
            _log("请提供 .sps 文件路径", "Please provide .sps file path")
            sys.exit(1)
        sys.exit(check_sps(sps_file))
    elif cmd == "version":
        stats_python_path = sys.argv[2] if len(sys.argv) > 2 else None
        sys.exit(show_version(stats_python_path))
    else:
        _log("未知命令: " + cmd, "Unknown command: " + cmd)
        sys.exit(1)


if __name__ == "__main__":
    main()
