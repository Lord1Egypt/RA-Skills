#!/usr/bin/env python3
"""Teleskopiq CLI. JSON on stdout, progress on stderr; no mutation retries."""

import argparse
import base64
import json
import mimetypes
import os
import re
import shlex
import sys
from datetime import date, time
from pathlib import Path
from urllib.parse import urlparse

import requests

from oauth_login import OAuthCredentials, OAuthError


class APIError(RuntimeError):
    pass


class QuestionPending(APIError):
    def __init__(self, result):
        self.result = result
        super().__init__("AI needs an answer; resume this script with --call-id and --answer.")


SCRIPT_FIELDS = """
    id title content status { name } createdAt updatedAt scheduledFor publishedAt
    activeCheckpointId activeMessageId activeVersionId showForwardMessages
    metadata { titles description tags suggestedPacing { targetMinutes targetWPM targetWords } }
    thumbnailIdeas { text visual } thumbnails { url idea ideaIndex }
    thumbnailAssets { url mimeType } thumbnailsGenerated
    comments { id type text status selectedText contextBefore contextAfter createdAt updatedAt resolvedAt lastAppliedAt }
"""
STYLE_FIELDS = """
    id channelName channelDescription targetAudience tone speakers signature_phrases structure
    vocabulary { words phrases } pacingTargets { targetMinutes targetWPM }
    sourceType originalDescription thumbnailAdditionalInstructions thumbnailAssets
    channelMetrics { wpm { avg median p90 sampleCount } videoLength { avgSeconds sampleCount } computedAt }
"""
HISTORY_FIELDS = """
    id role content files { uri mimeType name } createdAt archivedAt checkpointId
    agentQuestion { callId question options allowCustom answer answeredAt }
"""
VERSION_FIELDS = "id content author createdAt source kind checkpointId parentVersionId messageId"
EVENT_FIELDS = """
    type text reply script thought title patches { search replace } error
    question options allowCustom callId memoryUpdated memoryUpdates
"""
OPERATIONS = {
    "style": "query { styleProfile { " + STYLE_FIELDS + " } }",
    "channel": "query($id: String!) { channel(channelId: $id) { id title platform platformId preferredPublishingDay } }",
    "scripts": "query { scripts { id title status { name } scheduledFor updatedAt } }",
    "search": "query($q: String!, $limit: Int) { searchScripts(q: $q, limit: $limit) { id title status { name } scheduledFor } }",
    "script": "query($id: String!) { script(id: $id) { " + SCRIPT_FIELDS + " } }",
    "create": "mutation($input: CreateScriptInput!) { createScript(input: $input) { id title content status { name } } }",
    "update": "mutation($input: UpdateScriptInput!) { updateScript(input: $input) { success } }",
    "delete": "mutation($id: String!) { deleteScript(id: $id) { success } }",
    "comments": "mutation($id: String!, $comments: [ScriptCommentInput!]!) { updateScriptComments(id: $id, comments: $comments) { success } }",
    "history": "query($id: String!) { chatHistory(pageId: $id) { " + HISTORY_FIELDS + " } }",
    "versions": "query($id: String!) { scriptVersions(pageId: $id) { id checkpoint { " + VERSION_FIELDS + " } latestVersion { " + VERSION_FIELDS + " } manualSnapshots { " + VERSION_FIELDS + " } } }",
    "save-version": "mutation($id: String!, $content: String!) { saveScriptVersion(pageId: $id, content: $content) { success } }",
    "restore-version": "mutation($id: String!, $version: String!) { restoreScriptHistoryVersion(pageId: $id, versionId: $version) { success } }",
    "revert-checkpoint": "mutation($id: String!, $version: String!) { revertToScriptCheckpoint(pageId: $id, checkpointId: $version) { success } }",
    "schedule": "mutation($id: String!, $urgent: Boolean) { autoScheduleScript(scriptId: $id, urgent: $urgent) { scriptId scheduledFor slotsChecked bumped } }",
    "metadata": "subscription($id: String!, $content: String!) { metadataJob(scriptId: $id, scriptContent: $content) { type error result { titles description tags } } }",
    "thumbnail": "mutation($id: String!, $idea: String!, $index: Int, $assets: [ThumbnailAssetInput]) { generateScriptThumbnail(id: $id, idea: $idea, ideaIndex: $index, additionalAssets: $assets) { success url } }",
    "save-asset": "mutation($id: String!, $asset: ThumbnailAssetInput!) { saveScriptThumbnailAsset(id: $id, asset: $asset) { url } }",
    "remove-asset": "mutation($id: String!, $url: String!) { removeScriptThumbnailAsset(id: $id, assetUrl: $url) { success } }",
    "ideas": "subscription { ideasJob { type text error result { ideas } } }",
    "script-ideas": "subscription($id: String!) { scriptIdeasJob(scriptId: $id) { type text error result { ideas } } }",
    "chat": """subscription(
        $id: String!, $message: String!, $content: String, $history: [ChatHistoryInput!]!,
        $files: [FileInput], $tool: AgentToolResponseInput, $comments: [ScriptCommentInput!],
        $apply: Boolean, $kind: String, $pacing: SuggestedPacingInput,
        $selection: String, $context: SelectionContextInput
    ) { chatJob(pageId: $id, message: $message, currentScript: $content, history: $history,
        files: $files, toolResponse: $tool, comments: $comments, applyComments: $apply,
        requestKind: $kind, pacingTarget: $pacing, selection: $selection, selectionContext: $context
    ) { """ + EVENT_FIELDS + " } }",
}
DEFAULT_PROMPT = "Write a complete YouTube script for this video's title using the channel style and pacing. Use Markdown sections and relevant production directions."
STATUSES = ("Draft", "InProgress", "ReadyToShoot", "Recorded", "Editing", "Ready", "Published", "OnIce")


