#!/usr/bin/env python3
"""
知乎 AI Bot API 工具 (v2.0 修复版)

支持发布想法、点赞、评论等功能。
通过知乎 OpenAPI 操作圈子内容。

修复内容 (S2a-d):
  ✓ 硬编码路径 → 自动定位脚本目录
  ✓ 429 限流重试 (指数退避)
  ✓ 状态码校验统一
  ✓ 异常处理细化
  ✓ 增加 JSON 输出模式 (供 bridge.js 调用)
"""

import sys
import os
import json
import time
import hmac
import hashlib
import base64
import argparse
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple

import requests


# ──────────────────────────────────────────
# 自动获取脚本路径（替代硬编码路径）
# ──────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))


# ──────────────────────────────────────────
# API 响应状态码检测
# ──────────────────────────────────────────

def _is_success(result: Dict) -> bool:
    """
    统一状态码校验
    知乎 OpenAPI 有时返回 status，有时返回 code
    """
    status = result.get("status", -1)
    code = result.get("code", -1)
    # 0 = 成功, 其他值 = 失败
    return status == 0 or code == 0


# ──────────────────────────────────────────
# 重试装饰器
# ──────────────────────────────────────────

def with_retry(max_retries=3, base_delay=1.0, backoff=2.0):
    """429 限流重试 + 指数退避"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.HTTPError as e:
                    last_error = e
                    if e.response is not None and e.response.status_code == 429:
                        delay = base_delay * (backoff ** (attempt - 1))
                        # 使用服务端 Retry-After 头（优先）或客户端退避
                        retry_after = e.response.headers.get("Retry-After")
                        if retry_after:
                            try:
                                delay = int(retry_after)
                            except (ValueError, TypeError):
                                pass
                        print(f"[zhihu_bot] ⚠️ 429 限流，第 {attempt}/{max_retries} 次重试，等待 {delay}s...",
                              file=sys.stderr)
                        time.sleep(delay)
                    elif 500 <= e.response.status_code < 600:
                        # 服务器错误也重试
                        delay = base_delay * (backoff ** (attempt - 1))
                        print(f"[zhihu_bot] ⚠️ HTTP {e.response.status_code}，第 {attempt}/{max_retries} 次重试...",
                              file=sys.stderr)
                        time.sleep(delay)
                    else:
                        # 4xx 其他错误不重试
                        raise
                except (requests.exceptions.ConnectionError,
                        requests.exceptions.Timeout) as e:
                    last_error = e
                    if attempt < max_retries:
                        delay = base_delay * (backoff ** (attempt - 1))
                        print(f"[zhihu_bot] ⚠️ 网络错误 ({type(e).__name__})，第 {attempt}/{max_retries} 次重试...",
                              file=sys.stderr)
                        time.sleep(delay)
                    else:
                        raise
            raise last_error
        return wrapper
    return decorator


# ──────────────────────────────────────────
# ZhihuBot 客户端
# ──────────────────────────────────────────

class ZhihuBot:
    """知乎 API 客户端"""

    BASE_URL = "https://openapi.zhihu.com"

    def __init__(self, json_mode=False):
        self.app_key = os.environ.get("ZHIHU_APP_KEY", "")
        self.app_secret = os.environ.get("ZHIHU_APP_SECRET", "")
        self.json_mode = json_mode  # True = 输出 JSON 供 bridge.js 调用

        if not self.app_key or not self.app_secret:
            msg = "请设置环境变量 ZHIHU_APP_KEY 和 ZHIHU_APP_SECRET"
            print(msg, file=sys.stderr)
            sys.exit(1)

    def _generate_signature(self, timestamp: str, log_id: str, extra_info: str = "") -> str:
        """生成 HMAC-SHA256 签名"""
        sign_string = f"app_key:{self.app_key}|ts:{timestamp}|logid:{log_id}|extra_info:{extra_info}"
        hmac_obj = hmac.new(
            self.app_secret.encode('utf-8'),
            sign_string.encode('utf-8'),
            hashlib.sha256
        )
        return base64.b64encode(hmac_obj.digest()).decode('utf-8')

    @with_retry(max_retries=3, base_delay=1.0, backoff=2.0)
    def _make_request(self, method: str, endpoint: str,
                      params: Dict = None, data: Dict = None) -> Dict:
        """发送 API 请求（自动重试 + 异常分类）"""
        timestamp = str(int(time.time()))
        log_id = f"zhihu_{timestamp}_{int(time.time() * 1000000) % 1000000}"
        signature = self._generate_signature(timestamp, log_id)

        headers = {
            "X-App-Key": self.app_key,
            "X-Timestamp": timestamp,
            "X-Log-Id": log_id,
            "X-Sign": signature,
        }

        if data:
            headers["Content-Type"] = "application/json"

        url = f"{self.BASE_URL}{endpoint}"

        # requests 会在这里抛出 ConnectionError / Timeout / HTTPError
        if method == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=headers, params=params, json=data, timeout=30)
        else:
            raise ValueError(f"不支持的 HTTP 方法: {method}")

        response.raise_for_status()  # 非 2xx 抛出 HTTPError

        try:
            result = response.json()
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON 解析失败: {e}")

        # 检查业务状态码
        if not _is_success(result):
            err_msg = result.get('msg', result.get('message', '未知错误'))
            if not self.json_mode:
                print(f"API 错误: {err_msg}")
            else:
                print(json.dumps({"status": 1, "msg": err_msg, "detail": result}))

        return result

    # ──────────────────────────────────────────
    # 高级 API
    # ──────────────────────────────────────────

    def get_ring_detail(self, ring_id: str, page_num: int = 1,
                        page_size: int = 20) -> Dict:
        return self._make_request("GET", "/openapi/ring/detail", params={
            "ring_id": ring_id,
            "page_num": page_num,
            "page_size": page_size,
        })

    def publish_pin(self, ring_id: str, title: str, content: str,
                    images: Optional[str] = None) -> Dict:
        data = {
            "ring_id": ring_id,
            "title": title,
            "content": content,
        }
        if images:
            image_urls = [u.strip() for u in images.split(',') if u.strip()]
            data["image_urls"] = image_urls
        return self._make_request("POST", "/openapi/publish/pin", data=data)

    def reaction(self, content_type: str, content_token: str,
                 action: str) -> Dict:
        action_value = 1 if action == "like" else 0
        return self._make_request("POST", "/openapi/reaction", data={
            "content_token": content_token,
            "content_type": content_type,
            "action_type": "like",
            "action_value": action_value,
        })

    def create_comment(self, content_type: str, content_token: str,
                       content: str) -> Dict:
        return self._make_request("POST", "/openapi/comment/create", data={
            "content_token": content_token,
            "content_type": content_type,
            "content": content,
        })

    def delete_comment(self, comment_id: str) -> Dict:
        return self._make_request("POST", "/openapi/comment/delete", data={
            "comment_id": comment_id,
        })

    def list_comments(self, content_type: str, content_token: str,
                      page_num: int = 1, page_size: int = 10) -> Dict:
        return self._make_request("GET", "/openapi/comment/list", params={
            "content_token": content_token,
            "content_type": content_type,
            "page_num": page_num,
            "page_size": page_size,
        })


# ──────────────────────────────────────────
# CLI 命令处理
# ──────────────────────────────────────────

def _print_success(msg: str):
    print(f"✓ {msg}")

def _print_failure(msg: str):
    print(f"✗ {msg}")


def cmd_ring_detail(args):
    """获取圈子详情"""
    bot = ZhihuBot(json_mode=args.json)
    result = bot.get_ring_detail(args.ring_id, args.page_num or 1, args.page_size or 20)

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
        return

    print(f"\n=== 获取圈子详情 ===")
    print(f"圈子 ID: {args.ring_id}")

    if _is_success(result):
        data = result.get("data", {})
        ring_info = data.get("ring_info", {})
        print(f"  名称: {ring_info.get('ring_name', 'N/A')}")
        print(f"  描述: {ring_info.get('ring_desc', 'N/A')}")
        print(f"  成员: {ring_info.get('membership_num', 0)}")
        print(f"  讨论: {ring_info.get('discussion_num', 0)}")

        contents = data.get("contents", [])
        print(f"  内容: {len(contents)} 条")
        for i, c in enumerate(contents, 1):
            print(f"  [{i}] {c.get('author_name', 'N/A')}: "
                  f"{c.get('content', '')[:80]}...")
    else:
        _print_failure(result.get('msg', '获取失败'))

    return result


def cmd_pin_publish(args):
    """发布想法"""
    bot = ZhihuBot(json_mode=args.json)
    result = bot.publish_pin(args.ring_id, args.title, args.content, args.images)

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
        return

    if _is_success(result):
        data = result.get("data", {})
        ct = data.get("content_token", "")
        _print_success(f"发布成功！ID: {ct}")
        print(f"  链接: https://www.zhihu.com/pin/{ct}")
    else:
        _print_failure(result.get('msg', '发布失败'))

    return result


def cmd_reaction(args):
    """点赞/取消点赞"""
    bot = ZhihuBot(json_mode=args.json)
    result = bot.reaction(args.content_type, args.content_token, args.action)

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
        return

    action_desc = "点赞" if args.action == "like" else "取消点赞"
    if _is_success(result):
        data = result.get("data", {})
        if data.get("success"):
            _print_success(f"{action_desc}成功")
        else:
            _print_failure(f"{action_desc}失败")
    else:
        _print_failure(f"操作失败: {result.get('msg')}")

    return result


def cmd_comment_create(args):
    """创建评论"""
    bot = ZhihuBot(json_mode=args.json)
    result = bot.create_comment(args.content_type, args.content_token, args.content)

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
        return

    if _is_success(result):
        data = result.get("data", {})
        cid = data.get("comment_id", "")
        _print_success(f"评论成功！ID: {cid}")
    else:
        _print_failure(f"评论失败: {result.get('msg')}")

    return result


def cmd_comment_delete(args):
    """删除评论"""
    bot = ZhihuBot(json_mode=args.json)
    result = bot.delete_comment(args.comment_id)

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
        return

    if _is_success(result):
        data = result.get("data", {})
        if data.get("success"):
            _print_success("评论删除成功")
        else:
            _print_failure("评论删除失败")
    else:
        _print_failure(f"删除失败: {result.get('msg')}")

    return result


def cmd_comment_list(args):
    """获取评论列表"""
    bot = ZhihuBot(json_mode=args.json)
    result = bot.list_comments(args.content_type, args.content_token,
                                args.page_num or 1, args.page_size or 10)

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
        return

    if _is_success(result):
        data = result.get("data", {})
        comments = data.get("comments", [])
        has_more = data.get("has_more", False)
        print(f"✅ 共 {len(comments)} 条评论")
        if has_more:
            print("  (还有更多)")
        for i, c in enumerate(comments, 1):
            print(f"  [{i}] {c.get('author_name', 'N/A')}: {c.get('content', '')}")
    else:
        _print_failure(f"获取失败: {result.get('msg')}")

    return result


# ──────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="知乎 AI Bot API 工具")
    parser.add_argument("--json", action="store_true", help="JSON 输出模式（供 bridge.js 调用）")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # ring
    ring_p = subparsers.add_parser("ring", help="圈子操作")
    ring_subs = ring_p.add_subparsers(dest="ring_command")
    rd = ring_subs.add_parser("detail", help="获取圈子详情")
    rd.add_argument("ring_id", help="圈子 ID")
    rd.add_argument("--page-num", type=int)
    rd.add_argument("--page-size", type=int)
    rd.set_defaults(func=cmd_ring_detail)

    # pin
    pin_p = subparsers.add_parser("pin", help="想法操作")
    pin_subs = pin_p.add_subparsers(dest="pin_command")
    pp = pin_subs.add_parser("publish", help="发布想法")
    pp.add_argument("--ring-id", required=True)
    pp.add_argument("--title", required=True)
    pp.add_argument("--content", required=True)
    pp.add_argument("--images", help="图片 URL，逗号分隔")
    pp.set_defaults(func=cmd_pin_publish)

    # reaction
    react_p = subparsers.add_parser("reaction", help="点赞/取消")
    react_p.add_argument("content_type", choices=["pin", "comment"])
    react_p.add_argument("content_token")
    react_p.add_argument("action", choices=["like", "unlike"])
    react_p.set_defaults(func=cmd_reaction)

    # comment
    comm_p = subparsers.add_parser("comment", help="评论操作")
    comm_subs = comm_p.add_subparsers(dest="comment_command")
    cc = comm_subs.add_parser("create", help="创建评论")
    cc.add_argument("content_type", choices=["pin", "comment"])
    cc.add_argument("content_token")
    cc.add_argument("content")
    cc.set_defaults(func=cmd_comment_create)

    cd = comm_subs.add_parser("delete", help="删除评论")
    cd.add_argument("comment_id")
    cd.set_defaults(func=cmd_comment_delete)

    cl = comm_subs.add_parser("list", help="评论列表")
    cl.add_argument("content_type", choices=["pin", "comment"])
    cl.add_argument("content_token")
    cl.add_argument("--page-num", type=int)
    cl.add_argument("--page-size", type=int)
    cl.set_defaults(func=cmd_comment_list)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 路由到对应的命令处理函数
    if args.command == "ring" and args.ring_command == "detail":
        cmd_ring_detail(args)
    elif args.command == "pin" and args.pin_command == "publish":
        cmd_pin_publish(args)
    elif args.command == "reaction":
        cmd_reaction(args)
    elif args.command == "comment":
        if args.comment_command == "create":
            cmd_comment_create(args)
        elif args.comment_command == "delete":
            cmd_comment_delete(args)
        elif args.comment_command == "list":
            cmd_comment_list(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
