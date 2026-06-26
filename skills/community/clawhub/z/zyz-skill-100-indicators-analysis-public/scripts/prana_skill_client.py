#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prana 封装技能 — 薄客户端（无业务逻辑，仅负责与 Prana 服务通信）
从 GitHub / Claw Hub 等下载本技能包后，通过本脚本将用户输入转发到 Prana 执行真实能力。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import uuid
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlencode

# 技能根目录（本脚本位于 scripts/ 下）
SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = SKILL_ROOT / "config"
API_KEY_FILE = CONFIG_DIR / "api_key.txt"
API_KEY_JSON_FILE = CONFIG_DIR / "api_key.json"
SKILL_MD_FILE = SKILL_ROOT / "SKILL.md"

DEFAULT_PRANA_BASE = os.environ.get("NEXT_PUBLIC_URL", "https://www.prana.chat/")

# agent-run 为长连接场景；超时或失败后改查 agent-result（同一 request_id）
HTTP_TIMEOUT_SEC = 120
# 自动拉取 API key（GET /api/v1/api-keys）超时
API_KEYS_FETCH_TIMEOUT_SEC = 60

# 模板目录下与本脚本同级的 mock JSON（与 GET /api/v1/api-keys/、POST /api/claw/agent-run 响应结构一致）
_TEMPLATES_DIR = Path(__file__).resolve().parent
MOCK_API_KEYS_JSON = _TEMPLATES_DIR / "mock_prana_api_keys.json"
MOCK_AGENT_RUN_JSON = _TEMPLATES_DIR / "mock_prana_agent_run.json"


def _is_mock_mode() -> bool:
    """PRANA_SKILL_MOCK=1|true|yes 时跳过网络，使用 mock_prana_*.json 或内置占位。"""
    v = os.environ.get("PRANA_SKILL_MOCK", "").strip().lower()
    return v in ("1", "true", "yes", "on")


def _auto_fetch_api_key_disabled() -> bool:
    """PRANA_SKILL_NO_AUTO_API_KEY=1 时不在本地缺省时自动请求 create_key 接口。"""
    v = os.environ.get("PRANA_SKILL_NO_AUTO_API_KEY", "").strip().lower()
    return v in ("1", "true", "yes", "on")


def _skip_write_fetched_api_key() -> bool:
    """PRANA_SKILL_SKIP_WRITE_API_KEY=1 时不把接口拉取的 key 写入磁盘（默认会写入 config/api_key.txt）。"""
    v = os.environ.get("PRANA_SKILL_SKIP_WRITE_API_KEY", "").strip().lower()
    return v in ("1", "true", "yes", "on")


def _load_mock_json(path: Path, fallback: dict) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass
    return dict(fallback)


def _mock_credentials_from_file() -> Tuple[str, str]:
    raw = _load_mock_json(
        MOCK_API_KEYS_JSON,
        {
            "code": 200,
            "message": "success",
            "data": {
                "account_id": "00000000-0000-4000-8000-000000000001",
                "api_key": {
                    "public_key": "pk_mock_prana_skill_localdev",
                    "secret_key": "sk_mock_prana_skill_localdev",
                },
            },
        },
    )
    parsed = _parse_credentials_json(json.dumps(raw, ensure_ascii=False))
    if parsed:
        return parsed
    return "pk_mock_prana_skill_localdev", "sk_mock_prana_skill_localdev"


def _mock_agent_run_response(request_id: str) -> dict:
    base = _load_mock_json(
        MOCK_AGENT_RUN_JSON,
        {
            "code": 200,
            "message": "success",
            "data": {
                "thread_id": "00000000-0000-4000-8000-0000000000aa",
                "status": "completed",
                "content": "[MOCK] agent-run 模拟结果",
            },
        },
    )
    out = dict(base)
    data = out.get("data")
    if isinstance(data, dict):
        d = dict(data)
        d["_mock_request_id"] = request_id
        out["data"] = d
    else:
        out["_mock_request_id"] = request_id
    out["_mock"] = True
    return out


