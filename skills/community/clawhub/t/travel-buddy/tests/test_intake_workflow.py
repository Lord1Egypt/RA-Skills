#!/usr/bin/env python3
"""Regression tests for scripts/start_intake_workflow.py, specifically its --detach mode.

The defect these exist for is not a crash, which is why nothing caught it for so long. The
script's only mode was a blocking subprocess.run(): the intake server prints the traveller's
loopback link, flushes it, and then sits in serve_forever() for the minutes a real person spends
filling a form. Under Claude Code that is fine, because the harness can background the whole
command. Under opencode, Cursor, Cline or Codex there is no background primitive at all, so the
tool call itself holds the link until the harness's command timeout kills the server mid-fill.

The traveller therefore never sees the form -- and every honest exit from that position is
closed. `intake_context.method: html_form` requires the intake file the blocked server never
wrote; `chat_fallback` requires `declined_verbatim`, the traveller's own words declining the
form, which they never said because they were never offered it; and save_trip_deliverables.py
refuses a plan with neither, correctly and with no bypass flag. What is left is to fabricate a
quote or to abandon the save, which is the mechanism by which trip details went unexecuted on
those harnesses.

So the tests below are about a verb, not a rule: --detach must return in seconds with a link
that really answers, must keep the server's later output somewhere the caller can still read it,
and must fail loudly when no server came up -- because a detach that silently produced nothing
is worse than the blocking run it replaces. It reports a link nobody serves, and the traveller
opening it cannot tell that from a form that is merely slow.

The last four cases are about what that verb leaves on disk. Giving the caller the link through a
file instead of a pipe turns the intake server's one-time token -- which its own banner calls the
proof that the page is the one this terminal opened -- into a credential at rest in the
traveller's workspace, beside their profile. The first version wrote it world-readable (measured
at 0644, `-rw-r--r--`), cleared stale files only for the port the current run happened to reserve,
and never removed one at all, so a workspace accumulated a permanent public record of every dead
server it had ever run. That is the same "a link that was never served" failure the cases above
guard against, arriving one port and one run later, through a file rather than through a race --
and it contradicts what SKILL.md's profile rules and references/profile-and-storage.md promise
about local traveller data being written deliberately and narrowly.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import signal
import socket
import stat
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# A workspace name with a space and CJK in it. Workspaces are user-named folders, the default is
# literally "Travel Buddy" with a space, and the skill is used in Chinese -- so every path this
# mode writes (.intake-<port>.url, .intake-<port>.log) has to survive both. A test that only ever
# uses /tmp/ws proves the one case nobody's machine has.
WORKSPACE_NAME = "旅行 工作区"

# A stub that binds its port, announces a link, and only later prints the sentinel -- standing in
# for the minutes of form-filling between those two events. Using the real server here would test
# the form's validator instead of the detach mechanism, and would make the timing unpredictable.
STUB_SERVER = """
import socket, sys, time
port = int(sys.argv[sys.argv.index("--port") + 1])
sentinel_path, delay = sys.argv[1], float(sys.argv[2])
listener = socket.socket()
listener.bind(("127.0.0.1", port))
listener.listen(5)
print(f"OPEN THIS LOCAL LINK: http://127.0.0.1:{port}/?token=stub-token", flush=True)
time.sleep(delay)
print(f"TRAVEL BUDDY TRIP INPUT: {sentinel_path}", flush=True)
time.sleep(120)
"""

# A child that starts, stays alive, and never binds anything: the "detached but useless" case.
# It is the one a plain "is the process running?" check would call a success.
STUB_NEVER_BINDS = """
import time
time.sleep(120)
"""

# The sharpest version of the same failure: it prints a perfectly well-formed link and never
# serves it. A parent that trusted the log line alone would write that URL into .intake-<port>.url
# and print it to the caller, who hands a dead link to the traveller -- which is precisely the
# outcome --detach exists to avoid, dressed as success.
STUB_ANNOUNCES_BUT_NEVER_BINDS = """
import sys, time
port = int(sys.argv[sys.argv.index("--port") + 1])
print(f"OPEN THIS LOCAL LINK: http://127.0.0.1:{port}/?token=stub-token", flush=True)
time.sleep(120)
"""


def load_workflow():
    # scripts/ has to be importable first: start_intake_workflow.py does `from travel_workspace
    # import ...`, so exec_module() raises ModuleNotFoundError without this.
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location(
        "start_intake_workflow", ROOT / "scripts" / "start_intake_workflow.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_profile(profile_id: str) -> dict:
    """The smallest profile travel_workspace.validate_profile() accepts.

    Written here rather than generated by create-profile so the branch under test -- "exactly one
    valid profile exists" -- is reached by the same route a real workspace reaches it: a file on
    disk that the validator agrees with.
    """
    return {
        "profile_version": "1.0",
        "profile_id": profile_id,
        "storage_consent": {"personal_profile": True, "confirmed_at": "2026-08-29T00:00:00+02:00"},
        "identity_and_language": {"residence_status": "eu_eea_ch_citizen", "languages": ["nl", "en"]},
        "home_and_logistics": {"home_city": "Leiden", "home_country": "Netherlands"},
        "travel_history": {"visited_places": [], "wish_list": [], "excluded_places": []},
        "recurring_preferences": {"dietary_or_religious_needs": ["严重乳制品过敏"]},
        "data_controls": {"retention": "until_forgotten"},
    }


def write_profile(workspace: Path, profile_id: str) -> Path:
    path = workspace / "profiles" / f"{profile_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(valid_profile(profile_id), ensure_ascii=False), encoding="utf-8")
    return path


def stop_detached(pid: int | None) -> None:
    """Kill a server this test started, whatever happened to the test.

    Detached is detached: nothing reaps these when the test process exits, so a test that fails
    early would otherwise leave a loopback server listening on the developer's machine until they
    reboot. The whole process group is signalled because that is what --detach creates.

    Also used for the link-file watcher, which is deliberately started in its own session so the
    documented `kill -TERM -<server pid>` cannot take it down with the server it is watching. That
    means it survives the line above, and a test that stopped only the server would leave one
    watcher per case sitting in a workspace that is about to be deleted.
    """
    if not pid:
        return
    with contextlib.suppress(OSError, ProcessLookupError, PermissionError):
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        else:
            os.killpg(pid, signal.SIGTERM)


def link_record(workspace: Path) -> dict | None:
    matches = sorted(workspace.glob(".intake-*.url"))
    if not matches:
        return None
    return json.loads(matches[0].read_text(encoding="utf-8"))


def wait_for(predicate, timeout: float, poll: float = 0.1) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(poll)
    return predicate()


def check_detach_serves_a_real_link(module, check) -> None:
    """--detach must come back in seconds, and the link it reports must actually answer.

    Both halves matter and only together. Returning promptly with a dead link is the failure this
    mode would otherwise introduce, so the assertion is not "a file was written" but "an HTTP GET
    of the URL in that file returns the intake page". That is also the only check here that would
    have noticed a server which bound its socket and then died before serving anything.
    """
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / WORKSPACE_NAME
        pid = watcher_pid = None
        try:
            stdout = io.StringIO()
            started = time.monotonic()
            with contextlib.redirect_stdout(stdout):
                code = module.main(["--workspace", str(workspace), "--detach"])
            elapsed = time.monotonic() - started
            printed = stdout.getvalue()

            check("--detach exits 0 when the server came up", code == 0, printed)
            check("--detach returns promptly instead of blocking on the form",
                  elapsed < module.DETACH_READY_TIMEOUT_SECONDS / 2,
                  f"took {elapsed:.1f}s; the point of this mode is that the caller gets the link "
                  f"back while the traveller is still filling the form")
            check("--detach prints the link with the same prefix the blocking mode uses",
                  module.LOCAL_LINK_PREFIX in printed,
                  "a caller that already greps for OPEN THIS LOCAL LINK must not need a second parser")

            record = link_record(workspace)
            check("--detach writes the .intake-<port>.url file", record is not None, printed)
            if not record:
                return
            pid = record.get("pid")
            watcher_pid = record.get("watcher_pid")
            check("the link file carries the URL, the pid and the port",
                  all(record.get(key) for key in ("url", "pid", "port")), json.dumps(record))
            check("the recorded URL is the one that was printed",
                  record["url"] in printed, f"{record['url']} not in {printed!r}")
            check("the link file is named after the port it describes",
                  (workspace / f".intake-{record['port']}.url").exists(), json.dumps(record))
            check("the link file names a log the caller can poll",
                  Path(record["log_path"]).exists(), json.dumps(record))
            check("the link file carries a way to stop the server it started",
                  str(record["pid"]) in str(record.get("stop_command", "")), json.dumps(record))

            # The real artifact: fetch the URL and look at what comes back.
            try:
                with urllib.request.urlopen(record["url"], timeout=10) as response:
                    status, body = response.status, response.read().decode("utf-8", "replace")
            except (urllib.error.URLError, OSError) as exc:
                status, body = 0, f"request failed: {exc}"
            check("the reported link actually serves the intake page", status == 200, body[:300])
            check("what it serves is the profile form, not merely something listening",
                  "TRAVEL_BUDDY_PROFILE_INTAKE" in body, body[:300])

            check("the detached server outlives the parent that started it",
                  module.port_answers(record["port"]),
                  "the whole point is that it is still there after this call returned")
        finally:
            stop_detached(pid)
            stop_detached(watcher_pid)


def check_sentinel_survives_detaching(module, check) -> None:
    """The sentinel the caller polls for must still reach a file it can read.

    `TRAVEL BUDDY TRIP INPUT: <path>` is printed minutes after the link, when the traveller
    submits -- long after --detach returned and the parent's pipes are gone. If that line lands
    nowhere, --detach has traded one unusable mode for another: the caller gets a link, hands it
    over, and then has no way to learn that intake ever completed, which lands it back at
    inventing an intake_context.
    """
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / WORKSPACE_NAME
        workspace.mkdir(parents=True)
        stub = Path(tmp) / "stub_server.py"
        stub.write_text(STUB_SERVER, encoding="utf-8")
        # A CJK intake filename, because that is what a Chinese-language workspace produces and
        # the sentinel is read back out of a file the parent opened in text mode.
        sentinel_path = workspace / "plans" / "本次行程-intake.json"
        delay = 3.0
        port = module.reserve_loopback_port()
        pid = None
        # Initialised before the try so the finally can still stop the watcher when run_detached
        # raises before `record` is ever assigned; a NameError in cleanup hides the real failure.
        record = None
        try:
            stdout = io.StringIO()
            started = time.monotonic()
            with contextlib.redirect_stdout(stdout):
                code = module.run_detached(
                    [sys.executable, str(stub), str(sentinel_path), str(delay)], workspace, port)
            elapsed = time.monotonic() - started
            record = link_record(workspace)
            pid = (record or {}).get("pid")
            check("a detached start with a working server exits 0", code == 0, stdout.getvalue())
            check("the parent returned before the child printed the sentinel",
                  elapsed < delay,
                  f"returned after {elapsed:.1f}s of a {delay}s wait; it waited for the submission")

            log_path = Path((record or {}).get("log_path", workspace / f".intake-{port}.log"))
            arrived = wait_for(
                lambda: "TRAVEL BUDDY TRIP INPUT:" in log_path.read_text(encoding="utf-8", errors="replace"),
                timeout=delay + 15)
            check("the sentinel reaches the log after the parent exited", arrived,
                  log_path.read_text(encoding="utf-8", errors="replace"))
            check("the sentinel carries the intake path intact, CJK included",
                  str(sentinel_path) in log_path.read_text(encoding="utf-8", errors="replace"),
                  log_path.read_text(encoding="utf-8", errors="replace"))
        finally:
            stop_detached(pid)
            stop_detached((record or {}).get("watcher_pid"))


def check_detach_fails_loudly_when_the_port_is_taken(module, check) -> None:
    """A server that cannot bind must end the run, not leave a link behind.

    This is the reserve_loopback_port() race made deterministic: something else holds the port
    between the parent reserving it and the child binding it. The child exits 2 with "Address
    already in use", and the parent has to surface that text -- a bare non-zero exit sends the
    caller looking for a bug in the wrong place.

    The stale .url is the second half. Ports get reused; a leftover file from an earlier run on
    this port is a link to a server that is gone, and leaving it in place after a failed start
    reproduces the exact failure this mode exists to prevent, one run later.
    """
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / WORKSPACE_NAME
        workspace.mkdir(parents=True)
        squatter = socket.socket()
        squatter.bind(("127.0.0.1", 0))
        squatter.listen(1)
        port = squatter.getsockname()[1]
        stale = workspace / f".intake-{port}.url"
        stale.write_text('{"url": "http://127.0.0.1:1/?token=gone"}\n', encoding="utf-8")
        original_reserve = module.reserve_loopback_port
        try:
            module.reserve_loopback_port = lambda: port
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
                code = module.main(["--workspace", str(workspace), "--detach"])
            complaint = stderr.getvalue()
            check("a server that cannot start makes the run fail", code != 0, complaint)
            check("the failure quotes what the child actually said",
                  "Address already in use" in complaint or "in use" in complaint,
                  complaint or "(nothing was printed at all)")
            check("the failure names the log it came from",
                  ".intake-" in complaint and ".log" in complaint, complaint)
            check("no link file is left claiming a server that is not there",
                  not stale.exists() and not list(workspace.glob(".intake-*.url")),
                  f"still present: {[p.name for p in workspace.glob('.intake-*.url')]}")
        finally:
            module.reserve_loopback_port = original_reserve
            squatter.close()


def check_detach_fails_loudly_when_the_port_never_answers(module, check) -> None:
    """A child that lives but never serves must be stopped and reported, not handed over.

    Popen.poll() says the interpreter is running, which it also is while it hangs, waits on a
    lock, or blocks on stdin. Readiness is the socket answering, so this case -- alive, silent,
    never binding -- is the one a liveness check would call a success and report a link for.
    """
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / WORKSPACE_NAME
        workspace.mkdir(parents=True)
        stub = Path(tmp) / "never_binds.py"
        stub.write_text(STUB_NEVER_BINDS, encoding="utf-8")
        port = module.reserve_loopback_port()
        original_timeout = module.DETACH_READY_TIMEOUT_SECONDS
        try:
            module.DETACH_READY_TIMEOUT_SECONDS = 1.5
            stderr = io.StringIO()
            started = time.monotonic()
            with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
                code = module.run_detached([sys.executable, str(stub)], workspace, port)
            elapsed = time.monotonic() - started
            complaint = stderr.getvalue()
            check("a server that never answers makes the run fail", code != 0, complaint)
            check("the timeout is bounded by the timeout", elapsed < 10, f"{elapsed:.1f}s")
            check("the failure says the port never answered",
                  "did not answer" in complaint, complaint)
            check("the failure says the child was stopped rather than left running",
                  "stopped" in complaint, complaint)
            check("the empty-output case is stated rather than printed as blank space",
                  "no output" in complaint, complaint)
            check("no link file is written for a server that never served",
                  not list(workspace.glob(".intake-*.url")),
                  f"present: {[p.name for p in workspace.glob('.intake-*.url')]}")
            check("the useless child is actually gone", not module.port_answers(port))

            # Same shape, but the child announces a link it never serves. This isolates the port
            # probe: everything a log-scraping parent looks for is present and correct, and the
            # server still is not there.
            liar = Path(tmp) / "announces_but_never_binds.py"
            liar.write_text(STUB_ANNOUNCES_BUT_NEVER_BINDS, encoding="utf-8")
            other_port = module.reserve_loopback_port()
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
                code = module.run_detached([sys.executable, str(liar)], workspace, other_port)
            complaint = stderr.getvalue()
            check("a link that is announced but never served is still a failure", code != 0,
                  complaint)
            check("an announced-but-dead link is never written to the link file",
                  not list(workspace.glob(".intake-*.url")),
                  f"present: {[p.name for p in workspace.glob('.intake-*.url')]}")
            check("the announced-but-dead case is reported as an unanswered port",
                  "did not answer" in complaint, complaint)
        finally:
            module.DETACH_READY_TIMEOUT_SECONDS = original_timeout
            stop_detached(link_record(workspace) and link_record(workspace).get("pid"))


def check_every_entry_point_honours_the_flag(module, check) -> None:
    """All three ways in must route through start(), not just the first-trip one.

    start_intake_workflow.py opens a server from three places -- no profile, one profile, and
    --edit-profile -- and each used to call the blocking run() directly. Wiring --detach into one
    of them would leave the flag silently ignored on the other two, which is worse than not having
    it: the caller passes --detach, gets no error, and blocks anyway.
    """
    calls: list[tuple[str, list[str]]] = []
    original_run, original_detached = module.run, module.run_detached
    try:
        module.run = lambda command: calls.append(("blocking", command)) or 0
        module.run_detached = lambda command, workspace, port: calls.append(("detached", command)) or 0
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / WORKSPACE_NAME
            workspace.mkdir(parents=True)
            with contextlib.redirect_stdout(io.StringIO()):
                module.main(["--workspace", str(workspace), "--detach"])
                check("no profile yet: --detach reaches the profile form",
                      calls and calls[-1][0] == "detached"
                      and "serve_profile_intake.py" in " ".join(calls[-1][1]), str(calls[-1:]))

                write_profile(workspace, "alice")
                module.main(["--workspace", str(workspace), "--detach"])
                check("one profile: --detach reaches the current-trip form",
                      calls[-1][0] == "detached"
                      and "serve_trip_intake.py" in " ".join(calls[-1][1]), str(calls[-1:]))

                module.main(["--workspace", str(workspace), "--detach", "--edit-profile"])
                check("--edit-profile: --detach reaches the reopened profile form",
                      calls[-1][0] == "detached"
                      and "serve_profile_intake.py" in " ".join(calls[-1][1])
                      and "--edit" in calls[-1][1], str(calls[-1:]))

                module.main(["--workspace", str(workspace)])
                check("without the flag the blocking mode is unchanged",
                      calls[-1][0] == "blocking", str(calls[-1:]))
    finally:
        module.run, module.run_detached = original_run, original_detached


def check_detach_refuses_before_it_starts_anything(module, check) -> None:
    """The checks that run before a server exists must still run, and still stop the command.

    --detach adds a code path that creates directories and writes files, so it is the natural
    place for a guard to get skipped: an unusable workspace becomes a server nobody can find, and
    a profile ambiguity becomes a trip form silently prefilled from whichever profile sorted
    first. Both have to fail before anything is spawned, and say why.
    """
    with tempfile.TemporaryDirectory() as tmp:
        # A workspace path that is a file. mkdir cannot make it a directory, and guessing a
        # different location would hide the traveller's typo behind a workspace they never chose.
        bogus = Path(tmp) / "not-a-directory"
        bogus.write_text("i am a file\n", encoding="utf-8")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
            code = module.main(["--workspace", str(bogus), "--detach"])
        check("an unusable workspace fails instead of starting a server", code != 0, stderr.getvalue())
        check("the unusable workspace is named in the error",
              str(bogus) in stderr.getvalue(), stderr.getvalue())

        # Two valid profiles: which traveller this trip is for is genuinely unknown, and --detach
        # must not turn that question into a silently-prefilled form.
        workspace = Path(tmp) / WORKSPACE_NAME
        write_profile(workspace, "alice")
        write_profile(workspace, "bob")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
            code = module.main(["--workspace", str(workspace), "--detach"])
        check("--detach does not bypass the profile-selection stop", code == 2, stderr.getvalue())
        check("no server is left behind by a run that refused",
              not list(workspace.glob(".intake-*")),
              f"present: {[p.name for p in workspace.glob('.intake-*')]}")


# A listener that accepts TCP and speaks no HTTP at all: the "somebody else recycled that port"
# case. Everything a port probe looks at is satisfied and the intake server it is supposed to be
# is long gone, which is why liveness here is a fetch of the recorded URL and not a connect().
def raw_listener(port: int = 0) -> socket.socket:
    listener = socket.socket()
    listener.bind(("127.0.0.1", port))
    listener.listen(1)
    return listener


def fake_link_file(module, workspace: Path, name: str, url: str) -> Path:
    """Write a link file the way an earlier run would have left it, under an arbitrary name."""
    path = workspace / name
    module.write_link_record(path, {"url": url, "pid": 1, "port": 1, "started_at": "then"})
    return path


def check_the_token_on_disk_is_never_world_readable(module, check) -> None:
    """A one-time token written where anyone on the machine can read it is a different token.

    serve_trip_intake.py's banner calls it "what proves the page is the one this terminal opened".
    The blocking mode keeps that proof on one terminal line; --detach writes it into the
    traveller's workspace, next to their profile, and the first version did so with whatever the
    umask allowed -- measured at 0644, `-rw-r--r--`. So this asserts the mode of both files the
    mode writes, and then the two ways a naive fix still leaks: a permissive umask, and a
    world-readable file of the same name left by a run from before the fix, which O_CREAT will
    happily reuse the old permissions of.
    """
    if os.name == "nt":
        # Windows has no POSIX mode bits worth asserting on -- os.open()'s mode argument only
        # controls the read-only flag there -- and the protection comes from the directory ACL.
        return
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / WORKSPACE_NAME
        pid = watcher_pid = None
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                code = module.main(["--workspace", str(workspace), "--detach"])
            check("--detach still succeeds with the hardened writes", code == 0)
            record = link_record(workspace)
            if not record:
                check("a link file was written at all", False, "nothing matched .intake-*.url")
                return
            pid, watcher_pid = record.get("pid"), record.get("watcher_pid")
            url_path = workspace / f".intake-{record['port']}.url"
            log_path = Path(record["log_path"])
            for path in (url_path, log_path):
                mode = stat.S_IMODE(path.stat().st_mode)
                # Compared against the literal 0o600 and against the group/other bits directly,
                # never against module.LINK_FILE_MODE. An assertion that reads the very constant
                # it is policing passes for every value of it: flipping that constant back to
                # 0o644 left this whole case green, which is how this line came to be written.
                check(f"{path.name} is owner-only, not world-readable",
                      mode == 0o600 and not mode & 0o077,
                      f"{stat.filemode(path.stat().st_mode)} ({oct(mode)}); it holds the "
                      f"one-time token from the link")
            check("no temporary copy of the record is left behind",
                  not list(workspace.glob(".intake-*.url.tmp")),
                  f"present: {[p.name for p in workspace.glob('.intake-*.url.tmp')]}")
        finally:
            stop_detached(pid)
            stop_detached(watcher_pid)

    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        # A umask of 0 is what makes this an assertion about the code rather than about the
        # machine that ran it: with 0o600 passed to os.open the result is 0600 either way, but a
        # `path.open("w")` that merely inherited a strict umask would show up here as 0666.
        previous_umask = os.umask(0)
        try:
            fresh = workspace / "fresh.txt"
            with module.open_owner_only(fresh) as handle:
                handle.write("token")
            check("a new file is owner-only even under a fully permissive umask",
                  stat.S_IMODE(fresh.stat().st_mode) == 0o600,
                  stat.filemode(fresh.stat().st_mode))

            # The case O_CREAT alone cannot fix: the file already exists, so its mode is not
            # reconsidered, and a run from before this fix left exactly such a file.
            inherited = workspace / "inherited.txt"
            inherited.write_text("older run", encoding="utf-8")
            os.chmod(inherited, 0o644)
            with module.open_owner_only(inherited) as handle:
                handle.write("token")
            check("an existing world-readable file is narrowed before anything is written to it",
                  stat.S_IMODE(inherited.stat().st_mode) == 0o600,
                  stat.filemode(inherited.stat().st_mode))

            legacy = workspace / ".intake-1.url"
            legacy.write_text("{}\n", encoding="utf-8")
            os.chmod(legacy, 0o644)
            module.write_link_record(legacy, {"url": "http://127.0.0.1:1/?token=x"})
            check("replacing a 0644 record from an older run does not inherit its permissions",
                  stat.S_IMODE(legacy.stat().st_mode) == 0o600,
                  stat.filemode(legacy.stat().st_mode))

            # A record that cannot be serialised must not leave the half-written temporary on
            # disk: it is created before json.dumps runs, and it is the file the token lands in.
            doomed = workspace / ".intake-2.url"
            raised = False
            try:
                module.write_link_record(doomed, {"url": object()})
            except (TypeError, ValueError):
                raised = True
            check("a record that cannot be written fails loudly", raised,
                  "write_link_record accepted an unserialisable record")
            check("a failed write leaves no temporary file holding a partial record",
                  not doomed.exists() and not list(workspace.glob(".intake-*.url.tmp")),
                  f"present: {[p.name for p in workspace.glob('.intake-*')]}")
        finally:
            os.umask(previous_umask)


def check_dead_link_files_do_not_accumulate(module, check) -> None:
    """Every dead link file goes, not just the one that happens to share this run's port.

    The narrow version cleared `.intake-<reserved_port>.url` only, and reserve_loopback_port()
    almost never returns the same port twice, so a workspace grew one permanent world-readable
    record of a dead server per detached run. The measured shape was two files side by side, the
    older naming a port that no longer answered, and a caller globbing `.intake-*.url` picking the
    dead one because it sorted first.

    The opposite mistake is checked in the same place: a run that swept away the record of a
    server the traveller is still typing into would take with it the only copy of its stop
    command, so a live link has to survive the sweep.
    """
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / WORKSPACE_NAME
        first = second = None
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                module.main(["--workspace", str(workspace), "--detach"])
            first = link_record(workspace)
            with contextlib.redirect_stdout(io.StringIO()):
                module.main(["--workspace", str(workspace), "--detach"])
            files = sorted(p.name for p in workspace.glob(".intake-*.url"))
            second = next((json.loads((workspace / name).read_text())
                           for name in files
                           if json.loads((workspace / name).read_text())["pid"] != first["pid"]), None)
            check("a live link file survives a second run that did not start it",
                  f".intake-{first['port']}.url" in files, str(files))
            check("the second run's own link file is there too",
                  second is not None and f".intake-{second['port']}.url" in files, str(files))

            # Now the reviewer's case: the first server dies, and the next run must not leave its
            # record behind for a globbing caller to hand over.
            stop_detached(first.get("pid"))
            stop_detached(first.get("watcher_pid"))
            deadline = time.monotonic() + 10
            while module.port_answers(first["port"]) and time.monotonic() < deadline:
                time.sleep(0.1)
            with contextlib.redirect_stdout(io.StringIO()):
                module.main(["--workspace", str(workspace), "--detach"])
            third = next((json.loads(p.read_text()) for p in sorted(workspace.glob(".intake-*.url"))
                          if json.loads(p.read_text())["pid"] not in {first["pid"], second["pid"]}),
                         None)
            remaining = sorted(p.name for p in workspace.glob(".intake-*.url"))
            check("the dead server's link file is gone after the next run",
                  f".intake-{first['port']}.url" not in remaining, str(remaining))
            check("the still-live servers keep theirs",
                  f".intake-{second['port']}.url" in remaining, str(remaining))
            stop_detached((third or {}).get("pid"))
            stop_detached((third or {}).get("watcher_pid"))
        finally:
            for record in (first, second):
                stop_detached((record or {}).get("pid"))
                stop_detached((record or {}).get("watcher_pid"))

    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / WORKSPACE_NAME
        workspace.mkdir(parents=True)
        squatter = raw_listener()
        squatter_port = squatter.getsockname()[1]
        try:
            # A port that answers but is not the intake server any more. This is what makes a
            # connect()-based liveness test wrong rather than merely approximate: the record is
            # dead, its token is dead, and the port says yes.
            recycled = fake_link_file(module, workspace, f".intake-{squatter_port}.url",
                                      f"http://127.0.0.1:{squatter_port}/?token=gone")
            check("a port that answers but does not serve the form is not called live",
                  not module.link_is_live(f"http://127.0.0.1:{squatter_port}/?token=gone",
                                          squatter_port),
                  "port_answers() alone would have said this record was live")

            # Names this script cannot have produced. Deleting them on a guess is worse than
            # leaving them, so they are reported and left -- and a non-ASCII digit string that
            # int() would happily accept must not be mistaken for a port number.
            unicode_digits = fake_link_file(module, workspace, ".intake-٥٣.url",
                                            "http://127.0.0.1:53/?token=x")
            out_of_range = fake_link_file(module, workspace, ".intake-99999.url",
                                          "http://127.0.0.1:99999/?token=x")
            not_a_port = fake_link_file(module, workspace, ".intake-旅行.url",
                                        "http://127.0.0.1:1/?token=x")
            # f".intake-{port}.url" of an int never produces a leading zero, so this reads as a
            # valid port and still cannot be a file this script wrote. What decides deletion has
            # to match what this script writes, not merely what parses.
            leading_zero = fake_link_file(module, workspace, ".intake-012.url",
                                          "http://127.0.0.1:12/?token=x")
            zero_port = fake_link_file(module, workspace, ".intake-0.url",
                                       "http://127.0.0.1:0/?token=x")
            debris = workspace / f".intake-{squatter_port}.url.tmp"
            debris.write_text("half a record", encoding="utf-8")

            removed, unrecognised = module.clear_stale_link_files(workspace, reserved_port=1)
            names_removed = sorted(p.name for p in removed)
            names_left = sorted(p.name for p in unrecognised)
            check("the recycled-port record is removed", not recycled.exists(), str(names_removed))
            check("interrupted temporary records are removed too",
                  not debris.exists(), str(names_removed))
            check("a name with non-ASCII digits is not mistaken for a port and is left alone",
                  unicode_digits.exists() and unicode_digits.name in names_left,
                  f"removed={names_removed} left={names_left}")
            check("a port number outside the valid range is left alone",
                  out_of_range.exists() and out_of_range.name in names_left,
                  f"removed={names_removed} left={names_left}")
            check("a name that is not a port at all is left alone",
                  not_a_port.exists() and not_a_port.name in names_left,
                  f"removed={names_removed} left={names_left}")
            check("a port spelled with a leading zero is not a name this script writes",
                  leading_zero.exists() and leading_zero.name in names_left,
                  f"removed={names_removed} left={names_left}")
            check("port 0 is never a port the kernel handed out",
                  zero_port.exists() and zero_port.name in names_left,
                  f"removed={names_removed} left={names_left}")
            check("nothing is left unaccounted for",
                  not (set(names_removed) & set(names_left)),
                  f"removed={names_removed} left={names_left}")

            # And the caller is told about the ones it refused to touch, because a reader
            # globbing .intake-*.url will still find them.
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
                module.main(["--workspace", str(workspace), "--detach", "--profile", "nope"])
            # (that run stops at profile selection; the point is only that nothing was deleted)
            check("a refused run does not delete the unrecognised files either",
                  unicode_digits.exists() and not_a_port.exists(), stderr.getvalue())
        finally:
            squatter.close()


def check_a_link_file_does_not_outlive_its_server(module, check) -> None:
    """The token must stop existing when the thing it authenticates stops existing.

    Sweeping on the next run is not enough on its own: a traveller who runs --detach once and
    never again leaves the token on disk forever. Nothing in the two intake servers knows about a
    file this script invented, and the profile server does not even exit at the handover -- its
    pid stays alive while its port goes quiet and the current-trip form takes over on a new one --
    so a watcher process outlives the parent and removes the file when the link stops answering.

    The second half is the race that makes a naive watcher dangerous: ports are reused, so between
    a server dying and its watcher noticing, a new run can reserve the same port and write a new
    record under the same name. Deleting that would destroy a live run's link file.
    """
    original_poll, original_strikes = module.WATCHER_POLL_SECONDS, module.WATCHER_DEAD_STRIKES
    try:
        module.WATCHER_POLL_SECONDS, module.WATCHER_DEAD_STRIKES = 0.2, 2
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / WORKSPACE_NAME
            pid = watcher_pid = None
            try:
                with contextlib.redirect_stdout(io.StringIO()) as stdout:
                    module.main(["--workspace", str(workspace), "--detach"])
                printed = stdout.getvalue()
                record = link_record(workspace)
                if not record:
                    check("a link file was written at all", False, printed)
                    return
                pid, watcher_pid = record["pid"], record.get("watcher_pid")
                url_path = workspace / f".intake-{record['port']}.url"
                log_path = Path(record["log_path"])
                check("the record names the process that will clean it up",
                      isinstance(watcher_pid, int) and record.get("watcher_error") is None,
                      json.dumps(record, ensure_ascii=False))
                check("the caller is told which process will remove the file",
                      "INTAKE LINK FILE WATCHER PID:" in printed, printed)
                check("the file is still there while the link is live", url_path.exists())

                stop_detached(pid)
                gone = wait_for(lambda: not url_path.exists(), timeout=15)
                check("the link file is removed once its server stops answering", gone,
                      f"still present: {url_path}")
                check("the log says why it went, where the caller is already polling",
                      wait_for(lambda: "INTAKE LINK FILE REMOVED:" in log_path.read_text(
                          encoding="utf-8", errors="replace"), timeout=10),
                      log_path.read_text(encoding="utf-8", errors="replace"))
                check("the log file itself survives, because the sentinel has to",
                      log_path.exists(), "the caller polls it for TRAVEL BUDDY TRIP INPUT:")
            finally:
                stop_detached(pid)
                stop_detached(watcher_pid)

        # A newer run's record under the same filename must survive the older watcher.
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / WORKSPACE_NAME
            workspace.mkdir(parents=True)
            stub = Path(tmp) / "stub_server.py"
            stub.write_text(STUB_SERVER, encoding="utf-8")
            port = module.reserve_loopback_port()
            record = None
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    module.run_detached(
                        [sys.executable, str(stub), str(workspace / "x.json"), "600"],
                        workspace, port)
                record = link_record(workspace)
                url_path = workspace / f".intake-{port}.url"
                successor = dict(record, pid=record["pid"] + 100000, started_at="a later run")
                module.write_link_record(url_path, successor)
                stop_detached(record["pid"])
                time.sleep(module.WATCHER_POLL_SECONDS * (module.WATCHER_DEAD_STRIKES + 4) + 1.5)
                check("a watcher does not delete a record a newer run owns",
                      url_path.exists(),
                      "the old watcher removed the file a run that reused the port had written")
                if url_path.exists():
                    check("and it leaves that record's contents alone",
                          json.loads(url_path.read_text())["started_at"] == "a later run",
                          url_path.read_text())
            finally:
                stop_detached((record or {}).get("pid"))
                stop_detached((record or {}).get("watcher_pid"))
    finally:
        module.WATCHER_POLL_SECONDS, module.WATCHER_DEAD_STRIKES = original_poll, original_strikes


def check_a_reader_can_tell_a_live_link_from_a_dead_one(module, check) -> None:
    """Whoever opens one of these files has to be able to decide, without reading this script.

    The reader is usually a model that was told "read `<workspace>/.intake-<port>.url`". If the
    only signal is that the file exists, it hands over whatever it finds -- which is the
    "reported a link that was never served" failure --detach was written to prevent, arriving one
    port and one dead server later. So the record states its own test, and that test is a fetch of
    the URL rather than a look at the pid or the port: measured at the profile-to-trip handover,
    the recorded pid is still alive while the recorded port has stopped answering.
    """
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / WORKSPACE_NAME
        pid = watcher_pid = None
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                module.main(["--workspace", str(workspace), "--detach"])
            record = link_record(workspace)
            if not record:
                check("a link file was written at all", False, "nothing matched .intake-*.url")
                return
            pid, watcher_pid = record["pid"], record.get("watcher_pid")
            url, port = record["url"], record["port"]

            check("the record carries a liveness test a reader can follow",
                  module.INTAKE_PAGE_MARKER in record.get("live_check", "")
                  and url in record.get("live_check", ""),
                  json.dumps(record, ensure_ascii=False))
            check("a live link is reported live", module.link_is_live(url, port))
            check("a link whose token has been tampered with is not reported live",
                  not module.link_is_live(f"http://127.0.0.1:{port}/?token=wrong", port),
                  "the server answers that with a 403, which is not the intake page")
            check("an empty or missing URL is never reported live",
                  not module.link_is_live("", port) and not module.link_is_live(url, 0))
            check("a URL that points off loopback is refused without being fetched",
                  not module.link_is_live(f"http://example.com:{port}/?token=x", port),
                  "these files are editable, so the fetch is fenced to 127.0.0.1 and this port")
            check("a URL whose port disagrees with the record is refused",
                  not module.link_is_live(f"http://127.0.0.1:{port}/?token=x", port + 1))

            stop_detached(pid)
            stop_detached(watcher_pid)
            pid = watcher_pid = None
            became_dead = wait_for(lambda: not module.link_is_live(url, port), timeout=15)
            check("the same link is reported dead once the server is gone", became_dead,
                  "link_is_live still says yes for a server that has stopped")
        finally:
            stop_detached(pid)
            stop_detached(watcher_pid)


def check_a_blocking_run_tells_a_weaker_agent_what_to_do(module, check) -> None:
    """A foreground run blocks for minutes; it now says so and names --detach.

    Measured before the fix, with the server started exactly the way a Codex-style agent would:
    the link IS flushed before `serve_forever()` blocks, so it does reach the agent -- and then
    nothing else is ever said. A harness that cannot background a command holds its tool call open
    until the command timeout kills the server mid-fill, taking the traveller's unsaved answers
    with it, and no line anywhere told the agent that `--detach` was the way out. Every gate in
    this skill already names its successor for the same reason: an assistant that cannot hold
    SKILL.md in context rebuilds the next step from what the last command printed.

    The advice must ALSO stay silent when the run is already detached, or it becomes a stale
    instruction inside the log file an agent polls.
    """
    import serve_trip_intake

    advice = serve_trip_intake.blocking_advice()
    check("a foreground run is told about --detach",
          "--detach" in advice and advice.strip(),
          "a blocking command that does not name its escape hatch is the gap this closes")
    check("the advice names the log file to poll instead of the pipe",
          ".intake-" in advice and "log" in advice, advice)

    # A detached server is its own session leader: that is precisely what setsid() makes it, so
    # the check needs no plumbing between the launcher and the server.
    real = os.getsid
    try:
        os.getsid = lambda _pid: os.getpid()
        check("an already-detached run says nothing", serve_trip_intake.blocking_advice() == "",
              "advice to detach, printed inside a detached run, is a stale instruction in the one "
              "file an agent is polling")
    finally:
        os.getsid = real

    # Where POSIX sessions do not exist the safe answer is to advise, not to guess silent.
    try:
        def explode(_pid):
            raise OSError("no sessions here")
        os.getsid = explode
        check("a platform without sessions still gets the advice",
              "--detach" in serve_trip_intake.blocking_advice(),
              "silence costs the form; a redundant line costs nothing")
    finally:
        os.getsid = real

    # And both servers must use the one copy, not two that drift.
    import serve_profile_intake
    check("the profile server shares the trip server's copy",
          serve_profile_intake.blocking_advice is serve_trip_intake.blocking_advice,
          "two copies of a message is how the English-guard list drifted from the renderer")


# --------------------------------------------------------------------------------------------
# The language the traveller chose
# --------------------------------------------------------------------------------------------
# The profile collects `preferred_response_language`; the trip form received it and dropped it,
# and 0 of 15 real intakes carried it. The pages now speak zh or en, so the servers have to decide
# which, tell the page, answer in it, and write down what was used. These cases start the real
# servers the way a caller does -- through main(), detached -- and read what a browser would get.

# A trip intake exactly as trip-intake-form.html builds it (generated from its own build(), with
# the budget label a browser takes from the selected option). The server validates what it saves,
# so a hand-written dict would test the validator's patience instead of the language plumbing.
FORM_INTAKE = ROOT / "tests" / "form-intake-fixture.json"
LANGUAGE_HEADER = "X-Travel-Buddy-Language"


def has_cjk(text: str) -> bool:
    return any("㐀" <= ch <= "鿿" for ch in text)


def fetch(url: str, payload: dict | None = None, headers: dict | None = None) -> tuple[int, str]:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=data, method="GET" if payload is None else "POST",
                                     headers={"Content-Type": "application/json", **(headers or {})})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError) as exc:
        return 0, f"request failed: {exc}"


def page_config(body: str, name: str) -> dict:
    """The config object the server injected into the page, as the page's script reads it."""
    marker = f"window.{name}="
    start = body.find(marker)
    if start < 0:
        return {}
    end = body.find(";</script>", start)
    return json.loads(body[start + len(marker):end])