def load_credentials():
    """Read our env file as data, never execute shell code or print its contents."""
    path = Path(os.environ.get("TELESKOPIQ_ENV_FILE", "~/.config/teleskopiq/env")).expanduser()
    if path.is_file():
        for line in path.read_text().splitlines():
            if not re.match(r"^(?:export\s+)?TELESKOPIQ_(?:API_KEY|ENDPOINT)=", line.strip()):
                continue
            try:
                words = shlex.split(line, comments=True)
            except ValueError:
                raise APIError("Invalid credential-file syntax") from None
            if words and words[0] == "export":
                words = words[1:]
            if len(words) != 1:
                raise APIError("Invalid credential-file assignment")
            name, value = words[0].split("=", 1)
            os.environ.setdefault(name, value)


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def json_file(path):
    return json.loads(Path(path).read_text()) if path else None


def content_arg(args):
    if getattr(args, "content_file", None):
        return Path(args.content_file).read_text()
    return getattr(args, "content", None)


def image_asset(path):
    mime, _ = mimetypes.guess_type(path)
    if mime not in {"image/png", "image/jpeg", "image/webp", "image/gif"}:
        raise APIError("Thumbnail assets must be PNG, JPEG, WebP, or GIF images")
    return {"data": base64.b64encode(Path(path).read_bytes()).decode(), "mimeType": mime}


def sse_messages(response):
    """Parse SSE frames, including heartbeats, multiline data and transport errors."""
    event, data = "message", []
    for line in response.iter_lines(chunk_size=1, decode_unicode=True):
        if not line:
            if data or event in ("complete", "error"):
                yield event, "\n".join(data)
            event, data = "message", []
        elif line.startswith("event:"):
            event = line[6:].lstrip(" ")
        elif line.startswith("data:"):
            data.append(line[5:].lstrip(" "))
    if data or event in ("complete", "error"):
        yield event, "\n".join(data)


