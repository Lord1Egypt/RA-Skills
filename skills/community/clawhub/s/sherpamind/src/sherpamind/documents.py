from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from .db import connect, now_iso, replace_ticket_document_chunks, replace_ticket_documents
from .text_cleanup import normalize_ticket_text, summarize_resolution_from_logs


DOCUMENT_MATERIALIZATION_VERSION = 15


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _split_csv_values(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(',') if part and part.strip()]


def _first_present(*values: str | None) -> str | None:
    for value in values:
        if value is None:
            continue
        cleaned = str(value).strip()
        if cleaned:
            return cleaned
    return None


def _looks_like_identifier(value: str | None) -> bool:
    if value is None:
        return False
    candidate = value.strip()
    return bool(candidate) and candidate.isdigit()


def _join_name_parts(*parts: str | None) -> str | None:
    joined = " ".join(part.strip() for part in parts if part and part.strip())
    return joined or None


def _extract_email_domain(value: Any) -> str | None:
    if value is None:
        return None
    candidate = str(value).strip().lower()
    if not candidate or "@" not in candidate:
        return None
    domain = candidate.rsplit("@", 1)[-1].strip(" >).,;:'\"")
    if not domain or "." not in domain:
        return None
    return domain


def _collect_email_domains(*values: Any) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if isinstance(value, (list, tuple, set)):
            for item in value:
                domain = _extract_email_domain(item)
                if domain and domain not in seen:
                    seen.add(domain)
                    ordered.append(domain)
            continue
        domain = _extract_email_domain(value)
        if domain and domain not in seen:
            seen.add(domain)
            ordered.append(domain)
    return ordered


def _coerce_bool(value: Any) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    candidate = str(value).strip().lower()
    if candidate in {"1", "true", "yes", "y", "on"}:
        return True
    if candidate in {"0", "false", "no", "n", "off", ""}:
        return False
    return bool(candidate)