def _extract_frontmatter(content: str) -> Tuple[Optional[Dict[str, Any]], str]:
    if not content.strip().startswith("---"):
        return None, content
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if not match:
        return None, content
    try:
        import yaml

        fm = yaml.safe_load(match.group(1))
        return (fm if isinstance(fm, dict) else None), match.group(2)
    except Exception:
        return None, content


def load_skill_config() -> Dict[str, Any]:
    """
    从技能包根目录 SKILL.md 的 YAML frontmatter 读取配置。
    - original_skill_key：Prana 上实际执行的专业技能（agent-run body 使用）。
    - skill_key：公开包标识（一般为 源 key + _public）；若缺 original_skill_key 则回退仅用 skill_key（旧包）。
    """
    if not SKILL_MD_FILE.exists():
        print(
            "错误: 未找到 SKILL.md，请使用完整封装技能包解压后运行。",
            file=sys.stderr,
        )
        sys.exit(1)
    raw = SKILL_MD_FILE.read_text(encoding="utf-8")
    frontmatter, _ = _extract_frontmatter(raw)
    if not frontmatter:
        print("错误: SKILL.md 缺少有效的 YAML frontmatter。", file=sys.stderr)
        sys.exit(1)
    original = str(frontmatter.get("original_skill_key") or "").strip()
    pub = str(frontmatter.get("skill_key") or "").strip()
    # 调用远端：优先 original_skill_key；兼容旧包仅含 skill_key（且为源 key）
    sk = original if original else pub
    if not sk:
        print(
            "错误: SKILL.md frontmatter 需包含 original_skill_key 与 skill_key（或旧包仅 skill_key）。",
            file=sys.stderr,
        )
        sys.exit(1)
    sip = ""
    for key in ("input_format", "input_schema", "params"):
        v = frontmatter.get(key)
        if v is not None and str(v).strip():
            sip = str(v).strip()[:16000]
            break
    if not sip:
        d = frontmatter.get("description")
        if d is not None and str(d).strip():
            sip = str(d).strip()[:8000]
    return {"skill_key": sk, "skill_invocation_params": sip}


def _parse_credentials_json(text: str) -> Optional[Tuple[str, str]]:
    """解析 GET /api/v1/api-keys/ 完整响应，或仅含 public_key / secret_key 的 JSON。"""
    t = text.strip()
    if not t.startswith("{"):
        return None
    try:
        obj = json.loads(t)
    except json.JSONDecodeError:
        return None
    if not isinstance(obj, dict):
        return None
    data = obj.get("data")
    ak = None
    if isinstance(data, dict):
        ak = data.get("api_key")
    if isinstance(ak, dict) and ak.get("public_key") and ak.get("secret_key"):
        return str(ak["public_key"]).strip(), str(ak["secret_key"]).strip()
    ak = obj.get("api_key")
    if isinstance(ak, dict) and ak.get("public_key") and ak.get("secret_key"):
        return str(ak["public_key"]).strip(), str(ak["secret_key"]).strip()
    if obj.get("public_key") and obj.get("secret_key"):
        return str(obj["public_key"]).strip(), str(obj["secret_key"]).strip()
    return None


def _parse_credentials_line(line: str) -> Optional[Tuple[str, str]]:
    """单行 public_key:secret_key（取首个冒号分割，避免密钥中含冒号时误拆）。"""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if ":" not in line:
        return None
    pub, _, sec = line.partition(":")
    pub, sec = pub.strip(), sec.strip()
    if pub and sec:
        return pub, sec
    return None


def _headers_x_api_key(public_key: str, secret_key: str) -> dict[str, str]:
    """Claw 接口要求：x-api-key 为 public_key:secret_key。"""
    return {
        "Content-Type": "application/json",
        "x-api-key": f"{public_key}:{secret_key}",
    }