class Client:
    def __init__(self, key, endpoint="https://teleskopiq.com/api/graphql", timeout=300, oauth=None):
        self.oauth = oauth
        if oauth:
            if oauth.endpoint != endpoint:
                raise APIError('OAuth credentials belong to a different endpoint')
            key = oauth.token()["access_token"]
        if not key:
            raise APIError("Not connected; run login, or set TELESKOPIQ_API_KEY in the environment or ~/.config/teleskopiq/env")
        if not oauth and not re.fullmatch(r"tsk_(.+)_[a-f0-9]{64}", key):
            raise APIError("Invalid Teleskopiq API-key format; check for extra pasted characters before tsk_ or after the key")
        parsed = urlparse(endpoint)
        if parsed.scheme != "https" and not (parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1", "::1"}):
            raise APIError("Use HTTPS for the API endpoint (HTTP is allowed only for localhost)")
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise APIError("API endpoint must not contain credentials, a query, or a fragment")
        self.key, self.endpoint, self.timeout = key, endpoint, timeout
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {key}"})

    @property
    def channel_id(self):
        if self.oauth:
            return self.oauth.token()["channel_id"]
        match = re.fullmatch(r"tsk_(.+)_[a-f0-9]{64}", self.key)
        if not match:
            raise APIError("Cannot extract channel from this credential; expected a Teleskopiq API key")
        return match[1]

    def error(self, message):
        return APIError(str(message).replace(self.key, "[REDACTED]"))

    def payload(self, response):
        try:
            payload = response.json()
        except ValueError:
            raise self.error(f"API returned HTTP {response.status_code} with a non-JSON body") from None
        if isinstance(payload, dict) and payload.get("errors"):
            raise self.error("; ".join(str(e.get("message", "GraphQL error")) for e in payload["errors"]))
        if not response.ok:
            raise self.error(f"API returned HTTP {response.status_code}")
        if not isinstance(payload, dict) or not isinstance(payload.get("data"), dict):
            raise self.error("API response has no GraphQL data")
        return payload["data"]

    def refresh_auth(self):
        if self.oauth:
            self.key = self.oauth.token()["access_token"]
            self.session.headers.update({"Authorization": f"Bearer {self.key}"})

    def gql(self, query, variables=None, long=False):
        self.refresh_auth()
        try:
            with self.session.post(self.endpoint, json={"query": query, "variables": variables or {}},
                                   timeout=(10, self.timeout if long else 30), allow_redirects=False) as response:
                data = self.payload(response)
        except requests.RequestException as exc:
            raise self.error(f"Request failed ({type(exc).__name__}); not retried. Check existing results before retrying.") from None
        for result in data.values():
            if isinstance(result, dict) and result.get("success") is False:
                raise self.error("Operation returned success=false")
        return data

    def op(self, name, variables=None, long=False):
        return self.gql(OPERATIONS[name], variables, long=long)

    def stream(self, name, field, variables=None):
        self.refresh_auth()
        try:
            with self.session.post(self.endpoint, json={"query": OPERATIONS[name], "variables": variables or {}},
                                   headers={"Accept": "text/event-stream"}, stream=True,
                                   timeout=(10, self.timeout), allow_redirects=False) as response:
                response.encoding = "utf-8"
                if not response.ok or "text/event-stream" not in response.headers.get("Content-Type", ""):
                    self.payload(response)
                    raise self.error("Expected an SSE stream")
                for event, raw in sse_messages(response):
                    if event == "complete" and not raw:
                        break
                    try:
                        payload = json.loads(raw)
                    except ValueError:
                        raise self.error("Invalid JSON in SSE stream") from None
                    if event == "error" or (isinstance(payload, dict) and payload.get("errors")):
                        errors = payload.get("errors", []) if isinstance(payload, dict) else payload
                        raise self.error("GraphQL stream error: " + json.dumps(errors))
                    if not isinstance(payload, dict):
                        raise self.error("Invalid GraphQL stream response")
                    job = (payload.get("data") or {}).get(field)
                    if not isinstance(job, dict):
                        continue
                    if job.get("error") or job.get("type") == "error":
                        raise self.error(job.get("error") or "Generation failed")
                    yield job
                    if job.get("type") in {"complete", "question"}:
                        return
        except requests.RequestException as exc:
            raise self.error(f"Stream interrupted ({type(exc).__name__}); not retried. Inspect this script before retrying.") from None
        raise self.error("Stream ended without completion; inspect this script before retrying")

    def terminal(self, name, field, variables=None):
        terminal = None
        for job in self.stream(name, field, variables):
            terminal = job
        if not terminal or terminal.get("type") not in {"complete", "question"}:
            raise self.error("No terminal event received")
        return terminal

    def script(self, script_id):
        script = self.op("script", {"id": script_id}).get("script")
        if not script:
            raise self.error("Script not found")
        return script

    def create(self, title, content=None):
        if not title or not title.strip():
            raise self.error("A nonempty title is required")
        value = {"title": title}
        if content is not None:
            value["content"] = content
        script = self.op("create", {"input": value})["createScript"]
        print(f"Script ID: {script['id']}", file=sys.stderr)
        return script

    def chat(self, script_id, prompt, args):
        script = self.script(script_id)
        history = self.op("history", {"id": script_id})["chatHistory"] or []
        visible = [h for h in history if not h.get("archivedAt")]
        variables = {
            "id": script_id, "message": prompt, "content": script.get("content") or "",
            "history": [{"role": h["role"], "content": h["content"], "files": h.get("files") or []} for h in visible],
        }
        if getattr(args, "call_id", None):
            variables["tool"] = {"callId": args.call_id, "answer": args.answer}
        if getattr(args, "apply_comments", False):
            variables.update({"comments": script["comments"], "apply": True, "kind": "apply_comments"})
        if getattr(args, "request_kind", None):
            variables["kind"] = args.request_kind
        if getattr(args, "pacing_file", None):
            variables["pacing"] = json_file(args.pacing_file)
        if getattr(args, "files_json", None):
            variables["files"] = json_file(args.files_json)
        if getattr(args, "selection_file", None):
            selection = json_file(args.selection_file)
            variables.update({"selection": selection["selection"], "context": {"before": selection["before"], "after": selection["after"]}})
        terminal = self.terminal("chat", "chatJob", variables)
        if terminal["type"] == "question":
            raise QuestionPending({"scriptId": script_id, "status": "needs_answer", "question": terminal})
        # The server persists title, patches, content and checkpoints BEFORE its terminal event.
        # Never replace that canonical state with concatenated stream deltas.
        return {"script": self.script(script_id), "reply": terminal.get("reply"), "status": "complete"}

    def metadata(self, script_id):
        script = self.script(script_id)
        content = script.get("content") or ""
        if not content.strip():
            raise self.error("Cannot generate metadata for an empty script")
        self.terminal("metadata", "metadataJob", {"id": script_id, "content": content})
        return self.script(script_id)

    def thumbnails(self, script_id, args):
        script = self.script(script_id)
        assets = [image_asset(path) for path in (getattr(args, "asset", None) or [])]
        prompt = getattr(args, "prompt", None)
        index = getattr(args, "idea_index", None)
        if prompt:
            jobs = [(None, prompt)]
        else:
            ideas = script.get("thumbnailIdeas") or []
            if not ideas:
                raise self.error("No thumbnail ideas; generate metadata first or provide --prompt")
            if len(ideas) > 3 or (index is not None and index >= len(ideas)):
                raise self.error("Invalid thumbnail idea slot")
            slots = [index] if index is not None else range(len(ideas))
            jobs = [(i, "\n".join(filter(None, [ideas[i].get("visual"),
                    f"Text overlay: {ideas[i]['text']}" if ideas[i].get("text") else None]))) for i in slots]
        if any(not idea.strip() for _, idea in jobs):
            raise self.error("Thumbnail idea is empty")
        results = []
        for slot, idea in jobs:
            # Synchronous resolver returns the result of this exact generation, not a stale slot.
            result = self.op("thumbnail", {"id": script_id, "idea": idea, "index": slot, "assets": assets}, long=True)["generateScriptThumbnail"]
            if not result.get("url"):
                raise self.error("Thumbnail operation completed without a URL")
            results.append({"ideaIndex": slot, "url": result["url"]})
            print(f"Thumbnail slot {slot}: complete", file=sys.stderr)
        return {"scriptId": script_id, "thumbnails": results}


def schedule(client, script_id, args):
    if args.date:
        value = {"id": script_id, "scheduledFor": date.fromisoformat(args.date).isoformat() + "T12:00:00.000Z"}
        if getattr(args, "status", None):
            value["status"] = args.status
        client.op("update", {"input": value})
        return client.script(script_id)
    result = client.op("schedule", {"id": script_id, "urgent": getattr(args, "urgent", False)})
    if getattr(args, "status", None):
        client.op("update", {"input": {"id": script_id, "status": args.status}})
    return result


def run(client, args):
    command = args.command
    sid = getattr(args, "script_id", None)
    if command == "get-style":
        return client.op("style")
    if command == "get-channel":
        return client.op("channel", {"id": client.channel_id})
    if command == "list-scripts":
        return client.op("scripts")
    if command == "search-scripts":
        return client.op("search", {"q": args.query, "limit": args.limit})
    if command == "get-script":
        return client.script(sid)
    if command == "create-script":
        return client.create(args.title, content_arg(args))
    if command == "update-script":
        value = json_file(args.input_file) or {}
        if not isinstance(value, dict):
            raise APIError("--input-file must contain a JSON object")
        value["id"] = sid
        for field in ("title", "status"):
            if getattr(args, field, None) is not None:
                value[field] = getattr(args, field)
        content = content_arg(args)
        if content is not None:
            value["content"] = content
        if len(value) == 1:
            raise APIError("Provide fields to update")
        if "content" in value:
            existing = client.script(sid)
            if existing.get("content", "").strip():
                client.op("save-version", {"id": sid, "content": existing["content"]})
        client.op("update", {"input": value})
        return client.script(sid)
    if command == "delete-script":
        return client.op("delete", {"id": sid})
    if command == "set-comments":
        comments = json_file(args.comments_file)
        if not isinstance(comments, list):
            raise APIError("Comments file must contain a JSON array")
        return client.op("comments", {"id": sid, "comments": comments})
    if command in {"history", "versions"}:
        return client.op(command, {"id": sid})
    if command == "save-version":
        content = content_arg(args)
        if content is None:
            content = client.script(sid).get("content") or ""
        return client.op(command, {"id": sid, "content": content})
    if command in {"restore-version", "revert-checkpoint"}:
        return client.op(command, {"id": sid, "version": args.version_id})
    if command in {"schedule", "auto-schedule"}:
        return schedule(client, sid, args)
    if command == "generate-metadata":
        return client.metadata(sid)
    if command == "generate-thumbnails":
        return client.thumbnails(sid, args)
    if command == "select-thumbnail":
        if args.url not in {t["url"] for t in client.script(sid).get("thumbnails") or []}:
            raise APIError("Select a URL from this script's generated thumbnails")
        return client.op("update", {"input": {"id": sid, "thumbnails": {"selectedUrl": args.url}}})
    if command == "save-asset":
        return client.op(command, {"id": sid, "asset": image_asset(args.file)})
    if command == "remove-asset":
        return client.op(command, {"id": sid, "url": args.url})
    if command == "ideas":
        return client.terminal("script-ideas" if sid else "ideas", "scriptIdeasJob" if sid else "ideasJob", {"id": sid} if sid else {})
    if command in {"chat", "ai-write"}:
        # Fetch style before creating a new record so auth/schema errors leave no orphan script.
        client.op("style")
        if not sid:
            sid = client.create(args.title)["id"]
        result = client.chat(sid, args.prompt or DEFAULT_PROMPT, args)
        if command == "ai-write" and not (result["script"].get("content") or "").strip():
            raise APIError(f"AI returned no script content; inspect script {sid} and its chat history")
        return result
    if command == "full-flow":
        client.op("style")
        if not sid:
            sid = client.create(args.title, None if args.ai_write else content_arg(args))["id"]
        if args.ai_write:
            result = client.chat(sid, args.prompt or DEFAULT_PROMPT, args)
            if not (result["script"].get("content") or "").strip():
                raise APIError(f"AI returned no script content; inspect script {sid}")
        client.metadata(sid)
        # AI writing prompt is not a custom thumbnail prompt.
        thumbnail_args = argparse.Namespace(asset=args.asset, prompt=None, idea_index=None)
        client.thumbnails(sid, thumbnail_args)
        schedule(client, sid, args)
        return client.script(sid)
    if command == "graphql":
        return client.gql(Path(args.query_file).read_text(), json_file(args.variables_file))
    raise APIError("Unknown command")


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--timeout", type=int, default=300, help="Generation read timeout in seconds (no automatic retries)")
    sub = root.add_subparsers(dest="command", required=True)
    for name in ("get-style", "get-channel", "list-scripts"):
        sub.add_parser(name)
    p = sub.add_parser("search-scripts")
    p.add_argument("--query", required=True)
    p.add_argument("--limit", type=int, default=20)
    script_commands = ("get-script", "update-script", "delete-script", "set-comments", "history", "versions",
                       "save-version", "restore-version", "revert-checkpoint", "schedule", "auto-schedule",
                       "generate-metadata", "generate-thumbnails", "select-thumbnail", "save-asset", "remove-asset", "chat")
    parsers = {}
    for name in script_commands:
        parsers[name] = sub.add_parser(name)
        parsers[name].add_argument("--script-id", required=True)
    for name in ("create-script", "ai-write", "full-flow", "ideas"):
        parsers[name] = sub.add_parser(name)
        if name != "create-script":
            parsers[name].add_argument("--script-id")
    for name in ("create-script", "update-script", "ai-write", "full-flow"):
        parsers[name].add_argument("--title", required=name == "create-script")
    for name in ("create-script", "update-script", "save-version", "full-flow"):
        group = parsers[name].add_mutually_exclusive_group()
        group.add_argument("--content")
        group.add_argument("--content-file")
    parsers["update-script"].add_argument("--input-file", help="JSON UpdateScriptInput fields")
    for name in ("update-script", "schedule", "auto-schedule", "full-flow"):
        parsers[name].add_argument("--status", choices=STATUSES)
    parsers["set-comments"].add_argument("--comments-file", required=True)
    for name in ("restore-version", "revert-checkpoint"):
        parsers[name].add_argument("--version-id", required=True)
    for name in ("schedule", "auto-schedule", "full-flow"):
        parsers[name].add_argument("--date", help="Publishing day YYYY-MM-DD; omit for automatic scheduling")
        parsers[name].add_argument("--time", help="Deprecated; publishing schedules store a day, not a time")
        parsers[name].add_argument("--urgent", action="store_true")
    parsers["generate-thumbnails"].add_argument("--idea-index", type=int, choices=range(3))
    parsers["generate-thumbnails"].add_argument("--prompt", help="Generate the single custom thumbnail slot")
    for name in ("generate-thumbnails", "full-flow"):
        parsers[name].add_argument("--asset", action="append", help="Reference image path, repeatable")
    for name in ("select-thumbnail", "remove-asset"):
        parsers[name].add_argument("--url", required=True)
    parsers["save-asset"].add_argument("--file", required=True)
    for name in ("chat", "ai-write", "full-flow"):
        p = parsers[name]
        p.add_argument("--prompt")
        p.add_argument("--call-id")
        p.add_argument("--answer")
        p.add_argument("--apply-comments", action="store_true")
        p.add_argument("--request-kind", choices=("lengthen", "shorten"))
        p.add_argument("--pacing-file", help="JSON targetMinutes/targetWPM/targetWords")
        p.add_argument("--files-json", help="JSON FileInput array using uploaded Gemini URIs")
        p.add_argument("--selection-file", help="JSON selection, before, and after strings")
    parsers["full-flow"].add_argument("--ai-write", action="store_true")
    p = sub.add_parser("graphql", help="Execute a GraphQL document from disk; mutations are not retried")
    p.add_argument("--query-file", required=True)
    p.add_argument("--variables-file")
    login = sub.add_parser("login", help="Authorize this skill in your browser")
    login.add_argument("--no-browser", action="store_true")
    login.add_argument("--scope", default="scripts:read scripts:write thumbnails:write channel:read")
    sub.add_parser("logout", help="Revoke the saved OAuth connection")
    sub.add_parser("auth-status", help="Show saved login metadata without displaying credentials")
    return root


def validate_args(args):
    if args.timeout <= 0:
        raise APIError("--timeout must be positive")
    sid = getattr(args, "script_id", None)
    if args.command in {"ai-write", "full-flow"} and not sid and not args.title:
        raise APIError("Provide --title or an existing --script-id")
    if getattr(args, "call_id", None) or getattr(args, "answer", None) is not None:
        if not sid or not args.call_id or not (args.answer or "").strip():
            raise APIError("Resuming requires --script-id, --call-id, and a nonempty --answer")
    if getattr(args, "date", None):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
            raise APIError("Use a publishing day in YYYY-MM-DD format")
        date.fromisoformat(args.date)
        if args.urgent:
            raise APIError("--urgent applies only to automatic scheduling")
    if getattr(args, "time", None):
        time.fromisoformat(args.time)
        print("--time is ignored: Teleskopiq schedules publishing days, not times.", file=sys.stderr)
    if args.command == "full-flow":
        content = content_arg(args)
        if args.ai_write and content is not None:
            raise APIError("Choose supplied content or --ai-write, not both")
        if sid and content is not None:
            raise APIError("Use update-script for existing content before full-flow --script-id")
        if not sid and not args.ai_write and not (content or "").strip():
            raise APIError("full-flow needs nonempty content or --ai-write")
        if args.call_id and not args.ai_write:
            raise APIError("full-flow question continuation requires --ai-write")
    if args.command == "generate-thumbnails" and args.prompt and args.idea_index is not None:
        raise APIError("Choose --prompt for a custom thumbnail or --idea-index for an idea slot")
    if args.command == "search-scripts" and args.limit <= 0:
        raise APIError("--limit must be positive")
    # Read local inputs before creating any remote records.
    for field in ("input_file", "comments_file", "pacing_file", "files_json", "selection_file", "variables_file"):
        path = getattr(args, field, None)
        if path:
            value = json_file(path)
            expected = list if field in {"comments_file", "files_json"} else dict
            if not isinstance(value, expected):
                raise APIError(f"--{field.replace('_', '-')} must contain a JSON {expected.__name__}")
            if field == "selection_file" and not all(isinstance(value.get(key), str) for key in ("selection", "before", "after")):
                raise APIError("Selection file needs selection, before, and after strings")
    content_arg(args)
    for path in getattr(args, "asset", None) or []:
        image_asset(path)


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        validate_args(args)
        load_credentials()
        endpoint = os.environ.get("TELESKOPIQ_ENDPOINT", "https://teleskopiq.com/api/graphql")
        oauth_path = Path(os.environ.get("TELESKOPIQ_OAUTH_FILE", "~/.config/teleskopiq/oauth.json")).expanduser()
        oauth = OAuthCredentials(endpoint) if oauth_path.exists() or args.command in {"login", "logout", "auth-status"} else None
        if args.command in {"login", "logout", "auth-status"}:
            result = oauth.login(args.no_browser, args.scope) if args.command == "login" else (
                oauth.logout() if args.command == "logout" else oauth.status())
            emit(result)
            return 0
        client = Client(os.environ.get("TELESKOPIQ_API_KEY", ""), endpoint, args.timeout,
                        oauth=oauth)
        emit(run(client, args))
        return 0
    except QuestionPending as exc:
        emit(exc.result)
        return 2
    except (APIError, OAuthError, ValueError, OSError) as exc:
        key = os.environ.get("TELESKOPIQ_API_KEY", "")
        message = str(exc).replace(key, "[REDACTED]") if key else str(exc)
        print(f"Error: {message}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrupted; inspect the existing script before retrying.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
