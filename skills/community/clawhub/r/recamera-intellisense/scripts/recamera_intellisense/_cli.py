"""Unified CLI dispatcher.

Usage::

    recamera <command> [key=value ...] [--key value ...] [--key=value ...]
    recamera <command> '{"key": "value", ...}'
    recamera <command> --help

Arguments are matched to the command function's keyword parameters and
coerced using its type annotations:

* ``str``               — passed through verbatim
* ``int`` / ``float``   — parsed numerically (``quota_limit_bytes=-1`` works)
* ``bool``              — strict: ``true/false``, ``yes/no``, ``on/off``, ``1/0``
* ``Optional[...]``     — ``null`` / ``none`` select ``None``
* ``List`` / ``Dict``   — inline JSON, or ``@path/to/file.json`` (``@-`` = stdin)

In the key=value form, any value may come from a file via ``@path``
(``token=@token.txt`` keeps secrets out of shell history); ``@@`` gives a
literal leading ``@``. A single argument starting with ``{`` is parsed as one
JSON object for the whole call (no ``@`` expansion there). Keys are
case-sensitive but dashes are normalized to underscores (``--device-name`` ==
``device_name``). Results print as pretty JSON; errors print the failing
command's usage and an example to stderr, exit non-zero.
"""

from __future__ import annotations

import inspect
import json
import sys
import typing
from typing import Any, Callable, Dict, Iterable, Tuple

if __name__ == "__main__" and __package__ is None:
    # Direct execution: make absolute imports work like `python3 -m`.
    import os

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from recamera_intellisense import (
        acoustic,
        apps,
        backup,
        capture,
        detection,
        device,
        files,
        gpio,
        image,
        model,
        notify,
        records,
        relay,
        rule,
        storage,
        system,
        video,
    )
    from recamera_intellisense._coerce import to_bool
    from recamera_intellisense._errors import RecameraError
else:
    from . import (
        acoustic,
        apps,
        backup,
        capture,
        detection,
        device,
        files,
        gpio,
        image,
        model,
        notify,
        records,
        relay,
        rule,
        storage,
        system,
        video,
    )
    from ._coerce import to_bool
    from ._errors import RecameraError

_MODULES = (
    device,
    system,
    image,
    rule,
    storage,
    relay,
    records,
    capture,
    gpio,
    model,
    acoustic,
    apps,
    video,
    notify,
    backup,
    detection,
    files,
)


# Parameters that exist for Python callers but are not valid CLI arguments.
CLI_EXCLUDE = {"raw"}


def _derive_schema(fn: Callable[..., Any]) -> Dict[str, set]:
    """required = params without defaults; optional = params with defaults."""
    params = inspect.signature(fn).parameters.values()
    empty = inspect.Parameter.empty
    return {
        "required": {p.name for p in params if p.default is empty} - CLI_EXCLUDE,
        "optional": {p.name for p in params if p.default is not empty} - CLI_EXCLUDE,
    }


def _collect() -> Tuple[Dict[str, Callable[..., Any]], Dict[str, Dict[str, set]]]:
    cmds: Dict[str, Callable[..., Any]] = {}
    schemas: Dict[str, Dict[str, set]] = {}
    for mod in _MODULES:
        for name, fn in getattr(mod, "COMMANDS", {}).items():
            if name in cmds:
                raise RuntimeError(f"Duplicate CLI command {name!r}")
            cmds[name] = fn
            schemas[name] = _derive_schema(fn)
    return cmds, schemas


COMMANDS, COMMAND_SCHEMAS = _collect()

