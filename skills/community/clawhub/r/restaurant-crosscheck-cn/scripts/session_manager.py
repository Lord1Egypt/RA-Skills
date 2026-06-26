#!/usr/bin/env python3
"""
浏览器会话管理器 — 基于原始 session_manager.py
核心修复: async_playwright → sync_playwright（解决 'coroutine' object has no attribute 'goto'）
"""
import json
import os
import sys
import time
import shutil
from pathlib import Path
from typing import Dict

from playwright.sync_api import sync_playwright

from config import SESSION_BASE, DIANPING_SESSION, XHS_SESSION, BROWSER_ARGS

# 会话过期时间: 7 天
SESSION_EXPIRY_SECONDS = 7 * 24 * 3600


class BrowserSessionManager:
    """管理浏览器持久化登录会话（sync 版本）"""

    def __init__(self, base_dir: str = None, session_expiry: int = None):
        self.base_dir = Path(base_dir or SESSION_BASE)
        self.base_dir.mkdir(parents=True, exist_ok=True)

        self.dianping_session_dir = Path(DIANPING_SESSION)
        self.xhs_session_dir = Path(XHS_SESSION)
        self.dianping_session_dir.mkdir(parents=True, exist_ok=True)
        self.xhs_session_dir.mkdir(parents=True, exist_ok=True)

        self.state_file = self.base_dir / "session_state.json"
        self.session_expiry = session_expiry or SESSION_EXPIRY_SECONDS

    # ── 状态持久化 ──────────────────────────────────────

    def load_state(self) -> Dict:
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"dianping": {"logged_in": False}, "xiaohongshu": {"logged_in": False}}

    def save_state(self, state: Dict):
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    # ── 会话检查 ────────────────────────────────────────

    def is_session_valid(self, platform: str) -> bool:
        """检查会话是否有效且未过期"""
        state = self.load_state()
        ps = state.get(platform, {})

        if not ps.get("logged_in", False):
            return False

        last_login = ps.get("last_login", 0)
        if isinstance(last_login, str):
            try:
                last_login = float(last_login)
            except (ValueError, TypeError):
                return False

        elapsed = time.time() - last_login
        if elapsed > self.session_expiry:
            hours = elapsed / 3600
            print(f"  ⚠️ {platform} 会话已过期（{hours:.0f}小时前登录）")
            ps["logged_in"] = False
            self.save_state(state)
            return False

        return True

    # ── 交互式登录（sync） ──────────────────────────────

    def login(self, platform: str):
        """交互式登录指定平台（弹出浏览器，手动登录后按回车）"""
        platforms = {
            "dianping": ("大众点评", "https://www.dianping.com", self.dianping_session_dir),
            "xiaohongshu": ("小红书", "https://www.xiaohongshu.com", self.xhs_session_dir),
        }

        if platform not in platforms:
            print(f"❌ 未知平台: {platform}，支持: {', '.join(platforms.keys())}")
            return False

        name, url, session_dir = platforms[platform]

        print(f"\n{'=' * 50}")
        print(f"🔐 登录{name}")
        print(f"{'=' * 50}")
        print(f"1. 浏览器会自动打开 {name}")
        print(f"2. 请手动登录（手机号或微信扫码）")
        print(f"3. 登录成功后回到终端按回车")
        print(f"{'=' * 50}\n")

        try:
            with sync_playwright() as p:
                ctx = p.chromium.launch_persistent_context(
                    str(session_dir), headless=False, args=BROWSER_ARGS,
                )
                page = ctx.pages[0] if ctx.pages else ctx.new_page()
                page.goto(url, timeout=30000)
                input(f"✅ 登录{name}后按回车保存会话...")
                ctx.close()

            # 标记已登录
            state = self.load_state()
            state[platform] = {"logged_in": True, "last_login": time.time()}
            self.save_state(state)
            print(f"💾 {name}会话已保存\n")
            return True

        except Exception as e:
            print(f"❌ 登录失败: {e}")
            return False

    def ensure_session(self, platform: str):
        """确保会话有效，过期则重新登录"""
        if not self.is_session_valid(platform):
            self.login(platform)

    # ── 重置 ────────────────────────────────────────────

    def reset(self):
        """重置所有会话"""
        for d in [self.dianping_session_dir, self.xhs_session_dir]:
            if d.exists():
                shutil.rmtree(d)
                d.mkdir(parents=True)
        if self.state_file.exists():
            self.state_file.unlink()
        print("✅ 所有会话已重置")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CLI 入口
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    manager = BrowserSessionManager()

    if "--reset" in sys.argv:
        manager.reset()
        return

    if len(sys.argv) > 1 and sys.argv[1] in ("dianping", "xiaohongshu", "all"):
        target = sys.argv[1]
        if target == "all":
            manager.login("dianping")
            manager.login("xiaohongshu")
        else:
            manager.login(target)
        return

    # 交互模式
    print("=" * 50)
    print("🚀 浏览器会话管理器")
    print("=" * 50)
    print()

    state = manager.load_state()
    dp_ok = state.get("dianping", {}).get("logged_in", False)
    xhs_ok = state.get("xiaohongshu", {}).get("logged_in", False)

    print(f"  大众点评: {'✅ 已登录' if dp_ok else '❌ 未登录'}")
    print(f"  小红书:   {'✅ 已登录' if xhs_ok else '❌ 未登录'}")
    print()

    if dp_ok and xhs_ok:
        print("✅ 所有平台已配置完成！")
        print("💡 如需重置: python3 session_manager.py --reset")
        return

    print("用法:")
    print("  python3 session_manager.py dianping      # 登录大众点评")
    print("  python3 session_manager.py xiaohongshu   # 登录小红书")
    print("  python3 session_manager.py all           # 登录全部")
    print("  python3 session_manager.py --reset       # 重置会话")


if __name__ == "__main__":
    main()
