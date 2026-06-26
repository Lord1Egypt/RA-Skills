#!/usr/bin/env python3
"""
Minimal Volcengine ARK web search runner.

Defaults:
- Uses the Responses API.
- Enables the `web_search` tool.
- Returns markdown-friendly output in Chinese-oriented style.
- Supports dry runs for validation without network calls.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Any

DEFAULT_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DEFAULT_MODEL = "doubao-seed-1-6-250615"
DEFAULT_SYSTEM_PROMPT = (
    "You are a web research assistant. Answer in Chinese by default. "
    "When the user asks about today, recently, or the latest updates, prefer explicit dates. "
    "Return a concise summary body only. Do not add markdown headings, titles, or a sources section. "
    "Source links are handled by the caller."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search the public web through Volcengine ARK Responses API.",
    )
    parser.add_argument("query", help="Search prompt to send to the ARK model.")
    parser.add_argument(
        "--model",
        default=os.getenv("ARK_MODEL", DEFAULT_MODEL),
        help="ARK model id. Defaults to ARK_MODEL or %(default)s.",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("ARK_BASE_URL", DEFAULT_BASE_URL),
        help="ARK base URL. Defaults to ARK_BASE_URL or %(default)s.",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("ARK_API_KEY"),
        help="ARK API key. Defaults to ARK_API_KEY.",
    )
    parser.add_argument(
        "--max-keyword",
        type=int,
        default=2,
        help="web_search max_keyword value.",
    )
    parser.add_argument(
        "--search-context-size",
        choices=("low", "medium", "high"),
        help="Optional web_search search_context_size value. If ARK rejects it, the script retries without it.",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Use the streaming API and consume SSE events.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json", "raw"),
        default="markdown",
        help="Output format. Defaults to %(default)s.",
    )
    parser.add_argument(
        "--system-prompt",
        default=DEFAULT_SYSTEM_PROMPT,
        help="System prompt inserted before the user query.",
    )
    parser.add_argument(
        "--no-system-prompt",
        action="store_true",
        help="Send only the user query with no default system prompt.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="HTTP timeout per attempt in seconds. Defaults to %(default)s.",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=2,
        help="Retry transient failures this many times after the initial attempt. Defaults to %(default)s.",
    )
    parser.add_argument(
        "--retry-delay",
        type=float,
        default=1.0,
        help="Seconds to wait between retries. Defaults to %(default)s.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request payload and exit without sending network traffic.",
    )
    return parser.parse_args()


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    tool: dict[str, Any] = {
        "type": "web_search",
        "max_keyword": args.max_keyword,
    }
    if args.search_context_size:
        tool["search_context_size"] = args.search_context_size

    input_items: list[dict[str, Any]] = []
    if not args.no_system_prompt and args.system_prompt:
        input_items.append(
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": args.system_prompt,
                    }
                ],
            }
        )

    input_items.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": args.query,
                }
            ],
        }
    )

    return {
        "model": args.model,
        "stream": args.stream,
        "tools": [tool],
        "input": input_items,
    }


def create_request(url: str, api_key: str, payload: dict[str, Any], stream: bool) -> urllib.request.Request:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if stream:
        headers["Accept"] = "text/event-stream"
    return urllib.request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )


def payload_has_search_context_size(payload: dict[str, Any]) -> bool:
    tools = payload.get("tools")
    if not isinstance(tools, list):
        return False
    for tool in tools:
        if isinstance(tool, dict) and "search_context_size" in tool:
            return True
    return False


def strip_search_context_size(payload: dict[str, Any]) -> None:
    tools = payload.get("tools")
    if not isinstance(tools, list):
        return
    for tool in tools:
        if isinstance(tool, dict):
            tool.pop("search_context_size", None)


def looks_like_unsupported_search_context_size(code: int, body: str) -> bool:
    if code != 400:
        return False
    normalized = body.lower()
    if "search_context_size" not in normalized:
        return False
    keywords = (
        "unsupported",
        "not support",
        "not supported",
        "unknown",
        "unexpected",
        "unrecognized",
        "invalid",
        "not allowed",
        "does not support",
        "参数",
        "不支持",
        "未知",
        "非法",
    )
    return any(keyword in normalized for keyword in keywords)


def is_retryable_http_status(code: int) -> bool:
    return code in (408, 409, 425, 429, 500, 502, 503, 504)


def recursive_walk(node: Any):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from recursive_walk(value)
    elif isinstance(node, list):
        for item in node:
            yield from recursive_walk(item)


def extract_text_from_block(block: dict[str, Any]) -> list[str]:
    texts: list[str] = []
    block_type = block.get("type")
    text_value = block.get("text")

    if isinstance(text_value, str) and block_type in (None, "text", "output_text"):
        texts.append(text_value)
    elif isinstance(text_value, dict):
        nested = text_value.get("value")
        if isinstance(nested, str):
            texts.append(nested)

    if block_type == "output_text":
        delta = block.get("delta")
        if isinstance(delta, str):
            texts.append(delta)

    return texts


def extract_output_text(response_obj: dict[str, Any]) -> str:
    direct = response_obj.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct.strip()

    texts: list[str] = []
    output_items = response_obj.get("output")
    if isinstance(output_items, list):
        for item in output_items:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict):
                        texts.extend(extract_text_from_block(block))

    if texts:
        joined = "\n".join(part.strip() for part in texts if isinstance(part, str) and part.strip())
        if joined.strip():
            return joined.strip()

    fallback: list[str] = []
    for node in recursive_walk(response_obj.get("output")):
        if node.get("type") in ("text", "output_text"):
            fallback.extend(extract_text_from_block(node))

    joined = "\n".join(part.strip() for part in fallback if isinstance(part, str) and part.strip())
    return joined.strip()


def extract_sources(response_obj: dict[str, Any]) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for node in recursive_walk(response_obj):
        if not isinstance(node, dict):
            continue
        url = node.get("url") or node.get("href")
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            continue
        title = node.get("title") or node.get("name") or node.get("display_text") or url
        if not isinstance(title, str):
            title = url
        key = (title.strip(), url.strip())
        if key in seen:
            continue
        seen.add(key)
        results.append(
            {
                "title": title.strip() or url.strip(),
                "url": url.strip(),
            }
        )

    return results


def normalize_response(response_obj: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    query = ""
    input_items = payload.get("input")
    if isinstance(input_items, list):
        for item in input_items:
            if not isinstance(item, dict) or item.get("role") != "user":
                continue
            content = item.get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if isinstance(block, dict) and isinstance(block.get("text"), str):
                    query = block["text"].strip()
                    break
            if query:
                break

    return {
        "id": response_obj.get("id"),
        "model": response_obj.get("model") or payload.get("model"),
        "status": response_obj.get("status"),
        "query": query,
        "title": query or "ARK Web Search Result",
        "answer": extract_output_text(response_obj),
        "sources": extract_sources(response_obj),
        "raw": response_obj,
    }


def find_stream_delta(event_name: str | None, payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""

    payload_type = payload.get("type")
    if event_name == "response.output_text.delta" or payload_type == "response.output_text.delta":
        delta = payload.get("delta")
        if isinstance(delta, str):
            return delta

    if event_name and "output_text" in event_name:
        delta = payload.get("delta")
        if isinstance(delta, str):
            return delta

    for node in recursive_walk(payload):
        if not isinstance(node, dict):
            continue
        if node.get("type") == "response.output_text.delta" and isinstance(node.get("delta"), str):
            return node["delta"]
        if isinstance(node.get("delta"), str) and node.get("type") == "output_text":
            return node["delta"]

    return ""


def stream_response(
    request: urllib.request.Request,
    timeout: int,
    output_format: str,
) -> tuple[dict[str, Any], bool]:
    collected_text_parts: list[str] = []
    final_response: dict[str, Any] | None = None
    event_name: str | None = None
    data_lines: list[str] = []

    def flush_event() -> None:
        nonlocal event_name, data_lines, final_response
        if not data_lines:
            event_name = None
            return

        data_text = "\n".join(data_lines).strip()
        event = event_name
        event_name = None
        data_lines = []

        if not data_text or data_text == "[DONE]":
            return

        try:
            payload = json.loads(data_text)
        except json.JSONDecodeError:
            return

        delta = find_stream_delta(event, payload)
        if delta:
            collected_text_parts.append(delta)
            if output_format == "markdown":
                sys.stdout.write(delta)
                sys.stdout.flush()

        if isinstance(payload, dict):
            response_obj = payload.get("response")
            if isinstance(response_obj, dict):
                final_response = response_obj
            elif event == "response.completed":
                final_response = payload
            elif payload.get("type") == "response.completed":
                embedded = payload.get("response")
                if isinstance(embedded, dict):
                    final_response = embedded

    with urllib.request.urlopen(request, timeout=timeout) as response:
        for raw_line in response:
            line = raw_line.decode("utf-8").rstrip("\n")
            if not line.strip():
                flush_event()
                continue
            if line.startswith("event:"):
                event_name = line.split(":", 1)[1].strip()
                continue
            if line.startswith("data:"):
                data_lines.append(line.split(":", 1)[1].strip())
                continue

    flush_event()

    if final_response is None:
        final_response = {
            "status": "completed",
            "output_text": "".join(collected_text_parts).strip(),
        }
    elif collected_text_parts and not extract_output_text(final_response):
        final_response["output_text"] = "".join(collected_text_parts).strip()

    streamed_answer = bool("".join(collected_text_parts).strip())
    return final_response, streamed_answer


def non_stream_response(request: urllib.request.Request, timeout: int) -> dict[str, Any]:
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw_body = response.read().decode("utf-8")
    return json.loads(raw_body)


def execute_request(args: argparse.Namespace, payload: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    endpoint = args.base_url.rstrip("/") + "/responses"
    request = create_request(endpoint, args.api_key, payload, args.stream)
    if args.stream:
        return stream_response(request, args.timeout, args.format)
    return non_stream_response(request, args.timeout), False


def print_markdown(normalized: dict[str, Any]) -> None:
    title = normalized.get("title") or normalized.get("query") or "ARK Web Search Result"
    answer = normalized.get("answer") or ""
    sources = normalized.get("sources") or []

    print(f"# {title}\n")
    print("## 摘要\n")
    if answer:
        print(answer.strip())
    else:
        print("未返回可解析的正文结果。")

    print("\n## 来源\n")
    if sources:
        for index, source in enumerate(sources, start=1):
            source_title = source.get("title") or source.get("url") or "Untitled source"
            url = source.get("url") or ""
            print(f"{index}. {source_title}")
            if url:
                print(url)
    else:
        print("未返回可解析来源链接。")


def print_sources_only(normalized: dict[str, Any]) -> None:
    sources = normalized.get("sources") or []
    if not sources:
        return
    print("\nSources:")
    for index, source in enumerate(sources, start=1):
        title = source.get("title") or source.get("url") or "Untitled source"
        url = source.get("url") or ""
        print(f"{index}. {title}")
        if url:
            print(url)


def main() -> int:
    args = parse_args()
    payload = build_payload(args)

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if not args.api_key:
        print("ARK_API_KEY is required. Set ARK_API_KEY or pass --api-key.", file=sys.stderr)
        return 2

    active_payload = copy.deepcopy(payload)
    retries_left = max(args.retries, 0)
    used_search_context_fallback = False
    streamed_answer = False

    while True:
        try:
            response_obj, streamed_answer = execute_request(args, active_payload)
            if args.stream and args.format == "markdown":
                print()
            break
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if (
                not used_search_context_fallback
                and payload_has_search_context_size(active_payload)
                and looks_like_unsupported_search_context_size(exc.code, body)
            ):
                used_search_context_fallback = True
                strip_search_context_size(active_payload)
                print(
                    "ARK rejected search_context_size; retrying without it.",
                    file=sys.stderr,
                )
                continue

            if retries_left > 0 and is_retryable_http_status(exc.code):
                print(
                    f"HTTP {exc.code}; retrying in {args.retry_delay:g}s "
                    f"({retries_left} retries left before this retry).",
                    file=sys.stderr,
                )
                retries_left -= 1
                time.sleep(max(args.retry_delay, 0))
                continue

            print(f"HTTP {exc.code}: {body}", file=sys.stderr)
            return 1
        except urllib.error.URLError as exc:
            if retries_left > 0:
                print(
                    f"Network error: {exc}. Retrying in {args.retry_delay:g}s "
                    f"({retries_left} retries left before this retry).",
                    file=sys.stderr,
                )
                retries_left -= 1
                time.sleep(max(args.retry_delay, 0))
                continue
            print(f"Network error: {exc}", file=sys.stderr)
            return 1
        except json.JSONDecodeError as exc:
            print(f"Invalid JSON response: {exc}", file=sys.stderr)
            return 1

    normalized = normalize_response(response_obj, active_payload)

    if args.format == "raw":
        print(json.dumps(response_obj, ensure_ascii=False, indent=2))
    elif args.format == "json":
        print(json.dumps(normalized, ensure_ascii=False, indent=2))
    elif args.stream and args.format == "markdown" and streamed_answer:
        print_sources_only(normalized)
    else:
        print_markdown(normalized)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