def detached_link(module, workspace: Path, argv: list[str], check, label: str) -> dict | None:
    # An unknown flag makes argparse exit; that is one failed case, not the end of the run.
    with contextlib.redirect_stdout(io.StringIO()) as printed, contextlib.redirect_stderr(io.StringIO()) as errors:
        try:
            code = module.main(["--workspace", str(workspace), "--detach", "--assistant", "none", *argv])
        except SystemExit as exc:
            code = exc.code
    check(f"{label}: the detached server came up", code == 0, printed.getvalue() + errors.getvalue())
    return link_record(workspace) if code == 0 else None


def check_language_module(check) -> None:
    """The one place the language is decided: aliases, the order of sources, and the picker."""
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import intake_language as lang
    except ImportError as exc:
        check("scripts/intake_language.py exists", False, str(exc))
        return
    for value, expected in [("English", "en"), ("en", "en"), ("英文", "en"), (" EN ", "en"),
                            ("中文", "zh"), ("zh", "zh"), ("Chinese", "zh"),
                            ("中文和 English", None), ("其他", None), ("", None), (None, None), (5, None),
                            # what a profile written in chat, by any assistant, says instead
                            ("en_US", "en"), ("en-AU", "en"), ("English (UK)", "en"),
                            ("Simplified Chinese", "zh"), ("zh-TW", "zh"), ("zh_Hant_HK", "zh"),
                            ("繁體中文", "zh"), ("普通话", "zh"), ("Mandarin", "zh"),
                            ("English and Chinese", None), ("日本語", None), ("Deutsch", None),
                            # bilingual in one word: 英文 inside 中英文 used to read as English
                            ("中英文", None), ("中英文均可", None), ("中英双语", None),
                            ("English/中文", None)]:
        check(f"normalize_language({value!r}) is {expected!r}", lang.normalize_language(value) == expected,
              repr(lang.normalize_language(value)))
    english = {"identity_and_language": {"preferred_response_language": "English"}}
    both = {"identity_and_language": {"preferred_response_language": "中文和 English"}}
    for cli, profile, expected, why in [
        ("en", None, "en", "the flag alone"),
        ("zh", english, "zh", "the flag beats the profile"),
        (None, english, "en", "the profile's preference when there is no flag"),
        (None, both, "zh", "a bilingual preference names no single page language"),
        (None, None, "zh", "nothing said: Chinese"),
        (None, {"identity_and_language": "broken"}, "zh", "a malformed profile section is not an answer"),
        (None, {"identity_and_language": {"preferred_response_language": "",
                                          "profile_form_language": "en"}}, "en",
         "no preference: the language the profile was filled in"),
        (None, {"identity_and_language": {"preferred_response_language": "中文",
                                          "profile_form_language": "en"}}, "zh",
         "a stated preference beats the page the profile was filled in"),
    ]:
        check(f"resolve_form_language: {why}", lang.resolve_form_language(cli, profile) == expected,
              repr(lang.resolve_form_language(cli, profile)))
    check("pick chooses by language", lang.pick("en", "中", "E") == "E" and lang.pick("zh", "中", "E") == "中")
    try:
        lang.pick("fr", "中", "E")
        check("pick refuses a language it does not have", False, "returned instead of raising")
    except ValueError:
        pass