# Shown on `--help` and after every usage error so callers self-correct in one retry.
EXAMPLES: Dict[str, str] = {
    "detect_local_device": "recamera detect_local_device host=192.168.1.100",
    "add_device": "recamera add_device name=cam1 host=192.168.1.100 token=sk_xxxx",
    "update_device": "recamera update_device device_name=cam1 token=sk_new",
    "remove_device": "recamera remove_device device_name=cam1",
    "get_device": "recamera get_device device_name=cam1",
    "list_devices": "recamera list_devices",
    "get_device_info": "recamera get_device_info device_name=cam1",
    "get_resource_info": "recamera get_resource_info device_name=cam1",
    "get_system_time": "recamera get_system_time device_name=cam1",
    "reboot_device": "recamera reboot_device device_name=cam1 confirm=true",
    "get_image_settings": "recamera get_image_settings device_name=cam1",
    "set_image_settings": (
        "recamera set_image_settings device_name=cam1 "
        "section=adjustment 'values={\"saturation\":80}'"
    ),
    "get_rule_system_info": "recamera get_rule_system_info device_name=cam1",
    "get_record_config": "recamera get_record_config device_name=cam1",
    "set_record_config": (
        "recamera set_record_config device_name=cam1 "
        "rule_enabled=true writer_format=JPG writer_interval_ms=0"
    ),
    "get_schedule_rule": "recamera get_schedule_rule device_name=cam1",
    "set_schedule_rule": "recamera set_schedule_rule device_name=cam1 schedule=null",
    "get_record_trigger": "recamera get_record_trigger device_name=cam1",
    "get_record_sources": "recamera get_record_sources device_name=cam1",
    "get_notify_config": "recamera get_notify_config device_name=cam1",
    "list_apps": "recamera list_apps device_name=cam1",
    "get_app_logs": "recamera get_app_logs device_name=cam1 app_id=acousticslab tail=100",
    "list_acoustic_models": "recamera list_acoustic_models device_name=cam1",
    "get_video_encode": "recamera get_video_encode device_name=cam1 stream=sub",
    "get_battery_status": "recamera get_battery_status device_name=cam1",
    "export_device_config": "recamera export_device_config device_name=cam1 output=./cam1-config.tar",
    "set_notify_config": (
        "recamera set_notify_config device_name=cam1 mode=1 "
        "'mqtt={\"url\":\"mqtt://broker.local\",\"port\":1883,\"topic\":\"cam/events\"}'"
    ),
    "start_app": "recamera start_app device_name=cam1 app_id=my-app",
    "stop_app": "recamera stop_app device_name=cam1 app_id=my-app",
    "restart_app": "recamera restart_app device_name=cam1 app_id=my-app",
    "set_acoustic_model": (
        "recamera set_acoustic_model device_name=cam1 "
        "workspace_id=<workspace-uuid> head_id=<head-uuid>"
    ),
    "set_video_encode": (
        "recamera set_video_encode device_name=cam1 stream=sub codec=H.265 max_rate=1024"
    ),
    "set_record_trigger": (
        "recamera set_record_trigger device_name=cam1 "
        "'trigger={\"kind\":\"timer\",\"interval_seconds\":60}'"
    ),
    "activate_http_trigger": "recamera activate_http_trigger device_name=cam1",
    "get_storage_status": "recamera get_storage_status device_name=cam1",
    "set_storage_slot": "recamera set_storage_slot device_name=cam1 by_dev_path=/dev/mmcblk0p8",
    "configure_storage_quota": (
        "recamera configure_storage_quota device_name=cam1 "
        "dev_path=/dev/mmcblk0p8 quota_limit_bytes=-1 quota_rotate=true"
    ),
    "storage_task_submit": (
        "recamera storage_task_submit device_name=cam1 "
        "action=FREE_UP dev_path=/dev/mmcblk0p8 confirm=true"
    ),
    "storage_task_status": (
        "recamera storage_task_status device_name=cam1 "
        "action=FREE_UP dev_path=/dev/mmcblk0p8"
    ),
    "storage_task_cancel": (
        "recamera storage_task_cancel device_name=cam1 "
        "action=FREE_UP dev_path=/dev/mmcblk0p8"
    ),
    "list_records": "recamera list_records device_name=cam1 path=2026-04-20 limit=100",
    "fetch_record": "recamera fetch_record device_name=cam1 path=2026-04-20/clip-001.jpg",
    "get_capture_status": "recamera get_capture_status device_name=cam1",
    "start_capture": "recamera start_capture device_name=cam1 format=JPG",
    "stop_capture": "recamera stop_capture device_name=cam1",
    "capture_image": "recamera capture_image device_name=cam1 timeout=30",
    "list_gpios": "recamera list_gpios device_name=cam1",
    "get_gpio_info": "recamera get_gpio_info device_name=cam1 pin_id=106",
    "set_gpio_value": "recamera set_gpio_value device_name=cam1 pin_id=106 value=1",
    "get_gpio_value": "recamera get_gpio_value device_name=cam1 pin_id=106 debounce_ms=100",
    "get_detection_models_info": "recamera get_detection_models_info device_name=cam1",
    "get_detection_model": "recamera get_detection_model device_name=cam1",
    "set_detection_model": (
        "recamera set_detection_model "
        "device_name=cam1 model_name=yolo11n fps=30"
    ),
    "get_active_acoustic_model": "recamera get_active_acoustic_model device_name=cam1",
    "get_detection_schedule": "recamera get_detection_schedule device_name=cam1",
    "set_detection_schedule": "recamera set_detection_schedule device_name=cam1 schedule=null",
    "get_detection_rules": "recamera get_detection_rules device_name=cam1",
    "set_detection_rules": (
        "recamera set_detection_rules device_name=cam1 "
        "'rules=[{\"name\":\"person\",\"label_filter\":[\"person\"]}]'"
    ),
    "get_detection_events": (
        "recamera get_detection_events "
        "device_name=cam1 start_unix_ms=1745150000000"
    ),
    "clear_detection_events": "recamera clear_detection_events device_name=cam1",
    "fetch_file": (
        "recamera fetch_file device_name=cam1 "
        "path=/mnt/rc_mmcblk0p8/reCamera/snapshot.jpg"
    ),
    "delete_file": (
        "recamera delete_file device_name=cam1 "
        "path=/mnt/rc_mmcblk0p8/reCamera/snapshot.jpg confirm=true"
    ),
    "get_intellisense_events": (
        "recamera get_intellisense_events "
        "device_name=cam1 start_unix_ms=1745150000000"
    ),
    "clear_intellisense_events": "recamera clear_intellisense_events device_name=cam1",
}


