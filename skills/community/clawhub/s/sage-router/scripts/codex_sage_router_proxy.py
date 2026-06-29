#!/usr/bin/env python3
"""Expose Sage Router's Chat Completions endpoint as an OpenAI Responses endpoint."""
import http.server
import json
import os
import re
import time
import urllib.error
import urllib.request
import uuid

TARGET = os.environ.get("SAGE_ROUTER_TARGET", "http://cyber_sage_router:8790").rstrip("/")
TOOL_CALLS_OMITTED_RE = r"\[\s*tool\s+calls\s*omitted\s*\]"
MODEL_PREFIX_LABEL_RE = r"\[[A-Za-z0-9_.-]+/[^\]\s]+\]"
PARTIAL_MODEL_PREFIX_LABEL_RE = r"\[[A-Za-z0-9_.-]*(?:/[^\]\s]*)?$"


def looks_like_model_prefix_label(label):
    label = str(label or "").strip()
    if label.lower().startswith("sage-router "):
        label = label.split(None, 1)[1].strip()
    if len(label) > 140 or " " in label or "/" not in label:
        return False
    return bool(re.match(r"^[A-Za-z0-9_.-]+/[^\]\s]+$", label))


def strip_model_prefix_tool_placeholder_noise(text):
    remaining = str(text or "")
    if not remaining:
        return ""
    prefix_run_re = rf"(?:{MODEL_PREFIX_LABEL_RE}\s*)+"
    placeholder_run_re = rf"(?:{MODEL_PREFIX_LABEL_RE}\s*)*{TOOL_CALLS_OMITTED_RE}"
    cleaned_lines = []
    changed = False
    for line in remaining.splitlines():
        stripped = line.strip()
        if not stripped:
            cleaned_lines.append(line)
            continue
        labels = re.findall(MODEL_PREFIX_LABEL_RE, stripped)
        without_noise = re.sub(MODEL_PREFIX_LABEL_RE, "", stripped).strip()
        without_noise = re.sub(TOOL_CALLS_OMITTED_RE, "", without_noise, flags=re.IGNORECASE).strip()
        if labels:
            without_noise = re.sub(PARTIAL_MODEL_PREFIX_LABEL_RE, "", without_noise).strip()
        if not labels and "/" in stripped and stripped.rsplit("/", 1)[1] and re.fullmatch(PARTIAL_MODEL_PREFIX_LABEL_RE, stripped):
            changed = True
            continue
        if labels and not without_noise:
            changed = True
            continue
        if not labels and not without_noise and re.search(TOOL_CALLS_OMITTED_RE, stripped, flags=re.IGNORECASE):
            changed = True
            continue
        cleaned_lines.append(line)
    cleaned = "\n".join(cleaned_lines).strip() if changed else remaining
    if not cleaned.rstrip().endswith("]"):
        return cleaned
    suffix_noise_re = rf"(?:\s+(?:{placeholder_run_re}|{prefix_run_re}))+\s*$"
    suffix_cleaned = re.sub(suffix_noise_re, "", cleaned, flags=re.IGNORECASE).rstrip()
    if suffix_cleaned != cleaned:
        cleaned = suffix_cleaned
        changed = True
    if changed:
        return re.sub(PARTIAL_MODEL_PREFIX_LABEL_RE, "", cleaned.strip()).rstrip()
    return cleaned


def strip_leading_generic_model_prefix_labels(text):
    remaining = str(text or "")
    while True:
        stripped = remaining.lstrip()
        leading_ws = remaining[:len(remaining) - len(stripped)]
        match = re.match(r"^\[([^\]\n]{1,140})\](?=\s|$)\s*", stripped)
        if not match or not looks_like_model_prefix_label(match.group(1)):
            break
        remaining = leading_ws + stripped[match.end():].lstrip()
    return remaining.strip()


