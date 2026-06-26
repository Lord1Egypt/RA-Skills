from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.core.config import get_ingestion_accounts
from app.ingestion.adapters import GoogleWorkspaceSource, get_google_source
from app.ingestion.models import IngestionResult
from app.ingestion.run_log import (
    IngestRunContext,
    IngestRunCounts,
    finish_ingest_run,
    start_ingest_run,
)

SUPPORTED_IMPORT_FORMAT = """
Supported Google Docs import inputs:

- live Google Docs via `gog` CLI against one or more connected accounts
- a directory of `.json` files created by YouOS Docs caching
- a single cached `.json` file created by YouOS Docs caching

Live Google Docs ingestion uses:

- `gog drive search <query>` for discovery
- `gog docs info <docId>` for Docs metadata
- `gog drive get <docId>` for Drive file metadata
- `gog docs cat <docId>` for plain-text content

The local JSON fallback only supports YouOS cached snapshot files. It does not
accept arbitrary Google Docs export shapes.
""".strip()


def get_default_gog_accounts():
    return get_ingestion_accounts()


DEFAULT_DRIVE_QUERY = "mimeType = 'application/vnd.google-apps.document' and trashed = false"

# Hard cap on each `gog` CLI call so a stalled gog can't hang ingestion forever.
GOG_TIMEOUT_SECONDS = 120


@dataclass(slots=True)
class GogDocsLiveOptions:
    accounts: tuple[str, ...]
    query: str
    max_docs: int | None
    cache_dir: Path | None = None
    raw_query: bool = True
    all_tabs: bool = False
    max_bytes: int = 0
    doc_ids: tuple[str, ...] = ()


@dataclass(slots=True)
class NormalizedGoogleDoc:
    doc_id: str
    account_email: str | None
    source_name: str
    title: str | None
    author: str | None
    external_uri: str | None
    created_at: str | None
    updated_at: str | None
    content: str
    metadata: dict[str, Any]


@dataclass(slots=True)
class LoadDocPayloadsResult:
    payloads: list[dict[str, Any]]
    import_detail: str
    discovered_docs: int
    fetched_docs: int


class GoogleDocsLoadError(ValueError):
    def __init__(
        self,
        message: str,
        *,
        discovered_docs: int = 0,
        fetched_docs: int = 0,
    ) -> None:
        super().__init__(message)
        self.discovered_docs = discovered_docs
        self.fetched_docs = fetched_docs


