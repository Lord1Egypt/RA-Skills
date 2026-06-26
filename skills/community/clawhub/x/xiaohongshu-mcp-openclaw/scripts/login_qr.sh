#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVER_NAME="${1:-xiaohongshu-mcp}"
QR_FILE="${2:-${XHS_QR_FILE:-$HOME/.openclaw/workspace/xhs-login-qrcode.png}}"
TIMEOUT_MS="${XHS_QR_TIMEOUT_MS:-30000}"
WAIT_SECONDS="${XHS_QR_WAIT_SECONDS:-0}"
POLL_INTERVAL="${XHS_QR_POLL_INTERVAL:-3}"
AUTO_OPEN="${XHS_QR_AUTO_OPEN:-1}"

TMP_RAW="$(mktemp "/tmp/xhs_login_qr_raw.${SERVER_NAME//[^a-zA-Z0-9_.-]/_}.XXXXXX.json")"
TMP_PARSED="$(mktemp "/tmp/xhs_login_qr_parsed.${SERVER_NAME//[^a-zA-Z0-9_.-]/_}.XXXXXX.json")"

cleanup() {
  rm -f "$TMP_RAW" "$TMP_PARSED"
}
trap cleanup EXIT INT TERM

set +e
python3 "$BASE_DIR/scripts/xhs_mcp_client.py" \
  --server "$SERVER_NAME" \
  --timeout "$TIMEOUT_MS" \
  ensure-login \
  --wait-seconds "$WAIT_SECONDS" \
  --poll-interval "$POLL_INTERVAL" > "$TMP_RAW"
CLIENT_RC=$?
set -e

if [ "$CLIENT_RC" -ne 0 ]; then
  cat "$TMP_RAW"
  exit "$CLIENT_RC"
fi

set +e
python3 - "$TMP_RAW" "$QR_FILE" > "$TMP_PARSED" <<'PY'
import ast
import base64
import json
import os
import re
import sys
from typing import Any, Dict, Iterable, Optional
try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

raw_path = sys.argv[1]
qr_file = sys.argv[2]

with open(raw_path, "r", encoding="utf-8") as fh:
    payload = json.load(fh)


def replace_tokens_outside_strings(text: str, replacements: Dict[str, str]) -> str:
    if not replacements:
        return text

    result = []
    idx = 0
    in_string = False
    escaped = False
    quote_char = ""

    while idx < len(text):
        ch = text[idx]
        if in_string:
            result.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote_char:
                in_string = False
            idx += 1
            continue

        if ch in ('"', "'"):
            in_string = True
            quote_char = ch
            result.append(ch)
            idx += 1
            continue

        if ch == "_" or ch.isalpha():
            end = idx + 1
            while end < len(text) and (text[end] == "_" or text[end].isalnum()):
                end += 1
            token = text[idx:end]
            result.append(replacements.get(token, token))
            idx = end
            continue

        result.append(ch)
        idx += 1

    return "".join(result)


def parse_js_object_literal(text: str) -> Any:
    candidate = text.strip()
    if not candidate or candidate[0] not in "{[":
        raise ValueError("not js object literal")

    candidate = re.sub(
        r'([{\[,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:',
        r'\1"\2":',
        candidate,
    )
    candidate = replace_tokens_outside_strings(
        candidate,
        {"true": "True", "false": "False", "null": "None"},
    )
    return ast.literal_eval(candidate)


def try_parse_structured_text(text: Any) -> Any:
    if not isinstance(text, str):
        return None
    candidate = text.strip()
    if not candidate:
        return None

    try:
        return json.loads(candidate)
    except Exception:
        pass

    if yaml is not None:
        try:
            return yaml.safe_load(candidate)
        except Exception:
            pass

    try:
        return parse_js_object_literal(candidate)
    except Exception:
        return None


def extract_base64_from_text(text: str) -> Optional[str]:
    match = re.search(r"data\s*:\s*'([^']+)'", text, flags=re.DOTALL)
    if match:
        return match.group(1)
    match = re.search(r'data\s*:\s*"([^"]+)"', text, flags=re.DOTALL)
    if match:
        return match.group(1)
    return None


def walk(value: Any) -> Iterable[Dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)
    elif isinstance(value, str):
        parsed = try_parse_structured_text(value)
        if isinstance(parsed, (dict, list)):
            yield from walk(parsed)


result: Dict[str, Any] = {
    "already_logged_in": bool(payload.get("already_logged_in", False)),
    "login_status": payload.get("login_status"),
    "source_result_file": raw_path,
}

if result["already_logged_in"]:
    result["status"] = "already_logged_in"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0)

qr_payload = payload.get("qr_payload")
if qr_payload is None:
    result["status"] = "no_qr_payload"
    result["error"] = "ensure-login returned no qr_payload"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0)

if isinstance(qr_payload, str):
    parsed_qr_payload = try_parse_structured_text(qr_payload)
    if isinstance(parsed_qr_payload, (dict, list)):
        qr_payload = parsed_qr_payload

image_b64 = None
image_mime = "image/png"
qr_message = None
for item in walk(qr_payload):
    item_type = str(item.get("type", "")).lower()
    if qr_message is None and item_type == "text" and isinstance(item.get("text"), str):
        qr_message = item["text"]
    if image_b64 is None and item_type == "image" and isinstance(item.get("data"), str):
        image_b64 = item["data"]
        mime = item.get("mimeType") or item.get("mime_type")
        if isinstance(mime, str) and mime:
            image_mime = mime
    if qr_message is not None and image_b64 is not None:
        break

