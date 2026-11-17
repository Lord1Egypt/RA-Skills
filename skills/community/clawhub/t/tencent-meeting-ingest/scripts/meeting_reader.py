import datetime as dt
import json
import os
import re
import shutil
import tempfile
import time
from pathlib import Path

from external_skill_bridge import find_first_key, text_from_any
from gitea_api import GiteaClient
from tencent_meeting_bridge import call_tencent_tool
from utils import now, read_json_file, sha256_text, slugify, unique, write_json_file


MAX_WINDOW_DAYS = 31
DEFAULT_WINDOW_DAYS = 31
DEFAULT_HISTORY_DAYS = 14
DEFAULT_INCREMENTAL_OVERLAP_DAYS = 1
DEFAULT_MAX_RECORDS = 30
DEFAULT_PAGE_SIZE = 10
DEFAULT_CONTENT_PREVIEW_CHARS = 12000
DEFAULT_ENDED_MEETINGS_FALLBACK_RECENT_DAYS = 14
MEETING_OCCURRENCE_MERGE_TOLERANCE_MINUTES = 10
MAX_RECORDS = 500
PREPARE_CACHE_VERSION = 1


def prepare_context(payload):
    source = payload.get("source") or {}
    source_id = source.get("id") or payload.get("sourceId") or "tencent_meeting"
    config = source.get("config") or {}
    previous = source.get("lastSnapshot") or {}
    if not isinstance(previous, dict):
        previous = {}
    page_output = initialize_page_output(payload)

    scan_started_at = now()
    candidates, collect_errors = collect_candidate_records(source, config, previous)
    scan_complete = not collect_errors
    previous_hashes = previous.get("recordContentHashes") or {}
    if not isinstance(previous_hashes, dict):
        previous_hashes = {}

    client = GiteaClient(payload)
    input_items = []
    skipped = []
    incomplete = []
    archived_files = []
    content_hashes = dict(previous_hashes)
    processed_keys = set(previous.get("processedRecordKeys") or [])

    for record in candidates:
        material = materialize_record(record)
        record_key = material["recordKey"]
        if not material["smartMinutes"] and not material["transcript"]:
            incomplete.append({
                "recordKey": record_key,
                "title": material["title"],
                "reason": "no_minutes_or_transcript",
                "errors": material["errors"],
            })
            continue
        content_hash = material_content_hash(material)
        if previous_hashes.get(record_key) == content_hash:
            skipped.append({"recordKey": record_key, "reason": "unchanged"})
            processed_keys.add(record_key)
            continue
        archived_path = archive_meeting_source(client, source_id, material, content_hash)
        archived_files.append(archived_path)
        processed_keys.add(record_key)
        content_hashes[record_key] = content_hash
        input_items.append(source_item(source_id, material, archived_path, content_hash, config))

    scan_finished_at = now()
    scan_until = scan_finished_at if scan_complete else str(previous.get("scanUntil") or "")
    snapshot = {
        "sourceId": source_id,
        "scanStartedAt": scan_started_at,
        "scanFinishedAt": scan_finished_at,
        "scanUntil": scan_until,
        "scanComplete": scan_complete,
        "scanErrors": collect_errors,
        "processedRecordKeys": sorted(processed_keys)[-2000:],
        "recordContentHashes": dict(sorted(content_hashes.items())[-2000:]),
        "candidateCount": len(candidates),
        "newOrChangedCount": len(input_items),
        "incompleteCount": len(incomplete),
    }

    return {
        "mode": "skip" if not input_items else "ingest",
        "skill": "tencent_meeting_ingest",
        "source": {
            "id": source_id,
            "type": "tencent_meeting",
            "name": source.get("name") or "腾讯会议",
            "config": safe_context_config(config),
        },
        "scanPolicy": {
            "initialScan": not bool(previous.get("scanUntil")),
            "historyLookbackDays": int_value(config.get("historyLookbackDays") or config.get("lookbackDays"), DEFAULT_HISTORY_DAYS),
            "incrementalOverlapDays": int_value(config.get("incrementalOverlapDays"), DEFAULT_INCREMENTAL_OVERLAP_DAYS),
            "maxRecords": max_records(config),
            "pageSize": page_size(config),
            "windowDays": scan_window_days(config),
            "maxWindowDays": MAX_WINDOW_DAYS,
            "contentPreviewChars": content_preview_chars(config),
            "fallbackToEndedMeetings": bool_value(config.get("fallbackToEndedMeetings"), True),
            "endedMeetingsFallbackRecentDays": ended_meetings_fallback_recent_days(config),
            "scanComplete": scan_complete,
        },
        "analysisLimits": {
            "maxInputItems": max_records(config),
            "maxContentPreviewChars": content_preview_chars(config),
            "maxMeetingPagesPerItem": 1,
            "recommendedRelatedPageUpdates": 0,
            "maxRelatedPageUpdates": 2,
        },
        "inputItems": input_items,
        "archivedFiles": archived_files,
        "skippedSources": skipped,
        "incompleteItems": incomplete,
        "errors": [{"message": item} for item in collect_errors],
        "snapshot": snapshot,
        "pageOutput": page_output,
        "pageInstructions": meeting_page_instructions(),
    }