def sanitize_visible_output(text):
    cleaned = strip_model_prefix_tool_placeholder_noise(text)
    cleaned = strip_leading_generic_model_prefix_labels(cleaned)
    cleaned = re.sub(rf"(^|[\s]){TOOL_CALLS_OMITTED_RE}(?=\s|$)", r"\1", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def messages_from_response_request(payload):
    messages = []
    instructions = payload.get("instructions")
    if instructions:
        messages.append({"role": "system", "content": instructions})
    request_input = payload.get("input", "")
    if isinstance(request_input, str):
        messages.append({"role": "user", "content": request_input})
        return messages
    for item in request_input or []:
        if not isinstance(item, dict):
            continue
        item_type = item.get("type")
        if item_type == "function_call":
            call_id = item.get("call_id") or item.get("id") or f"call_{uuid.uuid4().hex[:24]}"
            arguments = item.get("arguments") or "{}"
            if not isinstance(arguments, str):
                arguments = json.dumps(arguments, separators=(",", ":"))
            messages.append({
                "role": "assistant",
                "content": "",
                "tool_calls": [{
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": item.get("name") or "tool",
                        "arguments": arguments,
                    },
                }],
            })
            continue
        if item_type == "function_call_output":
            call_id = item.get("call_id") or item.get("id") or ""
            if not call_id:
                continue
            messages.append({
                "role": "tool",
                "tool_call_id": call_id,
                "content": str(item.get("output", "")),
            })
            continue
        if item_type and item_type != "message" and "role" not in item:
            continue
        role = item.get("role", "user")
        content = item.get("content", "")
        if isinstance(content, list):
            text = "\n".join(
                str(part.get("text", ""))
                for part in content
                if isinstance(part, dict) and part.get("type") in {"input_text", "output_text"}
            )
        else:
            text = str(content)
        if role == "assistant":
            text = sanitize_visible_output(text)
        if text:
            messages.append({"role": role, "content": text})
    return messages or [{"role": "user", "content": "Hello"}]


def chat_tools(response_tools):
    tools = []
    for tool in response_tools or []:
        if tool.get("type") != "function":
            continue
        tools.append({
            "type": "function",
            "function": {
                "name": tool.get("name", ""),
                "description": tool.get("description", ""),
                "parameters": tool.get("parameters", {"type": "object", "properties": {}}),
            },
        })
    return tools


def response_output(chat_response):
    choice = (chat_response.get("choices") or [{}])[0]
    message = choice.get("message") or {}
    output = []
    for call in message.get("tool_calls") or []:
        function = call.get("function") or {}
        output.append({
            "id": call.get("id") or f"fc_{uuid.uuid4().hex}",
            "type": "function_call",
            "status": "completed",
            "call_id": call.get("id") or f"call_{uuid.uuid4().hex}",
            "name": function.get("name", ""),
            "arguments": function.get("arguments", "{}"),
        })
    content = sanitize_visible_output(message.get("content") or message.get("reasoning") or "")
    if content:
        output.append({
            "id": f"msg_{uuid.uuid4().hex}",
            "type": "message",
            "status": "completed",
            "role": "assistant",
            "content": [{"type": "output_text", "text": content, "annotations": []}],
        })
    return output


def response_usage(chat_response):
    usage = chat_response.get("usage") or {}
    input_tokens = usage.get("input_tokens", usage.get("prompt_tokens", 0))
    output_tokens = usage.get("output_tokens", usage.get("completion_tokens", 0))
    return {
        "input_tokens": input_tokens,
        "input_tokens_details": usage.get("input_tokens_details") or {"cached_tokens": 0},
        "output_tokens": output_tokens,
        "output_tokens_details": usage.get("output_tokens_details") or {"reasoning_tokens": 0},
        "total_tokens": usage.get("total_tokens", input_tokens + output_tokens),
    }


