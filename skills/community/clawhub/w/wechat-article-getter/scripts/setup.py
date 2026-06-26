#!/usr/bin/env python3
"""
一键安装 Playwright + Chromium 浏览器
运行一次即可: python3 setup.py
"""
import subprocess
import sys


def main():
    # 1. 安装 playwright Python 包
    print("📦 Installing playwright...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "beautifulsoup4", "-q"])

    # 2. 安装 Chromium 浏览器（~200MB）
    print("🌐 Installing Chromium browser...")
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])

    # 3. 安装系统依赖（Linux）
    print("📋 Installing system dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install-deps", "chromium"])
    except subprocess.CalledProcessError:
        print("⚠️  install-deps failed (may need sudo). Try:")
        print("   sudo npx playwright install-deps chromium")

    print("\n✅ Setup complete! You can now use fetch_article.py")


if __name__ == "__main__":
    main()