def collect_candidate_records(source, config, previous):
    explicit = explicit_records(source, config)
    if explicit:
        return merge_records_by_meeting_occurrence(expand_record_file_variants(explicit)), []

    windows = scan_windows(config, previous)
    errors = []
    records = []
    record_limit = max_records(config)
    source_record_limit = min(MAX_RECORDS * 3, record_limit * 3)
    include_ended_meetings = bool_value(config.get("includeEndedMeetings"), False)
    fallback_to_ended_meetings = bool_value(config.get("fallbackToEndedMeetings"), True)
    stop_scanning = False
    for window in windows:
        window_records = []
        try:
            window_records = paged_tool(
                "get_records_list",
                {"start_time": window["start"], "end_time": window["end"], "page_size": page_size(config)},
                {"record_file_id", "recordFileId", "meeting_record_id", "meetingRecordId", "meeting_id", "meetingId"},
                limit=max(1, source_record_limit - len(records)),
            )
            records.extend(window_records)
        except Exception as exc:
            message = f"get_records_list {window['start']}..{window['end']} failed: {exc}"
            errors.append(message)
            if is_quota_error(message):
                break

        should_fetch_ended_meetings = include_ended_meetings or (
            fallback_to_ended_meetings
            and not window_records
            and is_recent_ended_meetings_fallback_window(window, config)
        )
        if not should_fetch_ended_meetings:
            continue

        try:
            ended_meetings = paged_tool(
                "get_user_ended_meetings",
                {"start_time": window["start"], "end_time": window["end"], "page_size": page_size(config)},
                {"meeting_id", "meetingId", "meeting_code", "meetingCode", "subject", "topic"},
                limit=record_limit,
            )
        except Exception as exc:
            message = f"get_user_ended_meetings {window['start']}..{window['end']} failed: {exc}"
            errors.append(message)
            if is_quota_error(message):
                break
            ended_meetings = []

        for meeting in ended_meetings:
            meeting_id = record_id(meeting, "meeting_id", "meetingId", "id")
            meeting_code = record_id(meeting, "meeting_code", "meetingCode")
            if not meeting_id and not meeting_code:
                continue
            args = {"page_size": page_size(config)}
            if meeting_id:
                args["meeting_id"] = meeting_id
            elif meeting_code:
                args["meeting_code"] = meeting_code
            try:
                for record in paged_tool("get_records_list", args, {"record_file_id", "recordFileId", "meeting_record_id", "meetingRecordId"}, limit=10):
                    merged = dict(record)
                    merged.update({k: v for k, v in meeting.items() if k not in merged})
                    records.append(merged)
            except Exception as exc:
                message = f"get_records_list for meeting {meeting_id or meeting_code} failed: {exc}"
                errors.append(message)
                if is_quota_error(message):
                    stop_scanning = True
                    break
        if stop_scanning:
            break
        if len(records) >= source_record_limit:
            break

    records = merge_records_by_meeting_occurrence(expand_record_file_variants(records))
    return records[:record_limit], errors

def explicit_records(source, config):
    records = []
    for item in source.get("items") or []:
        if isinstance(item, dict):
            metadata = item.get("metadata") or {}
            merged = dict(metadata) if isinstance(metadata, dict) else {}
            merged.update(item)
            records.append(merged)
    direct = {
        "record_file_id": first_text(config, "recordFileId", "record_file_id"),
        "meeting_record_id": first_text(config, "meetingRecordId", "meeting_record_id"),
        "meeting_id": first_text(config, "meetingId", "meeting_id"),
        "meeting_code": first_text(config, "meetingCode", "meeting_code"),
        "subject": first_text(config, "topic", "subject", "name"),
    }
    if any(direct.values()):
        records.append(direct)
    return records


def scan_windows(config, previous):
    end = beijing_now()
    if first_text(config, "startTime", "start_time") and first_text(config, "endTime", "end_time"):
        return split_windows(parse_dt(first_text(config, "startTime", "start_time")), parse_dt(first_text(config, "endTime", "end_time")), scan_window_days(config))
    if previous.get("scanUntil"):
        overlap = max(0, int_value(config.get("incrementalOverlapDays"), DEFAULT_INCREMENTAL_OVERLAP_DAYS))
        start = parse_dt(previous.get("scanUntil")) - dt.timedelta(days=overlap)
    else:
        history_days = min(365, max(1, int_value(config.get("historyLookbackDays") or config.get("lookbackDays"), DEFAULT_HISTORY_DAYS)))
        start = end - dt.timedelta(days=history_days)
    return split_windows(start, end, scan_window_days(config))


def scan_window_days(config):
    return min(MAX_WINDOW_DAYS, max(1, int_value(config.get("windowDays"), DEFAULT_WINDOW_DAYS)))


def page_size(config):
    return min(50, max(1, int_value(config.get("pageSize"), DEFAULT_PAGE_SIZE)))


