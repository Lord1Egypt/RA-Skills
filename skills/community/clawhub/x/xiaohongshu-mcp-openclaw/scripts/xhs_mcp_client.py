#!/usr/bin/env python3
"""Unified client for xpzouying/xiaohongshu-mcp through mcporter.

Features:
- Discover available MCP tool names dynamically.
- Search notes by keyword.
- Fetch note detail and comments by note id.
- Normalize commonly used fields (title, author, like/comment counts).
"""

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import time
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import quote

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

SEARCH_TOOL_CANDIDATES = [
    "search_feeds",
    "GetFeedsByKeyword",
    "SearchFeeds",
    "SearchByKeyword",
]

DETAIL_TOOL_CANDIDATES = [
    "get_feed_detail",
    "GetFeedById",
    "GetFeedByID",
    "GetNoteById",
    "GetNoteDetail",
]

COMMENTS_TOOL_CANDIDATES = [
    "get_feed_comments",
    "get_feed_detail",
    "GetFeedCommentById",
    "GetFeedCommentsById",
    "GetCommentById",
    "GetCommentsByNoteId",
]

LOGIN_STATUS_TOOL_CANDIDATES = [
    "check_login_status",
    "get_login_status",
    "login_status",
]

LOGIN_QRCODE_TOOL_CANDIDATES = [
    "get_login_qrcode",
    "get_login_qr_code",
    "login_qrcode",
    "login_qr_code",
]

NOTE_ID_KEYS = ["note_id", "noteId", "id", "feed_id", "item_id"]
TITLE_KEYS = ["title", "note_title", "display_title", "displayTitle"]
AUTHOR_KEYS = ["author", "nickname", "nickName", "user_name"]
LIKE_KEYS = ["liked_count", "like_count", "likes", "digg_count", "likedCount", "likeCount"]
COMMENT_COUNT_KEYS = ["comment_count", "comments_count", "reply_count", "commentCount"]
CONTENT_KEYS = ["content", "desc", "text"]
XSEC_KEYS = ["xsec_token", "xsecToken", "token", "xsec"]

COMMENT_ID_KEYS = ["comment_id", "commentId", "id"]
COMMENT_LIST_KEYS = [
    "comments",
    "comment_list",
    "commentList",
    "hot_comments",
    "hotComments",
]


def resolve_base_dir() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)


def build_startup_commands(server: str) -> Dict[str, str]:
    base_dir = resolve_base_dir()
    client = f"python3 {base_dir}/scripts/xhs_mcp_client.py"
    return {
        "start_server": f"bash {base_dir}/scripts/start_server.sh",
        "register_server": f"bash {base_dir}/scripts/register.sh {server}",
        "check_login": f"{client} --server {server} ensure-login --wait-seconds 90",
    }


def build_login_commands(server: str) -> Dict[str, str]:
    base_dir = resolve_base_dir()
    client = f"python3 {base_dir}/scripts/xhs_mcp_client.py"
    return {
        "login_qr": f"bash {base_dir}/scripts/login_qr.sh {server}",
        "ensure_login": f"{client} --server {server} ensure-login --wait-seconds 90",
        "login_flow": f"bash {base_dir}/scripts/login_flow.sh {server} 120",
    }


