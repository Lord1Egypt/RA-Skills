#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""留学助理 skill — 引擎 API 客户端 + anon_id 管理。
- 引擎地址可用环境变量 STUDY_ENGINE_URL 覆盖
- anon_id 存 ~/.study-abroad/anon_id（首次生成），供匿名试用与进度延续
"""
from __future__ import annotations  # 注解惰性求值，兼容 Python 3.9（PEP 604 联合类型）

import json
import os
import sys
import uuid
from pathlib import Path

# 默认连生产引擎（开箱即用）；本地开发用 STUDY_ENGINE_URL=http://127.0.0.1:8100 覆盖
ENGINE_URL = os.environ.get("STUDY_ENGINE_URL", "https://compliancehub.cn")
API_PREFIX = "/api/study"   # 引擎统一前缀（本地与生产一致）；ENGINE_URL 只填引擎根
CONFIG_DIR = Path(os.environ.get("STUDY_CONFIG_DIR", Path.home() / ".study-abroad"))
ANON_FILE = CONFIG_DIR / "anon_id"
KEY_FILE = CONFIG_DIR / "api_key"   # 注册用户 API Key（0600），注册后保存

# 注册转化入口（匿名额度用尽 → 引导注册获取 API Key）
REGISTER_PAGE = "https://compliancehub.cn/account.html?skill=study-abroad-assistant"
REGISTER_GUIDE = (
    "\n🔑 匿名试用额度已用尽（画像/文书/套磁/报告共 5 次 / 7 天）。\n"
    f"注册即可继续使用，并获得 API Key 解锁注册权益（额度更高、进度保留）：\n"
    f"  1. 打开注册页: {REGISTER_PAGE}\n"
    "  2. 注册账户，获取你的 API Key（sk_ 开头）\n"
    "  3. 配置并合并匿名进度:  python3 scripts/guide.py register --key sk_xxx\n"
    "注册后自动携带 Key，匿名试用的画像/计划进度合并到你的账户。\n"
)


class ApiError(Exception):
    def __init__(self, status, body):
        self.status = status
        self.body = body
        super().__init__(f"引擎返回 {status}: {body}")


def _http():
    try:
        import httpx
        return httpx
    except ImportError:
        pass
    # 零依赖兜底：用 urllib（引擎 JSON 请求足够）
    import urllib.request  # noqa
    return None


def anon_id() -> str:
    if ANON_FILE.exists():
        return ANON_FILE.read_text().strip()
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    aid = str(uuid.uuid4())
    ANON_FILE.write_text(aid)
    return aid


def api_key() -> str | None:
    """注册用户 API Key：优先环境变量 STUDY_API_KEY，否则本地配置 KEY_FILE。"""
    k = os.environ.get("STUDY_API_KEY") or ""
    if k:
        return k.strip()
    if KEY_FILE.exists():
        k = KEY_FILE.read_text().strip()
        return k or None
    return None


def save_api_key(key: str):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    KEY_FILE.write_text(key.strip(), encoding="utf-8")
    os.chmod(KEY_FILE, 0o600)


def request(method: str, path: str, params=None, body=None) -> dict:
    """统一请求，返回解析后的 JSON（success.data）。
    一律绕过代理：引擎要么在本地、要么在服务器直连，均不需要 HTTP 代理。
    """
    url = ENGINE_URL.rstrip("/") + API_PREFIX + path
    headers = {"x-anon-id": anon_id(), "Content-Type": "application/json"}
    if api_key():
        headers["x-api-key"] = api_key()   # 注册用户身份（额度更高）
    payload = json.dumps(body, ensure_ascii=False).encode() if body is not None else None

    if _http():
        httpx = _http()
        try:
            r = httpx.request(method, url, params=params, headers=headers,
                              content=payload, timeout=20, trust_env=False)
        except httpx.ConnectError as e:
            raise ApiError(0, f"无法连接引擎 {ENGINE_URL}（{e}）。请确认引擎已启动，或设置 STUDY_ENGINE_URL。")
        try:
            data = r.json()
        except ValueError:
            raise ApiError(r.status_code, r.text[:200])
    else:
        import urllib.request
        import urllib.parse
        if params:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, data=payload, method=method, headers=headers)
        # 显式绕代理（urllib 默认会读 HTTP_PROXY 环境变量）
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        try:
            with opener.open(req, timeout=20) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            # 透传服务端 JSON detail（如 QUOTA 403）
            try:
                err_body = json.loads(e.read().decode())
                detail = err_body.get("detail") or err_body.get("error") or str(e)
                if isinstance(detail, dict):
                    detail = detail.get("message", json.dumps(detail, ensure_ascii=False))
            except Exception:
                detail = str(e)
            raise ApiError(e.code, detail)
        except Exception as e:
            raise ApiError(0, str(e))

    if "success" not in data:
        if "detail" in data:  # FastAPI HTTPException 格式（如 QUOTA 403）
            d = data["detail"]
            if isinstance(d, dict):
                raise ApiError(r.status_code if _http() else 500,
                               d.get("message", json.dumps(d, ensure_ascii=False)))
            raise ApiError(r.status_code if _http() else 500, str(d))
        return data  # 非包裹响应（如 /health）
    if not data.get("success"):
        err = data.get("error") or {}
        detail = err.get("message", err if isinstance(err, str) else json.dumps(err, ensure_ascii=False))
        raise ApiError(r.status_code if _http() else 500, detail)
    return data["data"]


# ---- 便捷封装 ----

def assess(profile: dict) -> dict:
    return request("POST", "/assess", body=profile)


def schools(**kw) -> dict:
    return request("GET", "/schools", params=kw)


def professors(**kw) -> dict:
    clean = {k: v for k, v in kw.items() if v is not None}
    return request("GET", "/professors", params=clean)


def feedback(doc_type: str, paragraph: str, context=None) -> dict:
    return request("POST", "/doc/feedback",
                   body={"type": doc_type, "paragraph": paragraph, "context": context})


def outreach(mode: str, professor: dict, sender: dict = None) -> dict:
    return request("POST", "/outreach/draft",
                   body={"mode": mode, "professor": professor, "sender": sender or {}})


def report(report_type: str, payload: dict) -> dict:
    return request("POST", "/report", body={"type": report_type, "payload": payload})


def plan_generate(profile: dict, season=None, degree=None) -> dict:
    return request("POST", "/plan/generate",
                   body={"profile": profile, "season": season, "degree": degree})


def plan_get(season=None) -> dict:
    return request("GET", "/plan", params={"season": season} if season else None)


def plan_task(season: str, task_id: str, status: str) -> dict:
    return request("PATCH", "/plan/task",
                   body={"season": season, "taskId": task_id, "status": status})


def apps_list() -> dict:
    return request("GET", "/applications")


def apps_add(item: dict) -> dict:
    return request("POST", "/applications", body=item)


def apps_update(app_id: str, fields: dict) -> dict:
    return request("PATCH", f"/applications/{app_id}", body=fields)


def apps_delete(app_id: str) -> dict:
    return request("DELETE", f"/applications/{app_id}")


def merge(anon_id_to_merge: str) -> dict:
    """注册用户合并匿名进度（需已配置 STUDY_API_KEY/本机 api_key）。"""
    return request("POST", "/merge", body={"anonId": anon_id_to_merge})


def profile_get() -> dict:
    return request("GET", "/profile")


def profile_update(fields: dict) -> dict:
    return request("POST", "/profile", body=fields)


if __name__ == "__main__":
    # 冒烟：用业务端点探测（/health 仅本地引擎有，生产 nginx 只暴露 /api/study/*）
    try:
        d = request("GET", "/schools", params={"mode": "framework"})
        print(f"引擎正常（framework {len(d['items'])} 示例）")
        print(f"anon_id: {anon_id()}")
    except ApiError as e:
        print(f"引擎不可达: {e}", file=sys.stderr)
        sys.exit(1)
