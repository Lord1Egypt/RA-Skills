#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Login flows and session management."""

from __future__ import annotations

import random
import re
import string
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from config import get_paths
from database import Database
from log_utils import get_logger
from mp_client import WechatLoginExpiredError, WechatMPClient, WechatRequestError
from openclaw_messaging import MessageTarget, OpenClawMessenger
from session_store import (
    clear_login_session,
    get_login_session,
    get_qrcode_session,
    save_login_session,
    save_qrcode_session,
    update_login_validation,
    update_qrcode_status,
)
from utils import cookiejar_to_entities, ensure_dir, failure, format_timestamp, now_ts, read_json, success


STATUS_MAP = {
    0: "等待扫码",
    1: "登录成功",
    2: "二维码已过期，请重新获取",
    3: "二维码已过期，请重新获取",
    4: "扫码成功，请在手机上确认",
    5: "账号未绑定公众号平台",
    6: "扫码成功，请在手机上确认",
}


LOGGER = get_logger(__name__)


def _generate_sid() -> str:
    suffix = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    return f"skill_{now_ts()}_{suffix}"


def _login_resume_command(
    sid: str,
    channel: str = "",
    target: str = "",
    account: str = "",
) -> str:
    parts = [
        "python scripts/wechat_article_assistant.py login-wait",
        f"--sid '{sid}'",
    ]
    if channel:
        parts.append(f"--channel '{channel}'")
    if target:
        parts.append(f"--target '{target}'")
    if account:
        parts.append(f"--account '{account}'")
    parts.append("--notify true")
    parts.append("--json")
    return " ".join(parts)


def _messenger_from_qrcode_session(qrcode_session: dict[str, Any] | None) -> OpenClawMessenger | None:
    if not qrcode_session:
        return None
    channel = str(qrcode_session.get("notify_channel") or "").strip()
    target = str(qrcode_session.get("notify_target") or "").strip()
    account = str(qrcode_session.get("notify_account") or "").strip()
    if not channel or not target:
        return None
    return OpenClawMessenger(MessageTarget(channel=channel, target=target, account=account))


