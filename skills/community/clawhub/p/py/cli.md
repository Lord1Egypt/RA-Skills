# Scripts and CLIs — Arguments, Exit Codes, Pipes

A script becomes a tool the moment someone else runs it in a pipeline or a cron job. These are the behaviors they will assume.

## The Skeleton

```python
def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    ...
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

- `main` returns an int and takes `argv` — that is what makes it testable without a subprocess (`testing.md`).
- The `if __name__` guard is not style: without it the body runs on import and again in every multiprocessing spawn child (Core Rule 9).
- Ship it as both `python -m mypkg` (a `__main__.py`) and a console entry point (`packaging.md`). The module form works before installation and in a debugger.

## argparse Without Surprises

- `type=` receives a string and may raise: `type=Path`, `type=int`, or your own function that raises `argparse.ArgumentTypeError` with a message the user can act on.
- Subcommands do not require a choice by default: `add_subparsers(dest="cmd", required=True)`, or a user typing just `tool` gets an `AttributeError` instead of the help text.
- `--flag` booleans: `action="store_true"` (default False) for the on-switch; `argparse.BooleanOptionalAction` (`python >=3.9`) generates `--flag/--no-flag` in one line.
- Prefix abbreviation is ON by default, so today's `--dry` is tomorrow's ambiguity when you add `--dry-run`, breaking scripts that relied on the short form. `allow_abbrev=False` in anything with users.
- `nargs="*"` yields `[]` when absent but `None` when the argument is not present at all with a `default=None` — pick `default=[]` deliberately and never mutate it.
- Mutually exclusive options: `parser.add_mutually_exclusive_group()`. Validation that argparse cannot express goes right after parsing, and calls `parser.error("...")` so the user gets usage + exit 2 rather than a traceback.
- Config precedence, stated once and implemented in this order: CLI flag > environment variable > config file > built-in default. Booleans from the environment need explicit parsing — `bool(os.getenv("DEBUG"))` is True for the string `"false"`.
- For a large multi-command tool, `click` or `typer` buys you completion, colors, and nesting; the stdlib is right for anything one file can hold.

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success — and nothing else may exit 0 |
| 1 | Generic failure (an uncaught exception also exits 1) |
| 2 | Usage error — argparse already uses this for bad arguments |
| 130 | Interrupted by Ctrl-C (128 + SIGINT) — the convention shells expect |
| 141 | SIGPIPE (128 + 13) — a downstream reader closed early, usually not an error |
| 137 / 143 | Killed by SIGKILL (OOM) / SIGTERM (`debugging.md`) |

`sys.exit("message")` prints the string to STDERR and exits 1 — convenient, and easy to misread as printing to stdout. `sys.exit(0)` inside a `try` still runs `finally` blocks, because `SystemExit` is an exception; `os._exit()` skips everything including buffer flushes, and is for post-fork children only.

## Streams

- stdout is for the OUTPUT (the data another program will consume); stderr is for logs, progress, and errors. A tool that prints progress to stdout cannot be piped.
- stdout is block-buffered when it is not a terminal: output can appear late, out of order relative to stderr, or be lost if the process is killed. `python -u`, `PYTHONUNBUFFERED=1`, or `print(..., flush=True)` at the points that matter. This is why Docker logs from Python containers appear in bursts.
- `UnicodeEncodeError` on output is the console's encoding, not your data's: set `PYTHONIOENCODING=utf-8`, or use `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` (`python >=3.7`) when you cannot control the environment.
- Reading stdin: `for line in sys.stdin` streams; `sys.stdin.read()` waits for EOF. Accept `-` as a filename meaning stdin — that is the convention every unix tool follows. `sys.stdin.buffer` for bytes.
- Piping into `head` raises `BrokenPipeError`, and Python also prints an ugly "Exception ignored" at shutdown. The documented fix:

```python
try:
    sys.exit(main())
except BrokenPipeError:
    os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
    sys.exit(141)
```

- Colour and progress bars only when `sys.stdout.isatty()`, and honour the `NO_COLOR` environment variable. Escape codes in a log file are noise nobody can grep.

## Signals and Interruption

- `signal.signal` can only be called from the main thread, and the handler runs between bytecodes — never inside a C call that is already blocking.
- SIGTERM (what a supervisor, Docker, or Kubernetes sends) has no default Python handler: the process dies immediately and `finally` blocks, context managers, and `atexit` do NOT run. Register one that raises `SystemExit` and cleanup starts working.
- Ctrl-C raises `KeyboardInterrupt` in the main thread only; a worker thread keeps running and can hold the process open unless it is a daemon (`concurrency.md`).
- Catch `KeyboardInterrupt` at the top level to exit 130 quietly instead of dumping a traceback that looks like a crash.

## Behaving Well In Automation

- Idempotent by default, and a `--dry-run` that prints exactly what the real run would do. This is what makes a destructive tool reviewable.
- Make the destructive path explicit (`--yes`, or a confirmation only when `stdin.isatty()`) — a prompt in a cron job hangs forever.
- Machine-readable output behind a flag (`--json`) so the tool is composable without parsing human text.
- Set the exit code from the result, not from "the code reached the end": partial failure in a batch should exit non-zero, and the summary belongs on stderr.
- Long jobs: log progress with a count and a rate to stderr, and make re-running after a crash safe (`files.md` atomic writes).
