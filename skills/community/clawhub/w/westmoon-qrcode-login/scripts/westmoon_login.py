#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Westmoon QR-code login entrypoint.
"""

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

import requests

from qr_code_client import QRCodeClient
from status_poller import LoginStatus, StatusPoller, StatusResult
from token_manager import TokenInfo, TokenManager


class Config:
    BASE_URL = "https://api-x.westmonth.com"
    GENERATE_ENDPOINT = (
        "/umc/miniprogram/qrcode/generate"
        "?client_id=&scene=login&path=p-user%2Fpages%2Flogin%2Findex"
        "&envVersion=release&source=PCLogin"
    )
    POLL_ENDPOINT = "/umc/miniprogram/qrcode/poll"
    USER_INFO_ENDPOINT = "/umc/user/user/info"

    GENERATE_SOURCE = "PCLogin"
    POLL_SOURCE = "xpw"
    POLL_INTERVAL_MS = 5000
    POLL_TIMEOUT_SECONDS = 300
    NON_BLOCKING_MODE = True
    OPEN_IMAGE = True


@dataclass
class LoginResult:
    success: bool
    message: str
    scan_token: str = ""
    qr_file_path: str = ""
    qr_data_uri: str = ""
    user_info: Optional[Dict[str, Any]] = None


class WestmoonLoginManager:
    def __init__(self, config: Optional[Config] = None) -> None:
        self.config = config or Config()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                ),
                "Accept": "application/json, text/plain, */*",
            }
        )
        self.qr_client = QRCodeClient(
            base_url=self.config.BASE_URL,
            generate_endpoint=self.config.GENERATE_ENDPOINT,
            session=self.session,
        )
        self.status_poller = StatusPoller(
            base_url=self.config.BASE_URL,
            poll_endpoint=self.config.POLL_ENDPOINT,
            poll_interval_ms=self.config.POLL_INTERVAL_MS,
            timeout_seconds=self.config.POLL_TIMEOUT_SECONDS,
            session=self.session,
        )
        self.token_manager = TokenManager()

    def login(
        self,
        blocking_mode: Optional[bool] = None,
        show_qr_callback: Optional[Callable[[bytes, str], None]] = None,
        send_qr_to_user_callback: Optional[Callable[[bytes, str], None]] = None,
        scan_token_to_poll: Optional[str] = None,
    ) -> LoginResult:
        if scan_token_to_poll:
            return self._poll_and_complete(scan_token_to_poll)

        print("=" * 60)
        print("西之月扫码登录")
        print("=" * 60)
        print("\n[1/3] 正在获取二维码...")

        success, result, qr_url = self.qr_client.generate_qr_code(
            {
                "source": self.config.GENERATE_SOURCE,
            }
        )
        if not success or not result:
            return LoginResult(False, f"获取二维码失败: {result}")

        data = result.get("data") or {}
        scan_token = data.get("scan_token", "")
        qr_data_uri = data.get("wxacode", "")
        poll_interval_ms = int(data.get("poll_interval") or self.config.POLL_INTERVAL_MS)
        expires_in = int(data.get("expires_in") or self.config.POLL_TIMEOUT_SECONDS)

        if not scan_token or not qr_data_uri:
            return LoginResult(False, "返回数据缺少 scan_token 或 wxacode")

        ok, image_bytes, image_format = self.qr_client.decode_wxacode(qr_data_uri)
        if not ok or not image_bytes:
            return LoginResult(False, "wxacode 解码失败", scan_token=scan_token)

        qr_file_path = self.qr_client.save_qr_image(image_bytes, image_format or "png") or ""

        print("[1/3] ✓ 获取二维码成功")
        print("\n[2/3] 正在展示二维码...")

        if show_qr_callback:
            show_qr_callback(image_bytes, image_format or "png")
        elif self.config.OPEN_IMAGE and qr_file_path:
            self.qr_client.open_qr_image(qr_file_path)

        if send_qr_to_user_callback:
            send_qr_to_user_callback(image_bytes, image_format or "png")

        if qr_file_path:
            print(f"[2/3] 二维码文件: {qr_file_path}")
        print(f"[2/3] scan_token: {scan_token}")
        print(f"[2/3] 二维码有效期: {expires_in} 秒")
        print(f"[2/3] 轮询间隔: {poll_interval_ms} ms")
        print(f"[2/3] 生成接口: {qr_url}")

        if os.environ.get("OPENCLAW_SESSION") == "1":
            if qr_file_path:
                print(f"[OPENCLAW_SEND_FILE]{qr_file_path}[/OPENCLAW_SEND_FILE]")
            print(qr_data_uri)

        use_blocking = (
            blocking_mode if blocking_mode is not None else not self.config.NON_BLOCKING_MODE
        )
        self.token_manager.save_pending_login(scan_token, poll_interval_ms=poll_interval_ms)

        if not use_blocking:
            print("\n[3/3] 请扫码确认后继续轮询")
            print(f"python scripts/westmoon_login.py --poll {scan_token}")
            return LoginResult(
                True,
                "二维码已展示，请扫码确认后使用 --poll 或 --continue 完成登录",
                scan_token=scan_token,
                qr_file_path=qr_file_path,
                qr_data_uri=qr_data_uri,
            )

        return self._poll_and_complete(scan_token)

    def _poll_and_complete(self, scan_token: str) -> LoginResult:
        print("\n[3/3] 正在轮询扫码状态...")

        def on_status_change(result: StatusResult) -> None:
            print(f"[轮询] {result.status_str}: {result.message}")

        result = self.status_poller.poll_until_complete(
            scan_token=scan_token,
            source=self.config.POLL_SOURCE,
            on_status_change=on_status_change,
        )
        if result.status != LoginStatus.CONFIRMED:
            return LoginResult(False, result.message, scan_token=scan_token)

        token_info = TokenInfo(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            token_type=result.token_type or "Bearer",
            expires_in=result.expires_in,
        )

        user_info = self.fetch_user_info(token_info.authorization_header)
        if not user_info["success"]:
            return LoginResult(
                False,
                f"登录成功，但校验用户信息失败: {user_info['message']}",
                scan_token=scan_token,
            )

        token_info.user_info = user_info["data"]
        self.token_manager.save_token(token_info)
        self.token_manager.clear_pending_login()
        self.qr_client.cleanup_qr_files()

        return LoginResult(
            True,
            "登录成功",
            scan_token=scan_token,
            user_info=user_info["data"],
        )

    def fetch_user_info(self, authorization_header: str) -> Dict[str, Any]:
        url = f"{self.config.BASE_URL}{self.config.USER_INFO_ENDPOINT}"
        try:
            response = self.session.get(
                url,
                headers={"Authorization": authorization_header},
                timeout=15,
            )
            if response.status_code == 401:
                return {"success": False, "message": "token 无效或已过期", "status_code": 401}
            response.raise_for_status()
            payload = response.json()
            return {
                "success": True,
                "message": "ok",
                "data": payload.get("data", payload),
                "raw": payload,
            }
        except requests.RequestException as exc:
            return {"success": False, "message": str(exc)}

    def check_login(self) -> Dict[str, Any]:
        token = self.token_manager.get_token()
        if not token:
            return {"success": False, "message": "没有有效登录态"}
        return self.fetch_user_info(token.authorization_header)

    def get_user_info(self) -> Dict[str, Any]:
        token = self.token_manager.get_token()
        if not token:
            return {"success": False, "message": "没有有效登录态"}
        return self.fetch_user_info(token.authorization_header)


def main() -> int:
    parser = argparse.ArgumentParser(description="西之月扫码登录")
    parser.add_argument("--blocking", action="store_true", help="阻塞等待扫码完成")
    parser.add_argument("--poll", help="使用指定 scan_token 继续轮询")
    parser.add_argument("--continue", dest="continue_login", action="store_true", help="继续上次轮询")
    parser.add_argument("--status", action="store_true", help="查看本地登录态摘要")
    parser.add_argument("--check", action="store_true", help="检查当前 token 是否有效")
    parser.add_argument("--userinfo", action="store_true", help="获取当前用户信息")
    parser.add_argument("--logout", action="store_true", help="清除本地登录态")
    args = parser.parse_args()

    manager = WestmoonLoginManager()

    if args.logout:
        manager.token_manager.remove_token()
        manager.token_manager.clear_pending_login()
        print("已清除本地登录态")
        return 0

    if args.status:
        manager.token_manager.print_summary()
        return 0

    if args.check:
        result = manager.check_login()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("success") else 1

    if args.userinfo:
        result = manager.get_user_info()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("success") else 1

    scan_token = args.poll
    if args.continue_login:
        pending = manager.token_manager.load_pending_login()
        if not pending:
            print("没有可继续的待处理扫码记录")
            return 1
        scan_token = pending["scan_token"]

    result = manager.login(
        blocking_mode=args.blocking,
        scan_token_to_poll=scan_token,
    )
    if result.user_info:
        print(json.dumps(result.user_info, ensure_ascii=False, indent=2))
    print(result.message)
    if result.scan_token:
        print(f"scan_token: {result.scan_token}")
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