def _spawn_login_wait_background(sid: str, messenger: OpenClawMessenger | None) -> dict[str, Any] | None:
    if not messenger or not messenger.is_ready():
        return None
    script_path = Path(__file__).resolve().parent / "wechat_article_assistant.py"
    command = [
        sys.executable,
        str(script_path),
        "login-wait",
        "--sid",
        sid,
        "--channel",
        messenger.message_target.channel,
        "--target",
        messenger.message_target.target,
        "--notify",
        "true",
        "--json",
    ]
    if messenger.message_target.account:
        command.extend(["--account", messenger.message_target.account])
    try:
        proc = subprocess.Popen(
            command,
            cwd=str(script_path.parent.parent),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        return {"started": True, "pid": proc.pid, "command": " ".join(command)}
    except Exception as exc:
        LOGGER.warning("spawn login-wait background failed sid=%s error=%s", sid, exc)
        return {"started": False, "error": str(exc), "command": " ".join(command)}


def login_start(
    db: Database,
    messenger: OpenClawMessenger | None = None,
    sid: str = "",
    wait: bool = False,
    timeout: int = 300,
    interval: int = 3,
    notify: bool = True,
) -> dict[str, Any]:
    client = WechatMPClient(db)
    sid = sid or _generate_sid()
    messenger_ready = bool(messenger and messenger.is_ready())
    LOGGER.info(
        "login_start sid=%s notify=%s wait=%s timeout=%s interval=%s",
        sid,
        messenger_ready,
        wait,
        timeout,
        interval,
    )
    session = client.new_session()

    client.request_json(
        session,
        "POST",
        "https://mp.weixin.qq.com/cgi-bin/bizlogin",
        params={"action": "startlogin"},
        data={
            "userlang": "zh_CN",
            "redirect_url": "",
            "login_type": 3,
            "sessionid": sid,
            "token": "",
            "lang": "zh_CN",
            "f": "json",
            "ajax": 1,
        },
        operation="api",
    )

    response = client.request(
        session,
        "GET",
        "https://mp.weixin.qq.com/cgi-bin/scanloginqrcode",
        params={"action": "getqrcode", "random": now_ts()},
        operation="api",
    )

    paths = get_paths()
    ensure_dir(paths.qrcodes_dir)
    qr_path = paths.qrcodes_dir / f"wechat_login_{sid}.png"
    qr_path.write_bytes(response.content)

    cookies = cookiejar_to_entities(session.cookies)
    save_qrcode_session(
        db,
        sid=sid,
        cookies=cookies,
        qr_path=str(qr_path),
        status=0,
        status_text=STATUS_MAP[0],
        expires_at=now_ts() + 5 * 60,
        notify_channel=messenger.message_target.channel if messenger and messenger.is_ready() else "",
        notify_target=messenger.message_target.target if messenger and messenger.is_ready() else "",
        notify_account=messenger.message_target.account if messenger and messenger.is_ready() else "",
    )

    notify_result: dict[str, Any] | None = None
    if notify and messenger and messenger.is_ready():
        ok, message = messenger.send_image(str(qr_path), "请使用微信扫描二维码登录微信公众号平台")
        notify_result = {"success": ok, "message": message}

    background_wait = None
    if notify and messenger and messenger.is_ready() and not wait:
        background_wait = _spawn_login_wait_background(sid, messenger)

    payload = {
        "sid": sid,
        "qr_path": str(qr_path),
        "expires_at": now_ts() + 5 * 60,
        "notify": notify_result,
        "auto_wait": bool(wait),
        "background_wait": background_wait,
        "resume_command": _login_resume_command(
            sid,
            channel=messenger.message_target.channel if messenger and messenger.is_ready() else "",
            target=messenger.message_target.target if messenger and messenger.is_ready() else "",
            account=messenger.message_target.account if messenger and messenger.is_ready() else "",
        ),
    }

    if wait and notify:
        if not messenger_ready:
            payload["wait_skipped"] = True
            payload["wait_skip_reason"] = "message_target_not_ready"
            LOGGER.warning("login_start sid=%s skip wait because messenger is not ready", sid)
            return failure("二维码已生成，但自动发送器未就绪；请手动发送二维码后再执行 login-wait", payload)
        if notify_result and not notify_result.get("success"):
            payload["wait_skipped"] = True
            payload["wait_skip_reason"] = "notify_failed"
            LOGGER.warning("login_start sid=%s skip wait because notify failed error=%s", sid, notify_result.get("message"))
            return failure("二维码已生成，但自动发送失败；请补发二维码后再执行 login-wait", payload)

    if wait:
        wait_result = login_wait(
            db,
            sid=sid,
            timeout=timeout,
            interval=interval,
            messenger=messenger,
            notify=notify,
        )
        payload["wait_result"] = wait_result.get("data", {})
        if wait_result.get("success"):
            return success(payload, wait_result.get("formatted_text") or f"登录成功: {sid}")
        return failure(wait_result.get("error") or "等待登录失败", payload)

    return success(
        payload,
        f"登录二维码已生成: {qr_path}",
    )


def login_poll(db: Database, sid: str, messenger: OpenClawMessenger | None = None, notify: bool = False) -> dict[str, Any]:
    qrcode_session = get_qrcode_session(db, sid)
    if not qrcode_session:
        return failure("未找到指定 sid 的登录二维码会话")
    if (not messenger or not messenger.is_ready()) and notify:
        messenger = _messenger_from_qrcode_session(qrcode_session)
    LOGGER.debug("login_poll sid=%s notify=%s messenger_ready=%s", sid, notify, bool(messenger and messenger.is_ready()))

    client = WechatMPClient(db)
    session = client.new_session(qrcode_session["cookies"])
    payload = client.request_json(
        session,
        "GET",
        "https://mp.weixin.qq.com/cgi-bin/scanloginqrcode",
        params={
            "action": "ask",
            "token": "",
            "lang": "zh_CN",
            "f": "json",
            "ajax": 1,
        },
        operation="api",
    )

    status = int(payload.get("status") or 0)
    status_text = STATUS_MAP.get(status, "未知状态")
    LOGGER.info("login_poll sid=%s status=%s status_text=%s", sid, status, status_text)

    if status == 1:
        login_payload = client.request_json(
            session,
            "POST",
            "https://mp.weixin.qq.com/cgi-bin/bizlogin",
            params={"action": "login"},
            data={
                "userlang": "zh_CN",
                "redirect_url": "",
                "cookie_forbidden": 0,
                "cookie_cleaned": 0,
                "plugin_used": 0,
                "login_type": 3,
                "token": "",
                "lang": "zh_CN",
                "f": "json",
                "ajax": 1,
            },
            operation="api",
        )
        redirect_url = login_payload.get("redirect_url") or ""
        token_match = re.search(r"[?&]token=(\d+)", redirect_url)
        token = token_match.group(1) if token_match else ""
        if not token:
            return failure("登录成功，但未从重定向地址中解析到 token")

        home_response = client.request(
            session,
            "GET",
            "https://mp.weixin.qq.com/cgi-bin/home",
            params={"t": "home/index", "token": token, "lang": "zh_CN"},
            operation="api",
        )
        html = home_response.text
        nickname_match = re.search(r'wx\.cgiData\.nick_name\s*=\s*"(?P<value>[^"]+)"', html)
        head_img_match = re.search(r'wx\.cgiData\.head_img\s*=\s*"(?P<value>[^"]+)"', html)
        nickname = nickname_match.group("value") if nickname_match else ""
        head_img = head_img_match.group("value") if head_img_match else ""

        cookies = cookiejar_to_entities(session.cookies)
        with db.transaction():
            save_login_session(
                db,
                token=token,
                cookies=cookies,
                nickname=nickname,
                head_img=head_img,
                source=f"qrcode:{sid}",
                valid=True,
            )
            update_qrcode_status(db, sid, status, status_text, cookies=cookies, completed=True)

        notify_result: dict[str, Any] | None = None
        if notify and messenger and messenger.is_ready():
            ok, message = messenger.send_text(f"微信公众号登录成功：{nickname or '未命名账号'}")
            notify_result = {"success": ok, "message": message}

        return success(
            {
                "sid": sid,
                "status": status,
                "status_text": status_text,
                "logged_in": True,
                "nickname": nickname,
                "token": token,
                "notify": notify_result,
            },
            f"登录成功: {nickname or '未命名账号'}",
        )

    update_qrcode_status(db, sid, status, status_text, cookies=cookiejar_to_entities(session.cookies), completed=False)
    notify_result = None
    if notify and messenger and messenger.is_ready() and status in {2, 3, 5}:
        ok, message = messenger.send_text(f"微信公众号登录状态：{status_text}")
        notify_result = {"success": ok, "message": message}

    return success(
        {
            "sid": sid,
            "status": status,
            "status_text": status_text,
            "logged_in": False,
            "need_refresh": status in {2, 3},
            "notify": notify_result,
        },
        f"登录状态: {status_text}",
    )


def login_wait(
    db: Database,
    sid: str,
    timeout: int = 300,
    interval: int = 3,
    messenger: OpenClawMessenger | None = None,
    notify: bool = True,
) -> dict[str, Any]:
    LOGGER.info("login_wait sid=%s timeout=%s interval=%s", sid, timeout, interval)
    start = time.time()
    while time.time() - start <= timeout:
        result = login_poll(db, sid=sid, messenger=messenger, notify=notify)
        if not result.get("success"):
            return result
        data = result.get("data", {})
        if data.get("logged_in"):
            return result
        if data.get("need_refresh") or int(data.get("status") or 0) == 5:
            return result
        time.sleep(interval)
    return failure(f"等待扫码登录超时，已等待 {timeout} 秒")


def login_import(db: Database, file_path: str, validate: bool = True) -> dict[str, Any]:
    path = Path(file_path)
    if not path.exists():
        return failure(f"登录文件不存在: {path}")
    LOGGER.info("login_import file=%s validate=%s", path, validate)
    payload = read_json(path)
    token = str(payload.get("token") or "").strip()
    cookies = payload.get("cookies") or []
    if not token or not cookies:
        return failure("登录文件缺少 token 或 cookies")
    save_login_session(
        db,
        token=token,
        cookies=cookies,
        source=f"import:{path}",
        valid=False,
    )
    if not validate:
        return success(
            {
                "token": token,
                "validated": False,
                "source": str(path),
            },
            f"已导入登录信息: {path}",
        )
    return login_info(db, validate=True)


def login_info(db: Database, validate: bool = False) -> dict[str, Any]:
    LOGGER.debug("login_info validate=%s", validate)
    session = get_login_session(db)
    if not session:
        return success(
            {
                "logged_in": False,
                "message": "未找到登录信息，请先扫码登录或导入登录文件",
            },
            "未找到登录信息",
        )

    validation: dict[str, Any] = {
        "requested": bool(validate),
        "validated": bool(session.get("valid")),
        "reason": "",
        "reason_type": "",
    }
    if validate:
        client = WechatMPClient(db)
        try:
            result = client.validate_login()
            update_login_validation(db, True, nickname=result.get("nickname", ""), head_img=result.get("head_img", ""))
            session = get_login_session(db) or session
            validation = {
                "requested": True,
                "validated": True,
                "reason": "登录态校验通过",
                "reason_type": "ok",
            }
        except WechatLoginExpiredError as exc:
            update_login_validation(db, False)
            session = get_login_session(db) or session
            validation = {
                "requested": True,
                "validated": False,
                "reason": str(exc),
                "reason_type": "login_expired",
            }
        except WechatRequestError as exc:
            update_login_validation(db, False)
            session = get_login_session(db) or session
            validation = {
                "requested": True,
                "validated": False,
                "reason": str(exc),
                "reason_type": "request_error",
            }

    logged_in = bool(session.get("valid"))
    formatted_text = f"当前登录账号: {session.get('nickname') or '未知'}"
    if validate and not validation.get("validated"):
        formatted_text = f"{formatted_text}，校验失败: {validation.get('reason') or '未知原因'}"
    return success(
        {
            "logged_in": logged_in,
            "nickname": session.get("nickname", ""),
            "head_img": session.get("head_img", ""),
            "token": session.get("token", ""),
            "source": session.get("source", ""),
            "expires_at": session.get("expires_at"),
            "expires_at_formatted": format_timestamp(session.get("expires_at")),
            "last_validated_at": session.get("last_validated_at"),
            "last_validated_at_formatted": format_timestamp(session.get("last_validated_at")),
            "validation": validation,
        },
        formatted_text,
    )


def login_clear(db: Database) -> dict[str, Any]:
    LOGGER.info("login_clear")
    clear_login_session(db)
    db.execute("DELETE FROM login_qrcode_session")
    return success({"message": "登录信息已清除"}, "登录信息已清除")