def max_records(config):
    return min(MAX_RECORDS, max(1, int_value(config.get("maxRecords"), DEFAULT_MAX_RECORDS)))


def content_preview_chars(config):
    return min(50000, max(2000, int_value(config.get("contentPreviewChars"), DEFAULT_CONTENT_PREVIEW_CHARS)))


def ended_meetings_fallback_recent_days(config):
    return min(365, max(0, int_value(config.get("endedMeetingsFallbackRecentDays"), DEFAULT_ENDED_MEETINGS_FALLBACK_RECENT_DAYS)))


def is_recent_ended_meetings_fallback_window(window, config):
    recent_days = ended_meetings_fallback_recent_days(config)
    if recent_days <= 0:
        return False
    window_end = parse_dt(window.get("end"))
    cutoff = beijing_now() - dt.timedelta(days=recent_days)
    return window_end >= cutoff


def split_windows(start, end, window_days=None):
    if end <= start:
        return []
    days = min(MAX_WINDOW_DAYS, max(1, int_value(window_days, DEFAULT_WINDOW_DAYS)))
    windows = []
    current = start
    while current < end:
        window_end = min(current + dt.timedelta(days=days), end)
        windows.append({"start": to_beijing_iso(current), "end": to_beijing_iso(window_end)})
        current = window_end
    return list(reversed(windows))


def paged_tool(tool_name, args, required_keys, limit=None):
    results = []
    page_args = dict(args)
    seen_tokens = set()
    for _ in range(80):
        data = call_tencent_tool(tool_name, page_args)
        if isinstance(data, str):
            raise RuntimeError(f"{tool_name} returned non-json text: {trim(data, 500)}")
        results.extend(find_dicts(data, required_keys))
        if limit and len(results) >= limit:
            return results[:limit]
        has_more = bool(find_first_key(data, ["has_more", "hasMore"]))
        next_token = find_first_key(data, ["next_page_token", "nextPageToken"])
        if not has_more or not next_token or next_token in seen_tokens:
            break
        seen_tokens.add(next_token)
        page_args["page_token"] = next_token
    return results


def materialize_merged_records(group_record, variants):
    materials = [materialize_record(variant) for variant in variants if isinstance(variant, dict)]
    if not materials:
        single = dict(group_record)
        single.pop("_mergedRecords", None)
        return materialize_record(single)

    readable = [item for item in materials if item.get("smartMinutes") or item.get("transcript")]
    primary = readable[0] if readable else materials[0]
    record_file_ids = unique([item.get("recordFileId") for item in materials])
    meeting_record_ids = unique([item.get("meetingRecordId") for item in materials])
    meeting_ids = unique([item.get("meetingId") for item in materials])
    meeting_codes = unique([item.get("meetingCode") for item in materials])
    title = best_meeting_title([group_record] + variants) or primary.get("title") or "\u817e\u8baf\u4f1a\u8bae"
    smart_minutes = "\n\n".join(unique([item.get("smartMinutes") for item in materials if item.get("smartMinutes")]))
    transcript = "\n\n".join(unique([item.get("transcript") for item in materials if item.get("transcript")]))
    errors = unique(sum([item.get("errors") or [] for item in materials], []))

    raw = {
        "mergedRecordCount": len(variants),
        "mergedSourceRecordKeys": group_record.get("_mergedSourceRecordKeys") or [],
        "records": variants,
    }
    return {
        "recordKey": str(group_record.get("_meetingOccurrenceKey") or primary.get("recordKey")),
        "title": title,
        "meetingId": meeting_ids[0] if meeting_ids else "",
        "meetingCode": meeting_codes[0] if meeting_codes else "",
        "recordFileId": record_file_ids[0] if record_file_ids else "",
        "recordFileIds": record_file_ids,
        "meetingRecordId": meeting_record_ids[0] if meeting_record_ids else "",
        "meetingRecordIds": meeting_record_ids,
        "meetingDate": meeting_date(group_record) or primary.get("meetingDate") or "",
        "smartMinutes": smart_minutes,
        "transcript": transcript,
        "raw": raw,
        "errors": errors,
        "mergedRecordCount": len(variants),
    }


