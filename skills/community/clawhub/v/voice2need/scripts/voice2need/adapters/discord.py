"""Import DiscordChatExporter JSON; optionally launch an explicitly scoped export.

Never discovers, joins or changes accounts. Images/video are not downloaded.
Truncated exports are recovered into new raw envelopes, never repaired in place.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import uuid
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from datetime import datetime
from pathlib import Path

from ..records import in_window, iso_time, make_record
from ..runtime import SourceError, require_env


def decode_export(blob):
    """Read top-level properties and complete messages up to a broken tail.

    Streaming JSON decoder honors strings/escapes: a literal '"messages":['
    inside a message is not mistaken for the real array.
    """
    encoding_truncated = False
    try:
        text = blob.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        if exc.end != len(blob):
            raise SourceError("schema-drift", "Export contains invalid UTF-8; original bytes are preserved") from None
        text = blob[:exc.start].decode("utf-8-sig")
        encoding_truncated = True
    try:
        data = json.loads(text)
        if not isinstance(data, dict) or not isinstance(data.get("messages"), list):
            raise SourceError("schema-drift", "Expected a DiscordChatExporter JSON object with messages")
        return data, encoding_truncated
    except json.JSONDecodeError:
        pass
    decoder = json.JSONDecoder()
    pos, result = 0, {}

    def space(p):
        while p < len(text) and text[p].isspace():
            p += 1
        return p

    pos = space(pos)
    if pos >= len(text) or text[pos] != "{":
        raise SourceError("schema-drift", "Cannot recover an export without its JSON header")
    pos += 1
    try:
        while True:
            pos = space(pos)
            if text[pos] == ",":
                pos = space(pos + 1)
            key, pos = decoder.raw_decode(text, pos)
            if not isinstance(key, str):
                break
            pos = space(pos)
            if text[pos] != ":":
                break
            pos = space(pos + 1)
            if key == "messages":
                if text[pos] != "[":
                    break
                pos += 1
                messages = []
                while True:
                    pos = space(pos)
                    if pos >= len(text) or text[pos] == "]":
                        break
                    try:
                        value, pos = decoder.raw_decode(text, pos)
                    except json.JSONDecodeError:
                        break
                    if not isinstance(value, dict):
                        break
                    messages.append(value)
                    pos = space(pos)
                    if pos >= len(text) or text[pos] != ",":
                        break
                    pos += 1
                result["messages"] = messages
                return result, True
            result[key], pos = decoder.raw_decode(text, pos)
    except (IndexError, json.JSONDecodeError):
        pass
    raise SourceError("schema-drift", "Export header is incomplete; original bytes are preserved")


def _import(ctx, job, paths):
    imported, recovered, selected, skipped, context_count, gaps = 0, 0, 0, 0, 0, []
    for path in paths:
        copied = ctx.import_raw(path)
        blob = ctx.path(copied["path"]).read_bytes()
        try:
            data, truncated = decode_export(blob)
        except SourceError as exc:
            gaps.append({"status": exc.status, "raw": copied, "detail": str(exc)})
            continue
        imported += 1
        channel = data.get("channel") or {}
        guild = data.get("guild") or {}
        if not isinstance(channel, dict) or not isinstance(guild, dict):
            gaps.append({"status": "schema-drift", "detail": "Invalid guild/channel metadata", "raw": copied})
            continue
        channel_id, guild_id = str(channel.get("id") or ""), str(guild.get("id") or "")
        if not channel_id.isdigit() or not guild_id.isdigit():
            gaps.append({"status": "schema-drift", "detail": "Missing guild/channel IDs", "raw": copied})
            continue
        # DCE calls a thread's parent `categoryId`; `category` is only its name.
        parent_channel_id = str(channel.get("categoryId") or "")
        if (job.get("channel_ids") and channel_id not in [str(c) for c in job["channel_ids"]]
                and not ("thread" in str(channel.get("type", "")).lower()
                         and parent_channel_id in [str(c) for c in job["channel_ids"]])):
            skipped += len(data["messages"])
            continue
        if str(channel.get("name") or "").lower() in job.get("skip_channel_names", ["welcome", "rules", "rank"]):
            skipped += len(data["messages"])
            continue
        if truncated:
            recovered += len(data["messages"])
            base = ctx.write_raw(data, recovery={"source": copied, "complete_messages_only": True})
            base_locator = "$.data"
            gaps.append({"status": "partial", "detail": "Recovered complete messages; export tail missing", "raw": copied})
        else:
            base, base_locator = copied, "$"
        records = []
        by_id = {str(message.get("id")): message for message in data["messages"] if isinstance(message, dict)}
        in_scope = {mid for mid, message in by_id.items()
                    if in_window(message.get("timestamp"), job.get("start"), job.get("end"))}
        retained = set(in_scope)
        for mid in in_scope:
            visited = {mid}
            message = by_id[mid]
            while isinstance(message.get("reference"), dict):
                reference = message["reference"]
                parent = str(reference.get("messageId") or "")
                if reference.get("channelId") and str(reference["channelId"]) != channel_id:
                    break
                if parent not in by_id or parent in visited:
                    break
                visited.add(parent)
                retained.add(parent)
                message = by_id[parent]
        for index, message in enumerate(data["messages"]):
            if not isinstance(message, dict) or not str(message.get("id", "")).isdigit():
                gaps.append({"status": "schema-drift", "detail": "Message without an ID", "index": index})
                continue
            if str(message["id"]) not in retained:
                skipped += 1
                continue
            mid = str(message["id"])
            reference = message.get("reference") or {}
            author = message.get("author") or {}
            if not isinstance(reference, dict) or not isinstance(author, dict):
                gaps.append({"status": "schema-drift", "detail": "Invalid message author/reference", "index": index})
                continue
            parent = reference.get("messageId")
            if parent and str(parent) not in retained:
                gaps.append({"status": "partial", "detail": "Referenced parent is outside supplied context",
                             "message_id": mid, "parent_id": str(parent)})
            within = mid in in_scope
            context_count += int(not within)
            metadata = {"guild_id": guild_id, "channel_id": channel_id,
                        "channel_name": channel.get("name"), "guild_name": guild.get("name"),
                        "channel_parent_id": parent_channel_id or None,
                        "reference_channel_id": reference.get("channelId"),
                        "message_type": message.get("type"), "recovered": truncated,
                        "attachment_count": len(message.get("attachments") or []),
                        "in_window": within, "context_only": not within}
            records.append(make_record(
                "discord", mid, "message", message.get("content") or "",
                author.get("id"), message.get("timestamp"),
                f"https://discord.com/channels/{guild_id}/{channel_id}/{mid}", channel_id,
                parent_id=str(parent) if parent else None,
                raw=[dict(base, locator=f"{base_locator}.messages[{index}]")], metadata=metadata))
        ctx.add_records(records)
        selected += len(records)
    return {"job_id": job["id"], "platform": "discord",
            "status": "partial" if gaps else ("complete" if selected else "no-results"),
            "counts": {"files": imported, "messages": selected, "recovered": recovered, "skipped": skipped,
                       "context_messages": context_count},
            "gaps": gaps, "completeness": "Supplied exports only; not all server channels"}


def _export_one(ctx, job, command, token, channel, relative, timeout):
    """One process and one DCE worker; private output never reaches the console."""
    directory = ctx.path(relative)
    directory.mkdir(parents=True, exist_ok=True)
    args = command + ["export", "-c", channel, "-f", "Json", "-o", str(directory) + os.sep,
                      "--after", iso_time(job["start"]), "--before", iso_time(job["end"]),
                      "--include-threads", "All", "--parallel", "1", "--media", "false",
                      "--markdown", "false", "--respect-rate-limits", "true"]
    stdout, stderr, code, status = b"", b"", None, "complete"
    try:
        result = subprocess.run(args, env={**os.environ, "DISCORD_TOKEN": token},
                                capture_output=True, timeout=timeout, check=False)
        stdout, stderr, code = result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired as exc:
        stdout, stderr, status = exc.stdout or b"", exc.stderr or b"", "timeout"
    except OSError:
        status = "start-failed"
    def clean(value):
        text = value.decode("utf-8", "replace") if isinstance(value, bytes) else str(value or "")
        return text.replace(token, "[REDACTED]")
    out, err = clean(stdout), clean(stderr)
    log_ref = ctx.write_raw({"stdout": out, "stderr": err, "exit_code": code,
                            "process_status": status}, kind="dce-log", channel_id=channel)
    paths = [str(path.relative_to(ctx.root)) for path in sorted(directory.rglob("*.json"))]
    gaps = []
    log = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", out + "\n" + err).lower()
    # DCE returns exit 0 when only some constituent threads failed.
    partial_output = any(phrase in log for phrase in (
        "failed to export the following", "missing access", "missing permissions",
        "forbidden", "unauthorized", "insufficient permission", "don't have access",
        "do not have access", "cannot access", "could not access",
    ))
    if status != "complete":
        gaps.append({"status": status, "channel_id": channel, "raw": log_ref})
    elif code != 0:
        status = "export-failed"
        gaps.append({"status": status, "channel_id": channel, "exit_code": code, "raw": log_ref})
    elif partial_output:
        status = "partial"
        gaps.append({"status": "thread-or-channel-permission-gap", "channel_id": channel, "raw": log_ref})
    elif not paths:
        status = "partial"
        gaps.append({"status": "empty-export-unverified", "channel_id": channel, "raw": log_ref})
    return {"status": status, "paths": paths, "raw": log_ref, "gaps": gaps, "directory": relative}


def _export(ctx, job):
    if not ctx.live:
        raise SourceError("invalid-input", "Discord export needs --live and approved visible channel IDs")
    if job.get("account_confirmed") is not True or job.get("access_confirmed") is not True:
        raise SourceError("forbidden", "Confirm the intended account and access to these specific channels first")
    channels = job.get("channel_ids", [])
    if not isinstance(channels, list) or not channels or any(not str(c).isdigit() for c in channels):
        raise SourceError("invalid-input", "Provide individual text/forum channel IDs, not categories or a whole guild")
    channels = list(dict.fromkeys(str(channel) for channel in channels))
    command = job.get("dce_command")
    if not isinstance(command, list) or not command or not all(isinstance(c, str) for c in command):
        raise SourceError("invalid-input", "Set dce_command to an installed executable, or dotnet plus its DLL")
    if not (len(command) == 1 or (len(command) == 2 and Path(command[0]).name == "dotnet"
                                  and command[1].lower().endswith(".dll"))):
        raise SourceError("invalid-input", "dce_command accepts only one executable or dotnet plus its DLL; no flags")
    if not job.get("start") or not job.get("end"):
        raise SourceError("invalid-input", "Discord export requires an explicit start and end")
    start, end = iso_time(job["start"]), iso_time(job["end"])
    if not start or not end or datetime.fromisoformat(start.replace("Z", "+00:00")) >= datetime.fromisoformat(end.replace("Z", "+00:00")):
        raise SourceError("invalid-input", "Discord export requires a valid increasing timestamp window")
    parallel = job.get("parallel", 2)
    if isinstance(parallel, bool) or parallel not in (1, 2):
        raise SourceError("invalid-input", "Discord parallel must be 1 or 2; respect service rate limits")
    timeout = job.get("timeout_seconds", 3600)
    if isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= 86400:
        raise SourceError("invalid-input", "timeout_seconds must be between 1 and 86400")
    token = require_env("DISCORD_TOKEN")
    state = ctx.get_checkpoint(job["id"])
    completed = dict(state.get("exported_channels", {}))
    channel_runs = dict(state.get("channel_runs", {}))
    all_paths, gaps, pending, interrupted = [], [], [], False
    for channel in channels:
        if channel in completed:
            existing = [ctx.path(path) for path in completed[channel]]
            if all(path.is_file() for path in existing):
                all_paths.extend(str(path) for path in existing)
            else:
                interrupted = True
                gaps.append({"status": "checkpoint-files-missing", "channel_id": channel})
            continue
        previous = channel_runs.get(channel)
        if previous:
            # A crashed exporter may still be alive. Never launch a duplicate.
            interrupted = True
            gaps.extend(previous.get("gaps", []))
            gaps.append({"status": "export-resume-needs-review", "channel_id": channel,
                         "previous_status": previous.get("status")})
            for path in previous.get("paths", []):
                if ctx.path(path).is_file():
                    all_paths.append(str(ctx.path(path)))
            if previous.get("status") == "running":
                gaps.append({"status": "export-outcome-indeterminate", "channel_id": channel,
                             "output_directory": previous.get("directory")})
        else:
            pending.append(channel)

    def checkpoint():
        ctx.checkpoint(job["id"], {"exported_channels": completed, "channel_runs": channel_runs})

    # Keep at most `parallel` tasks submitted. Inspect every completed task before
    # refilling a slot, so any observed failure prevents subsequent starts.
    if not interrupted:
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            active = {}
            def fill():
                while pending and len(active) < parallel and not interrupted:
                    channel = pending.pop(0)
                    relative = f"exports/{uuid.uuid4().hex}"
                    channel_runs[channel] = {"status": "running", "directory": relative, "paths": []}
                    checkpoint()
                    active[executor.submit(_export_one, ctx, job, command, token, channel, relative, timeout)] = channel
            fill()
            while active:
                done, _ = wait(active, return_when=FIRST_COMPLETED)
                for future in done:
                    channel = active.pop(future)
                    outcome = future.result()
                    channel_runs[channel] = outcome
                    all_paths.extend(str(ctx.path(path)) for path in outcome["paths"])
                    gaps.extend(outcome["gaps"])
                    if outcome["status"] == "complete":
                        completed[channel] = outcome["paths"]
                    else:
                        interrupted = True
                    checkpoint()
                fill()
    # Thread exports have their own channel IDs and categoryId=parent channel.
    result = _import(ctx, job, list(dict.fromkeys(all_paths)))
    result["gaps"].extend(gaps)
    result["export"] = {"channels_requested": channels, "completed_channels": sorted(completed),
                        "channels_not_started": pending, "process_parallelism": parallel,
                        "dce_parallelism_per_process": 1}
    result["limitations"] = [
        "DCE may silently omit inaccessible threads during discovery; thread population completeness is unverified.",
        "DCE performs its own API requests, outside Session request/unit accounting.",
    ]
    if interrupted:
        result["status"] = "partial"
        result["gaps"].append({"status": "export-interrupted", "detail": "Inspect saved exporter log; remaining channels not attempted"})
    return result


def collect(ctx, job):
    if job.get("mode", "import") == "export":
        return _export(ctx, job)
    if job.get("mode", "import") != "import":
        raise SourceError("invalid-input", "Discord mode must be import or export")
    paths = job.get("input", [])
    if isinstance(paths, str):
        paths = [paths]
    if not paths or not isinstance(paths, list):
        raise SourceError("invalid-input", "Provide exported JSON paths in input")
    return _import(ctx, job, paths)
