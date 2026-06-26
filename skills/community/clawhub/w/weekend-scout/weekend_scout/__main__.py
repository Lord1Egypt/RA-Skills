"""CLI entry point for Weekend Scout.

Provides subcommands:
  setup             -- interactive first-run setup wizard
  config            -- show current configuration
  init              -- load config + cities + cache for a scout run (JSON)
  init-skill        -- load compact skill startup context
  save              -- save discovered events to cache
  session-query     -- inspect run-scoped session candidates for one run
  prepare-digest    -- build deterministic scoring input from saved cache
  send              -- send formatted message to Telegram
  cache-query       -- query cached events for a weekend date
  log-search        -- log a completed search to the search log
  log-action        -- append a structured action log entry
  phase-c-cities    -- load a later-tier phase-C city batch
  phase-summary     -- log a canonical phase summary for a run phase
  score-summary     -- log a canonical flat score summary
  prepare-delivery  -- compute pre-send delivery stats for one run
  run-complete      -- log a canonical run_complete entry
  audit-run         -- validate one logged scout run by run_id
  cache-mark-served -- mark events as sent to Telegram
  format-message    -- format scout message and write to file
  install-skill     -- copy bundled skill files to the global skills directory
  find-city         -- look up a city in the GeoNames database
  download-data     -- download GeoNames cities15000.zip into the cache directory
  reset             -- delete local config and cache for the active install
  run               -- full automated run
"""

import argparse
import fnmatch
import json
import re
import shutil
import sys
from typing import Any, NoReturn

from weekend_scout.cache import VALIDATION_FETCH_LIMIT
from weekend_scout.diagnostics import CommandFailure, emit_command_failure

_TARGETED_RETRY_HINTS: dict[str, str] = {
    "de": "Stadtfest Markt Frühlingsfest Wochenende",
    "pl": "festyn jarmark festiwal plener weekend",
    "en": "festival market fair outdoor weekend",
}
_DIGEST_EVENT_FIELDS: tuple[str, ...] = (
    "event_name",
    "city",
    "country",
    "start_date",
    "end_date",
    "time_info",
    "location_name",
    "lat",
    "lon",
    "category",
    "description",
    "free_entry",
    "source_url",
    "source_name",
    "confidence",
)
_TIER_SORT_ORDER: dict[str, int] = {"tier1": 1, "tier2": 2, "tier3": 3, "unknown": 9}


def _print_error_and_exit(
    message: str,
    *,
    error_code: str = "command_failed",
    detail: dict[str, Any] | None = None,
    retryable: bool = False,
    run_id: str | None = None,
    phase: str | None = None,
    target_weekend: str | None = None,
    config: dict[str, Any] | None = None,
) -> NoReturn:
    raise CommandFailure(
        message=message,
        error_code=error_code,
        detail=detail or {},
        retryable=retryable,
        run_id=run_id,
        phase=phase,
        target_weekend=target_weekend,
        config=config,
    )


_FAILURE_CONTEXT_EXCLUDE = {
    "json_data",
    "message",
    "events",
    "city_events",
    "trips",
    "detail",
}


def _build_failure_context(args: argparse.Namespace) -> dict[str, Any]:
    """Build a safe diagnostics context from parsed CLI args."""
    context: dict[str, Any] = {}
    for key, value in vars(args).items():
        if key in _FAILURE_CONTEXT_EXCLUDE or value is None:
            continue
        if isinstance(value, (str, int, float, bool)):
            context[key] = value
    return context


def _resolve_target_weekend_arg(args: argparse.Namespace) -> str | None:
    """Best-effort target weekend extraction for diagnostics."""
    for attr in ("target_weekend", "saturday", "date"):
        value = getattr(args, attr, None)
        if isinstance(value, str) and value:
            return value
    run_id = getattr(args, "run_id", None)
    if isinstance(run_id, str):
        match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})_\d{4}", run_id)
        if match:
            return match.group(1)
    return None


def _load_config_for_diagnostics() -> dict[str, Any] | None:
    """Best-effort config load so failures land in the active cache dir."""
    try:
        from weekend_scout.config import load_config

        return load_config()
    except Exception:
        return None


def dispatch_command(args: argparse.Namespace, parser: argparse.ArgumentParser | None = None) -> None:
    """Run one parsed CLI command through the shared failure wrapper."""
    handler = COMMANDS.get(args.command)
    if handler is None:
        if parser is not None:
            parser.print_help()
        raise SystemExit(1)

    try:
        handler(args)
    except CommandFailure as exc:
        emit_command_failure(
            command=args.command,
            error_code=exc.error_code,
            message=exc.message,
            detail=exc.detail or _build_failure_context(args),
            retryable=exc.retryable,
            config=exc.config or _load_config_for_diagnostics(),
            run_id=exc.run_id or getattr(args, "run_id", None),
            phase=exc.phase or getattr(args, "phase", None),
            target_weekend=exc.target_weekend or _resolve_target_weekend_arg(args),
        )
    except SystemExit:
        raise
    except Exception as exc:
        emit_command_failure(
            command=args.command,
            error_code="unexpected_exception",
            message=f"{args.command} failed: {exc}",
            detail=_build_failure_context(args),
            retryable=False,
            exception=exc,
            config=_load_config_for_diagnostics(),
            run_id=getattr(args, "run_id", None),
            phase=getattr(args, "phase", None),
            target_weekend=_resolve_target_weekend_arg(args),
        )


def _is_skill_generated_payload_file(path: "Path", cache_dir: "Path") -> bool:
    """Return True when the payload file is in cache_dir and matches _tmp_*.tmp."""
    try:
        resolved_path = path.resolve()
        resolved_cache_dir = cache_dir.resolve()
    except OSError:
        return False

    if resolved_path.parent != resolved_cache_dir:
        return False
    return re.fullmatch(r"_tmp_.+\.tmp", resolved_path.name) is not None


def _cleanup_payload_files(paths: list["Path"]) -> None:
    """Best-effort cleanup for skill-generated payload files after command success."""
    for path in paths:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass


_TRANSPORT_ARTIFACT_EXACT_NAMES = {
    "setup.json",
    "events.json",
    "city-events.json",
    "trips.json",
    "covered-cities.json",
    "uncovered-tier1.json",
}
_TRANSPORT_ARTIFACT_PATTERNS = (
    "_tmp_*.tmp",
    "cities-*.json",
    "detail-*.json",
)


def _cleanup_transport_artifacts(cache_dir: "Path") -> list[str]:
    """Delete only known skill transport artifacts from the cache dir."""
    removed: list[str] = []
    try:
        items = list(cache_dir.iterdir())
    except OSError:
        return removed

    for path in items:
        if not path.is_file():
            continue
        name = path.name
        if (
            name in _TRANSPORT_ARTIFACT_EXACT_NAMES
            or any(fnmatch.fnmatch(name, pattern) for pattern in _TRANSPORT_ARTIFACT_PATTERNS)
        ):
            try:
                path.unlink(missing_ok=True)
                removed.append(name)
            except OSError:
                continue
    return removed


def _load_json_argument(
    *,
    inline_value: str | None,
    file_path: str | None,
    cache_dir: "Path | None" = None,
    cleanup_candidates: list["Path"] | None = None,
    option_name: str,
    expected_type: type,
    expected_label: str,
    default_json: str | None = None,
    required: bool = False,
):
    """Load JSON from an inline CLI arg or a UTF-8/UTF-8-BOM file."""
    if file_path:
        import re
        from pathlib import Path

        # Catch the specific corruption where a Windows drive letter has no
        # separator after the colon (e.g. "D:WorkWeekend-Scout..."). This
        # happens when a path with backslashes is passed unquoted through
        # bash and the shell eats every "\X" escape. Surface a diagnostic
        # instead of failing later with a misleading "file not found".
        if re.match(r"^[A-Za-z]:[^/\\]", file_path):
            _print_error_and_exit(
                f"{option_name}-file path looks malformed (Windows drive letter "
                f"with no separator): {file_path}. This usually means backslashes "
                f"were eaten by the shell; use the forward-slash `cache_dir` "
                f"returned by `init-skill` verbatim.",
                error_code="malformed_path",
                detail={"option": option_name, "path": file_path},
            )

        payload_path = Path(file_path)
        try:
            raw_value = payload_path.read_text(encoding="utf-8-sig")
        except FileNotFoundError:
            _print_error_and_exit(
                f"{option_name}-file not found: {file_path}",
                error_code="input_file_not_found",
                detail={"option": option_name, "path": file_path},
            )
        except OSError as exc:
            _print_error_and_exit(
                f"Failed to read {option_name}-file {file_path}: {exc}",
                error_code="input_file_read_failed",
                detail={"option": option_name, "path": file_path},
            )
    elif inline_value is not None:
        raw_value = inline_value
    elif default_json is not None:
        raw_value = default_json
    elif required:
        _print_error_and_exit(
            f"Provide {option_name} or {option_name}-file",
            error_code="missing_required_input",
            detail={"option": option_name},
        )
    else:
        return None

    try:
        parsed = json.loads(raw_value)
    except json.JSONDecodeError as exc:
        source = f"{option_name}-file {file_path}" if file_path else option_name
        _print_error_and_exit(
            f"Invalid JSON in {source}: {exc.msg}",
            error_code="invalid_json",
            detail={"option": option_name, "source": source},
        )

    if not isinstance(parsed, expected_type):
        _print_error_and_exit(
            f"{option_name} must be a {expected_label}",
            error_code="invalid_json_type",
            detail={"option": option_name, "expected_type": expected_label},
        )

    if (
        file_path
        and cache_dir is not None
        and cleanup_candidates is not None
        and _is_skill_generated_payload_file(payload_path, cache_dir)
    ):
        cleanup_candidates.append(payload_path)

    return parsed