result["qr_message"] = qr_message
url_hint = payload.get("qr_url_hint")
if isinstance(url_hint, str) and url_hint:
    result["qr_url_hint"] = url_hint
elif isinstance(qr_message, str):
    match = re.search(r"https?://[^\s\"'<>]+", qr_message)
    if match:
        result["qr_url_hint"] = match.group(0)

if not image_b64 and isinstance(qr_message, str):
    parsed_msg = try_parse_structured_text(qr_message)
    if isinstance(parsed_msg, (dict, list)):
        for item in walk(parsed_msg):
            item_type = str(item.get("type", "")).lower()
            if image_b64 is None and item_type == "image" and isinstance(item.get("data"), str):
                image_b64 = item["data"]
                mime = item.get("mimeType") or item.get("mime_type")
                if isinstance(mime, str) and mime:
                    image_mime = mime
            if qr_message is None and item_type == "text" and isinstance(item.get("text"), str):
                qr_message = item["text"]
            if image_b64 is not None:
                break

if not image_b64 and isinstance(qr_message, str):
    extracted = extract_base64_from_text(qr_message)
    if extracted:
        image_b64 = extracted
    mime_match = re.search(r"mimeType\s*:\s*'([^']+)'", qr_message)
    if mime_match:
        image_mime = mime_match.group(1)
    else:
        mime_match = re.search(r'mimeType\s*:\s*"([^"]+)"', qr_message)
        if mime_match:
            image_mime = mime_match.group(1)

if not image_b64:
    if isinstance(result.get("qr_url_hint"), str) and result.get("qr_url_hint"):
        result["status"] = "qr_url_ready"
    else:
        result["status"] = "no_qr_image"
    result["error"] = "qr_payload has no embedded image data"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0)

if image_b64.startswith("data:"):
    parts = image_b64.split(",", 1)
    if len(parts) == 2:
        image_b64 = parts[1]

try:
    image_bytes = base64.b64decode(image_b64, validate=True)
except Exception as exc:  # noqa: BLE001
    result["status"] = "decode_failed"
    result["error"] = f"failed to decode qr image: {exc}"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(4)

qr_path = os.path.abspath(qr_file)
os.makedirs(os.path.dirname(qr_path), exist_ok=True)
with open(qr_path, "wb") as fh:
    fh.write(image_bytes)

result.update(
    {
        "status": "qr_ready",
        "qr_file": qr_path,
        "qr_mime_type": image_mime,
        "qr_size_bytes": len(image_bytes),
    }
)
print(json.dumps(result, ensure_ascii=False, indent=2))
PY
PARSE_RC=$?
set -e

if [ "$PARSE_RC" -ne 0 ]; then
  cat "$TMP_PARSED"
  exit "$PARSE_RC"
fi

STATUS="$(python3 - "$TMP_PARSED" <<'PY'
import json
import sys
with open(sys.argv[1], "r", encoding="utf-8") as fh:
    data = json.load(fh)
print(str(data.get("status", "")))
PY
)"

if [ "$STATUS" != "qr_ready" ] && [ "$STATUS" != "qr_url_ready" ]; then
  cat "$TMP_PARSED"
  exit 0
fi

OPEN_TARGET="$(python3 - "$TMP_PARSED" "$STATUS" <<'PY'
import json
import sys
with open(sys.argv[1], "r", encoding="utf-8") as fh:
    data = json.load(fh)
status = sys.argv[2]
if status == "qr_ready":
    print(str(data.get("qr_file", "")))
elif status == "qr_url_ready":
    print(str(data.get("qr_url_hint", "")))
else:
    print("")
PY
)"

OPEN_BIN=""
if command -v open >/dev/null 2>&1; then
  OPEN_BIN="open"
elif command -v xdg-open >/dev/null 2>&1; then
  OPEN_BIN="xdg-open"
fi

AUTO_OPEN_ATTEMPTED=false
AUTO_OPEN_SUCCESS=false
OPEN_COMMAND=""

if [ -n "$OPEN_BIN" ] && [ -n "$OPEN_TARGET" ]; then
  OPEN_COMMAND="$OPEN_BIN \"$OPEN_TARGET\""
fi

if [ "$AUTO_OPEN" = "1" ] && [ -n "$OPEN_BIN" ] && [ -n "$OPEN_TARGET" ]; then
  AUTO_OPEN_ATTEMPTED=true
  if "$OPEN_BIN" "$OPEN_TARGET" >/dev/null 2>&1; then
    AUTO_OPEN_SUCCESS=true
  fi
fi

if command -v jq >/dev/null 2>&1; then
  if [ -n "$OPEN_COMMAND" ]; then
    jq \
      --arg open_command "$OPEN_COMMAND" \
      --argjson auto_open_attempted "$AUTO_OPEN_ATTEMPTED" \
      --argjson auto_open_success "$AUTO_OPEN_SUCCESS" \
      '. + {open_command: $open_command, auto_open_attempted: $auto_open_attempted, auto_open_success: $auto_open_success}' \
      "$TMP_PARSED"
  else
    jq \
      --argjson auto_open_attempted "$AUTO_OPEN_ATTEMPTED" \
      --argjson auto_open_success "$AUTO_OPEN_SUCCESS" \
      '. + {auto_open_attempted: $auto_open_attempted, auto_open_success: $auto_open_success}' \
      "$TMP_PARSED"
  fi
else
  cat "$TMP_PARSED"
fi
