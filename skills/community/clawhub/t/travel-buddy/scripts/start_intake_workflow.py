#!/usr/bin/env python3
"""Start the required Travel Buddy intake sequence.

Use this entry point for a new Travel Buddy request. It starts the one-time
reusable-profile form when no valid local profile exists; otherwise it starts
the current-trip form with the selected profile's stable defaults.

Usage: python start_intake_workflow.py [--workspace PATH] [--profile PROFILE_ID] [--assistant auto|codex|claude|none] [--language zh|en] [--detach]
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from travel_workspace import DEFAULT_WORKSPACE, profile_filename, validate_profile


SCRIPT_DIR = Path(__file__).resolve().parent
PROFILE_INTAKE_SERVER = SCRIPT_DIR / "serve_profile_intake.py"
TRIP_INTAKE_SERVER = SCRIPT_DIR / "serve_trip_intake.py"

# Both intake servers announce the traveller's link as `OPEN THIS LOCAL LINK: <url>` and flush it
# immediately. After --detach the parent can no longer see that on a pipe it owns, so this prefix
# is what it recovers the link from in the child's log file. The URL cannot be reconstructed:
# each server mints a single-use token and only prints it, so guessing http://127.0.0.1:<port>/
# would hand the traveller a link the server itself rejects.
LOCAL_LINK_PREFIX = "OPEN THIS LOCAL LINK: "

# How long the parent waits for a detached server to bind and answer its own port. Binding a
# loopback socket takes milliseconds; this budget is almost entirely interpreter start-up, and it
# is generous on purpose because the failure mode of being too impatient is killing a server that
# was about to work. Beyond it, something is wrong and saying so beats waiting silently.
DETACH_READY_TIMEOUT_SECONDS = 30.0
DETACH_POLL_SECONDS = 0.1

# What the link file is, and why it is treated as a credential from here down.
#
# serve_trip_intake.py's own banner tells the traveller that the token in the link "is what proves
# the page is the one this terminal opened". In the blocking mode that proof lives for exactly as
# long as one terminal line. --detach has to put it somewhere a caller with no live pipe can still
# read it, and that changes what it is: a single-use credential at rest, in the traveller's own
# workspace, one directory above their saved profile. The first version of this mode wrote it with
# whatever the umask allowed -- measured at 0644, `-rw-r--r--`, world-readable -- and never removed
# it. Two runs against one workspace therefore left two files, the older naming a server that had
# been dead for hours, and every later run added another. That is the opposite of what SKILL.md's
# profile rules and references/profile-and-storage.md promise about this skill's local storage:
# traveller data is written deliberately and narrowly, never incidentally and never left lying
# around. A caller told to read `<workspace>/.intake-<port>.url` and globbing `.intake-*.url` picks
# up whichever sorted first -- measured as the dead one -- and hands the traveller a link that was
# never served, one port over from the very failure run_detached() reasons about below.
LINK_FILE_MODE = 0o600
LINK_FILE_GLOB = ".intake-*.url"
LINK_FILE_TMP_GLOB = ".intake-*.url.tmp"
# re.ASCII on purpose. `"٥٣٩٠٠".isdigit()` is True and `int()` accepts it, and so does a bare `\d`,
# so a name-parser written the obvious way would decide `.intake-٥٣٩٠٠.url` was one of ours and
# delete a file this script cannot have written. Only the ASCII digits the kernel's port numbers
# are formatted with count.
#
# `[1-9]\d{0,4}` rather than `\d{1,5}` for the same reason one step further in: this pattern
# decides what gets deleted, so it has to match exactly the names this script produces and nothing
# that merely looks like them. `f".intake-{port}.url"` of an int never emits a leading zero, so
# `.intake-012.url` is somebody else's file even though it reads as port 12, and `.intake-0.url`
# names a port the kernel never hands out.
LINK_FILE_NAME_RE = re.compile(r"^\.intake-([1-9]\d{0,4})\.url(?:\.tmp)?$", re.ASCII)

# Both intake forms are served with `window.TRAVEL_BUDDY_PROFILE_INTAKE=` / `..._TRIP_INTAKE=`
# injected straight after `<head>`, and neither the token rejection (a text/plain 403) nor an
# unrelated program that happens to hold a recycled port can produce it. So this marker is what
# separates "something answers on that port" from "the intake server this record names is still
# there", which is the distinction the whole finding is about.
INTAKE_PAGE_MARKER = "window.TRAVEL_BUDDY_"
LIVE_LINK_TIMEOUT_SECONDS = 2.0
LIVE_LINK_SNIFF_BYTES = 65536

# How the watcher decides its server is gone. Three consecutive silent probes rather than one,
# because a single refused connection is a worse thing to act on than a slow one: acting on it
# deletes the link file of a server the traveller is still typing into. Fifteen seconds of
# tolerance costs nothing -- nobody is waiting on this file to disappear -- and the connect probe
# is cheap enough that a five-second interval is invisible next to a form that takes minutes.
WATCHER_POLL_SECONDS = 5.0
WATCHER_DEAD_STRIKES = 3

# The watcher itself, run as `python -c ...` rather than as a file next to this one.
#
# Something has to delete the link file at the moment its server stops answering, and it cannot be
# this process: --detach returns in about a second and the server it started outlives it by
# minutes. It cannot be the server either -- serve_profile_intake.py and serve_trip_intake.py know
# nothing about a file this script invented, and the profile server does not even exit at the
# handover (measured: pid stays alive, its port goes from answering to refused while the chained
# current-trip form runs on a thread in the same process). So the parent starts one more detached
# process whose only job is to outlive the server, notice the silence, and remove the file.
#
# It is inline source and not scripts/intake_link_watcher.py for two reasons. A second file would
# have to be listed in README.md and README_CN.md or tests/test_packaging.py fails the build, and
# more importantly the watcher must keep working when the rest of the tree does not: it is still
# running an hour later, after a `git checkout` or a half-finished edit that would make an import
# raise. Nothing here is imported, so nothing here can be broken out from under it.
#
# The identity stamp matters. Ports get reused, so between this server dying and this watcher
# noticing, a new --detach run can reserve the same port and write a new `.intake-<port>.url`.
# Deleting that would destroy a live run's record. The watcher therefore only ever removes a file
# whose `pid` and `started_at` are still the ones it was started for, and re-checks that
# immediately before the unlink rather than only at the top of the loop.
LINK_WATCHER_SOURCE = """
import json, os, socket, sys, time