class _UsageError(Exception):
    """Raised for malformed invocations; main() prints usage + example."""


def _hints(fn: Callable[..., Any]) -> Dict[str, Any]:
    target = (
        fn
        if inspect.isfunction(fn) or inspect.ismethod(fn)
        else getattr(fn, "__call__", None)
    )
    if target is None:
        return {}
    try:
        hints = typing.get_type_hints(target)
    except (NameError, TypeError, AttributeError):  # unresolvable annotations
        return {}
    hints.pop("return", None)
    return hints


def _unwrap_optional(hint: Any) -> Any:
    """Reduce ``Optional[X]``/``Union[X, None]`` to ``X``; pass anything else through."""
    if typing.get_origin(hint) is typing.Union:
        inner = [a for a in typing.get_args(hint) if a is not type(None)]
        if inner:
            return inner[0]
    return hint


def _command_help(name: str) -> str:
    spec = COMMAND_SCHEMAS.get(name, {"required": set(), "optional": set()})
    req = sorted(spec.get("required", set()))
    opt = sorted(spec.get("optional", set()))
    fn = COMMANDS.get(name)
    hints = _hints(fn) if fn is not None else {}

    def _label(key: str) -> str:
        hint = hints.get(key)
        if hint is None:
            return f"{key}=<value>"
        hint = _unwrap_optional(hint)
        if hint is bool:
            return f"{key}=<true|false>"
        if hint is int:
            return f"{key}=<int>"
        if hint is float:
            return f"{key}=<number>"
        origin = typing.get_origin(hint)
        if origin is list or hint is list:
            return f"{key}=<json-array>"
        if origin is dict or hint is dict:
            return f"{key}=<json-object>"
        return f"{key}=<string>"

    parts = [f"recamera {name}"]
    parts.extend(_label(k) for k in req)
    if opt:
        parts.append("[" + "] [".join(_label(k) for k in opt) + "]")
    lines = ["usage: " + " ".join(parts)]
    if name in EXAMPLES:
        lines.append(f"example: {EXAMPLES[name]}")
    return "\n".join(lines)


