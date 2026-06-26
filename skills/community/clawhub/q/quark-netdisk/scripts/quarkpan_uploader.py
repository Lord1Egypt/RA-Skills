"""QuarkPan-based uploader (vendored).

Goal: reuse the upload logic proven to work in https://github.com/lich0821/QuarkPan
while keeping this skill self-contained.

Notes:
- We keep the surface area minimal: an API client + multipart uploader.
- We force trust_env=False to avoid host proxy env issues (e.g. socks://127.0.0.1:7897).
- Cookies are provided as a single cookie string, exactly like QuarkPan's QuarkAPIClient.

Upstream reference:
- quark_client/core/api_client.py
- quark_client/services/file_upload_service.py

License: follow upstream project license; this file is a derived work for internal use.
"""

from __future__ import annotations

import base64
import hashlib
import json
import mimetypes
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

import httpx


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
        bit_len = self._message_byte_length * 8
        payload = {
            "hash_type": "sha1",
            "h0": str(self.h0),
            "h1": str(self.h1),
            "h2": str(self.h2),
            "h3": str(self.h3),
            "h4": str(self.h4),
            "Nl": str(bit_len),
            "Nh": "0",
            "data": "",
            "num": "0",
        }
        raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        return base64.b64encode(raw).decode("ascii")


BASE_URL = "https://drive-pc.quark.cn/1/clouddrive"
PAN_ORIGIN = "https://pan.quark.cn"


def _default_headers() -> dict[str, str]:
    # Same as QuarkPan get_default_headers()
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


@dataclass
class UploadResult:
    task_id: str
    fid: str | None
    obj_key: str | None
    md5: str
    sha1: str