def materialize_record(record):
    record = dict(record or {})
    variants = record.get("_mergedRecords")
    if isinstance(variants, list) and variants:
        return materialize_merged_records(record, variants)

    meeting_id = record_id(record, "meeting_id", "meetingId", "id")
    meeting_code = record_id(record, "meeting_code", "meetingCode")
    record_file_id = record_id(record, "record_file_id", "recordFileId", "record_fileid", "file_id")
    meeting_record_id = record_id(record, "meeting_record_id", "meetingRecordId", "meeting_recordid")
    record_file = first_record_file(record)
    if not record_file_id and record_file:
        record_file_id = record_id(record_file, "record_file_id", "recordFileId", "record_fileid", "file_id")
    title = first_text(record, "subject", "topic", "meeting_name", "meetingName", "title") or meeting_id or meeting_code or record_file_id or "腾讯会议"
    errors = []

    if not record_file_id and (meeting_id or meeting_code):
        args = {"meeting_id": meeting_id} if meeting_id else {"meeting_code": meeting_code}
        try:
            records = paged_tool("get_records_list", args, {"record_file_id", "recordFileId", "meeting_record_id", "meetingRecordId"})
            if records:
                record.update(records[0])
                record_file_id = record_id(record, "record_file_id", "recordFileId", "record_fileid", "file_id")
                meeting_record_id = record_id(record, "meeting_record_id", "meetingRecordId", "meeting_recordid")
        except Exception as exc:
            errors.append(f"录制列表获取失败：{exc}")

    smart_minutes = first_text(record, "smart_minutes", "smartMinutes", "ai_summary", "summary", "minutes")
    transcript = first_text(record, "transcript", "transcript_text", "content", "text")
    if record_file_id:
        if not smart_minutes:
            try:
                data = call_tencent_tool("get_smart_minutes", {"record_file_id": record_file_id})
                smart_minutes = text_from_any(data, ["text", "content", "summary", "minutes", "smart_minutes"])
            except Exception as exc:
                errors.append(f"智能纪要读取失败：{exc}")
        if not transcript:
            try:
                data = call_tencent_tool("get_transcripts_details", {"record_file_id": record_file_id, "pid": "0"})
                transcript = text_from_any(data, ["text", "content", "paragraph", "transcript", "sentence"])
            except Exception as exc:
                errors.append(f"转写详情读取失败：{exc}")

    if record_file_id and not transcript:
        transcript = transcript_from_paragraphs(record_file_id, errors)

    record_key = record_file_id or meeting_record_id or meeting_id or meeting_code or sha256_text(json.dumps(record, ensure_ascii=False, sort_keys=True))[:16]
    return {
        "recordKey": str(record_key),
        "title": title,
        "meetingId": meeting_id,
        "meetingCode": meeting_code,
        "recordFileId": record_file_id,
        "meetingRecordId": meeting_record_id,
        "meetingDate": meeting_date(record),
        "smartMinutes": smart_minutes or "",
        "transcript": transcript or "",
        "raw": record,
        "errors": errors,
    }


def transcript_from_paragraphs(record_file_id, errors):
    try:
        paragraphs = call_tencent_tool("get_transcripts_paragraphs", {"record_file_id": record_file_id})
    except Exception as exc:
        errors.append(f"get_transcripts_paragraphs failed: {exc}")
        return ""

    transcript = text_from_any(paragraphs, ["text", "content", "paragraph", "transcript", "sentence", "words", "word"])
    paragraph_ids = unique([str(item).strip() for item in find_values(paragraphs, {"pid", "paragraph_id", "paragraphId"}) if str(item).strip()])
    if not paragraph_ids:
        return transcript

    details = []
    for pid in paragraph_ids[:50]:
        try:
            data = call_tencent_tool("get_transcripts_details", {"record_file_id": record_file_id, "pid": pid})
            text = text_from_any(data, ["text", "content", "paragraph", "transcript", "sentence", "words", "word"])
            if text:
                details.append(text)
        except Exception as exc:
            errors.append(f"get_transcripts_details pid={pid} failed: {exc}")
            break
    return "\n\n".join(unique(details)) or transcript


def archive_meeting_source(client, source_id, material, content_hash):
    path = "source_files/tencent_meeting/{}/{}-{}-{}.md".format(source_id, material["meetingDate"], slugify(material["title"]), content_hash[:12])
    client.upsert_text(path, render_source_file(material, content_hash), f"Archive Tencent Meeting source {path}")
    return path


def render_source_file(material, content_hash):
    metadata = {
        "sourceType": "tencent_meeting",
        "title": material["title"],
        "meetingId": material["meetingId"],
        "meetingCode": material["meetingCode"],
        "recordFileId": material["recordFileId"],
        "recordFileIds": material.get("recordFileIds") or ([material["recordFileId"]] if material["recordFileId"] else []),
        "meetingRecordId": material["meetingRecordId"],
        "meetingRecordIds": material.get("meetingRecordIds") or ([material["meetingRecordId"]] if material["meetingRecordId"] else []),
        "meetingDate": material["meetingDate"],
        "mergedRecordCount": material.get("mergedRecordCount", 1),
        "contentHash": content_hash,
        "archivedAt": now(),
        "errors": material["errors"],
    }
    return "\n".join([
        f"# 腾讯会议源材料：{material['title']}",
        "",
        "## 元数据",
        "",
        "```json",
        json.dumps(metadata, ensure_ascii=False, indent=2),
        "```",
        "",
        "## AI 智能纪要",
        "",
        material["smartMinutes"] or "未获取到智能纪要。",
        "",
        "## 转写全文",
        "",
        material["transcript"] or "未获取到转写全文。",
        "",
        "## 原始记录",
        "",
        "```json",
        json.dumps(material["raw"], ensure_ascii=False, indent=2),
        "```",
        "",
    ])


