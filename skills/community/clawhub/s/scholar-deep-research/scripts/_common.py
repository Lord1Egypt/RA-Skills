"""Shared helpers for every scholar-deep-research script.

Provides:
  - USER_AGENT             polite-pool identifier for HTTP calls
  - EXIT_*                 stable, differentiated exit codes for agents/orchestrators
  - ok() / err()           unified stdout envelope
  - UpstreamError          typed exception for HTTP/API failures
  - make_paper / make_payload / emit   search-script normalization helpers

Envelope contract:
  success → {"ok": true, "data": <any>, ...}
  failure → {"ok": false, "error": {"code": str, "message": str,
                                    "retryable": bool, ...}}

Every script must print exactly one envelope to stdout and exit with one of
the EXIT_* codes. Diagnostics go to stderr. No prose on stdout, ever.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

# Canonical version string. Bump in lockstep with the `version` field in
# SKILL.md frontmatter so USER_AGENT, telemetry, and skill metadata agree.
VERSION = "0.5.0"

USER_AGENT = (
    f"scholar-deep-research/{VERSION} "
    "(+https://github.com/Agents365-ai/scholar-deep-research; "
    "polite-pool)"
)

# ---------- exit codes ----------
# Stable across versions. Documented in SKILL.md.
EXIT_OK = 0          # success
EXIT_RUNTIME = 1     # runtime / API logic error (e.g. malformed upstream response)
EXIT_UPSTREAM = 2    # upstream / network error (retryable)
EXIT_VALIDATION = 3  # bad input: missing flag, bad value, whitelist violation
EXIT_STATE = 4       # state file missing, corrupt, or schema mismatch


# ---------- TTY detection ----------

def stdout_is_tty() -> bool:
    """True if stdout is an interactive terminal.

    Scripts use this to pick a human-friendly default (raw text, tables)
    vs. an agent-friendly default (JSON envelope). Orchestrators that
    want the agent format regardless of terminal can pipe stdout, or
    pass an explicit `--format json` / `--output <file>` flag.
    """
    try:
        return sys.stdout.isatty()
    except (AttributeError, ValueError):
        return False


# ---------- auto-populated envelope metadata ----------
#
# Every ok()/err() envelope carries a `meta` block with:
#   - request_id: uuid-derived, stable for the life of this process. An
#     orchestrator may override via the SCHOLAR_REQUEST_ID env var to
#     correlate envelopes with its own trace.
#   - latency_ms: monotonic wall-clock since module load (process start).
#     Useful for SLO tracking even without external instrumentation.
#   - cli_version: canonical VERSION constant so an agent can detect
#     drift against a cached schema (Principle 6).
#   - schema_version: envelope schema version (not CLI version). Bumped
#     when the envelope shape changes.

_START_MONO = time.monotonic()
_REQUEST_ID = (
    os.environ.get("SCHOLAR_REQUEST_ID")
    or f"req_{uuid.uuid4().hex[:10]}"
)


def _auto_meta() -> dict[str, Any]:
    # Referenced at call time, so the ordering against SCHEMA_VERSION's
    # later definition is fine — Python resolves module globals lazily.
    return {
        "request_id": _REQUEST_ID,
        "latency_ms": int((time.monotonic() - _START_MONO) * 1000),
        "cli_version": VERSION,
        "schema_version": SCHEMA_VERSION,
    }


# ---------- envelope helpers ----------

def ok(data: Any = None, *, meta: dict[str, Any] | None = None,
       **extra: Any) -> None:
    """Print a success envelope to stdout.

    Does not exit. Caller returns normally (implicit exit 0).
    The `meta` block is auto-populated with request_id, latency_ms,
    cli_version, and schema_version; caller-supplied `meta` entries win
    on key conflict so a caller can override any of them if needed.
    """
    merged_meta = _auto_meta()
    if meta is not None:
        merged_meta.update(meta)
    payload: dict[str, Any] = {"ok": True}
    if data is not None:
        payload["data"] = data
    payload["meta"] = merged_meta
    payload.update(extra)
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def err(code: str, message: str, *, retryable: bool = False,
        exit_code: int = EXIT_RUNTIME, **ctx: Any) -> None:
    """Print an error envelope to stdout and exit with `exit_code`.

    `code` is a stable snake_case routing key (e.g. "state_not_found",
    "upstream_error"). `message` is the human-readable sentence. `retryable`
    signals whether calling the exact same command again may succeed. Any
    additional kwargs become extra fields on the error object (e.g. `field`,
    `source`, `allowed`). The top-level envelope carries auto-populated
    `meta` for correlation.
    """
    error: dict[str, Any] = {
        "code": code,
        "message": message,
        "retryable": retryable,
    }
    error.update(ctx)
    json.dump({"ok": False, "error": error, "meta": _auto_meta()},
              sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    sys.exit(exit_code)


class UpstreamError(Exception):
    """HTTP/API failure raised from inside a search function.

    The search script's main() catches this and calls err() so the agent sees
    a structured failure envelope rather than a silent empty result.
    """

    def __init__(self, source: str, message: str, *,
                 retryable: bool = True,
                 exit_code: int = EXIT_UPSTREAM,
                 status: int | None = None) -> None:
        super().__init__(message)
        self.source = source
        self.message = message
        self.retryable = retryable
        self.exit_code = exit_code
        self.status = status

# Fields that every normalized paper should have (None if unknown).
PAPER_FIELDS = (
    "doi", "title", "authors", "year", "venue", "abstract",
    "citations", "url", "pdf_url",
    "openalex_id", "arxiv_id", "pmid",
)


def make_paper(**kwargs: Any) -> dict[str, Any]:
    """Build a paper dict with all standard fields, missing → None."""
    p: dict[str, Any] = {f: None for f in PAPER_FIELDS}
    p.update({k: v for k, v in kwargs.items() if v is not None})
    # type discipline
    if p.get("authors") and not isinstance(p["authors"], list):
        p["authors"] = [p["authors"]]
    if p.get("year"):
        try:
            p["year"] = int(p["year"])
        except (TypeError, ValueError):
            p["year"] = None
    if p.get("citations") is not None:
        try:
            p["citations"] = int(p["citations"])
        except (TypeError, ValueError):
            p["citations"] = 0
    return p


def make_payload(source: str, query: str, round_: int,
                 papers: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "source": source,
        "query": query,
        "round": round_,
        "papers": papers,
    }


def emit(payload: dict[str, Any], output: str | None,
         state: str | None) -> None:
    """Write search payload to --output JSON and/or hand to research_state ingest.

    Always prints exactly one envelope to stdout:
      - with --state: envelope from apply_ingest() (routed through the state lock)
      - with --output only: {"ok": true, "data": {"output": path, "count": N, ...}}
      - with neither: {"ok": true, "data": <payload>}
    """
    if output:
        out_path = Path(output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))

    if state:
        # Call apply_ingest directly — no subprocess, no shared temp file.
        # Concurrent searches are serialized by the state lock inside
        # apply_ingest, so Phase 1 fanout is race-free.
        # Lazy import avoids a circular dependency at module load.
        from research_state import apply_ingest
        summary = apply_ingest(Path(state), payload)
        ok(summary)
        return

    if output:
        ok({
            "output": str(output),
            "source": payload.get("source"),
            "query": payload.get("query"),
            "round": payload.get("round"),
            "count": len(payload.get("papers", [])),
        })
        return

    # Neither --output nor --state: dump the whole payload, enveloped.
    ok(payload)


def reconstruct_inverted_abstract(idx: dict[str, list[int]] | None) -> str | None:
    """OpenAlex returns abstracts as inverted indexes; reconstruct flat text."""
    if not idx:
        return None
    positions: list[tuple[int, str]] = []
    for word, locs in idx.items():
        for loc in locs:
            positions.append((loc, word))
    positions.sort()
    return " ".join(w for _, w in positions) or None


# ---------- schema introspection ----------

SCHEMA_VERSION = 1

# Stable exit-code vocabulary, shared by every script. The schema response
# includes this so agents can route on code without reading SKILL.md.
EXIT_CODE_VOCAB: dict[str, str] = {
    "0": "success",
    "1": "runtime error (e.g. malformed upstream response, missing dependency)",
    "2": "upstream / network error (retryable)",
    "3": "validation error (bad input)",
    "4": "state error (missing, corrupt, or schema mismatch)",
}


def _action_type_name(action: argparse.Action) -> str:
    """Map an argparse action to a JSON-schema-ish type name."""
    if isinstance(action, (argparse._StoreTrueAction,
                           argparse._StoreFalseAction)):
        return "boolean"
    t = action.type
    if t is int:
        return "integer"
    if t is float:
        return "number"
    if t is None or t is str:
        return "string"
    return getattr(t, "__name__", str(t))


def set_command_meta(parser: argparse.ArgumentParser, **meta: Any) -> None:
    """Attach schema metadata to a parser or subparser.

    Supported keys (all optional):
      since:        first version the command appeared in (e.g. "0.4.0")
      deprecated:   True if the command is on the deprecation path
      replaced_by:  name of the command that supersedes this one
      dangerous:    True for destructive commands (init --force, etc.)
      tier:         "read" | "write" | "destructive" (for safety UIs)

    Surfaced in `--schema` output under each subcommand's `meta` field.
    Agents with a cached schema compare `since` / `deprecated` against
    their local copy to detect drift before calling a renamed method.
    """
    parser._schema_meta = dict(meta)  # type: ignore[attr-defined]


def _parser_to_schema(parser: argparse.ArgumentParser,
                      command: str) -> dict[str, Any]:
    """Walk an argparse parser into a JSON-serializable schema.

    Subparsers recurse into `subcommands`. Positional arguments are emitted
    alongside flags — every agent-visible parameter the command accepts.
    """
    params: dict[str, Any] = {}
    subcommands: dict[str, Any] = {}

    for action in parser._actions:
        if isinstance(action, argparse._HelpAction):
            continue
        if isinstance(action, argparse._SubParsersAction):
            for subname, subparser in action.choices.items():
                subcommands[subname] = _parser_to_schema(
                    subparser, f"{command} {subname}")
            continue

        dest = action.dest
        entry: dict[str, Any] = {
            "type": _action_type_name(action),
            "required": bool(action.required),
        }
        if action.option_strings:
            entry["flag"] = action.option_strings[0]
        else:
            entry["positional"] = True
        if action.help:
            entry["help"] = action.help
        if action.choices is not None:
            entry["choices"] = list(action.choices)
        if (action.default is not None
                and action.default is not argparse.SUPPRESS):
            try:
                json.dumps(action.default)  # ensure serializable
                entry["default"] = action.default
            except (TypeError, ValueError):
                entry["default"] = str(action.default)
        if action.nargs in ("*", "+") or isinstance(action,
                                                    argparse._AppendAction):
            entry["multiple"] = True
        params[dest] = entry

    out: dict[str, Any] = {
        "command": command,
        "description": parser.description or "",
        "params": params,
    }
    meta = getattr(parser, "_schema_meta", None)
    if meta:
        out["meta"] = meta
    if subcommands:
        out["subcommands"] = subcommands
    return out


def maybe_emit_schema(parser: argparse.ArgumentParser, command: str,
                      argv: list[str] | None = None) -> None:
    """If the caller passed --schema, emit the parser schema and exit 0.

    Call this at the top of every script's main() *before* parser.parse_args().
    The intercept is pre-parse so --schema works even when required flags are
    missing — an agent discovering a command should be able to ask for its
    schema without already knowing what the flags are.
    """
    argv = argv if argv is not None else sys.argv[1:]
    if "--schema" not in argv:
        return
    schema = _parser_to_schema(parser, command)
    schema["exit_codes"] = EXIT_CODE_VOCAB
    schema["envelope_version"] = SCHEMA_VERSION
    schema["cli_version"] = VERSION
    ok(schema)
    sys.exit(0)


# ---------- idempotency cache ----------
#
# The cache is a directory of JSON files, one per idempotency key. A cache
# entry stores `{response, signature, cached_at}`. When an agent retries a
# command with the same `--idempotency-key`, the cached response is returned
# unchanged so repeated calls do not re-spend API budget or re-mutate state.
#
# Cache directory precedence: $SCHOLAR_CACHE_DIR > .scholar_cache/ in cwd.
# There is no TTL — the agent (or a human) flushes stale keys manually. This
# is deliberate: an idempotency key names a *specific run*, not a time window,
# so silent expiry would violate the contract.

CACHE_ENTRY_VERSION = 1


def cache_dir() -> Path:
    """Return the cache directory path, creating it on first use."""
    d = Path(os.environ.get("SCHOLAR_CACHE_DIR", ".scholar_cache"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def cache_path_for(key: str) -> Path:
    """Map an idempotency key to its cache file path.

    Keys are sanitized to safe filenames: the raw key is hashed and the
    resulting hex prefix is used as the filename. This means arbitrary
    user-supplied key strings (including `/`, whitespace, unicode) are safe.
    """
    safe = hashlib.sha256(key.encode("utf-8")).hexdigest()[:32]
    return cache_dir() / f"{safe}.json"


def command_signature(args: argparse.Namespace,
                      *, exclude: tuple[str, ...] = ()) -> str:
    """Hash an argparse.Namespace into a short signature.

    Used to detect idempotency-key collisions: the same key MUST see the
    same (semantically meaningful) arguments. `exclude` names fields that
    do not affect output (e.g. `email` for polite-pool identification).
    The `idempotency_key` field is always excluded.
    """
    ignored = set(exclude) | {"idempotency_key", "dry_run", "schema", "func"}
    fields = {}
    for k, v in vars(args).items():
        if k in ignored or k.startswith("_"):
            continue
        # Skip callables (e.g. argparse's `func` set_defaults): their repr
        # contains the function's memory address and changes every process,
        # which would make every retry look like a signature mismatch.
        if callable(v):
            continue
        fields[k] = v
    blob = json.dumps(fields, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def read_cache(key: str) -> dict[str, Any] | None:
    """Read a cache entry by key, or None if missing/corrupt."""
    path = cache_path_for(key)
    if not path.exists():
        return None
    try:
        entry = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(entry, dict) or "response" not in entry:
        return None
    return entry


def write_cache(key: str, response: dict[str, Any], *,
                signature: str | None = None) -> None:
    """Persist a cache entry for an idempotency key."""
    path = cache_path_for(key)
    entry = {
        "version": CACHE_ENTRY_VERSION,
        "key": key,
        "signature": signature,
        "cached_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "response": response,
    }
    path.write_text(json.dumps(entry, ensure_ascii=False, indent=2))


def reject_dry_run_with_idempotency(args: argparse.Namespace) -> None:
    """Emit `idempotency_with_dry_run` / exit 3 if both flags are set.

    Call at the top of any command that has both `--dry-run` and
    `--idempotency-key` flags. Without this check, a command that
    short-circuits on dry-run before reaching `with_idempotency`
    would silently accept the nonsensical combination.
    """
    if getattr(args, "dry_run", False) and getattr(args, "idempotency_key", None):
        err("idempotency_with_dry_run",
            "--idempotency-key cannot be combined with --dry-run: a dry "
            "run does not mutate anything and nothing is cacheable.",
            retryable=False, exit_code=EXIT_VALIDATION,
            key=args.idempotency_key)


def with_idempotency(
    args: argparse.Namespace,
    compute: Callable[[], dict[str, Any]],
    *,
    signature_exclude: tuple[str, ...] = (),
) -> None:
    """Run `compute` under --idempotency-key semantics and emit ok(result).

    Wraps the common cache-check / compute / cache-write dance so every
    mutating command implements idempotency the same way. The caller
    supplies a zero-arg `compute` that returns the result dict; this
    helper handles cache hits, signature mismatches, and the final
    emission.

    `args` must be an argparse Namespace with an `idempotency_key`
    attribute (may be None). A non-None key combined with a truthy
    `dry_run` attribute returns a structured error — dry runs do not
    mutate and therefore cannot sensibly be cached.

    `signature_exclude` names parameters that should not participate in
    the signature hash (e.g. `email` for polite-pool fields that do not
    change the computed result).
    """
    key = getattr(args, "idempotency_key", None)
    dry = getattr(args, "dry_run", False)

    if not key:
        ok(compute())
        return

    if dry:
        err("idempotency_with_dry_run",
            "--idempotency-key cannot be combined with --dry-run: a dry "
            "run does not mutate anything and nothing is cacheable.",
            retryable=False, exit_code=EXIT_VALIDATION,
            key=key)

    sig = command_signature(args, exclude=signature_exclude)
    cached = read_cache(key)
    if cached is not None:
        if cached.get("signature") and cached["signature"] != sig:
            err("idempotency_key_mismatch",
                f"Idempotency key '{key}' was previously used with "
                f"different arguments. Use a new key or flush the cache entry.",
                retryable=False, exit_code=EXIT_VALIDATION,
                key=key,
                cached_signature=cached["signature"],
                current_signature=sig)
        ok(cached["response"], meta={
            "cache_hit": True,
            "idempotency_key": key,
            "cached_at": cached.get("cached_at"),
        })
        return

    result = compute()
    write_cache(key, result, signature=sig)
    ok(result, meta={"cache_hit": False, "idempotency_key": key})