def _load_string_array_argument(
    *,
    inline_value: str | None,
    file_path: str | None,
    cache_dir: "Path | None" = None,
    cleanup_candidates: list["Path"] | None = None,
    option_name: str,
) -> list[str]:
    """Load a JSON string array from an inline CLI arg or UTF-8/UTF-8-BOM file."""
    parsed = _load_json_argument(
        inline_value=inline_value,
        file_path=file_path,
        cache_dir=cache_dir,
        cleanup_candidates=cleanup_candidates,
        option_name=option_name,
        expected_type=list,
        expected_label="JSON array",
        default_json="[]",
    )
    if any(not isinstance(item, str) for item in parsed):
        _print_error_and_exit(
            f"{option_name} must be a JSON array of strings",
            error_code="invalid_json_type",
            detail={"option": option_name, "expected_type": "JSON array of strings"},
        )
    return parsed


def _parse_bool_arg(value: str, *, option_name: str) -> bool:
    """Parse a CLI boolean from a common true/false string."""
    lowered = value.strip().lower()
    if lowered in {"true", "1", "yes"}:
        return True
    if lowered in {"false", "0", "no"}:
        return False
    _print_error_and_exit(
        f"{option_name} must be true or false",
        error_code="invalid_boolean",
        detail={"option": option_name, "value": value},
    )


def _extract_saturday_from_run_id(run_id: str) -> str:
    """Extract the ISO Saturday prefix from a run_id."""
    match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})_\d{4}", run_id)
    if not match:
        _print_error_and_exit(
            f"run_id must look like YYYY-MM-DD_HHMM, got: {run_id}",
            error_code="invalid_run_id",
            detail={"run_id": run_id},
        )
    return match.group(1)


def cmd_setup(args: argparse.Namespace) -> None:
    """Run interactive setup wizard, or apply a JSON config payload directly."""
    from weekend_scout.config import (
        COUNTRY_CODE_MAP,
        COUNTRY_LANGUAGE_MAP,
        get_cache_dir,
        get_config_path,
        load_config,
        save_config,
    )
    from weekend_scout.cities import ensure_geonames, find_city_coords, normalize_city_input
    from pathlib import Path as _P

    old_config = load_config()
    cleanup_candidates: list[_P] = []
    incoming = _load_json_argument(
        inline_value=args.json_data,
        file_path=args.json_file,
        cache_dir=get_cache_dir(old_config),
        cleanup_candidates=cleanup_candidates,
        option_name="--json",
        expected_type=dict,
        expected_label="JSON object",
    )
    if incoming is not None:
        country_hint: str | None = None
        if incoming.get("home_city"):
            normalized_city, country_hint = normalize_city_input(str(incoming["home_city"]))
            if normalized_city:
                incoming["home_city"] = normalized_city

        needs_city_resolution = bool(incoming.get("home_city")) and (
            not incoming.get("home_country") or "home_coordinates" not in incoming
        )
        if needs_city_resolution:
            geonames_path = ensure_geonames()
            if geonames_path.exists():
                city_data = find_city_coords(
                    incoming["home_city"],
                    geonames_path,
                    country_filter=incoming.get("home_country") or country_hint,
                )
                if city_data:
                    incoming["home_city"] = (
                        city_data.get("name_local") or city_data.get("name") or incoming["home_city"]
                    )
                    resolved_country = COUNTRY_CODE_MAP.get(city_data["country"], "")
                    if resolved_country:
                        incoming["home_country"] = resolved_country
                        if "search_language" not in incoming:
                            incoming["search_language"] = COUNTRY_LANGUAGE_MAP.get(resolved_country, "en")
                    if "home_coordinates" not in incoming:
                        incoming["home_coordinates"] = {
                            "lat": city_data["lat"],
                            "lon": city_data["lon"],
                        }

        if "search_language" not in incoming:
            country = incoming.get("home_country") or old_config.get("home_country", "")
            if country:
                incoming["search_language"] = COUNTRY_LANGUAGE_MAP.get(country, "en")

        config = dict(old_config)
        config.update(incoming)
        save_config(config)
        # Invalidate city cache when city name or coordinates change
        old_city = old_config.get("home_city", "")
        new_city = config.get("home_city", "")
        old_coords = old_config.get("home_coordinates", {})
        new_coords = config.get("home_coordinates", {})
        if old_city != new_city or old_coords != new_coords:
            cache_dir = get_cache_dir(config)
            for city in {old_city, new_city} - {""}:
                for radius in {old_config.get("radius_km", 150), config.get("radius_km", 150)}:
                    stale = _P(cache_dir) / f"cities_{city}_{radius}.json"
                    if stale.exists():
                        stale.unlink()
        _cleanup_payload_files(cleanup_candidates)
        print(json.dumps({"saved": True, "config_path": str(get_config_path())}, ensure_ascii=False))
    else:
        from weekend_scout.config import run_setup_wizard
        run_setup_wizard()


def cmd_find_city(args: argparse.Namespace) -> None:
    """Look up a city in the GeoNames database and return matching entries."""
    from weekend_scout.cities import find_city_candidates, ensure_geonames, normalize_city_input

    geonames_path = ensure_geonames()
    normalized_name, country_hint = normalize_city_input(args.name)
    matches = find_city_candidates(
        normalized_name or args.name,
        geonames_path,
        country_filter=args.country or country_hint,
    )
    print(json.dumps({"matches": matches}, ensure_ascii=False))


def cmd_config(args: argparse.Namespace) -> None:
    """Print current configuration as JSON, or set a key."""
    from weekend_scout.config import load_config, save_config
    config = load_config()

    if args.key:
        key = args.key
        value = args.value
        if key not in config:
            _print_error_and_exit(
                f"Unknown config key: {key}",
                error_code="unknown_config_key",
                detail={"key": key},
                config=config,
            )
        if value is None:
            print(json.dumps({key: config[key]}, ensure_ascii=False))
            return
        # Coerce type to match existing value
        existing = config[key]
        try:
            if isinstance(existing, bool):
                value = value.lower() in ("true", "1", "yes")
            elif isinstance(existing, int):
                value = int(value)
            elif isinstance(existing, float):
                value = float(value)
            elif isinstance(existing, (dict, list)):
                value = json.loads(value)
                if not isinstance(value, type(existing)):
                    raise ValueError
        except (ValueError, TypeError, json.JSONDecodeError):
            _print_error_and_exit(
                f"Invalid value for {key}: expected {type(existing).__name__}",
                error_code="invalid_config_value",
                detail={"key": key, "expected_type": type(existing).__name__},
                config=config,
            )
        config[key] = value
        save_config(config)
        print(json.dumps({"set": {key: value}}))
    else:
        print(json.dumps(config, indent=2, ensure_ascii=False))


