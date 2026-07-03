#!/usr/bin/env python3
"""
Unity CI Agent — 通用 Unity 项目 CI 代理
==========================================
读取项目根目录的 ci_config.json，自动发现 Unity 安装路径，
执行 batchmode 构建/编译/测试，解析 Editor.log 返回结构化结果。

用法:
  python ci_agent.py build       # 完整 CI 构建
  python ci_agent.py compile     # 仅编译检查
  python ci_agent.py status      # 读取上次构建结果

适用: Unity 2019+ 所有版本，跨 Windows/macOS/Linux
"""

import subprocess
import sys
import re
import os
import json
import platform
from pathlib import Path
from datetime import datetime


# ============================================================
# 配置加载
# ============================================================

def load_config():
    """加载项目根目录的 ci_config.json"""
    config_path = os.path.join(os.getcwd(), "ci_config.json")
    if not os.path.exists(config_path):
        print("❌ ci_config.json not found in current directory!")
        print("   Run 'python ci_agent.py init' to create one, or create manually:")
        print("   https://github.com/example/unity-ci-kit#config")
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_unity(config):
    """查找 Unity 可执行文件路径"""
    # 1. 配置文件显式指定
    if config.get("unity_path"):
        path = config["unity_path"].replace("${version}", config.get("unity_version", ""))
        if os.path.exists(path):
            return path

    version = config.get("unity_version", "")
    system = platform.system()

    # 2. 自动搜索
    search_paths = []

    if system == "Windows":
        search_paths = [
            f"C:/Program Files/Unity/Hub/Editor/{version}/Editor/Unity.exe",
            f"C:/Program Files/Unity/{version}/Editor/Unity.exe",
            f"D:/Program Files/Unity/Hub/Editor/{version}/Editor/Unity.exe",
            f"D:/Program Files/Unity/{version}/Editor/Unity.exe",
        ]
        # 读取 Unity Hub 配置
        hub_config = os.path.expanduser("~/AppData/Roaming/UnityHub/secondaryInstallPath.json")
        if os.path.exists(hub_config):
            try:
                with open(hub_config, 'r') as f:
                    hub_data = json.load(f)
                    for k, v in hub_data.items():
                        if version in k:
                            search_paths.insert(0, os.path.join(v, "Editor", "Unity.exe"))
            except:
                pass

        # 从注册表查找
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Unity Technologies\Unity Editor " + version)
            path = winreg.QueryValueEx(key, "Location")[0]
            search_paths.insert(0, os.path.join(path, "Editor", "Unity.exe"))
        except:
            pass

    elif system == "Darwin":  # macOS
        search_paths = [
            f"/Applications/Unity/Hub/Editor/{version}/Unity.app/Contents/MacOS/Unity",
            f"/Applications/Unity/{version}/Unity.app/Contents/MacOS/Unity",
        ]
    else:  # Linux
        search_paths = [
            f"~/Unity/Hub/Editor/{version}/Editor/Unity",
            f"/opt/Unity/Editor/Unity",
        ]

    for path in search_paths:
        if os.path.exists(os.path.expanduser(path)):
            return os.path.expanduser(path)

    # 3. fallback: 试试不带版本的 Unity 命令
    for cmd in ["Unity", "unity"]:
        try:
            result = subprocess.run([cmd, "-version"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return cmd
        except:
            pass

    return None


# ============================================================
# 编译/构建执行
# ============================================================

def run_command(cmd, timeout=600):
    """运行命令，返回 (success, stdout)"""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            cwd=os.getcwd(), shell=(platform.system() == "Windows")
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    except Exception as e:
        return False, str(e)


def parse_errors(log_text):
    """解析 Unity Editor.log 中的编译错误和警告"""
    errors = []
    warnings = []
    for line in log_text.splitlines():
        m = re.match(r'.*error CS\d+.*', line)
        if m:
            errors.append(line.strip())
        m = re.match(r'.*warning CS\d+.*', line)
        if m:
            warnings.append(line.strip())

    ci_pass = "[AutoCI] RESULT: PASS" in log_text
    ci_fail = "[AutoCI] RESULT: FAIL" in log_text

    return {
        "errors": errors,
        "error_count": len(errors),
        "warnings": warnings,
        "warning_count": len(warnings),
        "ci_pass": ci_pass,
        "ci_fail": ci_fail,
        "has_critical_errors": len(errors) > 0
    }


# ============================================================
# CLI 命令
# ============================================================

def cmd_init():
    """创建 ci_config.json 模板"""
    template = {
        "unity_version": "2022.3.62f3c1",
        "unity_path": "",
        "execute_method": "StarVanguard.Editor.AutoCI.RunCI",
        "project_path": "",
        "timeout_seconds": 600
    }

    if os.path.exists("ci_config.json"):
        print("⚠️  ci_config.json already exists. Overwrite? (y/n)")
        if input().lower() != 'y':
            return 0

    with open("ci_config.json", 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    print("✅ ci_config.json created. Edit it to set your project's values.")
    return 0


def cmd_build():
    """完整 CI 构建"""
    config = load_config()
    unity = find_unity(config)

    if not unity:
        print("❌ Unity not found! Set 'unity_path' in ci_config.json")
        return 1

    log_file = os.path.join(os.getcwd(), config.get("log_file", "ci_output.log"))
    result_file = os.path.join(os.getcwd(), config.get("result_file", "ci_result.json"))

    print(f"🚀 Unity CI Build")
    print(f"   Unity: {unity}")
    print(f"   Method: {config.get('execute_method')}")
    print(f"   Project: {os.getcwd()}")
    print("")

    # 确保关闭 Unity Editor（避免冲突）
    if config.get("close_editor", True):
        pass  # batchmode 不会冲突

    execute_method = config.get("execute_method", "")
    cmd = (
        f'"{unity}" '
        f'-batchmode -quit -nographics '
        f'-projectPath "{os.getcwd()}" '
        f'-executeMethod {execute_method} '
        f'-logFile "{log_file}"'
    )

    print(f"▶ Running Unity batchmode...")
    ok, output = run_command(cmd, timeout=config.get("timeout_seconds", 600))

    # 读取日志
    log_text = ""
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            log_text = f.read()

    result = parse_errors(log_text)
    result["timestamp"] = datetime.now().isoformat()
    result["build_ok"] = ok and not result["has_critical_errors"]
    result["log_file"] = log_file

    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # 输出摘要
    print("")
    print("=" * 50)
    if result["build_ok"]:
        print("✅ BUILD PASSED")
    else:
        print(f"❌ BUILD FAILED: {result['error_count']} errors")
    print(f"   Errors:   {result['error_count']}")
    print(f"   Warnings: {result['warning_count']}")
    print(f"   CI:       {'PASS' if result['ci_pass'] else 'FAIL' if result['ci_fail'] else 'UNKNOWN'}")
    print(f"   Log:      {log_file}")

    if result["errors"]:
        print("\n--- ERRORS ---")
        for e in result["errors"][:10]:
            print(f"  {e}")
        if len(result["errors"]) > 10:
            print(f"  ... and {len(result['errors']) - 10} more")
    print("=" * 50)

    return 0 if result["build_ok"] else 1


def cmd_compile():
    """仅编译检查"""
    config = load_config()
    unity = find_unity(config)

    if not unity:
        print("❌ Unity not found! Set 'unity_path' in ci_config.json")
        return 1

    log_file = os.path.join(os.getcwd(), config.get("log_file", "ci_output.log"))

    print(f"🔍 Unity Compile Check")
    cmd = (
        f'"{unity}" '
        f'-batchmode -quit -nographics '
        f'-projectPath "{os.getcwd()}" '
        f'-logFile "{log_file}"'
    )

    ok, output = run_command(cmd, timeout=300)

    log_text = ""
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            log_text = f.read()

    result = parse_errors(log_text)

    if result["has_critical_errors"]:
        print(f"❌ {result['error_count']} compilation errors")
        for e in result["errors"][:5]:
            print(f"  {e}")
        return 1
    else:
        print(f"✅ Compilation OK ({result['warning_count']} warnings)")
        return 0


def cmd_status():
    """读取上次构建结果"""
    config = load_config()
    result_file = os.path.join(os.getcwd(), config.get("result_file", "ci_result.json"))

    if os.path.exists(result_file):
        with open(result_file, 'r') as f:
            result = json.load(f)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("No CI result found. Run 'python ci_agent.py build' first.")


def cmd_check():
    """检查环境就绪状态"""
    print("🔍 Unity CI Environment Check")
    print("")

    # Python
    print(f"✅ Python: {sys.version}")

    # ci_config.json
    config_path = os.path.join(os.getcwd(), "ci_config.json")
    if os.path.exists(config_path):
        print(f"✅ ci_config.json: found")
    else:
        print(f"❌ ci_config.json: not found — run 'python ci_agent.py init'")
        return 1

    # Unity
    try:
        config = json.load(open(config_path))
    except:
        print(f"❌ ci_config.json: invalid JSON")
        return 1

    unity = find_unity(config)
    if unity:
        print(f"✅ Unity: {unity}")
    else:
        print(f"❌ Unity: not found (version: {config.get('unity_version', 'unknown')})")
        print(f"   Set 'unity_path' in ci_config.json or install Unity {config.get('unity_version')}")
        return 1

    # Project
    if os.path.exists(os.path.join(os.getcwd(), "Assets")):
        print(f"✅ Project: {os.getcwd()}")
    else:
        print(f"❌ Project: no Assets/ directory — run from project root")
        return 1

    print(f"\n✅ All checks passed!")
    return 0


# ============================================================
# 入口
# ============================================================

USAGE = """
Unity CI Agent — 通用 Unity 项目 CI 代理

Commands:
  init      创建 ci_config.json 模板
  check     检查环境（Python/Unity/配置）
  build     完整 CI 构建（batchmode + executeMethod）
  compile   仅编译检查
  status    读取上次构建结果 JSON
"""

def main():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    cmd = sys.argv[1]
    commands = {
        "init": cmd_init,
        "check": cmd_check,
        "build": cmd_build,
        "compile": cmd_compile,
        "status": cmd_status,
    }

    if cmd in commands:
        sys.exit(commands[cmd]())
    else:
        print(f"Unknown command: {cmd}")
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
