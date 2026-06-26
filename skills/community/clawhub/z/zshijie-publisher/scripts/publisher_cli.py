#!/usr/bin/env python3

import argparse
import base64
import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional
from urllib import error, parse, request

PLACEHOLDER_RE = re.compile(r"{{\s*([^{}]+?)\s*}}")
ABSOLUTE_URL_RE = re.compile(r"^https?://", re.IGNORECASE)
DEFAULT_SESSION_PATH = Path(tempfile.gettempdir()) / "openclaw-zshijie-publisher-session.json"
DEFAULT_QR_HTML_PATH = Path(tempfile.gettempdir()) / "openclaw-zshijie-login.html"
DEFAULT_QR_PNG_PATH = Path(tempfile.gettempdir()) / "openclaw-zshijie-login.png"
DEFAULT_CONTRACT_PATH = Path(__file__).resolve().parents[1] / "references" / "zshijie-api.json"
QRCODE_ASSET_PATH = Path(__file__).resolve().parents[1] / "assets" / "qrcode.min.js"
FIXED_SOURCE_VALUE = "openclaw"

OPERATION_ALIASES = {
    "publish-article": "publish_article",
    "edit-article": "edit_article",
    "publish-video": "publish_video",
    "edit-video": "edit_video",
}

SESSION_KEY_CANDIDATES = (
    "sessionId",
    "session_id",
    "sessionid",
    "jsessionid",
    "creativebrain-sessionid",
)
COOKIE_NAME_CANDIDATES = ("sessionId", "creativebrain-sessionid")
USER_KEY_GROUPS = {
    "uuid": ("uuid",),
    "userId": ("userId", "user_id", "uid"),
    "mobile": ("mobile",),
}
ARTICLE_ID_PATHS = (
    "data.ugc.shortArticle.data.article_id",
    "data.ugc.video.data.article_id",
)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"[ERROR] JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"[ERROR] Invalid JSON in {path}: {exc}") from exc


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def merge_dicts(base: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in incoming.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def parse_scalar(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def parse_values(items: list[str]) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"[ERROR] Invalid --value '{item}'. Use key=value.")
        key, raw = item.split("=", 1)
        key = key.strip()
        if not key:
            raise SystemExit(f"[ERROR] Invalid --value '{item}'. Key is empty.")
        values[key] = parse_scalar(raw.strip())
    return values


def get_path(data: Any, path: str) -> Any:
    current = data
    if not path:
        return current
    for part in path.split("."):
        if isinstance(current, dict):
            if part not in current:
                raise KeyError(path)
            current = current[part]
            continue
        if isinstance(current, list):
            try:
                current = current[int(part)]
            except (ValueError, IndexError) as exc:
                raise KeyError(path) from exc
            continue
        raise KeyError(path)
    return current


def resolve_placeholder(expression: str, context: dict[str, Any]) -> Any:
    expression = expression.strip()
    try:
        return copy.deepcopy(get_path(context, expression))
    except KeyError as exc:
        raise SystemExit(f"[ERROR] Missing template value: {expression}") from exc


def render_template(value: Any, context: dict[str, Any]) -> Any:
    if isinstance(value, str):
        match = PLACEHOLDER_RE.fullmatch(value)
        if match:
            return resolve_placeholder(match.group(1), context)

        def replace(match_obj: re.Match[str]) -> str:
            resolved = resolve_placeholder(match_obj.group(1), context)
            if isinstance(resolved, (dict, list)):
                return json.dumps(resolved, ensure_ascii=False)
            if resolved is None:
                return ""
            return str(resolved)

        return PLACEHOLDER_RE.sub(replace, value)

    if isinstance(value, list):
        return [render_template(item, context) for item in value]

    if isinstance(value, dict):
        return {key: render_template(item, context) for key, item in value.items()}

    return value


def build_url(base_url: str, path_value: str, query: dict[str, Any]) -> str:
    if ABSOLUTE_URL_RE.match(path_value):
        resolved = path_value
    else:
        if not base_url:
            raise SystemExit("[ERROR] base_url is empty and operation path is not absolute.")
        base = base_url.rstrip("/") + "/"
        resolved = parse.urljoin(base, path_value.lstrip("/"))

    filtered = {}
    for key, value in query.items():
        if value in (None, ""):
            continue
        filtered[key] = value
    if not filtered:
        return resolved
    return f"{resolved}?{parse.urlencode(filtered, doseq=True)}"


def normalize_headers(headers: dict[str, Any]) -> dict[str, str]:
    normalized = {}
    for key, value in headers.items():
        if value is None:
            continue
        normalized[str(key)] = str(value)
    return normalized


def redact_headers(headers: dict[str, str]) -> dict[str, str]:
    redacted = {}
    for key, value in headers.items():
        if key.lower() in {"authorization", "cookie", "set-cookie", "x-api-key"}:
            redacted[key] = "[REDACTED]"
        else:
            redacted[key] = value
    return redacted


def redact_cookies(cookies: Iterable[str]) -> list[str]:
    return ["[REDACTED]" for _ in cookies]


def redact_captured(captured: dict[str, Any]) -> dict[str, Any]:
    redacted = {}
    for key, value in captured.items():
        if key.lower() in {"sessionid", "sessioncookie"}:
            redacted[key] = "[REDACTED]"
        else:
            redacted[key] = value
    return redacted


def redact_login_body(value: Any) -> Any:
    if isinstance(value, dict):
        redacted = {}
        for key, child in value.items():
            lowered = str(key).lower()
            if lowered in {"sessionid", "session_id", "sessioncookie", "qrcode", "sign", "creativebrain-sessionid"}:
                redacted[key] = "[REDACTED]"
            else:
                redacted[key] = redact_login_body(child)
        return redacted
    if isinstance(value, list):
        return [redact_login_body(item) for item in value]
    if isinstance(value, str):
        value = re.sub(r'("sessionId"\s*:\s*")([^"]+)(")', r'\1[REDACTED]\3', value)
        value = re.sub(r'("session_id"\s*:\s*")([^"]+)(")', r'\1[REDACTED]\3', value)
        value = re.sub(r'("qrCode"\s*:\s*")([^"]+)(")', r'\1[REDACTED]\3', value)
        value = re.sub(r'("sign"\s*:\s*")([^"]+)(")', r'\1[REDACTED]\3', value)
        value = re.sub(r"(sessionId=)([^;,\s]+)", r"\1[REDACTED]", value)
        value = re.sub(r"(creativebrain-sessionid=)([^;,\s]+)", r"\1[REDACTED]", value)
        return value
    return value


def encode_body(content_type: str, body: Any, headers: dict[str, str]) -> Optional[bytes]:
    kind = content_type.lower()
    if kind == "none":
        return None
    if kind == "json":
        headers.setdefault("Content-Type", "application/json")
        return json.dumps(body, ensure_ascii=False).encode("utf-8")
    if kind == "form":
        headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
        return parse.urlencode(body, doseq=True).encode("utf-8")
    if kind == "raw":
        if body is None:
            return None
        if isinstance(body, bytes):
            return body
        return str(body).encode("utf-8")
    raise SystemExit(f"[ERROR] Unsupported content_type: {content_type}")


def parse_response(raw_body: bytes, content_type: Optional[str]) -> Any:
    text = raw_body.decode("utf-8", errors="replace")
    if content_type and "json" in content_type.lower():
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def run_request(
    *,
    method: str,
    url: str,
    headers: dict[str, str],
    body: Optional[bytes],
    timeout_seconds: int,
) -> dict[str, Any]:
    req = request.Request(url=url, method=method.upper(), headers=headers, data=body)
    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            raw_body = response.read()
            parsed_body = parse_response(raw_body, response.headers.get("Content-Type"))
            response_headers = dict(response.headers.items())
            cookies = response.headers.get_all("Set-Cookie") or []
            return {
                "status": response.status,
                "headers": response_headers,
                "cookies": cookies,
                "body": parsed_body,
            }
    except error.HTTPError as exc:
        raw_body = exc.read()
        parsed_body = parse_response(raw_body, exc.headers.get("Content-Type") if exc.headers else None)
        response_headers = dict(exc.headers.items()) if exc.headers else {}
        cookies = exc.headers.get_all("Set-Cookie") if exc.headers else []
        raise SystemExit(
            "[ERROR] HTTP request failed: "
            f"status={exc.code} body={json.dumps(redact_login_body(parsed_body), ensure_ascii=False)} "
            f"headers={json.dumps(redact_headers(response_headers), ensure_ascii=False)} "
            f"cookies={json.dumps(redact_cookies(cookies or []), ensure_ascii=False)}"
        ) from exc
    except error.URLError as exc:
        raise SystemExit(f"[ERROR] Request failed: {exc}") from exc


def load_session(path: Optional[Path]) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    payload = load_json(path)
    if not isinstance(payload, dict):
        raise SystemExit(f"[ERROR] Session file must contain a JSON object: {path}")
    return payload


def find_first_by_keys(data: Any, candidates: Iterable[str]) -> Any:
    lookup = {candidate.lower() for candidate in candidates}

    def walk(value: Any) -> Any:
        if isinstance(value, dict):
            for key, child in value.items():
                if str(key).lower() in lookup:
                    return child
            for child in value.values():
                found = walk(child)
                if found is not None:
                    return found
        elif isinstance(value, list):
            for child in value:
                found = walk(child)
                if found is not None:
                    return found
        return None

    return walk(data)


def find_session_id_in_text(value: str) -> Optional[str]:
    patterns = [
        r'"sessionId"\s*:\s*"([^"]+)"',
        r'"session_id"\s*:\s*"([^"]+)"',
        r"sessionId=([^;,&\\s]+)",
        r"creativebrain-sessionid=([^;,&\\s]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    return None


def parse_cookie_session_id(cookies: Iterable[str]) -> Optional[str]:
    for cookie in cookies:
        for cookie_name in COOKIE_NAME_CANDIDATES:
            match = re.search(rf"(?:^|;\s*){re.escape(cookie_name)}=([^;]+)", cookie)
            if match:
                return match.group(1)
    return None


def capture_session_values(response_payload: dict[str, Any]) -> dict[str, Any]:
    captured: dict[str, Any] = {}
    body = response_payload.get("body")
    cookies = response_payload.get("cookies", [])

    session_id = parse_cookie_session_id(cookies)
    if session_id is None and isinstance(body, dict):
        for path in ("data.data.sessionId", "data.sessionId"):
            try:
                session_id = str(get_path(body, path))
                break
            except KeyError:
                continue
    if session_id is None and isinstance(body, (dict, list)):
        found = find_first_by_keys(body, SESSION_KEY_CANDIDATES)
        if found is not None:
            session_id = str(found)
    if session_id is None and isinstance(body, str):
        session_id = find_session_id_in_text(body)

    if session_id:
        captured["sessionId"] = session_id
        captured["sessionCookie"] = f"sessionId={session_id}"

    if isinstance(body, (dict, list)):
        for output_key, candidates in USER_KEY_GROUPS.items():
            found = find_first_by_keys(body, candidates)
            if found is not None:
                captured[output_key] = found

    return captured


def build_context(
    *,
    session_payload: dict[str, Any],
    input_payload: dict[str, Any],
) -> dict[str, Any]:
    context: dict[str, Any] = {}
    captured = session_payload.get("captured", {})
    if isinstance(captured, dict):
        context = merge_dicts(context, captured)
        context["session"] = copy.deepcopy(captured)
    login_response = session_payload.get("login_response")
    if login_response is not None:
        context["login_response"] = copy.deepcopy(login_response)
    if input_payload:
        context = merge_dicts(context, input_payload)
    return context


def command_to_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    body_payload: dict[str, Any] = {}

    if args.input_json:
        loaded = load_json(Path(args.input_json))
        if not isinstance(loaded, dict):
            raise SystemExit(f"[ERROR] --input-json must contain a JSON object: {args.input_json}")
        body_payload = merge_dicts(body_payload, loaded)

    overrides = parse_values(args.value or [])
    body_payload = merge_dicts(body_payload, overrides)

    if not body_payload:
        raise SystemExit(f"[ERROR] {args.command} requires --input-json or at least one --value.")

    if args.command in OPERATION_ALIASES:
        body_payload["source"] = FIXED_SOURCE_VALUE

    payload["payload"] = body_payload
    return payload


def require_session(context: dict[str, Any]) -> None:
    session_id = context.get("sessionId")
    if session_id:
        return
    session = context.get("session", {})
    if isinstance(session, dict) and session.get("sessionId"):
        return
    raise SystemExit("[ERROR] No sessionId found. Run the login command first.")


def extract_article_id(response_body: Any) -> Optional[Any]:
    if isinstance(response_body, dict):
        for path in ARTICLE_ID_PATHS:
            try:
                return get_path(response_body, path)
            except KeyError:
                continue
        found = find_first_by_keys(response_body, ("article_id", "articleId"))
        if found is not None:
            return found
    return None


def load_contract(path: Path) -> dict[str, Any]:
    contract = load_json(path)
    if not isinstance(contract, dict):
        raise SystemExit(f"[ERROR] Contract must contain a JSON object: {path}")
    if "operations" not in contract:
        raise SystemExit("[ERROR] Contract must define 'operations'.")
    return contract


def render_request_definition(
    *,
    definition: dict[str, Any],
    base_url: str,
    base_headers: dict[str, Any],
    context: dict[str, Any],
) -> dict[str, Any]:
    method = str(definition.get("method", "GET")).upper()
    path_value = render_template(str(definition.get("path", "")), context)
    headers = normalize_headers(
        merge_dicts(
            base_headers if isinstance(base_headers, dict) else {},
            render_template(definition.get("headers", {}), context),
        )
    )
    query = render_template(definition.get("query", {}), context)
    if query and not isinstance(query, dict):
        raise SystemExit("[ERROR] Operation query must render to an object.")
    body_template = definition.get("body")
    body_value = render_template(body_template, context) if body_template is not None else None
    content_type = str(definition.get("content_type", "none"))
    body = encode_body(content_type, body_value, headers)
    url = build_url(base_url, str(path_value), query or {})
    return {
        "method": method,
        "url": url,
        "headers": headers,
        "body": body,
    }


def extract_response_code(body: Any) -> Optional[str]:
    if isinstance(body, dict):
        code = body.get("code")
        if code is not None:
            return str(code)
    return None


def extract_response_msg(body: Any) -> str:
    if isinstance(body, dict):
        msg = body.get("msg")
        if msg is not None:
            return str(msg)
    return ""


def should_continue_qr_polling(code: Optional[str], msg: str, qr_config: dict[str, Any]) -> bool:
    pending_codes = qr_config.get("pending_codes")
    if isinstance(pending_codes, list):
        normalized = {str(item) for item in pending_codes}
    else:
        normalized = {str(qr_config.get("waiting_code", "3030"))}

    if code in normalized:
        return True

    pending_message_keywords = qr_config.get("pending_message_keywords")
    if isinstance(pending_message_keywords, list):
        keywords = [str(item) for item in pending_message_keywords]
    else:
        keywords = ["等待", "未确认", "扫码成功"]

    return any(keyword and keyword in msg for keyword in keywords)


def load_qrcode_library() -> str:
    try:
        content = QRCODE_ASSET_PATH.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SystemExit(f"[ERROR] QR code asset not found: {QRCODE_ASSET_PATH}") from exc
    if "Not found:" in content or "Couldn't find the requested file" in content:
        raise SystemExit(
            "[ERROR] QR code asset is invalid. Replace "
            f"{QRCODE_ASSET_PATH} with a working browser QR library."
        )
    if "QRCode" not in content:
        raise SystemExit(f"[ERROR] QR code asset does not expose a usable QRCode implementation: {QRCODE_ASSET_PATH}")
    return content


def build_qr_share_link(qr_config: dict[str, Any], qr_code: str) -> str:
    platform_name = str(qr_config.get("platform_name", "创作者平台"))
    platform_encoded = base64.b64encode(platform_name.encode("utf-8")).decode("ascii")
    share_payload = {
        "type": "login",
        "platForm": platform_encoded,
        "code": qr_code,
    }
    share_token = base64.b64encode(
        json.dumps(share_payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).decode("ascii")
    share_base_url = str(qr_config.get("share_base_url", ""))
    if not share_base_url:
        raise SystemExit("[ERROR] QR login config is missing share_base_url.")
    return f"{share_base_url}{share_token}"


def write_qr_html(html_output: Path, qr_link: str) -> None:
    qrcode_library = load_qrcode_library()
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Z视介扫码登录</title>
  <style>
    :root {{
      color-scheme: light;
      font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      background:
        radial-gradient(circle at top, rgba(190, 230, 255, 0.7), transparent 40%),
        linear-gradient(160deg, #f5fbff 0%, #eef6ff 100%);
      color: #10233d;
    }}
    .card {{
      width: min(420px, calc(100vw - 32px));
      padding: 28px 24px;
      border-radius: 24px;
      background: rgba(255, 255, 255, 0.92);
      box-shadow: 0 24px 80px rgba(16, 35, 61, 0.14);
      text-align: center;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 28px;
    }}
    p {{
      margin: 0;
      line-height: 1.6;
      color: #48617d;
    }}
    #qrcode {{
      width: 256px;
      height: 256px;
      margin: 24px auto 16px;
      display: grid;
      place-items: center;
      background: #fff;
      border-radius: 20px;
      border: 1px solid rgba(16, 35, 61, 0.08);
      padding: 12px;
    }}
    #qrcode img {{
      display: block;
      width: 100%;
      height: 100%;
    }}
    .hint {{
      margin-top: 14px;
      font-size: 13px;
      color: #67809c;
      word-break: break-all;
    }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Z视介扫码登录</h1>
    <p>请使用 Z视介创作者平台对应的 App 扫描二维码完成登录。</p>
    <div id="qrcode">二维码生成中...</div>
    <p class="hint">扫码成功后，CLI 会自动获取并保存 sessionId。</p>
  </div>
  <script>{qrcode_library}</script>
  <script>
    const qrLink = {json.dumps(qr_link, ensure_ascii=False)};
    const target = document.getElementById("qrcode");
    target.textContent = "";
    try {{
      new QRCode(target, {{
        text: qrLink,
        width: 232,
        height: 232,
        colorDark: "#10233d",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H
      }});
    }} catch (error) {{
      target.textContent = "二维码生成失败";
      console.error(error);
    }}
  </script>
</body>
</html>
"""
    write_text(html_output, html_content)


def build_qr_sign(secret: str, ts: str, qr_code: str) -> str:
    return hashlib.sha256(f"{secret}{ts}{qr_code}".encode("utf-8")).hexdigest()


def generate_qr_matrix(qr_link: str) -> list[list[bool]]:
    node_path = shutil.which("node")
    if not node_path:
        raise SystemExit("[ERROR] 'node' is required to generate a QR PNG but was not found on PATH.")

    script = f"""
const fs = require("fs");
const vm = require("vm");
const lib = fs.readFileSync({json.dumps(str(QRCODE_ASSET_PATH))}, "utf8");
const context = {{
  navigator: {{ userAgent: "node" }},
  document: {{
    documentElement: {{ tagName: "div" }},
    createElement: () => ({{ style: {{}} }}),
    createElementNS: () => ({{ setAttribute(){{}}, setAttributeNS(){{}}, appendChild(){{}}, style: {{}} }}),
    getElementById: () => null,
  }},
  console,
}};
vm.createContext(context);
vm.runInContext(lib, context);
const target = {{ childNodes: [] }};
Object.defineProperty(target, "innerHTML", {{
  get() {{ return this._html || ""; }},
  set(v) {{
    this._html = v;
    this.childNodes = [{{ offsetWidth: 256, offsetHeight: 256, style: {{}} }}];
  }},
}});
const qr = new context.QRCode(target, {{
  text: {json.dumps(qr_link, ensure_ascii=False)},
  width: 256,
  height: 256,
  correctLevel: context.QRCode.CorrectLevel.H
}});
const size = qr._oQRCode.getModuleCount();
const matrix = [];
for (let row = 0; row < size; row += 1) {{
  const line = [];
  for (let col = 0; col < size; col += 1) {{
    line.push(Boolean(qr._oQRCode.isDark(row, col)));
  }}
  matrix.push(line);
}}
process.stdout.write(JSON.stringify(matrix));
"""
    completed = subprocess.run(
        [node_path, "-e", script],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        raise SystemExit(f"[ERROR] Failed to generate QR matrix with node: {stderr or 'unknown error'}")

    try:
        matrix = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit("[ERROR] QR matrix generator returned invalid JSON.") from exc

    if not isinstance(matrix, list) or not matrix or not isinstance(matrix[0], list):
        raise SystemExit("[ERROR] QR matrix generator returned an invalid matrix.")
    return [[bool(cell) for cell in row] for row in matrix]


def write_qr_png(png_output: Path, qr_link: str) -> None:
    try:
        from PIL import Image, ImageDraw
    except Exception as exc:
        raise SystemExit("[ERROR] Pillow is required to generate a QR PNG but is not available.") from exc

    matrix = generate_qr_matrix(qr_link)
    module_count = len(matrix)
    border_modules = 4
    scale = 12
    image_size = (module_count + border_modules * 2) * scale
    image = Image.new("RGB", (image_size, image_size), "white")
    draw = ImageDraw.Draw(image)

    for row_index, row in enumerate(matrix):
        for col_index, is_dark in enumerate(row):
            if not is_dark:
                continue
            x0 = (col_index + border_modules) * scale
            y0 = (row_index + border_modules) * scale
            x1 = x0 + scale - 1
            y1 = y0 + scale - 1
            draw.rectangle((x0, y0, x1, y1), fill="#10233d")

    png_output.parent.mkdir(parents=True, exist_ok=True)
    image.save(png_output)


def request_qr_code(
    *,
    qr_config: dict[str, Any],
    base_headers: dict[str, Any],
    timeout_seconds: int,
) -> tuple[str, dict[str, Any], dict[str, Any]]:
    base_url = str(qr_config.get("base_url", ""))
    if not base_url:
        raise SystemExit("[ERROR] QR login config is missing base_url.")
    definition = qr_config.get("get_qrcode")
    if not isinstance(definition, dict):
        raise SystemExit("[ERROR] QR login config is missing get_qrcode definition.")

    request_info = render_request_definition(
        definition=definition,
        base_url=base_url,
        base_headers=base_headers,
        context={},
    )
    response_payload = run_request(timeout_seconds=timeout_seconds, **request_info)
    body = response_payload.get("body")
    if not isinstance(body, dict):
        raise SystemExit("[ERROR] QR code response body must be JSON.")
    try:
        qr_code = str(get_path(body, "data.qrCode"))
    except KeyError as exc:
        raise SystemExit(
            "[ERROR] QR code response did not expose data.qrCode. "
            "Provide a real response sample so the extractor can be updated."
        ) from exc
    return qr_code, request_info, response_payload


def poll_qr_login(
    *,
    qr_config: dict[str, Any],
    base_headers: dict[str, Any],
    timeout_seconds: int,
    qr_code: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    base_url = str(qr_config.get("base_url", ""))
    if not base_url:
        raise SystemExit("[ERROR] QR login config is missing base_url.")
    definition = qr_config.get("poll_login")
    if not isinstance(definition, dict):
        raise SystemExit("[ERROR] QR login config is missing poll_login definition.")
    secret = str(qr_config.get("sign_secret", ""))
    if not secret:
        raise SystemExit("[ERROR] QR login config is missing sign_secret.")

    ts = str(int(time.time() * 1000))
    context = {
        "qrCode": qr_code,
        "ts": ts,
        "sign": build_qr_sign(secret, ts, qr_code),
    }
    request_info = render_request_definition(
        definition=definition,
        base_url=base_url,
        base_headers=base_headers,
        context=context,
    )
    response_payload = run_request(timeout_seconds=timeout_seconds, **request_info)
    return request_info, response_payload


def perform_login(args: argparse.Namespace) -> int:
    contract_path = Path(args.contract) if args.contract else DEFAULT_CONTRACT_PATH
    contract = load_contract(contract_path)
    qr_config = contract.get("qr_login")
    if not isinstance(qr_config, dict):
        raise SystemExit("[ERROR] Contract must define a top-level qr_login object.")

    base_headers = contract.get("default_headers", {})
    if base_headers and not isinstance(base_headers, dict):
        raise SystemExit("[ERROR] Contract field 'default_headers' must be an object.")

    timeout_seconds = int(args.timeout or contract.get("default_timeout_seconds", 30))
    wait_timeout_seconds = int(args.wait_timeout or qr_config.get("wait_timeout_seconds", 300))
    poll_interval_seconds = float(args.poll_interval or qr_config.get("poll_interval_seconds", 1))
    if wait_timeout_seconds <= 0:
        raise SystemExit("[ERROR] --wait-timeout must be greater than 0.")
    if poll_interval_seconds <= 0:
        raise SystemExit("[ERROR] --poll-interval must be greater than 0.")

    session_path = Path(args.session) if args.session else DEFAULT_SESSION_PATH
    html_output = Path(args.html_output) if args.html_output else DEFAULT_QR_HTML_PATH
    png_output = Path(args.png_output) if args.png_output else DEFAULT_QR_PNG_PATH

    qr_code, get_qr_request, get_qr_response = request_qr_code(
        qr_config=qr_config,
        base_headers=base_headers,
        timeout_seconds=timeout_seconds,
    )
    qr_link = build_qr_share_link(qr_config, qr_code)
    write_qr_html(html_output, qr_link)
    write_qr_png(png_output, qr_link)
    print(
        f"[INFO] QR files ready. html={html_output} png={png_output}. "
        "Keep this command running until the user finishes scanning.",
        file=sys.stderr,
        flush=True,
    )

    waiting_code = str(qr_config.get("waiting_code", "3030"))
    success_code = str(qr_config.get("success_code", "200"))
    deadline = time.time() + wait_timeout_seconds
    poll_request: Optional[dict[str, Any]] = None
    poll_response: Optional[dict[str, Any]] = None
    last_code = ""
    last_msg = ""

    while time.time() < deadline:
        poll_request, poll_response = poll_qr_login(
            qr_config=qr_config,
            base_headers=base_headers,
            timeout_seconds=timeout_seconds,
            qr_code=qr_code,
        )
        code = extract_response_code(poll_response.get("body"))
        msg = extract_response_msg(poll_response.get("body"))
        last_code = code or ""
        last_msg = msg
        if code == waiting_code:
            time.sleep(poll_interval_seconds)
            continue
        if should_continue_qr_polling(code, msg, qr_config):
            time.sleep(poll_interval_seconds)
            continue
        if code != success_code:
            raise SystemExit(f"[ERROR] QR login failed: code={code or 'UNKNOWN'} msg={msg or '未知错误'}")
        break

    if poll_response is None:
        raise SystemExit("[ERROR] QR login polling did not start.")
    if extract_response_code(poll_response.get("body")) == waiting_code or should_continue_qr_polling(last_code or None, last_msg, qr_config):
        raise SystemExit(
            "[ERROR] QR login timed out before the code was scanned. "
            f"last_code={last_code or 'UNKNOWN'} last_msg={last_msg or '未知状态'} "
            f"html={html_output} png={png_output}"
        )

    captured = capture_session_values(poll_response)
    if "sessionId" not in captured:
        raise SystemExit(
            "[ERROR] QR login succeeded but no sessionId was found in the response. "
            "Provide a real success response sample so the extractor can be updated."
        )

    session_output = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "captured": captured,
        "login_response": poll_response["body"],
        "login_mode": "qr_code",
        "qr_login": {
            "login_page": str(qr_config.get("login_page", "https://mp.cztv.com/#/login")),
            "html_output": str(html_output),
            "png_output": str(png_output),
        },
    }
    write_json(session_path, session_output)

    output = {
        "operation": "login",
        "login_mode": "qr_code",
        "qr_html_file": str(html_output),
        "qr_png_file": str(png_output),
        "poll_interval_seconds": poll_interval_seconds,
        "request": {
            "get_qrcode": {
                "method": get_qr_request["method"],
                "url": get_qr_request["url"],
                "headers": redact_headers(get_qr_request["headers"]),
            },
            "poll_login": {
                "method": poll_request["method"] if poll_request else "POST",
                "url": poll_request["url"] if poll_request else "",
                "headers": redact_headers(poll_request["headers"]) if poll_request else {},
            },
        },
        "response": {
            "get_qrcode": {
                "status": get_qr_response["status"],
                "headers": redact_headers(get_qr_response["headers"]),
                "cookies": redact_cookies(get_qr_response.get("cookies", [])),
                "body": redact_login_body(get_qr_response["body"]),
            },
            "poll_login": {
                "status": poll_response["status"],
                "headers": redact_headers(poll_response["headers"]),
                "cookies": redact_cookies(poll_response.get("cookies", [])),
                "body": redact_login_body(poll_response["body"]),
            },
        },
        "session_file": str(session_path),
        "captured": redact_captured(captured),
    }

    if args.save_response:
        write_json(Path(args.save_response), output)

    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


def perform_operation(args: argparse.Namespace) -> int:
    contract_path = Path(args.contract) if args.contract else DEFAULT_CONTRACT_PATH
    contract = load_contract(contract_path)
    operation_name = OPERATION_ALIASES[args.command]

    operations = contract.get("operations", {})
    operation = operations.get(operation_name)
    if not isinstance(operation, dict):
        raise SystemExit(f"[ERROR] Operation not found in contract: {operation_name}")

    session_path = Path(args.session) if args.session else DEFAULT_SESSION_PATH
    session_payload = load_session(session_path)
    input_payload = command_to_payload(args)
    context = build_context(session_payload=session_payload, input_payload=input_payload)
    require_session(context)

    base_headers = contract.get("default_headers", {})
    if base_headers and not isinstance(base_headers, dict):
        raise SystemExit("[ERROR] Contract field 'default_headers' must be an object.")

    base_url = args.base_url or str(contract.get("base_url", ""))
    request_info = render_request_definition(
        definition=operation,
        base_url=base_url,
        base_headers=base_headers,
        context=context,
    )
    timeout_seconds = int(args.timeout or contract.get("default_timeout_seconds", 30))

    response_payload = run_request(timeout_seconds=timeout_seconds, **request_info)

    output = {
        "operation": operation_name,
        "request": {
            "method": request_info["method"],
            "url": request_info["url"],
            "headers": redact_headers(request_info["headers"]),
        },
        "response": {
            "status": response_payload["status"],
            "headers": redact_headers(response_payload["headers"]),
            "cookies": redact_cookies(response_payload.get("cookies", [])),
            "body": response_payload["body"],
        },
    }

    article_id = extract_article_id(response_payload["body"])
    if article_id is not None:
        output["result"] = {"article_id": article_id}

    if args.save_response:
        write_json(Path(args.save_response), output)

    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Log in to Z视介 with a QR code, then publish or edit article and video content.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common_arguments(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument(
            "--contract",
            help=f"Path to the contract JSON file. Defaults to {DEFAULT_CONTRACT_PATH}.",
        )
        subparser.add_argument(
            "--session",
            help="Path to the local session file. Defaults to a temp-file path outside the skill directory.",
        )
        subparser.add_argument("--save-response", help="Optional file path to save the console output JSON.")
        subparser.add_argument("--timeout", type=int, help="Optional per-request timeout override in seconds.")

    login_parser = subparsers.add_parser("login", help="Generate a QR code, wait for scan, and persist sessionId.")
    add_common_arguments(login_parser)
    login_parser.add_argument(
        "--html-output",
        help=f"Path for the generated QR HTML file. Defaults to {DEFAULT_QR_HTML_PATH}.",
    )
    login_parser.add_argument(
        "--png-output",
        help=f"Path for the generated QR PNG file. Defaults to {DEFAULT_QR_PNG_PATH}.",
    )
    login_parser.add_argument(
        "--wait-timeout",
        type=int,
        help="Maximum number of seconds to wait for the QR code to be scanned.",
    )
    login_parser.add_argument(
        "--poll-interval",
        type=float,
        help="Seconds between QR login polling requests.",
    )
    login_parser.set_defaults(func=perform_login)

    for name in ("publish-article", "edit-article", "publish-video", "edit-video"):
        subparser = subparsers.add_parser(name)
        add_common_arguments(subparser)
        subparser.add_argument("--input-json", help="Path to an input JSON file.")
        subparser.add_argument(
            "--value",
            action="append",
            default=[],
            help="Runtime value in key=value form. Repeat as needed.",
        )
        subparser.add_argument(
            "--base-url",
            help="Optional override for the publish/edit API host.",
        )
        subparser.set_defaults(func=perform_operation)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