def _present_metric(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    candidate = str(value).strip()
    return bool(candidate) and candidate not in {"0", "0.0", "0.00"}


_RESPONSE_LOG_TYPES = {"response", "initial post", "initial log", "log entry"}
_RESOLUTION_LOG_TYPES = {"closed", "close log"}


def _normalize_log_type(value: Any) -> str:
    return str(value or "").strip().lower()


def _coerce_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    candidate = str(value).strip()
    if not candidate:
        return None
    try:
        return int(candidate)
    except ValueError:
        try:
            return int(float(candidate))
        except ValueError:
            return None


def _resolve_account_label(record: dict) -> tuple[str | None, str]:
    joined_name = _first_present(record.get("account"))
    raw_name = _first_present(record.get("raw_account_name"), record.get("raw_account_location_name"))
    account_id = _first_present(record.get("account_id"))
    if joined_name and not _looks_like_identifier(joined_name):
        return joined_name, "joined"
    if raw_name:
        return raw_name, "raw"
    if joined_name:
        return joined_name, "joined"
    if account_id:
        return account_id, "id"
    return None, "missing"


def _resolve_user_label(record: dict) -> tuple[str | None, str]:
    joined_name = _first_present(record.get("user_name"))
    raw_name = _first_present(
        record.get("raw_user_name"),
        _join_name_parts(record.get("raw_user_firstname"), record.get("raw_user_lastname")),
        record.get("raw_user_fullname"),
    )
    user_email = _first_present(record.get("user_email"), record.get("raw_user_email"))
    user_id = _first_present(record.get("user_id"))
    if joined_name and not _looks_like_identifier(joined_name):
        return joined_name, "joined"
    if raw_name:
        return raw_name, "raw"
    if user_email:
        return user_email, "email"
    if joined_name:
        return joined_name, "joined"
    if user_id:
        return user_id, "id"
    return None, "missing"


def _resolve_technician_label(record: dict) -> tuple[str | None, str]:
    joined_name = _first_present(record.get("technician"))
    raw_name = _first_present(
        record.get("raw_assigned_technician_name"),
        record.get("raw_technician_name"),
        record.get("raw_tech_name"),
        _join_name_parts(record.get("raw_technician_firstname"), record.get("raw_technician_lastname")),
    )
    technician_id = _first_present(record.get("assigned_technician_id"))
    if joined_name and not _looks_like_identifier(joined_name):
        return joined_name, "joined"
    if raw_name:
        return raw_name, "raw"
    if joined_name:
        return joined_name, "joined"
    if technician_id:
        return technician_id, "id"
    return None, "missing"


def _resolve_department_label(record: dict) -> tuple[str | None, str]:
    support_group_name = _first_present(record.get("support_group_name"))
    class_name = _first_present(record.get("class_name"))
    submission_category = _first_present(record.get("submission_category"))
    department_key = _first_present(record.get("department_key"))
    if support_group_name:
        return support_group_name, "support_group_name"
    if class_name:
        return class_name, "class_name"
    if submission_category:
        return submission_category, "submission_category"
    if department_key and not _looks_like_identifier(department_key):
        return department_key, "department_key"
    return None, "missing"


_ATTACHMENT_KIND_BY_EXTENSION: dict[str, str] = {
    "png": "image",
    "jpg": "image",
    "jpeg": "image",
    "gif": "image",
    "webp": "image",
    "bmp": "image",
    "heic": "image",
    "tif": "image",
    "tiff": "image",
    "svg": "image",
    "pdf": "document",
    "doc": "document",
    "docx": "document",
    "txt": "document",
    "rtf": "document",
    "odt": "document",
    "csv": "spreadsheet",
    "xls": "spreadsheet",
    "xlsx": "spreadsheet",
    "ods": "spreadsheet",
    "tsv": "spreadsheet",
    "zip": "archive",
    "7z": "archive",
    "rar": "archive",
    "tar": "archive",
    "gz": "archive",
    "tgz": "archive",
    "bz2": "archive",
    "xz": "archive",
    "log": "log",
    "evt": "log",
    "evtx": "log",
    "json": "data",
    "xml": "data",
    "yaml": "data",
    "yml": "data",
    "sql": "data",
    "pcap": "data",
    "mp3": "audio",
    "wav": "audio",
    "m4a": "audio",
    "ogg": "audio",
    "mp4": "video",
    "mov": "video",
    "avi": "video",
    "mkv": "video",
    "wmv": "video",
    "eml": "message",
    "msg": "message",
}


def _attachment_extension(name: str | None) -> str | None:
    if not name:
        return None
    candidate = str(name).strip().rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    if "." not in candidate:
        return None
    extension = candidate.rsplit(".", 1)[-1].strip().lower()
    return extension or None


def _attachment_kind(name: str | None) -> str:
    extension = _attachment_extension(name)
    if not extension:
        return "unknown"
    return _ATTACHMENT_KIND_BY_EXTENSION.get(extension, "other")


def _summarize_attachment_metadata(rows: list[dict[str, Any]]) -> dict[str, Any]:
    names: list[str] = []
    extensions: list[str] = []
    kind_counts: dict[str, int] = {}
    kind_order: list[str] = []
    total_size_bytes = 0
    size_count = 0

    for row in rows:
        if not isinstance(row, dict):
            continue
        name = _first_present(row.get("name"))
        if name:
            names.append(name)
        extension = _attachment_extension(name)
        if extension:
            extensions.append(extension)
        kind = _attachment_kind(name)
        if kind not in kind_counts:
            kind_order.append(kind)
        kind_counts[kind] = kind_counts.get(kind, 0) + 1
        size = row.get("size")
        if isinstance(size, (int, float)):
            total_size_bytes += int(size)
            size_count += 1
        elif size not in (None, ""):
            try:
                total_size_bytes += int(str(size).strip())
                size_count += 1
            except ValueError:
                pass

    unique_extensions = sorted(set(extensions))
    attachment_kinds = sorted(kind_counts)
    return {
        "attachment_names": names,
        "attachment_extensions": unique_extensions,
        "attachment_extensions_csv": ", ".join(unique_extensions) if unique_extensions else None,
        "attachment_kinds": attachment_kinds,
        "attachment_kinds_csv": ", ".join(attachment_kinds) if attachment_kinds else None,
        "attachment_kind_counts": kind_counts,
        "attachment_kind_primary": (
            max(kind_order, key=lambda kind: (kind_counts.get(kind, 0), -kind_order.index(kind)))
            if kind_order else None
        ),
        "attachment_total_size_bytes": total_size_bytes if size_count else None,
        "attachment_size_known_count": size_count,
        "attachment_image_count": kind_counts.get("image", 0),
        "attachment_document_count": kind_counts.get("document", 0),
        "attachment_spreadsheet_count": kind_counts.get("spreadsheet", 0),
        "attachment_archive_count": kind_counts.get("archive", 0),
        "attachment_log_count": kind_counts.get("log", 0),
        "attachment_data_count": kind_counts.get("data", 0),
        "attachment_audio_count": kind_counts.get("audio", 0),
        "attachment_video_count": kind_counts.get("video", 0),
        "attachment_message_count": kind_counts.get("message", 0),
        "attachment_other_count": kind_counts.get("other", 0),
        "attachment_unknown_count": kind_counts.get("unknown", 0),
    }


def _split_text_hard(text: str, target_chars: int) -> list[str]:
    text = text.strip()
    if not text:
        return []
    words = text.split()
    if not words:
        return []
    chunks: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if len(candidate) <= target_chars:
            current = candidate
            continue
        chunks.append(current)
        current = word
    if current:
        chunks.append(current)
    return chunks


def _split_text_segment(text: str, target_chars: int) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if len(text) <= target_chars:
        return [text]

    sentence_candidates = [segment.strip() for segment in re.split(r"(?<=[.!?])\s+", text) if segment and segment.strip()]
    if len(sentence_candidates) <= 1:
        return _split_text_hard(text, target_chars)

    chunks: list[str] = []
    current = ""
    for sentence in sentence_candidates:
        if len(sentence) > target_chars:
            if current:
                chunks.append(current)
                current = ""
            chunks.extend(_split_text_hard(sentence, target_chars))
            continue
        candidate = sentence if not current else f"{current} {sentence}"
        if len(candidate) <= target_chars:
            current = candidate
            continue
        if current:
            chunks.append(current)
        current = sentence
    if current:
        chunks.append(current)
    return chunks


def _chunk_segment_length(segments: list[str]) -> int:
    if not segments:
        return 0
    return sum(len(segment) for segment in segments) + (len(segments) - 1)



def _rebalance_small_chunk_tail(
    chunk_segments: list[list[str]],
    *,
    target_chars: int,
    min_chunk_chars: int,
) -> list[list[str]]:
    if len(chunk_segments) < 2:
        return chunk_segments

    rebalanced = [list(segments) for segments in chunk_segments if segments]
    for idx in range(len(rebalanced) - 1, 0, -1):
        current = rebalanced[idx]
        previous = rebalanced[idx - 1]
        if not current or not previous:
            continue
        current_len = _chunk_segment_length(current)
        if current_len >= min_chunk_chars:
            continue

        while len(previous) > 1 and current_len < min_chunk_chars:
            candidate_segment = previous[-1]
            candidate_current = [candidate_segment, *current]
            candidate_previous = previous[:-1]
            candidate_current_len = _chunk_segment_length(candidate_current)
            candidate_previous_len = _chunk_segment_length(candidate_previous)
            if candidate_current_len > target_chars:
                break
            if candidate_previous and candidate_previous_len < min_chunk_chars:
                break
            current = candidate_current
            previous = candidate_previous
            current_len = candidate_current_len

        if current_len < min_chunk_chars and _chunk_segment_length(previous + current) <= target_chars:
            rebalanced[idx - 1] = previous + current
            rebalanced[idx] = []
            continue

        rebalanced[idx - 1] = previous
        rebalanced[idx] = current

    return [segments for segments in rebalanced if segments]



def _rebalance_small_chunk_heads(
    chunk_segments: list[list[str]],
    *,
    target_chars: int,
    min_chunk_chars: int,
) -> list[list[str]]:
    if len(chunk_segments) < 2:
        return chunk_segments

    rebalanced = [list(segments) for segments in chunk_segments if segments]
    for idx in range(len(rebalanced) - 1):
        current = rebalanced[idx]
        following = rebalanced[idx + 1]
        if not current or not following:
            continue
        current_len = _chunk_segment_length(current)
        if current_len >= min_chunk_chars:
            continue

        while len(following) > 1 and current_len < min_chunk_chars:
            candidate_segment = following[0]
            candidate_current = [*current, candidate_segment]
            candidate_following = following[1:]
            candidate_current_len = _chunk_segment_length(candidate_current)
            candidate_following_len = _chunk_segment_length(candidate_following)
            if candidate_current_len > target_chars:
                break
            if candidate_following and candidate_following_len < min_chunk_chars:
                break
            current = candidate_current
            following = candidate_following
            current_len = candidate_current_len

        if current_len < min_chunk_chars and _chunk_segment_length(current + following) <= target_chars:
            rebalanced[idx] = current + following
            rebalanced[idx + 1] = []
            continue

        rebalanced[idx] = current
        rebalanced[idx + 1] = following

    return [segments for segments in rebalanced if segments]



def _chunk_text(text: str, target_chars: int = 1800, min_chunk_chars: int = 250) -> list[str]:
    if len(text) <= target_chars:
        return [text]

    segments: list[str] = []
    for paragraph in text.split("\n"):
        cleaned = paragraph.strip()
        if not cleaned:
            continue
        segments.extend(_split_text_segment(cleaned, target_chars))

    chunk_segments: list[list[str]] = []
    current: list[str] = []
    current_len = 0
    for segment in segments:
        candidate_len = len(segment) if not current else current_len + 1 + len(segment)
        if current and candidate_len > target_chars:
            chunk_segments.append(current)
            current = [segment]
            current_len = len(segment)
            continue
        current.append(segment)
        current_len = candidate_len
    if current:
        chunk_segments.append(current)

    chunk_segments = _rebalance_small_chunk_heads(
        chunk_segments,
        target_chars=target_chars,
        min_chunk_chars=min_chunk_chars,
    )
    chunk_segments = _rebalance_small_chunk_tail(
        chunk_segments,
        target_chars=target_chars,
        min_chunk_chars=min_chunk_chars,
    )

    chunks: list[str] = []
    for segments_for_chunk in chunk_segments:
        chunk = "\n".join(segments_for_chunk).strip()
        if not chunk:
            continue
        if chunks and len(chunk) < min_chunk_chars and len(chunks[-1]) + 1 + len(chunk) <= target_chars:
            chunks[-1] = f"{chunks[-1]}\n{chunk}".strip()
            continue
        chunks.append(chunk)

    return chunks


def _parse_recent_logs(value: str | None) -> list[dict[str, Any]]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return []
    if not isinstance(parsed, list):
        return []
    rows: list[dict[str, Any]] = []
    for item in parsed:
        if isinstance(item, dict):
            rows.append(item)
    return rows


def _normalize_log_actor_label(log: dict[str, Any]) -> str | None:
    for value in (log.get("user_name"), log.get("user_email"), log.get("user_id")):
        if value is None:
            continue
        cleaned = str(value).strip()
        if cleaned:
            return cleaned
    return None


def _summarize_recent_log_participants(logs: list[dict[str, Any]]) -> dict[str, Any]:
    recent_public_actor_labels: list[str] = []
    recent_internal_actor_labels: list[str] = []
    seen_public: set[str] = set()
    seen_internal: set[str] = set()
    latest_public_actor_label: str | None = None
    latest_internal_actor_label: str | None = None
    recent_public_email_domains: list[str] = []
    recent_internal_email_domains: list[str] = []
    seen_public_domains: set[str] = set()
    seen_internal_domains: set[str] = set()

    for log in logs:
        actor_label = _normalize_log_actor_label(log)
        actor_domain = _extract_email_domain(log.get("user_email"))
        is_internal = bool(log.get("is_tech_only"))
        if not actor_label and not actor_domain:
            continue
        actor_key = actor_label.strip().lower() if actor_label else None
        if is_internal:
            if actor_label and latest_internal_actor_label is None:
                latest_internal_actor_label = actor_label
            if actor_label and actor_key and actor_key not in seen_internal:
                seen_internal.add(actor_key)
                recent_internal_actor_labels.append(actor_label)
            if actor_domain and actor_domain not in seen_internal_domains:
                seen_internal_domains.add(actor_domain)
                recent_internal_email_domains.append(actor_domain)
            continue
        if actor_label and latest_public_actor_label is None:
            latest_public_actor_label = actor_label
        if actor_label and actor_key and actor_key not in seen_public:
            seen_public.add(actor_key)
            recent_public_actor_labels.append(actor_label)
        if actor_domain and actor_domain not in seen_public_domains:
            seen_public_domains.add(actor_domain)
            recent_public_email_domains.append(actor_domain)

    participant_email_domains = _collect_email_domains(recent_public_email_domains, recent_internal_email_domains)
    return {
        "recent_public_actor_labels": recent_public_actor_labels,
        "recent_public_actor_labels_csv": ", ".join(recent_public_actor_labels) if recent_public_actor_labels else None,
        "recent_internal_actor_labels": recent_internal_actor_labels,
        "recent_internal_actor_labels_csv": ", ".join(recent_internal_actor_labels) if recent_internal_actor_labels else None,
        "latest_public_actor_label": latest_public_actor_label,
        "latest_internal_actor_label": latest_internal_actor_label,
        "recent_public_email_domains": recent_public_email_domains,
        "recent_public_email_domains_csv": ", ".join(recent_public_email_domains) if recent_public_email_domains else None,
        "recent_internal_email_domains": recent_internal_email_domains,
        "recent_internal_email_domains_csv": ", ".join(recent_internal_email_domains) if recent_internal_email_domains else None,
        "participant_email_domains": participant_email_domains,
        "participant_email_domains_csv": ", ".join(participant_email_domains) if participant_email_domains else None,
    }


def _derive_recent_log_cues(logs: list[dict[str, Any]]) -> dict[str, Any]:
    waiting_log = None
    response_log = None
    resolution_log = None
    for log in logs:
        cleaned_note = normalize_ticket_text(log.get("plain_note") or log.get("note"))
        log_type = _normalize_log_type(log.get("log_type"))
        log_record = {
            "log_type": log.get("log_type"),
            "record_date": log.get("record_date"),
            "cleaned_note": cleaned_note,
        }
        if waiting_log is None and cleaned_note and (bool(log.get("is_waiting")) or log_type == "waiting on response"):
            waiting_log = log_record
        if response_log is None and cleaned_note and log_type in _RESPONSE_LOG_TYPES:
            response_log = log_record
        if resolution_log is None and cleaned_note and log_type in _RESOLUTION_LOG_TYPES:
            resolution_log = log_record
    return {
        "waiting_log": waiting_log,
        "response_log": response_log,
        "resolution_log": resolution_log,
    }


def _resolve_followup_cue(
    explicit_followup_note: str | None,
    waiting_log_note: str | None,
) -> tuple[str | None, str]:
    if explicit_followup_note:
        return explicit_followup_note, "explicit_followup_note"
    if waiting_log_note:
        return waiting_log_note, "waiting_log"
    return None, "missing"


def _resolve_action_cue(
    cleaned_next_step: str | None,
    cleaned_followup_cue: str | None,
    cleaned_request_completion_note: str | None,
) -> tuple[str | None, str]:
    if cleaned_next_step:
        return cleaned_next_step, "next_step"
    if cleaned_followup_cue:
        return cleaned_followup_cue, "followup_note"
    if cleaned_request_completion_note:
        return cleaned_request_completion_note, "request_completion_note"
    return None, "missing"


def build_ticket_documents(db_path: Path, limit: int | None = None) -> list[dict]:
    query = """
        SELECT t.id,
               t.subject,
               t.status,
               t.priority,
               t.category,
               t.created_at,
               t.updated_at,
               t.closed_at,
               json_extract(t.raw_json, '$.number') AS ticket_number,
               json_extract(t.raw_json, '$.key') AS ticket_key,
               COALESCE(a.name, t.account_id) AS account,
               COALESCE(u.display_name, t.user_id) AS user_name,
               COALESCE(u.email, json_extract(t.raw_json, '$.user_email')) AS user_email,
               COALESCE(te.display_name, t.assigned_technician_id) AS technician,
               COALESCE(te.email, json_extract(t.raw_json, '$.technician_email'), json_extract(t.raw_json, '$.tech_email')) AS technician_email,
               t.account_id,
               t.user_id,
               t.assigned_technician_id,
               json_extract(t.raw_json, '$.account_name') AS raw_account_name,
               json_extract(t.raw_json, '$.account_location_name') AS raw_account_location_name,
               json_extract(t.raw_json, '$.user_name') AS raw_user_name,
               json_extract(t.raw_json, '$.user_fullname') AS raw_user_fullname,
               json_extract(t.raw_json, '$.user_firstname') AS raw_user_firstname,
               json_extract(t.raw_json, '$.user_lastname') AS raw_user_lastname,
               json_extract(t.raw_json, '$.user_email') AS raw_user_email,
               json_extract(t.raw_json, '$.tech_name') AS raw_tech_name,
               json_extract(t.raw_json, '$.technician_name') AS raw_technician_name,
               json_extract(t.raw_json, '$.assigned_technician_name') AS raw_assigned_technician_name,
               json_extract(t.raw_json, '$.technician_firstname') AS raw_technician_firstname,
               json_extract(t.raw_json, '$.technician_lastname') AS raw_technician_lastname,
               json_extract(t.raw_json, '$.initial_post') AS initial_post,
               json_extract(t.raw_json, '$.plain_initial_post') AS plain_initial_post,
               json_extract(td.raw_json, '$.initial_post') AS detail_initial_post,
               json_extract(td.raw_json, '$.plain_initial_post') AS detail_plain_initial_post,
               json_extract(t.raw_json, '$.creation_category_name') AS creation_category_name,
               json_extract(t.raw_json, '$.class_name') AS class_name,
               json_extract(t.raw_json, '$.submission_category') AS submission_category,
               json_extract(t.raw_json, '$.resolution_category_name') AS resolution_category_name,
               td.workpad,
               td.note AS detail_note,
               td.initial_response,
               json_extract(t.raw_json, '$.next_step') AS next_step,
               json_extract(td.raw_json, '$.next_step') AS detail_next_step,
               COALESCE(json_extract(td.raw_json, '$.next_step_date'), json_extract(t.raw_json, '$.next_step_date')) AS next_step_date,
               json_extract(td.raw_json, '$.followup_date') AS followup_date,
               json_extract(td.raw_json, '$.followup_note') AS followup_note,
               json_extract(td.raw_json, '$.request_completion_date') AS request_completion_date,
               json_extract(td.raw_json, '$.request_completion_note') AS request_completion_note,
               COALESCE(json_extract(td.raw_json, '$.support_group_name'), json_extract(t.raw_json, '$.support_group_name')) AS support_group_name,
               COALESCE(json_extract(td.raw_json, '$.default_contract_name'), json_extract(t.raw_json, '$.default_contract_name')) AS default_contract_name,
               COALESCE(json_extract(td.raw_json, '$.location_name'), json_extract(t.raw_json, '$.location_name')) AS location_name,
               COALESCE(json_extract(td.raw_json, '$.account_location_name'), json_extract(t.raw_json, '$.account_location_name')) AS account_location_name,
               COALESCE(json_extract(td.raw_json, '$.confirmed_by_name'), json_extract(t.raw_json, '$.confirmed_by_name')) AS confirmed_by_name,
               COALESCE(json_extract(td.raw_json, '$.confirmed_date'), json_extract(t.raw_json, '$.confirmed_date')) AS confirmed_date,
               COALESCE(json_extract(td.raw_json, '$.confirmed_note'), json_extract(t.raw_json, '$.confirmed_note')) AS confirmed_note,
               COALESCE(json_extract(td.raw_json, '$.department_key'), json_extract(t.raw_json, '$.department_key')) AS department_key,
               COALESCE(json_extract(td.raw_json, '$.is_via_email_parser'), json_extract(t.raw_json, '$.is_via_email_parser')) AS is_via_email_parser,
               COALESCE(json_extract(td.raw_json, '$.is_handle_by_callcentre'), json_extract(t.raw_json, '$.is_handle_by_callcentre')) AS is_handle_by_callcentre,
               json_extract(td.raw_json, '$.is_waiting_on_response') AS is_waiting_on_response,
               json_extract(td.raw_json, '$.is_resolved') AS is_resolved,
               json_extract(td.raw_json, '$.is_confirmed') AS is_confirmed,
               COALESCE(json_extract(td.raw_json, '$.user_phone'), json_extract(t.raw_json, '$.user_phone')) AS user_phone,
               COALESCE(json_extract(td.raw_json, '$.user_created_email'), json_extract(t.raw_json, '$.user_created_email')) AS user_created_email,
               COALESCE(json_extract(td.raw_json, '$.user_created_firstname'), json_extract(t.raw_json, '$.user_created_firstname')) AS user_created_firstname,
               COALESCE(json_extract(td.raw_json, '$.user_created_lastname'), json_extract(t.raw_json, '$.user_created_lastname')) AS user_created_lastname,
               COALESCE(json_extract(td.raw_json, '$.tech_type'), json_extract(t.raw_json, '$.tech_type')) AS technician_type,
               COALESCE(json_extract(td.raw_json, '$.days_old_in_minutes'), json_extract(t.raw_json, '$.days_old_in_minutes')) AS days_old_in_minutes,
               COALESCE(json_extract(td.raw_json, '$.waiting_minutes'), json_extract(t.raw_json, '$.waiting_minutes')) AS waiting_minutes,
               COALESCE(json_extract(td.raw_json, '$.project_id'), json_extract(t.raw_json, '$.project_id')) AS project_id,
               COALESCE(json_extract(td.raw_json, '$.project_name'), json_extract(t.raw_json, '$.project_name')) AS project_name,
               COALESCE(json_extract(td.raw_json, '$.scheduled_ticket_id'), json_extract(t.raw_json, '$.scheduled_ticket_id')) AS scheduled_ticket_id,
               COALESCE(json_extract(td.raw_json, '$.related_tickets_count'), json_extract(t.raw_json, '$.related_tickets_count')) AS related_tickets_count,
               COALESCE(json_extract(td.raw_json, '$.estimated_time'), json_extract(t.raw_json, '$.estimated_time')) AS estimated_time,
               COALESCE(json_extract(td.raw_json, '$.remaining_hours'), json_extract(t.raw_json, '$.remaining_hours')) AS remaining_hours,
               COALESCE(json_extract(td.raw_json, '$.total_hours'), json_extract(t.raw_json, '$.total_hours')) AS total_hours,
               COALESCE(json_extract(td.raw_json, '$.total_time_in_minutes'), json_extract(t.raw_json, '$.total_time_in_minutes')) AS total_time_in_minutes,
               COALESCE(json_extract(td.raw_json, '$.labor_cost'), json_extract(t.raw_json, '$.labor_cost')) AS labor_cost,
               COALESCE(json_extract(td.raw_json, '$.percentage_complete'), json_extract(t.raw_json, '$.percentage_complete')) AS percentage_complete,
               td.sla_response_date,
               td.sla_complete_date,
               td.ticketlogs_count,
               td.timelogs_count,
               td.attachments_count,
               (SELECT COUNT(*) FROM ticket_logs tl WHERE tl.ticket_id = t.id AND COALESCE(tl.is_tech_only, 0) = 0) AS public_log_count,
               (SELECT COUNT(*) FROM ticket_logs tl WHERE tl.ticket_id = t.id AND COALESCE(tl.is_tech_only, 0) = 1) AS internal_log_count,
               (
                   SELECT COUNT(*)
                   FROM (
                       SELECT DISTINCT COALESCE(NULLIF(lower(trim(tl.user_email)), ''), NULLIF(lower(trim(tl.user_name)), ''), NULLIF(trim(tl.user_id), ''), 'log:' || tl.id)
                       FROM ticket_logs tl
                       WHERE tl.ticket_id = t.id AND COALESCE(tl.is_tech_only, 0) = 0
                   ) participant_keys
               ) AS public_actor_count,
               (
                   SELECT COUNT(*)
                   FROM (
                       SELECT DISTINCT COALESCE(NULLIF(lower(trim(tl.user_email)), ''), NULLIF(lower(trim(tl.user_name)), ''), NULLIF(trim(tl.user_id), ''), 'log:' || tl.id)
                       FROM ticket_logs tl
                       WHERE tl.ticket_id = t.id AND COALESCE(tl.is_tech_only, 0) = 1
                   ) participant_keys
               ) AS internal_actor_count,
               (
                   SELECT COUNT(*)
                   FROM (
                       SELECT DISTINCT COALESCE(NULLIF(lower(trim(tl.user_email)), ''), NULLIF(lower(trim(tl.user_name)), ''), NULLIF(trim(tl.user_id), ''), 'log:' || tl.id)
                       FROM ticket_logs tl
                       WHERE tl.ticket_id = t.id
                   ) participant_keys
               ) AS total_actor_count,
               (SELECT COUNT(*) FROM ticket_logs tl WHERE tl.ticket_id = t.id AND (COALESCE(tl.is_waiting, 0) = 1 OR lower(COALESCE(tl.log_type, '')) = 'waiting on response')) AS waiting_log_count,
               (SELECT COUNT(*) FROM ticket_logs tl WHERE tl.ticket_id = t.id AND lower(COALESCE(tl.log_type, '')) IN ('response', 'initial post', 'initial log', 'log entry')) AS response_log_count,
               (SELECT COUNT(*) FROM ticket_logs tl WHERE tl.ticket_id = t.id AND lower(COALESCE(tl.log_type, '')) IN ('closed', 'close log')) AS resolution_log_count,
               (SELECT MAX(tl.record_date) FROM ticket_logs tl WHERE tl.ticket_id = t.id) AS latest_log_date,
               (SELECT MAX(tl.record_date) FROM ticket_logs tl WHERE tl.ticket_id = t.id AND COALESCE(tl.is_tech_only, 0) = 0) AS latest_public_log_date,
               (SELECT MAX(tl.record_date) FROM ticket_logs tl WHERE tl.ticket_id = t.id AND COALESCE(tl.is_tech_only, 0) = 1) AS latest_internal_log_date,
               (
                   SELECT COALESCE(NULLIF(tl.user_name, ''), NULLIF(tl.user_email, ''), NULLIF(tl.user_id, ''))
                   FROM ticket_logs tl
                   WHERE tl.ticket_id = t.id AND COALESCE(tl.is_tech_only, 0) = 0
                   ORDER BY tl.record_date DESC, tl.id DESC
                   LIMIT 1
               ) AS latest_public_actor_label,
               (
                   SELECT COALESCE(NULLIF(tl.user_name, ''), NULLIF(tl.user_email, ''), NULLIF(tl.user_id, ''))
                   FROM ticket_logs tl
                   WHERE tl.ticket_id = t.id AND COALESCE(tl.is_tech_only, 0) = 1
                   ORDER BY tl.record_date DESC, tl.id DESC
                   LIMIT 1
               ) AS latest_internal_actor_label,
               (SELECT MAX(tl.record_date) FROM ticket_logs tl WHERE tl.ticket_id = t.id AND (COALESCE(tl.is_waiting, 0) = 1 OR lower(COALESCE(tl.log_type, '')) = 'waiting on response')) AS latest_waiting_log_date,
               (SELECT MAX(tl.record_date) FROM ticket_logs tl WHERE tl.ticket_id = t.id AND lower(COALESCE(tl.log_type, '')) IN ('closed', 'close log')) AS latest_resolution_log_date,
               (
                   SELECT group_concat(COALESCE(tl.plain_note, tl.note), '\n---\n')
                   FROM (
                       SELECT plain_note, note
                       FROM ticket_logs
                       WHERE ticket_id = t.id
                       ORDER BY record_date DESC, id DESC
                       LIMIT 5
                   ) tl
               ) AS recent_log_text,
               (
                   SELECT group_concat(COALESCE(tl.log_type, 'log'), ', ')
                   FROM (
                       SELECT log_type
                       FROM ticket_logs
                       WHERE ticket_id = t.id
                       ORDER BY record_date DESC, id DESC
                       LIMIT 5
                   ) tl
               ) AS recent_log_types,
               (
                   SELECT json_group_array(json_object(
                       'id', tl.id,
                       'log_type', tl.log_type,
                       'record_date', tl.record_date,
                       'plain_note', tl.plain_note,
                       'note', tl.note,
                       'is_waiting', tl.is_waiting,
                       'is_tech_only', tl.is_tech_only,
                       'user_email', tl.user_email,
                       'user_name', tl.user_name
                   ))
                   FROM (
                       SELECT id, log_type, record_date, plain_note, note, is_waiting, is_tech_only, user_email, user_name
                       FROM ticket_logs
                       WHERE ticket_id = t.id
                       ORDER BY record_date DESC, id DESC
                       LIMIT 8
                   ) tl
               ) AS recent_logs_json,
               (
                   SELECT json_group_array(json_object(
                       'id', ta.id,
                       'name', ta.name,
                       'size', ta.size,
                       'recorded_at', ta.recorded_at,
                       'url', ta.url
                   ))
                   FROM ticket_attachments ta
                   WHERE ta.ticket_id = t.id
               ) AS attachment_metadata_json
        FROM tickets t
        LEFT JOIN accounts a ON a.id = t.account_id
        LEFT JOIN users u ON u.id = t.user_id
        LEFT JOIN technicians te ON te.id = t.assigned_technician_id
        LEFT JOIN ticket_details td ON td.ticket_id = t.id
        ORDER BY COALESCE(t.updated_at, t.created_at) DESC, t.id DESC
    """
    params: tuple = ()
    if limit is not None:
        query += " LIMIT ?"
        params = (limit,)

    with connect(db_path) as conn:
        rows = conn.execute(query, params).fetchall()

    docs: list[dict] = []
    for row in rows:
        record = dict(row)
        cleaned_initial_post = normalize_ticket_text(
            _first_present(
                record.get("detail_plain_initial_post"),
                record.get("detail_initial_post"),
                record.get("plain_initial_post"),
                record.get("initial_post"),
            )
        )
        cleaned_detail_note = normalize_ticket_text(record.get("detail_note"))
        cleaned_workpad = normalize_ticket_text(record.get("workpad"))
        recent_logs = _parse_recent_logs(record.get("recent_logs_json"))
        participant_summary = _summarize_recent_log_participants(recent_logs)
        log_cues = _derive_recent_log_cues(recent_logs)
        waiting_log = log_cues["waiting_log"]
        response_log = log_cues["response_log"]
        resolution_log = log_cues["resolution_log"]
        explicit_followup_note = normalize_ticket_text(record.get("followup_note"))
        waiting_log_note = waiting_log["cleaned_note"] if waiting_log else None
        cleaned_followup_note, followup_note_source = _resolve_followup_cue(explicit_followup_note, waiting_log_note)
        followup_date = _first_present(record.get("followup_date"), waiting_log["record_date"] if waiting_log else None)
        cleaned_request_completion_note = normalize_ticket_text(record.get("request_completion_note"))
        cleaned_recent_logs = normalize_ticket_text(record.get("recent_log_text"))
        cleaned_latest_response_note = normalize_ticket_text(response_log["cleaned_note"] if response_log else None)
        latest_response_date = response_log["record_date"] if response_log else None
        cleaned_resolution_log_note = normalize_ticket_text(resolution_log["cleaned_note"] if resolution_log else None)
        resolution_log_date = resolution_log["record_date"] if resolution_log else None
        resolution_summary = cleaned_resolution_log_note[:600] if cleaned_resolution_log_note else summarize_resolution_from_logs(record.get("recent_log_text"))
        normalized_category = (
            record.get("category")
            or record.get("creation_category_name")
            or record.get("class_name")
            or record.get("submission_category")
        )
        cleaned_subject = normalize_ticket_text(record.get("subject"))
        cleaned_confirmed_note = normalize_ticket_text(record.get("confirmed_note"))
        created_by_name = _join_name_parts(record.get("user_created_firstname"), record.get("user_created_lastname"))
        cleaned_next_step = normalize_ticket_text(_first_present(record.get("detail_next_step"), record.get("next_step")))
        cleaned_action_cue, action_cue_source = _resolve_action_cue(
            cleaned_next_step,
            cleaned_followup_note,
            cleaned_request_completion_note,
        )
        recent_log_types = _split_csv_values(record.get("recent_log_types"))
        account_label, account_label_source = _resolve_account_label(record)
        user_label, user_label_source = _resolve_user_label(record)
        technician_label, technician_label_source = _resolve_technician_label(record)
        department_label, department_label_source = _resolve_department_label(record)
        user_email_domain = _extract_email_domain(record.get("user_email"))
        user_created_email_domain = _extract_email_domain(record.get("user_created_email"))
        technician_email_domain = _extract_email_domain(record.get("technician_email"))
        participant_email_domains = _collect_email_domains(
            participant_summary["participant_email_domains"],
            record.get("user_email"),
            record.get("user_created_email"),
            record.get("technician_email"),
        )
        public_participant_email_domains = _collect_email_domains(
            participant_summary["recent_public_email_domains"],
            record.get("user_email"),
            record.get("user_created_email"),
        )
        internal_participant_email_domains = _collect_email_domains(
            participant_summary["recent_internal_email_domains"],
            record.get("technician_email"),
        )
        is_waiting_on_response = _coerce_bool(record.get("is_waiting_on_response"))
        is_resolved = _coerce_bool(record.get("is_resolved"))
        is_confirmed = _coerce_bool(record.get("is_confirmed"))
        is_via_email_parser = _coerce_bool(record.get("is_via_email_parser"))
        is_handle_by_callcentre = _coerce_bool(record.get("is_handle_by_callcentre"))
        has_project_context = bool(record.get("project_id") or record.get("project_name"))
        has_scheduled_parent = _present_metric(record.get("scheduled_ticket_id"))
        has_related_tickets = _present_metric(record.get("related_tickets_count"))
        public_log_count = _coerce_int(record.get("public_log_count"))
        internal_log_count = _coerce_int(record.get("internal_log_count"))
        waiting_log_count = _coerce_int(record.get("waiting_log_count"))
        response_log_count = _coerce_int(record.get("response_log_count"))
        resolution_log_count = _coerce_int(record.get("resolution_log_count"))
        public_actor_count = _coerce_int(record.get("public_actor_count"))
        internal_actor_count = _coerce_int(record.get("internal_actor_count"))
        total_actor_count = _coerce_int(record.get("total_actor_count"))
        has_public_logs = bool(public_log_count and public_log_count > 0)
        has_internal_logs = bool(internal_log_count and internal_log_count > 0)
        has_waiting_logs = bool(waiting_log_count and waiting_log_count > 0)
        has_resolution_logs = bool(resolution_log_count and resolution_log_count > 0)
        has_multi_public_participants = bool(public_actor_count and public_actor_count > 1)
        has_multi_internal_participants = bool(internal_actor_count and internal_actor_count > 1)
        has_mixed_visibility_activity = bool(has_public_logs and has_internal_logs)
        has_named_public_participants = bool(participant_summary["recent_public_actor_labels"])
        has_named_internal_participants = bool(participant_summary["recent_internal_actor_labels"])
        has_effort_tracking = any(
            _present_metric(record.get(field))
            for field in (
                "estimated_time",
                "remaining_hours",
                "total_hours",
                "total_time_in_minutes",
                "labor_cost",
                "percentage_complete",
            )
        )

        text_parts = [
            f"Ticket #{record['id']}: {record.get('subject') or '(no subject)'}",
            f"Status: {record.get('status') or 'unknown'}",
            f"Priority: {record.get('priority') or 'unknown'}",
            f"Category: {normalized_category or 'unknown'}",
            f"Account: {account_label or 'unknown'}",
            f"User: {user_label or 'unknown'}",
            f"Technician: {technician_label or 'unassigned'}",
            f"Created: {record.get('created_at') or 'unknown'}",
            f"Updated: {record.get('updated_at') or 'unknown'}",
            f"Closed: {record.get('closed_at') or 'not closed'}",
        ]
        if record.get("ticket_number"):
            text_parts.append(f"Ticket number: {record['ticket_number']}")
        if record.get("ticket_key"):
            text_parts.append(f"Ticket key: {record['ticket_key']}")
        if record.get("user_email"):
            text_parts.append(f"User email: {record['user_email']}")
        if user_email_domain:
            text_parts.append(f"User email domain: {user_email_domain}")
        if record.get("technician_email"):
            text_parts.append(f"Technician email: {record['technician_email']}")
        if technician_email_domain:
            text_parts.append(f"Technician email domain: {technician_email_domain}")
        if created_by_name:
            text_parts.append(f"Created by: {created_by_name}")
        if record.get("user_created_email"):
            text_parts.append(f"Created by email: {record['user_created_email']}")
        if user_created_email_domain:
            text_parts.append(f"Created by email domain: {user_created_email_domain}")
        if participant_email_domains:
            text_parts.append(f"Participant email domains: {', '.join(participant_email_domains)}")
        if public_participant_email_domains:
            text_parts.append(f"Public participant email domains: {', '.join(public_participant_email_domains)}")
        if internal_participant_email_domains:
            text_parts.append(f"Internal participant email domains: {', '.join(internal_participant_email_domains)}")
        if record.get("user_phone"):
            text_parts.append(f"User phone: {record['user_phone']}")
        if record.get("account_location_name"):
            text_parts.append(f"Account location: {record['account_location_name']}")
        if record.get("location_name"):
            text_parts.append(f"Location: {record['location_name']}")
        if department_label:
            text_parts.append(f"Department: {department_label}")
        if record.get("department_key"):
            text_parts.append(f"Department key: {record['department_key']}")
        if is_via_email_parser is not None:
            text_parts.append(f"Via email parser: {is_via_email_parser}")
        if is_handle_by_callcentre is not None:
            text_parts.append(f"Handled by call centre: {is_handle_by_callcentre}")
        if record.get("initial_response"):
            text_parts.append(f"Initial response flag/value: {record['initial_response']}")
        if record.get("sla_response_date"):
            text_parts.append(f"SLA response date: {record['sla_response_date']}")
        if record.get("sla_complete_date"):
            text_parts.append(f"SLA completion date: {record['sla_complete_date']}")
        if record.get("ticketlogs_count") is not None:
            text_parts.append(f"Ticket log count: {record['ticketlogs_count']}")
        if public_log_count is not None:
            text_parts.append(f"Public log count: {public_log_count}")
        if internal_log_count is not None:
            text_parts.append(f"Internal log count: {internal_log_count}")
        if public_actor_count is not None:
            text_parts.append(f"Distinct public participant count: {public_actor_count}")
        if internal_actor_count is not None:
            text_parts.append(f"Distinct internal participant count: {internal_actor_count}")
        if total_actor_count is not None:
            text_parts.append(f"Distinct participant count: {total_actor_count}")
        if waiting_log_count is not None:
            text_parts.append(f"Waiting log count: {waiting_log_count}")
        if response_log_count is not None:
            text_parts.append(f"Response log count: {response_log_count}")
        if resolution_log_count is not None:
            text_parts.append(f"Resolution log count: {resolution_log_count}")
        if record.get("latest_log_date"):
            text_parts.append(f"Latest log date: {record['latest_log_date']}")
        if record.get("latest_public_log_date"):
            text_parts.append(f"Latest public log date: {record['latest_public_log_date']}")
        if record.get("latest_internal_log_date"):
            text_parts.append(f"Latest internal log date: {record['latest_internal_log_date']}")
        if participant_summary["latest_public_actor_label"]:
            text_parts.append(f"Latest public participant: {participant_summary['latest_public_actor_label']}")
        elif record.get("latest_public_actor_label"):
            text_parts.append(f"Latest public participant: {record['latest_public_actor_label']}")
        if participant_summary["latest_internal_actor_label"]:
            text_parts.append(f"Latest internal participant: {participant_summary['latest_internal_actor_label']}")
        elif record.get("latest_internal_actor_label"):
            text_parts.append(f"Latest internal participant: {record['latest_internal_actor_label']}")
        if participant_summary["recent_public_actor_labels_csv"]:
            text_parts.append(f"Recent public participants: {participant_summary['recent_public_actor_labels_csv']}")
        if participant_summary["recent_internal_actor_labels_csv"]:
            text_parts.append(f"Recent internal participants: {participant_summary['recent_internal_actor_labels_csv']}")
        text_parts.append(f"Mixed visibility activity: {has_mixed_visibility_activity}")
        if record.get("latest_waiting_log_date"):
            text_parts.append(f"Latest waiting log date: {record['latest_waiting_log_date']}")
        if record.get("latest_resolution_log_date"):
            text_parts.append(f"Latest resolution log date: {record['latest_resolution_log_date']}")
        if record.get("timelogs_count") is not None:
            text_parts.append(f"Time log count: {record['timelogs_count']}")
        if record.get("attachments_count") is not None:
            text_parts.append(f"Attachment count: {record['attachments_count']}")
        if record.get("support_group_name"):
            text_parts.append(f"Support group: {record['support_group_name']}")
        if record.get("default_contract_name"):
            text_parts.append(f"Contract: {record['default_contract_name']}")
        if record.get("confirmed_by_name"):
            text_parts.append(f"Confirmed by: {record['confirmed_by_name']}")
        if record.get("confirmed_date"):
            text_parts.append(f"Confirmed date: {record['confirmed_date']}")
        if cleaned_confirmed_note:
            text_parts.append(f"Confirmed note: {cleaned_confirmed_note[:800]}")
        if is_waiting_on_response is not None:
            text_parts.append(f"Waiting on response: {is_waiting_on_response}")
        if record.get("waiting_minutes") not in (None, ""):
            text_parts.append(f"Waiting minutes: {record['waiting_minutes']}")
        if is_confirmed is not None:
            text_parts.append(f"Confirmed: {is_confirmed}")
        if is_resolved is not None:
            text_parts.append(f"Resolved flag: {is_resolved}")
        if record.get("days_old_in_minutes") not in (None, ""):
            text_parts.append(f"Ticket age minutes: {record['days_old_in_minutes']}")
        if record.get("technician_type"):
            text_parts.append(f"Technician type: {record['technician_type']}")
        if record.get("project_name"):
            text_parts.append(f"Project: {record['project_name']}")
        if record.get("project_id"):
            text_parts.append(f"Project ID: {record['project_id']}")
        if _present_metric(record.get("scheduled_ticket_id")):
            text_parts.append(f"Scheduled ticket ID: {record['scheduled_ticket_id']}")
        if _present_metric(record.get("related_tickets_count")):
            text_parts.append(f"Related ticket count: {record['related_tickets_count']}")
        if _present_metric(record.get("estimated_time")):
            text_parts.append(f"Estimated time: {record['estimated_time']}")
        if _present_metric(record.get("remaining_hours")):
            text_parts.append(f"Remaining hours: {record['remaining_hours']}")
        if _present_metric(record.get("total_hours")):
            text_parts.append(f"Total hours: {record['total_hours']}")
        if _present_metric(record.get("total_time_in_minutes")):
            text_parts.append(f"Total time minutes: {record['total_time_in_minutes']}")
        if _present_metric(record.get("labor_cost")):
            text_parts.append(f"Labor cost: {record['labor_cost']}")
        if _present_metric(record.get("percentage_complete")):
            text_parts.append(f"Percent complete: {record['percentage_complete']}")
        if cleaned_next_step:
            text_parts.append(f"Next step: {cleaned_next_step}")
        if record.get("next_step_date"):
            text_parts.append(f"Next step date: {record['next_step_date']}")
        if followup_date:
            text_parts.append(f"Follow-up date: {followup_date}")
        if cleaned_followup_note:
            text_parts.append(f"Follow-up note: {cleaned_followup_note[:1200]}")
        if record.get("request_completion_date"):
            text_parts.append(f"Requested completion date: {record['request_completion_date']}")
        if cleaned_request_completion_note:
            text_parts.append(f"Requested completion note: {cleaned_request_completion_note[:1200]}")
        if cleaned_initial_post:
            text_parts.append(f"Issue summary: {cleaned_initial_post[:2400]}")
        if cleaned_detail_note:
            text_parts.append(f"Internal note: {cleaned_detail_note[:1600]}")
        if cleaned_workpad:
            text_parts.append(f"Workpad summary: {cleaned_workpad[:1600]}")
        if latest_response_date:
            text_parts.append(f"Latest response date: {latest_response_date}")
        if cleaned_latest_response_note:
            text_parts.append(f"Latest response note: {cleaned_latest_response_note[:1600]}")
        if record.get("recent_log_types"):
            text_parts.append(f"Recent log types: {record['recent_log_types']}")
        if cleaned_recent_logs:
            text_parts.append(f"Recent log summary: {cleaned_recent_logs[:2400]}")
        if resolution_log_date:
            text_parts.append(f"Resolution log date: {resolution_log_date}")
        if cleaned_resolution_log_note:
            text_parts.append(f"Resolution log note: {cleaned_resolution_log_note[:1600]}")
        if resolution_summary:
            text_parts.append(f"Resolution/activity highlight: {resolution_summary}")
        if record.get("resolution_category_name"):
            text_parts.append(f"Resolution category: {record['resolution_category_name']}")

        attachment_metadata = []
        if record.get("attachment_metadata_json"):
            try:
                attachment_metadata = json.loads(record["attachment_metadata_json"]) or []
            except json.JSONDecodeError:
                attachment_metadata = []
        attachment_summary = _summarize_attachment_metadata(attachment_metadata)
        if attachment_metadata:
            text_parts.append(
                "Attachments (metadata only): " + ", ".join(
                    f"{item.get('name')} [{item.get('size')} bytes]" for item in attachment_metadata[:5]
                )
            )
        if attachment_summary.get("attachment_kinds_csv"):
            text_parts.append(f"Attachment kinds: {attachment_summary['attachment_kinds_csv']}")
        if attachment_summary.get("attachment_extensions_csv"):
            text_parts.append(f"Attachment extensions: {attachment_summary['attachment_extensions_csv']}")
        if attachment_summary.get("attachment_total_size_bytes") is not None:
            text_parts.append(f"Attachment total size bytes: {attachment_summary['attachment_total_size_bytes']}")

        text = "\n".join(text_parts)
        docs.append(
            {
                "doc_id": f"ticket:{record['id']}",
                "ticket_id": record["id"],
                "status": record.get("status"),
                "account": account_label,
                "account_id": record.get("account_id"),
                "user_name": user_label,
                "user_id": record.get("user_id"),
                "technician": technician_label,
                "technician_id": record.get("assigned_technician_id"),
                "updated_at": record.get("updated_at"),
                "created_at": record.get("created_at"),
                "text": text,
                "content_hash": _content_hash(text),
                "materialization_version": DOCUMENT_MATERIALIZATION_VERSION,
                "metadata": {
                    "priority": record.get("priority"),
                    "category": normalized_category,
                    "class_name": record.get("class_name"),
                    "submission_category": record.get("submission_category"),
                    "resolution_category": record.get("resolution_category_name"),
                    "department_label": department_label,
                    "department_label_source": department_label_source,
                    "closed_at": record.get("closed_at"),
                    "ticketlogs_count": record.get("ticketlogs_count"),
                    "public_log_count": public_log_count,
                    "internal_log_count": internal_log_count,
                    "public_actor_count": public_actor_count,
                    "internal_actor_count": internal_actor_count,
                    "total_actor_count": total_actor_count,
                    "waiting_log_count": waiting_log_count,
                    "response_log_count": response_log_count,
                    "resolution_log_count": resolution_log_count,
                    "latest_log_date": record.get("latest_log_date"),
                    "latest_public_log_date": record.get("latest_public_log_date"),
                    "latest_internal_log_date": record.get("latest_internal_log_date"),
                    "latest_public_actor_label": participant_summary["latest_public_actor_label"] or record.get("latest_public_actor_label"),
                    "latest_internal_actor_label": participant_summary["latest_internal_actor_label"] or record.get("latest_internal_actor_label"),
                    "recent_public_actor_labels": participant_summary["recent_public_actor_labels"],
                    "recent_public_actor_labels_csv": participant_summary["recent_public_actor_labels_csv"],
                    "recent_internal_actor_labels": participant_summary["recent_internal_actor_labels"],
                    "recent_internal_actor_labels_csv": participant_summary["recent_internal_actor_labels_csv"],
                    "latest_waiting_log_date": record.get("latest_waiting_log_date"),
                    "latest_resolution_log_date": record.get("latest_resolution_log_date"),
                    "timelogs_count": record.get("timelogs_count"),
                    "attachments_count": record.get("attachments_count"),
                    "attachments": attachment_metadata,
                    **attachment_summary,
                    "has_attachments": bool(attachment_metadata),
                    "detail_available": bool(
                        record.get("detail_note")
                        or record.get("workpad")
                        or record.get("initial_response")
                        or record.get("ticketlogs_count")
                        or record.get("attachments_count")
                        or record.get("detail_initial_post")
                        or record.get("detail_plain_initial_post")
                        or record.get("followup_note")
                        or record.get("request_completion_note")
                        or record.get("support_group_name")
                        or record.get("class_name")
                        or record.get("resolution_category_name")
                        or record.get("default_contract_name")
                        or record.get("account_location_name")
                        or record.get("department_key")
                        or record.get("confirmed_by_name")
                        or record.get("confirmed_date")
                        or cleaned_confirmed_note
                        or record.get("ticket_key")
                        or record.get("ticket_number")
                        or record.get("technician_email")
                        or record.get("user_phone")
                        or created_by_name
                        or record.get("user_created_email")
                        or record.get("technician_type")
                        or record.get("project_id")
                        or record.get("project_name")
                        or _present_metric(record.get("scheduled_ticket_id"))
                        or _present_metric(record.get("related_tickets_count"))
                        or _present_metric(record.get("estimated_time"))
                        or _present_metric(record.get("remaining_hours"))
                        or _present_metric(record.get("total_hours"))
                        or _present_metric(record.get("total_time_in_minutes"))
                        or _present_metric(record.get("labor_cost"))
                        or _present_metric(record.get("percentage_complete"))
                        or record.get("days_old_in_minutes") not in (None, "")
                        or record.get("waiting_minutes") not in (None, "")
                        or is_via_email_parser is not None
                        or is_handle_by_callcentre is not None
                    ),
                    "cleaned_subject": cleaned_subject[:300] if cleaned_subject else None,
                    "cleaned_initial_post": cleaned_initial_post[:400] if cleaned_initial_post else None,
                    "cleaned_detail_note": cleaned_detail_note[:400] if cleaned_detail_note else None,
                    "cleaned_workpad": cleaned_workpad[:400] if cleaned_workpad else None,
                    "cleaned_followup_note": cleaned_followup_note[:400] if cleaned_followup_note else None,
                    "cleaned_explicit_followup_note": explicit_followup_note[:400] if explicit_followup_note else None,
                    "cleaned_waiting_log_note": waiting_log_note[:400] if waiting_log_note else None,
                    "followup_note_source": followup_note_source,
                    "cleaned_request_completion_note": cleaned_request_completion_note[:400] if cleaned_request_completion_note else None,
                    "cleaned_next_step": cleaned_next_step[:300] if cleaned_next_step else None,
                    "cleaned_action_cue": cleaned_action_cue[:400] if cleaned_action_cue else None,
                    "action_cue_source": action_cue_source,
                    "cleaned_latest_response_note": cleaned_latest_response_note[:400] if cleaned_latest_response_note else None,
                    "latest_response_date": latest_response_date,
                    "cleaned_resolution_log_note": cleaned_resolution_log_note[:400] if cleaned_resolution_log_note else None,
                    "resolution_log_date": resolution_log_date,
                    "next_step_date": record.get("next_step_date"),
                    "followup_date": followup_date,
                    "request_completion_date": record.get("request_completion_date"),
                    "has_next_step": bool(cleaned_action_cue or record.get("next_step_date") or followup_date),
                    "recent_log_types": recent_log_types,
                    "recent_log_types_csv": ", ".join(recent_log_types) if recent_log_types else None,
                    "initial_response_present": record.get("initial_response") is not None,
                    "user_email": record.get("user_email"),
                    "user_email_domain": user_email_domain,
                    "user_created_email_domain": user_created_email_domain,
                    "technician_email_domain": technician_email_domain,
                    "participant_email_domains": participant_email_domains,
                    "participant_email_domains_csv": ", ".join(participant_email_domains) if participant_email_domains else None,
                    "participant_email_domain_count": len(participant_email_domains),
                    "public_participant_email_domains": public_participant_email_domains,
                    "public_participant_email_domains_csv": ", ".join(public_participant_email_domains) if public_participant_email_domains else None,
                    "public_participant_email_domain_count": len(public_participant_email_domains),
                    "internal_participant_email_domains": internal_participant_email_domains,
                    "internal_participant_email_domains_csv": ", ".join(internal_participant_email_domains) if internal_participant_email_domains else None,
                    "internal_participant_email_domain_count": len(internal_participant_email_domains),
                    "support_group_name": record.get("support_group_name"),
                    "default_contract_name": record.get("default_contract_name"),
                    "location_name": record.get("location_name"),
                    "account_location_name": record.get("account_location_name"),
                    "department_key": record.get("department_key"),
                    "department_label": department_label,
                    "department_label_source": department_label_source,
                    "ticket_number": record.get("ticket_number"),
                    "ticket_key": record.get("ticket_key"),
                    "technician_email": record.get("technician_email"),
                    "user_phone": record.get("user_phone"),
                    "user_created_name": created_by_name,
                    "user_created_email": record.get("user_created_email"),
                    "technician_type": record.get("technician_type"),
                    "project_id": record.get("project_id"),
                    "project_name": record.get("project_name"),
                    "scheduled_ticket_id": record.get("scheduled_ticket_id"),
                    "related_tickets_count": record.get("related_tickets_count"),
                    "estimated_time": record.get("estimated_time"),
                    "remaining_hours": record.get("remaining_hours"),
                    "total_hours": record.get("total_hours"),
                    "total_time_in_minutes": record.get("total_time_in_minutes"),
                    "labor_cost": record.get("labor_cost"),
                    "percentage_complete": record.get("percentage_complete"),
                    "has_project_context": has_project_context,
                    "has_scheduled_parent": has_scheduled_parent,
                    "has_related_tickets": has_related_tickets,
                    "has_effort_tracking": has_effort_tracking,
                    "has_public_logs": has_public_logs,
                    "has_internal_logs": has_internal_logs,
                    "has_multi_public_participants": has_multi_public_participants,
                    "has_multi_internal_participants": has_multi_internal_participants,
                    "has_named_public_participants": has_named_public_participants,
                    "has_named_internal_participants": has_named_internal_participants,
                    "has_mixed_visibility_activity": has_mixed_visibility_activity,
                    "has_waiting_logs": has_waiting_logs,
                    "has_resolution_logs": has_resolution_logs,
                    "days_old_in_minutes": record.get("days_old_in_minutes"),
                    "waiting_minutes": record.get("waiting_minutes"),
                    "confirmed_by_name": record.get("confirmed_by_name"),
                    "confirmed_date": record.get("confirmed_date"),
                    "cleaned_confirmed_note": cleaned_confirmed_note[:400] if cleaned_confirmed_note else None,
                    "is_via_email_parser": is_via_email_parser,
                    "is_handle_by_callcentre": is_handle_by_callcentre,
                    "is_waiting_on_response": is_waiting_on_response,
                    "is_resolved": is_resolved,
                    "is_confirmed": is_confirmed,
                    "account_label_source": account_label_source,
                    "user_label_source": user_label_source,
                    "technician_label_source": technician_label_source,
                    "resolution_summary": resolution_summary,
                    "has_resolution_summary": bool(resolution_summary),
                    "materialization_version": DOCUMENT_MATERIALIZATION_VERSION,
                },
            }
        )
    return docs


def build_ticket_document_chunks(docs: list[dict]) -> list[dict]:
    chunks: list[dict] = []
    for doc in docs:
        parts = _chunk_text(doc["text"])
        for idx, chunk_text in enumerate(parts):
            chunks.append(
                {
                    "chunk_id": f"{doc['doc_id']}:chunk:{idx}",
                    "doc_id": doc["doc_id"],
                    "ticket_id": doc["ticket_id"],
                    "account": doc.get("account"),
                    "account_id": doc.get("account_id"),
                    "status": doc.get("status"),
                    "technician": doc.get("technician"),
                    "technician_id": doc.get("technician_id"),
                    "chunk_index": idx,
                    "text": chunk_text,
                    "content_hash": _content_hash(chunk_text),
                    "updated_at": doc.get("updated_at"),
                    "created_at": doc.get("created_at"),
                }
            )
    return chunks


def materialize_ticket_documents(db_path: Path, limit: int | None = None) -> dict:
    docs = build_ticket_documents(db_path, limit=limit)
    chunks = build_ticket_document_chunks(docs)
    synced_at = now_iso()
    replace_ticket_documents(db_path, docs, synced_at=synced_at)
    replace_ticket_document_chunks(db_path, chunks, synced_at=synced_at)
    return {
        "status": "ok",
        "document_count": len(docs),
        "chunk_count": len(chunks),
        "synced_at": synced_at,
        "materialization_version": DOCUMENT_MATERIALIZATION_VERSION,
    }


def get_ticket_document_materialization_status(db_path: Path) -> dict:
    with connect(db_path) as conn:
        row = conn.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM tickets) AS ticket_count,
                (SELECT COUNT(*) FROM ticket_documents) AS document_count,
                (SELECT COUNT(*) FROM ticket_document_chunks) AS chunk_count,
                SUM(CASE WHEN COALESCE(json_extract(raw_json, '$.materialization_version'), json_extract(raw_json, '$.metadata.materialization_version'), 0) = ? THEN 1 ELSE 0 END) AS current_version_docs,
                SUM(CASE WHEN COALESCE(json_extract(raw_json, '$.materialization_version'), json_extract(raw_json, '$.metadata.materialization_version')) IS NULL THEN 1 ELSE 0 END) AS unversioned_docs,
                MIN(COALESCE(json_extract(raw_json, '$.materialization_version'), json_extract(raw_json, '$.metadata.materialization_version'))) AS min_version,
                MAX(COALESCE(json_extract(raw_json, '$.materialization_version'), json_extract(raw_json, '$.metadata.materialization_version'))) AS max_version
            FROM ticket_documents
            """,
            (DOCUMENT_MATERIALIZATION_VERSION,),
        ).fetchone()
    ticket_count = int(row["ticket_count"] or 0)
    document_count = int(row["document_count"] or 0)
    current_version_docs = int(row["current_version_docs"] or 0)
    unversioned_docs = int(row["unversioned_docs"] or 0)
    stale_docs = max(document_count - current_version_docs, 0)
    return {
        "current_version": DOCUMENT_MATERIALIZATION_VERSION,
        "ticket_count": ticket_count,
        "document_count": document_count,
        "chunk_count": int(row["chunk_count"] or 0),
        "current_version_docs": current_version_docs,
        "stale_docs": stale_docs,
        "stale_ratio": round((stale_docs / document_count), 4) if document_count else 0.0,
        "unversioned_docs": unversioned_docs,
        "min_version": int(row["min_version"]) if row["min_version"] is not None else None,
        "max_version": int(row["max_version"]) if row["max_version"] is not None else None,
        "needs_refresh": document_count != ticket_count or stale_docs > 0,
    }


def ensure_current_ticket_materialization(db_path: Path) -> dict:
    status = get_ticket_document_materialization_status(db_path)
    if not status["needs_refresh"]:
        return {"status": "ok", "refreshed": False, "materialization": status}
    refreshed = materialize_ticket_documents(db_path, limit=None)
    refreshed_status = get_ticket_document_materialization_status(db_path)
    return {
        "status": "ok",
        "refreshed": True,
        "reason": {
            "document_count_mismatch": status["document_count"] != status["ticket_count"],
            "stale_docs": status["stale_docs"],
        },
        "materialization": refreshed_status,
        "refresh_result": refreshed,
    }


def export_ticket_documents(db_path: Path, output_path: Path, limit: int | None = None) -> dict:
    docs = build_ticket_documents(db_path, limit=limit)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for doc in docs:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
    return {
        "status": "ok",
        "output_path": str(output_path),
        "document_count": len(docs),
    }


def export_ticket_chunks(db_path: Path, output_path: Path, limit: int | None = None) -> dict:
    docs = build_ticket_documents(db_path, limit=limit)
    chunks = build_ticket_document_chunks(docs)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    return {
        "status": "ok",
        "output_path": str(output_path),
        "chunk_count": len(chunks),
    }