def cmd_reset(args: argparse.Namespace) -> None:
    """Delete the local config file and cache directory for the active install."""
    from weekend_scout.config import get_config_dir, get_config_path

    config_dir = get_config_dir()
    config_path = get_config_path()
    cache_dir = config_dir / "cache"

    if not args.yes:
        _print_error_and_exit(
            "Reset deletes your Weekend Scout config and cache. Re-run with --yes after confirming.",
            error_code="confirmation_required",
            detail={
                "command": "reset",
                "config_path": str(config_path),
                "cache_dir": str(cache_dir),
            },
        )

    removed: list[str] = []
    if config_path.exists():
        config_path.unlink()
        removed.append(str(config_path))
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
        removed.append(str(cache_dir))
    try:
        if config_dir.exists() and not any(config_dir.iterdir()):
            config_dir.rmdir()
    except OSError:
        pass

    print(
        json.dumps(
            {
                "reset": True,
                "config_dir": str(config_dir),
                "removed": removed,
            },
            ensure_ascii=False,
        )
    )


def cmd_save(args: argparse.Namespace) -> None:
    """Save events (JSON array) to the cache."""
    from weekend_scout.config import load_config, get_cache_dir
    from weekend_scout.cache import save_events, log_action
    from weekend_scout.session_cache import finalize_session_candidates

    config = load_config()
    cleanup_candidates = []
    if args.from_session:
        if not args.run_id:
            _print_error_and_exit(
                "--run-id is required with --from-session",
                error_code="missing_run_id",
                detail={"command": "save", "mode": "from-session"},
                config=config,
            )
        finalized = finalize_session_candidates(config, args.run_id)
        events = finalized["candidates"]
    else:
        events = _load_json_argument(
            inline_value=args.events,
            file_path=args.events_file,
            cache_dir=get_cache_dir(config),
            cleanup_candidates=cleanup_candidates,
            option_name="--events",
            expected_type=list,
            expected_label="JSON array",
            required=True,
        )
    saved, skipped = save_events(config, events)
    log_action(config, "events_saved", run_id=args.run_id,
               detail={"saved": saved, "skipped": skipped})
    _cleanup_payload_files(cleanup_candidates)
    print(json.dumps({"saved": saved, "skipped": skipped}))


def cmd_send(args: argparse.Namespace) -> None:
    """Send a formatted message to Telegram."""
    from weekend_scout.config import load_config
    from weekend_scout.telegram import send_telegram
    from weekend_scout.cache import log_action

    config = load_config()

    if args.file:
        from pathlib import Path
        try:
            message = Path(args.file).read_text(encoding="utf-8-sig")
        except FileNotFoundError:
            _print_error_and_exit(
                f"File not found: {args.file}",
                error_code="message_file_not_found",
                detail={"path": args.file},
                run_id=args.run_id,
                config=config,
            )
        except OSError as exc:
            _print_error_and_exit(
                f"Failed to read message file {args.file}: {exc}",
                error_code="message_file_read_failed",
                detail={"path": args.file},
                run_id=args.run_id,
                config=config,
            )
    elif args.message:
        message = args.message
    else:
        _print_error_and_exit(
            "Provide --message or --file",
            error_code="missing_message_input",
            run_id=args.run_id,
            config=config,
        )

    send_result = send_telegram(config, message)
    send_target_weekend = _resolve_target_weekend_arg(args)
    log_action(
        config,
        "telegram_send",
        run_id=args.run_id,
        target_weekend=send_target_weekend,
        detail={
            "success": send_result["sent"],
            "reason": send_result["reason"],
            "error_code": send_result.get("error_code"),
            "status_code": send_result.get("status_code"),
            "error": send_result.get("error"),
            "parts_sent": send_result.get("parts_sent", 0),
            "char_count": len(message),
        },
    )
    print(json.dumps(send_result, ensure_ascii=False))


def cmd_cache_query(args: argparse.Namespace) -> None:
    """Query cached events for the weekend containing the given date."""
    from weekend_scout.config import load_config
    from weekend_scout.cache import query_events

    config = load_config()
    events = query_events(config, args.date)
    print(json.dumps(events, indent=2, ensure_ascii=False))


def cmd_log_search(args: argparse.Namespace) -> None:
    """Log a completed web search to the search log."""
    from pathlib import Path
    from weekend_scout.config import load_config, get_cache_dir
    from weekend_scout.cache import log_search
    from weekend_scout.session_cache import get_session_candidate_count

    config = load_config()
    if args.cities_file and args.events_file:
        try:
            same_payload_path = Path(args.cities_file).resolve() == Path(args.events_file).resolve()
        except OSError:
            same_payload_path = args.cities_file == args.events_file
        if same_payload_path:
            _print_error_and_exit(
                "--cities-file and --events-file must use separate files; write the city-name array and event array to different paths",
                error_code="duplicate_input_files",
                detail={"options": ["--cities-file", "--events-file"]},
                run_id=args.run_id,
                target_weekend=args.target_weekend,
                config=config,
            )
    cleanup_candidates = []
    cities = _load_json_argument(
        inline_value=args.cities,
        file_path=args.cities_file,
        cache_dir=get_cache_dir(config),
        cleanup_candidates=cleanup_candidates,
        option_name="--cities",
        expected_type=list,
        expected_label="JSON array",
        default_json="[]",
    )
    events = _load_json_argument(
        inline_value=args.events,
        file_path=args.events_file,
        cache_dir=get_cache_dir(config),
        cleanup_candidates=cleanup_candidates,
        option_name="--events",
        expected_type=list,
        expected_label="JSON array",
    )
    if events is not None and not args.run_id:
        _print_error_and_exit(
            "--run-id is required with --events or --events-file",
            error_code="missing_run_id",
            detail={"command": "log-search", "has_events": True},
            config=config,
        )
    try:
        result = log_search(
            config=config,
            query=args.query,
            target_weekend=args.target_weekend,
            result_count=args.result_count,
            cities_covered=cities,
            phase=args.phase,
            run_id=args.run_id,
            events_discovered=args.events_discovered,
            events=events,
        )
    except ValueError as exc:
        _print_error_and_exit(
            str(exc),
            error_code="invalid_log_search_request",
            detail={"query": args.query, "phase": args.phase},
            run_id=args.run_id,
            target_weekend=args.target_weekend,
            config=config,
        )
    session_candidate_count = result["session_candidate_count"]
    if events is None and args.run_id:
        session_candidate_count = get_session_candidate_count(config, args.run_id)
    _cleanup_payload_files(cleanup_candidates)
    print(json.dumps({
        "logged": True,
        "events_discovered": result["events_discovered"],
        "session_candidate_count": session_candidate_count,
        "duplicates_merged": result["duplicates_merged"],
    }, ensure_ascii=False))


def cmd_log_action(args: argparse.Namespace) -> None:
    """Append a structured action log entry to action_log.jsonl."""
    from weekend_scout.config import load_config, get_cache_dir
    from weekend_scout.cache import ensure_phase_started, log_action

    config = load_config()
    cleanup_candidates = []
    detail = _load_json_argument(
        inline_value=args.detail,
        file_path=args.detail_file,
        cache_dir=get_cache_dir(config),
        cleanup_candidates=cleanup_candidates,
        option_name="--detail",
        expected_type=dict,
        expected_label="JSON object",
        default_json="{}",
    )
    if (args.action == "skip" and args.phase in {"A", "B", "C", "D"}):
        ensure_phase_started(
            config,
            run_id=args.run_id,
            phase=args.phase,
            target_weekend=args.target_weekend,
            trigger=f"log_action:skip:{args.phase}",
        )
    log_action(
        config,
        args.action,
        phase=args.phase,
        detail=detail,
        run_id=args.run_id,
        source=args.source,
        target_weekend=args.target_weekend,
    )
    _cleanup_payload_files(cleanup_candidates)
    print(json.dumps({"logged": True}))


def cmd_cache_mark_served(args: argparse.Namespace) -> None:
    """Mark all events for the given weekend date as served."""
    from weekend_scout.config import load_config
    from weekend_scout.cache import mark_served, log_action

    config = load_config()
    count = mark_served(config, args.date)
    log_action(
        config,
        "events_served",
        run_id=args.run_id,
        target_weekend=args.date,
        detail={"count": count},
    )
    print(json.dumps({"marked": count}))


def cmd_session_query(args: argparse.Namespace) -> None:
    """Return canonical session candidates for the run's target weekend."""
    from weekend_scout.config import load_config
    from weekend_scout.session_cache import query_session_candidates

    config = load_config()
    print(json.dumps(query_session_candidates(config, args.run_id), ensure_ascii=False))