def _print_help(stream=sys.stdout) -> None:
    stream.write(__doc__ or "")
    stream.write("\nAvailable commands:\n")
    for name in sorted(COMMANDS):
        spec = COMMAND_SCHEMAS.get(name, {"required": set(), "optional": set()})
        req = sorted(spec.get("required", set()))
        opt = sorted(spec.get("optional", set()))
        parts = []
        if req:
            parts.append("required=" + ",".join(req))
        if opt:
            parts.append("optional=" + ",".join(opt))
        stream.write(f"  {name:32s} {'  '.join(parts)}\n")
    stream.write("\nRun 'recamera <command> --help' for usage and an example.\n")


_NULL_TOKENS = {"null", "none"}


def _load_at_value(raw: str) -> Any:
    """Resolve ``@path`` (or ``@-`` for stdin) values; ``@@`` escapes a literal ``@``."""
    if raw.startswith("@@"):
        return raw[1:]
    if not raw.startswith("@"):
        return raw
    source = raw[1:]
    try:
        if source == "-":
            text = sys.stdin.read()
        else:
            with open(source, "r", encoding="utf-8") as fh:
                text = fh.read()
    except OSError as exc:
        raise _UsageError(f"cannot read value file {source!r}: {exc}") from exc
    return text.strip()


def _coerce(cmd: str, key: str, value: Any, hint: Any) -> Any:
    """Coerce *value* to *hint*; *value* is a raw CLI string or native JSON data."""
    where = f"{cmd}: argument {key!r}"
    if hint is None:
        return value
    origin = typing.get_origin(hint)
    if origin is typing.Union:
        if value is None or (isinstance(value, str) and value.strip().lower() in _NULL_TOKENS):
            return None
        hint = _unwrap_optional(hint)
        origin = typing.get_origin(hint)
    if hint is bool:
        try:
            return to_bool(value, where)
        except ValueError as exc:
            raise _UsageError(str(exc)) from exc
    if hint is int:
        if isinstance(value, bool):
            raise _UsageError(f"{where} must be an integer; got {value!r}")
        if isinstance(value, int):
            return value
        if isinstance(value, float) and value.is_integer():
            return int(value)
        if isinstance(value, str):
            try:
                return int(value.strip(), 10)
            except ValueError:
                pass
        raise _UsageError(f"{where} must be an integer; got {value!r}")
    if hint is float:
        if isinstance(value, bool):
            raise _UsageError(f"{where} must be a number; got {value!r}")
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            try:
                return float(value.strip())
            except ValueError:
                pass
        raise _UsageError(f"{where} must be a number; got {value!r}")
    if hint is str:
        if isinstance(value, str):
            return value
        if isinstance(value, (bool, list, dict)) or value is None:
            raise _UsageError(f"{where} must be a string; got {value!r}")
        return str(value)  # int/float spellings are unambiguous (e.g. a numeric name)
    if origin is list or hint is list:
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError as exc:
                raise _UsageError(
                    f"{where} must be a JSON array (or @file); got {value!r} ({exc})"
                ) from exc
        if not isinstance(value, list):
            raise _UsageError(f"{where} must be a JSON array; got {value!r}")
        return value
    if origin is dict or hint is dict:
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError as exc:
                raise _UsageError(
                    f"{where} must be a JSON object (or @file); got {value!r} ({exc})"
                ) from exc
        if not isinstance(value, dict):
            raise _UsageError(f"{where} must be a JSON object; got {value!r}")
        return value
    return value