def check_english_reaches_the_profile_page(module, check) -> None:
    """--language en reaches the first page a new traveller sees, through --detach, and the
    server refuses a tokenless request in English too -- that refusal is also a page."""
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / WORKSPACE_NAME
        record = None
        try:
            record = detached_link(module, workspace, ["--language", "en"], check, "--language en")
            if not record:
                return
            command = record.get("command") or []
            check("--detach passes --language to the server it starts",
                  "--language" in command and command[command.index("--language") + 1] == "en", str(command))
            status, body = fetch(record["url"])
            config = page_config(body, "TRAVEL_BUDDY_PROFILE_INTAKE")
            check("the profile page is told to speak English", status == 200 and config.get("language") == "en",
                  f"{status} {config}")
            bare = record["url"].split("?", 1)[0]
            status, body = fetch(bare)
            check("a request without the token is refused", status == 403, f"{status} {body[:200]}")
            check("and the refusal is in English", not has_cjk(body), body[:200])
        finally:
            if record:
                stop_detached(record.get("pid"))
                stop_detached(record.get("watcher_pid"))


def check_the_profile_preference_chooses_the_trip_language(module, check) -> None:
    """With no flag, a saved profile that asks for English gets an English trip page; the flag
    still overrides it. This is the value that was collected and dropped."""
    for argv, expected, label in [([], "en", "profile prefers English, no flag"),
                                  (["--language", "zh"], "zh", "the flag overrides the profile")]:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / WORKSPACE_NAME
            path = write_profile(workspace, "alice")
            profile = json.loads(path.read_text(encoding="utf-8"))
            profile["identity_and_language"]["preferred_response_language"] = "English"
            path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")
            record = None
            try:
                record = detached_link(module, workspace, argv, check, label)
                if not record:
                    continue
                status, body = fetch(record["url"])
                config = page_config(body, "TRAVEL_BUDDY_TRIP_INTAKE")
                check(f"{label}: the trip page speaks {expected}", config.get("language") == expected,
                      f"{status} {config.get('language')!r}")
            finally:
                if record:
                    stop_detached(record.get("pid"))
                    stop_detached(record.get("watcher_pid"))