class QuarkPanAPIClient:
    def __init__(self, *, cookie_string: str, timeout_s: float = 60.0):
        self.cookies = cookie_string
        self.client = httpx.Client(
            timeout=timeout_s,
            headers=_default_headers(),
            follow_redirects=True,
            trust_env=False,
        )

    def _timestamp_ms(self) -> int:
        return int(time.time() * 1000)

    def _build_params(self, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        p: dict[str, Any] = {
            "pr": "ucpro",
            "fr": "pc",
            "uc_param_str": "",
            "__t": self._timestamp_ms(),
            "__dt": 1000,
        }
        if params:
            p.update(params)
        return p

    def _build_headers(self, extra: Optional[dict[str, str]] = None) -> dict[str, str]:
        h = _default_headers().copy()
        h["cookie"] = self.cookies
        if extra:
            h.update(extra)
        return h

    def get(self, path: str, *, params: Optional[dict[str, Any]] = None, headers: Optional[dict[str, str]] = None) -> dict[str, Any]:
        url = BASE_URL + "/" + path.lstrip("/")
        r = self.client.get(url, params=self._build_params(params), headers=self._build_headers(headers))
        if r.status_code >= 400:
            raise RuntimeError(f"HTTP {r.status_code} GET {r.url} -> {r.text[:500]}")
        return r.json()

    def post(self, path: str, *, json_data: dict[str, Any], params: Optional[dict[str, Any]] = None, headers: Optional[dict[str, str]] = None) -> dict[str, Any]:
        url = BASE_URL + "/" + path.lstrip("/")
        r = self.client.post(url, params=self._build_params(params), json=json_data, headers=self._build_headers(headers))
        if r.status_code >= 400:
            raise RuntimeError(f"HTTP {r.status_code} POST {r.url} -> {r.text[:500]}")
        return r.json()


class QuarkPanUploader:
    def __init__(self, api: QuarkPanAPIClient):
        self.api = api

    @staticmethod
    def _calc_hashes(file_path: Path, progress: Optional[Callable[[int, str], None]] = None) -> tuple[str, str]:
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        size = file_path.stat().st_size
        done = 0
        with file_path.open("rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                md5.update(chunk)
                sha1.update(chunk)
                done += len(chunk)
                if progress and size:
                    # map to 0..10
                    p = min(10, int(done / size * 10))
                    progress(p, "计算文件哈希")
        return md5.hexdigest(), sha1.hexdigest()

    def _pre_upload(self, *, file_name: str, file_size: int, parent_folder_id: str, mime_type: str) -> dict[str, Any]:
        current_time = int(time.time() * 1000)
        data = {
            "ccp_hash_update": True,
            "parallel_upload": True,
            "pdir_fid": parent_folder_id,
            "dir_name": "",
            "size": file_size,
            "file_name": file_name,
            "format_type": mime_type,
            "l_updated_at": current_time,
            "l_created_at": current_time,
        }
        res = self.api.post("file/upload/pre", json_data=data)
        if not (res.get("status") in (200, 2000000) and res.get("code") in (0, 200)):
            raise RuntimeError(f"pre_upload failed: {res}")
        return res.get("data") or {}

    def _update_hash(self, *, task_id: str, md5_hex: str, sha1_hex: str) -> dict[str, Any]:
        res = self.api.post("file/update/hash", json_data={"task_id": task_id, "md5": md5_hex, "sha1": sha1_hex})
        if not (res.get("status") in (200, 2000000) and res.get("code") in (0, 200)):
            raise RuntimeError(f"update/hash failed: {res}")
        return res.get("data") or {}

    @staticmethod
    def _oss_date() -> str:
        return datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

    def _get_upload_auth(self, *, task_id: str, auth_info: str, mime_type: str, part_number: int, upload_id: str, obj_key: str, bucket: str, hash_ctx: str = "") -> tuple[str, dict[str, str]]:
        oss_date = self._oss_date()
        if hash_ctx:
            auth_meta = f"""PUT\n\n{mime_type}\n{oss_date}\nx-oss-date:{oss_date}\nx-oss-hash-ctx:{hash_ctx}\nx-oss-user-agent:aliyun-sdk-js/1.0.0 Chrome Mobile 139.0.0.0 on Google Nexus 5 (Android 6.0)\n/{bucket}/{obj_key}?partNumber={part_number}&uploadId={upload_id}"""
        else:
            auth_meta = f"""PUT\n\n{mime_type}\n{oss_date}\nx-oss-date:{oss_date}\nx-oss-user-agent:aliyun-sdk-js/1.0.0 Chrome Mobile 139.0.0.0 on Google Nexus 5 (Android 6.0)\n/{bucket}/{obj_key}?partNumber={part_number}&uploadId={upload_id}"""

        res = self.api.post("file/upload/auth", json_data={"task_id": task_id, "auth_info": auth_info, "auth_meta": auth_meta})
        if not (res.get("status") in (200, 2000000) and res.get("code") in (0, 200)):
            raise RuntimeError(f"upload/auth failed: {res}")
        auth_key = (res.get("data") or {}).get("auth_key")
        if not auth_key:
            raise RuntimeError(f"upload/auth missing auth_key: {res}")

        upload_url = f"https://{bucket}.pds.quark.cn/{obj_key}?partNumber={part_number}&uploadId={upload_id}"
        headers = {
            "Content-Type": mime_type,
            "x-oss-date": oss_date,
            "x-oss-user-agent": "aliyun-sdk-js/1.0.0 Chrome Mobile 139.0.0.0 on Google Nexus 5 (Android 6.0)",
            "authorization": auth_key,
        }
        if hash_ctx:
            headers["X-Oss-Hash-Ctx"] = hash_ctx
        return upload_url, headers

    @staticmethod
    def _read_part(file_path: Path, *, part_number: int, part_size: int) -> bytes:
        with file_path.open("rb") as f:
            f.seek((part_number - 1) * part_size)
            return f.read(part_size)

    def upload(self, *, file_path: Path, parent_folder_id: str, progress: Optional[Callable[[int, str], None]] = None) -> UploadResult:
        file_path = file_path.expanduser().resolve()
        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(str(file_path))

        file_size = file_path.stat().st_size
        file_name = file_path.name
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if not mime_type:
            mime_type = "application/octet-stream"

        if progress:
            progress(0, "计算文件哈希")
        md5_hex, sha1_hex = self._calc_hashes(file_path, progress=progress)

        if progress:
            progress(10, "发起预上传")
        pre = self._pre_upload(file_name=file_name, file_size=file_size, parent_folder_id=parent_folder_id, mime_type=mime_type)
        task_id = pre.get("task_id")
        if not task_id:
            raise RuntimeError(f"task_id missing: {pre}")

        auth_info = pre.get("auth_info", "")
        upload_id = pre.get("upload_id", "")
        obj_key = pre.get("obj_key", "")
        bucket = pre.get("bucket", "ul-sz")
        callback_info = pre.get("callback") or {}

        if not (auth_info and upload_id and obj_key and bucket):
            raise RuntimeError(f"pre missing auth_info/upload_id/obj_key/bucket: {pre}")

        if progress:
            progress(20, "更新文件哈希")
        upd = self._update_hash(task_id=task_id, md5_hex=md5_hex, sha1_hex=sha1_hex)
        if upd.get("finish") is True:
            return UploadResult(task_id=task_id, fid=upd.get("fid"), obj_key=upd.get("obj_key"), md5=md5_hex, sha1=sha1_hex)

        # multipart (>=5MB) or single part
        chunk_size = 4 * 1024 * 1024
        if file_size < 5 * 1024 * 1024:
            parts = [(1, file_size)]
        else:
            parts = []
            remaining = file_size
            part_num = 1
            while remaining > 0:
                cur = min(chunk_size, remaining)
                parts.append((part_num, cur))
                remaining -= cur
                part_num += 1

        if progress:
            progress(30, f"开始上传 {len(parts)} 个分片")

        uploaded_parts: list[tuple[int, str]] = []

        sha1ctx = _SHA1Ctx()

        with file_path.open("rb") as f:
            for i, (part_number, cur_size) in enumerate(parts):
                data = f.read(cur_size)
                if not data:
                    break

                # For part >=2, OSS requires incremental hash ctx for parallel multipart.
                hash_ctx = sha1ctx.oss_hash_ctx_b64() if part_number > 1 else ""

                if progress:
                    progress(35 + int(i * (45 / max(1, len(parts)))), f"获取分片 {part_number} 授权")

                upload_url, headers = self._get_upload_auth(
                    task_id=task_id,
                    auth_info=auth_info,
                    mime_type=mime_type,
                    part_number=part_number,
                    upload_id=upload_id,
                    obj_key=obj_key,
                    bucket=bucket,
                    hash_ctx=hash_ctx,
                )

                if progress:
                    progress(35 + int(i * (45 / max(1, len(parts)))), f"上传分片 {part_number}")

                with httpx.Client(timeout=300.0, trust_env=False) as c:
                    r = c.put(upload_url, content=data, headers=headers)
                if r.status_code >= 400:
                    raise RuntimeError(f"OSS PUT failed: {r.status_code} {r.text[:400]}")

                etag = (r.headers.get("etag") or r.headers.get("ETag") or "").strip('"')
                if not etag:
                    raise RuntimeError(f"missing ETag for part {part_number}")
                uploaded_parts.append((part_number, etag))

                sha1ctx.update(data)

        if progress:
            progress(80, "POST完成合并")

        # Build CompleteMultipartUpload XML
        xml_parts = []
        for pn, et in uploaded_parts:
            xml_parts.append(f'<Part>\n<PartNumber>{pn}</PartNumber>\n<ETag>"{et}"</ETag>\n</Part>')
        xml_data = '<?xml version="1.0" encoding="UTF-8"?>\n<CompleteMultipartUpload>\n' + "\n".join(xml_parts) + "\n</CompleteMultipartUpload>"

        # MD5 base64 for XML
        xml_md5_b64 = base64.b64encode(hashlib.md5(xml_data.encode("utf-8")).digest()).decode("ascii")

        callback_b64 = base64.b64encode(json.dumps(callback_info, separators=(",", ":")).encode("utf-8")).decode("ascii")

        oss_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

        # POST complete auth_meta (QuarkPan style)
        auth_meta = f"""POST\n{xml_md5_b64}\napplication/xml\n{oss_date}\nx-oss-callback:{callback_b64}\nx-oss-date:{oss_date}\nx-oss-user-agent:aliyun-sdk-js/1.0.0 Chrome 139.0.0.0 on OS X 10.15.7 64-bit\n/{bucket}/{obj_key}?uploadId={upload_id}"""

        res = self.api.post("file/upload/auth", json_data={"task_id": task_id, "auth_info": auth_info, "auth_meta": auth_meta})
        if not (res.get("status") in (200, 2000000) and res.get("code") in (0, 200)):
            raise RuntimeError(f"upload/auth (complete) failed: {res}")
        auth_key = (res.get("data") or {}).get("auth_key")
        if not auth_key:
            raise RuntimeError(f"upload/auth missing auth_key (complete): {res}")

        complete_url = f"https://{bucket}.pds.quark.cn/{obj_key}?uploadId={upload_id}"
        complete_headers = {
            "Content-Type": "application/xml",
            "Content-MD5": xml_md5_b64,
            "x-oss-callback": callback_b64,
            "x-oss-date": oss_date,
            "x-oss-user-agent": "aliyun-sdk-js/1.0.0 Chrome 139.0.0.0 on OS X 10.15.7 64-bit",
            "authorization": auth_key,
        }
        with httpx.Client(timeout=300.0, trust_env=False) as c:
            cr = c.post(complete_url, content=xml_data.encode("utf-8"), headers=complete_headers)
        if cr.status_code >= 400:
            raise RuntimeError(f"CompleteMultipartUpload failed: {cr.status_code} {cr.text[:400]}")

        if progress:
            progress(95, "通知夸克完成")
        fin = self.api.post("file/upload/finish", json_data={"task_id": task_id, "obj_key": obj_key})
        if not (fin.get("status") in (200, 2000000) and fin.get("code") in (0, 200)):
            raise RuntimeError(f"upload/finish failed: {fin}")

        if progress:
            progress(100, "完成")

        # fid may be in finish response
        fid = (fin.get("data") or {}).get("fid")
        return UploadResult(task_id=task_id, fid=fid, obj_key=obj_key, md5=md5_hex, sha1=sha1_hex)
