#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禹锋量化 · A股选股 Skill 客户端脚本
────────────────────────────────────
调用云端 API，获取选股/分析结果并返回格式化数据。
此脚本由 OpenClaw SKILL.md 在需要时自动调用。

使用方式：
  python3 query_stocks.py --action screen --token TOKEN
  python3 query_stocks.py --action analyze --code 000001.SZ --token TOKEN
  python3 query_stocks.py --action sector --token TOKEN
  python3 query_stocks.py --action timing --code 000001.SZ --token TOKEN
"""

import argparse
import json
import os
import sys
import requests

# ── 服务端地址（用户无需修改，由 Skill 作者维护）──
API_BASE = os.environ.get("YUFENG_QUANT_API", "http://124.220.59.85:8080")
TIMEOUT = 30

def get_token(arg_token: str) -> str:
    """优先从参数获取 Token，其次从环境变量"""
    if arg_token:
        return arg_token.strip()
    t = os.environ.get("YUFENG_QUANT_TOKEN", "").strip()
    if t:
        return t
    print(json.dumps({
        "error": "未找到 Token",
        "message": "请先获取 Token：https://api.yufeng-quant.com/subscribe\n"
                   "购买后运行：export YUFENG_QUANT_TOKEN=your-token"
    }, ensure_ascii=False))
    sys.exit(1)


def call_api(endpoint: str, token: str, params: dict = None) -> dict:
    """统一 API 调用，自动处理错误"""
    headers = {
        "X-Token": token,
        "Content-Type": "application/json",
        "User-Agent": "OpenClaw-Skill/1.0"
    }
    try:
        resp = requests.get(
            f"{API_BASE}{endpoint}",
            headers=headers,
            params=params or {},
            timeout=TIMEOUT
        )
        data = resp.json()
        if resp.status_code == 401:
            return {"error": "Token 无效或已过期", "code": 401}
        if resp.status_code == 402:
            return {"error": "Token 余额不足，请充值", "code": 402,
                    "subscribe_url": "https://api.yufeng-quant.com/subscribe"}
        if resp.status_code == 429:
            return {"error": "请求过于频繁，请稍后再试", "code": 429}
        return data
    except requests.exceptions.Timeout:
        return {"error": "请求超时，服务器繁忙，请稍后重试"}
    except requests.exceptions.ConnectionError:
        return {"error": f"无法连接到服务器 {API_BASE}，请检查网络"}
    except Exception as e:
        return {"error": f"请求异常: {str(e)}"}


def action_screen(token: str) -> None:
    """今日选股 TOP5"""
    result = call_api("/api/v1/screen", token)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def action_analyze(token: str, code: str) -> None:
    """个股深度分析"""
    if not code:
        print(json.dumps({"error": "请提供股票代码，如 --code 000001.SZ"}, ensure_ascii=False))
        sys.exit(1)
    # 自动补全后缀
    if "." not in code:
        code = code + (".SH" if code.startswith("6") else ".SZ")
    result = call_api("/api/v1/analyze", token, {"code": code})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def action_sector(token: str) -> None:
    """热门板块资金流向"""
    result = call_api("/api/v1/sector", token)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def action_timing(token: str, code: str) -> None:
    """个股择时评分"""
    if not code:
        print(json.dumps({"error": "请提供股票代码，如 --code 000001.SZ"}, ensure_ascii=False))
        sys.exit(1)
    if "." not in code:
        code = code + (".SH" if code.startswith("6") else ".SZ")
    result = call_api("/api/v1/timing", token, {"code": code})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def action_status(token: str) -> None:
    """查询 Token 余额和状态"""
    result = call_api("/api/v1/token/status", token)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="禹锋量化 A股选股 API 客户端")
    parser.add_argument("--action", required=True,
                        choices=["screen", "analyze", "sector", "timing", "status"],
                        help="操作类型")
    parser.add_argument("--token", default="", help="API Token（或设置环境变量 YUFENG_QUANT_TOKEN）")
    parser.add_argument("--code", default="", help="股票代码（analyze/timing 时必填）")
    args = parser.parse_args()

    token = get_token(args.token)

    action_map = {
        "screen": lambda: action_screen(token),
        "analyze": lambda: action_analyze(token, args.code),
        "sector": lambda: action_sector(token),
        "timing": lambda: action_timing(token, args.code),
        "status": lambda: action_status(token),
    }
    action_map[args.action]()


if __name__ == "__main__":
    main()
