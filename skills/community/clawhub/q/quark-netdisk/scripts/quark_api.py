#!/usr/bin/env python3
"""Minimal Quark Drive API adapter (based on QuarkPan findings).

Goals for v1:
- API QR login (uop.quark.cn) and obtain cookie jar (httpOnly included)
- Create remote folder `/OpenClaw` under root if missing
- Upload a local file into that folder (multipart supported)

Module 3 (file ops) adds:
- resolve remote paths under allowlist (/OpenClaw/**)
- rename/move/copy/delete operations (delete is soft-delete to /OpenClaw/.trash)
- purge trash entries older than retention days

This module is intentionally small and self-contained for the OpenClaw skill.
"""

from __future__ import annotations

import base64
import hashlib
import json
import mimetypes
import os
import re
import time
import urllib.parse
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import formatdate
from pathlib import PurePosixPath, Path
from typing import Any, Callable, Optional

import httpx
import qrcode


BASE_URL = "https://drive-pc.quark.cn/1/clouddrive"
SHARE_BASE_URL = "https://drive.quark.cn/1/clouddrive"
PAN_ORIGIN = "https://pan.quark.cn"


def now_ms() -> int:
    return int(time.time() * 1000)


def default_headers() -> dict[str, str]:
    # Aligned with QuarkPan default headers (QQBrowser UA + explicit origin/referer).
    return {
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/94.0.4606.71 Safari/537.36 Core/1.94.225.400 QQBrowser/12.2.5544.400"
        ),
        "origin": PAN_ORIGIN,
        "referer": PAN_ORIGIN + "/",
        "accept-language": "zh-CN,zh;q=0.9",
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
    }


def build_params(extra: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    # Align with QuarkPan: always include __t/__dt.
    # Some endpoints are sensitive, but QuarkPan works with this.
    p: dict[str, Any] = {
        "pr": "ucpro",
        "fr": "pc",
        "uc_param_str": "",
        "__t": now_ms(),
        "__dt": 1000,
    }
    if extra:
        p.update(extra)
    return p


def save_png_qr(url: str, out_path: Path) -> None:
    img = qrcode.make(url)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)


@dataclass
class LoginResult:
    cookie_string: str
    cookies_json: list[dict[str, Any]]