def _build_api_keys_fetch_url(base_url: str) -> str:
    """
    组装 GET /api/v1/api-keys 完整 URL。
    查询参数（与 Prana 服务端一致）：account_id、email、phone_number；均可从环境变量注入。
    若全无则服务端会为随机新用户签发 key（见 api_keys_api.get_api_keys）。
    """
    root = base_url.rstrip("/")
    path = f"{root}/api/v1/api-keys"
    q: Dict[str, str] = {}
    aid = (os.environ.get("ACCOUNT_ID") or os.environ.get("PRANA_ACCOUNT_ID") or "").strip()
    if aid:
        q["account_id"] = aid
    email = (os.environ.get("PRANA_API_KEYS_EMAIL") or os.environ.get("EMAIL") or "").strip()
    if email:
        q["email"] = email
    phone = (
        os.environ.get("PHONE_NUMBER")
        or os.environ.get("PRANA_PHONE")
        or os.environ.get("phone_number")
        or ""
    ).strip()
    if phone:
        q["phone_number"] = phone
    if q:
        path = f"{path}?{urlencode(q)}"
    return path


def fetch_prana_api_keys_via_get(base_url: str) -> Optional[Tuple[str, str]]:
    """
    调用 Prana GET /api/v1/api-keys（无需 JWT），解析 data.api_key 的 public_key、secret_key。
    """
    url = _build_api_keys_fetch_url(base_url)
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=API_KEYS_FETCH_TIMEOUT_SEC) as resp:
            text = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        print(
            f"错误: 自动获取 API key 失败（HTTP {e.code}）：{err[:2000]}",
            file=sys.stderr,
        )
        return None
    except urllib.error.URLError as e:
        print(f"错误: 自动获取 API key 失败（网络）：{e.reason}", file=sys.stderr)
        return None
    except TimeoutError:
        print("错误: 自动获取 API key 超时。", file=sys.stderr)
        return None
    parsed = _parse_credentials_json(text)
    if not parsed:
        print(
            "错误: 自动获取 API key 成功但响应无法解析出 public_key/secret_key。",
            file=sys.stderr,
        )
        return None
    return parsed