def streaming_events(result):
    sequence = 0

    def event(event_type, **fields):
        nonlocal sequence
        payload = {"type": event_type, "sequence_number": sequence, **fields}
        sequence += 1
        return event_type, payload

    yield event("response.created", response={**result, "status": "in_progress", "output": []})
    for output_index, item in enumerate(result["output"]):
        yield event("response.output_item.added", output_index=output_index, item={**item, "status": "in_progress"})
        if item["type"] == "message":
            for content_index, part in enumerate(item.get("content", [])):
                in_progress_part = {**part, "text": ""}
                yield event(
                    "response.content_part.added",
                    item_id=item["id"],
                    output_index=output_index,
                    content_index=content_index,
                    part=in_progress_part,
                )
                yield event(
                    "response.output_text.delta",
                    item_id=item["id"],
                    output_index=output_index,
                    content_index=content_index,
                    delta=part.get("text", ""),
                    logprobs=[],
                )
                yield event(
                    "response.output_text.done",
                    item_id=item["id"],
                    output_index=output_index,
                    content_index=content_index,
                    text=part.get("text", ""),
                    logprobs=[],
                )
                yield event(
                    "response.content_part.done",
                    item_id=item["id"],
                    output_index=output_index,
                    content_index=content_index,
                    part=part,
                )
        elif item["type"] == "function_call":
            yield event(
                "response.function_call_arguments.delta",
                item_id=item["id"],
                output_index=output_index,
                delta=item.get("arguments", "{}"),
            )
            yield event(
                "response.function_call_arguments.done",
                item_id=item["id"],
                output_index=output_index,
                arguments=item.get("arguments", "{}"),
            )
        yield event("response.output_item.done", output_index=output_index, item=item)
    yield event("response.completed", response=result)


def normalize_models_payload(payload):
    models = payload.get("models") or payload.get("data")
    if not isinstance(models, list):
        return payload
    normalized = []
    seen = set()

    def add_row(row):
        model_id = row.get("id") or row.get("slug")
        if not model_id or model_id in seen:
            return
        seen.add(model_id)
        normalized.append(row)

    for item in models:
        if not isinstance(item, dict):
            continue
        model_id = item.get("id") or item.get("slug") or item.get("model") or item.get("name")
        if not model_id:
            continue
        display_name = item.get("displayName") or item.get("display_name") or item.get("name") or model_id
        reasoning_levels = item.get("supported_reasoning_levels") or item.get("supportedReasoningLevels")
        if reasoning_levels is None or all(isinstance(level, str) for level in reasoning_levels):
            reasoning_levels = []
        row = {
            **item,
            "id": model_id,
            "slug": item.get("slug") or model_id,
            "name": item.get("name") or display_name,
            "description": item.get("description"),
            "displayName": display_name,
            "display_name": item.get("display_name") or display_name,
            "shell_type": item.get("shell_type") or "shell_command",
            "visibility": item.get("visibility") or "list",
            "supported_in_api": item.get("supported_in_api", True),
            "priority": item.get("priority") or 100,
            "additional_speed_tiers": item.get("additional_speed_tiers") or [],
            "service_tiers": item.get("service_tiers") or [],
            "availability_nux": item.get("availability_nux"),
            "upgrade": item.get("upgrade"),
            "base_instructions": item.get("base_instructions") or "You are Codex, a coding agent. Help the user complete the requested task in the shared workspace.",
            "supports_reasoning_summaries": item.get("supports_reasoning_summaries", True),
            "support_verbosity": item.get("support_verbosity", True),
            "default_verbosity": item.get("default_verbosity") or "medium",
            "apply_patch_tool_type": item.get("apply_patch_tool_type") or "freeform",
            "web_search_tool_type": item.get("web_search_tool_type") or "text_and_image",
            "truncation_policy": item.get("truncation_policy") or {"mode": "tokens", "limit": 10000},
            "supports_parallel_tool_calls": item.get("supports_parallel_tool_calls", True),
            "supports_image_detail_original": item.get("supports_image_detail_original", True),
            "experimental_supported_tools": item.get("experimental_supported_tools") or [],
            "input_modalities": item.get("input_modalities") or item.get("inputModalities") or ["text"],
            "supports_search_tool": item.get("supports_search_tool", True),
            "supported_reasoning_levels": reasoning_levels,
            "supportedReasoningLevels": reasoning_levels,
            "context_window": item.get("context_window") or item.get("contextWindow") or 131072,
            "contextWindow": item.get("contextWindow") or item.get("context_window") or 131072,
            "max_context_window": item.get("max_context_window") or item.get("maxContextWindow") or item.get("context_window") or item.get("contextWindow") or 131072,
            "effective_context_window_percent": item.get("effective_context_window_percent") or item.get("effectiveContextWindowPercent") or 95,
            "max_output_tokens": item.get("max_output_tokens") or item.get("maxOutputTokens") or item.get("maxTokens") or 8192,
            "maxOutputTokens": item.get("maxOutputTokens") or item.get("max_output_tokens") or item.get("maxTokens") or 8192,
        }
        add_row(row)
        if model_id.startswith("openai-codex/"):
            alias_id = model_id.split("/", 1)[1]
            add_row({
                **row,
                "id": alias_id,
                "slug": alias_id,
                "name": alias_id,
                "displayName": alias_id,
                "display_name": alias_id,
            })
    if "gpt-5.5" not in seen:
        template = dict(normalized[0]) if normalized else {}
        add_row({
            **template,
            "id": "gpt-5.5",
            "slug": "gpt-5.5",
            "name": "gpt-5.5",
            "displayName": "gpt-5.5",
            "display_name": "gpt-5.5",
            "owned_by": "openai-codex",
            "provider": "openai-codex",
            "type": "provider_model",
        })
    return {**payload, "models": normalized, "data": normalized}