def check_the_saved_intake_carries_the_language(module, check) -> None:
    """A submission is answered in the language of the page that sent it, and the saved intake
    records that language and the traveller's preferred output language for the steps after it."""
    intake = json.loads(FORM_INTAKE.read_text(encoding="utf-8"))
    for preference, header, form_language, output_language in [
        ("中文和 English", "en", "en", "en"),   # bilingual preference: the page language decides
        ("English", "zh", "zh", "en"),          # switched to Chinese on the page, still wants English
    ]:
        label = f"preference {preference!r}, page {header}"
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / WORKSPACE_NAME
            path = write_profile(workspace, "alice")
            profile = json.loads(path.read_text(encoding="utf-8"))
            profile["identity_and_language"]["preferred_response_language"] = preference
            path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")
            record = None
            try:
                record = detached_link(module, workspace, ["--language", "en"], check, label)
                if not record:
                    continue
                status, body = fetch(record["url"])
                submit = urllib.parse.urljoin(record["url"], page_config(body, "TRAVEL_BUDDY_TRIP_INTAKE").get("submit_url", ""))
                broken = json.loads(json.dumps(intake))
                broken["party"]["traveler_count"] = 0
                status, body = fetch(submit, broken, {LANGUAGE_HEADER: header})
                check(f"{label}: an invalid submission is refused", status == 422, f"{status} {body[:200]}")
                check(f"{label}: in the language of the page that sent it", has_cjk(body) == (header == "zh"), body[:300])
                status, body = fetch(submit, intake, {LANGUAGE_HEADER: header})
                check(f"{label}: a valid submission is saved", status == 201, f"{status} {body[:300]}")
                if status != 201:
                    continue
                saved = json.loads(Path(json.loads(body)["intake_path"]).read_text(encoding="utf-8"))
                check(f"{label}: the intake records the form language", saved.get("form_language") == form_language,
                      repr(saved.get("form_language")))
                check(f"{label}: and the preferred output language", saved.get("preferred_output_language") == output_language,
                      repr(saved.get("preferred_output_language")))
            finally:
                if record:
                    stop_detached(record.get("pid"))
                    stop_detached(record.get("watcher_pid"))