def _build_city_lookup(cities: dict[str, list[str]]) -> tuple[dict[str, str], dict[str, str]]:
    tier_by_city: dict[str, str] = {}
    country_by_city: dict[str, str] = {}
    from weekend_scout.config import COUNTRY_CODE_MAP

    for tier_name in ("tier1", "tier2", "tier3"):
        for entry in cities.get(tier_name, []):
            if "|" not in entry:
                continue
            city_name, country_code = entry.rsplit("|", 1)
            tier_by_city.setdefault(city_name, tier_name)
            country_by_city.setdefault(city_name, COUNTRY_CODE_MAP.get(country_code, ""))
    return tier_by_city, country_by_city


def _build_retry_query(query: str, target: dict[str, str]) -> str:
    language = str(target.get("language") or "en")
    suffix = _TARGETED_RETRY_HINTS.get(language, _TARGETED_RETRY_HINTS["en"])
    return f"{query} {suffix}".strip()


def _digest_confidence_rank(value: object) -> int:
    if not isinstance(value, str):
        return 0
    lowered = value.strip().lower()
    if lowered == "confirmed":
        return 2
    if lowered == "likely":
        return 1
    return 0


def _digest_source_rank(candidate: dict[str, object]) -> int:
    source_name = str(candidate.get("source_name") or "").lower()
    source_url = str(candidate.get("source_url") or "").lower()
    official_markers = ("official", ".gov", ".de/", ".pl/", ".org/")
    aggregator_markers = ("visit", "event", "ticket", "facebook", "berlin.de/events")
    if any(marker in source_name or marker in source_url for marker in official_markers):
        return 2
    if any(marker in source_name or marker in source_url for marker in aggregator_markers):
        return 1
    return 0


def _digest_sort_key(candidate: dict[str, object]) -> tuple[object, ...]:
    return (
        -_digest_confidence_rank(candidate.get("confidence")),
        -int(bool(candidate.get("free_entry"))),
        -_digest_source_rank(candidate),
        str(candidate.get("start_date", "")),
        str(candidate.get("event_name", "")).lower(),
    )


def _trim_digest_event(candidate: dict[str, object]) -> dict[str, object]:
    return {
        field: candidate[field]
        for field in _DIGEST_EVENT_FIELDS
        if field in candidate and candidate[field] not in ("", None)
    }


def cmd_prepare_digest(args: argparse.Namespace) -> None:
    """Build deterministic Step 3 scoring input from saved cache rows."""
    from weekend_scout.config import load_config
    from weekend_scout.cache import query_events
    from weekend_scout.cities import get_city_list
    from weekend_scout.session_cache import canonicalize_candidates

    config = load_config()
    cached_events = query_events(config, args.date)
    canonical = canonicalize_candidates(config, args.date, cached_events)
    candidates = canonical["candidates"]

    try:
        cities = get_city_list(config)
    except Exception:
        cities = {"tier1": [], "tier2": [], "tier3": []}
    tier_by_city, country_code_by_city = _build_city_lookup(cities)

    home_city = str(config.get("home_city") or "")
    home_city_candidates = [
        _trim_digest_event(candidate)
        for candidate in sorted(
            (candidate for candidate in candidates if str(candidate.get("city") or "") == home_city),
            key=_digest_sort_key,
        )
    ]

    grouped_trip_candidates: dict[str, list[dict[str, object]]] = {}
    for candidate in candidates:
        city_name = str(candidate.get("city") or "")
        if not city_name or city_name == home_city:
            continue
        grouped_trip_candidates.setdefault(city_name, []).append(candidate)

    trip_city_groups: list[dict[str, object]] = []
    for city_name, city_candidates in grouped_trip_candidates.items():
        sorted_events = sorted(city_candidates, key=_digest_sort_key)
        city_events = [_trim_digest_event(event) for event in sorted_events]
        trip_city_groups.append(
            {
                "city": city_name,
                "country": str(
                    sorted_events[0].get("country")
                    or country_code_by_city.get(city_name, "")
                ),
                "tier": tier_by_city.get(city_name, "unknown"),
                "event_count": len(sorted_events),
                "confirmed_count": sum(
                    1 for event in sorted_events if _digest_confidence_rank(event.get("confidence")) >= 2
                ),
                "events": city_events,
            }
        )

    trip_city_groups.sort(
        key=lambda group: (
            _TIER_SORT_ORDER.get(str(group["tier"]), 9),
            str(group["city"]).lower(),
        )
    )

    summary = {
        "duplicates_collapsed": canonical["duplicates_collapsed"],
        "home_city_count": len(home_city_candidates),
        "trip_city_count": len(trip_city_groups),
        "total_pool": len(home_city_candidates) + len(trip_city_groups),
    }
    print(
        json.dumps(
            {
                "summary": summary,
                "home_city_candidates": home_city_candidates,
                "trip_city_groups": trip_city_groups,
            },
            ensure_ascii=False,
        )
    )


def cmd_download_data(args: argparse.Namespace) -> None:
    """Download and unzip GeoNames cities15000.zip into the cache directory."""
    from weekend_scout.cities import download_geonames
    path = download_geonames(force=args.force)
    print(json.dumps({"path": str(path)}))


def cmd_format_message(args: argparse.Namespace) -> None:
    """Format a scout message and write it to a file."""
    from pathlib import Path
    from weekend_scout.config import load_config, get_cache_dir
    from weekend_scout.telegram import format_scout_message, format_scout_preview
    from weekend_scout.cache import log_action

    config = load_config()
    cache_dir = get_cache_dir(config)
    cleanup_candidates = []
    city_events = _load_json_argument(
        inline_value=args.city_events,
        file_path=args.city_events_file,
        cache_dir=cache_dir,
        cleanup_candidates=cleanup_candidates,
        option_name="--city-events",
        expected_type=list,
        expected_label="JSON array",
        default_json="[]",
    )
    trips = _load_json_argument(
        inline_value=args.trips,
        file_path=args.trips_file,
        cache_dir=cache_dir,
        cleanup_candidates=cleanup_candidates,
        option_name="--trips",
        expected_type=list,
        expected_label="JSON array",
        default_json="[]",
    )
    stats_lines = _load_string_array_argument(
        inline_value=args.stats_lines,
        file_path=args.stats_lines_file,
        cache_dir=cache_dir,
        cleanup_candidates=cleanup_candidates,
        option_name="--stats-lines",
    )
    notes_lines = _load_string_array_argument(
        inline_value=args.notes_lines,
        file_path=args.notes_lines_file,
        cache_dir=cache_dir,
        cleanup_candidates=cleanup_candidates,
        option_name="--notes-lines",
    )
    low_results = args.low_results.lower() in ("true", "1", "yes") if args.low_results else False
    hint_searches = max(50, config.get("max_searches", 15) + 20)
    hint_fetches  = max(50, config.get("max_fetches",  15) + 20)
    msg = format_scout_message(
        config.get("home_city", ""),
        args.saturday,
        args.sunday,
        city_events,
        trips,
        stats_lines=stats_lines,
        notes_lines=notes_lines,
        low_results_hint=low_results,
        hint_max_searches=hint_searches,
        hint_max_fetches=hint_fetches,
    )
    preview = format_scout_preview(
        config.get("home_city", ""),
        args.saturday,
        args.sunday,
        city_events,
        trips,
        stats_lines=stats_lines,
        notes_lines=notes_lines,
        low_results_hint=low_results,
        hint_max_searches=hint_searches,
        hint_max_fetches=hint_fetches,
    )
    output_path = Path(args.output) if args.output else get_cache_dir(config) / "scout_message.txt"
    output_path.write_text(msg, encoding="utf-8")
    log_action(config, "message_formatted", run_id=args.run_id,
               target_weekend=args.saturday,
               detail={"city_events": len(city_events), "trips": len(trips),
                       "char_count": len(msg)})
    _cleanup_payload_files(cleanup_candidates)
    print(json.dumps({"written": str(output_path), "preview": preview}, ensure_ascii=False))


