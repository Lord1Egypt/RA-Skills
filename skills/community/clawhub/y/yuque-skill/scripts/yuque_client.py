#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语雀(Yuque)开放API的轻量Python客户端。

* 优先从环境变量 YUQUE_TOKEN 读取凭证;若没有,则回退到 ~/.yuque/config.json。
* 统一封装 GET/POST/PUT/DELETE,内置JSON解析、错误归一化与429退避。
* 仅依赖标准库(urllib),零额外安装,适合 Openclaw / Claude Code 的沙箱环境。

CLI示例:
    python yuque_client.py whoami
    python yuque_client.py raw GET /users/<login>/repos
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib import error, parse, request

DEFAULT_BASE_URL = "https://www.yuque.com/api/v2"
USER_AGENT = "openclaw-yuque-skill/1.0"
CONFIG_PATH = Path.home() / ".yuque" / "config.json"


class YuqueError(Exception):
    """所有语雀API失败统一抛此异常,带status与payload便于上层定位。"""

    def __init__(self, status: int, message: str, payload: Any = None):
        super().__init__(f"[{status}] {message}")
        self.status = status
        self.payload = payload


def _load_credentials() -> Tuple[str, str]:
    """返回 (token, base_url)。环境变量优先,然后是配置文件。"""
    token = os.environ.get("YUQUE_TOKEN", "").strip()
    base_url = os.environ.get("YUQUE_BASE_URL", "").strip() or DEFAULT_BASE_URL

    if not token and CONFIG_PATH.is_file():
        try:
            cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            token = (cfg.get("token") or "").strip()
            if cfg.get("base_url"):
                base_url = cfg["base_url"].strip()
        except (json.JSONDecodeError, OSError) as exc:
            raise YuqueError(0, f"读取配置文件 {CONFIG_PATH} 失败: {exc}")

    if not token:
        raise YuqueError(
            0,
            "未找到语雀Token。请设置环境变量 YUQUE_TOKEN,或在 "
            f"{CONFIG_PATH} 中写入 {{\"token\": \"...\"}}。"
            "Token可在 https://www.yuque.com/settings/tokens 创建。",
        )
    return token, base_url.rstrip("/")


class YuqueClient:
    """语雀v2 API客户端。所有方法返回解析后的JSON dict。"""

    def __init__(self, token: Optional[str] = None, base_url: Optional[str] = None):
        if token is None or base_url is None:
            t, b = _load_credentials()
            token = token or t
            base_url = base_url or b
        self.token = token
        self.base_url = base_url.rstrip("/")

    # ---------- 低层HTTP ----------

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        retry: int = 3,
    ) -> Dict[str, Any]:
        if not path.startswith("/"):
            path = "/" + path
        url = self.base_url + path
        if params:
            # 过滤None,避免空查询串
            qs = {k: v for k, v in params.items() if v is not None}
            if qs:
                url += "?" + parse.urlencode(qs, doseq=True)

        data: Optional[bytes] = None
        headers = {
            "X-Auth-Token": self.token,
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        }
        if body is not None:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = request.Request(url, data=data, method=method.upper(), headers=headers)
        attempt = 0
        while True:
            attempt += 1
            try:
                with request.urlopen(req, timeout=30) as resp:
                    raw = resp.read()
                    if not raw:
                        return {}
                    try:
                        return json.loads(raw.decode("utf-8"))
                    except json.JSONDecodeError:
                        return {"_raw": raw.decode("utf-8", "replace")}
            except error.HTTPError as e:
                payload: Any = None
                try:
                    payload = json.loads(e.read().decode("utf-8"))
                except Exception:
                    pass
                # 429 / 5xx 退避重试
                if e.code in (429, 500, 502, 503, 504) and attempt < retry:
                    time.sleep(min(8, 2 ** attempt))
                    continue
                msg = (
                    payload.get("message")
                    if isinstance(payload, dict) and payload.get("message")
                    else e.reason or "HTTP error"
                )
                raise YuqueError(e.code, str(msg), payload)
            except error.URLError as e:
                if attempt < retry:
                    time.sleep(min(8, 2 ** attempt))
                    continue
                raise YuqueError(0, f"网络错误: {e.reason}")

    # ---------- 高层快捷方法 ----------

    def get(self, path, **params):
        return self._request("GET", path, params=params or None)

    def post(self, path, body):
        return self._request("POST", path, body=body)

    def put(self, path, body):
        return self._request("PUT", path, body=body)

    def delete(self, path, **params):
        return self._request("DELETE", path, params=params or None)

    # ---------- 业务封装(被其他脚本复用) ----------

    def whoami(self) -> Dict[str, Any]:
        return self.get("/user").get("data", {})

    def list_user_repos(self, login: str) -> list:
        return self.get(f"/users/{login}/repos").get("data", [])

    def list_group_repos(self, group: str) -> list:
        return self.get(f"/groups/{group}/repos").get("data", [])

    def list_docs(self, namespace: str) -> list:
        # 语雀单页最多100条,需要分页
        results, offset = [], 0
        while True:
            page = self.get(f"/repos/{namespace}/docs", limit=100, offset=offset).get("data", [])
            if not page:
                break
            results.extend(page)
            if len(page) < 100:
                break
            offset += 100
        return results

    def get_doc(self, namespace: str, slug_or_id: str, raw: bool = True) -> Dict[str, Any]:
        return self.get(f"/repos/{namespace}/docs/{slug_or_id}", raw=1 if raw else 0).get("data", {})

    def create_doc(self, namespace: str, **fields) -> Dict[str, Any]:
        return self.post(f"/repos/{namespace}/docs", fields).get("data", {})

    def update_doc(self, namespace: str, doc_id: int, **fields) -> Dict[str, Any]:
        return self.put(f"/repos/{namespace}/docs/{doc_id}", fields).get("data", {})

    def delete_doc(self, namespace: str, doc_id: int) -> Dict[str, Any]:
        return self.delete(f"/repos/{namespace}/docs/{doc_id}").get("data", {})

    def get_toc(self, namespace: str) -> list:
        return self.get(f"/repos/{namespace}/toc").get("data", [])

    def update_toc(self, namespace: str, body: Dict[str, Any]) -> Any:
        # 语雀TOC接口接受单个action对象或action列表(取决于版本);此处统一PUT
        return self.put(f"/repos/{namespace}/toc", body).get("data", [])

    def search(self, q: str, **params) -> list:
        params["q"] = q
        return self.get("/search", **params).get("data", [])


# ---------- CLI入口(主要用于自检与调试) ----------

def _cli(argv=None) -> int:
    p = argparse.ArgumentParser(prog="yuque_client", description="语雀API低层调用工具")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("whoami", help="返回当前Token对应的用户")

    raw = sub.add_parser("raw", help="发任意HTTP请求")
    raw.add_argument("method", choices=["GET", "POST", "PUT", "DELETE"])
    raw.add_argument("path", help="API路径,如 /users/me")
    raw.add_argument("--body", help="JSON字符串作为请求体", default=None)

    args = p.parse_args(argv)
    try:
        client = YuqueClient()
        if args.cmd == "whoami":
            data = client.whoami()
        else:
            body = json.loads(args.body) if args.body else None
            data = client._request(args.method, args.path, body=body)
        json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except YuqueError as e:
        print(json.dumps({"error": str(e), "status": e.status, "payload": e.payload},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(_cli())
