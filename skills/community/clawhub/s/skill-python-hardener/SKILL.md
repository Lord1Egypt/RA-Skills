---
name: python-hardener
description: >
  Hardens Python scripts by applying a complete security review, clean-code
  refactoring, robust error handling, proper logging, and full docstring
  coverage — then produces a companion Markdown documentation file.

  Use this skill whenever the user uploads or references Python files and asks
  for any of the following (even if they only mention one):
  - security review, SQL injection check, shell injection, path traversal
  - error handling, try/except fixes, bare except removal
  - logging, RotatingFileHandler, proper log setup
  - clean code, refactoring, meaningful variable names
  - docstrings, type hints, parameter documentation
  - code review, code hardening, production-ready script
  - "fix this script", "improve this code", "make this safe"

  Also trigger when the user says things like "review and fix", "make this
  production-ready", "add proper error handling and logging", or uploads .py
  files alongside a review request. If multiple Python files are uploaded
  together, harden all of them.
---

# Python Hardener

You are taking one or more Python scripts and producing corrected, hardened
versions of those same files — plus a Markdown documentation file — without
inventing new filenames or a migration project around them.

## What to deliver

1. **The same Python files**, corrected in place. Keep original filenames exactly.
2. **One Markdown documentation file** named `<primary-script-name>.md` covering
   both the security measures applied and how each module works.

Do not create `.env.example`, migration guides, `requirements.txt`, or any file
not listed above unless the user explicitly asks for it.

---

## Analysis pass — what to look for

Read the entire file before making any changes. Build a mental list of issues
across four categories:

### Security
- **SQL/NoSQL injection** — table names, column names, or user input interpolated
  directly into query strings via f-strings or `%` formatting. Fix with allowlist
  validation (`assert table in frozenset({...})`); parameterised queries for values.
- **Shell injection** — any `subprocess` call that uses `shell=True` or joins a
  command into a single string. Fix with list-form calls and no `shell=True`.
- **Path traversal** — file paths constructed from user input without
  `Path.resolve()` and an allowlist check.
- **CWD mutation** — `os.chdir()` permanently changes process working directory.
  Replace with `subprocess.run(["git", "-C", repo_path, ...])` or equivalent.
- **Secrets in code** — API keys, passwords hardcoded. Flag for env-var migration.

### Error handling
- **Bare `except:`** — swallows every exception including `KeyboardInterrupt`,
  `SystemExit`, and `MemoryError`. Replace with specific types:
  `json.JSONDecodeError`, `subprocess.CalledProcessError`, `subprocess.TimeoutExpired`,
  `OSError`, `ValueError`, etc. Always log the caught exception.
- **Silent `pass`** in exception blocks — hides failures. Add at minimum a
  `logger.warning(...)` or `logger.error(...)` with the exception detail.
- **Missing finally / context managers** — database connections, file handles, or
  network sockets that are never closed. Use `with` statements or `contextmanager`.

### Performance / resource management
- **File opened on every call** — e.g. a `log()` function that opens the log file
  each time it runs. Configure handlers once (e.g. `RotatingFileHandler`) and reuse.
- **DB connection leaks** — `connect()` called in every method, connection never
  closed. Wrap in a `@contextmanager` that calls `conn.close()` in `finally`.
- **Module-level side effects** — `Path.mkdir()`, `sqlite3.connect()`, or network
  calls at import time. Move into `main()` or `__init__()`.
- **Non-atomic writes** — writing state/config files directly risks a torn write
  if the process is interrupted. Use `tempfile.mkstemp()` then `os.replace()`.

### Clean code
- Rename single-letter or cryptic variables to descriptive names.
- Break functions that do more than one thing.
- Add type hints to function signatures.

---

## Rewrite rules

Apply every fix from the analysis pass. Additionally:

**Logging** — Replace `print()` statements used for operational output and any
hand-rolled file-append logging with Python's `logging` module:
- Configure once via a setup function (not at module level, not per-call).
- Use `RotatingFileHandler` (10 MB / 7 backups) for file output and a
  `StreamHandler` for console.
- Read log level from an environment variable, falling back to `INFO`.
- Log errors with `logger.error("...", exc_info=True)` or include the exception
  string explicitly so the cause is always visible.

**Docstrings** — Add Google-style docstrings to every public function, method,
and class:

```python
def export_csv(self, table: str) -> Optional[Path]:
    """
    Exports a table as a CSV file.

    Args:
        table: Table name — must be in {'documents', 'skills', 'symlinks'}.

    Returns:
        Path to the generated CSV file, or None if the table is empty.

    Raises:
        ValueError: If the table name is not in the allowlist.
        sqlite3.Error: On database errors.
        OSError: On write errors.
    """
```

**Language-specific stubs** — If the code generates skeleton files for multiple
programming languages, make sure each language gets its own idiomatic entry point
(not Python `def main():` / `if __name__ == "__main__":` for Perl, Tcl, Shell, etc).

---

## Documentation file

Write a single Markdown file (`<primary-script-name>.md`) with these sections:

1. **Overview** — one-paragraph summary of what the script(s) do.
2. **Architecture** — ASCII diagram or table showing the main components and
   their relationships.
3. **Configuration** — environment variables consumed, with defaults.
4. **API / Functions** — per-module table of public functions (name, signature,
   what it does).
5. **Security** — table of threats addressed and the countermeasure applied.
6. **Error handling** — table mapping each function to the exceptions it handles
   and what happens on failure.

---

## Style constraints

- Preserve the original author's overall structure and naming conventions unless
  they are actively harmful (e.g., a function named `x` that does a critical thing).
- Do not add versioning, changelogs, or migration notes unless asked.
- Do not invent new filenames beyond the one documentation `.md`.
- If the user's `.env` already exists and is mentioned as the source of truth,
  do not create `.env.example`.

---

## Checklist before delivering

- [ ] Every bare `except:` replaced with specific exception type(s) + logging
- [ ] No `os.chdir()` — use `subprocess ... -C <path>` or `cwd=` argument instead
- [ ] SQL/shell injection vectors closed
- [ ] Connections / file handles closed via context manager
- [ ] Logging configured once, not per-call
- [ ] Atomic writes (`tempfile` + `os.replace()`) for state/config files
- [ ] All public functions have docstrings with Args/Returns/Raises
- [ ] Type hints on function signatures
- [ ] Module-level side effects moved into `main()` or `__init__()`
- [ ] Documentation `.md` file present and accurate