def source_item(source_id, material, archived_path, content_hash, config=None):
    preview_limit = content_preview_chars(config or {})
    preview = "\n\n".join([
        "# " + material["title"],
        "## AI 智能纪要\n" + (material["smartMinutes"] or "未获取到智能纪要。"),
        "## 转写全文\n" + (material["transcript"] or "未获取到转写全文。"),
    ])
    return {
        "sourceId": source_id,
        "itemKey": material["recordKey"],
        "title": material["title"],
        "kind": "tencent_meeting",
        "platform": "tencent_meeting",
        "meetingId": material["meetingId"],
        "meetingCode": material["meetingCode"],
        "recordFileId": material["recordFileId"],
        "recordFileIds": material.get("recordFileIds") or ([material["recordFileId"]] if material["recordFileId"] else []),
        "meetingRecordId": material["meetingRecordId"],
        "meetingRecordIds": material.get("meetingRecordIds") or ([material["meetingRecordId"]] if material["meetingRecordId"] else []),
        "meetingDate": material["meetingDate"],
        "mergedRecordCount": material.get("mergedRecordCount", 1),
        "archivedPath": archived_path,
        "sha256": content_hash,
        "readable": True,
        "contentPreview": trim(preview, preview_limit),
        "contentPreviewChars": min(len(preview), preview_limit),
        "contentPreviewTruncated": len(preview) > preview_limit,
        "smartMinutesChars": len(material["smartMinutes"] or ""),
        "transcriptChars": len(material["transcript"] or ""),
        "metadata": {
            "errors": material["errors"],
            "sourceRecord": compact_record_trace(material["raw"]),
        },
    }


def load_cached_prepare_context(payload):
    if int_value(payload.get("attemptNo"), 1) <= 1:
        return None
    cache_file = prepare_cache_file(payload)
    try:
        cached = read_json_file(cache_file)
    except Exception:
        return None
    if not isinstance(cached, dict):
        return None
    if cached.get("version") != PREPARE_CACHE_VERSION or cached.get("fingerprint") != prepare_cache_fingerprint(payload):
        return None
    context = cached.get("context")
    if not isinstance(context, dict) or context.get("mode") != "ingest" or not context.get("inputItems"):
        return None
    context = dict(context)
    context["pageOutput"] = initialize_page_output(payload)
    context["prepareCache"] = {
        "reused": True,
        "version": PREPARE_CACHE_VERSION,
        "cachedAt": cached.get("cachedAt") or "",
    }
    return context


def save_prepare_context_cache(payload, context):
    if not isinstance(context, dict) or context.get("mode") != "ingest" or not context.get("inputItems"):
        return
    cached_context = dict(context)
    cached_context.pop("prepareCache", None)
    write_json_file(prepare_cache_file(payload), {
        "version": PREPARE_CACHE_VERSION,
        "fingerprint": prepare_cache_fingerprint(payload),
        "cachedAt": now(),
        "context": cached_context,
    })


def delete_prepare_context_cache(payload):
    try:
        prepare_cache_file(payload).unlink(missing_ok=True)
    except Exception:
        pass


def prepare_cache_file(payload):
    shared_value = payload.get("sharedDir") or os.getenv("OPENCLAW_SHARED_DIR") or str(Path(tempfile.gettempdir()) / "research-kb")
    shared_root = Path(shared_value).expanduser().resolve()
    task_id = safe_run_component(payload.get("taskId") or "adhoc")
    cache_root = (shared_root / "work" / "tencent_meeting_ingest" / "_prepare_cache").resolve()
    try:
        cache_root.relative_to(shared_root)
    except ValueError as exc:
        raise ValueError("Tencent Meeting prepare cache escapes sharedDir") from exc
    cache_root.mkdir(parents=True, exist_ok=True)
    prune_prepare_cache(cache_root)
    return cache_root / f"{task_id}.json"


def prune_prepare_cache(cache_root, max_age_days=7):
    cutoff = time.time() - max_age_days * 86400
    for path in cache_root.glob("*.json"):
        try:
            if path.is_file() and path.stat().st_mtime < cutoff:
                path.unlink()
        except OSError:
            continue


def prepare_cache_fingerprint(payload):
    source = payload.get("source") or {}
    value = {
        "version": PREPARE_CACHE_VERSION,
        "taskId": payload.get("taskId"),
        "sourceId": source.get("id") or payload.get("sourceId"),
        "sourceType": source.get("type") or "tencent_meeting",
        "config": source.get("config") or {},
        "lastSnapshot": source.get("lastSnapshot") or {},
        "items": source.get("items") or [],
    }
    return sha256_text(json.dumps(value, ensure_ascii=False, sort_keys=True, default=str))


