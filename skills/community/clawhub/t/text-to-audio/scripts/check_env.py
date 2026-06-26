#!/usr/bin/env python3
"""
edge-tts 环境检测与自动初始化脚本

检查项:
1. Python 版本 >= 3.8
2. edge-tts 包是否已安装
3. 网络连接是否可用（能否访问微软 TTS 服务）

如缺失依赖，自动执行安装。
"""
import subprocess
import sys


def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"OK: Python {version.major}.{version.minor}.{version.micro}")
        return True
    print(f"ERROR: Python {version.major}.{version.minor} < 3.8, please upgrade")
    return False


def check_edge_tts():
    """检查 edge-tts 是否已安装"""
    try:
        import edge_tts
        print(f"OK: edge-tts {edge_tts.__version__}")
        return True
    except ImportError:
        print("MISSING: edge-tts not installed")
        return False


def install_edge_tts():
    """安装 edge-tts"""
    print("Installing edge-tts...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "edge-tts"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("OK: edge-tts installed successfully")
        return True
    print(f"ERROR: Failed to install edge-tts: {result.stderr[:200]}")
    return False


def check_network():
    """检查网络连接（尝试连接微软 TTS 服务）"""
    import urllib.request
    try:
        urllib.request.urlopen("https://speech.platform.bing.com", timeout=5)
        print("OK: Network connection available")
        return True
    except Exception as e:
        print(f"WARNING: Cannot reach Microsoft TTS service: {e}")
        return False


def list_voices():
    """列出可用的中文语音"""
    try:
        import edge_tts
        print("\nAvailable Chinese voices:")
        voices = asyncio.run(edge_tts.list_voices())
        zh_voices = [v for v in voices if v["Locale"].startswith("zh-CN")]
        for v in zh_voices:
            print(f"  {v['ShortName']:40s} {v['Gender']:8s} {v.get('Status', '')}")
    except Exception as e:
        print(f"WARNING: Cannot list voices: {e}")


# 用于 list_voices
import asyncio


def main():
    print("=" * 50)
    print("edge-tts Chinese TTS Environment Check")
    print("=" * 50)

    all_ok = True

    # 1. Python 版本
    if not check_python_version():
        all_ok = False

    # 2. edge-tts
    if not check_edge_tts():
        if not install_edge_tts():
            all_ok = False
        else:
            # 安装后重新检查
            if not check_edge_tts():
                all_ok = False

    # 3. 网络连接
    if not check_network():
        all_ok = False
        print("  Tip: Enable VPN/proxy and retry")

    # 4. 列出可用语音
    if all_ok:
        list_voices()

    print("\n" + "=" * 50)
    if all_ok:
        print("READY: Environment is set up correctly!")
    else:
        print("NOT READY: Please fix the issues above")
    print("=" * 50)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
