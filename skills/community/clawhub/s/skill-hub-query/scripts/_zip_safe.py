#!/usr/bin/env python3
"""ZIP list / extract helper -- works around Info-ZIP's non-ASCII filename mojibake.

Why this exists: Info-ZIP UnZip 6.00 (shipped by Debian/Ubuntu and many other
distros) does not honour the UTF-8 filename flag defined by the ZIP spec
(general purpose bit 11). It decodes UTF-8 filenames using the legacy local
codepage instead, so an entry like `references/mapping_table.json` written with
non-ASCII characters comes out as mojibake on disk (for example
`references/\\udcb5\\udce1...`).

The failure mode is nasty: the installed skill looks fine ("install succeeded"),
but any script inside it that opens the file by its real name raises
FileNotFoundError on the first run -- and the error points at the *installed*
skill, so it is very easy to misdiagnose as a bug in that skill rather than in
the installer.

`unzip -O <charset>` exists only in the Windows build; the Linux build rejects
it with a usage error, so there is no flag-level workaround. Python's `zipfile`
handles the UTF-8 flag correctly, so listing and extraction are delegated here.

Usage:
  python3 _zip_safe.py list <zip>              # one entry name per line (UTF-8)
  python3 _zip_safe.py extract <zip> <destdir> # extract with traversal defense

Exit codes: 0 success / 1 usage or IO error / 6 unsafe path detected
"""
import os
import sys
import zipfile
from pathlib import Path

_UTF8_FLAG = 0x800


def _force_utf8_stdio() -> None:
    """Force UTF-8 for stdio AND the filesystem encoding under C locale.

    On macOS environments without LANG (launchd, cron, bare ssh -- very common),
    macOS offers no C.UTF-8 locale, so PEP 538 coercion has nothing to coerce
    to and Python 3.7-3.10 falls back to ascii for BOTH stdout/stderr and
    sys.getfilesystemencoding():
      - printing a non-ASCII entry name (list output, error messages) raises
        UnicodeEncodeError;
      - Path.resolve()/realpath on a path containing non-ASCII names raises it
        too -- the filesystem encoding is independent of stdio, so reconfiguring
        streams alone is not enough (that was the first, insufficient fix).

    Fix: if the filesystem encoding is not UTF-8, set PYTHONUTF8=1 and exec
    ourselves with the same argv, letting interpreter-level UTF-8 mode take
    over every encoding uniformly. After re-exec the check passes and we
    continue. If exec is impossible, fall back to reconfiguring stdio only.
    """
    fs_enc = (sys.getfilesystemencoding() or "").lower()
    if "utf" in fs_enc:
        return  # filesystem already UTF-8; stdio shares the same mechanism
    if os.environ.get("_SHQ_ZIP_UTF8_REEXEC") != "1":
        env = dict(os.environ)
        env["PYTHONUTF8"] = "1"
        env["_SHQ_ZIP_UTF8_REEXEC"] = "1"
        try:
            os.execve(sys.executable, [sys.executable] + sys.argv, env)
        except OSError:
            pass  # exec unavailable (non-POSIX); fall through to reconfigure
    # Already re-exec'd, or exec failed: best-effort stdio reconfigure.
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        if stream is None:
            continue
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError, OSError):
            pass


_force_utf8_stdio()


def _decoded_name(info):
    """Best-effort correct filename for one zip entry.

    Two archive flavours exist in the wild and a naive reader breaks on one of
    them:

    * flag bit 11 SET   -> the name is UTF-8. `zipfile` decodes it correctly;
      Info-ZIP `unzip` 6.00 ignores the flag and re-encodes via the local
      codepage, which is exactly the mojibake this helper exists to avoid.
    * flag bit 11 UNSET -> the spec says the name is CP437, so `zipfile` decodes
      it as CP437. But many packers (older Info-ZIP, several CI zip steps) write
      raw UTF-8 bytes *without* setting the flag. Decoding those as CP437
      produces mojibake in the opposite direction -- e.g. a Chinese filename
      turns into `µÿáσ░äΦí¿`.

    So for unflagged entries we round-trip back to the original bytes and retry
    as UTF-8; if that decodes cleanly we trust it, otherwise we keep the CP437
    reading. Fully ASCII names are unaffected either way.
    """
    name = info.filename
    if info.flag_bits & _UTF8_FLAG:
        return name
    try:
        raw = name.encode('cp437')
    except UnicodeEncodeError:
        # zipfile already handed us a non-CP437 string; nothing to recover.
        return name
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        return name


