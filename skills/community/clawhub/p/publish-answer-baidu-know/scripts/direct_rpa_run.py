#!/usr/bin/env python3
"""直接启动 RPA 发布流程（跳过 account-manager）。

用法：
  # 手动提供回答文稿
  python direct_rpa_run.py --question-url <URL> --input-id <文稿路径> [options]

  # AI 智能生成/优化回答（无需 --input-id）
  python direct_rpa_run.py --question-url <URL> --optimize [options]

  # AI 优化已有草稿
  python direct_rpa_run.py --question-url <URL> --input-id <草稿路径> --optimize [options]

首次使用需先手动登录百度：
  python direct_rpa_run.py --login-only --profile-dir <Chrome profile>
"""
from __future__ import annotations

import asyncio
import json
import os
import sys

_scripts_dir = os.path.dirname(os.path.abspath(__file__))
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

from service.baidu_zhidao_rpa import (
    STATUS_FAILED,
    STATUS_PENDING_REVIEW,
    STATUS_SUCCESS,
    run_publish_answer_async,
)


def _default_profile_dir() -> str:
    data_root = os.getenv("JIANGCHANG_DATA_ROOT", "")
    user_id = os.getenv("JIANGCHANG_USER_ID", "_default")
    return os.path.join(
        data_root, user_id, "publish-answer-baidu-know", "chrome-profile", "baidu-zhidao-01"
    )


async def _login_only(profile_dir: str) -> None:
    """仅打开浏览器让用户手动登录百度，不执行发布。"""
    from service.browser_session import close_browser_context, start_browser_session

    pw, context, page = await start_browser_session(profile_dir, headless=False)
    print("浏览器已启动，请在 Chrome 中手动登录百度账号...")
    print("登录成功后，请回到终端按 Enter 键关闭浏览器。")
    await page.goto("https://zhidao.baidu.com", wait_until="domcontentloaded", timeout=60_000)
    input(">>> 按 Enter 关闭浏览器 <<<")
    await close_browser_context(pw, context)
    print("浏览器已关闭，登录态已保存到 profile 目录。")


async def _take_debug_screenshot(page, label: str) -> str:
    """截图保存到 skill data 目录，返回文件路径。"""
    import time as _time
    from service.browser_session import get_start_url
    data_root = os.getenv("JIANGCHANG_DATA_ROOT", "G:\\AI_worker\\jiangchang-test-data")
    user_id = os.getenv("JIANGCHANG_USER_ID", "_test_user")
    ss_dir = os.path.join(data_root, user_id, "publish-answer-baidu-know", "screenshots")
    os.makedirs(ss_dir, exist_ok=True)
    ts = _time.strftime("%Y%m%d-%H%M%S")
    filename = f"debug-{label}-{ts}.png"
    filepath = os.path.join(ss_dir, filename)
    try:
        await page.screenshot(path=filepath, full_page=True)
        print(f"[调试] 截图已保存: {filepath}")
    except Exception as exc:
        print(f"[调试] 截图失败: {exc}")
        filepath = ""
    return filepath


async def _run_publish(
    question_url: str,
    answer_path: str,
    profile_dir: str,
    idempotency_key: str,
    optimize: bool = False,
    auto_approve: bool = False,
) -> int:
    # direct_rpa_run.py 的工作：profile 准备 + LLM 环境变量
    # 实际发布逻辑全部委托给 task_service.cmd_run，自动应用 account-manager fallback

    # 设置 fallback profile 环境变量（如果指定了 profile_dir）
    if profile_dir:
        os.environ["PUBLISH_BAIDU_FALLBACK_PROFILE"] = profile_dir
        # 同时启用 fallback 开关（防止没有显式 OPENCLAW_ACCOUNT_FALLBACK 时不生效）
        os.environ.setdefault("OPENCLAW_ACCOUNT_FALLBACK", "1")

    # 在子线程中调用 cmd_run（同步函数），避免 asyncio.run 嵌套冲突
    import asyncio as _asyncio
    import concurrent.futures

    def _run_cmd() -> int:
        from service.task_service import cmd_run
        return cmd_run(
            target=None,
            input_id=answer_path or None,
            question_url=question_url,
            idempotency_key=idempotency_key or None,
            optimize=optimize,
            auto_approve=auto_approve,
        )

    # 用线程池执行同步 cmd_run，避开当前 event loop
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(_run_cmd)
        return future.result()


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="直接启动百度知道 RPA 发布（跳过 account-manager）")
    parser.add_argument("--question-url", help="百度知道问题页 URL")
    parser.add_argument("--input-id", default="", help="回答文稿本地路径（--optimize 模式下可选，作为优化草稿）")
    parser.add_argument("--profile-dir", default=None, help="Chrome profile 目录（默认自动生成）")
    parser.add_argument("--idempotency-key", default="", help="幂等键")
    parser.add_argument("--login-only", action="store_true", help="仅打开浏览器登录百度，不执行发布")
    parser.add_argument("--optimize", action="store_true", help="启用 AI 智能优化：根据问题上下文生成/优化回答，并人工审核")
    parser.add_argument("--auto-approve", action="store_true", help="--optimize 模式下自动确认通过审核（用于无人值守的端到端测试）")
    args = parser.parse_args()

    profile_dir = args.profile_dir or _default_profile_dir()
    os.makedirs(profile_dir, exist_ok=True)

    if args.login_only:
        asyncio.run(_login_only(profile_dir))
        return 0

    if not args.question_url:
        print("错误：--question-url 为必填参数", file=sys.stderr)
        return 1

    # --optimize 模式下 --input-id 可选（作为草稿）；非优化模式下 --input-id 必填
    if not args.optimize and not args.input_id:
        print("错误：非 --optimize 模式下 --input-id 为必填参数", file=sys.stderr)
        return 1

    if args.input_id and not os.path.isfile(args.input_id):
        print(f"错误：回答文稿不存在：{args.input_id}", file=sys.stderr)
        return 1

    if args.optimize:
        print("[AI 优化模式] 将根据问题上下文智能生成/优化回答，并等待人工审核。")
        if args.input_id:
            print(f"  草稿文件：{args.input_id}")
        else:
            print("  无草稿，将从头生成回答。")

    return asyncio.run(
        _run_publish(
            args.question_url,
            args.input_id or "",
            profile_dir,
            args.idempotency_key,
            optimize=args.optimize,
            auto_approve=args.auto_approve,
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