url_path = sys.argv[1]
port = int(sys.argv[2])
owner_pid = int(sys.argv[3])
started_at = sys.argv[4]
poll = float(sys.argv[5])
strikes_needed = int(sys.argv[6])
stop_command = sys.argv[7]


def answers():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.settimeout(0.5)
        return probe.connect_ex(("127.0.0.1", port)) == 0


def still_ours():
    # None: the file is gone, somebody else already cleaned up. False: a newer run owns this
    # filename now. True: it is still the record this watcher was started for -- including when
    # the read failed transiently, because refusing to watch on one unreadable poll is how a
    # crashed watcher leaves the token on disk forever.
    try:
        with open(url_path, encoding="utf-8") as handle:
            record = json.load(handle)
    except FileNotFoundError:
        return None
    except (OSError, ValueError):
        return True
    return record.get("pid") == owner_pid and record.get("started_at") == started_at


strikes = 0
while True:
    if still_ours() is not True:
        sys.exit(0)
    strikes = 0 if answers() else strikes + 1
    if strikes >= strikes_needed:
        break
    time.sleep(poll)

if still_ours() is not True:
    sys.exit(0)
try:
    os.remove(url_path)
except FileNotFoundError:
    sys.exit(0)
except OSError as exc:
    print("INTAKE LINK FILE COULD NOT BE REMOVED: %s: %s -- it still holds a one-time token."
          % (url_path, exc), flush=True)
    sys.exit(1)
print("INTAKE LINK FILE REMOVED: %s -- 127.0.0.1:%d stopped answering, so that URL and the "
      "one-time token in it are dead and must not be given to anyone. If the process is still "
      "running, the profile form has handed over to the current-trip form on a new port, "
      "announced above as CURRENT-TRIP INTAKE URL:. Stop it with: %s"
      % (url_path, port, stop_command), flush=True)