def _parse_cli(name: str, argv: Iterable[str]) -> Dict[str, Any]:
    """Parse post-command argv into coerced kwargs.

    Two input forms, never mixed:

    * a single argument starting with ``{`` — one JSON object for the call;
    * ``key=value`` / ``--key=value`` / ``--key value`` tokens.
    """
    tokens = list(argv)
    if not tokens:
        return {}
    fn = COMMANDS[name]
    hints = _hints(fn)

    if len(tokens) == 1 and tokens[0].lstrip().startswith("{"):
        try:
            data = json.loads(tokens[0])
        except json.JSONDecodeError as exc:
            raise _UsageError(
                f"{name}: invalid JSON arguments: {exc}. "
                "Hint: flat key=value arguments also work — see usage below."
            ) from exc
        if not isinstance(data, dict):
            raise _UsageError(f"{name}: JSON arguments must be an object.")
        parsed: Dict[str, Any] = {}
        for k, v in data.items():
            key = str(k).replace("-", "_")
            parsed[key] = _coerce(name, key, v, hints.get(key))
        return parsed

    if any(t.lstrip().startswith("{") for t in tokens):
        raise _UsageError(
            f"{name}: cannot mix a JSON object with key=value arguments; use one form."
        )

    kwargs: Dict[str, Any] = {}
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.startswith("--"):
            body = token[2:]
            if not body:
                raise _UsageError(f"{name}: stray '--' argument.")
            if "=" in body:
                key, raw = body.split("=", 1)
            else:
                key = body
                i += 1
                if i >= len(tokens):
                    raise _UsageError(f"{name}: --{key} requires a value.")
                raw = tokens[i]
        elif "=" in token:
            key, raw = token.split("=", 1)
        else:
            raise _UsageError(
                f"{name}: expected key=value or --key value, got {token!r}."
            )
        key = key.strip().replace("-", "_")
        if not key:
            raise _UsageError(f"{name}: empty argument name in {token!r}.")
        if key in kwargs:
            raise _UsageError(f"{name}: duplicate argument {key!r}.")
        value = _load_at_value(raw)
        kwargs[key] = _coerce(name, key, value, hints.get(key))
        i += 1
    return kwargs


def _apply_aliases(name: str, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Rename `name` → `device_name` for selector commands, so a record emitted
    by `list_devices` can be forwarded verbatim."""
    spec = COMMAND_SCHEMAS.get(name)
    if spec is None:
        return kwargs
    allowed = set(spec.get("required", set())) | set(spec.get("optional", set()))
    if (
        "name" in kwargs
        and "device_name" not in kwargs
        and "device_name" in allowed
        and "name" not in allowed
    ):
        kwargs = dict(kwargs)
        kwargs["device_name"] = kwargs.pop("name")
    return kwargs


def _validate(name: str, kwargs: Dict[str, Any]) -> None:
    spec = COMMAND_SCHEMAS.get(name)
    if spec is None:
        return
    required = set(spec.get("required", set()))
    optional = set(spec.get("optional", set()))
    allowed = required | optional
    missing = required - set(kwargs)
    if missing:
        raise _UsageError(f"{name}: missing required argument(s): {sorted(missing)}")
    extra = set(kwargs) - allowed
    if extra:
        hint = f" Did you mean one of: {sorted(allowed)}?" if allowed else ""
        raise _UsageError(f"{name}: unknown argument(s): {sorted(extra)}.{hint}")


def main(argv: Iterable[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("-h", "--help", "help"):
        _print_help()
        return 0
    if args[0] == "list-commands":
        print("\n".join(sorted(COMMANDS)))
        return 0

    name = args[0]
    if name not in COMMANDS:
        print(f"unknown command: {name}", file=sys.stderr)
        _print_help(sys.stderr)
        return 2

    rest = args[1:]
    if any(a in ("-h", "--help") for a in rest):
        print(_command_help(name))
        return 0

    try:
        kwargs = _parse_cli(name, rest)
        kwargs = _apply_aliases(name, kwargs)
        _validate(name, kwargs)
    except _UsageError as exc:
        print(str(exc), file=sys.stderr)
        print(_command_help(name), file=sys.stderr)
        return 2

    try:
        result = COMMANDS[name](**kwargs)
    except RecameraError as exc:
        print(
            json.dumps({"error": str(exc), "code": exc.code, "status": exc.status}),
            file=sys.stderr,
        )
        return 1
    except (TypeError, ValueError) as exc:
        print(f"{name}: {exc}", file=sys.stderr)
        print(_command_help(name), file=sys.stderr)
        return 2

    # None -> null and {} -> {}: the distinction is part of the output contract.
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=False))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