def check_the_profile_server_speaks_and_hands_over(module, check) -> None:
    """The profile server refuses in the page's language -- including the one refusal a traveller
    can cause by typing a passport number into a note -- and opens the trip form in the resolved
    language: the flag if there was one, else what the new profile asks for."""
    for argv, preference, page_language, expected, label in [
        (["--language", "en"], "中文", "en", "en", "flag en, profile prefers Chinese"),
        ([], "English", "zh", "en", "no flag, new profile prefers English"),
        ([], None, "zh", "zh", "no flag, no preference"),
        # The traveller switched the profile page to English and left the preference blank, or
        # chose "other": the page they used is the answer. Both used to open the trip form in
        # Chinese, because only a preference the dropdown could name counted.
        ([], None, "en", "en", "no flag, no preference, profile filled in English"),
        ([], "其他", "en", "en", "no flag, 'other', profile filled in English"),
    ]:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / WORKSPACE_NAME
            record = None
            try:
                record = detached_link(module, workspace, argv, check, label)
                if not record:
                    continue
                status, body = fetch(record["url"])
                submit = urllib.parse.urljoin(record["url"], page_config(body, "TRAVEL_BUDDY_PROFILE_INTAKE").get("submit_url", ""))
                leaky = valid_profile("bob")
                leaky["home_and_logistics"]["notes"] = "passport number: E12345678"
                status, body = fetch(submit, leaky, {LANGUAGE_HEADER: page_language})
                check(f"{label}: a profile carrying a passport number is refused", status == 422, f"{status} {body[:200]}")
                check(f"{label}: in the page's language", has_cjk(json.loads(body).get("error", "")) == (page_language == "zh"),
                      body[:300])
                profile = valid_profile("bob")
                if preference:
                    profile["identity_and_language"]["preferred_response_language"] = preference
                status, body = fetch(submit, profile, {LANGUAGE_HEADER: page_language})
                check(f"{label}: the profile is saved", status == 201, f"{status} {body[:300]}")
                if status != 201:
                    continue
                next_url = json.loads(body).get("next_url") or ""
                status, body = fetch(next_url)
                config = page_config(body, "TRAVEL_BUDDY_TRIP_INTAKE")
                check(f"{label}: the trip form it opens speaks {expected}", config.get("language") == expected,
                      f"{status} {config.get('language')!r}")
                # And later trips: the saved profile remembers the page it was filled in.
                saved = [json.loads(p.read_text(encoding="utf-8"))
                         for p in (workspace / "profiles").glob("*.json")]
                check(f"{label}: the saved profile records the page language it was filled in",
                      len(saved) == 1 and saved[0].get("identity_and_language", {})
                      .get("profile_form_language") == page_language,
                      [s.get("identity_and_language") for s in saved])
            finally:
                if record:
                    stop_detached(record.get("pid"))
                    stop_detached(record.get("watcher_pid"))


def main() -> int:
    module = load_workflow()
    failures: list[str] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        if not condition:
            failures.append(f"{name}\n{detail}")

    check_detach_serves_a_real_link(module, check)
    check_sentinel_survives_detaching(module, check)
    check_detach_fails_loudly_when_the_port_is_taken(module, check)
    check_detach_fails_loudly_when_the_port_never_answers(module, check)
    check_every_entry_point_honours_the_flag(module, check)
    check_detach_refuses_before_it_starts_anything(module, check)
    check_the_token_on_disk_is_never_world_readable(module, check)
    check_dead_link_files_do_not_accumulate(module, check)
    check_a_link_file_does_not_outlive_its_server(module, check)
    check_a_reader_can_tell_a_live_link_from_a_dead_one(module, check)
    check_a_blocking_run_tells_a_weaker_agent_what_to_do(module, check)
    check_language_module(check)
    check_english_reaches_the_profile_page(module, check)
    check_the_profile_preference_chooses_the_trip_language(module, check)
    check_the_saved_intake_carries_the_language(module, check)
    check_the_profile_server_speaks_and_hands_over(module, check)

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all intake-workflow detach cases passed")
    return 0


def test_intake_workflow_detach() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