def _persist_fetched_api_key_txt(public_key: str, secret_key: str) -> None:
    """将 public_key:secret_key 写入 config/api_key.txt（首行为注释，与现有读取逻辑兼容）。"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Auto-saved by prana_skill_client after GET /api/v1/api-keys; do not commit to public repos.",
        f"{public_key}:{secret_key}",
        "",
    ]
    API_KEY_FILE.write_text("\n".join(lines), encoding="utf-8")


def _persist_fetched_api_key_json(public_key: str, secret_key: str) -> None:
    """PRANA_SKILL_PERSIST_FETCHED_KEY=1 时额外写入 config/api_key.json（完整 API 响应形状）。"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "code": 200,
        "message": "success",
        "data": {"api_key": {"public_key": public_key, "secret_key": secret_key}},
    }
    API_KEY_JSON_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def load_prana_credentials(prana_base_url: Optional[str] = None) -> Tuple[str, str]:
    """
    从环境变量或配置文件读取 public_key、secret_key（来自 GET /api/v1/api-keys/ 返回的 data.api_key）。
    获取 Key 时可选查询参数 account_id；沙盒可从环境变量 ACCOUNT_ID 传入，无则省略。
    若设置 PRANA_SKILL_MOCK=1，不访问网络，使用 mock_prana_api_keys.json（或内置占位）模拟 GET /api/v1/api-keys/。
    若以上皆无且未禁止自动拉取，则对 Prana 发起 GET /api/v1/api-keys（见 _build_api_keys_fetch_url）。
    优先级：
      PRANA_SKILL_MOCK（为真时仅走 mock）
      PRANA_SKILL_PUBLIC_KEY + PRANA_SKILL_SECRET_KEY
      PRANA_SKILL_API_KEY（整段 JSON，或单行 public_key:secret_key）
      config/api_key.json
      config/api_key.txt（JSON 或单行 public_key:secret_key）
      GET /api/v1/api-keys（需可达的 base_url；成功后默认写入 config/api_key.txt）
    """
    if _is_mock_mode():
        return _mock_credentials_from_file()

    pk = os.environ.get("PRANA_SKILL_PUBLIC_KEY", "").strip()
    sk = os.environ.get("PRANA_SKILL_SECRET_KEY", "").strip()
    if pk and sk:
        return pk, sk

    raw = os.environ.get("PRANA_SKILL_API_KEY", "").strip()
    if raw:
        parsed = _parse_credentials_json(raw)
        if parsed:
            return parsed
        p = _parse_credentials_line(raw)
        if p:
            return p

    if API_KEY_JSON_FILE.exists():
        parsed = _parse_credentials_json(API_KEY_JSON_FILE.read_text(encoding="utf-8"))
        if parsed:
            return parsed

    if API_KEY_FILE.exists():
        txt = API_KEY_FILE.read_text(encoding="utf-8")
        lines = [ln for ln in txt.splitlines() if ln.strip() and not ln.strip().startswith("#")]
        joined = "\n".join(lines).strip()
        if joined:
            parsed = _parse_credentials_json(joined)
            if parsed:
                return parsed
            for line in lines:
                p = _parse_credentials_line(line)
                if p:
                    return p

    base = (prana_base_url or os.environ.get("NEXT_PUBLIC_URL") or DEFAULT_PRANA_BASE or "").strip()
    if base and not _is_mock_mode() and not _auto_fetch_api_key_disabled():
        fetched = fetch_prana_api_keys_via_get(base)
        if fetched:
            pub, sec = fetched
            if not _skip_write_fetched_api_key():
                try:
                    _persist_fetched_api_key_txt(pub, sec)
                except OSError as e:
                    print(f"警告: 无法写入 config/api_key.txt：{e}", file=sys.stderr)
            also_json = os.environ.get("PRANA_SKILL_PERSIST_FETCHED_KEY", "").strip().lower()
            if also_json in ("1", "true", "yes", "on"):
                try:
                    _persist_fetched_api_key_json(pub, sec)
                except OSError as e:
                    print(f"警告: 无法写入 config/api_key.json：{e}", file=sys.stderr)
            return pub, sec

    print(
        "错误: 未配置 API 凭证（public_key + secret_key），且自动 GET /api/v1/api-keys 失败或未启用。\n"
        "  可选方式：\n"
        "  1) 设置 PRANA_SKILL_PUBLIC_KEY + PRANA_SKILL_SECRET_KEY，或 PRANA_SKILL_API_KEY；或写入 config/api_key.json / api_key.txt。\n"
        "  2) 保证 --base-url（或 NEXT_PUBLIC_URL）可访问，并确保未设置 PRANA_SKILL_NO_AUTO_API_KEY；"
        "可选 ACCOUNT_ID / EMAIL / PHONE_NUMBER 作为创建 key 的查询参数；成功后默认写入 config/api_key.txt（"
        "若不想写盘可设 PRANA_SKILL_SKIP_WRITE_API_KEY=1）。\n"
        "  3) 仅离线调试可设 PRANA_SKILL_MOCK=1。",
        file=sys.stderr,
    )
    sys.exit(2)


def build_invoke_content(cfg: dict, user_message: str) -> str:
    """
    组装请求 question：参数说明 + 用户消息。
    skill_key 来自 SKILL.md frontmatter，由调用方单独传入 HTTP body。
    """
    params_from_skill = (cfg.get("skill_invocation_params") or "").strip()
    lines = [
        f"参数：{params_from_skill}",
        f"用户消息：{user_message}",
    ]
    return "\n".join(lines)


