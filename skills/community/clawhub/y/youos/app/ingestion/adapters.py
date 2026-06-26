"""Pluggable Google Workspace data sources for ingestion.

Gmail-thread and Google-Doc ingestion fetch their raw data through a
backend-agnostic :class:`GoogleWorkspaceSource`, so YouOS can decouple from the
OpenClaw ``gog`` CLI. Implementations:

- :class:`GogSource` — the OpenClaw ``gog`` CLI (default; zero behavior change).
- :class:`GwsSource` — Google's own open-source Workspace CLI ``gws``
  (single-account, JSON-by-default, ``gws <service> <resource> <method>
  --params '{...}'``).
- :class:`NativeSource` — a direct Google-API client
  (``google-api-python-client`` + ``google-auth-oauthlib``, the
  ``youos[google]`` extra), no external CLI; multi-account via per-account
  OAuth tokens.

Each method returns the **canonical payload** the ingestion normalizers already
consume (``_normalize_thread_payload`` / ``_wrap_live_doc_payload`` etc.) —
today that shape *is* what ``gog --json`` emits. Future backends satisfy the
same contract by mapping their responses onto it; ``GogSource`` satisfies it by
construction.

The active backend is selected by ``ingestion.google_backend`` in
``youos_config.yaml`` and defaults to ``gog`` so existing instances are
unchanged.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from app.core.config import get_ingestion_google_backend

logger = logging.getLogger(__name__)

SUPPORTED_BACKENDS = ("gog", "gws", "native")

# --- gws (Google Workspace CLI) transport tunables ------------------------
# Hard per-call cap so a stalled `gws` (auth prompt, token refresh, network)
# can't hang ingestion forever — mirrors the gog backend's GOG_TIMEOUT_SECONDS.
GWS_TIMEOUT_SECONDS = 120
# Same rate-limit backoff philosophy as the gog backend.
_GWS_BACKOFF_SECONDS = (2, 4, 8, 16)

# --- shared Google-API shaping (gws + native) -----------------------------
# Search-page size for Gmail threads.list pagination.
_THREAD_PAGE_SIZE = 50
# Drive file fields the docs normalizer reads (title/uri/timestamps/owner).
_DRIVE_FILE_FIELDS = (
    "id,name,mimeType,webViewLink,createdTime,modifiedTime,"
    "owners(displayName,emailAddress),lastModifyingUser(displayName,emailAddress)"
)
# OAuth scopes the native backend requests (read-only ingestion).
_NATIVE_SCOPES = (
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents.readonly",
)


def _build_drive_query(query: str, *, raw_query: bool) -> str:
    """Drive ``q`` for a docs search. Raw passes through; otherwise full-text,
    restricted to Google Docs (this is the Docs importer)."""
    if raw_query:
        return query
    escaped = query.replace("\\", "\\\\").replace("'", "\\'")
    return f"fullText contains '{escaped}' and mimeType = 'application/vnd.google-apps.document'"


def _truncate_text_bytes(text: str, max_bytes: int) -> str:
    """Truncate to ``max_bytes`` UTF-8 bytes (0/falsey = no limit), then strip."""
    if max_bytes and len(text.encode("utf-8")) > max_bytes:
        text = text.encode("utf-8")[:max_bytes].decode("utf-8", errors="ignore")
    return text.strip()


@runtime_checkable
class GoogleWorkspaceSource(Protocol):
    """Backend that fetches Gmail threads and Google Docs for ingestion."""

    name: str

    # --- Gmail ---
    def search_threads(self, *, account: str, query: str, max_threads: int | None) -> list[dict[str, Any]]:
        """Return search-result dicts (each carrying an extractable thread id)."""
        ...

    def get_thread(self, *, account: str, thread_id: str) -> dict[str, Any]:
        """Return the canonical normalized thread payload for ``thread_id``."""
        ...

    # --- Google Docs / Drive ---
    def drive_search(self, *, account: str, query: str, max_docs: int | None, raw_query: bool) -> list[dict[str, Any]]:
        """Return Drive search-result dicts (each carrying an extractable doc id)."""
        ...

    def docs_info(self, *, account: str, doc_id: str) -> dict[str, Any]:
        """Return Docs metadata for ``doc_id``."""
        ...

    def drive_get(self, *, account: str, doc_id: str) -> dict[str, Any]:
        """Return Drive file metadata for ``doc_id``."""
        ...

    def docs_cat(self, *, account: str, doc_id: str, max_bytes: int, all_tabs: bool) -> str:
        """Return the plain-text content of the Doc ``doc_id``."""
        ...


class GogSource:
    """Backend backed by the OpenClaw ``gog`` CLI.

    A thin delegating wrapper over the existing ``_gog_*`` helpers in
    ``gmail_threads`` / ``google_docs``; the subprocess transport, rate-limit
    retry and gog-shape normalization stay in those modules untouched, so this
    is behavior-preserving. The delegated imports are function-local because
    those modules import this one — a module-level import would cycle.
    """

    name = "gog"

    def search_threads(self, *, account: str, query: str, max_threads: int | None) -> list[dict[str, Any]]:
        from app.ingestion.gmail_threads import _gog_search_threads

        return _gog_search_threads(account=account, query=query, max_threads=max_threads)

    def get_thread(self, *, account: str, thread_id: str) -> dict[str, Any]:
        from app.ingestion.gmail_threads import _gog_get_thread

        return _gog_get_thread(account=account, thread_id=thread_id)

    def drive_search(self, *, account: str, query: str, max_docs: int | None, raw_query: bool) -> list[dict[str, Any]]:
        from app.ingestion.google_docs import _gog_drive_search

        return _gog_drive_search(account=account, query=query, max_docs=max_docs, raw_query=raw_query)

    def docs_info(self, *, account: str, doc_id: str) -> dict[str, Any]:
        from app.ingestion.google_docs import _gog_docs_info

        return _gog_docs_info(account=account, doc_id=doc_id)

    def drive_get(self, *, account: str, doc_id: str) -> dict[str, Any]:
        from app.ingestion.google_docs import _gog_drive_get

        return _gog_drive_get(account=account, doc_id=doc_id)

    def docs_cat(self, *, account: str, doc_id: str, max_bytes: int, all_tabs: bool) -> str:
        from app.ingestion.google_docs import _gog_docs_cat

        return _gog_docs_cat(account=account, doc_id=doc_id, max_bytes=max_bytes, all_tabs=all_tabs)


def _load_gws_credentials() -> dict[str, str]:
    """Optional per-account credentials map from ``ingestion.gws_credentials``.

    ``gws`` is single-account per credential (no per-command ``--account`` like
    ``gog``). To bridge YouOS's multi-account ingestion loop, an instance may
    map each ingestion account to a gws credentials file; the adapter sets
    ``GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE`` per call. With no mapping the
    ambient gws credentials (env / default login) are used as-is.
    """
    try:
        from app.core.config import load_config

        cfg = load_config() or {}
        ingestion = cfg.get("ingestion", {}) if isinstance(cfg, dict) else {}
        creds = ingestion.get("gws_credentials", {}) if isinstance(ingestion, dict) else {}
        if isinstance(creds, dict):
            return {str(k): str(v) for k, v in creds.items()}
    except Exception:  # never let a config hiccup break source construction
        logger.debug("Could not read ingestion.gws_credentials", exc_info=True)
    return {}


def _unwrap_gws_envelope(raw: Any) -> Any:
    """Drill through a possible ``{result|data|response: {...}}`` wrapper.

    ``gws`` emits structured JSON; whether it wraps the Google resource in an
    envelope is version-dependent, so we defensively descend a few common
    wrapper keys. Google resources themselves never use these as top-level
    keys (threads/messages/files nest their data under their own keys), so this
    is a no-op when ``gws`` returns the bare resource.
    """
    cur = raw
    for _ in range(4):
        if not isinstance(cur, dict):
            break
        for wrapper in ("result", "data", "response"):
            nested = cur.get(wrapper)
            if isinstance(nested, dict):
                cur = nested
                break
        else:
            break
    return cur


def _docs_document_to_text(document: dict[str, Any], *, all_tabs: bool) -> str:
    """Flatten a Docs API ``documents.get`` resource to plain text.

    Walks paragraph ``textRun`` content. Honors the tabs feature: with
    ``all_tabs`` every tab's body is concatenated; otherwise the top-level body
    (falling back to the first tab for tabs-only documents).
    """

    def walk_body(body: dict[str, Any]) -> str:
        out: list[str] = []
        for element in body.get("content", []) or []:
            if not isinstance(element, dict):
                continue
            paragraph = element.get("paragraph")
            if not isinstance(paragraph, dict):
                continue
            for pe in paragraph.get("elements", []) or []:
                if not isinstance(pe, dict):
                    continue
                text_run = pe.get("textRun")
                if isinstance(text_run, dict):
                    content = text_run.get("content")
                    if isinstance(content, str):
                        out.append(content)
        return "".join(out)

    tabs = document.get("tabs")
    bodies: list[str] = []
    if all_tabs and isinstance(tabs, list) and tabs:
        for tab in tabs:
            doc_tab = tab.get("documentTab") if isinstance(tab, dict) else None
            if isinstance(doc_tab, dict) and isinstance(doc_tab.get("body"), dict):
                bodies.append(walk_body(doc_tab["body"]))
    else:
        body = document.get("body")
        if isinstance(body, dict):
            bodies.append(walk_body(body))
        elif isinstance(tabs, list) and tabs:
            doc_tab = tabs[0].get("documentTab") if isinstance(tabs[0], dict) else None
            if isinstance(doc_tab, dict) and isinstance(doc_tab.get("body"), dict):
                bodies.append(walk_body(doc_tab["body"]))

    return "\n".join(b.strip() for b in bodies if b.strip())


class GwsSource:
    """Backend backed by Google's own Workspace CLI, ``gws``.

    ``gws`` (github.com/googleworkspace/cli) is dynamically generated from
    Google's Discovery Service, so its command surface mirrors the Google API
    method paths (``gws gmail users threads get --params '{...}'``) and it emits
    structured JSON by default. Because the Gmail normalizer already consumes
    the raw Gmail API message shape, the Gmail path is almost identity: we hand
    the threads.get resource straight to ``_normalize_gog_thread_payload`` (its
    unwrap/thread-id logic is backend-agnostic). Docs go through Drive
    ``files.get`` (metadata) + Docs ``documents.get`` (text).

    Command names follow the Google API method paths; if a future ``gws``
    Discovery rendering differs, they are all localized to this class.
    Live ingestion is verified on a real instance (the container has no
    authenticated ``gws``).
    """

    name = "gws"

    def __init__(self, *, credentials: dict[str, str] | None = None) -> None:
        self._credentials = credentials if credentials is not None else _load_gws_credentials()
        # Avoid re-fetching documents.get for both docs_info and docs_cat.
        self._doc_cache: dict[str, dict[str, Any]] = {}

    # --- transport ---------------------------------------------------------
    def _run_json(self, args: list[str], *, account: str | None, params: dict[str, Any]) -> Any:
        command = ["gws", *args, "--params", json.dumps(params, separators=(",", ":"))]
        env = os.environ.copy()
        creds = self._credentials.get(account) if account else None
        if creds:
            env["GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE"] = str(creds)

        last_error = ""
        from app.ingestion.gmail_threads import _looks_like_rate_limit

        for backoff in (*_GWS_BACKOFF_SECONDS, None):
            try:
                completed = subprocess.run(
                    command,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=GWS_TIMEOUT_SECONDS,
                    env=env,
                )
            except subprocess.TimeoutExpired as exc:
                raise ValueError(f"{' '.join(command)} timed out after {GWS_TIMEOUT_SECONDS}s") from exc

            if completed.returncode == 0:
                try:
                    return _unwrap_gws_envelope(json.loads(completed.stdout))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{' '.join(command)} returned invalid JSON: {exc}") from exc

            error_detail = completed.stderr.strip() or completed.stdout.strip() or "unknown gws error"
            last_error = error_detail
            if not _looks_like_rate_limit(error_detail) or backoff is None:
                raise ValueError(f"{' '.join(command)} failed: {error_detail}")
            time.sleep(backoff)

        raise ValueError(f"{' '.join(command)} failed after retries: {last_error}")

    # --- Gmail -------------------------------------------------------------
    def search_threads(self, *, account: str, query: str, max_threads: int | None) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        page_token: str | None = None
        while True:
            params: dict[str, Any] = {"userId": "me", "q": query, "maxResults": _THREAD_PAGE_SIZE}
            if page_token:
                params["pageToken"] = page_token
            payload = self._run_json(["gmail", "users", "threads", "list"], account=account, params=params)

            threads = payload.get("threads") if isinstance(payload, dict) else None
            if not isinstance(threads, list):
                threads = []
            results.extend(item for item in threads if isinstance(item, dict))

            if max_threads is not None and len(results) >= max_threads:
                return results[:max_threads]

            page_token = payload.get("nextPageToken") if isinstance(payload, dict) else None
            if not page_token or not threads:
                return results
            time.sleep(1.5)  # pace between pages, like the gog backend

    def get_thread(self, *, account: str, thread_id: str) -> dict[str, Any]:
        from app.ingestion.gmail_threads import _normalize_gog_thread_payload

        payload = self._run_json(
            ["gmail", "users", "threads", "get"],
            account=account,
            params={"userId": "me", "id": thread_id, "format": "full"},
        )
        if not isinstance(payload, dict):
            raise ValueError(f"gws gmail threads get returned malformed JSON for thread {thread_id}.")
        # The Gmail-API thread shape is exactly what the normalizer consumes.
        return _normalize_gog_thread_payload(payload, requested_thread_id=thread_id)

    # --- Drive / Docs ------------------------------------------------------
    def drive_search(self, *, account: str, query: str, max_docs: int | None, raw_query: bool) -> list[dict[str, Any]]:
        drive_q = _build_drive_query(query, raw_query=raw_query)
        results: list[dict[str, Any]] = []
        page_token: str | None = None
        page_size = 100
        while True:
            params: dict[str, Any] = {
                "q": drive_q,
                "pageSize": page_size,
                "fields": "files(id,name,mimeType,webViewLink),nextPageToken",
            }
            if page_token:
                params["pageToken"] = page_token
            payload = self._run_json(["drive", "files", "list"], account=account, params=params)

            files = payload.get("files") if isinstance(payload, dict) else None
            if not isinstance(files, list):
                files = []
            results.extend(item for item in files if isinstance(item, dict))

            if max_docs is not None and len(results) >= max_docs:
                return results[:max_docs]

            page_token = payload.get("nextPageToken") if isinstance(payload, dict) else None
            if not page_token or not files:
                return results
            time.sleep(1.0)

    def _document_get(self, *, account: str, doc_id: str) -> dict[str, Any]:
        cached = self._doc_cache.get(doc_id)
        if cached is not None:
            return cached
        payload = self._run_json(
            ["docs", "documents", "get"],
            account=account,
            params={"documentId": doc_id},
        )
        if not isinstance(payload, dict):
            raise ValueError(f"gws docs documents get returned malformed JSON for doc {doc_id}.")
        self._doc_cache[doc_id] = payload
        return payload

    def docs_info(self, *, account: str, doc_id: str) -> dict[str, Any]:
        document = self._document_get(account=account, doc_id=doc_id)
        # Keep it light — the full body lives in content_text, not metadata.
        return {"documentId": doc_id, "title": document.get("title")}

    def drive_get(self, *, account: str, doc_id: str) -> dict[str, Any]:
        payload = self._run_json(
            ["drive", "files", "get"],
            account=account,
            params={"fileId": doc_id, "fields": _DRIVE_FILE_FIELDS},
        )
        if not isinstance(payload, dict):
            raise ValueError(f"gws drive files get returned malformed JSON for doc {doc_id}.")
        return payload

    def docs_cat(self, *, account: str, doc_id: str, max_bytes: int, all_tabs: bool) -> str:
        document = self._document_get(account=account, doc_id=doc_id)
        return _truncate_text_bytes(_docs_document_to_text(document, all_tabs=all_tabs), max_bytes)


_GOOGLE_EXTRA_HINT = "The 'native' ingestion backend needs the google extra: pip install youos[google]"


def _native_config() -> dict[str, Any]:
    try:
        from app.core.config import load_config

        cfg = load_config() or {}
        ingestion = cfg.get("ingestion", {}) if isinstance(cfg, dict) else {}
        return ingestion if isinstance(ingestion, dict) else {}
    except Exception:
        logger.debug("Could not read ingestion config for native backend", exc_info=True)
        return {}


class NativeSource:
    """Backend backed by the Google API directly — no external CLI.

    Uses ``google-api-python-client`` + ``google-auth-oauthlib`` (the
    ``youos[google]`` extra). Per-account OAuth tokens are stored under the
    instance dir, so this is naturally multi-account (unlike ``gws``). The
    response shaping is identical to :class:`GwsSource` — both speak the raw
    Google API — so it reuses ``_normalize_gog_thread_payload`` and
    ``_docs_document_to_text``.

    Google libraries are imported lazily inside methods, so importing this
    module (and the base ``youos`` install) never requires the extra. First-run
    authorization is interactive (:meth:`authorize_account`) and is run on a
    real instance; the container has no browser/OAuth, so methods here are
    unit-tested against a mocked service.
    """

    name = "native"

    def __init__(self, *, token_dir: str | Path | None = None, client_secrets_path: str | None = None) -> None:
        self._token_dir_override = Path(token_dir) if token_dir else None
        self._client_secrets_override = client_secrets_path
        self._services: dict[tuple[str, str, str], Any] = {}
        self._doc_cache: dict[str, dict[str, Any]] = {}

    # --- auth / clients ----------------------------------------------------
    def _token_dir(self) -> Path:
        if self._token_dir_override is not None:
            return self._token_dir_override
        configured = _native_config().get("google_token_dir")
        if isinstance(configured, str) and configured.strip():
            return Path(configured).expanduser()
        from app.core.settings import get_instance_root

        return get_instance_root() / "var" / "google_tokens"

    def _token_path(self, account: str) -> Path:
        safe = account.replace("/", "_").replace("\\", "_")
        return self._token_dir() / f"{safe}.json"

    def _client_secrets(self) -> str:
        if self._client_secrets_override:
            return self._client_secrets_override
        configured = _native_config().get("google_oauth_client_secrets")
        if isinstance(configured, str) and configured.strip():
            return configured
        raise RuntimeError(
            "Set `ingestion.google_oauth_client_secrets` to your Google OAuth client JSON to use the native backend."
        )

    def _load_credentials(self, account: str) -> Any:
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
        except ImportError as exc:
            raise RuntimeError(_GOOGLE_EXTRA_HINT) from exc

        token_path = self._token_path(account)
        if not token_path.exists():
            raise RuntimeError(
                f"No stored Google credentials for {account!r} at {token_path}. "
                "Authorize first (youos setup, or NativeSource.authorize_account)."
            )
        creds = Credentials.from_authorized_user_file(str(token_path), scopes=list(_NATIVE_SCOPES))
        if not creds.valid:
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                token_path.write_text(creds.to_json(), encoding="utf-8")
            else:
                raise RuntimeError(f"Stored Google credentials for {account!r} are invalid; re-authorize.")
        return creds

    def _service(self, account: str, api: str, version: str) -> Any:
        key = (account, api, version)
        svc = self._services.get(key)
        if svc is None:
            try:
                from googleapiclient.discovery import build
            except ImportError as exc:
                raise RuntimeError(_GOOGLE_EXTRA_HINT) from exc
            svc = build(api, version, credentials=self._load_credentials(account), cache_discovery=False)
            self._services[key] = svc
        return svc

    def authorize_account(self, account: str, *, client_secrets_path: str | None = None) -> Path:
        """Run the interactive OAuth flow for ``account`` and store its token.

        Interactive (opens a browser) — invoked on a real instance, not in
        tests. Returns the path the token was written to.
        """
        try:
            from google_auth_oauthlib.flow import InstalledAppFlow
        except ImportError as exc:
            raise RuntimeError(_GOOGLE_EXTRA_HINT) from exc

        secrets = client_secrets_path or self._client_secrets()
        flow = InstalledAppFlow.from_client_secrets_file(secrets, scopes=list(_NATIVE_SCOPES))
        creds = flow.run_local_server(port=0)
        token_path = self._token_path(account)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json(), encoding="utf-8")
        return token_path

    # --- Gmail -------------------------------------------------------------
    def search_threads(self, *, account: str, query: str, max_threads: int | None) -> list[dict[str, Any]]:
        service = self._service(account, "gmail", "v1")
        results: list[dict[str, Any]] = []
        page_token: str | None = None
        while True:
            resp = (
                service.users()
                .threads()
                .list(userId="me", q=query, maxResults=_THREAD_PAGE_SIZE, pageToken=page_token)
                .execute()
            )
            threads = resp.get("threads") if isinstance(resp, dict) else None
            if not isinstance(threads, list):
                threads = []
            results.extend(item for item in threads if isinstance(item, dict))

            if max_threads is not None and len(results) >= max_threads:
                return results[:max_threads]

            page_token = resp.get("nextPageToken") if isinstance(resp, dict) else None
            if not page_token or not threads:
                return results

    def get_thread(self, *, account: str, thread_id: str) -> dict[str, Any]:
        from app.ingestion.gmail_threads import _normalize_gog_thread_payload

        service = self._service(account, "gmail", "v1")
        payload = service.users().threads().get(userId="me", id=thread_id, format="full").execute()
        if not isinstance(payload, dict):
            raise ValueError(f"native gmail threads get returned malformed payload for thread {thread_id}.")
        return _normalize_gog_thread_payload(payload, requested_thread_id=thread_id)

    # --- Drive / Docs ------------------------------------------------------
    def drive_search(self, *, account: str, query: str, max_docs: int | None, raw_query: bool) -> list[dict[str, Any]]:
        service = self._service(account, "drive", "v3")
        drive_q = _build_drive_query(query, raw_query=raw_query)
        results: list[dict[str, Any]] = []
        page_token: str | None = None
        while True:
            resp = (
                service.files()
                .list(
                    q=drive_q,
                    pageSize=100,
                    pageToken=page_token,
                    fields="files(id,name,mimeType,webViewLink),nextPageToken",
                )
                .execute()
            )
            files = resp.get("files") if isinstance(resp, dict) else None
            if not isinstance(files, list):
                files = []
            results.extend(item for item in files if isinstance(item, dict))

            if max_docs is not None and len(results) >= max_docs:
                return results[:max_docs]

            page_token = resp.get("nextPageToken") if isinstance(resp, dict) else None
            if not page_token or not files:
                return results

    def _document_get(self, *, account: str, doc_id: str) -> dict[str, Any]:
        cached = self._doc_cache.get(doc_id)
        if cached is not None:
            return cached
        service = self._service(account, "docs", "v1")
        payload = service.documents().get(documentId=doc_id).execute()
        if not isinstance(payload, dict):
            raise ValueError(f"native docs documents get returned malformed payload for doc {doc_id}.")
        self._doc_cache[doc_id] = payload
        return payload

    def docs_info(self, *, account: str, doc_id: str) -> dict[str, Any]:
        document = self._document_get(account=account, doc_id=doc_id)
        return {"documentId": doc_id, "title": document.get("title")}

    def drive_get(self, *, account: str, doc_id: str) -> dict[str, Any]:
        service = self._service(account, "drive", "v3")
        payload = service.files().get(fileId=doc_id, fields=_DRIVE_FILE_FIELDS).execute()
        if not isinstance(payload, dict):
            raise ValueError(f"native drive files get returned malformed payload for doc {doc_id}.")
        return payload

    def docs_cat(self, *, account: str, doc_id: str, max_bytes: int, all_tabs: bool) -> str:
        document = self._document_get(account=account, doc_id=doc_id)
        return _truncate_text_bytes(_docs_document_to_text(document, all_tabs=all_tabs), max_bytes)


def get_google_source(backend: str | None = None) -> GoogleWorkspaceSource:
    """Return the configured Google Workspace ingestion backend.

    ``backend`` overrides the configured value (handy for tests). When omitted
    it reads ``ingestion.google_backend`` (default ``gog``). An unrecognized
    explicit override raises :class:`ValueError`. (The ``native`` backend needs
    the ``youos[google]`` extra; that's enforced lazily when its methods run,
    not at construction.)
    """
    name = (backend or get_ingestion_google_backend()).strip().lower()
    if name == "gog":
        return GogSource()
    if name == "gws":
        return GwsSource()
    if name == "native":
        return NativeSource()
    raise ValueError(
        f"Unknown ingestion.google_backend {name!r}; expected one of {', '.join(SUPPORTED_BACKENDS)}."
    )
