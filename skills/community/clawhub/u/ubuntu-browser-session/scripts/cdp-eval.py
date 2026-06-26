#!/usr/bin/env python3
"""Minimal CDP evaluation helper using only the Python standard library."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import socket
import struct
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

TIMEOUT_SECONDS = 5
NAVIGATE_TIMEOUT_SECONDS = 15
WAIT_FOR_TIMEOUT_SECONDS = 10
USER_AGENT = "ubuntu-browser-session/cdp-eval"


class CdpError(RuntimeError):
    pass


def http_get_json(url: str) -> object:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def resolve_websocket_url(port: int, target_id: str | None) -> str:
    targets = http_get_json(f"http://127.0.0.1:{port}/json/list")
    if not isinstance(targets, list):
        raise CdpError("invalid target list response")

    page_targets = [target for target in targets if target.get("type") == "page"]

    if target_id:
        for target in page_targets:
            if target.get("id") == target_id:
                websocket_url = target.get("webSocketDebuggerUrl")
                if websocket_url:
                    return websocket_url
                break
        raise CdpError("target-id not found")

    if page_targets:
        websocket_url = page_targets[0].get("webSocketDebuggerUrl")
        if websocket_url:
            return websocket_url

    version = http_get_json(f"http://127.0.0.1:{port}/json/version")
    websocket_url = version.get("webSocketDebuggerUrl") if isinstance(version, dict) else None
    if not websocket_url:
        raise CdpError("missing webSocketDebuggerUrl")
    return websocket_url


def websocket_key() -> str:
    return base64.b64encode(os.urandom(16)).decode("ascii")


def build_frame(payload: str) -> bytes:
    raw = payload.encode("utf-8")
    mask_key = os.urandom(4)
    length = len(raw)
    header = bytearray([0x81])
    if length < 126:
        header.append(0x80 | length)
    elif length < (1 << 16):
        header.append(0x80 | 126)
        header.extend(struct.pack("!H", length))
    else:
        header.append(0x80 | 127)
        header.extend(struct.pack("!Q", length))
    masked = bytes(byte ^ mask_key[index % 4] for index, byte in enumerate(raw))
    return bytes(header) + mask_key + masked


def recv_exact(sock: socket.socket, size: int) -> bytes:
    chunks = []
    remaining = size
    while remaining > 0:
        chunk = sock.recv(remaining)
        if not chunk:
            raise CdpError("unexpected websocket EOF")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def read_frame(sock: socket.socket) -> str:
    first_two = recv_exact(sock, 2)
    first, second = first_two[0], first_two[1]
    opcode = first & 0x0F
    masked = second & 0x80
    length = second & 0x7F
    if length == 126:
        length = struct.unpack("!H", recv_exact(sock, 2))[0]
    elif length == 127:
        length = struct.unpack("!Q", recv_exact(sock, 8))[0]
    mask_key = recv_exact(sock, 4) if masked else b""
    payload = recv_exact(sock, length)
    if masked:
        payload = bytes(byte ^ mask_key[index % 4] for index, byte in enumerate(payload))
    if opcode == 0x8:
        raise CdpError("websocket closed by peer")
    if opcode == 0x9:
        sock.sendall(bytes([0x8A, 0x00]))
        return read_frame(sock)
    if opcode != 0x1:
        raise CdpError(f"unsupported websocket opcode: {opcode}")
    return payload.decode("utf-8")


class CdpSession:
    """Persistent CDP websocket connection supporting multiple messages and events."""

    def __init__(self, websocket_url: str, timeout: float = TIMEOUT_SECONDS):
        parsed = urllib.parse.urlparse(websocket_url)
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or (443 if parsed.scheme == "wss" else 80)
        if parsed.scheme != "ws":
            raise CdpError("only ws:// CDP endpoints are supported")

        key = websocket_key()
        request_path = parsed.path or "/"
        if parsed.query:
            request_path += f"?{parsed.query}"

        self._sock = socket.create_connection((host, port), timeout=timeout)
        self._sock.settimeout(timeout)
        handshake = (
            f"GET {request_path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self._sock.sendall(handshake.encode("utf-8"))
        response = b""
        while b"\r\n\r\n" not in response:
            chunk = self._sock.recv(4096)
            if not chunk:
                raise CdpError("incomplete websocket handshake")
            response += chunk
        header_blob = response.split(b"\r\n\r\n", 1)[0].decode("utf-8", errors="replace")
        if "101" not in header_blob.splitlines()[0]:
            raise CdpError(f"handshake failed: {header_blob.splitlines()[0]}")
        expected_accept = base64.b64encode(
            hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode("ascii")).digest()
        ).decode("ascii")
        if f"Sec-WebSocket-Accept: {expected_accept}" not in header_blob:
            raise CdpError("invalid websocket accept header")
        self._next_id = 1

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._sock.close()

    def send(self, method: str, params: dict | None = None) -> int:
        msg_id = self._next_id
        self._next_id += 1
        message = {"id": msg_id, "method": method}
        if params:
            message["params"] = params
        self._sock.sendall(build_frame(json.dumps(message)))
        return msg_id

    def recv(self) -> dict:
        return json.loads(read_frame(self._sock))

    def call(self, method: str, params: dict | None = None) -> dict:
        msg_id = self.send(method, params)
        while True:
            payload = self.recv()
            if payload.get("id") == msg_id:
                if "error" in payload:
                    raise CdpError(str(payload["error"]))
                return payload

    def wait_for_event(self, event_method: str, timeout: float) -> dict:
        deadline = time.monotonic() + timeout
        old_timeout = self._sock.gettimeout()
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise CdpError(f"timeout waiting for {event_method}")
                self._sock.settimeout(remaining)
                payload = self.recv()
                if payload.get("method") == event_method:
                    return payload
        finally:
            self._sock.settimeout(old_timeout)

    def set_timeout(self, timeout: float) -> None:
        self._sock.settimeout(timeout)


def websocket_request(websocket_url: str, message: dict[str, object]) -> dict[str, object]:
    parsed = urllib.parse.urlparse(websocket_url)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or (443 if parsed.scheme == "wss" else 80)
    if parsed.scheme != "ws":
        raise CdpError("only ws:// CDP endpoints are supported")

    key = websocket_key()
    request_path = parsed.path or "/"
    if parsed.query:
        request_path += f"?{parsed.query}"

    with socket.create_connection((host, port), timeout=TIMEOUT_SECONDS) as sock:
        sock.settimeout(TIMEOUT_SECONDS)
        handshake = (
            f"GET {request_path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        sock.sendall(handshake.encode("utf-8"))
        response = b""
        while b"\r\n\r\n" not in response:
            chunk = sock.recv(4096)
            if not chunk:
                raise CdpError("incomplete websocket handshake")
            response += chunk
        header_blob = response.split(b"\r\n\r\n", 1)[0].decode("utf-8", errors="replace")
        if "101" not in header_blob.splitlines()[0]:
            raise CdpError(f"handshake failed: {header_blob.splitlines()[0]}")
        expected_accept = base64.b64encode(
            hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode("ascii")).digest()
        ).decode("ascii")
        if f"Sec-WebSocket-Accept: {expected_accept}" not in header_blob:
            raise CdpError("invalid websocket accept header")

        sock.sendall(build_frame(json.dumps(message)))
        while True:
            payload = json.loads(read_frame(sock))
            if payload.get("id") == message["id"]:
                return payload


def evaluate(port: int, target_id: str | None, expression: str) -> dict[str, object]:
    websocket_url = resolve_websocket_url(port, target_id)
    response = websocket_request(
        websocket_url,
        {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": expression,
                "returnByValue": True,
            },
        },
    )
    if "error" in response:
        raise CdpError(str(response["error"]))
    result = response.get("result", {})
    if "exceptionDetails" in result:
        details = result["exceptionDetails"]
        description = details.get("exception", {}).get("description") or details.get("text") or "evaluation failed"
        raise CdpError(str(description))
    payload = result.get("result", {})
    return payload.get("value") if "value" in payload else payload


def detect_challenge(page_info: dict[str, object]) -> dict[str, object]:
    indicators = []
    haystack = " ".join(
        [
            str(page_info.get("title", "")),
            str(page_info.get("bodySnippet", "")),
            str(page_info.get("htmlSnippet", "")),
        ]
    ).lower()
    for token in [
        "请稍候",
        "just a moment",
        "checking your browser",
        "verify you are human",
        "cf-challenge",
        "challenge-platform",
        "turnstile",
        "captcha",
    ]:
        if token.lower() in haystack:
            indicators.append(token)
    return {
        "hasChallenge": bool(indicators),
        "indicators": indicators,
        "title": page_info.get("title", ""),
        "url": page_info.get("url", ""),
    }


def detect_login_wall(page_info: dict[str, object]) -> dict[str, object]:
    login_hits = []
    combined = " ".join([str(page_info.get("bodySnippet", "")), str(page_info.get("title", ""))]).lower()
    for token in ["sign in", "log in", "登录", "create your account", "sign up"]:
        if token.lower() in combined:
            login_hits.append(token)
    url = str(page_info.get("url", "")).lower()
    for token in ["/login", "/signin", "/auth", "/i/flow/login"]:
        if token in url and token not in login_hits:
            login_hits.append(token)
    return {
        "hasLoginWall": bool(login_hits),
        "loginHits": login_hits,
        "title": page_info.get("title", ""),
        "url": page_info.get("url", ""),
    }


def gather_page_info(port: int, target_id: str | None) -> dict[str, object]:
    expression = """(() => {
      const title = document.title || '';
      const url = location.href || '';
      const bodyText = document.body ? (document.body.innerText || '') : '';
      const html = document.documentElement ? (document.documentElement.outerHTML || '') : '';
      return {
        title,
        url,
        bodySnippet: bodyText.slice(0, 2000),
        htmlSnippet: html.slice(0, 4000)
      };
    })()"""
    value = evaluate(port, target_id, expression)
    if not isinstance(value, dict):
        raise CdpError("page-info did not return an object")
    return value


def navigate_and_wait(
    port: int,
    target_id: str | None,
    url: str,
    wait_selector: str | None = None,
    wait_navigation: bool = False,
) -> dict[str, object]:
    """Navigate to *url* via CDP, optionally wait for load and/or a CSS selector."""
    websocket_url = resolve_websocket_url(port, target_id)
    with CdpSession(websocket_url, timeout=NAVIGATE_TIMEOUT_SECONDS) as session:
        session.call("Page.enable")
        session.call("Page.navigate", {"url": url})
        if wait_navigation:
            session.wait_for_event("Page.loadEventFired", timeout=NAVIGATE_TIMEOUT_SECONDS)
        if wait_selector:
            _wait_for_selector(session, wait_selector)
        # Return current page info after navigation.
        resp = session.call(
            "Runtime.evaluate",
            {
                "expression": "({title: document.title, url: location.href})",
                "returnByValue": True,
            },
        )
        result = resp.get("result", {}).get("result", {})
        return result.get("value", result)


def _wait_for_selector(session: CdpSession, selector: str) -> None:
    """Poll for a CSS selector to appear, up to WAIT_FOR_TIMEOUT_SECONDS."""
    js = f"!!document.querySelector({json.dumps(selector)})"
    deadline = time.monotonic() + WAIT_FOR_TIMEOUT_SECONDS
    while True:
        resp = session.call("Runtime.evaluate", {"expression": js, "returnByValue": True})
        value = resp.get("result", {}).get("result", {}).get("value")
        if value:
            return
        if time.monotonic() >= deadline:
            raise CdpError(f"timeout waiting for selector: {selector}")
        time.sleep(0.3)


def click_link(port: int, target_id: str | None, text: str) -> dict[str, object]:
    expression = r"""((needle) => {
      const normalize = (value) => (value || '').replace(/\s+/g, ' ').trim();
      const isVisible = (anchor) => {
        if (!anchor || !anchor.isConnected) return false;
        if (anchor.hidden || anchor.getAttribute('aria-hidden') === 'true') return false;
        const style = window.getComputedStyle(anchor);
        if (!style || style.display === 'none' || style.visibility === 'hidden') return false;
        if (Number(style.opacity || '1') === 0) return false;
        return anchor.getClientRects().length > 0;
      };
      const wanted = normalize(needle).toLowerCase();
      const anchors = Array.from(document.querySelectorAll('a[href]'));
      const ranked = anchors.map((anchor, index) => {
        const anchorText = normalize(anchor.innerText || anchor.textContent);
        return {
          index,
          anchor,
          text: anchorText,
          href: anchor.href || '',
          visible: isVisible(anchor),
          exact: anchorText.toLowerCase() === wanted,
          includes: wanted && anchorText.toLowerCase().includes(wanted),
        };
      }).filter(item => item.text && item.href && item.visible);

      ranked.sort((a, b) => {
        const score = (item) => item.exact ? 0 : (item.includes ? 1 : 9);
        return score(a) - score(b) || a.text.length - b.text.length || a.index - b.index;
      });

      const hit = ranked.find(item => item.exact || item.includes);
      if (!hit) {
        return {
          clicked: false,
          requestedText: needle,
          candidates: ranked.slice(0, 10).map(item => ({ text: item.text, href: item.href }))
        };
      }

      hit.anchor.scrollIntoView({block: 'center', inline: 'center'});
      hit.anchor.click();
      return {
        clicked: true,
        requestedText: needle,
        text: hit.text,
        href: hit.href
      };
    })(%s)""" % json.dumps(text)
    value = evaluate(port, target_id, expression)
    if not isinstance(value, dict):
        raise CdpError("click-link did not return an object")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="cdp-eval", description="Evaluate page state over the Chrome DevTools Protocol.")
    parser.add_argument("--port", type=int, required=True, help="CDP HTTP/WebSocket port")
    parser.add_argument("--target-id", help="Specific target id from /json/list")
    parser.add_argument("--check", choices=["challenge", "login-wall", "page-info"])
    parser.add_argument("--eval", dest="expression", help="Arbitrary JavaScript expression for Runtime.evaluate")
    parser.add_argument("--navigate", metavar="URL", help="Navigate to URL before evaluating")
    parser.add_argument("--click-link-text", metavar="TEXT", help="Click the first anchor whose visible text matches or contains TEXT")
    parser.add_argument("--wait-for", metavar="SELECTOR", help="Wait for CSS selector to appear (timeout 10s)")
    parser.add_argument("--wait-navigation", action="store_true", help="Wait for page load event after --navigate")
    args = parser.parse_args()
    action_count = sum(bool(x) for x in [args.check, args.expression, args.click_link_text])
    if args.navigate:
        pass  # --navigate can be used alone or combined with one follow-up action
    elif action_count != 1:
        parser.error("provide exactly one of --check, --eval, or --click-link-text (or use --navigate)")
    if args.wait_for and not args.navigate and not args.expression and not args.check and not args.click_link_text:
        parser.error("--wait-for requires --navigate, --check, --eval, or --click-link-text")
    if args.wait_navigation and not args.navigate:
        parser.error("--wait-navigation requires --navigate")
    return args


def main() -> int:
    args = parse_args()
    try:
        if args.navigate:
            nav_result = navigate_and_wait(
                args.port, args.target_id, args.navigate,
                wait_selector=args.wait_for,
                wait_navigation=args.wait_navigation,
            )
            if not args.expression and not args.check:
                print(json.dumps(nav_result, ensure_ascii=False))
                return 0

        if args.expression:
            print(json.dumps(evaluate(args.port, args.target_id, args.expression), ensure_ascii=False))
            return 0

        if args.click_link_text:
            print(json.dumps(click_link(args.port, args.target_id, args.click_link_text), ensure_ascii=False))
            return 0

        page_info = gather_page_info(args.port, args.target_id)
        if args.check == "page-info":
            result = {
                "title": page_info.get("title", ""),
                "url": page_info.get("url", ""),
                "bodySnippet": page_info.get("bodySnippet", ""),
            }
        elif args.check == "challenge":
            result = detect_challenge(page_info)
        else:
            result = detect_login_wall(page_info)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, urllib.error.URLError, socket.timeout) as exc:
        print(json.dumps({"error": str(exc)}))
        return 1
    except CdpError as exc:
        print(json.dumps({"error": str(exc)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
