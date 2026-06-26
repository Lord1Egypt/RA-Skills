from __future__ import annotations

import base64
import json
import os
import re
import sqlite3
import subprocess
import time
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from email.utils import getaddresses, parseaddr
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from app.core.config import get_ingestion_accounts, get_user_emails, get_user_names
from app.ingestion.adapters import get_google_source
from app.ingestion.models import IngestionResult
from app.ingestion.run_log import (
    IngestRunContext,
    IngestRunCounts,
    finish_ingest_run,
    start_ingest_run,
)

# Hard cap on each `gog` CLI call so a stalled gog (auth prompt, network, token
# refresh) can't hang ingestion / the nightly pipeline forever.
GOG_TIMEOUT_SECONDS = 120

# Gmail rate-limit retry: detect Google's quota-exceeded responses
# (their wording varies — 429, "rate limit", "quota", "userRateLimitExceeded",
# "rateLimitExceeded") and back off exponentially. Caps at 5 attempts /
# ~30s total wait so a single search page can't stall ingestion indefinitely
# on a sustained outage.
_GOG_RATE_LIMIT_PATTERNS = (
    "429",
    "rateLimitExceeded",
    "userRateLimitExceeded",
    "quotaExceeded",
    "rate limit",
    "quota exceeded",
    "Too Many Requests",
)
_GOG_BACKOFF_SECONDS = (2, 4, 8, 16)  # 4 retries → max wait 30s


def _looks_like_rate_limit(text: str) -> bool:
    """True if a gog error string smells like a Google rate-limit response."""
    if not text:
        return False
    haystack = text.lower()
    return any(p.lower() in haystack for p in _GOG_RATE_LIMIT_PATTERNS)

SUPPORTED_IMPORT_FORMAT = """
Supported Gmail import inputs:

- live Gmail via `gog` CLI against one or more connected accounts
- a directory of `.json` files
- a single `.json` file containing one thread
- a single `.json` file containing `{"threads": [...]}`

Live Gmail ingestion uses:

- `gog gmail search <query>`
- `gog gmail thread get <threadId> --full`

Each imported thread can be either:

1. A normalized dump:
   {
     "thread_id": "thread-123",
     "account": "user@example.com",
     "source": "json_import",
     "subject": "Project follow-up",
     "messages": [
       {
         "id": "msg-1",
         "timestamp": "2026-03-01T09:00:00Z",
         "from_email": "alice@example.com",
         "from_name": "Alice",
         "body_text": "Can you send the draft?"
       }
     ]
   }

2. A saved Gmail API `users.threads.get` response JSON.

For live Gmail, YouOS first fetches matching thread ids via `gog gmail search`
and then fetches each full thread individually.
""".strip()


def get_default_gog_accounts() -> tuple[str, ...]:
    return get_ingestion_accounts()


def _default_user_emails() -> tuple[str, ...]:
    return get_user_emails()


def _default_user_names() -> tuple[str, ...]:
    return get_user_names()


class _HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data:
            self.parts.append(data)

    def text(self) -> str:
        return "".join(self.parts)


@dataclass(slots=True)
class NormalizedMessage:
    message_id: str
    thread_id: str
    account_email: str | None
    source_name: str
    subject: str | None
    timestamp: str | None
    sender_email: str | None
    sender_name: str | None
    recipient_context: dict[str, list[dict[str, str | None]]]
    body_text: str
    label_ids: list[str]
    metadata: dict[str, Any]
    self_authored: bool
    order_index: int


@dataclass(slots=True)
class ExtractedReplyPair:
    source_id: str
    thread_id: str
    document_source_id: str
    inbound_text: str
    reply_text: str
    inbound_author: str | None
    reply_author: str | None
    paired_at: str | None
    metadata: dict[str, Any]


@dataclass(slots=True)
class IngestCounts:
    discovered_threads: int = 0
    fetched_threads: int = 0
    threads: int = 0
    inbound_documents: int = 0
    chunks: int = 0
    reply_pairs: int = 0


@dataclass(slots=True)
class GogLiveOptions:
    accounts: tuple[str, ...]
    query: str
    max_threads: int | None
    cache_dir: Path | None = None


@dataclass(slots=True)
class LoadThreadPayloadsResult:
    payloads: list[dict[str, Any]]
    import_detail: str
    discovered_threads: int
    fetched_threads: int


class GmailLoadError(ValueError):
    def __init__(
        self,
        message: str,
        *,
        discovered_threads: int = 0,
        fetched_threads: int = 0,
    ) -> None:
        super().__init__(message)
        self.discovered_threads = discovered_threads
        self.fetched_threads = fetched_threads


