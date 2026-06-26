#!/usr/bin/env python3
"""
SnowVoice TTS Skill - Agent 初始化脚本
检测环境、自动安装、下载模型

安装流程：
1. git clone 仓库到 ~/.snowvoice-studio
2. 运行 install.sh（创建 venv + 安装依赖 + 下载 Base 模型）
3. 下载 VoiceDesign 模型
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# 配置
SNOWVOICE_REPO = "https://github.com/webkubor/snowvoice-studio.git"
DEFAULT_INSTALL_PATH = Path.home() / ".snowvoice-studio"
REQUIRED_MODELS = {
    "Base-1.7B": "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    "VoiceDesign-1.7B": "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
}


def run_cmd(cmd, **kwargs):
    """运行命令，返回 (returncode, stdout, stderr)"""
    result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    return result.returncode, result.stdout, result.stderr


def check_git():
    code, _, _ = run_cmd(["which", "git"])
    return code == 0


def check_python():
    code, out, _ = run_cmd(["python3", "--version"])
    if code == 0:
        try:
            parts = out.strip().split()[1].split(".")
            return int(parts[0]) >= 3 and int(parts[1]) >= 10
        except Exception:
            pass
    return False


def check_snowvoice_installed():
    """检查 SnowVoice 是否已安装，返回 (installed, path)"""
    # 优先检查默认路径
    for path in [DEFAULT_INSTALL_PATH, Path.home() / "Desktop" / "personal" / "tts"]:
        venv_python = path / ".venv" / "bin" / "python"
        main_py = path / "main.py"
        if venv_python.exists() and main_py.exists():
            return True, str(path)
    return False, None


def check_models(install_path):
    """检查已下载的模型"""
    models_dir = Path(install_path) / "models"
    if not models_dir.exists():
        return [], list(REQUIRED_MODELS.keys())

    installed = []
    missing = []
    for model_name in REQUIRED_MODELS:
        model_path = models_dir / model_name
        if model_path.exists() and (model_path / "model.safetensors").exists():
            installed.append(model_name)
        else:
            missing.append(model_name)
    return installed, missing


def get_env_status():
    """获取完整环境状态"""
    installed, install_path = check_snowvoice_installed()
    models_installed = []
    models_missing = list(REQUIRED_MODELS.keys())

    if installed:
        models_installed, models_missing = check_models(install_path)

    return {
        "git_installed": check_git(),
        "python_ok": check_python(),
        "snowvoice_installed": installed,
        "snowvoice_path": install_path,
        "models_installed": models_installed,
        "models_missing": models_missing,
        "ready": installed and len(models_missing) == 0,
    }


def install_snowvoice():
    """安装 SnowVoice Studio（git clone + install.sh）"""
    result = {"success": False, "message": "", "steps": []}
    install_path = DEFAULT_INSTALL_PATH

    try:
        # 1. 检查前置依赖
        if not check_git():
            result["message"] = "需要先安装 git"
            return result
        if not check_python():
            result["message"] = "需要 Python 3.10+"
            return result

        # 2. 克隆仓库
        if install_path.exists():
            result["steps"].append(f"⏭ 目录已存在: {install_path}")
        else:
            code, _, err = run_cmd(
                ["git", "clone", SNOWVOICE_REPO, str(install_path)]
            )
            if code != 0:
                result["message"] = f"克隆失败: {err}"
                return result
            result["steps"].append(f"✓ 克隆仓库完成")

        # 3. 运行 install.sh（会创建 venv、安装依赖、下载 Base 模型）
        install_script = install_path / "install.sh"
        if not install_script.exists():
            result["message"] = f"install.sh 不存在: {install_script}"
            return result

        run_cmd(["chmod", "+x", str(install_script)])

        # install.sh 会下载 Base-1.7B 模型
        code, out, err = run_cmd(
            ["bash", str(install_script)],
            cwd=str(install_path),
            timeout=600,
        )
        if code != 0:
            result["steps"].append(f"⚠ install.sh 部分失败（可能模型下载超时）: {err[:200]}")
        else:
            result["steps"].append("✓ 依赖安装完成")
            result["steps"].append("✓ Base-1.7B 模型下载完成")

        result["success"] = True
        result["message"] = "SnowVoice Studio 安装成功"

    except subprocess.TimeoutExpired:
        result["success"] = True  # 可能只是模型下载慢
        result["message"] = "安装超时，但可能部分完成，请重新运行 status 检查"
    except Exception as e:
        result["message"] = f"安装异常: {str(e)}"

    return result


def download_model(model_name, install_path=None):
    """使用 modelscope 下载指定模型"""
    if install_path is None:
        install_path = DEFAULT_INSTALL_PATH

    if model_name not in REQUIRED_MODELS:
        return {"success": False, "message": f"未知模型: {model_name}，可选: {list(REQUIRED_MODELS.keys())}"}

    model_id = REQUIRED_MODELS[model_name]
    local_dir = str(Path(install_path) / "models" / model_name)

    # 找到 venv 中的 python
    venv_python = str(Path(install_path) / ".venv" / "bin" / "python")

    result = {"success": False, "message": "", "model": model_name}

    try:
        code, out, err = run_cmd(
            [venv_python, "-m", "modelscope.cli.cli", "download",
             "--model", model_id, "--local_dir", local_dir],
            cwd=str(install_path),
            timeout=1800,  # 30 分钟超时
        )

        if code == 0:
            result["success"] = True
            result["message"] = f"模型 {model_name} 下载成功"
        else:
            result["message"] = f"下载失败: {err[:300]}"

    except subprocess.TimeoutExpired:
        result["message"] = "下载超时，请重新运行"
    except Exception as e:
        result["message"] = f"下载异常: {str(e)}"

    return result


def main():
    if len(sys.argv) < 2:
        command = "status"
    else:
        command = sys.argv[1]

    if command == "status":
        status = get_env_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))
        return 0 if status["ready"] else 1

    elif command == "install":
        result = install_snowvoice()
        for step in result["steps"]:
            print(f"  {step}")
        print(f"\n{'✅' if result['success'] else '❌'} {result['message']}")
        return 0 if result["success"] else 1

    elif command == "download-model":
        if len(sys.argv) < 3:
            print(f"用法: init.py download-model <model_name>")
            print(f"可选: {', '.join(REQUIRED_MODELS.keys())}")
            return 1
        result = download_model(sys.argv[2])
        print(f"{'✅' if result['success'] else '❌'} {result['message']}")
        return 0 if result["success"] else 1

    elif command == "setup":
        print("🔧 SnowVoice TTS 环境初始化\n")

        status = get_env_status()
        if status["ready"]:
            print("✅ 环境已就绪，无需初始化")
            return 0

        # 步骤 1: 安装 SnowVoice
        if not status["snowvoice_installed"]:
            print("📦 步骤 1: 安装 SnowVoice Studio...")
            result = install_snowvoice()
            for step in result["steps"]:
                print(f"  {step}")
            if not result["success"]:
                print(f"❌ 安装失败: {result['message']}")
                return 1
            print()

        # 重新检查路径
        _, install_path = check_snowvoice_installed()
        if not install_path:
            print("❌ 安装后仍找不到 SnowVoice")
            return 1

        # 步骤 2: 下载缺失的模型
        _, models_missing = check_models(install_path)
        for i, model_name in enumerate(models_missing):
            print(f"📥 步骤 {i+2}: 下载模型 {model_name}...")
            result = download_model(model_name, install_path)
            if result["success"]:
                print(f"  ✓ {result['message']}")
            else:
                print(f"  ❌ {result['message']}")
                return 1

        print("\n✅ 初始化完成！可以开始使用 SnowVoice TTS 了。")
        return 0

    else:
        print(f"未知命令: {command}")
        print("可用命令: status, install, download-model, setup")
        return 1


if __name__ == "__main__":
    sys.exit(main())