def _build_targeted_city_cards(
    entries: list[str],
    *,
    searches_this_week: list[str],
    targeted_by_country: dict[str, dict[str, str]],
    geonames_path: "Path",
    covered_cities: list[str] | None = None,
) -> list[dict[str, object]]:
    """Build compact targeted-search cards."""
    from weekend_scout.config import COUNTRY_CODE_MAP
    from weekend_scout.cities import get_query_city_name

    covered = {str(city) for city in covered_cities or []}
    cards: list[dict[str, object]] = []
    for entry in entries:
        if "|" not in entry:
            continue
        city_name, country_code = entry.rsplit("|", 1)
        target = targeted_by_country.get(country_code)
        if not target:
            continue
        query_city = get_query_city_name(
            city_name,
            lang=str(target.get("language") or "en"),
            geonames_path=geonames_path,
            country_filter=COUNTRY_CODE_MAP.get(country_code, "") or None,
        )
        query = target["template"].format(city=query_city, date=target["date"])
        still_uncovered = city_name not in covered
        cards.append({
            "city_name": city_name,
            "query": query,
            "query_already_done": query in searches_this_week,
            "still_uncovered": still_uncovered,
            "retry_on_rerun": query in searches_this_week and still_uncovered,
            "retry_query": _build_retry_query(query, target),
        })
    return cards


def _build_workflow_cards(
    *,
    config: dict[str, object],
    cities: dict[str, list[str]],
    cached_summary: dict[str, object],
    searches_this_week: list[str],
    broad_result: dict[str, object],
    targeted_by_country: dict[str, dict[str, str]],
    geonames_path: "Path",
    run_id: str,
) -> dict[str, object]:
    """Build minimal dynamic workflow data for the runtime skill."""
    max_searches = int(config.get("max_searches", 15))
    tier2_count = len(cities.get("tier2", []))
    tier3_count = len(cities.get("tier3", []))
    broad_queries = []
    for template in broad_result["templates"]:
        query = template.format(**broad_result["vars"])
        broad_queries.append({
            "query": query,
            "query_already_done": query in searches_this_week,
        })

    return {
        "audit_command": f'python -m weekend_scout audit-run --run-id "{run_id}"',
        "coverage": {
            "cached_covered_cities": cached_summary.get("covered_cities", []),
            "cached_city_counts": cached_summary.get("city_counts", {}),
            "tier1_required_cities": [
                entry.rsplit("|", 1)[0] if "|" in entry else entry
                for entry in cities.get("tier1", [])
            ],
            "minimum_home_city_events": int(config.get("max_city_options", 3)),
            "exclude_served": bool(config.get("exclude_served", False)),
        },
        "phase_a": {
            "search_limit": min(5, max_searches),
            "queries": broad_queries,
        },
        "phase_c": {
            "tier1": _build_targeted_city_cards(
                cities.get("tier1", []),
                searches_this_week=searches_this_week,
                targeted_by_country=targeted_by_country,
                geonames_path=geonames_path,
                covered_cities=list(cached_summary.get("covered_cities", [])),
            ),
            "tier2_request": {
                "available_count": tier2_count,
                "default_limit": 6,
                "request_command": (
                    'python -m weekend_scout phase-c-cities --run-id '
                    f'"{run_id}" --tier 2 --offset <offset> --limit 6'
                ),
            },
            "tier3_request": {
                "available_count": tier3_count,
                "default_limit": 6,
                "request_command": (
                    'python -m weekend_scout phase-c-cities --run-id '
                    f'"{run_id}" --tier 3 --offset <offset> --limit 6'
                ),
            },
        },
        "phase_d": {
            "max_candidates": 5,
            "validation_fetch_limit": VALIDATION_FETCH_LIMIT,
            "session_query_command": (
                'python -m weekend_scout session-query --run-id '
                f'"{run_id}"'
            ),
            "prepare_digest_command": (
                f'python -m weekend_scout prepare-digest --date "{_extract_saturday_from_run_id(run_id)}"'
            ),
        },
    }


def _build_init_payload(
    args: argparse.Namespace,
    *,
    compact_cache: bool,
) -> tuple[dict[str, object], dict[str, object] | None]:
    """Build the shared payload for init/init-skill commands."""
    import datetime
    from weekend_scout.config import (
        load_config, save_config, get_config_path, get_cache_dir,
        COUNTRY_CODE_MAP, COUNTRY_LANGUAGE_MAP,
    )
    from weekend_scout.cities import (
        get_city_list, generate_broad_queries, generate_targeted_by_country,
        find_city_coords, ensure_geonames, normalize_city_input,
    )
    from weekend_scout.cache import query_events, query_events_summary, get_searches_this_week
    from weekend_scout.distance import next_weekend_dates
    from weekend_scout.session_cache import cleanup_stale_sessions

    config = load_config()
    cache_dir = get_cache_dir(config)
    _cleanup_transport_artifacts(cache_dir)
    cleanup_stale_sessions(config)
    try:
        cache_dir_str = cache_dir.resolve().as_posix()
    except OSError:
        cache_dir_str = cache_dir.as_posix()

    had_saved_home_city = bool(config.get("home_city"))

    city_geocoded: bool | None = None
    geonames_path = None
    if args.radius:
        try:
            config["radius_km"] = int(args.radius)
        except ValueError:
            _print_error_and_exit(
                "radius must be an integer",
                error_code="invalid_radius",
                detail={"radius": args.radius},
                config=config,
            )

    if args.city:
        normalized_city, country_hint = normalize_city_input(args.city)
        config["home_city"] = normalized_city or args.city
        if not had_saved_home_city:
            config["home_country"] = ""
            config["home_coordinates"] = {"lat": 0.0, "lon": 0.0}
        geonames_path = ensure_geonames()
        if geonames_path.exists():
            city_data = find_city_coords(
                config["home_city"],
                geonames_path,
                country_filter=country_hint,
            )
            if city_data:
                config["home_city"] = city_data.get("name_local") or city_data.get("name") or config["home_city"]
                config["home_coordinates"] = {"lat": city_data["lat"], "lon": city_data["lon"]}
                country = COUNTRY_CODE_MAP.get(city_data["country"], "")
                if country:
                    config["home_country"] = country
                    config["search_language"] = COUNTRY_LANGUAGE_MAP.get(country, "en")
                city_geocoded = True
                if not had_saved_home_city:
                    save_config(config)
            else:
                city_geocoded = False
        else:
            city_geocoded = False

    if not config.get("home_city"):
        return {
            "needs_setup": True,
            "message": "Weekend Scout is not configured. Run: python -m weekend_scout setup",
            "config_path": str(get_config_path()),
            "cache_dir": cache_dir_str,
        }, None

    saturday, sunday = next_weekend_dates()
    target_weekend = {"saturday": saturday, "sunday": sunday}
    run_id = f"{saturday}_{datetime.datetime.now().strftime('%H%M')}"

    coords = config.get("home_coordinates", {})
    coords_valid = not (coords.get("lat", 0.0) == 0.0 and coords.get("lon", 0.0) == 0.0)

    if coords_valid:
        cities = get_city_list(config, bypass_cache=args.city is not None)
    else:
        cities = {"tier1": [], "tier2": [], "tier3": []}

    cached_summary = query_events_summary(config, saturday)
    cached_events = query_events(config, saturday)
    searches_this_week = get_searches_this_week(config, saturday)
    geonames_path = geonames_path or ensure_geonames()
    broad_result = generate_broad_queries(config, saturday, sunday, geonames_path=geonames_path)
    targeted_by_country = generate_targeted_by_country(config, cities, saturday)

    config_block: dict[str, object] = {
        "home_city": config.get("home_city"),
        "home_country": config.get("home_country", ""),
        "radius_km": config.get("radius_km"),
        "search_language": config.get("search_language"),
        "target_weekend": target_weekend,
        "max_city_options": config.get("max_city_options", 3),
        "max_trip_options": config.get("max_trip_options", 10),
        "max_searches": config.get("max_searches", 15),
        "max_fetches": config.get("max_fetches", 15),
        "exclude_served": config.get("exclude_served", False),
    }
    if city_geocoded is not None:
        config_block["city_geocoded"] = city_geocoded

    output: dict[str, object] = {
        "run_id": run_id,
        "cache_dir": cache_dir_str,
        "config": config_block,
        "cities": _build_compact_cities_payload(cities),
        "cached": cached_summary,
        "workflow": _build_workflow_cards(
            config=config_block,
            cities=cities,
            cached_summary=cached_summary,
            searches_this_week=searches_this_week,
            broad_result=broad_result,
            targeted_by_country=targeted_by_country,
            geonames_path=geonames_path,
            run_id=run_id,
        ),
    }
    if compact_cache:
        output["workflow"]["compact_note"] = (
            "Later phase-C tiers are fetched on demand. Compact runtime payload keeps only tier1 plus later-tier counts."
        )
    else:
        output["debug"] = _build_debug_payload(
            cities=cities,
            cached_events=cached_events,
            searches_this_week=searches_this_week,
            broad_result=broad_result,
            targeted_by_country=targeted_by_country,
            geonames_path=geonames_path,
        )
    if not coords_valid:
        output["warnings"] = ["coordinates_not_set: nearby city suggestions disabled"]
    return output, config