def strip_ansi(text: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", text)


def balanced_json_slice(text: str) -> Optional[str]:
    if not text:
        return None

    stack: List[str] = []
    in_string = False
    escaped = False
    quote_char = ""

    for idx, ch in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
                continue
            if ch == "\\":
                escaped = True
                continue
            if ch == quote_char:
                in_string = False
            continue

        if ch in ('"', "'"):
            in_string = True
            quote_char = ch
            continue

        if ch in "{[":
            stack.append(ch)
            continue

        if ch in "}]":
            if not stack:
                continue
            opened = stack.pop()
            if (opened == "{" and ch != "}") or (opened == "[" and ch != "]"):
                return None
            if not stack:
                return text[: idx + 1]

    return None


def replace_tokens_outside_strings(text: str, replacements: Dict[str, str]) -> str:
    if not replacements:
        return text

    result: List[str] = []
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


def try_parse_js_object_literal(text: str) -> Any:
    candidate = text.strip()
    if not candidate:
        raise ValueError("empty text")
    if candidate[0] not in "{[":
        raise ValueError("not a structured literal")

    # Convert JS-like object keys to quoted keys so Python literal_eval can parse.
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


def try_parse_structured(text: str) -> Any:
    last_error: Optional[Exception] = None
    try:
        return json.loads(text)
    except Exception as exc:  # pragma: no cover
        last_error = exc

    if yaml is not None:
        try:
            return yaml.safe_load(text)
        except Exception as exc:  # pragma: no cover
            last_error = exc

    try:
        return try_parse_js_object_literal(text)
    except Exception as exc:  # pragma: no cover
        last_error = exc

    if last_error is not None:
        raise last_error
    raise ValueError("unable to parse payload text")


def run_command(cmd: List[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    stderr = (proc.stderr or "").strip()
    stdout = (proc.stdout or "").strip()

    if proc.returncode != 0:
        raise RuntimeError(
            f"command failed: {' '.join(cmd)}\nstdout: {stdout}\nstderr: {stderr}"
        )

    if "Unknown MCP server" in stderr:
        raise RuntimeError(
            f"unknown server for command: {' '.join(cmd)}\nstderr: {stderr}"
        )

    if not stdout and stderr:
        raise RuntimeError(
            f"command returned empty stdout: {' '.join(cmd)}\nstderr: {stderr}"
        )

    return proc.stdout


def load_json(text: str) -> Any:
    text = strip_ansi(text).strip()
    if not text:
        return None

    candidates: List[str] = [text]
    first_obj = text.find("{")
    first_arr = text.find("[")
    starts = [x for x in (first_obj, first_arr) if x >= 0]
    if starts:
        sliced = text[min(starts):]
        candidates.append(sliced)
        balanced = balanced_json_slice(sliced)
        if balanced:
            candidates.append(balanced)

    for match in re.finditer(r"```(?:json)?\s*([\s\S]*?)```", text, flags=re.IGNORECASE):
        block = match.group(1).strip()
        if block:
            candidates.append(block)

    seen = set()
    last_exc: Optional[Exception] = None
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        try:
            return try_parse_structured(candidate)
        except Exception as exc:  # pragma: no cover
            last_exc = exc
            continue

    if last_exc is not None:
        raise last_exc
    raise ValueError("failed to parse response text")


def list_tools(server: str, timeout_ms: int = 20000) -> List[Dict[str, Any]]:
    output = run_command(
        [
            "mcporter",
            "list",
            server,
            "--json",
            "--schema",
            "--timeout",
            str(timeout_ms),
        ]
    )
    payload = load_json(output)
    if payload is None:
        raise RuntimeError("empty response from mcporter list")

    if isinstance(payload, dict):
        if payload.get("status") == "offline":
            issue = payload.get("issue") or {}
            issue_msg = issue.get("rawMessage") if isinstance(issue, dict) else ""
            raise RuntimeError(f"server is offline: {issue_msg or payload.get('error')}")
        if payload.get("error"):
            raise RuntimeError(str(payload.get("error")))

    if isinstance(payload, dict) and isinstance(payload.get("tools"), list):
        return payload["tools"]

    if isinstance(payload, dict) and isinstance(payload.get("servers"), list):
        for server_info in payload["servers"]:
            tools = server_info.get("tools")
            if isinstance(tools, list):
                return tools

    return []


def choose_tool_name(tools: Iterable[Dict[str, Any]], candidates: List[str]) -> Optional[str]:
    tool_names = [t.get("name") for t in tools if isinstance(t.get("name"), str)]
    name_lookup = {name.lower(): name for name in tool_names}

    for candidate in candidates:
        if candidate.lower() in name_lookup:
            return name_lookup[candidate.lower()]

    for name in tool_names:
        lower_name = name.lower()
        for candidate in candidates:
            lower_candidate = candidate.lower()
            if lower_candidate in lower_name or lower_name in lower_candidate:
                return name

    return None


def schema_properties(tool: Dict[str, Any]) -> Dict[str, Any]:
    schema = tool.get("inputSchema") or tool.get("input_schema")
    if not isinstance(schema, dict):
        return {}
    properties = schema.get("properties")
    if isinstance(properties, dict):
        return properties
    return {}


def pick_param_name(props: Dict[str, Any], candidates: List[str]) -> Optional[str]:
    lowered = {k.lower(): k for k in props.keys()}
    for candidate in candidates:
        if candidate.lower() in lowered:
            return lowered[candidate.lower()]

    for key in props.keys():
        lkey = key.lower()
        for candidate in candidates:
            lcand = candidate.lower()
            if lcand in lkey or lkey in lcand:
                return key
    return None


def call_tool(server: str, tool: str, args: Dict[str, Any], timeout_ms: int = 30000) -> Any:
    cmd = [
        "mcporter",
        "call",
        f"{server}.{tool}",
        "--output",
        "json",
        "--timeout",
        str(timeout_ms),
    ]

    for key, value in args.items():
        if value is None:
            continue
        cmd.append(f"{key}={value}")

    output = run_command(cmd)
    try:
        result = load_json(output)
    except Exception:
        # Some mcporter/tool versions return non-standard JSON-like text.
        # Keep the raw text so upper layers can degrade gracefully.
        result = {"content": [{"type": "text", "text": output.strip()}]}
    if isinstance(result, dict) and result.get("error"):
        raise RuntimeError(f"{tool} failed: {result.get('error')}")
    return result


def maybe_parse_json_text(text: str) -> Any:
    text = text.strip()
    if not text:
        return text
    if (text.startswith("{") and text.endswith("}")) or (
        text.startswith("[") and text.endswith("]")
    ):
        try:
            return try_parse_structured(text)
        except Exception:
            return text
    return text


def stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=False)
    except Exception:
        return str(value)


def coerce_bool(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        if value in (0, 1):
            return bool(value)
        return None
    if not isinstance(value, str):
        return None

    text = value.strip().lower()
    if not text:
        return None

    true_set = {"true", "1", "yes", "y", "ok", "success"}
    false_set = {"false", "0", "no", "n", "fail", "failed", "error"}
    if text in true_set:
        return True
    if text in false_set:
        return False
    return None


def iter_nested_items(value: Any, prefix: str = "") -> Iterable[Tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_key = f"{prefix}.{key}" if prefix else str(key)
            yield child_key, child
            yield from iter_nested_items(child, child_key)
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            child_key = f"{prefix}[{idx}]"
            yield from iter_nested_items(child, child_key)


def text_login_signal(text: str) -> Optional[bool]:
    if not text:
        return None
    lower = text.lower()

    negative_markers = [
        "未登录",
        "请登录",
        "登录失败",
        "fail to login",
        "not logged",
        "not login",
        "need login",
        "login required",
        "unlogin",
    ]
    positive_markers = [
        "已登录",
        "登录成功",
        "logged in",
        "login success",
        "already logged in",
    ]

    if any(marker.lower() in lower for marker in negative_markers):
        return False
    if any(marker.lower() in lower for marker in positive_markers):
        return True
    return None


def structured_login_state(payload: Any) -> Optional[bool]:
    login_key_tokens = ["logged", "login"]
    text_key_tokens = ["status", "state", "message", "msg", "desc", "text", "title"]

    # Pass 1: explicit login keys with bool-like values.
    for key, value in iter_nested_items(payload):
        lower_key = key.lower()
        if not any(token in lower_key for token in login_key_tokens):
            continue
        bool_value = coerce_bool(value)
        if bool_value is not None:
            return bool_value
        if isinstance(value, str):
            signal = text_login_signal(value)
            if signal is not None:
                return signal

    # Pass 2: common status/message fields.
    for key, value in iter_nested_items(payload):
        lower_key = key.lower()
        if not any(token in lower_key for token in text_key_tokens):
            continue
        if isinstance(value, str):
            signal = text_login_signal(value)
            if signal is not None:
                return signal

    return None


def is_logged_in_payload(payload: Any) -> bool:
    structured_state = structured_login_state(payload)
    if structured_state is not None:
        return structured_state

    text = stringify(payload)
    signal = text_login_signal(text)
    if signal is not None:
        return signal
    return False


def extract_first_url(value: Any) -> Optional[str]:
    text = stringify(value)
    match = re.search(r"https?://[^\s\"'<>]+", text)
    if match:
        return match.group(0)
    return None


def strip_embedded_image_data(payload: Any) -> Any:
    if isinstance(payload, list):
        return [strip_embedded_image_data(item) for item in payload]

    if isinstance(payload, dict):
        copied: Dict[str, Any] = {}
        for key, value in payload.items():
            copied[key] = strip_embedded_image_data(value)

        item_type = str(copied.get("type", "")).lower()
        data = copied.get("data")
        if item_type == "image" and isinstance(data, str):
            copied["data_length"] = len(data)
            copied["data_preview"] = f"{data[:32]}..." if len(data) > 32 else data
            copied.pop("data", None)
        return copied

    return payload


def classify_error(message: str, server: str = "xiaohongshu-mcp") -> Dict[str, Any]:
    msg = (message or "").strip()
    lower = msg.lower()

    if "unknown mcp server" in lower or "unknown server" in lower:
        startup_cmds = build_startup_commands(server)
        return {
            "error_type": "server_unregistered",
            "suggested_action": "Register MCP server name first, then retry query.",
            "next_commands": [
                startup_cmds["register_server"],
                startup_cmds["check_login"],
            ],
        }

    if (
        "未登录" in msg
        or "请登录" in msg
        or "not logged" in lower
        or "not login" in lower
        or "login required" in lower
        ):
        login_cmds = build_login_commands(server)
        return {
            "error_type": "login_required",
            "suggested_action": "Run login_qr first, complete scan/captcha, then retry query.",
            "next_commands": [
                login_cmds["login_qr"],
                login_cmds["ensure_login"],
            ],
        }

    if (
        "验证码" in msg
        or "滑块" in msg
        or "captcha" in lower
        or "fail to login" in lower
        or "登录失败" in msg
    ):
        login_cmds = build_login_commands(server)
        return {
            "error_type": "human_verification_required",
            "suggested_action": "Complete human verification, then rerun login flow.",
            "next_commands": [
                login_cmds["login_qr"],
                login_cmds["login_flow"],
            ],
        }

    if "timed out" in lower or "timeout" in lower:
        return {
            "error_type": "timeout",
            "suggested_action": (
                "Increase --timeout (e.g. 60000), verify server health, and retry."
            ),
        }

    if "econnrefused" in lower or "server is offline" in lower:
        startup_cmds = build_startup_commands(server)
        return {
            "error_type": "server_offline",
            "suggested_action": "Service is not started. Start and register MCP server before retry.",
            "next_commands": [
                startup_cmds["start_server"],
                startup_cmds["register_server"],
                startup_cmds["check_login"],
            ],
        }

    if "sorry, this page isn't available right now" in lower or "笔记不可访问" in msg:
        return {
            "error_type": "note_not_accessible",
            "suggested_action": "This note is not accessible for current account/session. Try another note.",
        }

    return {
        "error_type": "unknown",
        "suggested_action": "Check login status, server health, and MCP registration.",
    }


def extract_error_text(payload: Any) -> Optional[str]:
    text = stringify(payload)
    lowered = text.lower()
    markers = [
        "获取Feed详情失败",
        "笔记不可访问",
        "sorry, this page isn't available right now",
        "未登录",
        "请登录",
        "验证码",
        "滑块",
    ]
    for marker in markers:
        if marker.lower() in lowered:
            return text
    return None


def extract_payload(envelope: Any) -> Any:
    if envelope is None:
        return None

    if isinstance(envelope, dict):
        for key in ("payload", "result", "data"):
            value = envelope.get(key)
            if isinstance(value, (dict, list)):
                return value

        for key in ("response", "output"):
            value = envelope.get(key)
            if isinstance(value, dict):
                nested = extract_payload(value)
                if nested is not None:
                    return nested

        content = envelope.get("content")
        if isinstance(content, list):
            for item in content:
                if not isinstance(item, dict):
                    continue
                if "json" in item and isinstance(item["json"], (dict, list)):
                    return item["json"]
                if isinstance(item.get("text"), str):
                    parsed = maybe_parse_json_text(item["text"])
                    if isinstance(parsed, (dict, list)):
                        return parsed

    return envelope


def walk_dicts(value: Any):
    if isinstance(value, dict):
        yield value
        for v in value.values():
            yield from walk_dicts(v)
    elif isinstance(value, list):
        for item in value:
            yield from walk_dicts(item)


def find_value(obj: Any, keys: List[str]) -> Any:
    if not isinstance(obj, dict):
        return None

    for key in keys:
        lower_key = key.lower()
        for actual in obj.keys():
            if actual.lower() != lower_key:
                continue
            value = obj.get(actual)
            if value not in (None, ""):
                return value

    for nested in walk_dicts(obj):
        if nested is obj:
            continue
        for key in keys:
            lower_key = key.lower()
            for actual in nested.keys():
                if actual.lower() != lower_key:
                    continue
                value = nested.get(actual)
                if value not in (None, ""):
                    return value

    return None


def to_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        stripped = value.replace(",", "").strip()
        if stripped.endswith("万"):
            try:
                return int(float(stripped[:-1]) * 10000)
            except ValueError:
                return None
        if stripped.endswith("亿"):
            try:
                return int(float(stripped[:-1]) * 100000000)
            except ValueError:
                return None
        if stripped.isdigit():
            return int(stripped)
    return None


def flatten_items(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]

    if isinstance(payload, dict):
        for key in ("items", "list", "feeds", "notes", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]

        if "item" in payload and isinstance(payload["item"], dict):
            return [payload["item"]]

        return [payload]

    return []


def extract_comment_items(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]

    def from_container(container: Dict[str, Any]) -> List[Dict[str, Any]]:
        for key in COMMENT_LIST_KEYS:
            value = container.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
            if isinstance(value, dict):
                for inner_key in ("list", "items", "comments"):
                    inner_val = value.get(inner_key)
                    if isinstance(inner_val, list):
                        return [item for item in inner_val if isinstance(item, dict)]
        return []

    if isinstance(payload, dict):
        direct = from_container(payload)
        if direct:
            return direct

        for nested in walk_dicts(payload):
            nested_items = from_container(nested)
            if nested_items:
                return nested_items

    return flatten_items(payload)


def normalize_note(item: Dict[str, Any]) -> Dict[str, Any]:
    note_id = find_value(item, NOTE_ID_KEYS)
    title = find_value(item, TITLE_KEYS)
    author = find_value(item, AUTHOR_KEYS)
    if not author and isinstance(item.get("user"), dict):
        user = item.get("user", {})
        author = user.get("nickname") or user.get("nickName")
    like_count = to_int(find_value(item, LIKE_KEYS))
    comment_count = to_int(find_value(item, COMMENT_COUNT_KEYS))
    content = find_value(item, CONTENT_KEYS)
    xsec_token = find_value(item, XSEC_KEYS)
    url = None
    if isinstance(note_id, str) and note_id:
        base = f"https://www.xiaohongshu.com/explore/{note_id}"
        if isinstance(xsec_token, str) and xsec_token:
            url = (
                f"{base}?xsec_token={quote(xsec_token, safe='')}"
                "&xsec_source=pc_search"
            )
        else:
            url = base

    normalized = {
        "note_id": note_id,
        "title": title,
        "author": author,
        "like_count": like_count,
        "comment_count": comment_count,
        "content": content,
        "xsec_token": xsec_token,
        "url": url,
    }

    return normalized


def normalize_comment(item: Dict[str, Any]) -> Dict[str, Any]:
    comment_id = find_value(item, COMMENT_ID_KEYS)
    author = find_value(item, AUTHOR_KEYS)
    if not author and isinstance(item.get("userInfo"), dict):
        user = item.get("userInfo", {})
        author = user.get("nickname") or user.get("nickName")
    content = find_value(item, CONTENT_KEYS)
    if not isinstance(content, str):
        content = None
    if not isinstance(author, str):
        author = None
    like_count = to_int(find_value(item, LIKE_KEYS))
    return {
        "comment_id": comment_id,
        "author": author,
        "content": content,
        "like_count": like_count,
    }


def print_json(data: Any):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def require_tool(tools: List[Dict[str, Any]], candidates: List[str], op_name: str) -> Tuple[str, Dict[str, Any]]:
    tool_name = choose_tool_name(tools, candidates)
    if not tool_name:
        available = [t.get("name") for t in tools if t.get("name")]
        raise RuntimeError(
            f"cannot find a tool for '{op_name}'. Available tools: {available}"
        )

    tool_obj = next((t for t in tools if t.get("name") == tool_name), {})
    return tool_name, schema_properties(tool_obj)


def do_search(args: argparse.Namespace, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
    tool_name, props = require_tool(tools, SEARCH_TOOL_CANDIDATES, "search")
    keyword_key = pick_param_name(props, ["keyword", "query", "q"])
    if not keyword_key:
        raise RuntimeError(f"search tool '{tool_name}' has no keyword-like parameter")

    limit_key = pick_param_name(props, ["limit", "count", "size", "num", "page_size"])

    call_args = {keyword_key: args.keyword}
    if limit_key and args.limit is not None:
        call_args[limit_key] = args.limit

    raw = call_tool(args.server, tool_name, call_args, timeout_ms=args.timeout)
    payload = extract_payload(raw)
    notes = []
    for raw_item in flatten_items(payload):
        model_type = find_value(raw_item, ["modelType", "model_type"])
        note_id = find_value(raw_item, NOTE_ID_KEYS)
        if model_type and str(model_type).lower() != "note":
            continue
        if isinstance(note_id, str) and "#" in note_id:
            continue
        notes.append(normalize_note(raw_item))

    return {
        "tool": tool_name,
        "request_args": call_args,
        "raw_response": raw,
        "normalized": notes[: args.limit] if args.limit else notes,
    }


def do_detail(args: argparse.Namespace, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
    tool_name, props = require_tool(tools, DETAIL_TOOL_CANDIDATES, "detail")
    note_key = pick_param_name(props, ["note_id", "noteId", "id", "feed_id", "item_id"])
    xsec_key = pick_param_name(props, ["xsec_token", "xsecToken", "xsec", "token"])

    if not note_key:
        raise RuntimeError(f"detail tool '{tool_name}' has no note-id parameter")

    call_args = {note_key: args.note_id}
    if xsec_key and args.xsec_token:
        call_args[xsec_key] = args.xsec_token

    raw = call_tool(args.server, tool_name, call_args, timeout_ms=args.timeout)
    embedded_error = extract_error_text(raw)
    if embedded_error:
        raise RuntimeError(embedded_error)

    payload = extract_payload(raw)
    detail_items = flatten_items(payload)
    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, dict) and isinstance(data.get("note"), dict):
            detail_items = [data["note"]]
    notes = [normalize_note(x) for x in detail_items]

    return {
        "tool": tool_name,
        "request_args": call_args,
        "raw_response": raw,
        "normalized": notes[0] if notes else {},
    }


def do_comments(args: argparse.Namespace, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
    tool_name, props = require_tool(tools, COMMENTS_TOOL_CANDIDATES, "comments")
    note_key = pick_param_name(props, ["note_id", "noteId", "id", "feed_id", "item_id"])
    xsec_key = pick_param_name(props, ["xsec_token", "xsecToken", "xsec", "token"])
    limit_key = pick_param_name(props, ["limit", "count", "size", "num", "page_size"])

    if not note_key:
        raise RuntimeError(f"comments tool '{tool_name}' has no note-id parameter")

    call_args = {note_key: args.note_id}
    if xsec_key and args.xsec_token:
        call_args[xsec_key] = args.xsec_token
    if limit_key and args.limit is not None:
        call_args[limit_key] = args.limit

    raw = call_tool(args.server, tool_name, call_args, timeout_ms=args.timeout)
    embedded_error = extract_error_text(raw)
    if embedded_error:
        raise RuntimeError(embedded_error)

    payload = extract_payload(raw)
    comment_items = extract_comment_items(payload)
    comments = [normalize_comment(x) for x in comment_items]

    comments = [
        c
        for c in comments
        if (isinstance(c.get("content"), str) and c.get("content").strip())
        or (isinstance(c.get("author"), str) and c.get("author").strip())
    ]
    comments.sort(key=lambda c: c.get("like_count") or -1, reverse=True)

    if args.limit:
        comments = comments[: args.limit]

    return {
        "tool": tool_name,
        "request_args": call_args,
        "raw_response": raw,
        "normalized": comments,
    }


def do_login_status(args: argparse.Namespace, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
    tool_name, _ = require_tool(tools, LOGIN_STATUS_TOOL_CANDIDATES, "login_status")
    raw = call_tool(args.server, tool_name, {}, timeout_ms=args.timeout)
    payload = extract_payload(raw)
    return {
        "tool": tool_name,
        "raw_response": raw,
        "normalized": payload,
    }


def do_ensure_login(
    args: argparse.Namespace,
    tools: List[Dict[str, Any]],
    *,
    request_qrcode: bool = True,
    wait_seconds: Optional[int] = None,
    poll_interval: Optional[int] = None,
) -> Dict[str, Any]:
    wait_seconds_final = (
        wait_seconds
        if wait_seconds is not None
        else int(getattr(args, "wait_seconds", 0) or 0)
    )
    poll_interval_final = (
        poll_interval
        if poll_interval is not None
        else int(getattr(args, "poll_interval", 3) or 3)
    )
    poll_interval_final = max(1, poll_interval_final)

    status_data = do_login_status(args, tools)
    normalized_status = status_data.get("normalized")
    already_logged_in = is_logged_in_payload(normalized_status)

    result: Dict[str, Any] = {
        "already_logged_in": already_logged_in,
        "login_status": normalized_status,
    }

    if already_logged_in:
        return result

    if request_qrcode:
        qrcode_tool, _ = require_tool(tools, LOGIN_QRCODE_TOOL_CANDIDATES, "login_qrcode")
        raw = call_tool(args.server, qrcode_tool, {}, timeout_ms=args.timeout)
        payload = extract_payload(raw)
        include_qr_image = bool(getattr(args, "include_qr_image", False))
        strip_qr_image = bool(getattr(args, "strip_qr_image", False))
        include_qr_raw = bool(getattr(args, "include_qr_raw", False))
        if include_qr_image:
            strip_qr_image = False
        payload_for_output = strip_embedded_image_data(payload) if strip_qr_image else payload

        result.update(
            {
                "qr_tool": qrcode_tool,
                "qr_payload": payload_for_output,
                "qr_url_hint": extract_first_url(payload_for_output),
                "qr_image_included": not strip_qr_image,
            }
        )
        if include_qr_raw:
            result["qr_raw_response"] = raw

    if wait_seconds_final <= 0:
        return result

    start = time.time()
    deadline = start + wait_seconds_final
    poll_count = 0

    while time.time() < deadline:
        time.sleep(poll_interval_final)
        poll_count += 1
        latest = do_login_status(args, tools)
        latest_payload = latest.get("normalized")
        if is_logged_in_payload(latest_payload):
            result["already_logged_in"] = True
            result["login_status"] = latest_payload
            result["wait_result"] = {
                "logged_in": True,
                "poll_count": poll_count,
                "elapsed_seconds": int(time.time() - start),
            }
            return result

    result["wait_result"] = {
        "logged_in": False,
        "poll_count": poll_count,
        "elapsed_seconds": int(time.time() - start),
    }
    return result


def do_login_precheck(args: argparse.Namespace, tools: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if bool(getattr(args, "skip_login_check", False)):
        return None

    wait_seconds = int(getattr(args, "auto_login_wait_seconds", 0) or 0)
    poll_interval = int(getattr(args, "auto_login_poll_interval", 3) or 3)
    precheck = do_ensure_login(
        args,
        tools,
        request_qrcode=False,
        wait_seconds=wait_seconds,
        poll_interval=poll_interval,
    )
    if precheck.get("already_logged_in"):
        return None

    message = (
        "login precheck failed: current account is not logged in. "
        "Run ensure-login and complete QR/captcha verification first."
    )
    error_info = classify_error(message, args.server)
    next_command = None
    next_commands = error_info.get("next_commands")
    if isinstance(next_commands, list) and next_commands:
        next_command = str(next_commands[0])
    return {
        "error": "login_precheck_failed",
        "cmd": getattr(args, "cmd", ""),
        "server": args.server,
        "message": message,
        "error_type": error_info["error_type"],
        "suggested_action": error_info["suggested_action"],
        "precheck": precheck,
        "next_command": next_command,
        "next_commands": next_commands,
    }


def do_report(args: argparse.Namespace, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
    search_args = argparse.Namespace(
        server=args.server,
        keyword=args.keyword,
        limit=args.search_limit,
        timeout=args.timeout,
    )
    search_data = do_search(search_args, tools)

    report_items = []
    errors = []
    for note in search_data.get("normalized", []):
        note_id = note.get("note_id")
        if not note_id:
            continue

        xsec_token = note.get("xsec_token")

        detail_args = argparse.Namespace(
            server=args.server,
            note_id=note_id,
            xsec_token=xsec_token,
            timeout=args.timeout,
        )
        comments_args = argparse.Namespace(
            server=args.server,
            note_id=note_id,
            xsec_token=xsec_token,
            limit=args.comment_limit,
            timeout=args.timeout,
        )

        try:
            detail_data = do_detail(detail_args, tools)
            comments_data = do_comments(comments_args, tools)

            search_note = dict(note) if isinstance(note, dict) else {}
            detail_note = detail_data.get("normalized")
            if not isinstance(detail_note, dict):
                detail_note = {}

            # Prefer detail fields when present, but keep search fields as fallback.
            merged_note = dict(search_note)
            for key, value in detail_note.items():
                if value not in (None, ""):
                    merged_note[key] = value

            merged_note["top_comments"] = comments_data.get("normalized", [])
            report_items.append(merged_note)
        except Exception as exc:
            fallback = dict(note)
            fallback["top_comments"] = []
            fallback["error"] = str(exc)
            report_items.append(fallback)
            errors.append({"note_id": note_id, "message": str(exc)})

    return {
        "keyword": args.keyword,
        "search_limit": args.search_limit,
        "comment_limit": args.comment_limit,
        "normalized": report_items,
        "errors": errors,
        "raw_search_response": search_data.get("raw_response"),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="xiaohongshu-mcp client wrapper")
    parser.add_argument("--server", default="xiaohongshu-mcp", help="mcporter server name")
    parser.add_argument("--timeout", type=int, default=30000, help="mcporter call timeout in ms")
    parser.add_argument(
        "--skip-login-check",
        action="store_true",
        help="skip login precheck before query commands (search/detail/comments/report)",
    )
    parser.add_argument(
        "--auto-login-wait-seconds",
        type=int,
        default=0,
        help="for precheck, wait and poll login status up to this many seconds before failing",
    )
    parser.add_argument(
        "--auto-login-poll-interval",
        type=int,
        default=3,
        help="for precheck login polling, interval in seconds",
    )

    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("tools", help="list discovered tools")
    sub.add_parser("login-status", help="check xiaohongshu login status")
    sub.add_parser(
        "ensure-login",
        help="if already logged in, return status only; otherwise return QR payload",
    )
    p_ensure = sub.choices["ensure-login"]
    p_ensure.add_argument("--wait-seconds", type=int, default=0)
    p_ensure.add_argument("--poll-interval", type=int, default=3)
    p_ensure.add_argument("--no-qrcode", action="store_true")
    p_ensure.add_argument(
        "--include-qr-image",
        action="store_true",
        help="compatibility flag: full QR image is included by default",
    )
    p_ensure.add_argument(
        "--strip-qr-image",
        action="store_true",
        help="strip full QR image base64 from output payload",
    )
    p_ensure.add_argument(
        "--include-qr-raw",
        action="store_true",
        help="include raw MCP response envelope for QR tool",
    )

    p_search = sub.add_parser("search", help="search notes by keyword")
    p_search.add_argument("--keyword", required=True)
    p_search.add_argument("--limit", type=int, default=5)

    p_detail = sub.add_parser("detail", help="get note detail by note id")
    p_detail.add_argument("--note-id", required=True)
    p_detail.add_argument("--xsec-token", default=None)

    p_comments = sub.add_parser("comments", help="get note comments by note id")
    p_comments.add_argument("--note-id", required=True)
    p_comments.add_argument("--xsec-token", default=None)
    p_comments.add_argument("--limit", type=int, default=10)

    p_report = sub.add_parser("report", help="search + detail + comments")
    p_report.add_argument("--keyword", required=True)
    p_report.add_argument("--search-limit", type=int, default=3)
    p_report.add_argument("--comment-limit", type=int, default=3)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        tools = list_tools(args.server, timeout_ms=args.timeout)
    except Exception as exc:
        err_info = classify_error(str(exc), args.server)
        result: Dict[str, Any] = {
            "error": "list_tools_failed",
            "server": args.server,
            "message": str(exc),
            "error_type": err_info["error_type"],
            "suggested_action": err_info["suggested_action"],
        }
        next_commands = err_info.get("next_commands")
        if isinstance(next_commands, list) and next_commands:
            result["next_commands"] = next_commands
            result["next_command"] = str(next_commands[0])
        if err_info["error_type"] == "server_offline":
            result["message"] = (
                "xiaohongshu-mcp service is not started or unreachable. "
                "Please run startup commands first."
            )
            result["suggested_action"] = "Run start + register, then retry your query."
        print_json(
            result
        )
        return 1

    if args.cmd == "tools":
        summary = []
        for tool in tools:
            summary.append(
                {
                    "name": tool.get("name"),
                    "description": tool.get("description"),
                    "parameters": sorted(schema_properties(tool).keys()),
                }
            )
        print_json({"server": args.server, "tools": summary})
        return 0

    if args.cmd in {"search", "detail", "comments", "report"}:
        precheck_error = do_login_precheck(args, tools)
        if precheck_error is not None:
            print_json(precheck_error)
            return 1

    try:
        if args.cmd == "search":
            result = do_search(args, tools)
        elif args.cmd == "detail":
            result = do_detail(args, tools)
        elif args.cmd == "comments":
            result = do_comments(args, tools)
        elif args.cmd == "login-status":
            result = do_login_status(args, tools)
        elif args.cmd == "ensure-login":
            result = do_ensure_login(
                args,
                tools,
                request_qrcode=not bool(getattr(args, "no_qrcode", False)),
            )
        elif args.cmd == "report":
            result = do_report(args, tools)
        else:
            raise RuntimeError(f"unsupported cmd: {args.cmd}")
    except Exception as exc:
        err_info = classify_error(str(exc), args.server)
        result = {
            "error": "tool_call_failed",
            "cmd": args.cmd,
            "server": args.server,
            "message": str(exc),
            "error_type": err_info["error_type"],
            "suggested_action": err_info["suggested_action"],
        }
        next_commands = err_info.get("next_commands")
        if isinstance(next_commands, list) and next_commands:
            result["next_commands"] = next_commands
            result["next_command"] = str(next_commands[0])
        print_json(result)
        return 1

    print_json(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
