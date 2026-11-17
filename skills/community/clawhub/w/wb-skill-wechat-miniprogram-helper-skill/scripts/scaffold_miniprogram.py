#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scaffold a minimal, runnable WeChat Mini Program project.

Usage:
    python scaffold_miniprogram.py <target_dir> [--appid APPID] [--name NAME] [--force]

Creates a complete, importable project:
    <target>/
        app.js
        app.json
        app.wxss
        project.config.json
        sitemap.json
        pages/index/index.{js,json,wxml,wxss}

Safety:
    If the target directory already contains any of the files above, the script
    will NOT overwrite them silently. It prints a warning and asks for
    confirmation. Use --force to overwrite without prompting. In
    non-interactive environments it aborts instead of overwriting.
"""
import argparse
import json
import os
import sys

DEFAULT_APPID = "touristappid"  # guest mode in DevTools (no account needed)


APP_JS = """// app.js
App({
  onLaunch() {
    // 全局初始化逻辑（登录、读取本地缓存等）
  },
  globalData: {
    theme: 'light'
  }
})
"""

APP_JSON = {
    "pages": ["pages/index/index"],
    "window": {
        "navigationBarTitleText": "小程序",
        "navigationBarBackgroundColor": "#ffffff",
        "navigationBarTextStyle": "black",
        "backgroundColor": "#f5f5f5"
    },
    "style": "v2",
    "sitemapLocation": "sitemap.json"
}

APP_WXSS = """/* app.wxss 全局样式 */
page {
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
  color: #333;
}
"""

PROJECT_CONFIG = {
    "description": "微信小程序脚手架",
    "packOptions": {"ignore": [], "include": []},
    "setting": {
        "es6": True,
        "enhance": True,
        "postcss": True,
        "minified": True,
        "newFeature": True,
        "urlCheck": False
    },
    "compileType": "miniprogram",
    "libVersion": "3.0.0",
    "appid": "APPID_PLACEHOLDER",
    "projectname": "PROJECT_NAME_PLACEHOLDER",
    "condition": {}
}

SITEMAP = {
    "desc": "关于本文件的更多信息，请参考文档 https://developers.weixin.qq.com/miniprogram/dev/framework/sitemap.html",
    "rules": [{"action": "allow", "page": "*"}]
}

INDEX_JS = """// pages/index/index.js
Page({
  data: {
    title: 'Hello Mini Program'
  },
  onLoad() {
    // 页面加载时触发
  },
  onTap() {
    wx.showToast({ title: ' tapped', icon: 'none' })
  }
})
"""

INDEX_JSON = {
    "navigationBarTitleText": "首页",
    "usingComponents": {}
}

INDEX_WXML = """<!-- pages/index/index.wxml -->
<view class="container">
  <text class="title">{{title}}</text>
  <button bindtap="onTap">点击我</button>
</view>
"""

INDEX_WXSS = """/* pages/index/index.wxss */
.container {
  padding: 40rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.title {
  font-size: 40rpx;
  margin-bottom: 30rpx;
}
"""


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("  created:", path)


# All files this scaffolder will write, relative to the target directory.
RELATIVE_FILES = [
    "app.js",
    "app.json",
    "app.wxss",
    "project.config.json",
    "sitemap.json",
    "pages/index/index.js",
    "pages/index/index.json",
    "pages/index/index.wxml",
    "pages/index/index.wxss",
]


def find_conflicts(target_dir):
    """Return a list of existing files that the scaffolder would overwrite."""
    target_dir = os.path.abspath(target_dir)
    conflicts = []
    for rel in RELATIVE_FILES:
        fp = os.path.join(target_dir, rel)
        if os.path.exists(fp):
            conflicts.append(fp)
    return conflicts


def confirm_overwrite(target_dir, conflicts):
    """Ask the user before overwriting. Returns True to proceed, False to abort.

    In non-interactive environments (no TTY) we default to aborting, so the
    script never silently clobbers existing work.
    """
    print("\nWARNING: the target directory already contains files that would be overwritten:")
    for fp in conflicts:
        print("  -", fp)
    if not sys.stdin.isatty():
        print("Non-interactive mode: aborting to avoid overwriting existing files. "
              "Re-run with --force to overwrite, or choose an empty directory.", file=sys.stderr)
        return False
    try:
        ans = input("Overwrite the above files? [y/N]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.", file=sys.stderr)
        return False
    return ans in ("y", "yes")


def scaffold(target_dir, appid, name, force=False):
    target_dir = os.path.abspath(target_dir)

    # Safety: never silently overwrite an existing, non-empty project.
    conflicts = find_conflicts(target_dir)
    if conflicts and not force:
        if not confirm_overwrite(target_dir, conflicts):
            print("Aborted. No files were written.", file=sys.stderr)
            sys.exit(1)

    os.makedirs(target_dir, exist_ok=True)

    # root files
    write_file(os.path.join(target_dir, "app.js"), APP_JS)
    write_file(os.path.join(target_dir, "app.json"),
               json.dumps(APP_JSON, ensure_ascii=False, indent=2))
    write_file(os.path.join(target_dir, "app.wxss"), APP_WXSS)

    cfg = dict(PROJECT_CONFIG)
    cfg["appid"] = appid
    cfg["projectname"] = name
    write_file(os.path.join(target_dir, "project.config.json"),
               json.dumps(cfg, ensure_ascii=False, indent=2))
    write_file(os.path.join(target_dir, "sitemap.json"),
               json.dumps(SITEMAP, ensure_ascii=False, indent=2))

    # index page (four-file set)
    base = os.path.join(target_dir, "pages", "index")
    write_file(os.path.join(base, "index.js"), INDEX_JS)
    write_file(os.path.join(base, "index.json"),
               json.dumps(INDEX_JSON, ensure_ascii=False, indent=2))
    write_file(os.path.join(base, "index.wxml"), INDEX_WXML)
    write_file(os.path.join(base, "index.wxss"), INDEX_WXSS)

    print("\nDone. Open '%s' in 微信开发者工具 (WeChat DevTools) and preview." % target_dir)
    print("AppID: %s  (change in project.config.json to use your own)" % appid)


def main():
    parser = argparse.ArgumentParser(description="Scaffold a WeChat Mini Program project")
    parser.add_argument("target_dir", help="Output directory for the project")
    parser.add_argument("--appid", default=DEFAULT_APPID,
                        help="Mini Program AppID (default: touristappid / guest mode)")
    parser.add_argument("--name", default="miniprogram", help="Project name")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing files in the target directory without prompting")
    args = parser.parse_args()

    try:
        scaffold(args.target_dir, args.appid, args.name, force=args.force)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
