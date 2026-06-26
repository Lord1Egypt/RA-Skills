"""Unified CLI dispatcher.

Usage::

    python3 -m recamera_intellisense <command> ['<json-args>']
    recamera <command> ['<json-args>']

JSON args are a single object whose keys match the function keyword arguments.
Results print as pretty JSON; errors exit non-zero with the message on stderr.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Callable, Dict, Iterable, Tuple

from . import (
    capture,
    detection,
    device,
    files,
    gpio,
    model,
    records,
    relay,
    rule,
    storage,
)
from ._errors import RecameraError

_MODULES = (
    device,
    rule,
    storage,
    relay,
    records,
    capture,
    gpio,
    model,
    detection,
    files,
)


def _collect() -> Tuple[Dict[str, Callable[..., Any]], Dict[str, Dict[str, set]]]:
    cmds: Dict[str, Callable[..., Any]] = {}
    schemas: Dict[str, Dict[str, set]] = {}
    for mod in _MODULES:
        for name, fn in getattr(mod, "COMMANDS", {}).items():
            if name in cmds:
                raise RuntimeError(f"Duplicate CLI command {name!r}")
            cmds[name] = fn
        for name, spec in getattr(mod, "COMMAND_SCHEMAS", {}).items():
            schemas[name] = spec
    return cmds, schemas


COMMANDS, COMMAND_SCHEMAS = _collect()


def _print_help(stream=sys.stdout) -> None:
    stream.write("recamera <command> ['<json-args>']\n\n")
    stream.write("Available commands:\n")
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


def _parse_args(raw: str) -> Dict[str, Any]:
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON arguments: {exc}")
    if not isinstance(data, dict):
        raise SystemExit("JSON arguments must be an object")
    return data


def _apply_aliases(name: str, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize common argument aliases.

    ``list_devices`` emits records keyed by ``name`` (the device's own
    identifier), while selector commands such as ``get_device`` /
    ``remove_device`` expect ``device_name``. Agents often forward the
    list-devices payload verbatim, so transparently rename ``name`` →
    ``device_name`` when the command's schema accepts ``device_name`` and
    does not already accept ``name`` (e.g. ``add_device``).
    """
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
        raise SystemExit(f"{name}: missing required arg(s): {sorted(missing)}")
    extra = set(kwargs) - allowed
    if extra:
        raise SystemExit(f"{name}: unknown arg(s): {sorted(extra)}")


def main(argv: Iterable[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("-h", "--help", "help"):
        _print_help()
        return 0
    if args[0] == "list-commands":
        print("\n".join(sorted(COMMANDS)))
        return 0

    name = args[0]
    raw = args[1] if len(args) > 1 else "{}"
    if name not in COMMANDS:
        print(f"unknown command: {name}", file=sys.stderr)
        _print_help(sys.stderr)
        return 2

    kwargs = _parse_args(raw)
    kwargs = _apply_aliases(name, kwargs)
    _validate(name, kwargs)
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
        return 2

    if result is None:
        print("{}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=False))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