def meeting_page_instructions():
    return {
        "requiredEntityRoot": "meetings/",
        "requiredSections": ["会议信息", "议程与背景", "关键讨论", "决议", "行动项", "风险与阻塞", "开放问题", "关联页面", "来源与证据索引"],
        "allowedRelatedRoots": ["projects/", "papers/", "surveys/", "code/", "experiments/", "tech-notes/", "notes/", "concepts/", "resources/", "overview/"],
        "rules": [
            "每个 inputItems[] 必须至少生成或更新一个 meetings/ 实体页。",
            "不要把没有证据的负责人、日期或决议写成事实；缺失时写“来源未提及”。",
            "写 Markdown 草稿和页面 manifest 前先私下做一次图谱规划：会议实体页优先，然后判断是否需要更新 overview/、projects/、concepts/、resources/ 或其他相关页面。",
            "如果会议内容明确影响项目路线、研究主题、资源选择、实验设计或团队导航页，应额外更新相关页面；证据不足时不要硬建页面。",
            "用 relatedConcepts、relatedResources、relatedCodePages 和 relatedPages 维护 catalog 关系；relatedPages 用于 overview/、projects/、papers/、surveys/、meetings/、experiments/、tech-notes/、notes/ 等普通 Wiki 页面。",
            "正文中写解释性的 KB 根路径 wikilink；Python 会从链接推导 relatedConcepts、relatedResources、relatedCodePages 和 relatedPages。",
            "不要写 qa/ 页面；问答沉淀由 kb_query 负责。",
        ],
    }


def initialize_page_output(payload):
    return page_output_contract(payload, reset=True)


def expected_page_output(payload):
    return page_output_contract(payload, reset=False)


def page_output_contract(payload, reset=False):
    shared_value = payload.get("sharedDir") or os.getenv("OPENCLAW_SHARED_DIR") or str(Path(tempfile.gettempdir()) / "research-kb")
    shared_root = Path(shared_value).expanduser().resolve()
    task_id = safe_run_component(payload.get("taskRunId") or payload.get("taskId") or "adhoc")
    attempt = safe_run_component(payload.get("attemptNo") or "1")
    work_root = (shared_root / "work" / "tencent_meeting_ingest" / f"{task_id}-attempt-{attempt}").resolve()
    try:
        work_root.relative_to(shared_root)
    except ValueError as exc:
        raise ValueError("Tencent Meeting page work directory escapes sharedDir") from exc
    if reset and work_root.exists():
        shutil.rmtree(work_root)
    draft_dir = work_root / "drafts"
    if reset:
        draft_dir.mkdir(parents=True, exist_ok=True)
    return {
        "protocol": "research-kb-markdown-drafts/v1",
        "draftDir": str(draft_dir),
        "manifestPath": str(work_root / "pages-manifest.json"),
        "draftPathRule": "draftFile 使用 KB 根目录相对路径且同时作为最终页面路径，例如 meetings/2026-07-11-project-sync.md。",
        "manifestRule": "manifest 只保存短元数据，不嵌入 Markdown 正文；每项至少包含 draftFile 和 sourceItemKeys。",
    }


def safe_run_component(value):
    text = re.sub(r"[^A-Za-z0-9_.-]+", "-", str(value or "")).strip(".-")
    return text[:80] or "adhoc"


def compact_record_trace(raw):
    if not isinstance(raw, dict):
        return {}
    allowed = {
        "meeting_id", "meetingId", "meeting_code", "meetingCode", "record_file_id", "recordFileId",
        "meeting_record_id", "meetingRecordId", "subject", "topic", "title", "state", "record_type",
        "start_time", "startTime", "end_time", "endTime", "media_start_time", "mediaStartTime",
        "record_start_time", "recordStartTime", "record_end_time", "recordEndTime", "mergedRecordCount",
        "mergedSourceRecordKeys",
    }
    result = {key: value for key, value in raw.items() if key in allowed and scalar_trace_value(value)}
    record_files = raw.get("record_files") or raw.get("recordFiles")
    if isinstance(record_files, list):
        result["recordFiles"] = [compact_record_trace(item) for item in record_files[:20] if isinstance(item, dict)]
    records = raw.get("records")
    if isinstance(records, list):
        result["records"] = [compact_record_trace(item) for item in records[:30] if isinstance(item, dict)]
    return result


def scalar_trace_value(value):
    return isinstance(value, (str, int, float, bool)) or value is None


def material_content_hash(material):
    return sha256_text(json.dumps({
        "title": material["title"],
        "meetingId": material["meetingId"],
        "meetingCode": material["meetingCode"],
        "recordFileId": material["recordFileId"],
        "recordFileIds": material.get("recordFileIds") or ([material["recordFileId"]] if material["recordFileId"] else []),
        "meetingRecordId": material["meetingRecordId"],
        "meetingRecordIds": material.get("meetingRecordIds") or ([material["meetingRecordId"]] if material["meetingRecordId"] else []),
        "mergedRecordCount": material.get("mergedRecordCount", 1),
        "smartMinutes": material["smartMinutes"],
        "transcript": material["transcript"],
    }, ensure_ascii=False, sort_keys=True))


def expand_record_file_variants(records):
    expanded = []
    for record in records or []:
        if not isinstance(record, dict):
            continue
        files = record.get("record_files") or record.get("recordFiles") or []
        if not isinstance(files, list) or not files:
            expanded.append(record)
            continue
        valid_files = [item for item in files if isinstance(item, dict)]
        if not valid_files:
            expanded.append(record)
            continue
        for record_file in valid_files:
            variant = dict(record)
            variant.pop("recordFiles", None)
            variant["record_files"] = [record_file]
            record_file_id = record_id(record_file, "record_file_id", "recordFileId", "record_fileid", "file_id")
            if record_file_id:
                variant["record_file_id"] = record_file_id
            expanded.append(variant)
    return expanded