def _entries(zf):
    """All entry names in the archive, with filename encoding normalised."""
    return [_decoded_name(i) for i in zf.infolist()]


def _unsafe(names):
    """Return absolute-path / directory-traversal entries.

    Same semantics as the previous awk-based check in install.sh.
    """
    bad = []
    for n in names:
        # Absolute paths: POSIX `/x`, Windows `C:\x` and `\\server\share`
        if n.startswith('/') or n.startswith('\\'):
            bad.append(f"absolute path: {n}")
            continue
        if len(n) > 1 and n[1] == ':':
            bad.append(f"absolute path: {n}")
            continue
        # Directory traversal: any path segment equal to `..`
        parts = n.replace('\\', '/').split('/')
        if any(p == '..' for p in parts):
            bad.append(f"traversal: {n}")
    return bad


def cmd_list(zip_path):
    with zipfile.ZipFile(zip_path) as zf:
        for n in _entries(zf):
            print(n)
    return 0


def cmd_extract(zip_path, dest):
    dest = Path(dest).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        infos = zf.infolist()
        names = [_decoded_name(i) for i in infos]

        bad = _unsafe(names)
        if bad:
            print("[error] zip contains unsafe paths; refusing to extract:",
                  file=sys.stderr)
            for b in bad:
                print(b, file=sys.stderr)
            return 6

        # Second line of defense: resolve every target up front and confirm it
        # lands inside dest. Catches symlink tricks and platform-specific quirks;
        # it does not replace the string check above.
        for n in names:
            target = (dest / n).resolve()
            if target != dest and dest not in target.parents:
                print(f"[error] extraction target escapes dest: {n}",
                      file=sys.stderr)
                return 6

        # Write entries out one by one using the CORRECTED name. `extractall`
        # cannot be used here: it would fall back to zipfile's own (possibly
        # CP437-mangled) `info.filename`, undoing the fix in _decoded_name.
        # A mid-extract failure (disk full, permission) cleans up the partially
        # written files so a half-installed directory is never mistaken for a
        # complete version.
        written: list[Path] = []
        for info, name in zip(infos, names):
            target = dest / name
            if info.is_dir() or name.endswith('/'):
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                with zf.open(info) as src, open(target, 'wb') as out:
                    written.append(target)
                    while True:
                        chunk = src.read(65536)
                        if not chunk:
                            break
                        out.write(chunk)
            except OSError as e:
                print(f"[error] write failed, aborted and cleaned up: {name}: {e}",
                      file=sys.stderr)
                for p in written:
                    try:
                        p.unlink()
                    except OSError:
                        pass
                return 1
            # Preserve the executable bit when the archive recorded UNIX modes
            # (scripts/*.sh in a skill package must stay runnable).
            mode = info.external_attr >> 16
            if mode & 0o111:
                target.chmod(target.stat().st_mode | 0o111)
    return 0


def main(argv):
    if len(argv) < 3:
        print(__doc__, file=sys.stderr)
        return 1
    op, zip_path = argv[1], argv[2]
    if not Path(zip_path).is_file():
        print(f"[error] zip not found: {zip_path}", file=sys.stderr)
        return 1
    try:
        if op == 'list':
            return cmd_list(zip_path)
        if op == 'extract':
            if len(argv) < 4:
                print("[error] extract requires <destdir>", file=sys.stderr)
                return 1
            return cmd_extract(zip_path, argv[3])
    except zipfile.BadZipFile as e:
        print(f"[error] corrupt or non-zip file: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"[error] IO error: {e}", file=sys.stderr)
        return 1
    print(f"[error] unknown operation: {op}", file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
