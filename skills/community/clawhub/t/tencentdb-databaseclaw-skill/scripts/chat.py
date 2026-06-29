#!/usr/bin/env python3
# pyright: reportAny=false, reportUnusedCallResult=false, reportExplicitAny=false
# pyright: reportUnknownVariableType=false, reportUnknownMemberType=false, reportUnknownArgumentType=false
"""
TencentDB-DatabaseClaw Chat Client
====================================
Stream chat with a DatabaseClaw instance via CreateChatCompletion SSE API.

Usage:
  # Public cloud (TC3 signed)
  python3 chat.py --instance-id clawins-pl14zpe3 \\
      --secret-id AKIDxxxx --secret-key xxxx \\
      --message "查询近7天慢查询 TOP 10"

  # Interactive mode (omit --message)
  python3 chat.py --instance-id clawins-pl14zpe3 \\
      --secret-id AKIDxxxx --secret-key xxxx

  # Internal dev gateway (no signing)
  python3 chat.py --internal --instance-id clawins-xxxxx --message "SELECT 1"

Dependencies: Python 3.9+ stdlib only (no pip install needed)
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any


# ─── Constants ───────────────────────────────────────────────
SSE_HOST: str = "tdai.ai.tencentcloudapi.com"
NON_SSE_HOST: str = "tdai.tencentcloudapi.com"
INTERNAL_ENDPOINT: str = "/interface_v3"
SERVICE: str = "tdai"
API_VERSION: str = "2025-07-17"
ACTION: str = "CreateChatCompletion"
ACTION_CREATE_SESSION: str = "CreateClawSession"


# ─── TC3 Signing ─────────────────────────────────────────────
def tc3_sign(
    secret_id: str,
    secret_key: str,
    host: str,
    payload: str,
    region: str = "ap-guangzhou",  # noqa: ARG001 - kept for API consistency
) -> tuple[str, int]:
    """Generate TC3-HMAC-SHA256 authorization. Returns (auth, timestamp)."""
    _ = region  # reserved for future region-scoped signing
    timestamp: int = int(time.time())
    date: str = time.strftime("%Y-%m-%d", time.gmtime(timestamp))

    canonical_headers: str = (
        f"content-type:application/json\n"
        f"host:{host}\n"
        f"x-tc-timestamp:{timestamp}\n"
    )
    signed_headers: str = "content-type;host;x-tc-timestamp"
    hashed_payload: str = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    canonical_request: str = (
        f"POST\n/\n\n{canonical_headers}\n{signed_headers}\n{hashed_payload}"
    )

    credential_scope: str = f"{date}/{SERVICE}/tc3_request"
    hashed_canonical: str = hashlib.sha256(
        canonical_request.encode("utf-8")
    ).hexdigest()
    string_to_sign: str = (
        f"TC3-HMAC-SHA256\n{timestamp}\n{credential_scope}\n{hashed_canonical}"
    )

    def _hmac_sha256(key: bytes, msg: str) -> bytes:
        return hmac.digest(key, msg.encode("utf-8"), "sha256")

    k_date: bytes = _hmac_sha256(f"TC3{secret_key}".encode("utf-8"), date)
    k_service: bytes = _hmac_sha256(k_date, SERVICE)
    k_signing: bytes = _hmac_sha256(k_service, "tc3_request")
    signature: str = hmac.digest(
        k_signing, string_to_sign.encode("utf-8"), "sha256"
    ).hex()

    auth: str = (
        f"TC3-HMAC-SHA256 Credential={secret_id}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )
    return auth, timestamp


# ─── SSE Event Model ─────────────────────────────────────────
@dataclass
class SSEEvent:
    """A single parsed SSE event from the DatabaseClaw stream."""

    object: str = ""          # chat.chunk / chat.final / tool.call / tool.result / error
    chat_id: str = ""
    streaming_id: str = ""
    content: str = ""         # Delta.Content (text chunks)
    finish_reason: str = ""   # "stop" / "error" / ""
    error_message: str = ""
    tool_name: str = ""       # tool call function name
    tool_args: str = ""       # tool call arguments (JSON string)
    reasoning: str = ""       # Delta.ReasoningContent (thinking)
    raw: dict[str, Any] = field(default_factory=dict)


# ─── Client ──────────────────────────────────────────────────
class DBClawChatError(Exception):
    """Raised on API or network errors."""


class DBClawClient:
    """DatabaseClaw CreateChatCompletion SSE client (stdlib only)."""

    def __init__(
        self,
        *,
        secret_id: str = "",
        secret_key: str = "",
        use_internal: bool = False,
        internal_host: str = "http://127.0.0.1:30080",
        region: str = "ap-guangzhou",
        silent: bool = False,
    ) -> None:
        self.secret_id: str = secret_id
        self.secret_key: str = secret_key
        self.use_internal: bool = use_internal
        self.internal_host: str = internal_host
        self.region: str = region
        self.silent: bool = silent

    def create_session(self, instance_id: str, *, timeout: int = 30) -> str:
        """Call CreateClawSession to get a SessionKey for console visibility.

        Returns the SessionKey string which should be passed as ChatId to chat().
        """
        payload: dict[str, str] = {"InstanceId": instance_id}
        body: str = json.dumps(payload, ensure_ascii=False)

        if self.use_internal:
            raise DBClawChatError("CreateClawSession not supported in internal mode")

        if not self.secret_id or not self.secret_key:
            raise DBClawChatError("secret_id and secret_key required for CreateClawSession")

        auth, ts = tc3_sign(
            self.secret_id, self.secret_key, NON_SSE_HOST, body, self.region
        )
        url: str = f"https://{NON_SSE_HOST}/"
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Host": NON_SSE_HOST,
            "X-TC-Action": ACTION_CREATE_SESSION,
            "X-TC-Version": API_VERSION,
            "X-TC-Region": self.region,
            "X-TC-Timestamp": str(ts),
            "Authorization": auth,
        }

        req = urllib.request.Request(
            url, data=body.encode("utf-8"), headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                resp_body: str = resp.read().decode("utf-8")
                data: dict[str, Any] = json.loads(resp_body)
                response: dict[str, Any] = data.get("Response", data)
                if "Error" in response:
                    err = response["Error"]
                    raise DBClawChatError(
                        f"CreateClawSession failed: {err.get('Code')}: {err.get('Message')}"
                    )
                session_key: str = response.get("SessionKey", "")
                if not session_key:
                    raise DBClawChatError("CreateClawSession returned empty SessionKey")
                return session_key
        except urllib.error.HTTPError as e:
            err_body: str = e.read().decode("utf-8", errors="replace")
            raise DBClawChatError(f"CreateClawSession HTTP {e.code}: {err_body}") from e
        except urllib.error.URLError as e:
            raise DBClawChatError(f"CreateClawSession connection failed: {e.reason}") from e

    def chat(
        self,
        instance_id: str,
        message: str,
        *,
        chat_id: str | None = None,
        timeout: int = 120,
    ) -> Iterator[SSEEvent]:
        """Send message, yield SSE events."""
        payload: dict[str, str] = {
            "InstanceId": instance_id,
            "InputContent": message,
        }
        if chat_id:
            payload["ChatId"] = chat_id

        body: str = json.dumps(payload, ensure_ascii=False)

        if self.use_internal:
            url: str = f"{self.internal_host}{INTERNAL_ENDPOINT}"
            headers: dict[str, str] = {
                "Content-Type": "application/json",
                "Accept": "text/event-stream",
            }
        else:
            if not self.secret_id or not self.secret_key:
                raise DBClawChatError(
                    "secret_id and secret_key required for public cloud"
                )
            auth, ts = tc3_sign(
                self.secret_id, self.secret_key, SSE_HOST, body, self.region
            )
            url = f"https://{SSE_HOST}/"
            headers = {
                "Content-Type": "application/json",
                "Accept": "text/event-stream",
                "Host": SSE_HOST,
                "X-TC-Action": ACTION,
                "X-TC-Version": API_VERSION,
                "X-TC-Region": self.region,
                "X-TC-Timestamp": str(ts),
                "Authorization": auth,
            }

        req = urllib.request.Request(
            url, data=body.encode("utf-8"), headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                yield from self._parse_stream(resp)
        except urllib.error.HTTPError as e:
            err_body: str = e.read().decode("utf-8", errors="replace")
            raise DBClawChatError(f"HTTP {e.code}: {err_body}") from e
        except urllib.error.URLError as e:
            raise DBClawChatError(f"Connection failed: {e.reason}") from e

    def _parse_stream(self, resp: Any) -> Iterator[SSEEvent]:
        """Parse SSE stream: 'data: {json}\\n\\n', ends with 'data: [DONE]'."""
        buf: bytes = b""
        for chunk in resp:
            buf += chunk
            while b"\n\n" in buf:
                raw_bytes: bytes
                raw_bytes, buf = buf.split(b"\n\n", 1)
                text: str = raw_bytes.decode("utf-8", errors="replace").strip()

                if text.startswith("data: "):
                    text = text[6:]
                elif text.startswith("data:"):
                    text = text[5:].strip()
                else:
                    continue

                if not text or text == "[DONE]":
                    return

                try:
                    data: dict[str, Any] = json.loads(text)
                except json.JSONDecodeError:
                    if not self.silent:
                        print(
                            f"[warn] unparseable: {text[:80]}", file=sys.stderr
                        )
                    continue

                # Unwrap {"Response": {...}} wrapper
                resp_inner = data.get("Response")
                if isinstance(resp_inner, dict):
                    data = resp_inner  # type: ignore[assignment]

                # Error frame
                if "Error" in data:
                    err: dict[str, Any] = data["Error"]
                    yield SSEEvent(
                        object="error",
                        finish_reason="error",
                        error_message=f"{err.get('Code')}: {err.get('Message')}",
                        raw=data,
                    )
                    return

                # Normal frame
                choices: list[dict[str, Any]] = data.get("Choices") or [{}]
                c: dict[str, Any] = choices[0] if choices else {}
                delta: dict[str, Any] = c.get("Delta", {})
                finish: str = c.get("FinishReason", "")

                # Determine event type
                obj: str = data.get("Object", "")
                tool_name: str = ""
                tool_args: str = ""
                reasoning: str = delta.get("ReasoningContent", "")

                # Tool call frames (ToolCalls array in Delta)
                tool_calls_raw = delta.get("ToolCalls")
                if tool_calls_raw and isinstance(tool_calls_raw, list):
                    for tc_item in tool_calls_raw:
                        if not isinstance(tc_item, dict):
                            continue
                        fn: dict[str, str] = tc_item.get("Function", {})
                        fn_name: str = fn.get("Name", "")
                        fn_args: str = fn.get("Arguments", "")
                        if fn_name:
                            tool_name = fn_name
                        if fn_args:
                            tool_args += fn_args
                    if not obj:
                        obj = "tool.call"

                # Tool result frames (Role == "tool")
                if delta.get("Role") == "tool" and not obj:
                    obj = "tool.result"

                # Infer object if still empty
                if not obj:
                    if finish == "stop":
                        obj = "chat.final"
                    elif delta.get("Content"):
                        obj = "chat.chunk"
                    elif reasoning:
                        obj = "reasoning"

                yield SSEEvent(
                    object=obj,
                    chat_id=data.get("ChatId", ""),
                    streaming_id=data.get("StreamingId", ""),
                    content=delta.get("Content", ""),
                    finish_reason=finish,
                    error_message=c.get("ErrorMessage", ""),
                    tool_name=tool_name,
                    tool_args=tool_args,
                    reasoning=reasoning,
                    raw=data,
                )

                if finish == "stop" or obj in ("chat.final", "claw.final", "error"):
                    return


# ─── CLI ─────────────────────────────────────────────────────
def main() -> None:
    """CLI entry point."""
    p = argparse.ArgumentParser(description="DatabaseClaw SSE Chat Client")
    p.add_argument(
        "--instance-id", "-i", required=True, help="Instance ID (clawins-xxx)"
    )
    p.add_argument("--message", "-m", help="Message (omit for interactive mode)")
    p.add_argument("--secret-id", default="", help="TencentCloud SecretId")
    p.add_argument("--secret-key", default="", help="TencentCloud SecretKey")
    p.add_argument("--chat-id", default=None, help="Chat ID for multi-turn")
    p.add_argument(
        "--no-session", action="store_true",
        help="Skip CreateClawSession (conversation won't appear in console session list)"
    )
    p.add_argument(
        "--internal", action="store_true", help="Use internal gateway (no signing)"
    )
    p.add_argument("--internal-host", default="http://127.0.0.1:30080")
    p.add_argument("--region", default="ap-guangzhou")
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--verbose", "-v", action="store_true",
                   help="Show tool calls and reasoning process (default: final output only)")
    p.add_argument("--silent", action="store_true",
                   help="Suppress parse warnings")
    args = p.parse_args()

    client = DBClawClient(
        secret_id=args.secret_id,
        secret_key=args.secret_key,
        use_internal=args.internal,
        internal_host=args.internal_host,
        region=args.region,
        silent=args.silent,
    )

    if args.message:
        _single_message(client, args)
    else:
        _interactive(client, args)


def _single_message(client: DBClawClient, args: argparse.Namespace) -> None:
    """Send a single message and print the response."""
    verbose: bool = args.verbose
    chat_id: str | None = args.chat_id

    # Create session by default (makes conversation visible in console)
    if not args.no_session and not chat_id and not args.internal:
        try:
            session_key = client.create_session(args.instance_id)
            chat_id = session_key
            if verbose:
                print(f"[session] Created SessionKey={session_key}", file=sys.stderr)
        except DBClawChatError as e:
            print(f"[warn] CreateClawSession failed: {e}", file=sys.stderr)
            print("[warn] Proceeding without session (conversation won't appear in console list)", file=sys.stderr)

    if verbose:
        print(f"[DatabaseClaw] Instance={args.instance_id}", file=sys.stderr)
        print(f"[Message] {args.message}\n", file=sys.stderr)
    try:
        for event in client.chat(
            args.instance_id, args.message, chat_id=chat_id, timeout=args.timeout
        ):
            if event.object == "connect":
                if verbose:
                    print(f"[connected] ChatId={event.chat_id}", file=sys.stderr)
            elif event.object == "reasoning":
                if verbose and event.reasoning:
                    print(f"\U0001f4ad {event.reasoning}", end="", flush=True,
                          file=sys.stderr)
            elif event.object in ("tool.call", "claw.tool_call"):
                if verbose:
                    info: str = event.content or event.tool_name or ""
                    print(f"\U0001f527 {info}", file=sys.stderr)
            elif event.object in ("tool.result", "claw.tool_result"):
                if verbose:
                    info = event.content or ""
                    print(f"\U0001f4cb {info}", file=sys.stderr)
            elif event.object in ("chat.chunk", "claw.partial", ""):
                if event.content:
                    print(event.content, end="", flush=True)
            elif event.object in ("chat.final", "claw.final"):
                if verbose:
                    print(f"\n\n[done] FinishReason={event.finish_reason}",
                          file=sys.stderr)
            elif event.object == "heartbeat":
                pass
            elif event.object == "error":
                print(f"\n[error] {event.error_message}", file=sys.stderr)
                sys.exit(1)
    except DBClawChatError as e:
        print(f"\n[fatal] {e}", file=sys.stderr)
        sys.exit(1)


def _interactive(client: DBClawClient, args: argparse.Namespace) -> None:
    """Interactive multi-turn chat loop."""
    print("=" * 50)
    print("DatabaseClaw Chat (Ctrl+C to exit)")
    print("=" * 50)
    chat_id: str | None = args.chat_id

    # Create session by default for console visibility
    if not args.no_session and not chat_id and not args.internal:
        try:
            session_key = client.create_session(args.instance_id)
            chat_id = session_key
            print(f"[session] Created SessionKey={session_key} (visible in console)")
        except DBClawChatError as e:
            print(f"[warn] CreateClawSession failed: {e}")
            print("[warn] Proceeding without session")

    while True:
        try:
            msg: str = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye.")
            break
        if not msg:
            continue
        print()
        try:
            for event in client.chat(
                args.instance_id, msg, chat_id=chat_id, timeout=args.timeout
            ):
                if event.object == "connect" and event.chat_id:
                    chat_id = event.chat_id
                elif event.content:
                    print(event.content, end="", flush=True)
                elif event.object == "error":
                    print(f"\n[error] {event.error_message}")
                    break
            print()
        except DBClawChatError as e:
            print(f"[error] {e}")


if __name__ == "__main__":
    main()