class Handler(http.server.BaseHTTPRequestHandler):
    def write_json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = "/v1/models" if self.path.startswith("/v1/models") else self.path
        try:
            with urllib.request.urlopen(TARGET + path, timeout=15) as response:
                body = response.read()
                content_type = response.headers.get("Content-Type", "application/json")
                if path == "/v1/models":
                    body = json.dumps(normalize_models_payload(json.loads(body or b"{}"))).encode()
                self.send_response(response.status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        except Exception as error:
            self.write_json(502, {"error": str(error)})

    def do_POST(self):
        if self.path not in {"/v1/responses", "/responses"}:
            self.write_json(404, {"error": "not_found"})
            return
        body = self.rfile.read(int(self.headers.get("Content-Length", 0) or 0))
        payload = json.loads(body or b"{}")
        chat_payload = {
            "model": payload.get("model") or "sage-router/agentic",
            "messages": messages_from_response_request(payload),
            "stream": False,
        }
        tools = chat_tools(payload.get("tools"))
        if tools:
            chat_payload["tools"] = tools
            if payload.get("tool_choice"):
                chat_payload["tool_choice"] = payload["tool_choice"]
        if payload.get("max_output_tokens"):
            chat_payload["max_tokens"] = payload["max_output_tokens"]
        request = urllib.request.Request(
            TARGET + "/v1/chat/completions",
            data=json.dumps(chat_payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=600) as response:
                chat_response = json.loads(response.read() or b"{}")
        except urllib.error.HTTPError as error:
            self.write_json(error.code, json.loads(error.read() or b"{}"))
            return
        except Exception as error:
            self.write_json(502, {"error": str(error)})
            return
        response_id = f"resp_{uuid.uuid4().hex}"
        output = response_output(chat_response)
        result = {
            "id": response_id,
            "object": "response",
            "created_at": int(time.time()),
            "status": "completed",
            "model": chat_response.get("model") or chat_payload["model"],
            "output": output,
            "usage": response_usage(chat_response),
            "error": None,
        }
        if not payload.get("stream"):
            self.write_json(200, result)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()
        for event_type, event_payload in streaming_events(result):
            self.wfile.write(f"event: {event_type}\ndata: {json.dumps(event_payload)}\n\n".encode())
        self.wfile.flush()
        self.close_connection = True

    def log_message(self, fmt, *args):
        print(f"[codex-sage-router-proxy] {fmt % args}", flush=True)


if __name__ == "__main__":
    port = int(os.environ.get("CODEX_SAGE_ROUTER_PORT", "8789"))
    print(f"Codex Sage Router proxy on :{port} -> {TARGET}", flush=True)
    http.server.ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