def fetch_agent_result(
    base_url: str,
    request_id: str,
    public_key: str,
    secret_key: str,
) -> dict:
    """
    当 agent-run 超时或失败时，用同一 request_id 查询运行结果。
    POST /api/claw/agent-result  body: request_id（鉴权见 x-api-key）
    Header: x-api-key: public_key:secret_key
    """
    if _is_mock_mode():
        d = _mock_agent_run_response(request_id)
        d["_from"] = "agent-result"
        return d

    url = base_url.rstrip("/") + "/api/claw/agent-result"
    body = {"request_id": request_id}
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers=_headers_x_api_key(public_key, secret_key),
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SEC) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(err_body)
        except json.JSONDecodeError:
            return {
                "error": True,
                "status": e.code,
                "detail": err_body,
                "_from": "agent-result",
            }
    except urllib.error.URLError as e:
        return {"error": True, "detail": str(e.reason), "_from": "agent-result"}


def _mark_recovered(d: dict) -> dict:
    d = dict(d)
    d["_recovered_via"] = "agent-result"
    return d


def invoke_prana(
    base_url: str,
    skill_key: str,
    content: str,
    thread_id: str | None,
    request_id: str,
    public_key: str,
    secret_key: str,
) -> dict:
    """
    调用 Prana 技能执行接口。
    body: skill_key, question, thread_id, request_id（不含 api_key）
    Header: x-api-key: public_key:secret_key
    若 HTTP 超时、连接失败，或网关类错误（5xx / 408 / 504），则改调 agent-result 用 request_id 取结果。
    若设置 PRANA_SKILL_MOCK=1，不访问网络，返回 mock_prana_agent_run.json（模拟 POST /api/claw/agent-run）。
    """
    if _is_mock_mode():
        return _mock_agent_run_response(request_id)

    url = base_url.rstrip("/") + "/api/claw/agent-run"
    body = {
        "skill_key": skill_key,
        "question": content,
        "thread_id": thread_id or "",
        "request_id": request_id,
    }
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers=_headers_x_api_key(public_key, secret_key),
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SEC) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except json.JSONDecodeError:
        return _mark_recovered(fetch_agent_result(base_url, request_id, public_key, secret_key))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        # 网关/服务端错误或超时类状态：任务可能已在服务端执行，改查 agent-result
        if e.code >= 500 or e.code in (408, 504):
            return _mark_recovered(fetch_agent_result(base_url, request_id, public_key, secret_key))
        try:
            return json.loads(err_body)
        except json.JSONDecodeError:
            return {"error": True, "status": e.code, "detail": err_body}
    except urllib.error.URLError:
        # 含连接失败、DNS、超时等
        return _mark_recovered(fetch_agent_result(base_url, request_id, public_key, secret_key))
    except TimeoutError:
        return _mark_recovered(fetch_agent_result(base_url, request_id, public_key, secret_key))


def main() -> None:
    parser = argparse.ArgumentParser(description="调用 Prana 远程技能服务")
    parser.add_argument("--message", "-m", required=True, help="用户消息 / 任务描述")
    parser.add_argument("--thread-id", "-t", default="", help="对话 thread_id，首轮可留空")
    parser.add_argument("--base-url", "-b", default=DEFAULT_PRANA_BASE, help="Prana API 根地址")
    args = parser.parse_args()

    cfg = load_skill_config()
    skill_key = cfg.get("skill_key") or ""
    if not skill_key:
        print("错误: 配置中缺少远端 skill_key（请检查 SKILL.md 的 original_skill_key）", file=sys.stderr)
        sys.exit(1)

    public_key, secret_key = load_prana_credentials(args.base_url)
    request_id = str(uuid.uuid4())
    content = build_invoke_content(cfg, args.message)
    result = invoke_prana(
        args.base_url,
        skill_key,
        content,
        args.thread_id or None,
        request_id,
        public_key,
        secret_key,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