def cmd_init(args: argparse.Namespace) -> None:
    """Load the runtime contract plus a debug inspection block. Output JSON."""
    from weekend_scout.cache import log_action

    output, config = _build_init_payload(args, compact_cache=False)
    if config is None:
        print(json.dumps(output, ensure_ascii=False))
        return

    saturday = output["config"]["target_weekend"]["saturday"]
    cached = output["cached"]
    log_action(config, "run_init", run_id=output["run_id"], target_weekend=saturday,
               detail={"home_city": config.get("home_city"),
                       "radius_km": config.get("radius_km"),
                       "cached_count": cached["count"],
                       "tier1": output["cities"].get("tier1", [])})
    print(json.dumps(output, indent=2, ensure_ascii=False))


def cmd_init_skill(args: argparse.Namespace) -> None:
    """Load compact run context for the skill without full cached event rows."""
    from weekend_scout.cache import log_action

    output, config = _build_init_payload(args, compact_cache=True)
    if config is None:
        print(json.dumps(output, ensure_ascii=False))
        return

    saturday = output["config"]["target_weekend"]["saturday"]
    cached = output["cached"]
    log_action(config, "run_init", run_id=output["run_id"], target_weekend=saturday,
               detail={"home_city": config.get("home_city"),
                       "radius_km": config.get("radius_km"),
                       "cached_count": cached["count"],
                       "tier1": output["cities"].get("tier1", [])})
    print(json.dumps(output, ensure_ascii=False))


def cmd_phase_c_cities(args: argparse.Namespace) -> None:
    """Return one filtered phase-C batch for tier2 or tier3."""
    from weekend_scout.config import load_config, get_cache_dir
    from weekend_scout.cities import get_city_list, generate_targeted_by_country, ensure_geonames
    from weekend_scout.cache import (
        ensure_phase_started,
        get_searches_this_week,
        log_action,
        query_events_summary,
    )
    from weekend_scout.session_cache import get_session_covered_cities

    if args.offset < 0:
        _print_error_and_exit(
            "--offset must be >= 0",
            error_code="invalid_offset",
            detail={"offset": args.offset},
        )
    if args.limit <= 0:
        _print_error_and_exit(
            "--limit must be > 0",
            error_code="invalid_limit",
            detail={"limit": args.limit},
        )

    config = load_config()
    saturday = _extract_saturday_from_run_id(args.run_id)
    cities = get_city_list(config)
    tier_key = f"tier{args.tier}"
    tier_entries = cities.get(tier_key, [])

    cleanup_candidates = []
    _load_json_argument(
        inline_value=args.covered_cities,
        file_path=args.covered_cities_file,
        cache_dir=get_cache_dir(config),
        cleanup_candidates=cleanup_candidates,
        option_name="--covered-cities",
        expected_type=list,
        expected_label="JSON array",
    )

    searches_this_week = get_searches_this_week(config, saturday)
    targeted_by_country = generate_targeted_by_country(config, cities, saturday)
    geonames_path = ensure_geonames()

    all_cards = _build_targeted_city_cards(
        tier_entries,
        searches_this_week=searches_this_week,
        targeted_by_country=targeted_by_country,
        geonames_path=geonames_path,
    )
    cached_covered = query_events_summary(config, saturday).get("covered_cities", [])
    session_covered = get_session_covered_cities(config, args.run_id)
    covered = {str(city) for city in cached_covered} | {str(city) for city in session_covered}
    filtered_cards = [
        card for card in all_cards
        if card["city_name"] not in covered and not card["query_already_done"]
    ]

    batch = filtered_cards[args.offset: args.offset + args.limit]
    next_offset = args.offset + len(batch)
    result = {
        "run_id": args.run_id,
        "tier": args.tier,
        "offset": args.offset,
        "limit": args.limit,
        "available_count": len(filtered_cards),
        "cards": batch,
        "has_more": next_offset < len(filtered_cards),
        "next_offset": next_offset if next_offset < len(filtered_cards) else None,
        "request_note": "Finish and log the current batch before requesting the next batch.",
    }
    ensure_phase_started(
        config,
        run_id=args.run_id,
        phase="C",
        target_weekend=saturday,
        trigger="phase_c_batch_requested",
    )
    log_action(
        config,
        "phase_c_batch_requested",
        phase="C",
        run_id=args.run_id,
        source="skill",
        target_weekend=saturday,
        detail={
            "tier": args.tier,
            "offset": args.offset,
            "limit": args.limit,
            "covered_count": len(covered),
            "returned_count": len(batch),
            "has_more": result["has_more"],
            "next_offset": result["next_offset"],
        },
    )
    _cleanup_payload_files(cleanup_candidates)
    print(json.dumps(result, ensure_ascii=False))


def cmd_phase_summary(args: argparse.Namespace) -> None:
    """Log one canonical phase_summary entry for a run phase."""
    from weekend_scout.config import load_config
    from weekend_scout.cache import log_phase_summary

    config = load_config()
    detail, logged, error = log_phase_summary(
        config,
        run_id=args.run_id,
        phase=args.phase,
        target_weekend=args.target_weekend,
    )
    payload: dict[str, object] = {"logged": logged, "phase": args.phase, "detail": detail}
    if error:
        payload["error"] = error
    print(json.dumps(payload, ensure_ascii=False))


def cmd_score_summary(args: argparse.Namespace) -> None:
    """Log one canonical flat score_summary entry."""
    from weekend_scout.config import load_config
    from weekend_scout.cache import log_score_summary

    config = load_config()
    detail, logged = log_score_summary(
        config,
        run_id=args.run_id,
        target_weekend=args.target_weekend,
        total_pool=args.total_pool,
        city_events_selected=args.city_events_selected,
        trip_options=args.trip_options,
    )
    print(json.dumps({"logged": logged, "detail": detail}, ensure_ascii=False))


def cmd_prepare_delivery(args: argparse.Namespace) -> None:
    """Compute pre-send delivery stats without logging any new action."""
    from weekend_scout.config import load_config
    from weekend_scout.cache import build_delivery_detail

    config = load_config()
    detail = build_delivery_detail(
        config,
        run_id=args.run_id,
        events_sent=args.events_sent,
    )
    print(json.dumps({"detail": detail}, ensure_ascii=False))


def cmd_run_complete(args: argparse.Namespace) -> None:
    """Log one canonical run_complete entry with computed usage counts."""
    from weekend_scout.config import load_config, get_cache_dir
    from weekend_scout.cache import log_run_complete

    config = load_config()
    cleanup_candidates = []
    _load_json_argument(
        inline_value=args.uncovered_tier1,
        file_path=args.uncovered_tier1_file,
        cache_dir=get_cache_dir(config),
        cleanup_candidates=cleanup_candidates,
        option_name="--uncovered-tier1",
        expected_type=list,
        expected_label="JSON array",
        default_json="[]",
    )
    detail, logged = log_run_complete(
        config,
        run_id=args.run_id,
        target_weekend=args.target_weekend,
        events_sent=args.events_sent,
        sent=_parse_bool_arg(args.sent, option_name="--sent"),
        send_reason=args.send_reason,
        served_marked=_parse_bool_arg(args.served_marked, option_name="--served-marked"),
    )
    _cleanup_payload_files(cleanup_candidates)
    _cleanup_transport_artifacts(get_cache_dir(config))
    print(json.dumps({"logged": logged, "detail": detail}, ensure_ascii=False))


def cmd_audit_run(args: argparse.Namespace) -> None:
    """Audit one logged scout run; only fail non-zero in strict mode."""
    from weekend_scout.config import load_config
    from weekend_scout.cache import audit_run

    config = load_config()
    result = audit_run(config, args.run_id, stage=args.stage)
    print(json.dumps(result, ensure_ascii=False))
    if args.strict and not result["ok"]:
        sys.exit(1)


def cmd_run(args: argparse.Namespace) -> None:
    """Print instructions for a manual /weekend-scout run."""
    print(json.dumps({
        "message": "Run /weekend-scout in Claude Code to start an automated scout.",
        "automation": "planned",
    }))


