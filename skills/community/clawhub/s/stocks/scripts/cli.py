"""
Command-line runner for this skill, so agents never have to write Python.

Usage:
  python scripts/cli.py list                       # every function and its parameters
  python scripts/cli.py <function> key=value ...   # call one function

Values: numbers, true/false/null and [json lists] are converted; anything else is text.
"""
import asyncio
import inspect
import json
import logging
import os
import sys

MODULE = "yfinance_ai"
SETUP = "python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt   (run inside the skill folder)"


def parse_value(raw):
    lowered = raw.strip().lower()
    if lowered in ("true", "false"):
        return lowered == "true"
    if lowered in ("null", "none"):
        return None
    if raw.strip()[:1] in ("[", "{"):
        try:
            return json.loads(raw)
        except ValueError:
            return raw
    for cast in (int, float):
        try:
            return cast(raw)
        except ValueError:
            pass
    return raw


def public_methods(tools):
    return {
        name: method for name, method in inspect.getmembers(tools, predicate=inspect.ismethod)
        if not name.startswith("_")
    }


def signature_text(method):
    params = []
    for name, param in inspect.signature(method).parameters.items():
        if name.startswith("__"):
            continue
        params.append(name if param.default is inspect.Parameter.empty else f"{name}={param.default!r}")
    return ", ".join(params)


def main(argv):
    logging.basicConfig(level=logging.WARNING)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        module = __import__(MODULE)
    except ImportError as e:
        print(f"Missing dependency ({e}). Set up the skill first:\n  {SETUP}", file=sys.stderr)
        return 2
    tools = module.Tools()
    methods = public_methods(tools)

    if len(argv) < 2 or argv[1] in ("list", "help", "-h", "--help"):
        for name, method in methods.items():
            doc = (inspect.getdoc(method) or "").strip().splitlines()
            print(f"{name}({signature_text(method)})" + (f"\n    {doc[0]}" if doc else ""))
        return 0

    name = argv[1]
    if name not in methods:
        print(f"Unknown function '{name}'. Run: python scripts/cli.py list", file=sys.stderr)
        return 2
    args, kwargs = [], {}
    for item in argv[2:]:
        key, sep, value = item.partition("=")
        if sep and key.isidentifier():
            kwargs[key] = parse_value(value)
        else:
            args.append(parse_value(item))
    try:
        inspect.signature(methods[name]).bind(*args, **kwargs)
    except TypeError as e:
        print(f"{e}. Usage: {name}({signature_text(methods[name])})", file=sys.stderr)
        return 2

    result = methods[name](*args, **kwargs)
    if inspect.isawaitable(result):
        result = asyncio.run(result)
    if isinstance(result, str):
        print(result)
    else:
        print(json.dumps(result, indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
