# Files and Encodings — Reading, Writing, Not Losing Data

Two rules cover most of this file: declare the encoding at every boundary, and never let a partially written file take the place of a good one.

## Encoding

- `open(path)` uses the platform's default encoding, not UTF-8: cp1252 on Windows, ASCII under `LANG=C` in a lean container. The same code reads a file on your laptop and raises `UnicodeDecodeError: ... byte 0x93 in position 12` in CI. Write `encoding="utf-8"` on every text `open`, `read_text`, `write_text`, and `subprocess` call (Core Rule 8).
- Find the ones you missed: `python -X warn_default_encoding` (`python >=3.10`) emits an `EncodingWarning` at each site. `PYTHONUTF8=1` / `python -X utf8` forces UTF-8 process-wide as a stopgap for code you cannot edit; PEP 686 makes that the default in `python >=3.15`.
- Files exported from Excel start with a BOM: read them with `encoding="utf-8-sig"` (strips it) — otherwise the first column name is `"﻿id"` and every dict lookup on `"id"` fails.
- `errors="replace"` belongs only at a display boundary. Applying it to data silently substitutes `�` and destroys the bytes you needed.
- Bytes in, bytes out: read binary (`"rb"`) when the content is not text. Round-tripping unknown bytes through `str` corrupts them unless you use `errors="surrogateescape"`, which is also how paths with invalid encodings survive.
- Unicode equality is not byte equality: macOS filesystems hand back NFD (`e` + combining accent) where Linux gives NFC. Two visually identical names compare unequal. Normalize before comparing: `unicodedata.normalize("NFC", s)`.

## Paths

- `pathlib` by default: `Path("data") / "in.csv"`, `p.with_suffix(".json")`, `p.read_text(encoding="utf-8")`, `p.stem`, `p.parent`, `p.exists()`.
- Anchor relative paths to the code, not the caller's cwd: `HERE = Path(__file__).resolve().parent`. A script that works from the project root and fails from anywhere else is this bug.
- Joining with an absolute second element DISCARDS the first: `Path("/srv/data") / "/etc/passwd"` is `/etc/passwd`, and `os.path.join` does the same. Any user-supplied path component needs the containment check in `security.md`.
- `.resolve()` follows symlinks and normalizes `..`; `.absolute()` does neither. Compare and store resolved paths, or the same file has two names.
- `Path.glob("*.csv")` is one level, `rglob` recurses; neither matches dotfiles. For large trees `os.scandir` avoids a second `stat()` per entry and is several times faster than `os.walk`+`os.path.isdir`.
- Package data files are NOT filesystem paths: `importlib.resources.files("mypkg") / "schema.json"` works when the package is a zip or an installed wheel (`packaging.md`).

## Writing Without Losing Data

```python
tmp = path.with_suffix(path.suffix + ".tmp")
with open(tmp, "w", encoding="utf-8") as f:
    f.write(payload)
    f.flush()
    os.fsync(f.fileno())      # durability: bytes on disk, not just in the page cache
os.replace(tmp, path)          # atomic on the same filesystem, on POSIX and Windows
```

- `os.replace` overwrites atomically; `os.rename` raises on Windows when the destination exists. Same-filesystem only — a temp file in `/tmp` and a target in `/var` is a copy, not an atomic swap, so create the temp beside the target.
- Skip the `fsync` for caches and scratch output; keep it for anything a crash must not lose. Full durability also needs the directory fsynced on POSIX.
- Appending from multiple processes: writes under the pipe/PIPE_BUF size are atomic in `"a"` mode on POSIX, larger ones interleave. If two processes must write one file, give them a lock or a queue instead.
- There is no portable file lock in the stdlib: `fcntl.flock` on POSIX, `msvcrt.locking` on Windows, both advisory. The portable primitive is an exclusive create: `os.open(lock, os.O_CREAT | os.O_EXCL)`, with a stale-lock policy you write down.

## Temp Files

- `tempfile.NamedTemporaryFile(delete=False)` when another process must open it; on Windows the file cannot be reopened while the handle is live, so close first. `tempfile.TemporaryDirectory()` as a context manager cleans up even on exception.
- Never build a temp path yourself (`/tmp/myapp-{pid}`): it is a symlink race and a collision (`security.md`). `mkstemp` returns an OS-level fd — wrap it in `os.fdopen` or you leak the descriptor.

## CSV

- `open(path, newline="")` for both reading and writing with the `csv` module. Without it, files written on Windows get a blank line between rows, and quoted fields containing newlines split into phantom rows.
- Never split a CSV line on `,` yourself: quoted fields legally contain commas, quotes, and newlines. `csv.reader` handles all three.
- Everything comes back as `str` — there are no types in CSV. Convert explicitly, and expect empty strings where you wanted `None`.
- `_csv.Error: field larger than field limit (131072)` on a legitimate large field: raise it with `csv.field_size_limit(10**7)`.
- `csv.DictWriter` needs `fieldnames` up front and raises on extra keys (`extrasaction="ignore"` to drop them).

## JSON

- `json.dumps` cannot serialize `datetime`, `Decimal`, `set`, `bytes`, or dataclasses: pass `default=` (or `cls=`) and decide the representation once, centrally.
- Dict keys become strings: `{1: "a"}` round-trips to `{"1": "a"}`. Silent, lossy, and a classic source of "the key disappeared after caching".
- `allow_nan` is True by default, so `float("nan")` and `inf` are emitted as bare `NaN`/`Infinity` — which is NOT valid JSON and blows up in other languages' parsers. Pass `allow_nan=False` to find them at the source.
- Floats round-trip exactly through `repr`, but `Decimal("0.10")` becomes `0.1` unless you serialize it as a string. For money, string in and string out (`types.md`).
- `ensure_ascii=True` (default) escapes every non-ASCII character; set `ensure_ascii=False` plus an explicit UTF-8 encoding for human-readable output.
- Untrusted input: `json.loads` is memory-safe but not size-safe — a 500 MB body becomes a 2 GB object graph. Cap the read length before parsing.

## Large Files

- `for line in f` streams with buffering; `f.read()` loads everything. `f.readlines()` is the same mistake with extra steps.
- Binary chunks: `iter(functools.partial(f.read, 1 << 16), b"")` reads 64 KiB at a time until EOF.
- Random access over a big file: `mmap` gives you slices without loading it; the OS pages it in and out.
- Counting or filtering lines is I/O-bound; parallelizing it usually does nothing (`performance.md`).
- Compressed files stream too: `gzip.open(path, "rt", encoding="utf-8")` is a drop-in for text mode.