def _get_install_targets() -> dict[str, "Path"]:
    from pathlib import Path as _P
    return {
        "claude-code": _P.home() / ".claude"   / "skills" / "weekend-scout",
        "codex":       _P.home() / ".agents"   / "skills" / "weekend-scout",
        "openclaw":    _P.home() / ".openclaw" / "skills" / "weekend-scout",
    }


def _build_compact_cities_payload(cities: dict[str, list[str]]) -> dict[str, object]:
    """Build the compact init-skill city payload."""
    return {
        "tier1": cities.get("tier1", []),
        "tier2_count": len(cities.get("tier2", [])),
        "tier3_count": len(cities.get("tier3", [])),
    }


def _build_debug_payload(
    *,
    cities: dict[str, list[str]],
    cached_events: list[dict[str, object]],
    searches_this_week: list[str],
    broad_result: dict[str, object],
    targeted_by_country: dict[str, dict[str, str]],
    geonames_path: "Path",
) -> dict[str, object]:
    """Build debug-only data for the pretty-printed init command."""
    return {
        "searches_this_week": searches_this_week,
        "suggested_queries": {
            "vars": broad_result["vars"],
            "broad": broad_result["templates"],
            "targeted_by_country": targeted_by_country,
        },
        "cached_events": cached_events,
        "cities_full": cities,
        "phase_c_full": {
            "tier2": _build_targeted_city_cards(
                cities.get("tier2", []),
                searches_this_week=searches_this_week,
                targeted_by_country=targeted_by_country,
                geonames_path=geonames_path,
            ),
            "tier3": _build_targeted_city_cards(
                cities.get("tier3", []),
                searches_this_week=searches_this_week,
                targeted_by_country=targeted_by_country,
                geonames_path=geonames_path,
            ),
        },
    }


def _get_platform_detection_dirs() -> dict[str, tuple["Path", ...]]:
    """Return directories used only to detect whether a platform is present."""
    from pathlib import Path as _P
    return {
        "claude-code": (_P.home() / ".claude",),
        # Codex installs skills into ~/.agents/skills, but installations may expose
        # either ~/.codex or ~/.agents as a platform marker on disk.
        "codex":       (_P.home() / ".codex", _P.home() / ".agents"),
        "openclaw":    (_P.home() / ".openclaw",),
    }


def _resolve_platforms(platform_arg: str | None) -> list[str]:
    """Determine which platforms to install for."""
    targets = _get_install_targets()
    if platform_arg == "all":
        return list(targets.keys())
    if platform_arg:
        return [platform_arg]
    platform_detection_dirs = _get_platform_detection_dirs()
    detected = [
        name for name, base_dirs in platform_detection_dirs.items()
        if any(base_dir.exists() for base_dir in base_dirs)
    ]
    return detected if detected else ["claude-code"]


def _copy_tree(src: "Path", dst: "Path") -> None:
    """Recursively copy all files from src to dst."""
    import shutil as _shutil
    for item in src.rglob("*"):
        if item.is_file():
            rel = item.relative_to(src)
            target_file = dst / rel
            target_file.parent.mkdir(parents=True, exist_ok=True)
            _shutil.copy2(item, target_file)


