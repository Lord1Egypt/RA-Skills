#!/usr/bin/env python3
"""xz01 hook-style gate.

Purpose:
- Provide an xz01-specific pre/post gate that can be called manually, by Claude Code hooks,
  or by Hermes/Kanban workers.
- It does NOT install any hook by itself and does NOT include generic security scanning.
- It enforces xz01 boundaries: no /root/.openclaw writes, theme-only development,
  no backend/PHP/controller/config changes for template tasks, no demo_xz01 edits,
  and reminder/status gates for runtime clearing, screenshots, AI visual review, and packaging.

Usage examples:
  python3 xz01-hook-gate.py pre-dev --changed-files file1 file2
  python3 xz01-hook-gate.py post-dev --changed-files file1 file2 --runtime-cleared
  python3 xz01-hook-gate.py pre-package --theme-dir /www/wwwroot/www.900az.com/public/themes/default \
    --static-pass --http-pass --screenshot-pass --ai-pass --rule-pass
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

OPENCLAW_PREFIX = "/root/.openclaw/"
DEMO_PREFIX = "/root/.openclaw/workspace/demo_xz01"
BACKEND_MARKERS = (
    "/application/",
    "/config/",
    "/route/",
    "/thinkphp/",
    "/vendor/",
)
BACKEND_SUFFIXES = (".php",)
THEME_MARKER = "/public/themes/"


def norm(path: str) -> str:
    if not path:
        return path
    try:
        return str(Path(path).expanduser().resolve())
    except Exception:
        return path.replace("~", str(Path.home()))


def is_openclaw_write(path: str) -> bool:
    p = norm(path)
    return p == "/root/.openclaw" or p.startswith(OPENCLAW_PREFIX)


def is_demo(path: str) -> bool:
    p = norm(path)
    return p == DEMO_PREFIX or p.startswith(DEMO_PREFIX + "/")


def is_backend(path: str) -> bool:
    p = norm(path)
    return any(marker in p for marker in BACKEND_MARKERS) and p.endswith(BACKEND_SUFFIXES)


def is_theme(path: str) -> bool:
    return THEME_MARKER in norm(path)


def fail(msg: str) -> int:
    print(f"❌ xz01-hook-gate: {msg}", file=sys.stderr)
    return 2


def warn(msg: str) -> None:
    print(f"⚠️ xz01-hook-gate: {msg}", file=sys.stderr)


def ok(msg: str) -> int:
    print(f"✅ xz01-hook-gate: {msg}")
    return 0


def check_changed_files(files: list[str], allow_openclaw_readonly: bool = False) -> int:
    for f in files:
        p = norm(f)
        if is_demo(p):
            return fail(f"禁止修改 demo_xz01 示例模板: {p}")
        if is_openclaw_write(p):
            return fail(f"禁止写入 /root/.openclaw，只允许只读学习: {p}")
        if is_backend(p):
            return fail(f"xz01 模板任务禁止修改 PHP/backend/controller/model/config/route/core/vendor 文件: {p}")
        if files and not is_theme(p):
            warn(f"变更文件不在 public/themes 下，需确认是否为用户明确授权的非模板任务: {p}")
    return 0


def cmd_pre_dev(args: argparse.Namespace) -> int:
    rc = check_changed_files(args.changed_files)
    if rc:
        return rc
    return ok("pre-dev 通过：允许继续，但 dev 仍必须精准修改、简洁实现、成功标准自检。")


def cmd_post_dev(args: argparse.Namespace) -> int:
    rc = check_changed_files(args.changed_files)
    if rc:
        return rc
    if args.changed_files and not args.runtime_cleared:
        return fail("检测到开发变更后必须清空 /www/wwwroot/www.900az.com/runtime/，再进入验证。")
    return ok("post-dev 通过：变更边界与 runtime 清理状态满足进入 test 的最低条件。")


def cmd_pre_test(args: argparse.Namespace) -> int:
    if not args.runtime_cleared:
        return fail("test 前必须确认 runtime 已清空，避免 ThinkPHP 缓存掩盖问题。")
    return ok("pre-test 通过：可以执行 PC+移动端截图、HTTP/静态检查与 AI 视觉分析。")


def cmd_post_test(args: argparse.Namespace) -> int:
    missing = []
    if not args.pc_screenshot:
        missing.append("PC 截图")
    if not args.mobile_screenshot:
        missing.append("移动端截图")
    if not args.ai_pass:
        missing.append("AI 视觉分析通过/记录")
    if missing:
        return fail("test 未闭环，缺少: " + ", ".join(missing))
    return ok("post-test 通过：截图与 AI 视觉分析已完成，可进入 rule 或返工。")


def cmd_pre_package(args: argparse.Namespace) -> int:
    required = {
        "static-pass": args.static_pass,
        "http-pass": args.http_pass,
        "screenshot-pass": args.screenshot_pass,
        "ai-pass": args.ai_pass,
        "rule-pass": args.rule_pass,
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        return fail("禁止打包，缺少门禁: " + ", ".join(missing))
    if args.theme_dir:
        td = norm(args.theme_dir)
        if is_openclaw_write(td) or is_demo(td) or not is_theme(td):
            return fail(f"打包来源必须是已验证的 public/themes 主题目录，且不能在 /root/.openclaw: {td}")
    return ok("pre-package 通过：允许将彻底验证通过的模板按编号压缩到 /root/.hermes/workspace/xz01/。")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="xz01 hook-style gate")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("pre-dev")
    p.add_argument("--changed-files", nargs="*", default=[])
    p.set_defaults(func=cmd_pre_dev)

    p = sub.add_parser("post-dev")
    p.add_argument("--changed-files", nargs="*", default=[])
    p.add_argument("--runtime-cleared", action="store_true")
    p.set_defaults(func=cmd_post_dev)

    p = sub.add_parser("pre-test")
    p.add_argument("--runtime-cleared", action="store_true")
    p.set_defaults(func=cmd_pre_test)

    p = sub.add_parser("post-test")
    p.add_argument("--pc-screenshot", action="store_true")
    p.add_argument("--mobile-screenshot", action="store_true")
    p.add_argument("--ai-pass", action="store_true")
    p.set_defaults(func=cmd_post_test)

    p = sub.add_parser("pre-package")
    p.add_argument("--theme-dir", default="")
    p.add_argument("--static-pass", action="store_true")
    p.add_argument("--http-pass", action="store_true")
    p.add_argument("--screenshot-pass", action="store_true")
    p.add_argument("--ai-pass", action="store_true")
    p.add_argument("--rule-pass", action="store_true")
    p.set_defaults(func=cmd_pre_package)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
