#!/usr/bin/env python3
"""
远程授权专用：仅通过授权服务器 /api/activate、/api/check 校验，不包含本地签名校验。
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import time
import uuid
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from app_errors import LicenseError

# 默认授权服务（可被环境变量 TMO_LICENSE_SERVER 覆盖）
_DEFAULT_LICENSE_SERVER = "http://120.27.202.105:8000"
_LICENSE_ENV = os.environ.get("TMO_LICENSE_SERVER")
LICENSE_SERVER_URL = (_LICENSE_ENV if _LICENSE_ENV is not None and _LICENSE_ENV.strip() != "" else _DEFAULT_LICENSE_SERVER).rstrip(
    "/"
)


def machine_fingerprint() -> str:
    node = platform.node() or ""
    system = platform.system() or ""
    machine = platform.machine() or ""
    mac = str(uuid.getnode())
    raw = f"{node}|{system}|{machine}|{mac}".encode("utf-8", errors="ignore")
    return hashlib.sha256(raw).hexdigest()[:24]


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def _save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _fmt_ts(ts: int) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ts)))


def _http_post_json(url: str, payload: dict[str, Any], timeout: float = 10.0) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8")
            data = json.loads(text or "{}")
            return data if isinstance(data, dict) else {}
    except urllib.error.HTTPError as exc:
        try:
            text = exc.read().decode("utf-8")
            data = json.loads(text or "{}")
            if isinstance(data, dict) and "detail" in data:
                raise LicenseError(f"授权服务器错误: {data['detail']}") from exc
        except Exception:
            pass
        raise LicenseError(f"授权服务器响应异常 (HTTP {exc.code})，请稍后重试。") from exc
    except urllib.error.URLError as exc:
        raise LicenseError("无法连接授权服务器，请检查服务器是否可访问或稍后重试。") from exc


def _remote_activate(card_key: str, machine_fp: str) -> dict[str, Any]:
    if not LICENSE_SERVER_URL:
        raise LicenseError("未配置授权服务器地址，请设置环境变量 TMO_LICENSE_SERVER。")
    url = f"{LICENSE_SERVER_URL}/api/activate"
    data = _http_post_json(url, {"card_key": card_key, "machine_fp": machine_fp})
    if (data.get("status") or "").lower() != "ok":
        msg = str(data.get("message") or "卡密激活失败，请确认卡密是否正确或联系卖家。")
        raise LicenseError(msg)
    return data


def _remote_check(machine_fp: str, card_key: str | None = None) -> dict[str, Any]:
    if not LICENSE_SERVER_URL:
        raise LicenseError("未配置授权服务器地址，请设置环境变量 TMO_LICENSE_SERVER。")
    url = f"{LICENSE_SERVER_URL}/api/check"
    payload: dict[str, Any] = {"machine_fp": machine_fp}
    if card_key:
        payload["card_key"] = card_key
    data = _http_post_json(url, payload)
    if (data.get("status") or "").lower() != "ok":
        msg = str(data.get("message") or "授权校验失败，请重新输入卡密或联系卖家。")
        raise LicenseError(msg)
    return data


def load_license_status(license_file: Path) -> dict[str, Any]:
    now = int(time.time())
    fp = machine_fingerprint()
    act = _load_json(license_file)
    if not act:
        return {
            "status": "missing",
            "license_file": str(license_file),
            "machine_fp": fp,
        }
    ver = int(act.get("version") or 0)
    if ver < 2:
        return {
            "status": "legacy_local",
            "license_file": str(license_file),
            "machine_fp": fp,
            "message": "检测到旧版本地授权文件，请删除该文件后使用服务器卡密重新激活。",
        }
    if str(act.get("machine_fp") or "") != fp:
        return {
            "status": "wrong_machine",
            "license_file": str(license_file),
            "machine_fp": fp,
            "bound_machine_fp": str(act.get("machine_fp") or ""),
        }
    expires_at = int(act.get("expires_at") or 0)
    if expires_at <= now:
        return {
            "status": "expired",
            "license_file": str(license_file),
            "machine_fp": fp,
            "expires_at": expires_at,
            "expires_at_text": _fmt_ts(expires_at),
            "plan": str(act.get("plan") or ""),
        }
    return {
        "status": "valid",
        "license_file": str(license_file),
        "machine_fp": fp,
        "expires_at": expires_at,
        "expires_at_text": _fmt_ts(expires_at),
        "activated_at": int(act.get("activated_at") or 0),
        "plan": str(act.get("plan") or ""),
    }


def ensure_license(license_file: Path, key_from_cli: str = "") -> dict[str, Any]:
    if not LICENSE_SERVER_URL:
        raise LicenseError("未配置授权服务器地址，请设置环境变量 TMO_LICENSE_SERVER。")

    now = int(time.time())
    fp = machine_fingerprint()
    act = _load_json(license_file)

    if act and int(act.get("version") or 0) < 2:
        raise LicenseError(
            "检测到旧版本地授权文件，本版本仅支持服务器卡密。\n"
            f"请手动删除后重新激活：\n  {license_file}"
        )

    if act and str(act.get("machine_fp") or "") == fp:
        try:
            remote = _remote_check(fp, card_key=str(act.get("key") or ""))
            act["plan"] = remote.get("plan") or act.get("plan") or "custom"
            expires = int(remote.get("expires_at") or act.get("expires_at") or now)
            act["expires_at"] = expires
            _save_json(license_file, act)
            return act
        except LicenseError:
            pass

    key = (key_from_cli or "").strip()
    if not key:
        print("未发现有效授权，请输入卡密（由卖家提供）：")
        key = input("Card Key: ").strip()
    if not key:
        raise LicenseError("未输入卡密，已退出。")

    remote = _remote_activate(key, fp)
    expires_at = int(remote.get("expires_at") or 0)
    if not expires_at or expires_at <= now:
        raise LicenseError("卡密已过期或授权异常，请联系卖家处理。")

    act = {
        "version": 2,
        "key": key,
        "plan": str(remote.get("plan") or "custom"),
        "machine_fp": fp,
        "activated_at": now,
        "expires_at": expires_at,
    }
    _save_json(license_file, act)
    print(f"授权激活成功，方案: {act['plan']}，到期: {_fmt_ts(act['expires_at'])}")
    return act
