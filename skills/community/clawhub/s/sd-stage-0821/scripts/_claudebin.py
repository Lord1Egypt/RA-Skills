"""Resolve the `claude` CLI binary.

0.8.17 — under systemd, PATH is the minimal unit default (`/usr/bin:/bin`),
so a `claude` installed by npm/curl into a user-local bin is invisible to
`shutil.which()` even though it runs fine in the owner's interactive shell.
Every call site that shells out to claude must resolve through here: the
responder otherwise dies with FileNotFoundError on exactly the boxes that
run it as a service, and pulse advertises no brain so the platform stops
dispatching to the duck at all.

Falls back to the bare name so behaviour is unchanged wherever PATH already
works, and the existing FileNotFoundError handlers still see what they expect.
"""
import os
import shutil

ENV_OVERRIDE = 'SPACEDUCK_CLAUDE_BIN'

# Ordered by how commonly the installers land here. First executable wins.
_CANDIDATES = (
    '~/.local/bin/claude',
    '~/.npm-global/bin/claude',
    '~/.bun/bin/claude',
    '/usr/local/bin/claude',
    '/opt/homebrew/bin/claude',
)

_cached = None


def _usable(path):
    return bool(path) and os.path.isfile(path) and os.access(path, os.X_OK)


def resolve_claude(refresh=False):
    """Absolute path to the claude CLI, or 'claude' when nothing resolves."""
    global _cached
    if _cached and not refresh:
        return _cached

    override = os.environ.get(ENV_OVERRIDE)
    if _usable(override):
        _cached = override
        return _cached

    found = shutil.which('claude')
    if found:
        _cached = found
        return _cached

    for cand in _CANDIDATES:
        expanded = os.path.expanduser(cand)
        if _usable(expanded):
            _cached = expanded
            return _cached

    # Nothing found. Return the bare name rather than None so callers keep
    # their existing "claude CLI missing" error path instead of a TypeError.
    _cached = 'claude'
    return _cached


def claude_available():
    """True when a runnable claude CLI exists anywhere we look."""
    resolved = resolve_claude()
    return resolved != 'claude' or bool(shutil.which('claude'))


# --- deleted-cwd guard -----------------------------------------------------
# 2026-09-02 — the second way a supervised responder dies. The listener is a
# long-lived process started with `directory=<dir>`; when that directory is
# later removed or replaced (container overlay path rotated, skill dir
# reinstalled by update.sh), every process in the tree keeps a cwd pointing at
# a deleted inode. Absolute-path file I/O keeps working, so the listener looks
# healthy and keeps delivering pecks — but the claude CLI hard-fails:
#     error: The current working directory was deleted, so that command
#     didn't work. Please cd into a different directory and try again.
# Result is the exact "inbox fills up, nothing ever replies" symptom. Every
# call site that shells out to claude must therefore also pin a cwd that is
# known to exist.

_SAFE_CWD_CANDIDATES = ('~/.space-duck', '~', '/tmp')


def safe_cwd():
    """A directory that definitely exists, for use as subprocess cwd=."""
    for cand in _SAFE_CWD_CANDIDATES:
        expanded = os.path.expanduser(cand)
        if os.path.isdir(expanded):
            return expanded
    return '/'


def ensure_cwd():
    """chdir out of a deleted cwd. Returns the cwd in effect afterwards.

    Cheap and idempotent: os.getcwd() raises FileNotFoundError exactly when
    the process is parked on a deleted directory, which is the only case we
    need to repair. Fixing it in-process also fixes every child we spawn.
    """
    try:
        return os.getcwd()
    except (FileNotFoundError, OSError):
        target = safe_cwd()
        try:
            os.chdir(target)
        except Exception:
            return target
        return target
