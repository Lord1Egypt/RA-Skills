#!/usr/bin/env python3
"""Every place this skill talks to its host agent. The only file a port edits.

The skill itself knows nothing about any agent. Reminders live in tklr, and
delivery is a plain shell command stored in the tklr workspace's `[alerts]`
section, which `tklr_alert_poller.py` runs on a schedule. The poller does not
call the host at all -- it runs the string it is given. That is what keeps the
host swappable: the agent is a client of this skill, never a component of it.

Three things do need a host, and all three live here:

  1. CHAT DISCOVERY -- what destinations can this machine reach, and what is
     the shell command that sends to one? `chat_list`, `chat_platforms`,
     `chat_target_ids`, `platform_targets`, `chat_targets`, `chat_send_command`.
  2. SCHEDULING -- run the dispatcher once a minute. `dispatcher_path`,
     `cron_job_present`, `create_cron_job`.
  3. HOST PATHS -- where a scheduled script must live, and where its log goes.
     `dispatcher_path`, `LOG_PATH`.

PORTING TO ANOTHER AGENT
Rewrite the bodies in this file; change nothing else. Each function's docstring
says what its replacement has to return, in terms of this skill rather than of
Hermes. Two of the three delivery routes the skill offers -- `himalaya` for
email and `notify-send` for the desktop -- are ordinary CLIs and are not host
calls, so they keep working untouched. Concretely, a port needs:

  * chat discovery: some way to enumerate destinations. If the host has no
    equivalent of `send --list`, `chat_list` can read a config file the user
    writes, and `chat_targets` can parse that instead. Returning nothing is
    valid and degrades honestly: the skill offers email and desktop only.
  * scheduling: `create_cron_job` can shell out to `crontab`, write a systemd
    timer, or do nothing and return a message telling the user what to add by
    hand. `dispatcher_path` exists only because Hermes' scheduler refuses any
    script outside `~/.hermes/scripts/`; a host without that restriction can
    return the skill's own copy and the deploy step becomes a no-op.

What a port must NOT do is reach past this file. If a new host call is needed,
add it here rather than at the point of use -- the value of one adapter is that
`grep -c hermes` outside this file stays at zero, so nobody has to discover the
seams by searching for them.

Nothing here exits the process. Failures raise HostError and each caller maps
it to its own reporting, because a missing host command means something
different to `setup` (fatal) than to `status` (worth reporting and carrying on).
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

# --------------------------------------------------------------------------
# The host. Everything below is expressed in terms of these.
# --------------------------------------------------------------------------

HOST_CLI = "hermes"

# Where a scheduled script must live for the host's scheduler to accept it, and
# where the dispatcher appends one line per delivery. Both are Hermes layout;
# the log is already overridable so a port can leave it alone.
HOST_HOME = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes")
LOG_PATH = Path(os.environ.get("TKLR_ALERTS_LOG")
                or HOST_HOME / "logs" / "tklr-alerts.log")

CRON_JOB_NAME = "tklr-alert-poller"

# `--list` and `cron list` are read often; `cron create` writes once.
READ_TIMEOUT = 60
WRITE_TIMEOUT = 120


class HostError(RuntimeError):
    """A host command could not be run, or ran and failed.

    `detail` is the host's own output when there is any -- worth showing,
    never worth parsing.
    """

    def __init__(self, message: str, detail: str = "") -> None:
        super().__init__(message)
        self.detail = detail


def _run(argv: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(argv, capture_output=True, text=True,
                              timeout=timeout, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise HostError(f"could not run `{' '.join(argv)}`: {exc}") from exc


# --------------------------------------------------------------------------
# Seam 1: chat discovery and the delivery command
# --------------------------------------------------------------------------

_list_cache: dict[str | None, str] = {}


def chat_list(platform: str | None = None) -> str:
    """The host's list of reachable chat destinations, verbatim.

    A replacement returns whatever text `chat_targets` and `chat_platforms`
    below can parse -- the two are a pair, and a port is free to change the
    format as long as it changes both. Returning "" is valid and means this
    machine reaches no chat destination.

    Cached per process: `setup` consults it three times and each call is a
    subprocess with a 60s timeout.
    """
    if platform in _list_cache:
        return _list_cache[platform]
    argv = [HOST_CLI, "send", "--list"] + ([platform] if platform else [])
    proc = _run(argv, READ_TIMEOUT)
    if proc.returncode != 0:
        raise HostError(f"`{' '.join(argv)}` failed", (proc.stderr or "").strip())
    _list_cache[platform] = proc.stdout or ""
    return _list_cache[platform]


def chat_send_command(target: str, message: str) -> str:
    """The shell command that sends `message` to `target`.

    This return value is stored in the tklr workspace and run by the
    dispatcher, so it must be a complete shell command and must survive being
    written to TOML. `message` arrives with tklr's `{name}`/`{when}`/`{start}`
    placeholders already in it and must be passed through untouched -- tklr
    substitutes them at delivery, not here.
    """
    return f"{HOST_CLI} send --to {target} {message}"


# A `--list` entry: leading whitespace, `platform:id`, anything else on the
# line, and an optional trailing `(kind)` annotation.
CHAT_LINE = re.compile(r"^\s+(\w+:\S+).*?(?:\((\w+)\)\s*)?$")

# A `--list` section heading: a platform with no targets indented under it.
PLATFORM_HEADING = re.compile(r"^\s*([A-Za-z][\w-]*):\s*$", re.M)

# Any `platform:id` anywhere in the output.
ANY_TARGET = re.compile(r"\b\w+:\S+")

# An id a person would recognise reads like a name: it starts with a letter and
# continues with letters, digits, spaces, `_`, `-` or `.`. Everything else --
# room ids, phone numbers, numeric group ids, user handles -- is an internal
# identifier whatever platform produced it. This deliberately knows nothing
# about any particular service: the skill supports whatever the host supports,
# including platforms that did not exist when this was written, so there is no
# list of sigils to keep current.
READABLE_ID = re.compile(r"^[A-Za-z][\w .-]*$")

# `--list` annotations that mean one-to-one rather than a shared destination.
# English words it prints, not platforms: anything else is treated as a named
# room and offered by that name.
DIRECT_KINDS = {"dm", "chat", "direct", "private"}


def chat_platforms(listed: str | None = None) -> set[str]:
    """Lowercase names of every platform this machine has, for validation.

    Names come from the `platform:id` targets and from the section headings the
    listing groups them under, so a platform configured with only a home
    channel is still recognised. A replacement may return an empty set, which
    every caller reads as "cannot tell" and treats as passing.
    """
    out = chat_list() if listed is None else listed
    return ({t.split(":", 1)[0].lower() for t in ANY_TARGET.findall(out)}
            | {s.lower() for s in PLATFORM_HEADING.findall(out)})


def chat_target_ids(listed: str | None = None) -> list[str]:
    """Every `platform:id` target in the listing, for validating one against it."""
    out = chat_list() if listed is None else listed
    return ANY_TARGET.findall(out)


def platform_targets(platform: str) -> list[str]:
    """Every target this machine has on one platform, in listed order.

    `setup` auto-selects when there is exactly one and asks when there are
    several, so order matters only in what it shows the user.
    """
    # An empty platform makes the pattern below `\b:\S+`, which matches the
    # colon in every line of the listing and returns targets with no platform on
    # them (`:Ryan`). They look like data and are accepted by anything that does
    # not re-parse them. The one caller validates first, so this is a guard on
    # the seam rather than a live fault -- but returning shaped nonsense is the
    # wrong contract for a file whose whole job is to be re-implemented.
    if not (platform or "").strip():
        raise HostError("platform_targets needs a platform name")
    seen, targets = set(), []
    for match in re.findall(rf"\b{re.escape(platform)}:\S+", chat_list(platform)):
        target = match.rstrip(".,")
        if target not in seen:
            seen.add(target)
            targets.append(target)
    return targets


def chat_targets(listed: str) -> list[tuple[str, str, str]]:
    """[(target, label, how to offer it)] -- one per destination worth offering.

    The label matters as much as the target. An offer the user cannot evaluate
    is not an offer, and a raw room id or phone number is exactly that -- so an
    opaque target is described by its platform and kind, and only a
    human-readable id is quoted. Identical labels collapse: two direct-message
    targets on one platform are a single offer to name that platform.

    Everything here is derived from the listing itself. The platform name, the
    kind and the id all come from its output; nothing is special-cased, and a
    port must keep it that way -- no chat platform may be named in this file.
    """
    out: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    for line in listed.splitlines():
        m = CHAT_LINE.match(line)
        if not m:
            continue
        target, kind = m.group(1), (m.group(2) or "chat")
        platform, _, ident = target.partition(":")
        name = platform.capitalize()
        readable = bool(READABLE_ID.match(ident))
        label = f"{name} {kind}: {ident}" if readable else f"{name} {kind}"
        # The kind is the listing's own annotation, not a platform trait. A
        # named shared destination is offered by its name whatever the
        # annotation calls it -- group, channel, room; a one-to-one one by its
        # platform.
        if not readable:
            offer = name
        elif kind in DIRECT_KINDS:
            offer = f"{name} ({ident})"
        elif kind == "group":
            offer = f"the {ident} group chat"
        else:
            offer = f"the {ident} {kind}"
        if label in seen:
            continue
        seen.add(label)
        out.append((target, label, offer))
    return out


def target_hint() -> str:
    """Where to copy a known-good target from, for an error message."""
    return f"`{HOST_CLI} send --list`"


# --------------------------------------------------------------------------
# Seam 2 and 3: scheduling, and where a scheduled script must live
# --------------------------------------------------------------------------


def dispatcher_path() -> Path:
    """Where the dispatcher must be copied to before it can be scheduled.

    Hermes' scheduler refuses any script path outside this directory --
    absolute paths, `../` and symlinks are all rejected -- so the skill's own
    copy can never be scheduled directly. A host without that restriction
    should return the skill's own copy, which makes the deploy step a no-op.
    """
    return HOST_HOME / "scripts" / "tklr_alert_poller.py"


def workspace_pin_path() -> Path:
    """Where the resolved workspace is recorded for unattended runs.

    The dispatcher runs from a scheduler, in an environment that does not
    inherit the shell the workspace was chosen in. Re-resolving there reads
    different environment variables and can name a different directory, which
    is invisible: alerts are written in one workspace and polled in another,
    and every report says success. So setup resolves once and records the
    answer here, beside the dispatcher, and the dispatcher reads it instead of
    resolving again.

    Beside the dispatcher on purpose: a host that can schedule the dispatcher
    at all can write next to it, so the two cannot become separated.
    """
    return dispatcher_path().parent / "tklr-workspace-path"


def cron_job_present() -> bool | None:
    """Is the every-minute dispatcher job scheduled?

    True or False when the schedule could be read, None when it could not.
    None is not False: callers report "could not verify" rather than claiming
    the job is missing, because the repair for the two differs.
    """
    try:
        proc = _run([HOST_CLI, "cron", "list"], WRITE_TIMEOUT)
    except HostError:
        return None
    if proc.returncode != 0:
        return None
    return CRON_JOB_NAME in (proc.stdout or "")


def create_cron_job() -> tuple[bool, str]:
    """Schedule the dispatcher every minute. (ok, one line saying what happened).

    Called only after `cron_job_present()` returned False. A replacement that
    cannot schedule anything should return False with a message naming the
    command the user must run by hand -- an honest refusal here is fine, since
    the caller surfaces the message, but silently returning True is not: the
    missing job has no other symptom.
    """
    # --script takes the BARE FILENAME: the scheduler resolves it inside its own
    # scripts directory and rejects anything that escapes it.
    try:
        proc = _run([HOST_CLI, "cron", "create", "* * * * *",
                     "--script", dispatcher_path().name, "--no-agent",
                     "--name", CRON_JOB_NAME, "--deliver", "local"],
                    WRITE_TIMEOUT)
    except HostError as exc:
        return False, str(exc)
    if proc.returncode != 0:
        return False, (f"`{HOST_CLI} cron create` failed: "
                       f"{(proc.stderr or '').strip()}")
    if cron_job_present():
        return True, f"created cron job '{CRON_JOB_NAME}' — dispatching every minute"
    return False, (f"`{HOST_CLI} cron create` reported success but the job is "
                   f"not in `{HOST_CLI} cron list`")


def schedule_hint() -> str:
    """How to inspect the schedule by hand, for an error message."""
    return f"`{HOST_CLI} cron list`"
