#!/usr/bin/env python3
"""Bounded, read-only source collection. Fixture output is never live evidence."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import signal
import shlex
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from urllib.parse import parse_qs, parse_qsl, urlencode, urljoin, urlsplit, urlunsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
MODES = ("youtube-transcript", "youtube-comments", "google-citations", "xiaohongshu", "price")
SENSITIVE = {"authorization", "cookie", "cookies", "password", "proxy_password", "xsec_token", "xsectoken", "token", "access_token", "api_key", "x-api-key", "sign", "signature"}
FIXTURE_TIME = "2026-10-07T00:00:00Z"


class CollectionError(Exception):
    def __init__(self, status, code, message):
        super().__init__(message)
        self.status, self.code = status, code


def clean_url(value):
    try:
        p = urlsplit(value)
        if not p.scheme or not p.hostname:
            return value
        host = p.hostname + (f":{p.port}" if p.port else "")
        query = [(k, "[REDACTED]" if k.lower() in SENSITIVE else v) for k, v in parse_qsl(p.query, keep_blank_values=True)]
        return urlunsplit((p.scheme, host, p.path, urlencode(query), ""))
    except ValueError:
        return "[INVALID_URL]"


class Redactor:
    def __init__(self):
        self.secrets = set()

    def add(self, value):
        if value:
            self.secrets.add(str(value))

    def text(self, value):
        for secret in sorted(self.secrets, key=len, reverse=True):
            value = value.replace(secret, "[REDACTED]") if len(secret) >= 4 else re.sub(r"(?<!\w)" + re.escape(secret) + r"(?!\w)", "[REDACTED]", value)
        return re.sub(r"(?:https?|socks5h?)://[^\s\"'<>]+", lambda m: clean_url(m.group()), value)

    def value(self, value):
        if isinstance(value, dict):
            return {str(k): "[REDACTED]" if str(k).lower() in SENSITIVE else self.value(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [self.value(v) for v in value]
        return self.text(value) if isinstance(value, str) else value


REDACTOR = Redactor()


def proxy_input(args, required=True):
    value = os.environ.get("PROXYLANE_PROXY_URL", "")
    if args.proxy_file:
        # A private user-provided file containing one URL, never printed or copied.
        value = Path(args.proxy_file).read_text().strip()
    if not value:
        if required:
            raise CollectionError("missing_input", "proxy_required", "Supply PROXYLANE_PROXY_URL or --proxy-file with an approved ProxyLane HTTP connection")
        return None
    p = urlsplit(value)
    if p.scheme not in {"http", "https"} or not p.hostname or not p.port or p.path not in {"", "/"} or p.query:
        raise CollectionError("input_error", "unsupported_proxy", "This adapter accepts HTTP/HTTPS proxy URLs with an explicit port; SOCKS is not in this release contract")
    REDACTOR.add(value)
    REDACTOR.add(p.username)
    REDACTOR.add(p.password)
    REDACTOR.add(unquote(p.username or ""))
    REDACTOR.add(unquote(p.password or ""))
    return value


def proxy_metadata(value):
    return {"configured": bool(value), "provider": "user-supplied ProxyLane connection", "provenance_verified": False, "exit_ip_verified": False}


def http_session(proxy=None):
    import requests

    class BoundedSession(requests.Session):
        def request(self, *args, **kwargs):
            kwargs.setdefault("timeout", (8, 20))
            return super().request(*args, **kwargs)

    session = BoundedSession()
    session.trust_env = False
    if proxy:
        session.proxies.update({"http": proxy, "https": proxy})
    return session


def bounded_get(session, url, attempts=2, **kwargs):
    for attempt in range(attempts):
        response = session.get(url, **kwargs)
        if response.status_code not in {429, 500, 502, 503, 504} or attempt == attempts - 1:
            break
        time.sleep(0.5 * (attempt + 1))
    if response.status_code in {401, 403, 407, 429}:
        raise CollectionError("blocked", f"http_{response.status_code}", "Target or proxy rejected the request; retries do not guarantee access")
    response.raise_for_status()
    return response


def persist(args, name, raw):
    # Evidence is the exact selected DOM/API input after credential redaction, not
    # a full browser profile, cookie jar, unfiltered script state, or screenshot.
    raw = REDACTOR.value(raw)
    payload = json.dumps(raw, ensure_ascii=False, sort_keys=True, indent=2).encode()
    record = {"name": name, "sha256": hashlib.sha256(payload).hexdigest(), "bytes": len(payload), "redacted": True}
    if args.out:
        directory = Path(args.out)
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        path = directory / (name + ".raw.json")
        path.write_bytes(payload)
        path.chmod(0o600)
        record["path"] = path.name
    else:
        record["input"] = raw
    return record


def normalize(rows, identity):
    output, seen = [], set()
    for row in rows:
        key = row.get(identity)
        if key is None or key == "":
            key = hashlib.sha256(json.dumps(row, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        if str(key) in seen:
            continue
        seen.add(str(key))
        output.append(REDACTOR.value(row))
    return output


def outcome(args, status, observations=None, diagnostics=None, evidence=None, **extra):
    return REDACTOR.value({
        "schema_version": "1.0", "mode": args.mode, "status": status,
        "proof_mode": "fixture" if args.fixture else "live",
        "observed_at": FIXTURE_TIME if args.fixture else datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "observations": observations or [], "diagnostics": diagnostics or [],
        "evidence": evidence or [], **extra,
    })


def fixture(mode):
    return json.loads((ROOT / "fixtures" / f"{mode}.json").read_text())


def video_id(value):
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value or ""):
        return value
    p = urlsplit(value or "")
    if p.hostname in {"youtu.be", "www.youtu.be"}:
        result = p.path.strip("/")
    elif p.hostname in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        result = parse_qs(p.query).get("v", [""])[0]
        if not result and p.path.startswith(("/shorts/", "/embed/")):
            result = p.path.split("/")[2]
    else:
        result = ""
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", result):
        raise CollectionError("input_error", "video_id_required", "Supply an 11-character YouTube video id or supported YouTube video URL")
    return result


def transcript(args):
    if args.fixture:
        raw = fixture(args.mode)
        proxy = None
    else:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api.proxies import GenericProxyConfig
        identifier = video_id(args.target)
        proxy = proxy_input(args)
        session = http_session(proxy)
        api = YouTubeTranscriptApi(http_client=session, proxy_config=GenericProxyConfig(http_url=proxy, https_url=proxy))
        languages = args.languages.split(",")
        fetched = None
        for attempt in range(args.attempts):
            try:
                fetched = api.fetch(identifier, languages=languages)
                break
            except Exception as error:
                name = type(error).__name__
                if "407" in str(error) and "proxy" in str(error).casefold():
                    raise CollectionError("blocked", "proxy_auth_required", "Proxy CONNECT authentication was rejected (407); source content was not reached") from error
                if name in {"RequestBlocked", "IpBlocked", "YouTubeRequestFailed"} and attempt + 1 < args.attempts:
                    time.sleep(0.5)
                    continue
                if name in {"NoTranscriptFound", "TranscriptsDisabled", "VideoUnavailable", "VideoUnplayable", "AgeRestricted"}:
                    raise CollectionError("no_data", name, "No retrievable caption track for the requested video/languages; a proxy does not create missing captions") from error
                raise CollectionError("blocked" if name in {"RequestBlocked", "IpBlocked"} else "error", name, str(error)) from error
        raw = {"video_id": fetched.video_id, "language": fetched.language, "language_code": fetched.language_code,
               "is_generated": fetched.is_generated, "segments": fetched.to_raw_data()}
        if raw["video_id"] != identifier or raw["language_code"] not in languages:
            raise CollectionError("error", "caption_target_mismatch", "Caption metadata did not match the requested video and language priority list")
        session.close()
    identifier = raw["video_id"]
    rows = []
    for segment in raw["segments"][:args.limit]:
        if not isinstance(segment.get("text"), str) or not segment["text"].strip():
            continue
        start, duration = float(segment["start"]), float(segment["duration"])
        if start < 0 or duration < 0:
            raise CollectionError("error", "invalid_timing", "Source returned a negative caption time")
        rows.append({"video_id": identifier, "text": segment["text"], "start_seconds": start,
                     "duration_seconds": duration, "language": raw["language_code"], "is_generated": raw["is_generated"],
                     "source_url": f"https://www.youtube.com/watch?v={identifier}&t={int(start)}"})
    # Keep distinct captions with the same integer timestamp.
    rows = normalize([{**r, "segment_id": f"{identifier}:{r['start_seconds']}:{hashlib.sha256(r['text'].encode()).hexdigest()[:12]}"} for r in rows], "segment_id")
    truncated = len(raw["segments"]) > args.limit
    return outcome(args, "partial" if truncated else "ok" if rows else "no_data", rows,
                   [{"code": "limit_reached", "message": "Caption segment limit reached"}] if truncated else [],
                   [persist(args, args.mode, raw)], proxy=proxy_metadata(proxy), coverage={"returned": len(rows), "limit": args.limit, "complete_track": not truncated})


def comments(args):
    if args.fixture:
        raw, proxy = fixture(args.mode), None
    else:
        identifier = video_id(args.target)
        proxy = proxy_input(args)
        # yt-dlp accepts --proxy. Put the option into an explicit private config
        # so credentials do not become subprocess argv or collected diagnostics.
        with tempfile.NamedTemporaryFile("w", suffix=".conf", delete=False, dir=args._scratch) as config:
            os.chmod(config.name, 0o600)
            config.write("--proxy " + shlex.quote(proxy) + "\n")
            config_path = config.name
        command = [args.ytdlp, "--ignore-config", "--config-locations", config_path,
                   "--skip-download", "--write-comments", "--dump-single-json", "--no-warnings",
                   "--socket-timeout", "15", "--retries", "0", "--extractor-retries", "0",
                   "--extractor-args", f"youtube:comment_sort={args.comment_sort};max_comments={args.limit}",
                   "https://www.youtube.com/watch?v=" + identifier]
        try:
            completed = None
            for attempt in range(args.attempts):
                completed = subprocess.run(command, capture_output=True, text=True, timeout=max(10, args.timeout - 5))
                if completed.returncode == 0:
                    break
                if attempt + 1 < args.attempts:
                    time.sleep(0.5)
            if completed.returncode:
                if "407" in completed.stderr and "proxy" in completed.stderr.casefold():
                    raise CollectionError("blocked", "proxy_auth_required", "Proxy CONNECT authentication was rejected (407); source content was not reached")
                raise CollectionError("blocked", "ytdlp_failed", REDACTOR.text(completed.stderr[-2000:]))
            raw = json.loads(completed.stdout)
        finally:
            Path(config_path).unlink(missing_ok=True)
        if raw.get("id") != identifier or not raw.get("title"):
            raise CollectionError("error", "target_mismatch", "yt-dlp did not return the requested video id and title")
    rows = []
    for item in raw.get("comments", [])[:args.limit]:
        if not item.get("id") or not isinstance(item.get("text"), str) or not item["text"].strip():
            continue
        rows.append({"comment_id": item["id"], "video_id": raw["id"], "text": item["text"],
                     "likes": item.get("like_count"), "timestamp": item.get("timestamp"), "parent": item.get("parent"),
                     "source_url": f"https://www.youtube.com/watch?v={raw['id']}&lc={item['id']}"})
    rows = normalize(rows, "comment_id")
    diagnostics = [{"code": "bounded_sample", "message": "A ranked bounded sample, not all comments and not a representative VOC survey"}]
    if not rows:
        diagnostics.append({"code": "empty_comments", "message": "Empty response does not distinguish disabled, unavailable or genuinely empty comments"})
    selected_raw = {k: raw.get(k) for k in ("id", "title", "webpage_url", "comment_count", "comments")}
    return outcome(args, "partial" if rows else "no_data", rows, diagnostics, [persist(args, args.mode, selected_raw)],
                   proxy=proxy_metadata(proxy), coverage={"returned": len(rows), "limit": args.limit, "sort": args.comment_sort, "complete": False})


def browser_page(args, proxy, url):
    from playwright.sync_api import sync_playwright
    p = urlsplit(proxy)
    config = {"server": f"{p.scheme}://{p.hostname}:{p.port}"}
    if p.username:
        config["username"], config["password"] = unquote(p.username), unquote(p.password or "")
    runtime = sync_playwright().start()
    try:
        launch = {"headless": not args.visible, "proxy": config}
        if args.browser_executable:
            executable = Path(args.browser_executable)
            if not executable.is_file():
                raise CollectionError("missing_dependency", "browser_executable_missing", "Selected browser executable is absent")
            launch["executable_path"] = str(executable)
        browser = runtime.chromium.launch(**launch)
        context = browser.new_context(locale=args.locale, viewport={"width": 1440, "height": 1000})
        page = context.new_page()
        try:
            response = page.goto(url, wait_until="domcontentloaded", timeout=35000)
        except Exception as error:
            message = str(error)
            if "ERR_INVALID_AUTH_CREDENTIALS" in message or "407" in message:
                raise CollectionError("blocked", "proxy_auth_required", "Browser proxy authentication was rejected; target content was not verified") from error
            if "ERR_HTTP_RESPONSE_CODE_FAILURE" in message:
                raise CollectionError("blocked", "navigation_rejected", "Browser navigation received an unsuccessful HTTP response before semantic fields could be verified; target/proxy status is not established") from error
            raise
        page.wait_for_timeout(min(args.render_wait * 1000, 15000))
        return runtime, browser, context, page, response
    except Exception:
        runtime.stop()
        raise


def blocked_page(html, status=None):
    low = html.lower()
    return status in {401, 403, 407, 429} or any(marker in low for marker in ["unusual traffic from your computer", "sorry/index", "enter the characters you see below", "robot check"])


def google(args):
    if args.fixture:
        raw, proxy = fixture(args.mode), None
    else:
        if not args.query or not args.dom_contract:
            raise CollectionError("missing_input", "google_contract_required", "Supply --query and a reviewed --dom-contract JSON with surface, answer and citation selectors")
        contract = json.loads(Path(args.dom_contract).read_text())
        required = {"surface_selector", "answer_selector", "citation_selector", "surface_marker"}
        if not required.issubset(contract) or not all(isinstance(contract[k], str) and contract[k] for k in required):
            raise CollectionError("input_error", "invalid_dom_contract", "Google DOM contract must specify nonempty surface, answer, citation selectors and visible surface marker")
        if contract.get("reviewed") is not True or contract.get("surface") != args.surface or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(contract.get("observed_on", ""))):
            raise CollectionError("unsupported_surface", "unreviewed_dom_contract", "DOM contract needs reviewed=true, matching surface and observed_on date from actual rendered source-scope validation")
        proxy = proxy_input(args)
        params = {"q": args.query, "hl": args.language, "gl": args.country}
        if args.surface == "ai-mode":
            params["udm"] = "50"
        url = "https://www.google.com/search?" + urlencode(params)
        runtime, browser, context, page, response = browser_page(args, proxy, url)
        try:
            page_html = page.content()
            if blocked_page(page_html, response.status if response else None):
                raise CollectionError("blocked", "google_challenge", "Google returned a challenge or access rejection")
            final = urlsplit(page.url)
            if final.hostname not in {"google.com", "www.google.com"} or parse_qs(final.query).get("q", [""])[0] != args.query:
                raise CollectionError("error", "target_mismatch", "Final page is not the requested Google query")
            root = page.locator(contract["surface_selector"])
            if root.count() != 1 or not root.is_visible():
                raise CollectionError("unsupported_surface", "surface_missing_or_ambiguous", "Reviewed AI surface root is missing or ambiguous; organic links are not substituted")
            root_text = root.inner_text()
            marker_text = root_text
            if contract.get("surface_marker_selector"):
                marker_node = page.locator(contract["surface_marker_selector"])
                if marker_node.count() != 1 or not marker_node.is_visible():
                    raise CollectionError("unsupported_surface", "surface_marker_node_missing", "Reviewed visible AI surface label is missing or ambiguous")
                marker_text = marker_node.inner_text()
            if contract["surface_marker"].casefold() not in marker_text.casefold():
                raise CollectionError("unsupported_surface", "surface_marker_missing", "Expected visible AI surface marker is absent")
            answer = root.locator(contract["answer_selector"])
            if answer.count() != 1 or not answer.is_visible():
                raise CollectionError("unsupported_surface", "answer_missing_or_ambiguous", "The reviewed answer node is missing or ambiguous")
            citations = []
            # Citation selector is evaluated INSIDE the answer, never the
            # surrounding legal/privacy panels or organic SERP results.
            for anchor in answer.locator(contract["citation_selector"]).all()[:args.limit]:
                if anchor.is_visible():
                    citations.append({"url": anchor.get_attribute("href") or "", "title": anchor.inner_text()})
            location = None
            if contract.get("location_selector"):
                node = page.locator(contract["location_selector"])
                if node.count() == 1 and node.is_visible():
                    location = node.inner_text()
            raw = {"url": page.url, "query": args.query, "surface": args.surface, "marker": contract["surface_marker"],
                   "answer_text": answer.inner_text(), "citations": citations, "location_text": location,
                   "requested_country": args.country, "requested_language": args.language, "dom_contract": contract}
        finally:
            context.close(); browser.close(); runtime.stop()
    citations = []
    for citation in raw["citations"]:
        value = urljoin(raw["url"], citation["url"])
        p = urlsplit(value)
        if p.hostname in {"google.com", "www.google.com"} and p.path == "/url":
            value = parse_qs(p.query).get("q", parse_qs(p.query).get("url", [""]))[0]
            p = urlsplit(value)
        if p.scheme not in {"http", "https"} or not p.hostname or p.hostname == "google.com" or p.hostname.endswith(".google.com"):
            continue
        citations.append({"url": clean_url(value), "title": citation.get("title", "")})
    citations = normalize(citations, "url")
    if not raw["answer_text"].strip() or not citations:
        return outcome(args, "no_data", diagnostics=[{"code": "no_cited_answer", "message": "No supported visible answer with external citations was captured"}], evidence=[persist(args, args.mode, raw)])
    row = {"query": raw["query"], "surface": raw["surface"], "answer_text": raw["answer_text"], "citations": citations,
           "source_url": clean_url(raw["url"]), "requested_country": raw["requested_country"], "requested_language": raw["requested_language"],
           "observed_location_text": raw.get("location_text"), "regional_validation": "unverified"}
    return outcome(args, "partial", [row], [{"code": "region_unverified", "message": "gl/hl, proxy configuration and location footer are evidence inputs, not proof of regional causality or a regional ranking"}],
                   [persist(args, args.mode, raw)], proxy=proxy_metadata(proxy), coverage={"citations_returned": len(citations), "limit": args.limit, "expanded_sources": False})


class MCPClient:
    def __init__(self, url):
        p = urlsplit(url)
        if p.scheme not in {"http", "https"} or not p.hostname or p.username or p.password:
            raise CollectionError("input_error", "invalid_mcp_url", "Use a credential-free HTTP(S) MCP endpoint URL")
        self.url, self.session, self.next_id = url, http_session(), 0
        self.headers = {"Accept": "application/json, text/event-stream", "Content-Type": "application/json"}
        token = os.environ.get("XHS_MCP_AUTH_TOKEN", "")
        REDACTOR.add(token)
        if token:
            self.headers["Authorization"] = "Bearer " + token

    def call(self, method, params=None, notification=False):
        message = {"jsonrpc": "2.0", "method": method, "params": params or {}}
        if not notification:
            self.next_id += 1
            message["id"] = self.next_id
        response = self.session.post(self.url, headers=self.headers, json=message, timeout=(8, 35))
        if response.status_code in {401, 403}:
            raise CollectionError("blocked", "mcp_auth_required", "Existing MCP endpoint rejected authentication")
        response.raise_for_status()
        if response.headers.get("Mcp-Session-Id"):
            self.headers["Mcp-Session-Id"] = response.headers["Mcp-Session-Id"]
        if notification or not response.content:
            return {}
        if "text/event-stream" in response.headers.get("Content-Type", ""):
            messages = [json.loads(line[6:]) for line in response.text.splitlines() if line.startswith("data: ")]
            result = next((m for m in messages if m.get("id") == message["id"]), None)
            if result is None:
                raise CollectionError("error", "mcp_no_result", "MCP stream did not contain the requested JSON-RPC result")
        else:
            result = response.json()
        if result.get("error"):
            raise CollectionError("error", "mcp_rpc_error", json.dumps(result["error"], ensure_ascii=False))
        return result.get("result", {})

    def tool(self, name, arguments=None):
        result = self.call("tools/call", {"name": name, "arguments": arguments or {}})
        if result.get("isError"):
            raise CollectionError("blocked", "mcp_tool_error", json.dumps(result.get("content", []), ensure_ascii=False))
        return result


def mcp_data(result):
    if isinstance(result.get("structuredContent"), dict):
        return result["structuredContent"]
    for item in result.get("content", []):
        if item.get("type") == "text":
            try:
                return json.loads(item["text"])
            except (json.JSONDecodeError, KeyError):
                pass
    raise CollectionError("error", "mcp_shape_unsupported", "Read-only MCP tool did not return supported JSON text/structuredContent")


def xiaohongshu(args):
    if args.fixture:
        raw = fixture(args.mode)
        selected_id = raw["feed_id"]
        proxy = None
    else:
        if not args.mcp_url:
            raise CollectionError("missing_input", "mcp_required", "Supply an existing logged-in --mcp-url; this collector never creates a login or installs a server")
        # XHS proxy is SERVER startup configuration. This environment value is
        # only a declaration and cannot configure or prove a remote server.
        proxy = os.environ.get("XHS_PROXY", "")
        REDACTOR.add(proxy)
        if not proxy:
            raise CollectionError("missing_input", "xhs_proxy_required", "Declare XHS_PROXY matching the existing MCP server startup connection; this client cannot change server egress")
        client = MCPClient(args.mcp_url)
        initialized = client.call("initialize", {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "proxylane-web-evidence", "version": "1.0.0"}})
        client.headers["MCP-Protocol-Version"] = initialized.get("protocolVersion", "2024-11-05")
        client.call("notifications/initialized", notification=True)
        names = set()
        cursor = None
        for _ in range(3):
            tools = client.call("tools/list", {"cursor": cursor} if cursor else {})
            names.update(item.get("name") for item in tools.get("tools", []))
            cursor = tools.get("nextCursor")
            if not cursor:
                break
        if not {"check_login_status", "get_feed_detail"}.issubset(names):
            raise CollectionError("unsupported_surface", "xhs_tools_missing", "Required read-only upstream MCP tools are absent within three discovery pages")
        login = client.tool("check_login_status")
        text = "\n".join(item.get("text", "") for item in login.get("content", []) if item.get("type") == "text")
        if "已登录" not in text or "未登录" in text:
            raise CollectionError("missing_session", "xhs_login_required", "The existing upstream session is not positively confirmed logged in")
        token = os.environ.get("XHS_XSEC_TOKEN", "")
        REDACTOR.add(token)
        selected_id = args.target
        discovery = None
        if not selected_id and args.query:
            if "search_feeds" not in names:
                raise CollectionError("unsupported_surface", "search_tool_missing", "MCP server does not expose search_feeds")
            discovery = mcp_data(client.tool("search_feeds", {"keyword": args.query}))
            feeds = discovery.get("feeds", [])
            selected = next((f for f in feeds if f.get("modelType") == "note" and f.get("id") and f.get("xsecToken")), None)
            if not selected:
                raise CollectionError("no_data", "no_note_found", "No supported note id/xsecToken pair was returned by search_feeds")
            selected_id, token = selected["id"], selected["xsecToken"]
            REDACTOR.add(token)
        if not selected_id or not token:
            raise CollectionError("missing_input", "note_identity_required", "Supply --target note id and XHS_XSEC_TOKEN, or --query to discover one note")
        result = mcp_data(client.tool("get_feed_detail", {"feed_id": selected_id, "xsec_token": token,
                    "load_all_comments": True, "limit": min(args.limit, 100), "click_more_replies": False, "scroll_speed": "normal"}))
        raw = {"feed_id": selected_id, "data": result.get("data", result), "discovery": discovery}
        client.session.close()
    data = raw.get("data", raw)
    note = data.get("note", {})
    if note.get("noteId") != selected_id or not note.get("title") or not isinstance(note.get("desc"), str):
        raise CollectionError("error", "note_target_mismatch", "Detail response lacks matching noteId, title and description")
    source = "https://www.xiaohongshu.com/explore/" + selected_id
    comments_data = data.get("comments", {})
    comment_rows = [{"comment_id": c["id"], "text": c["content"], "likes_text": c.get("likeCount"), "source_url": source}
                    for c in comments_data.get("list", [])[:args.limit] if c.get("id") and isinstance(c.get("content"), str) and c["content"].strip()]
    row = {"note_id": selected_id, "title": note["title"], "text": note["desc"], "source_url": source,
           "interaction_counts_raw": note.get("interactInfo", {}), "comments": normalize(comment_rows, "comment_id"),
           "image_content_read": False}
    return outcome(args, "partial", [row], [{"code": "bounded_note", "message": "One note, bounded top-level comments, no replies/OCR. Server proxy declaration is not independently verified"}],
                   [persist(args, args.mode, raw)], proxy={"configured": bool(proxy), "scope": "existing MCP server declaration", "provenance_verified": False, "exit_ip_verified": False},
                   coverage={"notes": 1, "comments_returned": len(comment_rows), "comment_limit": args.limit, "upstream_has_more": comments_data.get("hasMore"), "complete": False})


def scalar(value):
    if isinstance(value, dict):
        return value.get("@value")
    return value if isinstance(value, (str, int, float)) else None


def product_nodes(value):
    if isinstance(value, list):
        for item in value:
            yield from product_nodes(item)
    elif isinstance(value, dict):
        types = value.get("@type", [])
        if types == "Product" or isinstance(types, list) and "Product" in types:
            yield value
        if "@graph" in value:
            yield from product_nodes(value["@graph"])


def parse_price(html, url, expected_id, platform, variant=None):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    products = []
    for script in soup.select('script[type="application/ld+json"]'):
        try:
            products.extend(product_nodes(json.loads(script.get_text())))
        except (json.JSONDecodeError, TypeError):
            continue
    if platform == "amazon":
        title_node, id_node = soup.select_one("#productTitle"), soup.select_one('input#ASIN')
        title = title_node.get_text(" ", strip=True) if title_node else ""
        identifier = id_node.get("value", "") if id_node else ""
        price_node = soup.select_one("#corePriceDisplay_desktop_feature_div .a-price .a-offscreen, #corePrice_feature_div .a-price .a-offscreen")
        availability_node = soup.select_one("#availability")
        selections = [n.get_text(" ", strip=True) for n in soup.select('[id^="variation_"] .selection')]
        raw = {"selectors": {"title": "#productTitle", "identity": "input#ASIN", "price": "#corePriceDisplay_desktop_feature_div .a-price .a-offscreen, #corePrice_feature_div .a-price .a-offscreen", "availability": "#availability", "variant": '[id^="variation_"] .selection'},
               "title": title, "identifier": identifier, "price_text": price_node.get_text(" ", strip=True) if price_node else None,
               "availability_text": availability_node.get_text(" ", strip=True) if availability_node else None, "variant_text": selections, "jsonld_products": products}
        if not title or identifier != expected_id:
            raise CollectionError("error", "product_target_mismatch", "Amazon page lacks a title and matching ASIN")
        if variant and variant.casefold() not in " ".join(selections).casefold():
            raise CollectionError("error", "variant_mismatch", "Expected variant is not confirmed by selected variation fields")
        if not raw["price_text"] or not raw["availability_text"]:
            raise CollectionError("no_data", "offer_fields_missing", "Matching product lacks the supported price/availability fields; HTTP success is insufficient")
        row = {"product_id": identifier, "title": title, "source_url": clean_url(url), "price_text": raw["price_text"], "price": None,
               "currency": None, "availability_text": raw["availability_text"], "variant_text": selections,
               "shipping_tax_included": "unknown", "offer_identity": "visible desktop offer"}
        return row, raw, [{"code": "currency_not_inferred", "message": "Rendered price text is preserved; ambiguous currency symbols are not converted to a typed price"}]
    matching = [p for p in products if str(scalar(p.get("sku")) or scalar(p.get("productID")) or "") == expected_id]
    if len(matching) != 1:
        raise CollectionError("error", "product_target_mismatch", "JSON-LD must contain exactly one Product with the expected sku/productID")
    product = matching[0]
    title = scalar(product.get("name"))
    offers = product.get("offers", [])
    if isinstance(offers, dict):
        offers = [offers]
    offers = [o for o in offers if isinstance(o, dict) and o.get("@type") == "Offer"]
    if not title or len(offers) != 1:
        raise CollectionError("no_data", "offer_ambiguous", "Requires a named matching Product and one explicit Offer; aggregate/variant ranges are not an observed offer price")
    offer = offers[0]
    price, currency, availability = scalar(offer.get("price")), scalar(offer.get("priceCurrency")), scalar(offer.get("availability"))
    try:
        numeric = Decimal(str(price))
        if not numeric.is_finite() or numeric < 0:
            raise InvalidOperation
    except InvalidOperation as error:
        raise CollectionError("no_data", "invalid_price", "Offer price is not a finite nonnegative decimal") from error
    availability_types = {"InStock", "OutOfStock", "PreOrder", "PreSale", "SoldOut", "BackOrder", "Discontinued", "LimitedAvailability", "OnlineOnly", "InStoreOnly"}
    if not isinstance(currency, str) or not re.fullmatch("[A-Z]{3}", currency) or not isinstance(availability, str) or not availability.startswith(("https://schema.org/", "http://schema.org/")) or availability.rsplit("/", 1)[-1] not in availability_types:
        raise CollectionError("no_data", "offer_fields_missing", "Offer requires explicit ISO currency and schema.org availability")
    if variant and variant.casefold() not in str(title).casefold():
        raise CollectionError("error", "variant_unverified", "Requested variant is not confirmed by the matching Product name")
    row = {"product_id": expected_id, "title": title, "source_url": clean_url(url), "price": str(numeric), "currency": currency,
           "availability": availability, "variant_text": variant, "shipping_tax_included": "unknown", "offer_identity": "JSON-LD Offer"}
    return row, {"matching_product": product}, [{"code": "publisher_structured_data", "message": "An observed publisher Offer, not a checkout verification; shipping/tax and delivery location remain unverified"}]


def price(args):
    if args.fixture:
        raw = fixture(args.mode)
        url, expected_id, platform = raw["url"], raw["expected_id"], raw["platform"]
        row, extracted, diagnostics = parse_price(raw["html"], url, expected_id, platform, raw.get("variant"))
        proxy = None
        evidence_raw = {**raw, "extracted": extracted}
    else:
        p = urlsplit(args.target or "")
        if p.scheme not in {"http", "https"} or not p.hostname or p.username or p.password or not args.expected_id:
            raise CollectionError("input_error", "product_inputs_required", "Supply a credential-free product URL and --expected-id sku/ASIN")
        if args.platform == "amazon":
            if not re.fullmatch(r"[A-Z0-9]{10}", args.expected_id) or not re.fullmatch(r"(?:www\.)?amazon\.(?:com|co\.uk|de|fr|it|es|co\.jp|ca|com\.au|in)", p.hostname) or not re.search(r"/(?:dp|gp/product)/" + re.escape(args.expected_id) + r"(?:/|$)", p.path):
                raise CollectionError("input_error", "amazon_product_url_required", "Amazon mode accepts a known product /dp/ASIN or /gp/product/ASIN URL on listed Amazon markets")
        proxy = proxy_input(args)
        runtime, browser, context, page, response = browser_page(args, proxy, args.target)
        try:
            html = page.content()
            if blocked_page(html, response.status if response else None):
                raise CollectionError("blocked", "product_challenge", "Product page returned a challenge or access rejection")
            if urlsplit(page.url).hostname != p.hostname:
                raise CollectionError("error", "product_redirect_host", "Product navigation redirected to a different host")
            row, extracted, diagnostics = parse_price(html, page.url, args.expected_id, args.platform, args.variant)
            evidence_raw = {"url": clean_url(page.url), "http_status": response.status if response else None, "extracted": extracted}
        finally:
            context.close(); browser.close(); runtime.stop()
    return outcome(args, "partial", [row], diagnostics, [persist(args, args.mode, evidence_raw)], proxy=proxy_metadata(proxy),
                   coverage={"pages": 1, "pagination": False, "checkout_verified": False, "delivery_location_verified": False})


COLLECTORS = {"youtube-transcript": transcript, "youtube-comments": comments, "google-citations": google, "xiaohongshu": xiaohongshu, "price": price}


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mode", required=True, choices=(*MODES, "demo"))
    p.add_argument("--fixture", action="store_true")
    p.add_argument("--target")
    p.add_argument("--query")
    p.add_argument("--out")
    p.add_argument("--proxy-file")
    p.add_argument("--verify-egress", action="store_true", help="Optional separate HTTP exit-IP probe; no country or target-IP inference")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--attempts", type=int, default=1)
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--languages", default="en")
    p.add_argument("--comment-sort", choices=("top", "new"), default="top")
    local_ytdlp = Path(sys.executable).parent / "yt-dlp"
    p.add_argument("--ytdlp", default=str(local_ytdlp) if local_ytdlp.is_file() else "yt-dlp")
    p.add_argument("--surface", choices=("ai-mode", "ai-overview"), default="ai-overview")
    p.add_argument("--country", default="us")
    p.add_argument("--language", default="en")
    p.add_argument("--locale", default="en-US")
    p.add_argument("--dom-contract")
    p.add_argument("--render-wait", type=int, default=5)
    p.add_argument("--visible", action="store_true")
    p.add_argument("--browser-executable", help="Approved already installed Chromium-family executable; isolated temporary browser context")
    p.add_argument("--mcp-url")
    p.add_argument("--platform", choices=("amazon", "jsonld"), default="amazon")
    p.add_argument("--expected-id")
    p.add_argument("--variant")
    p.add_argument("--_worker", action="store_true", help=argparse.SUPPRESS)
    p.add_argument("--_scratch", help=argparse.SUPPRESS)
    return p


def worker(args):
    if args.mode == "demo":
        if not args.fixture:
            raise CollectionError("input_error", "demo_fixture_only", "Demo requires --fixture; live sources must be requested explicitly one at a time")
        results = []
        for mode in MODES:
            args.mode = mode
            results.append(COLLECTORS[mode](args))
        return {"schema_version": "1.0", "proof_mode": "fixture", "status": "fixture_demo", "results": results}
    probe = None
    if args.verify_egress and not args.fixture:
        if args.mode == "xiaohongshu":
            raise CollectionError("input_error", "xhs_egress_not_client", "Probe XHS server egress in its own runtime; a client-side probe does not verify the server")
        connection = proxy_input(args)
        with http_session(connection) as session:
            body = bounded_get(session, "https://api.ipify.org?format=json", attempts=args.attempts).json()
        import ipaddress
        ip = str(ipaddress.ip_address(body["ip"]))
        probe = {"source": "https://api.ipify.org?format=json", "exit_ip": ip, "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                 "country_verified": False, "target_request_ip_verified": False, "note": "Separate HTTP probe; rotating sessions may use another IP for the target"}
    result = COLLECTORS[args.mode](args)
    if probe:
        result["egress_probe"] = probe
    return result


def main():
    args = parser().parse_args()
    if not 1 <= args.limit <= 500 or not 1 <= args.attempts <= 2 or not 10 <= args.timeout <= 300 or not 0 <= args.render_wait <= 15:
        result = outcome(args, "input_error", diagnostics=[{"code": "invalid_bounds", "message": "limit 1..500, attempts 1..2, timeout 10..300, render-wait 0..15"}])
    elif not args._worker:
        try:
            with tempfile.TemporaryDirectory(prefix="proxylane-evidence-") as scratch:
                # POSIX process group also owns browser/yt-dlp/JS descendants.
                child = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), *sys.argv[1:], "--_worker", "--_scratch", scratch], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
                try:
                    stdout, _ = child.communicate(timeout=args.timeout)
                    result = json.loads(stdout)
                finally:
                    try:
                        os.killpg(child.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    child.wait()
        except subprocess.TimeoutExpired:
            result = outcome(args, "timeout", diagnostics=[{"code": "total_deadline", "message": "Collector exceeded the total wall-clock deadline"}])
        except (json.JSONDecodeError, ValueError):
            result = outcome(args, "error", diagnostics=[{"code": "worker_failed", "message": "Worker did not return the JSON outcome contract"}])
    else:
        try:
            result = worker(args)
        except CollectionError as error:
            result = outcome(args, error.status, diagnostics=[{"code": error.code, "message": str(error)}])
        except (ImportError, FileNotFoundError) as error:
            result = outcome(args, "missing_dependency", diagnostics=[{"code": type(error).__name__, "message": str(error)}])
        except subprocess.TimeoutExpired:
            result = outcome(args, "timeout", diagnostics=[{"code": "source_deadline", "message": "Source subprocess exceeded its deadline"}])
        except Exception as error:
            # Register secret inputs even when dependency/argument processing failed early.
            for name in ("PROXYLANE_PROXY_URL", "XHS_PROXY", "XHS_XSEC_TOKEN", "XHS_MCP_AUTH_TOKEN"):
                REDACTOR.add(os.environ.get(name, ""))
            result = outcome(args, "error", diagnostics=[{"code": type(error).__name__, "message": str(error)}])
    result = REDACTOR.value(result)
    if args.out and not args._worker:
        path = Path(args.out)
        path.mkdir(parents=True, exist_ok=True, mode=0o700)
        receipt = path / "outcome.json"
        receipt.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
        receipt.chmod(0o600)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if result.get("status") in {"ok", "partial", "fixture_demo"} else 2


if __name__ == "__main__":
    sys.exit(main())