def ingest_gmail_threads(
    export_path: Path | None = None,
    *,
    db_path: Path | None = None,
    user_emails: tuple[str, ...] = (),
    user_names: tuple[str, ...] = (),
    live: GogLiveOptions | None = None,
) -> IngestionResult:
    target_db_path = db_path or _default_sqlite_path()
    _ensure_sqlite_schema(target_db_path)

    counts = IngestCounts()
    ingestion_run_id = f"gmail-{uuid.uuid4()}"
    connection = sqlite3.connect(target_db_path)
    try:
        start_ingest_run(
            connection,
            IngestRunContext(
                run_id=ingestion_run_id,
                source="gmail",
                accounts=tuple(live.accounts) if live is not None else (),
                metadata={"import_source": _import_source_label(export_path, live=live)},
            ),
        )
        connection.commit()

        try:
            load_result = _load_thread_payloads(export_path, live=live)
        except (OSError, ValueError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
            source_label = _import_source_label(export_path, live=live)
            detail = f"Failed to load Gmail import from {source_label}: {exc}\n\n{SUPPORTED_IMPORT_FORMAT}"
            finish_ingest_run(
                connection,
                run_id=ingestion_run_id,
                status="failed",
                counts=IngestRunCounts(
                    discovered=getattr(exc, "discovered_threads", 0),
                    fetched=getattr(exc, "fetched_threads", 0),
                ),
                error_summary=f"Failed to load Gmail import from {source_label}",
                error_detail=detail,
            )
            connection.commit()
            return IngestionResult(
                source_type="gmail_thread",
                status="failed",
                detail=detail,
                run_id=ingestion_run_id,
            )

        thread_payloads = load_result.payloads
        import_detail = load_result.import_detail
        counts.discovered_threads = load_result.discovered_threads
        counts.fetched_threads = load_result.fetched_threads

        if not thread_payloads:
            detail = f"No Gmail threads were found from {import_detail}.\n\n{SUPPORTED_IMPORT_FORMAT}"
            finish_ingest_run(
                connection,
                run_id=ingestion_run_id,
                status="failed",
                counts=IngestRunCounts(
                    discovered=counts.discovered_threads,
                    fetched=counts.fetched_threads,
                ),
                error_summary="No Gmail threads were found",
                error_detail=detail,
            )
            connection.commit()
            return IngestionResult(
                source_type="gmail_thread",
                status="failed",
                detail=detail,
                run_id=ingestion_run_id,
            )

        try:
            normalized_threads = [
                _normalize_thread_payload(
                    payload,
                    user_emails=user_emails,
                    user_names=user_names,
                )
                for payload in thread_payloads
            ]
        except ValueError as exc:
            finish_ingest_run(
                connection,
                run_id=ingestion_run_id,
                status="failed",
                counts=IngestRunCounts(
                    discovered=counts.discovered_threads,
                    fetched=counts.fetched_threads,
                ),
                error_summary="Failed to normalize Gmail payloads",
                error_detail=str(exc),
            )
            connection.commit()
            return IngestionResult(
                source_type="gmail_thread",
                status="failed",
                detail=str(exc),
                run_id=ingestion_run_id,
            )

        counts.threads = len(normalized_threads)
        warning_count = _gmail_warning_count(normalized_threads)

        try:
            for thread in normalized_threads:
                inserted_documents = _ingest_thread_documents(
                    connection,
                    thread,
                    ingestion_run_id=ingestion_run_id,
                )
                counts.inbound_documents += inserted_documents
                counts.chunks += inserted_documents
                counts.reply_pairs += _ingest_thread_reply_pairs(connection, thread)
            status, detail, error_summary = _gmail_run_outcome(
                counts=counts,
                import_detail=import_detail,
                target_db_path=target_db_path,
                warning_count=warning_count,
            )
            finish_ingest_run(
                connection,
                run_id=ingestion_run_id,
                status=status,
                counts=IngestRunCounts(
                    discovered=counts.discovered_threads,
                    fetched=counts.fetched_threads,
                    stored_documents=counts.inbound_documents,
                    stored_chunks=counts.chunks,
                    stored_reply_pairs=counts.reply_pairs,
                ),
                error_summary=error_summary,
                error_detail=detail if status != "completed" else None,
            )
            connection.commit()
            return IngestionResult(
                source_type="gmail_thread",
                status=status,
                detail=detail,
                run_id=ingestion_run_id,
            )
        except Exception as exc:
            connection.rollback()
            finish_ingest_run(
                connection,
                run_id=ingestion_run_id,
                status="failed",
                counts=IngestRunCounts(
                    discovered=counts.discovered_threads,
                    fetched=counts.fetched_threads,
                ),
                error_summary="Failed while storing Gmail ingestion results",
                error_detail=str(exc),
            )
            connection.commit()
            return IngestionResult(
                source_type="gmail_thread",
                status="failed",
                detail=str(exc),
                run_id=ingestion_run_id,
            )
    finally:
        connection.close()


def _load_thread_payloads(
    export_path: Path | None,
    *,
    live: GogLiveOptions | None,
) -> LoadThreadPayloadsResult:
    if live is not None:
        payloads, discovered_threads = _load_live_thread_payloads(live)
        account_list = ", ".join(live.accounts)
        return LoadThreadPayloadsResult(
            payloads=payloads,
            import_detail=f"live Gmail via gog for [{account_list}] with query {live.query!r}",
            discovered_threads=discovered_threads,
            fetched_threads=len(payloads),
        )

    if export_path is None:
        raise ValueError("A local export path is required when live Gmail ingestion is not selected.")
    if not export_path.exists():
        raise ValueError(f"Path does not exist: {export_path}")

    json_files: list[Path]
    if export_path.is_dir():
        json_files = sorted(path for path in export_path.rglob("*.json") if path.is_file())
        payloads: list[dict[str, Any]] = []
        for path in json_files:
            payloads.extend(_load_thread_payload_file(path))
        return LoadThreadPayloadsResult(
            payloads=payloads,
            import_detail=str(export_path),
            discovered_threads=len(payloads),
            fetched_threads=len(payloads),
        )

    if export_path.suffix.lower() != ".json":
        raise ValueError("Expected a .json file or a directory containing .json files.")
    payloads = _load_thread_payload_file(export_path)
    return LoadThreadPayloadsResult(
        payloads=payloads,
        import_detail=str(export_path),
        discovered_threads=len(payloads),
        fetched_threads=len(payloads),
    )


def _load_live_thread_payloads(live: GogLiveOptions) -> tuple[list[dict[str, Any]], int]:
    payloads: list[dict[str, Any]] = []
    discovered_threads = 0
    source = get_google_source()
    for account in live.accounts:
        try:
            search_results = source.search_threads(
                account=account,
                query=live.query,
                max_threads=live.max_threads,
            )
            discovered_threads += len(search_results)
            time.sleep(2)
            for result in search_results:
                thread_id = _gog_thread_id_from_search_result(result)
                if not thread_id:
                    raise GmailLoadError(
                        f"gog gmail search returned a result without a thread id for account {account}: {json.dumps(result, sort_keys=True)}",
                        discovered_threads=discovered_threads,
                        fetched_threads=len(payloads),
                    )
                thread_payload = source.get_thread(account=account, thread_id=thread_id)
                time.sleep(0.5)
                enriched_payload = _wrap_live_thread_payload(
                    thread_payload,
                    account=account,
                    query=live.query,
                    search_result=result,
                )
                payloads.append(enriched_payload)
                if live.cache_dir is not None:
                    _cache_live_thread_payload(
                        live.cache_dir,
                        payload=enriched_payload,
                        account=account,
                        thread_id=thread_id,
                    )
        except GmailLoadError:
            raise
        except ValueError as exc:
            raise GmailLoadError(
                str(exc),
                discovered_threads=discovered_threads,
                fetched_threads=len(payloads),
            ) from exc
    return payloads, discovered_threads


def _load_thread_payload_file(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and isinstance(payload.get("threads"), list):
        threads = payload["threads"]
    elif isinstance(payload, dict):
        threads = [payload]
    else:
        raise ValueError(f"{path} must contain a JSON object.")

    if not all(isinstance(item, dict) for item in threads):
        raise ValueError(f"{path} contains a malformed thread list.")
    return list(threads)


def _gog_search_threads(
    *,
    account: str,
    query: str,
    max_threads: int | None,
) -> list[dict[str, Any]]:
    """Paginate through gog gmail search results with delays to avoid rate limits."""
    all_results: list[dict[str, Any]] = []
    page_token: str | None = None
    page_size = 50

    while True:
        command = [
            "gog",
            "gmail",
            "search",
            query,
            "--account",
            account,
            "--json",
            "--no-input",
            "--limit",
            str(page_size),
        ]
        if page_token:
            command.extend(["--page", page_token])

        # Route through `_run_gog_json` so search pages get the same rate-
        # limit retry/backoff as individual thread fetches — without this,
        # a 429 in the middle of a long search would abort the whole run.
        payload = _run_gog_json(command)

        # nextPageToken lives in the envelope when --results-only is omitted
        next_page_token: str | None = None
        if isinstance(payload, dict):
            next_page_token = _string(payload.get("nextPageToken"))
            results = _coerce_list_payload(payload, command_name="gog gmail search")
        else:
            results = _coerce_list_payload(payload, command_name="gog gmail search")

        if not all(isinstance(item, dict) for item in results):
            raise ValueError(f"gog gmail search returned malformed results for account {account}.")

        all_results.extend(results)

        if max_threads is not None and len(all_results) >= max_threads:
            all_results = all_results[:max_threads]
            break

        if not next_page_token or not results:
            break

        page_token = next_page_token
        time.sleep(1.5)  # pace between search pages to avoid rate limits

    return all_results


def _gog_get_thread(*, account: str, thread_id: str) -> dict[str, Any]:
    command = [
        "gog",
        "gmail",
        "thread",
        "get",
        thread_id,
        "--account",
        account,
        "--json",
        "--results-only",
        "--full",
        "--no-input",
    ]
    payload = _run_gog_json(command)
    if not isinstance(payload, dict):
        raise ValueError(f"gog gmail thread get returned malformed JSON for thread {thread_id}.")
    return _normalize_gog_thread_payload(payload, requested_thread_id=thread_id)


def _run_gog_json(command: list[str]) -> Any:
    """Run a gog subprocess and parse stdout as JSON, with rate-limit retry.

    On a returncode != 0 we inspect stderr/stdout for Google's quota-exceeded
    wording (`_looks_like_rate_limit`) and retry with exponential backoff
    (2s, 4s, 8s, 16s — 4 retries, ~30s max wait). Non-rate-limit errors
    raise immediately; transient quota errors get a chance to clear before
    propagating. Without this, a single rate-limited search page would
    abort the whole ingestion run on the first 429 of a long sync.
    """
    last_error: str = ""
    for _attempt, backoff in enumerate((*_GOG_BACKOFF_SECONDS, None), start=1):
        try:
            completed = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=GOG_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired as exc:
            raise ValueError(f"{' '.join(command)} timed out after {GOG_TIMEOUT_SECONDS}s") from exc

        if completed.returncode == 0:
            try:
                return json.loads(completed.stdout)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{' '.join(command)} returned invalid JSON: {exc}") from exc

        error_detail = completed.stderr.strip() or completed.stdout.strip() or "unknown gog error"
        last_error = error_detail
        if not _looks_like_rate_limit(error_detail) or backoff is None:
            # Either a non-retryable error or we're out of attempts.
            raise ValueError(f"{' '.join(command)} failed: {error_detail}")
        # Rate-limited; wait and retry.
        time.sleep(backoff)

    # Defensive — the loop above always returns or raises.
    raise ValueError(f"{' '.join(command)} failed after retries: {last_error}")


def _coerce_list_payload(payload: Any, *, command_name: str) -> list[Any]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("threads", "results", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    raise ValueError(f"{command_name} did not return a list payload.")


def _gog_thread_id_from_search_result(result: dict[str, Any]) -> str | None:
    candidate_fields = ("threadId", "thread_id", "id")
    for field in candidate_fields:
        value = _string(result.get(field))
        if value:
            return value

    for key in ("thread", "gmail_thread", "gmailThread", "result", "data", "item"):
        nested = result.get(key)
        if isinstance(nested, dict):
            nested_id = _gog_thread_id_from_search_result(nested)
            if nested_id:
                return nested_id

    return _find_nested_thread_id(result)


def _normalize_gog_thread_payload(payload: dict[str, Any], *, requested_thread_id: str) -> dict[str, Any]:
    thread_payload = _unwrap_gog_thread_payload(payload)
    normalized = dict(thread_payload)
    warning: str | None = None
    try:
        thread_id = _thread_id_from_payload(normalized)
    except ValueError:
        if not _payload_has_messages(normalized):
            raise
        thread_id = requested_thread_id
        warning = "gog gmail thread get returned messages without a thread id; YouOS used the requested thread id."

    normalized.setdefault("thread_id", thread_id)
    if warning is not None:
        warnings = normalized.get("ingestion_warnings")
        if isinstance(warnings, list):
            warning_list = [str(item) for item in warnings]
        else:
            warning_list = []
        warning_list.append(warning)
        normalized["ingestion_warnings"] = warning_list
    return normalized


def _unwrap_gog_thread_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if _payload_has_messages(payload):
        return payload

    for key in ("thread", "gmail_thread", "gmailThread", "result", "data", "item"):
        nested = payload.get(key)
        if isinstance(nested, dict):
            try:
                candidate = _unwrap_gog_thread_payload(nested)
            except ValueError:
                continue
            if _payload_has_messages(candidate):
                return candidate

    raise ValueError("gog gmail thread get returned a payload without a messages list.")


def _payload_has_messages(payload: dict[str, Any]) -> bool:
    return isinstance(payload.get("messages"), list)


def _find_nested_thread_id(value: Any) -> str | None:
    candidate_fields = ("threadId", "thread_id", "id")
    if isinstance(value, dict):
        for field in candidate_fields:
            candidate = _string(value.get(field))
            if candidate:
                return candidate
        for key, nested in value.items():
            if key in {"messages", "payload", "headers", "parts"}:
                continue
            nested_id = _find_nested_thread_id(nested)
            if nested_id:
                return nested_id
    elif isinstance(value, list):
        for item in value:
            nested_id = _find_nested_thread_id(item)
            if nested_id:
                return nested_id
    return None


def _wrap_live_thread_payload(
    payload: dict[str, Any],
    *,
    account: str,
    query: str,
    search_result: dict[str, Any],
) -> dict[str, Any]:
    enriched = dict(payload)
    enriched.setdefault("thread_id", _thread_id_from_payload(payload))
    enriched["account"] = account
    enriched["source"] = "gog_gmail"
    enriched["query"] = query
    enriched["fetched_at"] = datetime.now(tz=UTC).isoformat().replace("+00:00", "Z")
    enriched["search_result"] = search_result
    return enriched


def _gmail_warning_count(normalized_threads: list[list[NormalizedMessage]]) -> int:
    warning_keys: set[str] = set()
    for thread_index, thread in enumerate(normalized_threads):
        if not thread:
            continue
        warnings = thread[0].metadata.get("ingestion_warnings")
        if not isinstance(warnings, list):
            continue
        for warning in warnings:
            warning_keys.add(f"{thread_index}:{warning}")
    return len(warning_keys)


def _gmail_run_outcome(
    *,
    counts: IngestCounts,
    import_detail: str,
    target_db_path: Path,
    warning_count: int,
) -> tuple[str, str, str | None]:
    base_detail = (
        f"Ingested {counts.threads} Gmail thread(s) from {import_detail} into {target_db_path}. "
        f"Discovered {counts.discovered_threads} thread(s), fetched {counts.fetched_threads} payload(s), "
        f"stored {counts.inbound_documents} inbound document(s), {counts.chunks} chunk(s), "
        f"and {counts.reply_pairs} reply pair(s). "
        "Message bodies came from full thread payloads and reply pairs were extracted from ordered thread messages."
    )
    useful_rows = counts.inbound_documents + counts.reply_pairs
    if useful_rows == 0:
        return (
            "failed",
            f"{base_detail} YouOS fetched input but no useful Gmail corpus rows landed.",
            "No useful Gmail rows landed",
        )
    if warning_count > 0:
        return (
            "completed_with_warnings",
            f"{base_detail} Observed {warning_count} ingestion warning(s) in the source payloads.",
            "Gmail ingestion completed with warnings",
        )
    return "completed", base_detail, None


def _cache_live_thread_payload(
    cache_dir: Path,
    *,
    payload: dict[str, Any],
    account: str,
    thread_id: str,
) -> None:
    account_dir = cache_dir / _safe_path_component(account)
    account_dir.mkdir(parents=True, exist_ok=True)
    target_path = account_dir / f"{_safe_path_component(thread_id)}.json"
    target_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _normalize_thread_payload(
    payload: dict[str, Any],
    *,
    user_emails: tuple[str, ...],
    user_names: tuple[str, ...],
) -> list[NormalizedMessage]:
    thread_id = _thread_id_from_payload(payload)
    account_email = _normalize_email(_string(payload.get("account")))
    source_name = _string(payload.get("source")) or "json_import"
    raw_messages = payload.get("messages")
    if not isinstance(raw_messages, list) or not raw_messages:
        raise ValueError(f"Thread {thread_id!r} is missing a non-empty messages list.")

    normalized_messages: list[NormalizedMessage] = []
    for order_index, raw_message in enumerate(raw_messages):
        if not isinstance(raw_message, dict):
            raise ValueError(f"Thread {thread_id!r} contains a malformed message entry.")
        normalized_messages.append(
            _normalize_message(
                raw_message,
                thread_id=thread_id,
                account_email=account_email,
                source_name=source_name,
                default_subject=_string(payload.get("subject")),
                default_metadata=_thread_level_metadata(payload),
                user_emails=user_emails,
                user_names=user_names,
                order_index=order_index,
            )
        )

    normalized_messages.sort(key=lambda message: (_sort_key(message.timestamp), message.order_index))
    return normalized_messages


def _normalize_message(
    payload: dict[str, Any],
    *,
    thread_id: str,
    account_email: str | None,
    source_name: str,
    default_subject: str | None,
    default_metadata: dict[str, Any],
    user_emails: tuple[str, ...],
    user_names: tuple[str, ...],
    order_index: int,
) -> NormalizedMessage:
    message_id = _message_id_from_payload(payload, thread_id=thread_id, order_index=order_index)
    subject = _message_subject(payload) or default_subject
    sender_name, sender_email = _message_sender(payload)
    recipient_context = _message_recipient_context(payload)
    label_ids = _message_labels(payload)
    metadata = {**default_metadata, **_message_metadata(payload)}
    timestamp = _message_timestamp(payload)
    body_text = _message_body_text(payload).strip()
    self_authored = _is_user_message(
        payload,
        sender_email=sender_email,
        sender_name=sender_name,
        label_ids=label_ids,
        user_emails=_merge_identity_emails(user_emails, account_email),
        user_names=user_names,
    )
    return NormalizedMessage(
        message_id=message_id,
        thread_id=thread_id,
        account_email=account_email,
        source_name=source_name,
        subject=subject,
        timestamp=timestamp,
        sender_email=sender_email,
        sender_name=sender_name,
        recipient_context=recipient_context,
        body_text=body_text,
        label_ids=label_ids,
        metadata=metadata,
        self_authored=self_authored,
        order_index=order_index,
    )


def _thread_level_metadata(payload: dict[str, Any]) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    for field in ("account", "source", "query", "fetched_at", "search_result", "ingestion_warnings"):
        if field in payload:
            metadata[field] = payload[field]
    return metadata


def _thread_id_from_payload(payload: dict[str, Any]) -> str:
    thread_id = _string(payload.get("thread_id")) or _string(payload.get("threadId")) or _string(payload.get("id"))
    if thread_id:
        return thread_id

    messages = payload.get("messages")
    if isinstance(messages, list):
        for message in messages:
            if isinstance(message, dict):
                thread_id = _string(message.get("threadId")) or _string(message.get("thread_id"))
                if thread_id:
                    return thread_id

    raise ValueError("A thread payload is missing thread_id/threadId/id.")


def _message_id_from_payload(payload: dict[str, Any], *, thread_id: str, order_index: int) -> str:
    return (
        _string(payload.get("id")) or _string(payload.get("message_id")) or _string(payload.get("gmail_message_id")) or f"{thread_id}-message-{order_index + 1}"
    )


def _message_subject(payload: dict[str, Any]) -> str | None:
    return _string(payload.get("subject")) or _header_value(payload, "Subject") or _header_value(payload, "subject")


def _message_sender(payload: dict[str, Any]) -> tuple[str | None, str | None]:
    raw_name = _string(payload.get("from_name"))
    raw_email = _string(payload.get("from_email"))
    if raw_name or raw_email:
        return raw_name, _normalize_email(raw_email)

    header_from = _header_value(payload, "From") or _header_value(payload, "from")
    if header_from:
        name, email = parseaddr(header_from)
        return name or None, _normalize_email(email)

    from_obj = payload.get("from")
    if isinstance(from_obj, dict):
        return _string(from_obj.get("name")), _normalize_email(_string(from_obj.get("email")))

    return None, None


def _message_recipient_context(payload: dict[str, Any]) -> dict[str, list[dict[str, str | None]]]:
    context: dict[str, list[dict[str, str | None]]] = {}
    for field in ("to", "cc", "bcc", "reply_to"):
        recipients = _recipient_list(payload.get(field))
        if recipients:
            context[field] = recipients

    header_fields = {
        "to": "To",
        "cc": "Cc",
        "bcc": "Bcc",
        "reply_to": "Reply-To",
    }
    for output_field, header_name in header_fields.items():
        if output_field in context:
            continue
        header_value = _header_value(payload, header_name) or _header_value(payload, header_name.lower())
        recipients = _recipient_list(header_value)
        if recipients:
            context[output_field] = recipients
    return context


def _recipient_list(value: Any) -> list[dict[str, str | None]]:
    if value is None:
        return []
    if isinstance(value, str):
        return _addresses_from_text(value)
    if isinstance(value, list):
        recipients: list[dict[str, str | None]] = []
        for item in value:
            if isinstance(item, dict):
                recipient = {
                    "name": _string(item.get("name")),
                    "email": _normalize_email(_string(item.get("email"))),
                }
                if recipient["name"] or recipient["email"]:
                    recipients.append(recipient)
                continue
            if isinstance(item, str):
                recipients.extend(_addresses_from_text(item))
        return recipients
    if isinstance(value, dict):
        recipient = {
            "name": _string(value.get("name")),
            "email": _normalize_email(_string(value.get("email"))),
        }
        return [recipient] if recipient["name"] or recipient["email"] else []
    return []


def _addresses_from_text(value: str) -> list[dict[str, str | None]]:
    recipients: list[dict[str, str | None]] = []
    for name, email in getaddresses([value]):
        recipient = {
            "name": name or None,
            "email": _normalize_email(email),
        }
        if recipient["name"] or recipient["email"]:
            recipients.append(recipient)
    return recipients


def _message_labels(payload: dict[str, Any]) -> list[str]:
    labels = payload.get("labelIds")
    if not isinstance(labels, list):
        labels = payload.get("label_ids") or payload.get("labels") or []
    return [str(item) for item in labels if item is not None]


def _message_metadata(payload: dict[str, Any]) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    fields = (
        "snippet",
        "historyId",
        "history_id",
        "internalDate",
        "internal_date",
        "internal_date_ms",
        "to",
        "cc",
        "bcc",
    )
    for field in fields:
        if field in payload:
            metadata[field] = payload[field]
    return metadata


def _message_timestamp(payload: dict[str, Any]) -> str | None:
    candidates = (
        payload.get("timestamp"),
        payload.get("created_at"),
        payload.get("sent_at"),
        payload.get("internal_date"),
        payload.get("internal_date_ms"),
        payload.get("internalDate"),
        _header_value(payload, "Date"),
        _header_value(payload, "date"),
    )
    for value in candidates:
        parsed = _normalize_timestamp(value)
        if parsed:
            return parsed
    return None


def _message_body_text(payload: dict[str, Any]) -> str:
    direct_fields = (
        "body_text",
        "body",
        "text",
        "plain_text",
        "content",
        "snippet",
    )
    for field in direct_fields:
        value = _string(payload.get(field))
        if value:
            return value

    payload_obj = payload.get("payload")
    if isinstance(payload_obj, dict):
        text_parts = _extract_payload_parts(payload_obj, mime_type="text/plain")
        if text_parts:
            return "\n".join(part for part in text_parts if part.strip()).strip()

        html_parts = _extract_payload_parts(payload_obj, mime_type="text/html")
        if html_parts:
            return _html_to_text("\n".join(html_parts)).strip()

    return ""


def _extract_payload_parts(payload: dict[str, Any], *, mime_type: str) -> list[str]:
    parts: list[str] = []
    if payload.get("mimeType") == mime_type:
        decoded = _decode_gmail_body(payload.get("body"))
        if decoded:
            parts.append(decoded)

    for part in payload.get("parts", []) or []:
        if isinstance(part, dict):
            parts.extend(_extract_payload_parts(part, mime_type=mime_type))
    return parts


def _decode_gmail_body(body_payload: Any) -> str:
    if not isinstance(body_payload, dict):
        return ""
    data = body_payload.get("data")
    if not data:
        return ""
    try:
        padded = str(data) + "=" * (-len(str(data)) % 4)
        decoded = base64.urlsafe_b64decode(padded.encode("ascii"))
    except (ValueError, UnicodeEncodeError):
        return ""
    return decoded.decode("utf-8", errors="replace")


def _html_to_text(html: str) -> str:
    parser = _HTMLTextExtractor()
    parser.feed(html)
    return parser.text()


def _header_value(payload: dict[str, Any], header_name: str) -> str | None:
    payload_obj = payload.get("payload")
    if not isinstance(payload_obj, dict):
        return None
    headers = payload_obj.get("headers")
    if not isinstance(headers, list):
        return None
    expected_name = header_name.lower()
    for header in headers:
        if not isinstance(header, dict):
            continue
        if str(header.get("name", "")).lower() == expected_name:
            return _string(header.get("value"))
    return None


def _is_user_message(
    payload: dict[str, Any],
    *,
    sender_email: str | None,
    sender_name: str | None,
    label_ids: list[str],
    user_emails: tuple[str, ...],
    user_names: tuple[str, ...],
) -> bool:
    explicit_role = _string(payload.get("author_role")) or _string(payload.get("mailbox_role"))
    if explicit_role and explicit_role.lower() in {"self", "user", "me"}:
        return True

    if payload.get("is_user") is True or payload.get("self_authored") is True:
        return True

    if any(label.upper() == "SENT" for label in label_ids):
        return True

    normalized_emails = {email.lower() for email in user_emails}
    normalized_names = {name.strip().lower() for name in user_names}
    if sender_email and sender_email.lower() in normalized_emails:
        return True
    if sender_name and sender_name.strip().lower() in normalized_names:
        return True

    return False


def _ingest_thread_documents(
    connection: sqlite3.Connection,
    thread: list[NormalizedMessage],
    *,
    ingestion_run_id: str,
) -> int:
    inserted_count = 0
    for message in thread:
        if message.self_authored or not message.body_text:
            continue
        document_id = _upsert_document(connection, message, ingestion_run_id=ingestion_run_id)
        _upsert_chunk(connection, document_id=document_id, message=message)
        inserted_count += 1
    return inserted_count


_ACKNOWLEDGMENT_ONLY = re.compile(
    r"^\s*(ok|okay|k|sure|thanks|thank you|ty|thx|noted|got it|will do|sounds good|great|perfect|"
    r"received|ack|acknowledged|\+1|roger|copy that|understood)\s*[.!]?\s*$",
    re.IGNORECASE,
)
_FORWARDED_PATTERN = re.compile(
    r"(-{5,}\s*forwarded message|-{5,}\s*original message|begin forwarded message)",
    re.IGNORECASE,
)
_OUT_OF_OFFICE = re.compile(
    r"\b(out of (office|office message)|on (vacation|leave|holiday)|auto(-|\s*)reply|"
    r"i am (away|unavailable|currently out)|be back on|return(ing)? (on|from))\b",
    re.IGNORECASE,
)


def _is_low_quality_reply(text: str) -> bool:
    """E9: Return True for replies that are too short or purely acknowledgments/OOO."""
    stripped = text.strip()
    if len(stripped.split()) < 3:
        return True
    if _ACKNOWLEDGMENT_ONLY.match(stripped):
        return True
    if _OUT_OF_OFFICE.search(stripped[:400]):
        return True
    return False


def _is_forwarded_inbound(message: "NormalizedMessage") -> bool:
    """E21: Return True if the inbound message is a forwarded email."""
    if _FORWARDED_PATTERN.search(message.body_text[:500]):
        return True
    labels = [lbl.upper() for lbl in (message.label_ids or [])]
    if "FORWARDED" in labels:
        return True
    return False


def _ingest_thread_reply_pairs(connection: sqlite3.Connection, thread: list[NormalizedMessage]) -> int:
    document_ids_by_source = _load_document_ids(connection, thread_id=thread[0].thread_id)
    pair_count = 0
    pending_inbound: list[NormalizedMessage] = []

    for message in thread:
        if message.self_authored:
            if pending_inbound and message.body_text:
                # E9: skip low-quality replies
                if not _is_low_quality_reply(message.body_text):
                    latest_inbound = pending_inbound[-1]
                    pair = _build_reply_pair(
                        pending_inbound,
                        reply_message=message,
                        document_source_id=latest_inbound.message_id,
                    )
                    document_id = document_ids_by_source.get(pair.document_source_id)
                    if document_id is not None:
                        _upsert_reply_pair(connection, pair=pair, document_id=document_id)
                        pair_count += 1
            pending_inbound = []
            continue

        # E22: skip inbound messages with <10 chars (calendar invites, empty payloads)
        # E21: skip forwarded emails
        if message.body_text and len(message.body_text.strip()) >= 10 and not _is_forwarded_inbound(message):
            pending_inbound.append(message)

    return pair_count


def _build_reply_pair(
    inbound_messages: list[NormalizedMessage],
    *,
    reply_message: NormalizedMessage,
    document_source_id: str,
) -> ExtractedReplyPair:
    blocks = []
    for message in inbound_messages:
        if len(inbound_messages) == 1:
            blocks.append(message.body_text)
            continue
        author = _display_author(message.sender_name, message.sender_email) or "Unknown"
        if message.timestamp:
            blocks.append(f"From: {author}\nAt: {message.timestamp}\n\n{message.body_text}")
        else:
            blocks.append(f"From: {author}\n\n{message.body_text}")

    inbound_author = _display_author(
        inbound_messages[-1].sender_name,
        inbound_messages[-1].sender_email,
    )
    reply_author = _display_author(reply_message.sender_name, reply_message.sender_email)
    return ExtractedReplyPair(
        source_id=f"{reply_message.thread_id}:{reply_message.message_id}",
        thread_id=reply_message.thread_id,
        document_source_id=document_source_id,
        inbound_text="\n\n---\n\n".join(blocks).strip(),
        reply_text=reply_message.body_text,
        inbound_author=inbound_author,
        reply_author=reply_author,
        paired_at=reply_message.timestamp,
        metadata={
            "subject": reply_message.subject,
            "account_email": reply_message.account_email,
            "source": reply_message.source_name,
            "pair_strategy": "messages_since_last_self_authored_message",
            "inbound_message_ids": [message.message_id for message in inbound_messages],
            "reply_message_id": reply_message.message_id,
            "inbound_recipient_contexts": [message.recipient_context for message in inbound_messages],
            "reply_recipient_context": reply_message.recipient_context,
            "inbound_authors": [_display_author(message.sender_name, message.sender_email) for message in inbound_messages],
            "reply_labels": reply_message.label_ids,
        },
    )


def _upsert_document(
    connection: sqlite3.Connection,
    message: NormalizedMessage,
    *,
    ingestion_run_id: str,
) -> int:
    metadata_json = json.dumps(
        {
            "message_id": message.message_id,
            "thread_id": message.thread_id,
            "account_email": message.account_email,
            "source": message.source_name,
            "sender": {
                "name": message.sender_name,
                "email": message.sender_email,
            },
            "recipients": message.recipient_context,
            "self_authored": message.self_authored,
            "label_ids": message.label_ids,
            **message.metadata,
        },
        sort_keys=True,
    )
    connection.execute(
        """
        INSERT INTO documents (
            source_type,
            source_id,
            title,
            author,
            external_uri,
            thread_id,
            created_at,
            updated_at,
            content,
            metadata_json,
            ingestion_run_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(source_type, source_id) DO UPDATE SET
            title = excluded.title,
            author = excluded.author,
            thread_id = excluded.thread_id,
            created_at = excluded.created_at,
            updated_at = excluded.updated_at,
            content = excluded.content,
            metadata_json = excluded.metadata_json,
            ingestion_run_id = excluded.ingestion_run_id
        """,
        (
            "gmail_thread",
            message.message_id,
            message.subject,
            _display_author(message.sender_name, message.sender_email),
            None,
            message.thread_id,
            message.timestamp,
            message.timestamp,
            message.body_text,
            metadata_json,
            ingestion_run_id,
        ),
    )
    row = connection.execute(
        "SELECT id FROM documents WHERE source_type = ? AND source_id = ?",
        ("gmail_thread", message.message_id),
    ).fetchone()
    if row is None:
        raise ValueError(f"Failed to load document id for message {message.message_id}")
    return int(row[0])


def _upsert_chunk(connection: sqlite3.Connection, *, document_id: int, message: NormalizedMessage) -> None:
    metadata_json = json.dumps(
        {
            "thread_id": message.thread_id,
            "message_id": message.message_id,
            "account_email": message.account_email,
            "source": message.source_name,
            "chunk_role": "full_message",
        },
        sort_keys=True,
    )
    connection.execute(
        """
        INSERT INTO chunks (
            document_id,
            chunk_index,
            content,
            token_count,
            char_count,
            metadata_json
        )
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(document_id, chunk_index) DO UPDATE SET
            content = excluded.content,
            token_count = excluded.token_count,
            char_count = excluded.char_count,
            metadata_json = excluded.metadata_json
        """,
        (
            document_id,
            0,
            message.body_text,
            None,
            len(message.body_text),
            metadata_json,
        ),
    )


def _load_document_ids(connection: sqlite3.Connection, *, thread_id: str) -> dict[str, int]:
    rows = connection.execute(
        """
        SELECT source_id, id
        FROM documents
        WHERE source_type = ? AND thread_id = ?
        """,
        ("gmail_thread", thread_id),
    ).fetchall()
    return {str(source_id): int(document_id) for source_id, document_id in rows}


def _upsert_reply_pair(
    connection: sqlite3.Connection,
    *,
    pair: ExtractedReplyPair,
    document_id: int,
) -> None:
    # E14: detect language from inbound text for language-filtered retrieval
    language: str | None = None
    try:
        from app.core.text_utils import detect_language
        language = detect_language(pair.inbound_text or "")
    except Exception:
        pass

    connection.execute(
        """
        INSERT INTO reply_pairs (
            source_type,
            source_id,
            document_id,
            thread_id,
            inbound_text,
            reply_text,
            inbound_author,
            reply_author,
            paired_at,
            metadata_json,
            language
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(source_type, source_id) DO UPDATE SET
            document_id = excluded.document_id,
            thread_id = excluded.thread_id,
            inbound_text = excluded.inbound_text,
            reply_text = excluded.reply_text,
            inbound_author = excluded.inbound_author,
            reply_author = excluded.reply_author,
            paired_at = excluded.paired_at,
            metadata_json = excluded.metadata_json,
            language = excluded.language
        """,
        (
            "gmail_thread",
            pair.source_id,
            document_id,
            pair.thread_id,
            pair.inbound_text,
            pair.reply_text,
            pair.inbound_author,
            pair.reply_author,
            pair.paired_at,
            json.dumps(pair.metadata, sort_keys=True),
            language,
        ),
    )


def _ensure_sqlite_schema(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    schema_path = Path(__file__).resolve().parents[2] / "docs" / "schema.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(schema_sql)
        connection.commit()
    finally:
        connection.close()


def _display_author(name: str | None, email: str | None) -> str | None:
    if name and email:
        return f"{name} <{email}>"
    return name or email


def _normalize_email(email: str | None) -> str | None:
    if not email:
        return None
    return email.strip().lower()


def _merge_identity_emails(
    user_emails: tuple[str, ...],
    account_email: str | None,
) -> tuple[str, ...]:
    if account_email is None:
        return user_emails
    return (*user_emails, account_email)


def _normalize_timestamp(value: Any) -> str | None:
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return _timestamp_from_epoch(value)

    text = str(value).strip()
    if not text:
        return None

    if text.isdigit():
        return _timestamp_from_epoch(int(text))

    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _timestamp_from_epoch(value: int | float) -> str | None:
    try:
        seconds = float(value)
        if seconds > 1_000_000_000_000:
            seconds /= 1000
        parsed = datetime.fromtimestamp(seconds, tz=UTC)
    except (OSError, OverflowError, ValueError):
        return None
    return parsed.isoformat().replace("+00:00", "Z")


def _sort_key(timestamp: str | None) -> tuple[int, str]:
    if timestamp is None:
        return (1, "")
    return (0, timestamp)


def _string(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return str(value)


def _safe_path_component(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_", "."} else "_" for char in value)


def _import_source_label(export_path: Path | None, *, live: GogLiveOptions | None) -> str:
    if live is not None:
        return f"live Gmail via gog for {', '.join(live.accounts)}"
    if export_path is None:
        return "<unknown>"
    return str(export_path)


def _default_sqlite_path() -> Path:
    database_url = os.getenv("YOUOS_DATABASE_URL", "sqlite:///var/youos.db")
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        raise ValueError("Only sqlite:/// database URLs are supported for Gmail ingestion.")
    return Path(database_url.removeprefix(prefix))
