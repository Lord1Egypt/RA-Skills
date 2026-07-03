#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_env.py — 腾讯云短信 Skill 环境变量检测工具

功能：
  检测 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY 环境变量是否已配置。
  如果当前进程 os.environ 中没有，会自动扫描以下文件尝试加载：
    ~/.profile
    ~/.bashrc
    ~/.zshrc
    ~/.bash_profile
    ~/.env
    /etc/environment
    /etc/profile

用法：
    python3 check_env.py            # 检测环境变量是否已配置
    python3 check_env.py --verbose  # 显示详细扫描日志
"""

import json
import os
import re
import sys

# 需要检测的必需变量
_REQUIRED_VARS = ["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"]

# 扫描的候选文件列表
_ENV_FILES = [
    os.path.expanduser("~/.profile"),
    os.path.expanduser("~/.bashrc"),
    os.path.expanduser("~/.zshrc"),
    os.path.expanduser("~/.bash_profile"),
    os.path.expanduser("~/.env"),
    "/etc/environment",
    "/etc/profile",
]

# KEY=VALUE 行的正则（支持 export 和带引号的值）
_KV_RE = re.compile(
    r"""^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(['"]?)(.*?)\2\s*$"""
)


def _parse_env_file(filepath: str) -> dict:
    """解析 shell 风格的环境变量文件，返回 {key: value} 字典。"""
    result = {}
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.rstrip("\n")
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                m = _KV_RE.match(line)
                if m:
                    result[m.group(1)] = m.group(3)
    except (OSError, IOError):
        pass
    return result


def _load_from_files(verbose: bool = False) -> dict:
    """扫描候选文件，将包含目标变量的内容加载到 os.environ（不覆盖已存在的值）。"""
    target_set = set(_REQUIRED_VARS)
    newly_loaded = {}

    for filepath in _ENV_FILES:
        if not os.path.isfile(filepath):
            if verbose:
                print(f"[check_env] 跳过（不存在）: {filepath}", file=sys.stderr)
            continue

        parsed = _parse_env_file(filepath)
        if not (target_set & set(parsed.keys())):
            if verbose:
                print(f"[check_env] 跳过（无目标变量）: {filepath}", file=sys.stderr)
            continue

        if verbose:
            print(f"[check_env] 加载文件: {filepath}", file=sys.stderr)

        for key, value in parsed.items():
            if key in target_set and key not in os.environ:
                os.environ[key] = value
                newly_loaded[key] = value
                if verbose:
                    display = value[:4] + "****" if len(value) > 4 else "****"
                    print(f"[check_env]   设置 {key}={display}", file=sys.stderr)

    return newly_loaded


def check_env(verbose: bool = False) -> dict:
    """
    检测密钥环境变量是否已配置。

    流程：
      1. 先检查 os.environ 中是否已有
      2. 如缺失，扫描候选文件尝试加载
      3. 输出最终检测结果（JSON）

    返回 JSON 结构：
      {
        "configured": true/false,
        "variables": {
          "TENCENTCLOUD_SECRET_ID": {"status": "ok", "preview": "AKID****"},
          "TENCENTCLOUD_SECRET_KEY": {"status": "missing"}
        }
      }
    """
    # 尝试从文件加载
    _load_from_files(verbose=verbose)

    # 检测结果
    variables = {}
    all_ok = True

    for var in _REQUIRED_VARS:
        val = os.environ.get(var, "")
        if val:
            preview = val[:4] + "****" if len(val) > 4 else "****"
            variables[var] = {"status": "ok", "preview": preview}
        else:
            variables[var] = {"status": "missing"}
            all_ok = False

    return {"configured": all_ok, "variables": variables}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="检测腾讯云短信服务所需的环境变量是否已配置"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="显示详细扫描日志"
    )
    args = parser.parse_args()

    result = check_env(verbose=args.verbose)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["configured"] else 1)