def cmd_install_skill(args: argparse.Namespace) -> None:
    """Copy bundled skill files from the installed package to the global skills dir."""
    from pathlib import Path
    from weekend_scout.skill_install import copy_skill_tree
    skill_data_dir = Path(__file__).resolve().parent / "skill_data"
    if not skill_data_dir.exists():
        _print_error_and_exit(
            "skill_data directory not found in package",
            error_code="skill_data_missing",
            detail={"path": str(skill_data_dir)},
        )

    platforms = _resolve_platforms(args.platform)
    install_targets = _get_install_targets()

    results = []
    for platform in platforms:
        source_dir = skill_data_dir / platform
        if not source_dir.exists():
            results.append({"platform": platform, "status": "skipped",
                            "reason": f"no skill data for {platform}"})
            continue
        target_dir = install_targets[platform]
        copy_skill_tree(source_dir, target_dir, executable=sys.executable)
        results.append({"platform": platform, "status": "installed",
                        "path": str(target_dir)})

    print(json.dumps({"installed": results}, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="weekend_scout",
        description="Weekend Scout -- discover outdoor events near your city",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # setup
    p_setup = sub.add_parser("setup", help="Interactive first-run setup wizard")
    p_setup.add_argument(
        "--json", dest="json_data", default=None, metavar="JSON",
        help="Apply JSON config payload directly (no wizard)",
    )
    p_setup.add_argument(
        "--json-file", dest="json_file", default=None, metavar="PATH",
        help="Read JSON config payload from a UTF-8 .json file",
    )

    # config
    p_cfg = sub.add_parser("config", help="Show or set configuration")
    p_cfg.add_argument("key", nargs="?", help="Config key to set (omit to show all)")
    p_cfg.add_argument("value", nargs="?", help="Value to set")

    # reset
    p_reset = sub.add_parser("reset", help="Delete local config and cache for the active install")
    p_reset.add_argument("--yes", action="store_true", help="Confirm deletion of config.yaml and cache/")

    # init
    p_init = sub.add_parser("init", help="Load config + cities + cache for a scout run")
    p_init.add_argument("--city", help="Override home city")
    p_init.add_argument("--radius", help="Override search radius in km")

    # init-skill
    p_init_skill = sub.add_parser("init-skill", help="Load compact skill startup context")
    p_init_skill.add_argument("--city", help="Override home city")
    p_init_skill.add_argument("--radius", help="Override search radius in km")

    # phase-c-cities
    p_pcc = sub.add_parser("phase-c-cities", help="Load one on-demand phase-C city batch")
    p_pcc.add_argument("--run-id", required=True, dest="run_id", help="Run identifier from init-skill")
    p_pcc.add_argument("--tier", required=True, type=int, choices=[2, 3], help="Later city tier to request")
    p_pcc.add_argument("--offset", type=int, default=0, help="Filtered-batch offset")
    p_pcc.add_argument("--limit", type=int, default=6, help="Maximum number of city cards to return")
    p_pcc.add_argument("--covered-cities", default=None, help="Deprecated no-op kept for one-release compatibility")
    p_pcc.add_argument("--covered-cities-file", default=None, dest="covered_cities_file",
                       help="Deprecated no-op kept for one-release compatibility")
    p_pcc.add_argument("--searches-used", default=None, type=int, dest="searches_used",
                       help="Deprecated no-op kept for one-release compatibility")

    # phase-summary
    p_ps = sub.add_parser("phase-summary", help="Log one canonical phase_summary entry")
    p_ps.add_argument("--run-id", required=True, dest="run_id", help="Run identifier from init-skill")
    p_ps.add_argument("--phase", required=True, choices=["A", "B", "C", "D"], help="Run phase to summarize")
    p_ps.add_argument("--target-weekend", required=True, dest="target_weekend", help="ISO Saturday date")

    # score-summary
    p_ss = sub.add_parser("score-summary", help="Log one canonical flat score_summary entry")
    p_ss.add_argument("--run-id", required=True, dest="run_id", help="Run identifier from init-skill")
    p_ss.add_argument("--target-weekend", required=True, dest="target_weekend", help="ISO Saturday date")
    p_ss.add_argument("--total-pool", required=True, type=int, dest="total_pool", help="Total ranked pool size")
    p_ss.add_argument("--city-events-selected", required=True, type=int, dest="city_events_selected",
                      help="Number of selected home-city events")
    p_ss.add_argument("--trip-options", required=True, type=int, dest="trip_options",
                      help="Number of selected trip options")

    # prepare-delivery
    p_prep = sub.add_parser("prepare-delivery", help="Compute pre-send delivery stats for one run")
    p_prep.add_argument("--run-id", required=True, dest="run_id", help="Run identifier from init-skill")
    p_prep.add_argument("--target-weekend", required=True, dest="target_weekend", help="ISO Saturday date")
    p_prep.add_argument("--events-sent", required=True, type=int, dest="events_sent", help="Digest item count")

    # run-complete
    p_rc = sub.add_parser("run-complete", help="Log one canonical run_complete entry")
    p_rc.add_argument("--run-id", required=True, dest="run_id", help="Run identifier from init-skill")
    p_rc.add_argument("--target-weekend", required=True, dest="target_weekend", help="ISO Saturday date")
    p_rc.add_argument("--events-sent", required=True, type=int, dest="events_sent", help="Digest item count")
    p_rc.add_argument("--sent", required=True, help="Whether Telegram send succeeded (true/false)")
    p_rc.add_argument("--send-reason", required=True, dest="send_reason",
                      choices=["sent", "telegram_not_configured", "telegram_internal", "send_failed"],
                      help="Final delivery outcome")
    p_rc.add_argument("--served-marked", required=True, dest="served_marked",
                      help="Whether cache-mark-served was executed (true/false)")
    p_rc.add_argument("--uncovered-tier1", default=None, dest="uncovered_tier1",
                      help="Deprecated no-op kept for one-release compatibility")
    p_rc.add_argument("--uncovered-tier1-file", default=None, dest="uncovered_tier1_file",
                      help="Deprecated no-op kept for one-release compatibility")

    # audit-run
    p_audit = sub.add_parser("audit-run", help="Audit a logged scout run by run_id")
    p_audit.add_argument("--run-id", required=True, dest="run_id", help="Run identifier from init-skill")
    p_audit.add_argument("--stage", default="post_send", choices=["pre_send", "post_send"],
                         help="Audit stage: pre-send prerequisites or post-send validation")
    p_audit.add_argument("--strict", action="store_true",
                         help="Exit non-zero when the audit reports ok=false")

    # save
    p_save = sub.add_parser("save", help="Save discovered events to cache")
    save_group = p_save.add_mutually_exclusive_group(required=True)
    save_group.add_argument("--events", help="JSON array of event objects")
    save_group.add_argument("--events-file", dest="events_file",
                            help="Path to UTF-8 JSON array of event objects")
    save_group.add_argument("--from-session", action="store_true",
                            help="Load canonical event candidates from the run session file")
    p_save.add_argument("--run-id", default=None, dest="run_id", help="Run identifier from init")

    # send
    p_send = sub.add_parser("send", help="Send formatted message to Telegram")
    grp = p_send.add_mutually_exclusive_group(required=True)
    grp.add_argument("--message", help="Message text")
    grp.add_argument("--file", help="Path to file containing message text")
    p_send.add_argument("--run-id", default=None, dest="run_id",
                        help="Run identifier from init")

    # cache-query
    p_cq = sub.add_parser("cache-query", help="Query cached events for a weekend date")
    p_cq.add_argument("--date", required=True, help="ISO date (Saturday of target weekend)")

    # session-query
    p_sq = sub.add_parser("session-query", help="Query canonical session candidates for a run")
    p_sq.add_argument("--run-id", required=True, dest="run_id", help="Run identifier from init-skill")

    # prepare-digest
    p_pd = sub.add_parser("prepare-digest", help="Build deterministic scoring input from saved weekend cache rows")
    p_pd.add_argument("--date", required=True, help="ISO date (Saturday of target weekend)")

    # log-search
    p_ls = sub.add_parser("log-search", help="Log a completed search")
    p_ls.add_argument("--query", required=True, help="Search query string")
    p_ls.add_argument("--target-weekend", required=True, help="ISO date of target Saturday")
    p_ls.add_argument("--result-count", type=int, default=0, help="Number of results returned")
    p_ls.add_argument("--cities", help="JSON array of city names covered")
    p_ls.add_argument("--cities-file", dest="cities_file",
                      help="Path to UTF-8 JSON array of city names covered")
    p_ls.add_argument("--events", default=None, help="Optional JSON array of canonical event objects")
    p_ls.add_argument("--events-file", default=None, dest="events_file",
                      help="Path to UTF-8 JSON array of canonical event objects")
    p_ls.add_argument("--phase", default="broad", choices=["broad", "aggregator", "targeted", "verification"])
    p_ls.add_argument("--run-id", default=None, dest="run_id", help="Run identifier from init")
    p_ls.add_argument("--events-discovered", type=int, default=0, dest="events_discovered",
                      help="Deprecated manual event count; ignored when --events/--events-file is supplied")

    # log-action
    p_la = sub.add_parser("log-action", help="Append a structured action log entry")
    p_la.add_argument("--action", required=True, help="Action type (phase_start, score_summary, ...)")
    p_la.add_argument("--phase", default=None, help="Search phase context (A, B, C, D, ...)")
    p_la.add_argument("--detail", default=None, help="JSON object with action-specific data")
    p_la.add_argument("--detail-file", default=None, dest="detail_file",
                      help="Path to UTF-8 JSON object with action-specific data")
    p_la.add_argument("--run-id", default=None, dest="run_id", help="Run identifier from init")
    p_la.add_argument("--source", default="skill", help="Source: skill or python")
    p_la.add_argument("--target-weekend", default=None, dest="target_weekend", help="ISO Saturday date")

    # cache-mark-served
    p_cms = sub.add_parser("cache-mark-served", help="Mark weekend events as served")
    p_cms.add_argument("--date", required=True, help="ISO date (Saturday of target weekend)")
    p_cms.add_argument("--run-id", required=True, dest="run_id", help="Run identifier from init-skill")

    # format-message
    p_fm = sub.add_parser("format-message", help="Format scout message and write to file")
    p_fm.add_argument("--saturday", required=True, help="ISO date of target Saturday")
    p_fm.add_argument("--sunday", required=True, help="ISO date of target Sunday")
    p_fm.add_argument("--city-events", default="[]", help="JSON array of event dicts")
    p_fm.add_argument("--city-events-file", default=None, dest="city_events_file",
                      help="Path to UTF-8 JSON array of event dicts")
    p_fm.add_argument("--trips", default="[]", help="JSON array of trip option dicts")
    p_fm.add_argument("--trips-file", default=None, dest="trips_file",
                      help="Path to UTF-8 JSON array of trip option dicts")
    p_fm.add_argument("--stats-lines", default="[]", dest="stats_lines",
                      help="JSON array of plain-string stats lines to append after the digest")
    p_fm.add_argument("--stats-lines-file", default=None, dest="stats_lines_file",
                      help="Path to UTF-8 JSON array of plain-string stats lines to append after the digest")
    p_fm.add_argument("--notes-lines", default="[]", dest="notes_lines",
                      help="JSON array of plain-string notes/debug lines to append after the stats block")
    p_fm.add_argument("--notes-lines-file", default=None, dest="notes_lines_file",
                      help="Path to UTF-8 JSON array of plain-string notes/debug lines to append after the stats block")
    p_fm.add_argument("--output", default=None, help="Output file path (default: app cache dir)")
    p_fm.add_argument("--low-results", default=None, dest="low_results",
                      help="Pass 'true' to append a budget-increase hint to the message")
    p_fm.add_argument("--run-id", default=None, dest="run_id",
                      help="Run identifier from init")

    # install-skill
    p_is = sub.add_parser(
        "install-skill",
        help="Copy bundled skill files from the installed package to your global skills directory",
    )
    p_is.add_argument(
        "--platform",
        choices=["claude-code", "codex", "openclaw", "all"],
        default=None,
        help="Target platform (auto-detected if not specified)",
    )

    # find-city
    p_fc = sub.add_parser("find-city", help="Look up a city in the GeoNames database")
    p_fc.add_argument("--name", required=True, help="City name to search")
    p_fc.add_argument("--country", default=None, help="Optional country filter (full English name)")

    # download-data
    p_dd = sub.add_parser("download-data", help="Download GeoNames cities15000.zip into cache dir")
    p_dd.add_argument("--force", action="store_true", help="Re-download even if file already exists")

    # run
    sub.add_parser("run", help="Full automated run (instructions)")

    return parser


COMMANDS = {
    "setup": cmd_setup,
    "config": cmd_config,
    "reset": cmd_reset,
    "init": cmd_init,
    "init-skill": cmd_init_skill,
    "phase-c-cities": cmd_phase_c_cities,
    "phase-summary": cmd_phase_summary,
    "score-summary": cmd_score_summary,
    "prepare-delivery": cmd_prepare_delivery,
    "run-complete": cmd_run_complete,
    "audit-run": cmd_audit_run,
    "find-city": cmd_find_city,
    "save": cmd_save,
    "session-query": cmd_session_query,
    "prepare-digest": cmd_prepare_digest,
    "send": cmd_send,
    "cache-query": cmd_cache_query,
    "log-search": cmd_log_search,
    "log-action": cmd_log_action,
    "cache-mark-served": cmd_cache_mark_served,
    "format-message": cmd_format_message,
    "install-skill": cmd_install_skill,
    "download-data": cmd_download_data,
    "run": cmd_run,
}


def main() -> None:
    # Ensure Unicode output works on Windows (cp1251/cp850 consoles)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args()
    dispatch_command(args, parser)


if __name__ == "__main__":
    main()
