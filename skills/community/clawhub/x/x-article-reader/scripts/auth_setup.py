#!/usr/bin/env python3
"""
auth_setup.py — X Article Reader 一次性认证设置
================================================
运行后打开浏览器登录 X 账号，认证数据保存在本技能目录内。
与其他任何技能完全隔离。

用法:
  python3 auth_setup.py          # 设置认证
  python3 auth_setup.py status   # 查看认证状态
"""

import json
import sys
import time
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data" / "browser_state"
BROWSER_PROFILE_DIR = DATA_DIR / "browser_profile"
STATE_FILE = DATA_DIR / "state.json"
META_FILE = DATA_DIR / "meta.json"


def setup():
    try:
        from patchright.sync_api import sync_playwright
    except ImportError:
        print("❌ 请先安装 patchright：")
        print("   pip install patchright")
        print("   python3 -m patchright install chromium")
        sys.exit(1)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BROWSER_PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 55)
    print("  X Article Reader — 首次认证设置")
    print("=" * 55)
    print()
    print("即将打开浏览器，请在浏览器中登录您的 X 账号。")
    print("登录完成并到达首页 (x.com/home) 后，认证将自动保存。")
    print()
    print(f"认证数据将保存至：{DATA_DIR}")
    print("（仅在本技能内使用，不与其他技能共享）")
    print()

    playwright = sync_playwright().start()
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=str(BROWSER_PROFILE_DIR),
        headless=False,
        args=["--no-sandbox"],
    )

    page = context.new_page()
    page.goto("https://x.com/login", wait_until="domcontentloaded")

    print("⏳ 等待您完成登录（最多 3 分钟）...")

    deadline = time.time() + 180
    while time.time() < deadline:
        try:
            if "/home" in page.url:
                break
        except Exception:
            pass
        time.sleep(1)
    else:
        print("⏰ 超时，请重新运行。")
        context.close()
        playwright.stop()
        sys.exit(1)

    # 保存 storage state
    state = context.storage_state()
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))

    # 保存 meta
    META_FILE.write_text(json.dumps({
        "authenticated": True,
        "authenticated_at": time.time(),
    }, indent=2))

    context.close()
    playwright.stop()

    print()
    print("✅ 认证完成！有效期约 7 天。")
    print()
    print("现在可以运行：")
    print('  python3 read_article.py "https://x.com/user/articles/xxx"')


def status():
    print("=" * 55)
    if STATE_FILE.exists() and META_FILE.exists():
        meta = json.loads(META_FILE.read_text())
        age_h = (time.time() - meta.get("authenticated_at", 0)) / 3600
        print(f"✅ 已认证（{age_h:.1f} 小时前）")
        print(f"   位置：{DATA_DIR}")
    else:
        print("❌ 未认证，请运行：python3 auth_setup.py")
    print("=" * 55)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "setup"
    if cmd == "status":
        status()
    else:
        setup()
