#!/usr/bin/env python3
"""
Send a message to an agent session and collect the response.

Connects via WebSocket, sends a prompt, and streams the response until
the turn is complete.

Usage:
    python3 agent_chat.py SESSION_ID "your message here"
    python3 agent_chat.py SESSION_ID "check this file {{@core_node:NODE_ID:filename.png}}"

Output (JSON):
    {
      "session_id": "...",
      "response": {
        "text": "...",
        "thinking": "...",
        "tool_calls": [ ... ],
        "media": [ ... ]
      }
    }
"""

import argparse
import json
import sys
import os
import time
from uuid import uuid4

sys.path.insert(0, os.path.dirname(__file__))
from _common import require_access_key, create_ws

TIMEOUT_SECONDS = 300  # 5 minutes max wait
HEARTBEAT_INTERVAL = 25  # Send heartbeat every 25s (server expects within 60s)
RECV_TIMEOUT = 5  # Short recv timeout so we can interleave heartbeats


def _send_heartbeat(ws):
    """Send a heartbeat ping to keep the connection alive."""
    msg = {
        "jsonrpc": "2.0",
        "id": f"hb-{uuid4()}",
        "method": "heartbeat",
        "params": {"heartbeat_id": str(uuid4())},
    }
    try:
        ws.send(json.dumps(msg))
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="Chat with agent")
    parser.add_argument("session_id", help="Session ID (from create_session.py)")
    parser.add_argument("message", help="Message to send")
    parser.add_argument("--timeout", type=int, default=TIMEOUT_SECONDS,
                        help=f"Timeout in seconds (default {TIMEOUT_SECONDS})")
    parser.add_argument("--auto-approve", action="store_true",
                        help="Automatically approve all tool execution requests")
    args = parser.parse_args()

    require_access_key()

    ws = create_ws(args.session_id)

    # Collect response parts
    text_parts = []
    thinking_parts = []
    tool_calls = []
    media = []
    finished = False
    is_replaying = True
    start_time = time.time()
    last_heartbeat = time.time()
    last_msg_received = time.time()

    def maybe_heartbeat():
        nonlocal last_heartbeat
        now = time.time()
        if now - last_heartbeat >= HEARTBEAT_INTERVAL:
            _send_heartbeat(ws)
            last_heartbeat = now

    # Wait for ReplayComplete before sending
    while True:
        maybe_heartbeat()
        msg_str = ws.recv(timeout=RECV_TIMEOUT)
        if msg_str is None:
            if (time.time() - start_time) > 60:
                break  # Gave up waiting for replay
            continue
        last_msg_received = time.time()
        try:
            msg = json.loads(msg_str)
        except json.JSONDecodeError:
            continue

        # Check for ReplayComplete or history_complete
        params = msg.get("params", {})
        if (msg.get("method") == "event" and params.get("type") == "ReplayComplete") or msg.get("method") == "history_complete":
            is_replaying = False
            break

        # Also handle session_status
        if msg.get("method") == "session_status":
            continue

    if is_replaying:
        # Timeout waiting for replay - try sending anyway
        pass

    # Send the prompt
    prompt_msg = {
        "jsonrpc": "2.0",
        "method": "prompt",
        "id": str(uuid4()),
        "params": {"user_input": args.message},
    }
    ws.send(json.dumps(prompt_msg))
    last_heartbeat = time.time()

    # Collect response
    while not finished and (time.time() - start_time) < args.timeout:
        maybe_heartbeat()
        msg_str = ws.recv(timeout=RECV_TIMEOUT)
        if msg_str is None:
            # No message this cycle — check if we should keep waiting
            has_pending_tools = any("result" not in tc for tc in tool_calls)
            idle_seconds = time.time() - last_msg_received
            # Keep waiting if: pending tool calls, or haven't been idle too long
            if has_pending_tools or idle_seconds < 60:
                continue
            # Idle for 60s with no pending tools — assume done
            if text_parts or tool_calls:
                finished = True
            break

        last_msg_received = time.time()

        try:
            msg = json.loads(msg_str)
        except json.JSONDecodeError:
            continue

        # Heartbeat response - ignore
        if isinstance(msg.get("id"), str) and msg["id"].startswith("hb-"):
            continue

        # Finished signal
        result = msg.get("result", {})
        if isinstance(result, dict) and result.get("status") == "finished":
            finished = True
            break

        # Error
        if msg.get("error"):
            text_parts.append(f"[Error: {msg['error'].get('message', 'Unknown')}]")
            finished = True
            break

        # Events
        params = msg.get("params", {})
        event_type = params.get("type")

        if event_type == "ContentPart":
            payload = params.get("payload", {})
            part_type = payload.get("type")
            if part_type == "text":
                text_parts.append(payload.get("text", ""))
            elif part_type == "think":
                thinking_parts.append(payload.get("think", ""))
            elif part_type in ("image_url", "video_url", "audio_url"):
                url_data = payload.get(part_type, {})
                if url_data and url_data.get("url"):
                    media.append({"type": part_type.replace("_url", ""), "url": url_data["url"]})

        elif event_type == "ToolCall":
            payload = params.get("payload", {})
            tc = {
                "id": payload.get("id"),
                "name": payload.get("function", {}).get("name", ""),
                "arguments": payload.get("function", {}).get("arguments", ""),
            }
            tool_calls.append(tc)

        elif event_type == "ToolCallPart":
            payload = params.get("payload", {})
            if tool_calls:
                tool_calls[-1]["arguments"] += payload.get("arguments_part", "")

        elif event_type == "ToolResult":
            payload = params.get("payload", {})
            tc_id = payload.get("tool_call_id")
            rv = payload.get("return_value", {})
            for tc in tool_calls:
                if tc["id"] == tc_id:
                    tc["result"] = {
                        "is_error": rv.get("is_error", False),
                        "message": rv.get("message", ""),
                    }
                    break

        elif event_type == "ApprovalRequest":
            payload = params.get("payload", {})
            rpc_id = msg.get("id", payload.get("id"))
            if args.auto_approve:
                approval_resp = {
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "result": {
                        "request_id": payload.get("id"),
                        "response": "approve",
                    },
                }
                ws.send(json.dumps(approval_resp))
            else:
                # Report the approval request and let the caller decide
                text_parts.append(
                    f"\n[Approval Required: {payload.get('action', '')} - {payload.get('description', '')}]\n"
                    f"Re-run with --auto-approve to auto-approve, or use respond_approval.py"
                )
                finished = True
                break

    ws.close()

    # Parse tool call arguments
    for tc in tool_calls:
        try:
            tc["arguments"] = json.loads(tc["arguments"]) if tc["arguments"] else {}
        except json.JSONDecodeError:
            pass

    response = {
        "session_id": args.session_id,
        "response": {
            "text": "".join(text_parts),
        },
    }
    if thinking_parts:
        response["response"]["thinking"] = "".join(thinking_parts)
    if tool_calls:
        response["response"]["tool_calls"] = tool_calls
    if media:
        response["response"]["media"] = media
    if not finished:
        response["response"]["warning"] = "Response may be incomplete (timeout or connection lost)"

    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
