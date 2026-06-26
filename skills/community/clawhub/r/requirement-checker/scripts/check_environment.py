#!/usr/bin/env python3
"""
环境检测工具 v1.0

检测 requirement-checker 运行环境是否满足要求
"""

import sys
import subprocess


def check_python_version():
    """检查 Python 版本"""
    print("🔍 检查 Python 版本...")

    py_version = sys.version_info
    version_str = f"{py_version.major}.{py_version.minor}.{py_version.micro}"

    print(f"   当前版本：Python {version_str}")

    if py_version < (3, 7):
        print("❌ Python 版本过低，需要 >= 3.7")
        print("💡 请升级 Python 版本")
        return False

    print("✅ Python 版本满足要求 (>= 3.7)")
    return True


def check_requests():
    """检查 requests 依赖"""
    print("\n🔍 检查 requests...")

    try:
        import requests

        version = requests.__version__
        print(f"✅ requests 已安装 (v{version})")
        return True
    except ImportError:
        print("❌ requests 未安装（必需依赖）")
        print("💡 安装命令：pip3 install requests")
        return False


def check_config():
    """检查配置文件"""
    print("\n🔍 检查配置文件...")

    from pathlib import Path

    config_path = Path(__file__).parent.parent / "config.json"

    if not config_path.exists():
        print("⚠️  配置文件不存在（首次使用会自动创建）")
        return True

    try:
        import json

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        print("✅ 配置文件存在")

        # 检查 API 配置
        if "api" in config:
            api_config = config["api"]
            if "api_key" in api_config and api_config["api_key"]:
                print("✅ API 已配置")
            else:
                print("⚠️  API 未配置（首次使用会自动引导配置）")

        return True
    except Exception as e:
        print(f"⚠️  配置文件读取失败：{e}")
        return False


def main():
    """主检测函数"""
    print("=" * 60)
    print("Requirement-Checker 环境检测")
    print("=" * 60)

    results = {
        "python_version": check_python_version(),
        "requests": check_requests(),
        "config": check_config(),
    }

    print("\n" + "=" * 60)
    print("检测结果")
    print("=" * 60)

    if results["python_version"] and results["requests"]:
        print("✅ 核心环境满足要求")

        if not results["config"]:
            print("⚠️  配置文件异常（首次使用会自动创建）")

        print("\n💡 环境正常，可以开始使用！")
        print("\n使用方式：")
        print("  在 OpenClaw 中说：'请检查需求文档'")
        return 0
    else:
        print("❌ 环境检测失败")

        if not results["python_version"]:
            print("   - Python 版本不满足要求")

        if not results["requests"]:
            print("   - requests 库未安装")

        print("\n💡 请根据上述提示修复问题后重试")
        print("\n手动安装依赖：")
        print("  pip3 install requests")
        return 1


if __name__ == "__main__":
    sys.exit(main())
