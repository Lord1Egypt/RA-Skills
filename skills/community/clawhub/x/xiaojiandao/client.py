from __future__ import annotations

import json
import time
import os
import uuid
import platform
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, Iterator

try:
    import requests
except ImportError:
    requests = None

from crypto import AesContext

def default_device_info(*, pkgname: str, appid: int = 1001, api_vn: int = 1) -> Dict[str, Any]:
    sys_name = platform.system().lower()
    os_name = "macos" if sys_name == "darwin" else ("windows" if sys_name.startswith("win") else sys_name)
    os_version = platform.version()
    arch = platform.machine() or "unknown"
    return {
        "app_os": f"{os_name} {os_version}",
        "app_vn": "1.0.0",
        "appid": appid,
        "pkg_name": pkgname,
        "mac": "00:00:00:00:00:00",
        "arch": arch,
        "cpu_model": platform.processor() or "Generic CPU",
        "api_vn": api_vn,
        "cl": "official",
        "device_id": str(uuid.uuid4()),
    }

@dataclass
class HookHttpClient:
    base_url: str
    pkgname: str
    appsecret: str
    appid: int = 1001
    api_vn: int = 1
    timeout_s: int = 60
    device_info: Optional[Dict[str, Any]] = field(default=None)
    _session: requests.Session = field(default_factory=lambda: requests.Session() if requests else None, init=False)

    def _aes(self) -> AesContext:
        return AesContext(pkgname=self.pkgname)

    def _build_headers(self, *, unix_ms: int, device: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        aes = self._aes()
        device_info = device or self.device_info or default_device_info(
            pkgname=self.pkgname, appid=self.appid, api_vn=self.api_vn
        )
        device_json = json.dumps(device_info, ensure_ascii=False, separators=(",", ":"))
        encrypted_device = aes.encrypt_to_base64(device_json, unix_ms=unix_ms)
        return {
            "Content-Type": "application/x-aes-ms-txt",
            "pkgname": self.pkgname,
            "device": encrypted_device,
            "appsecret": self.appsecret,
            "X-API-Token": self.appsecret,
            "x-ms-at": str(unix_ms),
        }

    def post(self, endpoint: str, payload: Any) -> Dict[str, Any]:
        if requests is None:
            raise RuntimeError("Missing dependency: pip install requests")

        unix_ms = int(time.time() * 1000)
        aes = self._aes()
        headers = self._build_headers(unix_ms=unix_ms)

        if payload is None:
            body_plain = "null"
        elif isinstance(payload, str):
            body_plain = payload
        else:
            body_plain = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))

        body_enc = aes.encrypt_to_base64(body_plain, unix_ms=unix_ms)
        url = self.base_url.rstrip("/") + (endpoint if endpoint.startswith("/") else f"/{endpoint}")
        
        try:
            resp = self._session.post(url, data=body_enc.encode("utf-8"), headers=headers, timeout=self.timeout_s)
        except Exception as e:
            return {"err_code": 500, "err_message": f"Network Error: {str(e)}", "data": None}

        if resp.status_code != 200:
            return {"err_code": resp.status_code, "err_message": resp.text, "data": None}

        lower_headers = {str(k).lower(): v for k, v in resp.headers.items()}
        resp_unix_ms = unix_ms
        if "x-ms-at" in lower_headers:
            try:
                resp_unix_ms = int(str(lower_headers["x-ms-at"]))
            except:
                pass

        try:
            decrypted = aes.decrypt_base64(resp.text, unix_ms=resp_unix_ms)
            # 处理解密后可能存在的非 JSON 干扰
            try:
                return json.loads(decrypted)
            except:
                start = decrypted.find("{")
                end = decrypted.rfind("}")
                if start != -1 and end != -1:
                    return json.loads(decrypted[start:end+1])
                raise
        except Exception:
            try:
                return resp.json()
            except:
                return {"err_code": -1, "err_message": "success", "data": resp.text}

    def stream_post(self, url: str, payload: Any, headers: Dict[str, str] = None) -> Iterator[Dict[str, Any]]:
        if headers is None:
            headers = {"Content-Type": "application/json"}
        resp = self._session.post(url, json=payload, headers=headers, timeout=None, stream=True)
        for line in resp.iter_lines():
            if line:
                line_str = line.decode("utf-8")
                if line_str.startswith("data: "):
                    try:
                        yield json.loads(line_str[6:])
                    except:
                        yield {"raw": line_str}
                else:
                    try:
                        yield json.loads(line_str)
                    except:
                        yield {"raw": line_str}

    def poll_task(self, query_endpoint: str, task_id: Any, interval: int = 2, timeout: int = 300, id_field: str = "task_id") -> Dict[str, Any]:
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self.post(query_endpoint, {id_field: task_id})
            # 适配嵌套的 state 结构
            data = result.get("data", {})
            st = result.get("state")
            if st is None and isinstance(data, dict):
                st = data.get("state")
            
            if st == 2:
                return result
            if st == 3:
                return {"err_code": 500, "err_message": f"Task Failed: {result}", "data": result}
            time.sleep(interval)
        return {"err_code": 504, "err_message": "Polling Timeout", "data": None}