def ingest_google_docs(
    export_path: Path | None = None,
    *,
    db_path: Path | None = None,
    live: GogDocsLiveOptions | None = None,
) -> IngestionResult:
    target_db_path = db_path or _default_sqlite_path()
    _ensure_sqlite_schema(target_db_path)

    ingestion_run_id = f"google-docs-{uuid.uuid4()}"
    document_count = 0
    chunk_count = 0
    discovered_docs = 0
    fetched_docs = 0
    connection = sqlite3.connect(target_db_path)
    try:
        start_ingest_run(
            connection,
            IngestRunContext(
                run_id=ingestion_run_id,
                source="google_docs",
                accounts=tuple(live.accounts) if live is not None else (),
                metadata={"import_source": _import_source_label(export_path, live=live)},
            ),
        )
        connection.commit()

        try:
            load_result = _load_doc_payloads(export_path, live=live)
        except (OSError, ValueError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
            source_label = _import_source_label(export_path, live=live)
            detail = f"Failed to load Google Docs import from {source_label}: {exc}\n\n{SUPPORTED_IMPORT_FORMAT}"
            finish_ingest_run(
                connection,
                run_id=ingestion_run_id,
                status="failed",
                counts=IngestRunCounts(
                    discovered=getattr(exc, "discovered_docs", 0),
                    fetched=getattr(exc, "fetched_docs", 0),
                ),
                error_summary=f"Failed to load Google Docs import from {source_label}",
                error_detail=detail,
            )
            connection.commit()
            return IngestionResult(
                source_type="google_doc",
                status="failed",
                detail=detail,
                run_id=ingestion_run_id,
            )

        doc_payloads = load_result.payloads
        import_detail = load_result.import_detail
        discovered_docs = load_result.discovered_docs
        fetched_docs = load_result.fetched_docs

        if not doc_payloads:
            detail = f"No Google Docs were found from {import_detail}.\n\n{SUPPORTED_IMPORT_FORMAT}"
            finish_ingest_run(
                connection,
                run_id=ingestion_run_id,
                status="failed",
                counts=IngestRunCounts(discovered=discovered_docs, fetched=fetched_docs),
                error_summary="No Google Docs were found",
                error_detail=detail,
            )
            connection.commit()
            return IngestionResult(
                source_type="google_doc",
                status="failed",
                detail=detail,
                run_id=ingestion_run_id,
            )

        try:
            normalized_docs = [_normalize_doc_payload(payload) for payload in doc_payloads]
        except ValueError as exc:
            finish_ingest_run(
                connection,
                run_id=ingestion_run_id,
                status="failed",
                counts=IngestRunCounts(discovered=discovered_docs, fetched=fetched_docs),
                error_summary="Failed to normalize Google Docs payloads",
                error_detail=str(exc),
            )
            connection.commit()
            return IngestionResult(
                source_type="google_doc",
                status="failed",
                detail=str(exc),
                run_id=ingestion_run_id,
            )

        skipped_docs = 0
        try:
            for doc in normalized_docs:
                if not doc.content.strip():
                    skipped_docs += 1
                    continue
                document_id = _upsert_document(connection, doc, ingestion_run_id=ingestion_run_id)
                chunk_count += _upsert_chunks(connection, document_id=document_id, doc=doc)
                document_count += 1
            status, detail, error_summary = _google_docs_run_outcome(
                fetched_docs=fetched_docs,
                document_count=document_count,
                chunk_count=chunk_count,
                skipped_docs=skipped_docs,
                import_detail=import_detail,
                target_db_path=target_db_path,
            )
            finish_ingest_run(
                connection,
                run_id=ingestion_run_id,
                status=status,
                counts=IngestRunCounts(
                    discovered=discovered_docs,
                    fetched=fetched_docs,
                    stored_documents=document_count,
                    stored_chunks=chunk_count,
                ),
                error_summary=error_summary,
                error_detail=detail if status != "completed" else None,
            )
            connection.commit()
            return IngestionResult(
                source_type="google_doc",
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
                counts=IngestRunCounts(discovered=discovered_docs, fetched=fetched_docs),
                error_summary="Failed while storing Google Docs ingestion results",
                error_detail=str(exc),
            )
            connection.commit()
            return IngestionResult(
                source_type="google_doc",
                status="failed",
                detail=str(exc),
                run_id=ingestion_run_id,
            )
    finally:
        connection.close()


def _load_doc_payloads(
    export_path: Path | None,
    *,
    live: GogDocsLiveOptions | None,
) -> LoadDocPayloadsResult:
    if live is not None:
        payloads, discovered_docs = _load_live_doc_payloads(live)
        if live.doc_ids:
            target = ", ".join(live.doc_ids)
            return LoadDocPayloadsResult(
                payloads=payloads,
                import_detail=f"live Google Docs via gog for doc ids [{target}]",
                discovered_docs=discovered_docs,
                fetched_docs=len(payloads),
            )
        account_list = ", ".join(live.accounts)
        return LoadDocPayloadsResult(
            payloads=payloads,
            import_detail=f"live Google Docs via gog for [{account_list}] with query {live.query!r}",
            discovered_docs=discovered_docs,
            fetched_docs=len(payloads),
        )

    if export_path is None:
        raise ValueError("A local export path is required when live Google Docs ingestion is not selected.")
    if not export_path.exists():
        raise ValueError(f"Path does not exist: {export_path}")

    json_files: list[Path]
    if export_path.is_dir():
        json_files = sorted(path for path in export_path.rglob("*.json") if path.is_file())
        payloads: list[dict[str, Any]] = []
        for path in json_files:
            payloads.extend(_load_doc_payload_file(path))
        return LoadDocPayloadsResult(
            payloads=payloads,
            import_detail=str(export_path),
            discovered_docs=len(payloads),
            fetched_docs=len(payloads),
        )

    if export_path.suffix.lower() != ".json":
        raise ValueError("Expected a .json file or a directory containing .json files.")
    payloads = _load_doc_payload_file(export_path)
    return LoadDocPayloadsResult(
        payloads=payloads,
        import_detail=str(export_path),
        discovered_docs=len(payloads),
        fetched_docs=len(payloads),
    )


def _load_live_doc_payloads(live: GogDocsLiveOptions) -> tuple[list[dict[str, Any]], int]:
    payloads: list[dict[str, Any]] = []
    discovered_docs = 0
    source = get_google_source()
    for account in live.accounts:
        try:
            doc_targets = (
                [(doc_id, None) for doc_id in live.doc_ids]
                if live.doc_ids
                else _discover_doc_ids(account=account, live=live, source=source)
            )
            discovered_docs += len(doc_targets)
            for doc_id, search_result in doc_targets:
                docs_info = source.docs_info(account=account, doc_id=doc_id)
                drive_file = source.drive_get(account=account, doc_id=doc_id)
                content_text = source.docs_cat(
                    account=account,
                    doc_id=doc_id,
                    max_bytes=live.max_bytes,
                    all_tabs=live.all_tabs,
                )
                payload = _wrap_live_doc_payload(
                    account=account,
                    query=live.query,
                    doc_id=doc_id,
                    search_result=search_result,
                    docs_info=docs_info,
                    drive_file=drive_file,
                    content_text=content_text,
                )
                payloads.append(payload)
                if live.cache_dir is not None:
                    _cache_live_doc_payload(
                        live.cache_dir,
                        payload=payload,
                        account=account,
                        doc_id=doc_id,
                    )
        except GoogleDocsLoadError:
            raise
        except ValueError as exc:
            raise GoogleDocsLoadError(
                str(exc),
                discovered_docs=discovered_docs,
                fetched_docs=len(payloads),
            ) from exc
    return payloads, discovered_docs


def _discover_doc_ids(
    account: str, *, live: GogDocsLiveOptions, source: GoogleWorkspaceSource
) -> list[tuple[str, dict[str, Any] | None]]:
    search_results = source.drive_search(
        account=account,
        query=live.query,
        max_docs=live.max_docs,
        raw_query=live.raw_query,
    )
    doc_targets: list[tuple[str, dict[str, Any] | None]] = []
    for result in search_results:
        doc_id = _doc_id_from_search_result(result)
        if not doc_id:
            raise GoogleDocsLoadError(
                f"gog drive search returned a result without a doc id for account {account}: {json.dumps(result, sort_keys=True)}",
                discovered_docs=len(doc_targets) + len(search_results),
            )
        doc_targets.append((doc_id, result))
    return doc_targets


def _load_doc_payload_file(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and payload.get("snapshot_type") == "gog_google_doc":
        payloads = [payload]
    elif isinstance(payload, dict) and isinstance(payload.get("documents"), list):
        payloads = payload["documents"]
    else:
        raise ValueError(f"{path} is not a supported YouOS Google Docs cache file. Only cached gog snapshot JSON is accepted for local Docs import.")

    if not all(isinstance(item, dict) for item in payloads):
        raise ValueError(f"{path} contains a malformed Google Docs payload list.")
    return list(payloads)


def _gog_drive_search(
    *,
    account: str,
    query: str,
    max_docs: int | None,
    raw_query: bool,
) -> list[dict[str, Any]]:
    command = [
        "gog",
        "drive",
        "search",
        query,
        "--account",
        account,
        "--json",
        "--results-only",
        "--no-input",
    ]
    if raw_query:
        command.append("--raw-query")
    if max_docs is not None:
        command.extend(["--max", str(max_docs)])

    payload = _run_gog_json(command)
    results = _coerce_list_payload(payload, command_name="gog drive search")
    if not all(isinstance(item, dict) for item in results):
        raise ValueError(f"gog drive search returned malformed results for account {account}.")
    return list(results)


def _gog_docs_info(*, account: str, doc_id: str) -> dict[str, Any]:
    command = [
        "gog",
        "docs",
        "info",
        doc_id,
        "--account",
        account,
        "--json",
        "--results-only",
        "--no-input",
    ]
    payload = _run_gog_json(command)
    if not isinstance(payload, dict):
        raise ValueError(f"gog docs info returned malformed JSON for doc {doc_id}.")
    return payload


def _gog_drive_get(*, account: str, doc_id: str) -> dict[str, Any]:
    command = [
        "gog",
        "drive",
        "get",
        doc_id,
        "--account",
        account,
        "--json",
        "--results-only",
        "--no-input",
    ]
    payload = _run_gog_json(command)
    if not isinstance(payload, dict):
        raise ValueError(f"gog drive get returned malformed JSON for doc {doc_id}.")
    return payload


def _gog_docs_cat(*, account: str, doc_id: str, max_bytes: int, all_tabs: bool) -> str:
    command = [
        "gog",
        "docs",
        "cat",
        doc_id,
        "--account",
        account,
        "--max-bytes",
        str(max_bytes),
        "--no-input",
    ]
    if all_tabs:
        command.append("--all-tabs")
    return _run_gog_text(command).strip()


def _run_gog_json(command: list[str]) -> Any:
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
    if completed.returncode != 0:
        error_detail = completed.stderr.strip() or completed.stdout.strip() or "unknown gog error"
        raise ValueError(_format_gog_error(command, error_detail))
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{' '.join(command)} returned invalid JSON: {exc}") from exc


def _run_gog_text(command: list[str]) -> str:
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
    if completed.returncode != 0:
        error_detail = completed.stderr.strip() or completed.stdout.strip() or "unknown gog error"
        raise ValueError(_format_gog_error(command, error_detail))
    return completed.stdout


def _format_gog_error(command: list[str], error_detail: str) -> str:
    command_text = " ".join(command)
    if _is_drive_api_disabled_error(error_detail):
        return (
            f"{command_text} failed: {error_detail}\n"
            "Google Drive API is not enabled for the gog project/environment, so live Google Docs "
            "ingestion cannot run. Enable the Drive API for gog or use cached YouOS Docs snapshots."
        )
    return f"{command_text} failed: {error_detail}"


def _is_drive_api_disabled_error(error_detail: str) -> bool:
    normalized = error_detail.lower()
    indicators = (
        "service_disabled",
        "accessnotconfigured",
        "google drive api has not been used",
        "drive api",
        "api has not been used in project",
    )
    return any(indicator in normalized for indicator in indicators)


def _coerce_list_payload(payload: Any, *, command_name: str) -> list[Any]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("files", "documents", "results", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    raise ValueError(f"{command_name} did not return a list payload.")


def _doc_id_from_search_result(result: dict[str, Any]) -> str | None:
    for field in ("docId", "doc_id", "documentId", "fileId", "file_id", "id"):
        value = _string(result.get(field))
        if value:
            return value

    for field in ("document", "doc", "file"):
        nested = result.get(field)
        if isinstance(nested, dict):
            for nested_field in ("docId", "doc_id", "documentId", "fileId", "file_id", "id"):
                value = _string(nested.get(nested_field))
                if value:
                    return value
    return None


def _wrap_live_doc_payload(
    *,
    account: str,
    query: str,
    doc_id: str,
    search_result: dict[str, Any] | None,
    docs_info: dict[str, Any],
    drive_file: dict[str, Any],
    content_text: str,
) -> dict[str, Any]:
    return {
        "snapshot_type": "gog_google_doc",
        "doc_id": doc_id,
        "account": account,
        "source": "gog_docs",
        "query": query,
        "fetched_at": datetime.now(tz=UTC).isoformat().replace("+00:00", "Z"),
        "search_result": search_result,
        "docs_info": docs_info,
        "drive_file": drive_file,
        "content_text": content_text,
    }


def _cache_live_doc_payload(
    cache_dir: Path,
    *,
    payload: dict[str, Any],
    account: str,
    doc_id: str,
) -> None:
    account_dir = cache_dir / _safe_path_component(account)
    account_dir.mkdir(parents=True, exist_ok=True)
    target_path = account_dir / f"{_safe_path_component(doc_id)}.json"
    target_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _google_docs_run_outcome(
    *,
    fetched_docs: int,
    document_count: int,
    chunk_count: int,
    skipped_docs: int,
    import_detail: str,
    target_db_path: Path,
) -> tuple[str, str, str | None]:
    base_detail = (
        f"Ingested {document_count} Google Doc(s) from {import_detail} into {target_db_path}. "
        f"Fetched {fetched_docs} payload(s) and stored {chunk_count} retrieval chunk(s). "
        "Metadata came from gog docs/drive adapters where available; missing owner or modified fields "
        "are preserved as documented gaps rather than synthesized."
    )
    if document_count == 0 or chunk_count == 0:
        return (
            "failed",
            f"{base_detail} YouOS fetched input but no useful Google Docs corpus rows landed.",
            "No useful Google Docs rows landed",
        )
    if skipped_docs > 0:
        return (
            "completed_with_warnings",
            f"{base_detail} Skipped {skipped_docs} doc(s) with empty content.",
            "Google Docs ingestion completed with warnings",
        )
    return "completed", base_detail, None


def _normalize_doc_payload(payload: dict[str, Any]) -> NormalizedGoogleDoc:
    doc_id = _doc_id_from_payload(payload)
    account_email = _normalize_email(_string(payload.get("account")))
    source_name = _string(payload.get("source")) or "gog_docs_cache"
    docs_info = _dict_or_empty(payload.get("docs_info"))
    drive_file = _dict_or_empty(payload.get("drive_file"))
    search_result = _dict_or_empty(payload.get("search_result"))

    metadata_sources = [docs_info, drive_file, search_result, payload]
    title = _first_string(metadata_sources, ("title", "name", "documentTitle", "docTitle"))
    external_uri = _first_string(
        metadata_sources,
        ("webViewLink", "documentUrl", "url", "link", "alternateLink"),
    )
    created_at = _first_timestamp(
        metadata_sources,
        ("createdTime", "created_at", "createdAt", "creationTime"),
    )
    updated_at = _first_timestamp(
        metadata_sources,
        ("modifiedTime", "modified_at", "modifiedAt", "updatedAt", "updateTime"),
    )
    owner = _primary_owner(drive_file, docs_info)
    owner_list = _owner_list(drive_file, docs_info)
    last_modifying_user = _display_person(_person_from_field(drive_file.get("lastModifyingUser")))
    content = _string(payload.get("content_text")) or ""

    metadata = {
        "doc_id": doc_id,
        "account_email": account_email,
        "source": source_name,
        "query": _string(payload.get("query")),
        "fetched_at": _normalize_timestamp(payload.get("fetched_at")),
        "owner": owner,
        "owners": owner_list,
        "last_modifying_user": last_modifying_user,
        "docs_info": docs_info,
        "drive_file": drive_file,
        "search_result": search_result,
        "missing_fields": _missing_fields(
            owner=owner,
            updated_at=updated_at,
            external_uri=external_uri,
        ),
    }

    return NormalizedGoogleDoc(
        doc_id=doc_id,
        account_email=account_email,
        source_name=source_name,
        title=title,
        author=owner,
        external_uri=external_uri,
        created_at=created_at,
        updated_at=updated_at,
        content=content,
        metadata=metadata,
    )


def _doc_id_from_payload(payload: dict[str, Any]) -> str:
    for field in ("doc_id", "docId", "documentId", "fileId", "file_id", "id"):
        value = _string(payload.get(field))
        if value:
            return value

    for field in ("docs_info", "drive_file", "search_result"):
        nested = payload.get(field)
        if isinstance(nested, dict):
            value = _doc_id_from_search_result(nested)
            if value:
                return value

    raise ValueError("A Google Docs payload is missing doc_id/docId/fileId/id.")


def _dict_or_empty(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _first_string(sources: list[dict[str, Any]], fields: tuple[str, ...]) -> str | None:
    for source in sources:
        for field in fields:
            value = _string(source.get(field))
            if value:
                return value
    return None


def _first_timestamp(sources: list[dict[str, Any]], fields: tuple[str, ...]) -> str | None:
    for source in sources:
        for field in fields:
            value = _normalize_timestamp(source.get(field))
            if value:
                return value
    return None


def _primary_owner(*sources: dict[str, Any]) -> str | None:
    owners = _owner_list(*sources)
    if owners:
        return owners[0]
    for source in sources:
        last_modifying_user = _display_person(_person_from_field(source.get("lastModifyingUser")))
        if last_modifying_user:
            return last_modifying_user
    return None


def _owner_list(*sources: dict[str, Any]) -> list[str]:
    owners: list[str] = []
    for source in sources:
        raw_owners = source.get("owners")
        if isinstance(raw_owners, list):
            for owner in raw_owners:
                display = _display_person(_person_from_field(owner))
                if display and display not in owners:
                    owners.append(display)

        raw_owner = source.get("owner")
        display = _display_person(_person_from_field(raw_owner))
        if display and display not in owners:
            owners.append(display)
    return owners


def _person_from_field(value: Any) -> tuple[str | None, str | None]:
    if isinstance(value, dict):
        name = _string(value.get("displayName")) or _string(value.get("name"))
        email = _normalize_email(_string(value.get("emailAddress")) or _string(value.get("email")))
        return name, email
    if isinstance(value, str):
        return value.strip() or None, None
    return None, None


def _display_person(person: tuple[str | None, str | None]) -> str | None:
    name, email = person
    if name and email:
        return f"{name} <{email}>"
    return name or email


def _missing_fields(*, owner: str | None, updated_at: str | None, external_uri: str | None) -> list[str]:
    missing: list[str] = []
    if owner is None:
        missing.append("owner")
    if updated_at is None:
        missing.append("updated_at")
    if external_uri is None:
        missing.append("external_uri")
    return missing


def _upsert_document(
    connection: sqlite3.Connection,
    doc: NormalizedGoogleDoc,
    *,
    ingestion_run_id: str,
) -> int:
    metadata_json = json.dumps(doc.metadata, sort_keys=True)
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
            external_uri = excluded.external_uri,
            created_at = excluded.created_at,
            updated_at = excluded.updated_at,
            content = excluded.content,
            metadata_json = excluded.metadata_json,
            ingestion_run_id = excluded.ingestion_run_id
        """,
        (
            "google_doc",
            doc.doc_id,
            doc.title,
            doc.author,
            doc.external_uri,
            None,
            doc.created_at,
            doc.updated_at,
            doc.content,
            metadata_json,
            ingestion_run_id,
        ),
    )
    row = connection.execute(
        "SELECT id FROM documents WHERE source_type = ? AND source_id = ?",
        ("google_doc", doc.doc_id),
    ).fetchone()
    if row is None:
        raise ValueError(f"Failed to load document id for Google Doc {doc.doc_id}")
    return int(row[0])


def _upsert_chunks(connection: sqlite3.Connection, *, document_id: int, doc: NormalizedGoogleDoc) -> int:
    chunks = _chunk_document_text(doc.content)
    for chunk_index, chunk_text in enumerate(chunks):
        metadata_json = json.dumps(
            {
                "doc_id": doc.doc_id,
                "account_email": doc.account_email,
                "source": doc.source_name,
                "chunk_role": "document_text",
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
                chunk_index,
                chunk_text,
                None,
                len(chunk_text),
                metadata_json,
            ),
        )
    return len(chunks)


def _chunk_document_text(content: str, *, max_chars: int = 2000) -> list[str]:
    text = content.strip()
    if not text:
        return []

    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]
    if not paragraphs:
        return [text]

    chunks: list[str] = []
    current_parts: list[str] = []
    current_length = 0

    for paragraph in paragraphs:
        paragraph_length = len(paragraph)
        if paragraph_length > max_chars:
            if current_parts:
                chunks.append("\n\n".join(current_parts))
                current_parts = []
                current_length = 0
            chunks.extend(_split_long_paragraph(paragraph, max_chars=max_chars))
            continue

        separator_length = 2 if current_parts else 0
        if current_parts and current_length + separator_length + paragraph_length > max_chars:
            chunks.append("\n\n".join(current_parts))
            current_parts = [paragraph]
            current_length = paragraph_length
            continue

        current_parts.append(paragraph)
        current_length += separator_length + paragraph_length

    if current_parts:
        chunks.append("\n\n".join(current_parts))
    return chunks


def _split_long_paragraph(paragraph: str, *, max_chars: int) -> list[str]:
    words = paragraph.split()
    if not words:
        return [paragraph]

    parts: list[str] = []
    current_words: list[str] = []
    current_length = 0
    for word in words:
        separator_length = 1 if current_words else 0
        if current_words and current_length + separator_length + len(word) > max_chars:
            parts.append(" ".join(current_words))
            current_words = [word]
            current_length = len(word)
            continue
        current_words.append(word)
        current_length += separator_length + len(word)

    if current_words:
        parts.append(" ".join(current_words))
    return parts


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


def _normalize_email(email: str | None) -> str | None:
    if not email:
        return None
    return email.strip().lower()


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


def _string(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return str(value)


def _safe_path_component(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_", "."} else "_" for char in value)


def _import_source_label(export_path: Path | None, *, live: GogDocsLiveOptions | None) -> str:
    if live is not None:
        if live.doc_ids:
            return f"live Google Docs via gog for doc ids {', '.join(live.doc_ids)}"
        return f"live Google Docs via gog for {', '.join(live.accounts)}"
    if export_path is None:
        return "<unknown>"
    return str(export_path)


def _default_sqlite_path() -> Path:
    database_url = os.getenv("YOUOS_DATABASE_URL", "sqlite:///var/youos.db")
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        raise ValueError("Only sqlite:/// database URLs are supported for Google Docs ingestion.")
    return Path(database_url.removeprefix(prefix))