class QuarkSession:
    def __init__(self, timeout_s: int = 60, cookie_string: str | None = None, cookies_json: list[dict[str, Any]] | None = None):
        # Disable environment proxies by default (common cause: ALL_PROXY=socks://...)
        # We only want direct HTTPS to quark domains unless explicitly configured.
        # cookie_string is kept for debugging; prefer cookies_json (domain/path-aware) for correctness.
        self.cookie_string = cookie_string
        self.cookies_json = cookies_json or []
        # Align with QuarkPan request semantics, but keep trust_env=False because this host has
        # a socks:// proxy env that httpx can't parse.
        self.client = httpx.Client(
            timeout=timeout_s,
            headers=default_headers(),
            follow_redirects=True,
            trust_env=False,
        )

        # Load structured cookies into jar (QuarkPan-style).
        for c in self.cookies_json:
            try:
                name = c.get("name")
                value = c.get("value")
                domain = c.get("domain")
                path = c.get("path") or "/"
                if name and value and domain:
                    self.client.cookies.set(name, value, domain=domain, path=path)
            except Exception:
                pass

    def close(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    # ---------- login ----------
    def get_qr_token(self) -> str:
        url = "https://uop.quark.cn/cas/ajax/getTokenForQrcodeLogin"
        params = {"client_id": "532", "v": "1.2", "request_id": str(uuid.uuid4())}
        r = self.client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        if data.get("status") != 2000000:
            raise RuntimeError(f"getTokenForQrcodeLogin failed: {data}")
        token = data.get("data", {}).get("members", {}).get("token")
        if not token:
            raise RuntimeError(f"token missing: {data}")
        return token

    def build_qr_url(self, token: str) -> str:
        base = "https://su.quark.cn/4_eMHBJ"
        params = {
            "token": token,
            "client_id": "532",
            "ssb": "weblogin",
            "uc_param_str": "",
            "uc_biz_str": "S:custom|OPT:SAREA@0|OPT:IMMERSIVE@1|OPT:BACK_BTN_STYLE@0",
        }
        return base + "?" + urllib.parse.urlencode(params)

    def poll_service_ticket(
        self,
        token: str,
        timeout_s: int = 300,
        progress_cb: Optional[Callable[[int, str], None]] = None,
        progress_interval_s: int = 30,
        poll_interval_s: float = 2.0,
    ) -> str:
        url = "https://uop.quark.cn/cas/ajax/getServiceTicketByQrcodeToken"
        start = time.time()
        last_progress = 0.0

        def report(msg: str):
            if not progress_cb:
                return
            elapsed = int(time.time() - start)
            remaining = max(0, int(timeout_s - elapsed))
            progress_cb(remaining, msg)

        while time.time() - start < timeout_s:
            now = time.time()
            if progress_cb and (now - last_progress) >= progress_interval_s:
                last_progress = now
                report("等待扫码确认中")

            params = {
                "client_id": "532",
                "v": "1.2",
                "token": token,
                "request_id": str(uuid.uuid4()),
            }
            r = self.client.get(url, params=params)
            if r.status_code != 200:
                time.sleep(poll_interval_s)
                continue
            data = r.json()
            st = data.get("data", {}).get("members", {}).get("service_ticket")
            if data.get("status") == 2000000 and data.get("message") == "ok" and st:
                report("扫码确认成功")
                return st
            # waiting code is often 50004001; treat as pending
            time.sleep(poll_interval_s)
        report("登录超时")
        raise TimeoutError("QR login timeout")

    def exchange_ticket_for_cookies(self, service_ticket: str) -> None:
        # visiting account/info sets baseline cookies in cookie jar
        url = "https://pan.quark.cn/account/info"
        params = {"st": service_ticket, "lw": "scan"}
        r = self.client.get(url, params=params)
        r.raise_for_status()
        _ = r.json()

    def hydrate_drive_pc_cookies(self, cookie_string: str) -> None:
        """Trigger drive-pc to set additional cookies (e.g. __puus) needed by upload/auth.

        Empirically, calling behavior/recent/list on drive-pc yields Set-Cookie: __puus=...
        when authenticated.
        """
        h = default_headers()
        h["cookie"] = cookie_string
        # 1) recent list
        try:
            self.client.get(
                "https://drive-pc.quark.cn/1/clouddrive/behavior/recent/list",
                params={"pr": "ucpro", "fr": "pc", "uc_param_str": "", "item_size": 1},
                headers=h,
            )
        except Exception:
            pass
        # 2) a cheap file api
        try:
            self.client.get(
                "https://drive-pc.quark.cn/1/clouddrive/file/sort",
                params={"pr": "ucpro", "fr": "pc", "uc_param_str": ""},
                headers=h,
            )
        except Exception:
            pass

    def export_cookies(self) -> LoginResult:
        cookies_json: list[dict[str, Any]] = []
        pairs: list[str] = []
        for c in self.client.cookies.jar:
            # keep all quark.cn cookies
            if c.domain and "quark.cn" in c.domain:
                # Align with QuarkPan: normalize all cookie domains to .quark.cn
                # so they are sent to drive-pc.quark.cn as well.
                cookies_json.append(
                    {
                        "name": c.name,
                        "value": c.value,
                        "domain": ".quark.cn",
                        "path": "/",
                        "secure": bool(getattr(c, "secure", False)),
                        "expires": getattr(c, "expires", None),
                        "httponly": bool(getattr(c, "rest", {}).get("HttpOnly")) if hasattr(c, "rest") else None,
                    }
                )
                pairs.append(f"{c.name}={c.value}")
        return LoginResult(cookie_string="; ".join(pairs), cookies_json=cookies_json)

    # ---------- api calls ----------
    def _safe_http_error(self, r: httpx.Response) -> str:
        """Return a safe, compact error string without leaking cookies/tokens."""
        if os.environ.get("QUARK_DEBUG_HTTP") == "1":
            return r.text[:800]
        # Best-effort parse JSON
        try:
            j = r.json()
            if isinstance(j, dict):
                code = j.get("code")
                msg = j.get("message")
                status = j.get("status")
                if code is not None or msg is not None or status is not None:
                    return json.dumps({"status": status, "code": code, "message": msg}, ensure_ascii=False)
        except Exception:
            pass
        # Fallback: do not include URL query/body
        return (r.text or "").strip().splitlines()[0][:200]

    def api_get(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
        *,
        base_url: str = BASE_URL,
        raw_params: bool = False,
    ) -> dict[str, Any]:
        url = base_url.rstrip("/") + "/" + path.lstrip("/")
        # Align with QuarkPan: explicitly send cookie header string on every API call.
        h = default_headers()
        if self.cookie_string:
            h["cookie"] = self.cookie_string
        p = (params or {})
        if not raw_params:
            p = build_params(p)
        r = self.client.get(url, params=p, headers=h)
        if r.status_code in (401, 403):
            raise PermissionError(f"Unauthorized: {r.status_code} {self._safe_http_error(r)}")
        if r.status_code >= 400:
            raise RuntimeError(f"HTTP {r.status_code} GET {path} -> {self._safe_http_error(r)}")
        return r.json()

    def api_post(
        self,
        path: str,
        json_data: dict[str, Any],
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        raw_params: bool = False,
        *,
        base_url: str = BASE_URL,
    ) -> dict[str, Any]:
        """POST helper.

        - headers: optional header overrides/extra.
        - raw_params: if True, do not apply build_params() (caller provides final params).
        - base_url: override base URL (e.g. SHARE_BASE_URL for share-page APIs).
        """
        url = base_url.rstrip("/") + "/" + path.lstrip("/")
        h = default_headers()
        if self.cookie_string:
            h["cookie"] = self.cookie_string
        if headers:
            h.update(headers)
        p = (params or {})
        if not raw_params:
            p = build_params(p)

        r = self.client.post(url, params=p, json=json_data, headers=h)
        if r.status_code in (401, 403):
            raise PermissionError(f"Unauthorized: {r.status_code} {self._safe_http_error(r)}")
        if r.status_code >= 400:
            raise RuntimeError(f"HTTP {r.status_code} POST {path} -> {self._safe_http_error(r)}")
        return r.json()


# ------------------------------
# Share (create + save)
# ------------------------------

def file_info(session: QuarkSession, fid: str) -> dict[str, Any]:
    return session.api_get("file/info", params={"fid": fid})


def resolve_fid_path(session: QuarkSession, fid: str) -> str:
    """Resolve a fid to an absolute path by walking parents via file/info.

    Returns: /<parent>/<name>
    """
    if fid == "0":
        return "/"
    parts: list[str] = []
    cur = fid
    guard = 0
    while cur and cur != "0" and guard < 50:
        guard += 1
        info = file_info(session, cur)
        if info.get("status") != 200:
            raise RuntimeError(f"file/info failed: {info}")
        data = info.get("data") or {}
        name = data.get("file_name")
        pdir = str(data.get("pdir_fid") or "0")
        if name:
            parts.append(str(name))
        cur = pdir
    if guard >= 50:
        raise RuntimeError("resolve_fid_path guard exceeded")
    return "/" + "/".join(reversed([p for p in parts if p]))


def parse_share_url(text: str) -> tuple[str, str | None]:
    """Parse Quark share URL/text and return (share_id, passcode?).

    Accepts:
      - https://pan.quark.cn/s/<id>
      - https://pan.quark.cn/s/<id> ... 提取码/密码 xxxx
    """
    m = re.search(r"https?://pan\.quark\.cn/s/([a-zA-Z0-9]+)", text)
    if not m:
        raise ValueError(f"无法解析分享链接: {text}")
    share_id = m.group(1)

    passcode = None
    m2 = re.search(r"(?:提取码|密码)[：:\s]*([a-zA-Z0-9]+)", text)
    if m2:
        passcode = m2.group(1)
    return share_id, passcode


def create_share(
    session: QuarkSession,
    fid_list: list[str],
    *,
    title: str = "",
    expire_days: int = 0,
    passcode: str | None = None,
    poll_timeout_s: int = 20,
) -> dict[str, Any]:
    """Create a share link for files/folders.

    Implementation mirrors QuarkPan:
      POST /share (drive-pc) -> task_id
      GET /task?task_id=... polling -> share_id
      POST /share/password -> full share info (incl. share_url)

    Defaults: no password + permanent.
    """
    data: dict[str, Any] = {
        "fid_list": fid_list,
        "title": title,
        "url_type": 2 if passcode else 1,
        "expired_type": 1 if expire_days == 0 else 2,
    }
    if expire_days > 0:
        data["expired_at"] = int((time.time() + expire_days * 24 * 3600) * 1000)
    if passcode:
        data["passcode"] = passcode

    resp = session.api_post("share", json_data=data)
    if resp.get("status") != 200:
        raise RuntimeError(f"创建分享失败: {resp}")
    task_id = (resp.get("data") or {}).get("task_id")
    if not task_id:
        raise RuntimeError(f"无法获取分享任务ID: {resp}")

    start = time.time()
    retry_index = 0
    share_id = None
    last_task = None
    while time.time() - start < poll_timeout_s:
        t = session.api_get("task", params={"task_id": task_id, "retry_index": retry_index})
        last_task = t
        if t.get("status") == 200:
            td = t.get("data") or {}
            st = td.get("status")
            if st == 2:
                share_id = td.get("share_id") or (td.get("share") or {}).get("share_id")
                break
            if st == 3:
                raise RuntimeError(f"分享创建失败: {t}")
        retry_index += 1
        time.sleep(1)

    if not share_id:
        raise RuntimeError(f"分享创建未返回 share_id（可能接口字段变化/权限限制）: {last_task}")

    details = session.api_post("share/password", json_data={"share_id": share_id})
    if details.get("status") != 200:
        raise RuntimeError(f"获取分享详情失败: {details}")
    return details.get("data") or {}


def get_share_token(session: QuarkSession, share_id: str, passcode: str | None) -> str:
    resp = session.api_post(
        "share/sharepage/token",
        json_data={
            "pwd_id": share_id,
            "passcode": passcode or "",
            "support_visit_limit_private_share": True,
        },
        base_url=SHARE_BASE_URL,
    )
    if resp.get("status") != 200:
        raise RuntimeError(f"获取分享 token 失败: {resp}")
    stoken = (resp.get("data") or {}).get("stoken")
    if not stoken:
        raise RuntimeError(f"token 缺失: {resp}")
    return stoken


def get_share_detail(session: QuarkSession, share_id: str, stoken: str, pdir_fid: str = "0") -> dict[str, Any]:
    return session.api_get(
        "share/sharepage/detail",
        params={
            "pwd_id": share_id,
            "stoken": stoken,
            "pdir_fid": pdir_fid,
            "force": "0",
            "_page": 1,
            "_size": 200,
            "_fetch_banner": "1",
            "_fetch_share": "1",
            "_fetch_total": "1",
            "_sort": "file_type:asc,file_name:asc",
        },
        base_url=SHARE_BASE_URL,
    )


def save_share_to_my_drive(
    session: QuarkSession,
    *,
    share_id: str,
    stoken: str,
    to_pdir_fid: str,
    save_all: bool = True,
    fid_list: list[str] | None = None,
    pdir_fid: str = "0",
    wait: bool = True,
    timeout_s: int = 60,
) -> dict[str, Any]:
    data = {
        "fid_list": [] if save_all else (fid_list or []),
        "fid_token_list": [],
        "to_pdir_fid": to_pdir_fid,
        "pwd_id": share_id,
        "stoken": stoken,
        "pdir_fid": pdir_fid,
        "pdir_save_all": bool(save_all),
        "exclude_fids": [],
        "scene": "link",
    }
    try:
        resp = session.api_post("share/sharepage/save", json_data=data, base_url=SHARE_BASE_URL)
    except RuntimeError as e:
        # Typical business error when trying to save your own share:
        # {"status":404,"code":41017,"message":"用户禁止转存自己的分享",...}
        s = str(e)
        if "\"code\":41017" in s or "用户禁止转存自己的分享" in s:
            raise PermissionError("用户禁止转存自己的分享（请使用他人分享链接测试/转存）") from e
        raise

    if resp.get("status") != 200:
        raise RuntimeError(f"转存失败: {resp}")

    if not wait:
        return resp

    task_id = (resp.get("data") or {}).get("task_id")
    if not task_id:
        return resp

    # Poll task on drive-pc (matches QuarkPan behavior)
    start = time.time()
    retry_index = 0
    last = None
    while time.time() - start < timeout_s:
        t = session.api_get("task", params={"task_id": task_id, "retry_index": retry_index})
        last = t
        if t.get("status") == 200:
            td = t.get("data") or {}
            st = td.get("status")
            if st == 2:
                resp["task_result"] = t
                return resp
            if st == 3:
                raise RuntimeError(f"转存任务失败: {t}")
        retry_index += 1
        time.sleep(1)

    resp["task_result"] = last
    return resp


# ------------------------------
# Listing/search/mkdir
# ------------------------------

def list_folder(session: QuarkSession, parent_id: str = "0", size: int = 200) -> list[dict[str, Any]]:
    res = session.api_get(
        "file/sort",
        params={
            "pdir_fid": parent_id,
            "_page": 1,
            "_size": size,
            "_sort": "file_name:asc",
        },
    )
    return res.get("data", {}).get("list", [])


def search(session: QuarkSession, keyword: str, page: int = 1, size: int = 50) -> dict[str, Any]:
    return session.api_get(
        "file/search",
        params={
            "q": keyword,
            "_page": page,
            "_size": size,
            "_fetch_total": 1,
            "_sort": "file_type:desc,updated_at:desc",
            "_is_hl": 1,
        },
    )


def ensure_folder(session: QuarkSession, name: str, parent_id: str = "0") -> str:
    lst = list_folder(session, parent_id=parent_id, size=200)
    for item in lst:
        # Quark API uses numeric file_type: 0=folder, 1=file (observed)
        if item.get("file_name") == name and item.get("file_type") in (0, "folder"):
            return item.get("fid")
    # create (may return same-name conflict if created concurrently)
    data = {"pdir_fid": parent_id, "file_name": name, "dir_init_lock": False, "dir_path": ""}
    try:
        created = session.api_post("file", json_data=data)
        fid = created.get("data", {}).get("fid") or created.get("data", {}).get("file", {}).get("fid")
        if fid:
            return fid
    except Exception:
        pass
    # fallback: re-list
    return ensure_folder(session, name, parent_id)


# ------------------------------
# Remote path helpers + file ops
# ------------------------------

def _norm_remote_path(p: str) -> str:
    if not p.startswith("/"):
        p = "/" + p
    # Use posix normalization and strip trailing slash (except root)
    pp = str(PurePosixPath(p))
    if pp != "/" and pp.endswith("/"):
        pp = pp[:-1]
    return pp


def enforce_remote_allowlist(remote_path: str, allowlist: list[str]) -> None:
    """Allowlist semantics: entries like '/OpenClaw/**' or '/OpenClaw'."""
    rp = _norm_remote_path(remote_path)
    ok = False
    for a in allowlist:
        a = _norm_remote_path(a)
        if a.endswith("/**"):
            base = a[:-3]
            if rp == base or rp.startswith(base + "/"):
                ok = True
                break
        else:
            if rp == a or rp.startswith(a + "/"):
                ok = True
                break
    if not ok:
        raise PermissionError(f"远端路径不在 allowlist: {rp}")


def split_remote_path(remote_path: str) -> tuple[str, str]:
    rp = _norm_remote_path(remote_path)
    parent = str(PurePosixPath(rp).parent)
    name = PurePosixPath(rp).name
    if parent == "/" and name == "":
        raise ValueError("remote_path cannot be root")
    return parent, name


def resolve_remote_fid(session: QuarkSession, remote_path: str) -> str:
    """Resolve an absolute path to a fid by walking from root id=0."""
    rp = _norm_remote_path(remote_path)
    if rp == "/":
        return "0"
    cur = "0"
    for part in [p for p in rp.split("/") if p]:
        lst = list_folder(session, parent_id=cur, size=200)
        found = None
        for it in lst:
            if it.get("file_name") == part:
                found = it
                break
        if not found:
            raise FileNotFoundError(f"远端不存在: {remote_path}")
        cur = str(found.get("fid"))
    return cur


def ensure_remote_dir(session: QuarkSession, remote_dir_path: str) -> str:
    """Ensure a directory path exists; returns dir fid."""
    rp = _norm_remote_path(remote_dir_path)
    if rp == "/":
        return "0"
    cur = "0"
    for part in [p for p in rp.split("/") if p]:
        # if exists and is folder, reuse; else create
        lst = list_folder(session, parent_id=cur, size=200)
        found = None
        for it in lst:
            if it.get("file_name") == part and it.get("file_type") in (0, "folder"):
                found = it
                break
        if found:
            cur = str(found.get("fid"))
            continue
        cur = ensure_folder(session, part, parent_id=cur)
    return cur


def rename_file(session: QuarkSession, fid: str, new_name: str) -> dict[str, Any]:
    """Rename by fid. Endpoint observed in QuarkPan: file/rename."""
    return session.api_post("file/rename", json_data={"fid": fid, "file_name": new_name})


def move_file(session: QuarkSession, fid: str, new_parent_fid: str, current_dir_fid: str | None = None) -> dict[str, Any]:
    """Move file/folder by fid to new directory fid.

    Quark backend expects `filelist` (and sometimes also `current_dir_fid`).
    Error observed: "Bad Parameter: [current_dir_fid,filelist 不能同时为空]".
    """
    # Some backends accept only filelist; others want current_dir_fid. We'll try filelist-only first.
    payload: dict[str, Any] = {"to_pdir_fid": new_parent_fid, "filelist": [fid]}
    try:
        return session.api_post("file/move", json_data=payload)
    except Exception:
        if current_dir_fid:
            payload2 = {"to_pdir_fid": new_parent_fid, "filelist": [fid], "current_dir_fid": current_dir_fid}
            return session.api_post("file/move", json_data=payload2)
        raise


def delete_file(session: QuarkSession, fid: str) -> dict[str, Any]:
    """Hard delete by fid.

    Backend expects `filelist`.
    """
    return session.api_post("file/delete", json_data={"filelist": [fid]})


def soft_delete_to_trash(
    session: QuarkSession,
    src_remote_path: str,
    trash_root: str = "/OpenClaw/.trash",
) -> dict[str, Any]:
    """Soft delete: move item under /OpenClaw/.trash/<YYYYmmdd-HHMMSS>_<name>.

    This avoids permanent deletion. Caller should enforce allowlist.
    """
    src_parent, src_name = split_remote_path(src_remote_path)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    safe_name = src_name.replace("/", "_")
    trash_dir = _norm_remote_path(trash_root)
    trash_fid = ensure_remote_dir(session, trash_dir)

    src_fid = resolve_remote_fid(session, src_remote_path)
    src_parent_fid = resolve_remote_fid(session, src_parent)

    # First move to trash folder, then rename to include timestamp.
    mv = move_file(session, src_fid, trash_fid, current_dir_fid=src_parent_fid)
    rn = rename_file(session, src_fid, f"{ts}_{safe_name}")
    return {"move": mv, "rename": rn, "trash": trash_dir}


def purge_trash(
    session: QuarkSession,
    trash_root: str = "/OpenClaw/.trash",
    retention_days: int = 30,
    now_ts: Optional[datetime] = None,
) -> dict[str, Any]:
    """Delete items under trash older than retention_days.

    Items are considered trash entries if name starts with 'YYYYmmdd-HHMMSS_'.
    """
    if now_ts is None:
        now_ts = datetime.now(timezone.utc)
    trash_dir = _norm_remote_path(trash_root)
    trash_fid = ensure_remote_dir(session, trash_dir)

    lst = list_folder(session, parent_id=trash_fid, size=500)
    deleted: list[dict[str, Any]] = []
    kept: int = 0

    for it in lst:
        name = str(it.get("file_name") or "")
        fid = str(it.get("fid") or "")
        if not fid:
            continue
        cutoff_ok = False
        try:
            prefix = name.split("_", 1)[0]
            dt = datetime.strptime(prefix, "%Y%m%d-%H%M%S").replace(tzinfo=timezone.utc)
            age_days = (now_ts - dt).total_seconds() / 86400.0
            cutoff_ok = age_days > float(retention_days)
        except Exception:
            cutoff_ok = False

        if cutoff_ok:
            res = delete_file(session, fid)
            deleted.append({"fid": fid, "name": name, "result": res})
        else:
            kept += 1

    return {"trash": trash_dir, "retention_days": retention_days, "deleted": deleted, "kept": kept, "total": len(lst)}


# ------------------------------
# Upload implementation (web-aligned)
# ------------------------------

class _SHA1Ctx:
    """Incremental SHA1 with exposed internal state (h0..h4, bit length).

    Used to generate Aliyun OSS `X-Oss-Hash-Ctx` (base64(JSON)).
    """

    __slots__ = ("h0", "h1", "h2", "h3", "h4", "_unprocessed", "_message_byte_length")

    def __init__(self) -> None:
        self.h0 = 0x67452301
        self.h1 = 0xEFCDAB89
        self.h2 = 0x98BADCFE
        self.h3 = 0x10325476
        self.h4 = 0xC3D2E1F0
        self._unprocessed = b""
        self._message_byte_length = 0

    @staticmethod
    def _left_rotate(n: int, b: int) -> int:
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

    def update(self, arg: bytes) -> None:
        if not arg:
            return
        self._message_byte_length += len(arg)
        arg = self._unprocessed + arg

        # Process 64-byte chunks
        for i in range(0, len(arg) - (len(arg) % 64), 64):
            self._process_chunk(arg[i : i + 64])

        self._unprocessed = arg[len(arg) - (len(arg) % 64) :]

    def _process_chunk(self, chunk: bytes) -> None:
        assert len(chunk) == 64
        w = [0] * 80
        for i in range(16):
            w[i] = int.from_bytes(chunk[i * 4 : (i + 1) * 4], "big")
        for i in range(16, 80):
            w[i] = self._left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

        a = self.h0
        b = self.h1
        c = self.h2
        d = self.h3
        e = self.h4

        for i in range(80):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (self._left_rotate(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF
            e = d
            d = c
            c = self._left_rotate(b, 30)
            b = a
            a = temp

        self.h0 = (self.h0 + a) & 0xFFFFFFFF
        self.h1 = (self.h1 + b) & 0xFFFFFFFF
        self.h2 = (self.h2 + c) & 0xFFFFFFFF
        self.h3 = (self.h3 + d) & 0xFFFFFFFF
        self.h4 = (self.h4 + e) & 0xFFFFFFFF

    def oss_hash_ctx_b64(self) -> str:
        # Aliyun OSS expects Nl/Nh as bit length low/high.
        bit_len = self._message_byte_length * 8
        nl = bit_len & 0xFFFFFFFF
        nh = (bit_len >> 32) & 0xFFFFFFFF
        payload = {
            "hash_type": "sha1",
            "h0": str(self.h0),
            "h1": str(self.h1),
            "h2": str(self.h2),
            "h3": str(self.h3),
            "h4": str(self.h4),
            "Nl": str(nl),
            "Nh": str(nh),
            "data": "",
            "num": "0",
        }
        raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        return base64.b64encode(raw).decode("ascii")


def _rfc1123_gmt_now() -> str:
    # Example: Thu, 19 Mar 2026 12:11:44 GMT
    return formatdate(timeval=None, usegmt=True)


def _build_put_auth_meta(*, mime: str, date_gmt: str, bucket: str, obj_key: str, upload_id: str, part_number: int, oss_hash_ctx_b64: str | None) -> str:
    """Build auth_meta for `file/upload/auth` (PUT part).

    Aligned with QuarkPan templates:
    - use lowercase `x-oss-hash-ctx:` in canonical string
    - mobile-ish aliyun-sdk-js UA string
    """
    lines: list[str] = []
    lines.append("PUT")
    lines.append("")
    lines.append(mime)
    lines.append(date_gmt)
    lines.append(f"x-oss-date:{date_gmt}")
    if oss_hash_ctx_b64:
        lines.append(f"x-oss-hash-ctx:{oss_hash_ctx_b64}")
    lines.append("x-oss-user-agent:aliyun-sdk-js/1.0.0 Chrome Mobile 139.0.0.0 on Google Nexus 5 (Android 6.0)")
    lines.append(f"/{bucket}/{obj_key}?partNumber={part_number}&uploadId={upload_id}")
    return "\\n".join(lines)


def _build_complete_auth_meta(*, content_md5_b64: str, date_gmt: str, bucket: str, obj_key: str, upload_id: str, callback_b64: str) -> str:
    # Aligned with QuarkPan (desktop-ish UA for complete)
    lines: list[str] = []
    lines.append("POST")
    lines.append(content_md5_b64)
    lines.append("application/xml")
    lines.append(date_gmt)
    lines.append(f"x-oss-callback:{callback_b64}")
    lines.append(f"x-oss-date:{date_gmt}")
    lines.append("x-oss-user-agent:aliyun-sdk-js/1.0.0 Chrome 139.0.0.0 on OS X 10.15.7 64-bit")
    lines.append(f"/{bucket}/{obj_key}?uploadId={upload_id}")
    return "\\n".join(lines)

def _calculate_incremental_hash_ctx(file_path: Path, part_number: int, part_size: int) -> str:
    """Best-effort implementation of QuarkPan's incremental SHA1 context.

    Quark's OSS upload auth for part 2+ may require this header.
    """

    h = hashlib.sha1()
    # Feed sha1 with previous parts' bytes (not scalable for large files, but fine for small)
    # For our use-case (backups), larger files should still work via OSS default behavior.
    with file_path.open("rb") as f:
        remaining = (part_number - 1) * part_size
        if remaining > 0:
            h.update(f.read(remaining))
    return base64.b64encode(h.digest()).decode("ascii")


# NOTE: Legacy direct OSS multipart uploader removed.
# We rely on the smaller, battle-tested implementation in quarkpan_uploader.py.