def merge_records_by_meeting_occurrence(records):
    groups = []
    seen_source_records = set()
    for record in records:
        if not isinstance(record, dict):
            continue
        source_key = source_record_key(record)
        if source_key in seen_source_records:
            continue
        seen_source_records.add(source_key)
        signature = meeting_occurrence_signature(record)
        group = matching_occurrence_group(groups, signature)
        if group is None:
            group = {"signature": signature, "records": [], "sourceKeys": []}
            groups.append(group)
        group["records"].append(record)
        group["sourceKeys"].append(source_key)
        group["signature"] = extend_occurrence_signature(group["signature"], signature)

    merged = []
    for group in groups:
        records = group["records"]
        if len(records) == 1:
            merged.append(records[0])
            continue
        base = dict(best_group_base(records))
        base["_mergedRecords"] = records
        base["_meetingOccurrenceKey"] = meeting_occurrence_key(group["signature"], records)
        base["_mergedSourceRecordKeys"] = unique(group["sourceKeys"])
        merged.append(base)
    return merged


def source_record_key(record):
    record_file = first_record_file(record)
    value = (
        record_id(record, "record_file_id", "recordFileId", "record_fileid", "file_id")
        or record_id(record_file, "record_file_id", "recordFileId", "record_fileid", "file_id")
        or record_id(record, "meeting_record_id", "meetingRecordId", "meeting_recordid")
    )
    if value:
        return "record:" + value
    signature = meeting_occurrence_signature(record)
    occurrence = meeting_occurrence_key(signature, [record])
    return "occurrence:" + occurrence if occurrence else "raw:" + sha256_text(json.dumps(record, ensure_ascii=False, sort_keys=True))


def meeting_occurrence_signature(record):
    start, end = record_interval(record)
    title = normalize_meeting_title(record_title(record))
    identity = record_id(record, "meeting_id", "meetingId", "id") or record_id(record, "meeting_code", "meetingCode")
    date = start.date().isoformat() if start else meeting_date(record)
    start_minute = minutes_from_occurrence_day(start, date) if start else None
    end_minute = minutes_from_occurrence_day(end, date) if end else start_minute
    return {"identity": identity, "date": date, "startMinute": start_minute, "endMinute": end_minute, "title": title}


def matching_occurrence_group(groups, signature):
    if not signature.get("identity") or signature.get("startMinute") is None:
        return None
    for group in groups:
        current = group["signature"]
        if current.get("identity") != signature.get("identity"):
            continue
        if current.get("date") != signature.get("date"):
            continue
        if current.get("title") and signature.get("title") and current.get("title") != signature.get("title"):
            continue
        if intervals_touch(current, signature):
            return group
    return None


def intervals_touch(left, right):
    left_start = left.get("startMinute")
    right_start = right.get("startMinute")
    if left_start is None or right_start is None:
        return False
    left_end = left.get("endMinute") if left.get("endMinute") is not None else left_start
    right_end = right.get("endMinute") if right.get("endMinute") is not None else right_start
    tolerance = MEETING_OCCURRENCE_MERGE_TOLERANCE_MINUTES
    return left_start <= right_end + tolerance and right_start <= left_end + tolerance


def extend_occurrence_signature(current, incoming):
    result = dict(current or {})
    for key in ("identity", "date", "title"):
        if not result.get(key) and incoming.get(key):
            result[key] = incoming.get(key)
    starts = [value for value in [result.get("startMinute"), incoming.get("startMinute")] if value is not None]
    ends = [value for value in [result.get("endMinute"), incoming.get("endMinute")] if value is not None]
    if starts:
        result["startMinute"] = min(starts)
    if ends:
        result["endMinute"] = max(ends)
    return result


def meeting_occurrence_key(signature, records):
    identity = signature.get("identity") or "meeting"
    date = signature.get("date") or "unknown-date"
    minute = signature.get("startMinute")
    if minute is None:
        return ""
    return "{}:{}:{:04d}:{}".format(identity, date, minute, signature.get("title") or best_meeting_title(records))


def best_group_base(records):
    return sorted(records, key=record_quality_score, reverse=True)[0]


def record_quality_score(record):
    title = record_title(record)
    normalized = normalize_meeting_title(title)
    score = 0
    if title and title == normalized:
        score += 4
    if record_id(record, "record_file_id", "recordFileId", "record_fileid", "file_id") or record_id(first_record_file(record), "record_file_id", "recordFileId", "record_fileid", "file_id"):
        score += 2
    if first_text(record, "smart_minutes", "smartMinutes", "ai_summary", "summary", "minutes"):
        score += 2
    if first_text(record, "transcript", "transcript_text", "content", "text"):
        score += 2
    return (score, len(normalized), normalized)


