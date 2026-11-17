# Subprocess — Running External Commands

The default line covers 90% of cases; every deviation from it should be a decision you can name.

```python
r = subprocess.run(
    ["git", "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True, timeout=30, cwd=repo,
)
sha = r.stdout.strip()
```

- `check=True` or you must inspect `r.returncode` yourself. Without it, a failed command returns quietly and you parse an empty string — the most common subprocess bug by a wide margin.
- `text=True` decodes with the locale encoding; add `encoding="utf-8"` when the child's output is UTF-8 regardless of the platform (`files.md`).
- `timeout=` on every call. A child that hangs hangs you (`debugging.md`).
- Argument list, not a string: quoting, spaces, and `$` in filenames stop existing as a problem.

## shell=True

- Only when you genuinely need shell features (pipes, globs, `&&`, redirection) and the whole command line is a literal you wrote.
- With any interpolated value it is command injection: `subprocess.run(f"grep {pattern} file", shell=True)` where `pattern` is `x; rm -rf ~` runs both. If you must build a shell string, every interpolated value goes through `shlex.quote`.
- On POSIX, `shell=True` runs `/bin/sh`, not bash — bashisms (`[[`, arrays, `pipefail`) fail with a syntax error. Call `["bash", "-c", script]` explicitly when you need bash.
- Prefer doing it in Python: a pipe is two `Popen`s or, more often, `run(...)` plus a Python transformation; a glob is `Path.glob`.
- Never `os.system`: no argument control, and its return value is a wait status (exit code × 256 on POSIX), not an exit code.

## Deadlocks and Streaming

- `Popen(..., stdout=PIPE)` then `p.wait()` deadlocks as soon as the child writes more than the pipe buffer (64 KiB on Linux): the child blocks writing, you block waiting. `communicate()` reads and waits together — use it, or `run()`, which does it for you.
- Two pipes (`stdout=PIPE, stderr=PIPE`) read sequentially deadlock the same way. `stderr=subprocess.STDOUT` merges them into one stream when the interleaving is acceptable; otherwise let `communicate()` handle both.
- Streaming output as it arrives:

```python
with subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, bufsize=1) as p:
    for line in p.stdout:
        handle(line.rstrip())
if p.returncode:                      # the with-block waits, but does not check
    raise subprocess.CalledProcessError(p.returncode, cmd)
```

- The child decides its own buffering: most programs block-buffer when stdout is a pipe instead of a terminal, so "nothing appears until it finishes" is the child's behavior, not yours. Fix it on their side: `PYTHONUNBUFFERED=1` for Python children, `stdbuf -oL` for C ones, or a pty if the tool has no flag.
- Gigabytes of output: `capture_output=True` holds it all in memory. Redirect to a file (`stdout=open(path, "wb")`) or consume the stream as it arrives.

## Timeouts, Signals, and Orphans

- `timeout=` kills the direct child only. A child that spawned its own children leaves them running: start with `start_new_session=True` and kill the group with `os.killpg(os.getpgid(p.pid), signal.SIGTERM)`.
- Escalate, do not start at SIGKILL: TERM, wait a few seconds, then KILL. SIGKILL leaves temp files and half-written output.
- `p.kill()` after a `TimeoutExpired` still requires a second `communicate()` to reap the process and drain its pipes.
- A `Popen` you never `wait()` on becomes a zombie in the process table. Use the context manager or `run()`.
- Ctrl-C in a terminal sends SIGINT to the entire foreground process group, so your child often dies before your handler runs — do not assume you get to clean up after it (`cli.md`).

## Environment and Path

- `env=` REPLACES the environment; `env={"TOKEN": t}` leaves the child with no `PATH`, no `HOME`, and a mystery "command not found". Always `env = {**os.environ, "TOKEN": t}` — and drop the variables the child should not see, because it inherits every secret otherwise (`security.md`).
- The program name is resolved against `PATH`, not against `cwd`: `run(["./script.sh"])` needs the explicit `./` and an executable bit; `cwd=` changes the child's directory but not how the program name resolves.
- `shutil.which("tool")` before running gives a clear error instead of a `FileNotFoundError` from deep inside a call stack — and `FileNotFoundError` from `run()` means the PROGRAM is missing, not a file argument.
- Windows: no fork, `shell=True` means `cmd.exe`, argument quoting rules differ, and `.bat`/`.cmd` files require `shell=True` or an explicit interpreter.

## Return Values

- `CalledProcessError` carries `.returncode`, `.stdout`, `.stderr` — log `e.stderr`, not just the exception, or you lose the only useful part.
- Exit codes above 128 mean killed by signal `code − 128` (137 = SIGKILL/OOM, 143 = SIGTERM). 127 is "command not found" from a shell, 126 "found but not executable".
- Non-zero is not always failure: `grep` exits 1 when it matches nothing, `diff` exits 1 when files differ. For these, drop `check=True` and branch on the specific code.

## When Not To Shell Out At All

Reach for the stdlib first: `shutil.copy2`/`copytree`/`rmtree` instead of `cp`/`rm`, `pathlib.glob` instead of `ls`, `tarfile`/`zipfile` instead of `tar`, `urllib`/`httpx` instead of `curl`, `os.replace` instead of `mv`. Each one removes a quoting bug, a portability difference, and a dependency on what is installed on the host.
