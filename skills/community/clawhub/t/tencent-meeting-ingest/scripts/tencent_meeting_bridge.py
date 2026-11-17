import datetime as dt
import json
import os
import shlex

from external_skill_bridge import find_sibling_file, run_external_command


def tencent_skill_command():
    configured = os.getenv("TENCENT_MEETING_SKILL_COMMAND") or os.getenv("TENCENT_MEETING_COMMAND")
    if configured:
        return configured
    sibling = find_sibling_file("tencent-meeting-skill", "scripts", "tencent_meeting.py")
    if sibling:
        return "python3 " + shlex.quote(str(sibling))
    sibling = find_sibling_file("tencent-meeting-mcp", "scripts", "tencent_meeting.py")
    if sibling:
        return "python3 " + shlex.quote(str(sibling))
    sibling = find_sibling_file("@wemeeting", "tencent-meeting-skill", "scripts", "tencent_meeting.py")
    if sibling:
        return "python3 " + shlex.quote(str(sibling))
    return ""


def call_tencent_tool(tool_name, arguments=None):
    command = tencent_skill_command()
    if not command:
        raise RuntimeError("未配置 TENCENT_MEETING_SKILL_COMMAND，也未找到已安装的 tencent-meeting-skill / tencent-meeting-mcp。tencent_meeting_ingest 不直连腾讯会议 API，必须通过该 skill 拉取会议内容。")
    args = dict(arguments or {})
    args.setdefault("_client_info", {
        "os": os.getenv("TENCENT_MEETING_CLIENT_OS", "Linux"),
        "agent": os.getenv("TENCENT_MEETING_CLIENT_AGENT", "OpenClaw"),
        "model": os.getenv("TENCENT_MEETING_CLIENT_MODEL", "manual-test"),
    })
    params = {"name": tool_name, "arguments": args}
    return unwrap_tencent_response(run_external_command(command, ["tools/call", json.dumps(params, ensure_ascii=False)], timeout=300))


def unwrap_tencent_response(value):
    if isinstance(value, str):
        text = value.strip()
        parsed = parse_json_text(text)
        if parsed is not None:
            return unwrap_tencent_response(parsed)
        if is_error_text(text):
            raise RuntimeError(text)
        return value
    if isinstance(value, dict):
        wrapped_data = unwrap_transport_data(value.get("data"))
        if wrapped_data is not None:
            return unwrap_tencent_response(wrapped_data)

        status_code = value.get("status_code", value.get("statusCode"))
        if status_code is not None and status_code not in (200, "200"):
            body = value.get("body")
            parsed_body = parse_json_text(body) if isinstance(body, str) else body
            raise RuntimeError(error_message_from_response(parsed_body) or json.dumps(value, ensure_ascii=False))
        body = value.get("body")
        if isinstance(body, str):
            parsed = parse_json_text(body)
            if parsed is not None:
                return parsed
            if is_error_text(body):
                raise RuntimeError(body.strip())
        result = value.get("result")
        if isinstance(result, dict):
            if "error" in result:
                raise RuntimeError(json.dumps(result["error"], ensure_ascii=False))
            content = result.get("content")
            if isinstance(content, list):
                texts = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text = item.get("text") or ""
                        parsed = parse_json_text(text)
                        if parsed is not None:
                            return parsed
                        if is_error_text(text):
                            raise RuntimeError(text.strip())
                        if text:
                            texts.append(text)
                if texts:
                    return "\n".join(texts)
    return value


def unwrap_transport_data(value):
    """Return an outer Skill transport envelope's payload, if present."""
    if isinstance(value, str):
        value = parse_json_text(value)
    if not isinstance(value, dict):
        return None
    if any(key in value for key in ("status_code", "statusCode", "body", "result")):
        return value
    return None


def is_error_text(text):
    if not text:
        return False
    lowered = text.lower()
    stripped = text.lstrip()
    return (
        stripped.startswith("[错误]")
        or stripped.startswith("Error:")
        or stripped.startswith("ERROR:")
        or "usage quota exhausted" in lowered
        or "quota exhausted" in lowered
        or "usage limit" in lowered
        or "500246" in lowered
        or "mcp请求失败" in lowered
        or ("请求失败" in stripped and ("mcp" in lowered or "urlopen" in lowered))
        or "connection reset by peer" in lowered
    )


def parse_json_text(text):
    text = str(text or "").strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char not in "{[":
            continue
        try:
            parsed, _ = decoder.raw_decode(text[index:])
            return parsed
        except Exception:
            continue
    return None


def error_message_from_response(value):
    if not isinstance(value, dict):
        return ""
    for key in ("error_info", "error"):
        error = value.get(key)
        if isinstance(error, dict):
            code = error.get("new_error_code") or error.get("error_code") or error.get("code") or ""
            message = error.get("message") or json.dumps(error, ensure_ascii=False)
            return f"Tencent Meeting MCP error {code}: {message}" if code else f"Tencent Meeting MCP error: {message}"
    message = value.get("message")
    if message:
        return f"Tencent Meeting MCP error: {message}"
    return ""


def meeting_date(source):
    config = source.get("config") or {}
    raw = first_non_empty(source.get("scheduled_time"), source.get("scheduledTime"), config.get("scheduled_time"), config.get("startTime"), config.get("start_time"))
    if isinstance(raw, str) and len(raw) >= 10:
        return raw[:10]
    return dt.date.today().isoformat()


def first_non_empty(*values):
    for value in values:
        if value not in (None, "", []):
            return value
    return ""
