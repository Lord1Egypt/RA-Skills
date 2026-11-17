#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
retry_helper.py — workbuddy-skill-assistant 外部调用统一重试封装

把 SKILL.md 中约定的 `_with_retry` 语义固化为确定性脚本：
  - 最多重试 max_retries 次（默认 2，不含首次，共 3 次尝试）
  - 退避序列 backoff 秒（默认 "2,5"）—— 每次重试前的等待
  - 最终仍失败：退出码 2，并打印结构化失败信息；
    调用方负责"标记跳过、不整轮崩"（绝不抛异常终止整轮检查）

设计原则（对齐 P37 脚本四原则）：确定性 / 结构化输出 / 幂等 / 安全边界。
  - 不修改被包装命令的任何行为，只负责"重试 + 退避 + 失败码"。
  - 超时由被包装命令自身处理（如 skillhub 的网络超时）。

用法：
  python scripts/retry_helper.py --max-retries 2 --backoff 2,5 -- <命令> [参数...]
示例：
  python scripts/retry_helper.py --max-retries 2 --backoff 2,5 -- skillhub search "自动化"
退出码：
  0 = 命令成功（stdout/stderr 逐字透传）
  2 = 重试耗尽仍失败（调用方应 mark-and-skip，不要整轮 abort）
  3 = 本脚本自身参数错误
"""
import argparse
import subprocess
import sys
import time


def parse_backoff(s: str):
    vals = []
    for p in s.split(","):
        p = p.strip()
        if not p:
            continue
        try:
            vals.append(float(p))
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"backoff 须为逗号分隔的数字，如 2,5；收到: {s!r}")
    if not vals:
        raise argparse.ArgumentTypeError("backoff 不能为空")
    return vals


def run(cmd, max_retries, backoff):
    attempts = max_retries + 1  # 首次 + 重试次数
    last_rc = None
    for i in range(attempts):
        if i > 0:
            wait = backoff[(i - 1) % len(backoff)]
            print(f"[retry_helper] 第 {i} 次重试，退避 {wait}s ...",
                  file=sys.stderr, flush=True)
            time.sleep(wait)
        print(f"[retry_helper] 执行（第 {i + 1}/{attempts} 次）：{' '.join(cmd)}",
              file=sys.stderr, flush=True)
        last_rc = subprocess.run(cmd).returncode
        if last_rc == 0:
            return 0
    print(
        f"[retry_helper] 重试 {max_retries} 次后仍失败（最后退出码 {last_rc}），"
        f"退出码 2（调用方应 mark-and-skip）",
        file=sys.stderr, flush=True)
    return 2


def main():
    ap = argparse.ArgumentParser(
        description="外部调用统一重试封装（workbuddy-skill-assistant）")
    ap.add_argument("--max-retries", type=int, default=2,
                    help="重试次数（不含首次），默认 2")
    ap.add_argument("--backoff", type=parse_backoff, default="2,5",
                    help="退避秒序列，逗号分隔，默认 2,5")
    ap.add_argument("command", nargs=argparse.REMAINDER,
                    help="要执行的命令及其参数（-- 之后）")
    args = ap.parse_args()

    # REMAINDER 可能把 "--" 留在开头，去掉它
    cmd = args.command[1:] if args.command and args.command[0] == "--" else args.command
    if not cmd:
        print("[retry_helper] 错误：未提供要执行的命令", file=sys.stderr)
        return 3
    return run(cmd, args.max_retries, args.backoff)


if __name__ == "__main__":
    sys.exit(main())