def best_meeting_title(records):
    titles = unique([record_title(record) for record in records if isinstance(record, dict)])
    if not titles:
        return ""
    return sorted(titles, key=lambda title: (title == normalize_meeting_title(title), len(normalize_meeting_title(title))), reverse=True)[0]


def record_title(record):
    return first_text(record, "subject", "topic", "meeting_name", "meetingName", "title")


def normalize_meeting_title(title):
    text = str(title or "").strip()
    text = re.sub("^(\\u8f6c\\u5199|\\u6587\\u5b57\\u8f6c\\u5199|\\u5f55\\u5236|\\u4e91\\u5f55\\u5236)[_\\uff1a:\\s-]+", "", text).strip()
    return text or str(title or "").strip()


def minutes_from_occurrence_day(value, date_text):
    if not value or not date_text:
        return None
    try:
        base_date = dt.date.fromisoformat(str(date_text)[:10])
        base = dt.datetime.combine(base_date, dt.time.min, tzinfo=value.tzinfo)
        return int((value - base).total_seconds() // 60)
    except Exception:
        return value.hour * 60 + value.minute


def record_start_dt(record):
    start, _ = record_interval(record)
    return start


def record_interval(record):
    record_file = first_record_file(record)
    start = first_dt(
        first_text(record, "record_start_time", "recordStartTime"),
        first_text(record_file, "record_start_time", "recordStartTime"),
        first_text(record, "media_start_time", "mediaStartTime"),
        first_text(record, "start_time", "startTime", "meeting_start_time", "meetingStartTime", "scheduled_time", "scheduledTime"),
    )
    end = first_dt(
        first_text(record, "record_end_time", "recordEndTime"),
        first_text(record_file, "record_end_time", "recordEndTime"),
        first_text(record, "media_end_time", "mediaEndTime"),
        first_text(record, "end_time", "endTime", "meeting_end_time", "meetingEndTime"),
    )
    if start and end and end < start:
        end = start
    return start, end


def first_dt(*values):
    for value in values:
        if not value:
            continue
        try:
            return parse_dt(value).astimezone(dt.timezone(dt.timedelta(hours=8)))
        except Exception:
            continue
    return None


def find_dicts(value, required_keys):
    found = []
    if isinstance(value, dict):
        if any(key in value for key in required_keys):
            found.append(value)
            return found
        for child in value.values():
            found.extend(find_dicts(child, required_keys))
    elif isinstance(value, list):
        for child in value:
            found.extend(find_dicts(child, required_keys))
    return found


def find_values(value, keys):
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in keys and child not in (None, "", []):
                found.append(child)
            found.extend(find_values(child, keys))
    elif isinstance(value, list):
        for child in value:
            found.extend(find_values(child, keys))
    return found


def meeting_date(record):
    raw = first_text(record, "start_time", "startTime", "media_start_time", "mediaStartTime", "meeting_start_time", "meetingStartTime", "record_start_time", "recordStartTime", "scheduled_time", "scheduledTime", "end_time", "endTime")
    if raw and len(raw) >= 10:
        return raw[:10]
    return dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).date().isoformat()

def first_record_file(record):
    files = record.get("record_files") or record.get("recordFiles") if isinstance(record, dict) else []
    if isinstance(files, list):
        for item in files:
            if isinstance(item, dict):
                return item
    return {}

def record_id(record, *keys):
    for key in keys:
        value = record.get(key) if isinstance(record, dict) else None
        if value not in (None, "", []):
            return str(value)
    return ""


def first_text(mapping, *keys):
    if not isinstance(mapping, dict):
        return ""
    for key in keys:
        value = mapping.get(key)
        if value not in (None, "", []):
            return str(value).strip()
    return ""

def bool_value(value, fallback=False):
    if value in (None, ""):
        return fallback
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def is_quota_error(message):
    text = str(message or "").lower()
    return "500246" in text or "quota" in text or "usage limit" in text

def int_value(value, fallback):
    try:
        if value in (None, ""):
            return fallback
        return int(value)
    except Exception:
        return fallback


def trim(text, max_chars):
    text = str(text or "")
    return text[:max_chars] + ("\n..." if len(text) > max_chars else "")


def beijing_now():
    return dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).replace(microsecond=0)


def parse_dt(value):
    if isinstance(value, dt.datetime):
        return value
    text = str(value or "").strip()
    if not text:
        return beijing_now()
    return dt.datetime.fromisoformat(text.replace("Z", "+00:00"))


def to_beijing_iso(value):
    if value.tzinfo is None:
        value = value.replace(tzinfo=dt.timezone(dt.timedelta(hours=8)))
    return value.astimezone(dt.timezone(dt.timedelta(hours=8))).replace(microsecond=0).isoformat()


def safe_context_config(config):
    sensitive = ("token", "secret", "password", "credential", "api_key", "apikey")

    def clean(value):
        if isinstance(value, dict):
            return {
                key: clean(child)
                for key, child in value.items()
                if not any(marker in str(key).lower() for marker in sensitive)
            }
        if isinstance(value, list):
            return [clean(child) for child in value]
        return value

    return clean(dict(config or {}))