"""


def valid_profiles(workspace: Path) -> list[Path]:
    profiles_dir = workspace / "profiles"
    if not profiles_dir.is_dir():
        return []
    valid: list[Path] = []
    for path in sorted(profiles_dir.glob("*.json")):
        try:
            profile = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not validate_profile(profile):
            valid.append(path)
    return valid


def run(command: list[str]) -> int:
    """Run an intake server in the foreground, blocking until the traveller submits.

    This is the right mode only when the caller can background the whole command itself, which
    is what SKILL.md means by "background is not a preference". The server flushes its link and
    then sits in serve_forever() for however long the form takes to fill, so in a foreground
    tool call this return statement is what holds the link hostage. --detach exists for harnesses
    with no way to background anything; see run_detached().
    """
    return subprocess.run(command, check=False).returncode


def reserve_loopback_port() -> int:
    """Choose the port the detached server will bind, before it is started.

    The parent has to know the port up front for two reasons: it is the name of the two files
    this mode writes (.intake-<port>.url and .intake-<port>.log), and it is what the parent
    probes to decide the server is really answering rather than merely still alive. Letting the
    child pick with --port 0 would mean discovering the port only by parsing the log, which is
    the same thing this function does without a window in which the parent knows nothing.

    Binding to port 0 and closing hands back a port the kernel had free a moment ago; between
    that moment and the child's own bind another process could take it. That race is not papered
    over -- the child then exits with "Could not start local intake server", and run_detached()
    fails loudly with that text rather than reporting a link nobody is serving.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def port_answers(port: int) -> bool:
    """True when something accepts a loopback connection on this port.

    A live child process is not the same claim: Popen.poll() says the interpreter is running,
    which it also is while it imports modules, reads a profile, or dies three lines later. The
    traveller's link is only real once the socket accepts, so that is what is tested. The probe
    connects and drops immediately; BaseHTTPRequestHandler treats an empty request as a closed
    connection and logs nothing.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.settimeout(0.5)
        return probe.connect_ex(("127.0.0.1", port)) == 0


def link_is_live(url: str, port: int) -> bool:
    """True when this exact recorded link still serves the intake form.

    port_answers() is deliberately not enough here, and the difference is the whole reason stale
    link files are dangerous rather than merely untidy. Ports are recycled: a `.intake-8080.url`
    left by a run that ended yesterday names a port some unrelated program may be holding today,
    so "the port answers" would call that record live and a reader would hand its dead token to
    the traveller. What the record actually claims is that *this URL* serves the form, so that is
    what gets tested -- the same claim tests/test_intake_workflow.py verifies by fetching the URL
    and looking for the page, rather than by asking whether a socket is open.

    The GET is fenced to loopback and to the port in the filename first. The URL comes out of a
    file in the workspace, and a file is something a user or another program can edit; without the
    fence, editing one line of it would turn this cleanup pass into a request to any host the
    editor chose.
    """
    if not url or not port_answers(port):
        return False
    parsed = urllib.parse.urlsplit(url)
    try:
        recorded_port = parsed.port
    except ValueError:
        # A port that will not parse as an integer at all -- the record is not one we wrote.
        return False
    if parsed.scheme != "http" or parsed.hostname != "127.0.0.1" or recorded_port != port:
        return False
    try:
        with urllib.request.urlopen(url, timeout=LIVE_LINK_TIMEOUT_SECONDS) as response:
            if response.status != 200:
                return False
            body = response.read(LIVE_LINK_SNIFF_BYTES).decode("utf-8", "replace")
    except (urllib.error.URLError, OSError, ValueError):
        # A refused connection, a 403 from the token guard, a timeout, a program that speaks
        # something other than HTTP on a recycled port: none of them is the server this record
        # names, and every one of them means the link is dead.
        return False
    return INTAKE_PAGE_MARKER in body


def link_file_port(path: Path) -> int | None:
    """The loopback port a link file names, or None when this script cannot have written it.

    None is not "assume zero" and not "assume stale": it is the signal that the file is outside
    what this code knows, and the caller leaves it alone and says so out loud. Deleting files in
    the traveller's workspace on a guess is the one outcome worse than leaving one behind.
    """
    match = LINK_FILE_NAME_RE.match(path.name)
    if not match:
        return None
    port = int(match.group(1))
    # Anything above 65535 is not a port the kernel ever handed this script, so a file naming one
    # was not written here. It also keeps such a number away from connect_ex(), which raises
    # OverflowError rather than returning a refusal -- an unhandled crash in a cleanup pass, on a
    # filename anyone can create in the workspace.
    return port if port <= 65535 else None


def recorded_url(path: Path) -> str:
    """The URL a link file claims, or "" when it cannot be read back as one.

    An empty string makes link_is_live() return False without a probe, which is the right
    reading: a record whose URL cannot be recovered cannot be vouched for, so it must never be
    treated as a live link to hand over.
    """
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    url = record.get("url") if isinstance(record, dict) else None
    return url if isinstance(url, str) else ""


def open_owner_only(path: Path):
    """Open a file for writing that is never, even for an instant, readable by anyone else.

    `path.open("w")` creates at 0666 & ~umask, which on this machine measured as 0644 -- and the
    token is written into that file a moment later, so the world-readable window is not
    theoretical, it is where the credential lands. The mode argument to os.open() closes the
    window for a new file, and fchmod() closes it for one that already exists: O_CREAT applies its
    mode only when it creates, so an 0644 log left by an earlier run would otherwise keep its old
    permissions through a fresh open. fchmod acts on the descriptor rather than the path, so a
    file swapped in between the two calls cannot receive the permissions meant for this one.

    Windows has no os.fchmod and its os.open() mode argument only controls the read-only bit; the
    hasattr guard keeps this importable and working there, where the equivalent protection comes
    from the profile directory's own ACL rather than from mode bits.
    """
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, LINK_FILE_MODE)
    try:
        if hasattr(os, "fchmod"):
            os.fchmod(fd, LINK_FILE_MODE)
        return os.fdopen(fd, "w", encoding="utf-8")
    except BaseException:
        # os.fdopen() takes ownership of the descriptor only once it returns; if it raised, this
        # is the only thing left that can close it, and a leaked fd on a file holding a token is
        # not a leak to shrug at.
        os.close(fd)
        raise


def write_link_record(url_path: Path, record: dict) -> None:
    """Publish the link record so no reader ever sees a half-written or wide-open version.

    Written to a sibling temporary file and moved into place with os.replace(), which is atomic:
    the watcher and any polling caller see either the previous complete record or the new one,
    never the empty middle of an O_TRUNC. The move is also what fixes an already-existing 0644
    file from before this mode was hardened -- replace() swaps in the new inode with its 0600,
    instead of writing fresh secrets into an old file's permissions.

    The temporary name is derived from the port, not from a random suffix, because the port is
    already this run's exclusive reservation: no concurrent run can be writing the same temporary,
    and a crash leaves exactly one predictable file that clear_stale_link_files() knows to remove.
    """
    tmp_path = url_path.with_name(url_path.name + ".tmp")
    try:
        with open_owner_only(tmp_path) as handle:
            handle.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
        os.replace(tmp_path, url_path)
    except BaseException:
        with contextlib.suppress(OSError):
            tmp_path.unlink(missing_ok=True)
        raise


def clear_stale_link_files(workspace: Path, reserved_port: int) -> tuple[list[Path], list[Path]]:
    """Remove every dead link file in this workspace, not only the one for this run's port.

    The narrow version of this -- unlink `.intake-<reserved_port>.url` and nothing else -- was
    almost useless in practice, because reserve_loopback_port() asks the kernel for a free port
    and gets a different one nearly every time. Measured: two runs against one workspace, the
    first server killed, left `.intake-53865.url` and `.intake-53871.url` side by side, the older
    one naming a port that no longer answered and still holding its token at `-rw-r--r--`. A
    workspace used for a few trips accumulates one of those per run, permanently.

    Liveness, not age, decides. The banner this mode prints tells the caller not to rerun the
    command while a traveller is filling the form, but people do, and a run that deleted the
    record of the server they are typing into would take away the only copy of its stop command.
    So a file whose link still serves the form is left exactly where it is.

    The reserved port is the one exception, cleared whether or not something answers there. What
    answers on it now cannot be the server the old record names -- that server is gone, this run
    just reserved its port -- so an answer means an unrelated program has taken it, which is the
    case where the old record is at its most misleading and this run is about to fail loudly
    anyway when its child cannot bind.

    Returns the files removed and the ones left alone as unrecognised, so the caller can report
    both rather than deleting or ignoring anything silently.
    """
    removed: list[Path] = []
    unrecognised: list[Path] = []
    for path in sorted(workspace.glob(LINK_FILE_GLOB)) + sorted(workspace.glob(LINK_FILE_TMP_GLOB)):
        port = link_file_port(path)
        if port is None:
            unrecognised.append(path)
            continue
        if path.name.endswith(".tmp"):
            # Debris from a write that was interrupted between os.open() and os.replace(). It is
            # never a record anyone reads, and it can still hold a token, so it goes unconditionally.
            path.unlink(missing_ok=True)
            removed.append(path)
            continue
        if port != reserved_port and link_is_live(recorded_url(path), port):
            continue
        path.unlink(missing_ok=True)
        removed.append(path)
    return removed, unrecognised


def read_local_link(log_path: Path) -> str | None:
    """Recover the traveller's tokenised link from the detached child's log, or None yet.

    Only lines that are already newline-terminated are considered. A print() of a short string
    with flush=True reaches the file in one write, but "short" is a property of this particular
    message rather than a guarantee, and half a URL handed to a traveller is worse than waiting
    one more 100ms poll: it fails in the browser, where nobody can tell a truncated link from a
    rejected token.
    """
    try:
        text = log_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        # The child may not have created the file yet, or the filesystem may be refusing us.
        # Either way there is no link to report on this poll; the timeout is what escalates.
        return None
    for line in text.split("\n")[:-1]:
        if line.startswith(LOCAL_LINK_PREFIX):
            url = line[len(LOCAL_LINK_PREFIX):].strip()
            if url:
                return url
    return None


def detached_popen(command: list[str], log_handle) -> subprocess.Popen:
    """Start the intake server so it outlives this process, on POSIX and on Windows both.

    plugin.json advertises "Runs under any assistant", and the harnesses that need --detach at
    all are the ones with no background primitive -- which is a property of the harness, not of
    the operating system. A hand-rolled double fork would be POSIX-only and would silently make
    this flag a lie on Windows, so the platform's own primitive is used on each side:
    start_new_session=True (setsid) on POSIX, DETACHED_PROCESS|CREATE_NEW_PROCESS_GROUP on
    Windows. Both mean the same thing here: no controlling terminal, own process group, so the
    server survives the parent exiting and a Ctrl-C in the parent's terminal does not reach it.

    The flags are read with getattr because they exist only in the Windows subprocess module;
    importing them unconditionally would make this file fail to load on the platform it is
    normally used on.
    """
    kwargs: dict[str, object] = {
        "stdin": subprocess.DEVNULL,
        "stdout": log_handle,
        "stderr": subprocess.STDOUT,
        "close_fds": True,
    }
    if os.name == "nt":
        kwargs["creationflags"] = (getattr(subprocess, "DETACHED_PROCESS", 0)
                                   | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0))
    else:
        kwargs["start_new_session"] = True
    return subprocess.Popen(command, **kwargs)


def stop_command_for(pid: int) -> str:
    """A copy-pasteable way to stop the detached server.

    Nothing else on the machine knows what this process is once the parent exits. The negative
    PID on POSIX is the process group, which start_new_session made the child the leader of, so
    one signal also takes the chained current-trip server it may have started.
    """
    if os.name == "nt":
        return f"taskkill /PID {pid} /T /F"
    return f"kill -TERM -{pid}"


def start_link_watcher(url_path: Path, port: int, owner_pid: int, started_at: str,
                       stop_command: str, log_handle) -> subprocess.Popen:
    """Start the process that deletes the link file when the link it names stops answering.

    Deliberately in its own session, via the same detached_popen() the server uses. The stop
    command this mode prints is `kill -TERM -<server pid>`, the whole process group, and a watcher
    inside that group would be killed by the very event it exists to clean up after -- leaving the
    token on disk exactly when the server is gone. Being outside the group also means it is never
    what a user's Ctrl-C reaches.

    Its one line of output goes to the same log the caller is already polling, because the link
    file is where the stop command lives and removing it would otherwise take that away with no
    trace. This is a hygiene measure, not a precondition: run_detached() treats a watcher that
    fails to start as a warning, since refusing a working intake server over an uncollected
    temporary file would trade the traveller's form for a tidy directory.
    """
    command = [
        sys.executable, "-c", LINK_WATCHER_SOURCE,
        str(url_path), str(port), str(owner_pid), started_at,
        str(WATCHER_POLL_SECONDS), str(WATCHER_DEAD_STRIKES), stop_command,
    ]
    return detached_popen(command, log_handle)


def fail_detached(message: str, log_path: Path) -> int:
    """Refuse a detached start out loud, quoting whatever the child managed to say.

    A detach that silently produces no server is worse than a blocking run, because the caller
    reports a link that was never served: the traveller opens it, gets nothing, and the model is
    left believing intake happened. So this exits non-zero and prints the child's captured
    output verbatim -- usually one line such as "ERROR: Could not start local intake server:
    [Errno 48] Address already in use", which names the fix. The empty case is stated explicitly
    rather than printed as blank space, because "no output" is itself the diagnosis when a
    server never reached its first print.
    """
    try:
        captured = log_path.read_text(encoding="utf-8", errors="replace").strip()
    except OSError as exc:
        captured = f"(the log at {log_path} could not be read back: {exc})"
    print(f"ERROR: {message}", file=sys.stderr)
    print(f"--- captured output of the detached intake server ({log_path}) ---", file=sys.stderr)
    print(captured or "(the server produced no output at all before it stopped)", file=sys.stderr)
    print("--- end of captured output ---", file=sys.stderr)
    # 3 rather than 2: 2 is this script's usage/selection error, and a caller that retries on
    # "bad arguments" must not retry a detach that failed for an occupied port.
    return 3


def run_detached(command: list[str], workspace: Path, port: int) -> int:
    """Start an intake server in the background when the harness itself cannot background it.

    The defect this exists for: opencode, Cursor, Cline and Codex offer no non-blocking command
    primitive, and this script's only mode was subprocess.run(), which blocks in serve_forever()
    for the minutes a traveller spends filling the form. The link therefore never reached the
    traveller at all, and the harness's command timeout eventually killed the server mid-fill.
    A model in that position has no honest exit: `intake_context.method: html_form` needs the
    intake file the blocked server never wrote, and `chat_fallback` needs `declined_verbatim` --
    the traveller's own words declining the form -- which they never said, because they were
    never offered it. render_final_trip_html.py and save_trip_deliverables.py both require one
    of those, correctly and with no bypass, so the remaining moves were to invent a quote or to
    abandon the save. That is the mechanism by which trip details went unexecuted on those
    harnesses: not a missing rule, a missing verb.

    So the parent does the waiting instead of the caller: it starts the child in its own session,
    polls until the child's port actually answers, writes the link and PID where they can be read
    later, prints both, and exits 0 within seconds. Everything the server says from then on --
    including the `TRAVEL BUDDY TRIP INPUT: <path>` sentinel that arrives minutes later, and the
    chained current-trip URL when the profile form hands over -- keeps streaming into the log
    file, which is what the caller polls in place of a live pipe.
    """
    try:
        workspace.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"ERROR: could not use the workspace {workspace}: {exc}", file=sys.stderr)
        return 3
    log_path = workspace / f".intake-{port}.log"
    url_path = workspace / f".intake-{port}.url"
    # Clear both before starting. Ports get reused, and a stale .url from an earlier run on this
    # port is a link to a server that is gone; leaving it in place on a failed start is exactly
    # the "reported a link that was never served" failure, one run delayed. Truncating the log
    # matters for the same reason in reverse: read_local_link() would otherwise happily return
    # the previous run's URL and this run would call itself ready.
    #
    # The sweep is over the whole workspace and not just this port because this port is almost
    # never the one the last run used -- reserve_loopback_port() takes whatever the kernel offers.
    # See clear_stale_link_files() for the measurement that made that obvious.
    try:
        removed, unrecognised = clear_stale_link_files(workspace, port)
    except OSError as exc:
        stuck = getattr(exc, "filename", None) or url_path
        print(f"ERROR: could not clear the stale link file {stuck}: {exc}", file=sys.stderr)
        return 3
    for path in removed:
        print(f"CLEARED STALE INTAKE LINK FILE: {path}", flush=True)
    for path in unrecognised:
        # Left in place rather than deleted, because this script cannot have written it and
        # guessing is how cleanup code eats a file somebody wanted. Said out loud rather than
        # ignored, because a caller globbing .intake-*.url will still find it and must not read
        # it as a live link.
        print(f"WARNING: {path} looks like an intake link file but does not name a loopback port "
              f"this script could have written, so it was left alone. Do not treat it as a live "
              f"link.", file=sys.stderr, flush=True)

    command = [*command, "--port", str(port)]
    try:
        # Owner-only for the same reason as the link file: every line the server prints goes here,
        # and the first of them is `OPEN THIS LOCAL LINK:` with the one-time token in it. Unlike
        # the link file the log is meant to outlive its server -- it carries the
        # `TRAVEL BUDDY TRIP INPUT: <path>` sentinel the caller polls for, long after the form is
        # submitted -- so its permissions are the only lever there is on it.
        log_handle = open_owner_only(log_path)
    except OSError as exc:
        print(f"ERROR: could not open the detached server log {log_path}: {exc}", file=sys.stderr)
        return 3
    with log_handle:
        try:
            process = detached_popen(command, log_handle)
        except OSError as exc:
            print(f"ERROR: could not start the detached intake server: {exc}", file=sys.stderr)
            return 3

        url: str | None = None
        deadline = time.monotonic() + DETACH_READY_TIMEOUT_SECONDS
        while True:
            if url is None:
                url = read_local_link(log_path)
            exited = process.poll()
            if url and port_answers(port):
                break
            if exited is not None:
                # Checked after the ready test, not before: a child can print its link, bind its
                # port and still be racing us: readiness is about the socket, not the pid.
                return fail_detached(
                    f"the detached intake server exited with code {exited} before it served a "
                    f"link on 127.0.0.1:{port}.", log_path)
            if time.monotonic() >= deadline:
                process.terminate()
                return fail_detached(
                    f"the detached intake server did not answer 127.0.0.1:{port} within "
                    f"{DETACH_READY_TIMEOUT_SECONDS:.0f}s; it has been stopped.", log_path)
            time.sleep(DETACH_POLL_SECONDS)

        # A URL that does not name the port we reserved means the child bound something else and
        # every path here -- the file names, the readiness probe, the stop command -- is about a
        # different server than the link. Assert it rather than hand over the mismatch.
        if f"127.0.0.1:{port}" not in url:
            process.terminate()
            return fail_detached(
                f"the detached intake server advertised {url!r}, which is not the reserved "
                f"loopback port {port}; it has been stopped.", log_path)

        started_at = datetime.now().astimezone().isoformat()
        record = {
            "url": url,
            "pid": process.pid,
            "port": port,
            "log_path": str(log_path),
            "stop_command": stop_command_for(process.pid),
            "started_at": started_at,
            "command": command,
            # The record states its own liveness test, in the file, because the reader is usually
            # a model that was told "read <workspace>/.intake-<port>.url" and has no way to tell
            # this file apart from one a dead server left behind. `pid` cannot answer that
            # question: measured at the profile-to-trip handover, the pid stays alive while the
            # recorded port goes from answering to refused, because the current-trip form runs on
            # a thread inside the same process on a new port. What the record actually claims is
            # that this URL serves the form, so that is the test it hands the reader.
            "live_check": (
                f"GET {url} — HTTP 200 whose body contains {INTAKE_PAGE_MARKER!r} means this link "
                f"is live. Anything else — connection refused, a 403 from the token guard, a page "
                f"without that marker — means this file is stale: the server is gone, the one-time "
                f"token in `url` is dead, and the URL must not be given to anyone."),
            # Filled in below. null with a `watcher_error` means nothing is going to remove this
            # file on its own, so whoever reads it should run the live_check above rather than
            # trusting the file's existence.
            "watcher_pid": None,
            "watcher_error": None,
        }
        try:
            write_link_record(url_path, record)
        except OSError as exc:
            process.terminate()
            return fail_detached(
                f"the server started but its link could not be recorded at {url_path}: {exc}. "
                f"It has been stopped rather than left running unrecorded.", log_path)

        # Written once before the watcher starts so the watcher has a file to claim, then once
        # more to record which process claimed it. The stamp the watcher matches on -- pid and
        # started_at -- is identical in both versions, so a watcher that reads between the two
        # sees its own record either way.
        watcher: subprocess.Popen | None = None
        try:
            watcher = start_link_watcher(
                url_path, port, process.pid, started_at, record["stop_command"], log_handle)
        except OSError as exc:
            record["watcher_error"] = str(exc)
            print(f"WARNING: the intake server is running normally, but the watcher that would "
                  f"delete {url_path} when its link dies could not be started: {exc}. That file "
                  f"holds a one-time token, so delete it once the form is submitted; the next "
                  f"--detach run in this workspace clears it too.", file=sys.stderr, flush=True)
        else:
            record["watcher_pid"] = watcher.pid
        try:
            write_link_record(url_path, record)
        except OSError as exc:
            # Not fatal, and specifically not a reason to stop a server that is serving. The first
            # write succeeded, so the link, the pid, the stop command and the live_check are all
            # already on disk at the right mode; only the watcher's pid is missing from them.
            print(f"WARNING: could not record the watcher pid in {url_path}: {exc}",
                  file=sys.stderr, flush=True)

    # Same `OPEN THIS LOCAL LINK:` prefix the blocking mode prints, so a caller that already
    # greps for it needs no second parser to support --detach.
    print(f"OPEN THIS LOCAL LINK: {url}", flush=True)
    print(f"INTAKE LINK FILE: {url_path}", flush=True)
    print(f"INTAKE SERVER LOG: {log_path}", flush=True)
    print(f"INTAKE SERVER PID: {process.pid} — stop it with: {record['stop_command']}", flush=True)
    if watcher is not None:
        print(f"INTAKE LINK FILE WATCHER PID: {watcher.pid} — it deletes {url_path.name} when "
              f"127.0.0.1:{port} stops answering, so the token in it does not outlive the server.",
              flush=True)
    print(
        "GIVE THE LINK ABOVE TO THE TRAVELLER, then poll the log file for "
        "`TRAVEL BUDDY TRIP INPUT: <path>` and continue from that file. Do not rerun this "
        "command while waiting: a second run opens a second server on a second port, and the "
        "traveller is already typing into the first. When the profile form hands over to the "
        "current-trip form, its URL appears in the same log as `CURRENT-TRIP INTAKE URL:`. "
        "The link file above holds a one-time token and exists only while its link answers: it "
        "is deleted when the server stops, and its `live_check` field states the test to run "
        "before trusting any `.intake-*.url` you did not just create.",
        flush=True,
    )
    return 0


def start(command: list[str], *, detach: bool, workspace: Path) -> int:
    """Run an intake server either way, so every call site gets --detach for free."""
    if not detach:
        return run(command)
    return run_detached(command, workspace, reserve_loopback_port())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Start the one-time profile and current-trip Travel Buddy intake workflow.")
    parser.add_argument("--workspace", default=str(DEFAULT_WORKSPACE), help="Workspace containing reusable profiles and trip plans")
    parser.add_argument("--profile", default=None, help="Existing reusable profile ID; required only when more than one valid profile exists")
    parser.add_argument("--assistant", choices=("auto", "codex", "claude", "none"), default="auto", help="Assistant to start automatically after the current-trip form submits")
    parser.add_argument("--edit-profile", action="store_true", help="Reopen the saved profile for review and editing before the current-trip form")
    parser.add_argument(
        "--detach", action="store_true",
        help="Start the intake server in its own session, print its link and PID, and exit 0. "
             "Use this when the harness has no way to run a command in the background; the "
             "server's output, including TRAVEL BUDDY TRIP INPUT, streams to "
             "<workspace>/.intake-<port>.log for you to poll.")
    parser.add_argument(
        "--language", choices=("zh", "en"), default=None,
        help="Language the forms open in. Default: the saved profile's preferred output language, "
             "else the language that profile was filled in, else zh; a first-time traveller's trip "
             "form follows the profile they just saved.")
    # argv is a parameter so the tests can drive this the way a caller does, through main(),
    # instead of asserting on internals that a caller never touches. A --detach path proved by
    # calling run_detached() directly would not prove the flag reaches it.
    args = parser.parse_args(argv)
    # Passed on only when given: each server resolves the rest from the profile it holds, and the
    # profile server must be able to tell "the traveller asked for zh" from "nobody said".
    language = ["--language", args.language] if args.language else []
    workspace = Path(args.workspace).expanduser()
    profiles = valid_profiles(workspace)

    if args.profile:
        try:
            selected = workspace / "profiles" / profile_filename(args.profile)
        except ValueError as exc:
            print(f"ERROR: Invalid profile ID: {exc}", file=sys.stderr)
            return 2
        if selected not in profiles:
            print("ERROR: The requested reusable profile does not exist or is invalid in this workspace.", file=sys.stderr)
            return 2
    elif not profiles:
        print("NO REUSABLE PROFILE FOUND: starting the one-time local profile form.", flush=True)
        return start([sys.executable, str(PROFILE_INTAKE_SERVER), "--workspace", str(workspace), "--next-trip", "--assistant", args.assistant, *language],
                     detach=args.detach, workspace=workspace)
    elif len(profiles) == 1:
        selected = profiles[0]
    else:
        print("PROFILE SELECTION REQUIRED: more than one reusable profile is available.", file=sys.stderr)
        for path in profiles:
            print(f"- {path.stem}", file=sys.stderr)
        print("Restart with --profile PROFILE_ID. No profile data was changed.", file=sys.stderr)
        return 2

    print(f"USING REUSABLE PROFILE: {selected}", flush=True)
    if args.edit_profile:
        print("REOPENING THE SAVED PROFILE FOR EDITING; the current-trip form follows automatically.", flush=True)
        return start([sys.executable, str(PROFILE_INTAKE_SERVER), "--workspace", str(workspace),
                      "--next-trip", "--overwrite", "--edit", str(selected), "--assistant", args.assistant, *language],
                     detach=args.detach, workspace=workspace)
    print("STARTING CURRENT-TRIP INTAKE WITH SAVED STABLE DEFAULTS", flush=True)
    return start([sys.executable, str(TRIP_INTAKE_SERVER), "--workspace", str(workspace), "--profile", str(selected), "--assistant", args.assistant, *language],
                 detach=args.detach, workspace=workspace)


if __name__ == "__main__":
    raise SystemExit(main())
