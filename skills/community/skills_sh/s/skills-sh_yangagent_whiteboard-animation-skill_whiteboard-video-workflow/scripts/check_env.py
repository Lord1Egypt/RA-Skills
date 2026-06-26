#!/usr/bin/env python3
"""
Whiteboard Video Workflow - 环境预检脚本

一次性检查所有依赖：
  1. Python 虚拟环境 + opencv/numpy/av（调用 setup_env.py）
  2. RUNNINGHUB_API_KEY

用法：
  python3 check_env.py                # 检测并自动安装缺失依赖
  python3 check_env.py --check-only   # 仅检测，不安装

退出码：
  0 - 全部就绪（最后一行输出 JSON 结果）
  1 - 存在不可自动修复的问题
"""
import json
import subprocess
import sys
from pathlib import Path

# 各 skill 目录的相对路径（相对于本脚本所在目录）
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
SKILLS_ROOT = SKILL_DIR.parent

ANIMATION_SKILL = SKILLS_ROOT / "whiteboard-animation"
IMAGE_GEN_SKILL = SKILL_DIR  # .env 已迁入本 skill 根目录


def check_python_venv(check_only):
    """检查 Python 虚拟环境，必要时安装依赖"""
    setup_script = ANIMATION_SKILL / "scripts" / "setup_env.py"
    if not setup_script.exists():
        return {"ok": False, "error": f"setup_env.py 不存在: {setup_script}"}

    # 先检查
    result = subprocess.run(
        [sys.executable, str(setup_script), "--check"],
        capture_output=True, text=True,
    )

    python_path = None
    # 从输出中提取 PYTHON_PATH
    for line in result.stdout.strip().splitlines():
        if line.startswith("PYTHON_PATH="):
            python_path = line.split("=", 1)[1]

    if result.returncode == 0 and python_path:
        return {"ok": True, "pythonPath": python_path}

    # 检查失败，如果不是 check-only 则尝试安装
    if not check_only:
        print("[..] Python 依赖缺失，正在安装...")
        result = subprocess.run(
            [sys.executable, str(setup_script)],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            # 安装成功，再次检查
            result2 = subprocess.run(
                [sys.executable, str(setup_script), "--check"],
                capture_output=True, text=True,
            )
            for line in result2.stdout.strip().splitlines():
                if line.startswith("PYTHON_PATH="):
                    python_path = line.split("=", 1)[1]
            if python_path:
                return {"ok": True, "pythonPath": python_path}

        return {"ok": False, "error": "Python 虚拟环境安装失败，请手动运行 setup_env.py"}

    return {"ok": False, "error": "Python 虚拟环境未就绪，缺少依赖"}


def check_api_key():
    """检查 RUNNINGHUB_API_KEY"""
    env_file = SKILL_DIR / ".env"
    if not env_file.exists():
        return {"ok": False, "error": f".env 文件不存在: {env_file}，请创建并设置 RUNNINGHUB_API_KEY"}

    content = env_file.read_text(encoding="utf-8")
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("RUNNINGHUB_API_KEY="):
            value = stripped.split("=", 1)[1].strip().strip('"').strip("'")
            if value:
                return {"ok": True}
            break

    return {"ok": False, "error": f"RUNNINGHUB_API_KEY 未设置，请在 {env_file} 中设置"}


def main():
    check_only = "--check-only" in sys.argv

    results = {}
    all_ok = True

    # 1. Python 虚拟环境
    print("[检查] Python 虚拟环境...")
    results["python"] = check_python_venv(check_only)
    if not results["python"]["ok"]:
        all_ok = False

    # 2. API Key
    print("[检查] RUNNINGHUB_API_KEY...")
    results["apiKey"] = check_api_key()
    if not results["apiKey"]["ok"]:
        all_ok = False

    # 输出结果
    output = {
        "allOk": all_ok,
        "checks": results,
    }

    if all_ok:
        print(f"\n[OK] 所有环境检查通过")
        print(f"PYTHON_PATH={results['python']['pythonPath']}")
    else:
        print(f"\n[失败] 部分检查未通过：")
        for name, r in results.items():
            status = "OK" if r["ok"] else f"失败 - {r.get('error', '未知错误')}"
            print(f"  {name}: {status}")

    # 最后一行输出 JSON（供大模型解析）
    print(f"\nENV_RESULT={json.dumps(output, ensure_ascii=False)}")

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
