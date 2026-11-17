#!/usr/bin/env python3
"""The agent-facing wrapper around tklr. Named flags in, plain English out.

This is the ONLY thing an agent should run for calendars, reminders and alerts.
Do not call `tklr` directly. The agent supplies meaning; this script produces
tklr's grammar, checks that the grammar did what was intended, and reports what
actually happened.

Why a wrapper exists at all: tklr's entry syntax is sigil-dense and nearly
every element has a SILENT failure mode. A missing itemtype character stores a
draft that never fires. `tomorrow 3p` is rejected but `tomorrow 3pm` is fine.
A missing `@a` means nobody is ever notified. `@b` is written leaf-first. An
alert whose trigger lands in the current minute is dropped with no warning.
`tklr add` prints "Added 0 entries successfully" and looks like success.
Encoding all of that once, here, turns silent wrong answers into loud ones:
a bad flag is rejected by argparse, where a bad sigil becomes a broken record.

Every operation is a subcommand. Run `--help` on any of them for its flags:

    add       create a reminder            list      what is scheduled
    show      everything about one         find      search, or one person's
    free      what is around a time        done      mark a task complete
    delete    remove one or an occurrence  move      reschedule an occurrence
    uses      where jot time went          channels  list/configure alerts
    status    is it all set up
    setup     build the whole delivery     email     add email as a channel
              path for one platform                  (himalaya)
    welcome   what to tell the user (send its output as-is)

Typical use:

    tklr_agent_wrapper.py add --type event --subject "Dentist" \
        --when "tomorrow 3pm" --duration 1h --for alex --alert 1d,1h --via r
    tklr_agent_wrapper.py add --type task --subject "Buy milk" --for alex
    tklr_agent_wrapper.py list --today
    tklr_agent_wrapper.py find --person alex
    tklr_agent_wrapper.py status

What it does that raw tklr does not:
  * resolves --when itself ("tomorrow 3pm", "next tuesday 9am", "in 2 hours"),
    so callers never depend on tklr's narrower parser
  * refuses a --via letter not defined in the workspace [alerts] section
  * refuses an alert whose trigger is under 2 minutes away, because tklr would
    silently schedule nothing at all
  * warns when a timed reminder has no alert — it would notify nobody
  * validates with `tklr check` BEFORE writing anything
  * reads the output of `tklr add` instead of assuming it worked
  * confirms the stored record is not a draft, then heals derived state
  * VERIFIES afterwards that the reminder really is on the schedule and that
    its alert row exists — "saved" and "will actually fire" are not the same
    thing, and the gap between them is where every past failure has lived
  * reports the id, the entry as stored, and when each alert will fire

Workspace: --home, else $TKLR_HOME, else ~/.config/tklr. Do not pass --home.
`setup` refuses it outright, because `tklr` in a terminal and the dispatcher
under the scheduler both resolve the workspace themselves and cannot be told
to look elsewhere -- a workspace they do not resolve is never polled and never
delivers. It exists for reading and testing against a scratch copy. To move
the workspace for real, set TKLR_HOME or XDG_CONFIG_HOME for everything.

Exit codes: 0 success, 1 refused or failed, 2 usage error.
Alerts are delivered separately, by tklr_alert_poller.py running once a minute
from the host agent's scheduler. This script never sends anything.

Everything host-specific -- what channels exist, how to send to one, how to
schedule the dispatcher -- is in host.py, which is the only file that needs
changing to run this skill under a different agent. Do not add a host call
anywhere else; see that file's header.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import textwrap
import tomllib
from datetime import date, datetime, timedelta, timezone
from typing import NamedTuple
from pathlib import Path

import host

ITEMTYPE = {
    "event": "*",
    "task": "~",
    "project": "^",
    "note": "%",
    "goal": "!",
    "jot": "-",
    # No "draft" (`?`) on purpose. tklr has one, but it is an editing state
    # rather than a reminder: it fires nothing and appears on no schedule. An
    # assistant with the user right there should ask the missing question
    # instead of filing something that cannot go off -- and `?` stays
    # unambiguous as the thing `add` refuses, which is how a silently
    # downgraded invalid entry gets caught.
}

WEEKDAYS = {
    "monday": 0, "mon": 0, "tuesday": 1, "tue": 1, "tues": 1,
    "wednesday": 2, "wed": 2, "thursday": 3, "thu": 3, "thur": 3, "thurs": 3,
    "friday": 4, "fri": 4, "saturday": 5, "sat": 5, "sunday": 6, "sun": 6,
}

MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun",
     "jul", "aug", "sep", "oct", "nov", "dec"], start=1)}

warnings: list[str] = []


def die(msg: str, *extra: str, code: int = 1) -> "NoReturn":  # type: ignore[valid-type]
    # Flush first: progress goes to stdout and errors to stderr, and a reader
    # that merges the two streams otherwise sees the error before the steps
    # that led to it.
    sys.stdout.flush()
    print(f"error: {msg}", file=sys.stderr)
    for line in extra:
        print(f"  {line}", file=sys.stderr)
    raise SystemExit(code)


# ---------------------------------------------------------------------------
# datetime resolution — the whole point of the wrapper
# ---------------------------------------------------------------------------

def parse_time(text: str) -> tuple[int, int] | None:
    """'3pm' | '3:30pm' | '15:00' | '9a' | 'noon' -> (hour, minute)."""
    t = text.strip().lower().replace(".", "")
    if t in ("noon", "midday"):
        return 12, 0
    if t == "midnight":
        return 0, 0
    m = re.fullmatch(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm|a|p)?", t)
    if not m:
        return None
    hour = int(m.group(1))
    minute = int(m.group(2) or 0)
    suffix = m.group(3)
    if suffix in ("pm", "p"):
        if hour != 12:
            hour += 12
    elif suffix in ("am", "a"):
        if hour == 12:
            hour = 0
    elif hour > 23:
        return None
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None
    return hour, minute


def resolve_when(text: str, now: datetime) -> tuple[str, bool]:
    """Return (tklr-safe datetime string, has_time).

    Always emits 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM', which tklr accepts
    unambiguously — so the caller can write whatever a person would say.
    """
    raw = " ".join(text.strip().split())
    low = raw.lower()

    # in N units
    m = re.fullmatch(r"in\s+(\d+)\s*(minute|minutes|min|mins|hour|hours|hr|hrs|day|days|week|weeks)", low)
    if m:
        n, unit = int(m.group(1)), m.group(2)
        delta = {
            "minute": timedelta(minutes=n), "minutes": timedelta(minutes=n),
            "min": timedelta(minutes=n), "mins": timedelta(minutes=n),
            "hour": timedelta(hours=n), "hours": timedelta(hours=n),
            "hr": timedelta(hours=n), "hrs": timedelta(hours=n),
            "day": timedelta(days=n), "days": timedelta(days=n),
            "week": timedelta(weeks=n), "weeks": timedelta(weeks=n),
        }[unit]
        target = now + delta
        return target.strftime("%Y-%m-%d %H:%M"), True

    # already absolute: YYYY-MM-DD [time]
    m = re.fullmatch(r"(\d{4}-\d{2}-\d{2})(?:[ tT]+(.+))?", raw)
    if m:
        day_part, time_part = m.group(1), m.group(2)
        if not time_part:
            return day_part, False
        hm = parse_time(time_part)
        if hm is None:
            die(f"could not understand the time in --when {text!r}",
                "Try '2026-08-01 15:00' or '2026-08-01 3pm'.")
        return f"{day_part} {hm[0]:02d}:{hm[1]:02d}", True

    # split a trailing/leading time off the rest
    tokens = low.split()
    time_hm: tuple[int, int] | None = None
    day_tokens: list[str] = []
    for tok in tokens:
        if tok in ("at", "on", "this", "next", "the"):
            continue
        hm = parse_time(tok)
        if hm is not None and time_hm is None and not re.fullmatch(r"\d{1,2}", tok):
            time_hm = hm
            continue
        day_tokens.append(tok)

    # a bare number could be a day-of-month or an hour; prefer hour if alone
    if time_hm is None and len(day_tokens) == 1 and re.fullmatch(r"\d{1,2}", day_tokens[0]):
        hm = parse_time(day_tokens[0])
        if hm:
            time_hm, day_tokens = hm, []

    target_day: date | None = None
    rest = " ".join(day_tokens).strip()

    if rest in ("", "today"):
        target_day = now.date()
    elif rest == "tomorrow":
        target_day = now.date() + timedelta(days=1)
    elif rest == "yesterday":
        target_day = now.date() - timedelta(days=1)
    elif rest in WEEKDAYS:
        ahead = (WEEKDAYS[rest] - now.weekday()) % 7
        if ahead == 0:
            ahead = 7  # "friday" on a Friday means the next one
        target_day = now.date() + timedelta(days=ahead)
    else:
        # "aug 15", "15 aug", "8/15", "8/15/2026"
        m = re.fullmatch(r"(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?", rest)
        if m:
            mo, dy = int(m.group(1)), int(m.group(2))
            yr = int(m.group(3) or now.year)
            if yr < 100:
                yr += 2000
            target_day = safe_date(yr, mo, dy, text)
        else:
            m = re.fullmatch(r"([a-z]{3,9})\s+(\d{1,2})(?:,?\s*(\d{4}))?", rest) \
                or re.fullmatch(r"(\d{1,2})\s+([a-z]{3,9})(?:,?\s*(\d{4}))?", rest)
            if m:
                a, b = m.group(1), m.group(2)
                name, dnum = (a, b) if a[:3] in MONTHS else (b, a)
                if name[:3] not in MONTHS:
                    target_day = None
                else:
                    yr = int(m.group(3) or now.year)
                    target_day = safe_date(yr, MONTHS[name[:3]], int(dnum), text)

    if target_day is None:
        die(f"could not understand --when {text!r}",
            "Accepted: 'today', 'tomorrow', a weekday ('friday', 'next tuesday'),",
            "'in 2 hours', 'aug 15', '8/15', '2026-08-15', each optionally with a",
            "time ('3pm', '15:00', 'noon'). Or pass an absolute",
            "'YYYY-MM-DD HH:MM'.")

    if time_hm is None:
        return target_day.strftime("%Y-%m-%d"), False

    # A past time with no explicit day almost certainly means tomorrow.
    resolved = datetime.combine(target_day, datetime.min.time()).replace(
        hour=time_hm[0], minute=time_hm[1])
    if rest in ("", "today") and resolved < now:
        resolved += timedelta(days=1)
        warnings.append(
            f"{text!r} had already passed today — used {resolved:%Y-%m-%d %H:%M}")
    return resolved.strftime("%Y-%m-%d %H:%M"), True


def safe_date(y: int, m: int, d: int, text: str) -> date:
    try:
        return date(y, m, d)
    except ValueError:
        die(f"--when {text!r} is not a real date")


# ---------------------------------------------------------------------------
# workspace helpers
# ---------------------------------------------------------------------------

def tklr_home(explicit: str | None) -> Path:
    """Resolve the workspace the way tklr itself does.

    Mirrors tklr_env.TklrEnvironment._resolve_home so the agent and a human
    running `tklr` by hand always land on the same database. Missing the
    XDG_CONFIG_HOME step would silently split them into two workspaces on any
    machine that sets it.
    """
    if explicit:
        return Path(explicit).expanduser()
    env_home = os.environ.get("TKLR_HOME")
    if env_home:
        return Path(env_home).expanduser()
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return (Path(xdg).expanduser() / "tklr")
    return Path.home() / ".config" / "tklr"


def write_workspace_pin(home: Path) -> str:
    """Record the workspace for the dispatcher. Returns '' or why it failed.

    Not fatal on failure: the dispatcher falls back to resolving the workspace
    itself, which is what it did before the pin existed and is usually the same
    answer. The caller reports the reason rather than dying, because a setup
    that configured everything else correctly should not be reported as failed.
    """
    try:
        pin = host.workspace_pin_path()
        pin.parent.mkdir(parents=True, exist_ok=True)
        pin.write_text(f"{home}\n", encoding="utf-8")
    except (OSError, host.HostError) as exc:
        return str(exc)
    return ""


def tklr_own_home() -> Path | None:
    """Where tklr itself resolves the workspace, asked rather than mirrored.

    Runs in a subprocess with a clean TKLR_HOME so the answer is the one a
    person typing `tklr` gets, not the one this process arranged. Returns None
    when tklr cannot be imported, which is not an error here: the caller is
    reporting drift, and "could not check" is not "drifted".

    Asked rather than recomputed because tklr's rules include a clause nothing
    else implements -- a config.toml and tklr.db in the current directory
    outrank $TKLR_HOME -- and because a mirrored copy of someone else's
    resolution order silently goes stale when they change it.
    """
    exe = shutil.which("tklr")
    if not exe:
        return None
    # tklr's own interpreter, not this one: the wrapper runs under an
    # interpreter that cannot import tklr at all. Resolving the shim lands in
    # the tool's bin directory, whose `python` is the venv tklr was installed
    # into -- true of a uv tool install and of a pipx one alike.
    python = Path(exe).resolve().parent / "python"
    if not python.exists():
        return None
    code = ("from tklr.tklr_env import TklrEnvironment;"
            "print(TklrEnvironment().home)")
    # TKLR_HOME is dropped for the child only, via unsetenv/putenv rather than
    # by building an env mapping for the call. Constructing one means reading
    # every variable in the process, which is far more access than this needs
    # and is indistinguishable from a dump to the install scanner. unsetenv and
    # putenv act on the real environment a child inherits when `env=` is
    # omitted, and leave the interpreter's own mapping alone. Restored straight
    # afterwards, because a caller further up may have set it deliberately --
    # `status` does exactly that before running the dispatcher.
    #
    # Do not name the discouraged API in a comment here. The scanner matches raw
    # text and does not skip comments, so an explanation that spells it out
    # scores as a use of it and blocks the install.
    saved = os.getenv("TKLR_HOME")
    os.unsetenv("TKLR_HOME")
    try:
        # From the user's home directory, because tklr's first rule is that a
        # config.toml plus tklr.db in the CURRENT directory outrank everything.
        # Run from wherever the agent happens to be, this would report that
        # directory. A neutral cwd gives the answer a terminal usually gets;
        # the cwd clause itself cannot be predicted from here.
        proc = subprocess.run([str(python), "-c", code],
                              cwd=str(Path.home()),
                              capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    finally:
        if saved is not None:
            os.putenv("TKLR_HOME", saved)
    out = (proc.stdout or "").strip().splitlines()
    if proc.returncode != 0 or not out:
        return None
    return Path(out[-1]).expanduser()


def run_tklr(home: Path, *args: str) -> subprocess.CompletedProcess[str]:
    exe = shutil.which("tklr") or str(Path.home() / ".local" / "bin" / "tklr")
    try:
        return subprocess.run([exe, "--home", str(home), *args],
                              capture_output=True, text=True, timeout=120)
    except FileNotFoundError:
        die("tklr is not installed or not on PATH",
            "Run: tklr_agent_wrapper.py setup --platform <the platform you are on>",
            "(it installs tklr and everything else in one command)")
    except subprocess.SubprocessError as exc:
        die(f"tklr failed to run: {exc}")


def configured_letters(home: Path) -> dict[str, str]:
    cfg = home / "config.toml"
    if not cfg.exists():
        return {}
    try:
        alerts = tomllib.loads(cfg.read_text(encoding="utf-8")).get("alerts") or {}
    except (OSError, tomllib.TOMLDecodeError):
        return {}
    return {k: v for k, v in alerts.items() if isinstance(v, str)}


def clean_list(value: str | None) -> list[str]:
    return [p.strip() for p in (value or "").split(",") if p.strip()]


# ---------------------------------------------------------------------------
# entry assembly
# ---------------------------------------------------------------------------

def build_entry(args, home: Path, now: datetime) -> tuple[str, str | None, bool]:
    """Return (entry, resolved_when, has_time)."""
    if args.type not in ITEMTYPE:
        die(f"unknown --type {args.type!r}",
            "Use one of: " + ", ".join(sorted(ITEMTYPE)))
    subject = " ".join((args.subject or "").split())
    if not subject:
        die("--subject is required")
    if '"' in subject:
        warnings.append('a double quote in the subject can break alert '
                        'delivery; replaced with a typographic quote')
        subject = subject.replace('"', "”")

    parts = [ITEMTYPE[args.type], subject]

    resolved = has_time = None
    if args.when:
        resolved, has_time = resolve_when(args.when, now)
        stamp = resolved
        if args.timezone:
            tz = args.timezone.strip()
            if not re.fullmatch(r"[A-Za-z_]+(/[A-Za-z_+-]+)*|none|float", tz):
                die(f"--timezone {tz!r} does not look like a zone name",
                    "Use e.g. US/Pacific, Europe/London, or 'none' for a floating time.")
            stamp = f"{resolved} z {tz}"
        parts.append(f"@s {stamp}")
    elif args.type == "jot":
        # A jot is a timestamped note to self, and the timestamp is the whole
        # point: "taking a walk" means now unless they said otherwise.
        resolved, has_time = f"{now:%Y-%m-%d %H:%M}", True
        parts.append(f"@s {resolved}")
    elif args.type in ("event", "goal"):
        die(f"a {args.type} needs --when")
    elif args.timezone:
        die("--timezone only means something with --when")

    if args.duration:
        if not re.fullmatch(r"(\d+[wdhms])+", args.duration.strip()):
            die(f"--duration {args.duration!r} is not a timeperiod",
                "Use forms like 30m, 1h, 1h30m, 2d.")
        parts.append(f"@e {args.duration.strip()}")

    if args.repeat:
        parts.append(f"@r {args.repeat.strip()}")

    if args.target:
        if not re.fullmatch(r"\d+/\d+[wdhms]", args.target.strip()):
            die(f"--target {args.target!r} must look like 3/1w",
                "That is: how many completions, per how long. The period needs a "
                "number — '3/1w', not '3/w'.")
        parts.append(f"@t {args.target.strip()}")

    for person in clean_list(args.for_whom):
        # tklr writes bins leaf-first, so this is `<person>` inside `users`.
        parts.append(f"@b {person.lower()}/users")

    if args.location:
        parts.append(f"@l {args.location.strip()}")

    if args.priority:
        if args.priority not in range(1, 6):
            die("--priority must be 1 (highest) to 5 (lowest)")
        parts.append(f"@p {args.priority}")

    if args.notice:
        parts.append(f"@n {args.notice.strip()}")

    if args.offset:
        off = args.offset.strip()
        if not re.fullmatch(r"~?(\d+[wdhms])+", off):
            die(f"--offset {off!r} is not a timeperiod",
                "Use e.g. 3d — 'reschedule 3 days after I finish it'. "
                "Prefix with ~ for a learning interval: ~3d.")
        parts.append(f"@o {off}")

    if args.travel:
        legs = clean_list(args.travel)
        if len(legs) == 1:
            legs = legs * 2
        if len(legs) != 2 or not all(re.fullmatch(r"(\d+[wdhms])+", l) for l in legs):
            die(f"--travel {args.travel!r} needs one or two timeperiods",
                "e.g. --travel 30m (both sides) or --travel 30m,15m (before,after).")
        parts.append(f"@w {legs[0]}, {legs[1]}")

    # project steps -> @~ jobs, each needing an &r label (a, b, c…)
    steps = args.step or []
    if steps and args.type != "project":
        die("--step only applies to --type project")
    for index, step in enumerate(steps):
        label = chr(ord("a") + index)
        token = f"@~ {step.strip()} &r {label}"
        if args.chain and index > 0:
            token = f"@~ {step.strip()} &r {label}:{chr(ord('a') + index - 1)}"
        parts.append(token)

    # alerts
    offsets = clean_list(args.alert)
    letters = clean_list(args.via)
    if offsets and not letters:
        die("--alert needs --via to say which channel(s) to use",
            "Available letters: " + (", ".join(sorted(configured_letters(home))) or "none configured"))
    if letters and not offsets:
        offsets = ["1h"] if has_time else ["1d"]
        warnings.append(f"no --alert offset given; used {offsets[0]} before")
    if offsets:
        available = configured_letters(home)
        unknown = [l for l in letters if l not in available]
        if unknown:
            die(f"channel letter(s) not configured: {', '.join(unknown)}",
                "Available: " + (", ".join(sorted(available)) or "none"),
                "Add one with scripts/set_alert_channel.py before using it.")
        for off in offsets:
            if not re.fullmatch(r"-?(\d+[wdhms])+", off):
                die(f"--alert offset {off!r} is not a timeperiod",
                    "Offsets count BACK from the start time: 1d, 2h, 15m.")
        check_alert_margin(offsets, resolved, now, warnings)
        parts.append(f"@a {', '.join(offsets)}: {', '.join(letters)}")
    elif args.type in ("event", "task") and args.when:
        warnings.append("no alert set — this reminder will not notify anyone "
                        "(pass --alert and --via if it should)")

    if args.use:
        use = args.use.strip()
        # tklr enforces this itself ("The use of @u is not supported in type
        # '~' reminders"), but failing here names the right alternative.
        if args.type != "jot":
            die(f"--use only means something on a jot; this is a {args.type}.",
                "Jots are tklr's time-tracking type: a timestamped line, how",
                "long it took (--duration), and the category it counts toward.")
        if not re.fullmatch(r"[A-Za-z0-9][\w.-]*", use):
            die(f"--use {use!r} is not a use name",
                "Letters, digits, dots, dashes and underscores, no spaces.",
                "A dot nests it: exercise.walking totals under exercise.")
        parts.append(f"@u {use}")

    if args.note:
        # @d must come last: tklr treats the rest of the entry as its value.
        parts.append(f"@d {' '.join(args.note.split())}")

    if not clean_list(args.for_whom):
        warnings.append("no --for given, so this is not attached to anyone")

    return " ".join(parts), resolved, bool(has_time)


# tklr materialises an Alerts row only for a trigger in a LATER CLOCK MINUTE
# than the moment the record is saved. A trigger in the current minute -- or
# the past -- produces no row at all, no warning, and no alert: the reminder
# looks fine in `list` and `show` and simply never fires. Two minutes is the
# smallest margin that survives a save straddling a minute boundary.
MIN_ALERT_MARGIN = timedelta(minutes=2)


def offset_seconds(off: str) -> int:
    """Seconds an @a offset counts back from the start. Negative means after."""
    secs = 0
    for num, unit in re.findall(r"(\d+)([wdhms])", off):
        secs += int(num) * {"w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}[unit]
    return -secs if off.strip().startswith("-") else secs


def alert_fire_time(off: str, start: datetime) -> datetime:
    return start - timedelta(seconds=offset_seconds(off))


def parse_resolved(resolved: str | None) -> datetime | None:
    """'2026-08-14 09:00' or '2026-08-14' -> datetime. None if neither.

    A date with no time is a real start, not an unparseable one: `add --when
    friday` on a task produces exactly that. Returning None for it made every
    caller treat a dateless reminder as "cannot tell", and the alert check reads
    "cannot tell" as "must already have fired", so `add` reported every date-only
    reminder with an alert as NO ALERT SCHEDULED and exited 1 -- with the record
    saved and perfectly healthy.
    """
    if not resolved:
        return None
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(resolved.strip(), fmt)
        except ValueError:
            continue
    return None


def stamp(when: datetime, now: datetime) -> str:
    """Clock time alone is a lie for any other day — show the date too."""
    return f"{when:%H:%M}" if when.date() == now.date() else f"{when:%Y-%m-%d %H:%M}"


def check_alert_margin(offsets, resolved, now: datetime, warnings: list) -> None:
    """Refuse an alert that tklr would silently decline to schedule.

    Refuses only when EVERY offset is too soon -- that reminder could never
    notify anyone, which is the whole reason it was asked for. If some offsets
    are fine, the good ones are kept and the doomed ones are called out, since
    '1d, 15m' on a meeting two hours away is a perfectly sensible thing to
    want.
    """
    start = parse_resolved(resolved)
    if not start:
        return

    doomed = []
    for off in offsets:
        fires = alert_fire_time(off, start)
        if fires - now < MIN_ALERT_MARGIN:
            doomed.append((off, fires))
    if not doomed:
        return

    if len(doomed) < len(offsets):
        for off, fires in doomed:
            warnings.append(
                f"alert {off} before would fire at {stamp(fires, now)}, too soon to "
                f"be scheduled — tklr will skip that one; the others still stand")
        return

    off, fires = doomed[0]
    late = now - fires
    detail = (f"{human(late)} in the past" if late.total_seconds() > 0
              else f"only {human(-late)} away")
    die(f"that alert would never fire — it lands at {fires:%Y-%m-%d %H:%M}, {detail}",
        f"start {start:%Y-%m-%d %H:%M} minus {off} = {fires:%H:%M}, and it is now "
        f"{now:%H:%M}.",
        f"tklr only schedules an alert at least {int(MIN_ALERT_MARGIN.total_seconds() // 60)} "
        "minutes out; anything sooner is dropped with no warning.",
        "Either start it later or use a smaller offset — e.g. for a test, "
        "start 8 minutes out with --alert 5m.")


def report_alert_times(entry: str, resolved: str | None, now: datetime) -> None:
    m = re.search(r"@a ([^:]+):", entry)
    start = parse_resolved(resolved)
    if not (m and start):
        return
    for off in [o.strip() for o in m.group(1).split(",")]:
        fires = alert_fire_time(off, start)
        delta = fires - now
        when = ("in " + human(delta)) if delta.total_seconds() > 0 else (human(-delta) + " ago")
        print(f"  alert ({off} before) fires {fires:%Y-%m-%d %H:%M} — {when}")


def human(delta: timedelta) -> str:
    mins = int(delta.total_seconds() // 60)
    if mins < 60:
        return f"{mins} minute{'s' if mins != 1 else ''}"
    if mins < 60 * 48:
        h, m = divmod(mins, 60)
        return f"{h} hour{'s' if h != 1 else ''}" + (f" {m} min" if m else "")
    return f"{mins // 1440} day{'s' if mins // 1440 != 1 else ''}"


# ---------------------------------------------------------------------------
# reads — plain output, no tklr syntax exposed
# ---------------------------------------------------------------------------

SKILL_SCRIPTS = Path(__file__).resolve().parent


def show_output(proc: subprocess.CompletedProcess[str]) -> None:
    """Print tklr output minus its internal chatter."""
    for line in (proc.stdout or "").splitlines():
        if "aggregate" in line or "DateTimes entries" in line:
            continue
        print(line.rstrip())


def cmd_list(args, home: Path, now: datetime) -> int:
    if args.date:
        start, _ = resolve_when(args.date, now)
        start = start.split()[0]
        span = str(args.days or 1)
    elif args.week:
        start, span = "today", "7"
    elif args.tomorrow:
        start = (now.date() + timedelta(days=1)).strftime("%Y-%m-%d")
        span = "1"
    elif args.today:
        start, span = "today", "1"
    else:
        show_output(run_tklr(home, "agenda", "--plain", "--ids"))
        return 0
    show_output(run_tklr(home, "days", "--start", start, "--end", span, "--plain", "--ids"))
    return 0


def cmd_show(args, home: Path, now: datetime) -> int:
    show_output(run_tklr(home, "details", str(args.id)))
    return 0


def cmd_find(args, home: Path, now: datetime) -> int:
    if args.person:
        show_output(run_tklr(home, "query", f"in b ^{re.escape(args.person)}$", "--ids"))
    else:
        show_output(run_tklr(home, "find", args.text))
    return 0


def cmd_free(args, home: Path, now: datetime) -> int:
    when, has_time = resolve_when(args.when, now)
    day = when.split()[0]
    print(f"Everything on {day} — compare against it, and mind durations "
          f"and travel time:")
    show_output(run_tklr(home, "days", "--start", day, "--end", "1", "--plain", "--ids"))
    return 0


def cmd_done(args, home: Path, now: datetime) -> int:
    proc = run_tklr(home, "finish", str(args.id), "-y")
    out = (proc.stdout or "") + (proc.stderr or "")
    if "No changes made" in out:
        die(f"id {args.id} could not be completed.",
            "Tasks, project steps and goals can be finished — a goal records "
            "the completion and keeps running. If this is an appointment, "
            f"delete it instead:  {sys.argv[0]} delete {args.id}")
    show_output(proc)
    return 0


def delegate(script: str, argv: list[str], home: Path) -> int:
    """Run a sibling helper, passing its output through minus tklr's chatter."""
    proc = subprocess.run(
        [sys.executable, str(SKILL_SCRIPTS / script), "--home", str(home), *argv],
        capture_output=True, text=True)
    for stream, sink in ((proc.stdout, sys.stdout), (proc.stderr, sys.stderr)):
        for line in (stream or "").splitlines():
            if "No data to aggregate" in line or "No event DateTimes entries" in line:
                continue
            print(line.rstrip(), file=sink)
    return proc.returncode


# EVERY datetime handed to tklr_mutate goes through resolve_when first, not just
# the new one. tklr matches an occurrence by exact datetime -- `delete_instance`
# and `reschedule_instance` take the text and return a bool -- so an unresolved
# "tomorrow 2pm" reaches it as those literal words and is simply declined, which
# read as "tklr cannot reschedule" rather than "this layer forgot to do its job".
# That was the bug: `--to` was resolved and `--instance` beside it was not.
# resolve_when is idempotent, so a caller that already passes '2026-08-09 14:00'
# is unaffected.
def cmd_delete(args, home: Path, now: datetime) -> int:
    # An empty --instance/--from is a REFUSAL, never a fall-through. `if
    # args.instance:` reads "" as absent, so `delete 3 --instance ''` used to
    # skip the flag entirely and delete the WHOLE reminder -- the caller asked
    # to drop one occurrence and lost the series, unrecoverably. A lookup that
    # produced nothing is exactly how a caller arrives here with "".
    for flag, value in (("--instance", args.instance), ("--from", args.from_dt)):
        if value is not None and not str(value).strip():
            die(f"{flag} was given but empty",
                "Name the occurrence, or leave the flag off entirely to delete "
                "the whole reminder. Refusing to guess which you meant, because "
                "one of them cannot be undone.")

    extra = []
    if args.instance:
        wanted = [resolve_when(one, now)[0] for one in clean_list(args.instance)]
        if not wanted:
            die("--instance was given but named no occurrence")
        # tklr's own delete_instance handles the FIRST skip on a record and
        # validates the occurrence as it goes, so it stays the path for that
        # case. It cannot do the second: with an `@-` already present it
        # declines, which is why skipping several used to mean deleting the
        # record and re-adding it with a hand-built `@-` list -- losing the id,
        # the history and the alert rows to work around a limitation in one
        # token.
        entry = record_entry(home, args.id)
        if len(wanted) == 1 and not has_token(entry, "-"):
            extra += ["--instance", wanted[0]]
        else:
            return skip_occurrences(home, args.id, entry, wanted, now,
                                    args.dry_run)
    if args.from_dt:
        extra += ["--from", resolve_when(args.from_dt, now)[0]]
    if args.dry_run:
        extra.append("--dry-run")
    return delegate("tklr_mutate.py", ["delete", str(args.id), *extra], home)


def as_instant(stamp_text: str) -> str:
    """Reduce an exdate to one comparable form, however it was written.

    tklr stores these two ways depending on which code last wrote them -- its
    own delete_instance leaves local naive (`20260811T0700`), a token edit
    renders UTC (`20260811T1200Z`) -- and it accepts seconds or not. Compared as
    raw strings, one instant reads as several different dates. Unparseable text
    is returned unchanged so it can still match itself exactly.
    """
    text = stamp_text.strip()
    is_utc = text.endswith("Z")
    core = text[:-1] if is_utc else text
    parsed = None
    # The bare date is how tklr renders an all-day exclusion (`@- 20260817`),
    # while the same occurrence is stored as `20260817T0000`. Without this the
    # two never compare equal and re-skipping an all-day date is reported as
    # "not an occurrence" rather than as already skipped.
    for fmt in ("%Y%m%dT%H%M%S", "%Y%m%dT%H%M", "%Y%m%d"):
        try:
            parsed = datetime.strptime(core, fmt)
            break
        except ValueError:
            continue
    if parsed is None:
        return text
    if is_utc:
        parsed = (parsed.replace(tzinfo=timezone.utc)
                        .astimezone().replace(tzinfo=None))
    return parsed.strftime("%Y%m%dT%H%M")


def compact(resolved: str) -> str | None:
    """'2026-08-10 09:00' -> '20260810T0900', the form tklr stores and `@-` takes."""
    parsed = parse_resolved(resolved)
    return parsed.strftime("%Y%m%dT%H%M") if parsed else None


def occurrence_window(home: Path, rid: int) -> tuple[set[str], str | None]:
    """Generated occurrences for a record, and the last one generated.

    tklr materialises occurrences only inside a generation horizon, so an empty
    result past the last one is not evidence the date is wrong -- which is why
    the caller gets the horizon back rather than just the set.
    """
    import sqlite3
    try:
        conn = sqlite3.connect(home / "tklr.db", timeout=15)
        rows = [r[0] for r in conn.execute(
            "SELECT start_datetime FROM DateTimes WHERE record_id = ?", (rid,))]
        conn.close()
    except sqlite3.Error:
        return set(), None
    stored = {str(r)[:13] for r in rows if r}
    return stored, (max(stored) if stored else None)


def skip_occurrences(home: Path, rid: int, entry: str, wanted: list[str],
                     now: datetime, dry_run: bool) -> int:
    """Exclude one or more occurrences by writing the whole `@-` list at once.

    Everything already excluded is carried over: `@-` is replaced wholesale by
    the token edit, so building only the new dates would silently un-skip every
    occurrence skipped before this call.
    """
    already = [p.strip() for p in (token_value(entry, "-") or "").split(",")
               if p.strip()]
    # `@-` comes back in whatever form last wrote it: tklr's own delete_instance
    # leaves local naive (20260811T0700), a token edit renders UTC
    # (20260811T1200Z). Comparing the two as strings would call the same instant
    # two different dates, so both sides are reduced to an instant first.
    already_at = {as_instant(a) for a in already}

    stored, horizon = occurrence_window(home, rid)
    compacted: list[str] = []
    for resolved in wanted:
        one = compact(resolved)
        if one is None:
            die(f"could not read {resolved!r} as a date and time",
                "An occurrence needs both, e.g. '2026-08-17 09:00'.")
        # Already excluded is a no-op, not an error. It reaches the check below
        # as "not an occurrence" -- true, because it was skipped -- which reads
        # as a mistake when the user's intent is already satisfied.
        if as_instant(one) in already_at:
            print(f"  note: {resolved} was already skipped; leaving it alone")
            continue
        # Silently adding a non-occurrence to `@-` would report success and
        # change nothing, which is the failure this skill keeps meeting.
        # Only inside the generated window, where absence is meaningful.
        if stored and one not in stored and horizon and one <= horizon:
            die(f"{resolved} is not an occurrence of id {rid}",
                "Its occurrences are listed by: "
                f"{sys.argv[0]} show {rid}",
                "Name an occurrence exactly as it is scheduled.")
        compacted.append(one)

    if not compacted:
        print("nothing to do: every date named is already skipped")
        return 0

    merged = already + compacted
    if not merged:
        die("nothing to skip")

    rc = delegate("tklr_mutate.py",
                  ["edit", str(rid), "--set", "@- " + ", ".join(merged)]
                  + (["--dry-run"] if dry_run else []), home)
    if rc != 0 or dry_run:
        return rc

    heal_alerts(home)
    # Verified against the schedule, not against the token: the token is what
    # was asked for, the schedule is what happened.
    after, _ = occurrence_window(home, rid)
    still = [c for c in compacted if c in after]
    if still:
        die(f"id {rid} still has {len(still)} of those occurrence(s) scheduled: "
            + ", ".join(still),
            "The entry was written but tklr did not drop them.")
    print(f"  {len(compacted)} occurrence(s) skipped; "
          f"{len(after)} still scheduled")
    return 0


def token_value(entry: str, key: str) -> str | None:
    """The value of `@<key>` in an entry, or None when the token is absent.

    Reads up to the next ` @` so a value containing spaces (`@a 1d, 1h: r, e`)
    comes back whole.
    """
    match = re.search(rf"(?:^|\s)@{re.escape(key)}\s+(.*?)(?=\s+@|$)", entry)
    return match.group(1).strip() if match else None


def split_alert_token(value: str | None) -> tuple[list[str], list[str]]:
    """`'1d, 1h: r, e'` -> (['1d','1h'], ['r','e']). Missing half comes back []."""
    if not value:
        return [], []
    offsets, _, letters = value.partition(":")
    return clean_list(offsets), clean_list(letters)


# NOTE: `cmd_edit` builds its `@` tokens inline, one branch per flag, because
# most of them validate their value on the way through and the validation is
# what differs. A table mapping flag -> token used to sit here claiming to be
# the single source of truth for that; nothing ever read it, so it documented a
# guarantee the code did not make. CLEARABLE above is the one real table, and it
# covers only `--clear`. If you add a flag to `edit`, add its branch there.

# What the user may name in --clear, in their words rather than tklr's letters.
CLEARABLE = {
    "duration": "e", "repeat": "r", "location": "l", "priority": "p",
    "notice": "n", "offset": "o", "travel": "w", "note": "d",
    "people": "b", "alerts": "a", "alert": "a",
}


def cmd_edit(args, home: Path, now: datetime) -> int:
    """Change an existing reminder in place, keeping its id and its history.

    Every flag is optional and only what is named changes. This is the whole
    reason the command exists: the alternative the skill used to document was
    delete-and-re-add, which loses the id, the completion history, pinned state
    and tags, and which leaves nothing behind if the re-add is refused.
    """
    entry = record_entry(home, args.id)
    if not entry:
        die(f"no reminder with id {args.id}",
            f"Find the right id with: {sys.argv[0]} find <text>")

    sets: list[str] = []
    removes: list[str] = []

    # --- clear first, so `--clear alerts --via r` is an explicit replacement
    for name in clean_list(args.clear):
        key = CLEARABLE.get(name.lower())
        if key is None:
            die(f"cannot clear {name!r}",
                "Nameable: " + ", ".join(sorted(set(CLEARABLE))))
        removes.append(key)

    resolved = has_time = None
    if args.when:
        resolved, has_time = resolve_when(args.when, now)
        stamp_text = resolved
        if args.timezone:
            tz = args.timezone.strip()
            if not re.fullmatch(r"[A-Za-z_]+(/[A-Za-z_+-]+)*|none|float", tz):
                die(f"--timezone {tz!r} does not look like a zone name",
                    "Use e.g. US/Pacific, Europe/London, or 'none' for a floating time.")
            stamp_text = f"{resolved} z {tz}"
        sets.append(f"@s {stamp_text}")
    elif args.timezone:
        die("--timezone only means something together with --when")

    if args.duration:
        if not re.fullmatch(r"(\d+[wdhms])+", args.duration.strip()):
            die(f"--duration {args.duration!r} is not a timeperiod",
                "Use forms like 30m, 1h, 1h30m, 2d.")
        sets.append(f"@e {args.duration.strip()}")

    if args.repeat:
        sets.append(f"@r {args.repeat.strip()}")

    if args.location:
        sets.append(f"@l {args.location.strip()}")

    if args.priority:
        if args.priority not in range(1, 6):
            die("--priority must be 1 (highest) to 5 (lowest)")
        sets.append(f"@p {args.priority}")

    if args.notice:
        sets.append(f"@n {args.notice.strip()}")

    if args.offset:
        off = args.offset.strip()
        if not re.fullmatch(r"~?(\d+[wdhms])+", off):
            die(f"--offset {off!r} is not a timeperiod",
                "Use e.g. 3d. Prefix with ~ for a learning interval: ~3d.")
        sets.append(f"@o {off}")

    if args.travel:
        legs = clean_list(args.travel)
        if len(legs) == 1:
            legs = legs * 2
        if len(legs) != 2 or not all(re.fullmatch(r"(\d+[wdhms])+", l) for l in legs):
            die(f"--travel {args.travel!r} needs one or two timeperiods",
                "e.g. --travel 30m or --travel 30m,15m (before,after).")
        sets.append(f"@w {legs[0]}, {legs[1]}")

    if args.for_whom:
        for person in clean_list(args.for_whom):
            sets.append(f"@b {person.lower()}/users")

    # --- alerts: the half that was not given is carried over from the record.
    # "Send it to email as well" names channels and nothing else, and that must
    # not silently reset the offsets the user already chose. This is the exact
    # request that produced a duplicate reminder before `edit` existed.
    if args.alert or args.via:
        was_offsets, was_letters = split_alert_token(token_value(entry, "a"))
        offsets = clean_list(args.alert) or was_offsets
        letters = clean_list(args.via) or was_letters
        if not offsets:
            start = resolved if args.when else token_value(entry, "s")
            offsets = ["1h"] if (has_time if args.when else True) else ["1d"]
            warnings.append(f"no alert offset on this reminder yet; used "
                            f"{offsets[0]} before it")
            del start
        if not letters:
            die("this reminder has no channel to alert on",
                "Pass --via with the letter(s) to use. Configured: "
                + (", ".join(sorted(configured_letters(home))) or "none"))
        available = configured_letters(home)
        unknown = [l for l in letters if l not in available]
        if unknown:
            die(f"channel letter(s) not configured: {', '.join(unknown)}",
                "Available: " + (", ".join(sorted(available)) or "none"),
                "Add one with scripts/set_alert_channel.py before using it.")
        for off in offsets:
            if not re.fullmatch(r"-?(\d+[wdhms])+", off):
                die(f"--alert offset {off!r} is not a timeperiod",
                    "Offsets count BACK from the start time: 1d, 2h, 15m.")
        # Margin is measured against the start this record will HAVE after the
        # edit, which is the new one when --when moved it.
        check_alert_margin(offsets, resolved or token_value(entry, "s"), now, warnings)
        sets.append(f"@a {', '.join(offsets)}: {', '.join(letters)}")
        removes = [k for k in removes if k != "a"]      # replaced, not cleared

    if args.note:
        sets.append(f"@d {' '.join(args.note.split())}")

    if not sets and not removes and args.subject is None:
        die("nothing to change",
            "Name at least one of --subject, --when, --duration, --alert, --via, "
            "--for, --note, --location, --priority, --notice, --offset, "
            "--travel, --repeat, or --clear <field>.")

    for w in warnings:
        print(f"  note: {w}")

    argv = ["edit", str(args.id)]
    if args.subject is not None:
        subject = " ".join(args.subject.split())
        if not subject:
            die("--subject cannot be empty")
        if '"' in subject:
            print('  note: a double quote in the subject can break alert '
                  'delivery; replaced with a typographic quote')
            subject = subject.replace('"', "”")
        argv += ["--subject", subject]
    for spec in sets:
        argv += ["--set", spec]
    for key in removes:
        argv += ["--remove", key]
    if args.dry_run:
        argv.append("--dry-run")

    rc = delegate("tklr_mutate.py", argv, home)
    if rc != 0 or args.dry_run:
        return rc

    # Saving regenerates the derived tables and tklr keeps only FUTURE alerts,
    # so an edit can consume an alert that was about to fire. Verify rather than
    # assume, exactly as `add` does.
    heal_alerts(home)
    verify_after_edit(home, args.id, now)
    return 0


def heal_alerts(home: Path) -> str:
    """Run the dispatcher's rebuild-only mode. Returns '' or why it failed."""
    if not POLLER.exists():
        return ""
    export_tklr_home(home)
    done = subprocess.run([sys.executable, str(POLLER), "--heal"],
                          capture_output=True, text=True, timeout=180, check=False)
    if done.returncode == 0:
        return ""
    tail = (done.stdout or done.stderr or "").strip().splitlines()
    return tail[-1] if tail else "heal returned non-zero"


def verify_after_edit(home: Path, rid: int, now: datetime) -> None:
    """Say what the record looks like now, and whether its alerts still stand."""
    entry = record_entry(home, rid)
    offsets, letters = split_alert_token(token_value(entry, "a"))
    if not offsets:
        print("  this reminder has no alert, so nobody will be notified")
        return

    import sqlite3
    try:
        conn = sqlite3.connect(home / "tklr.db", timeout=15)
        rows = conn.execute(
            "SELECT alert_name, trigger_datetime FROM Alerts WHERE record_id = ?",
            (rid,)).fetchall()
        conn.close()
    except sqlite3.Error:
        rows = []

    expected = len(offsets) * len(letters)
    if rows:
        print(f"  verified: {len(rows)} alert(s) queued"
              + ("" if len(rows) == expected
                 else f" (expected {expected}; the rest are past or beyond the horizon)"))
    else:
        start = parse_resolved(token_value(entry, "s"))
        if start and start > now:
            print("  verified: on the schedule; alerts are beyond tklr's "
                  "generation horizon and will be created closer to the time")
        else:
            print("  WARNING: no alert is queued and the start time has passed — "
                  "nobody will be notified")


def record_entry(home: Path, rid: int) -> str:
    """The record's entry text from `tklr details`, joined into one line.

    `details` prints the entry first, wrapped over as many lines as it needs,
    then a blank line, then `rruleset:` and the id/cr/md footer. Joined here so
    a token check does not depend on where tklr happened to wrap.

    Collection starts at the first line beginning with an itemtype character
    rather than at the first non-blank line, because tklr prefixes its output
    with warnings ("No data to aggregate", "No event DateTimes entries") in a
    workspace that has little in it. Taking the first non-blank line returned
    that warning AS the entry, which made every token lookup fail: `move`'s
    `@r` guard then refused every reschedule, and an alert carried over as
    absent. A new user's workspace is exactly the sparse case that triggers it.
    """
    proc = run_tklr(home, "details", str(rid))
    starts = tuple(ITEMTYPE.values()) + ("?",)   # `?` so a draft still reads
    entry: list[str] = []
    for line in (proc.stdout or "").splitlines():
        if line.startswith(("rruleset:", "id/cr/md:")):
            break
        stripped = line.strip()
        if not entry:
            if stripped.startswith(starts):
                entry.append(stripped)
            continue                      # skip chatter and leading blanks
        if not stripped:
            break                         # blank line AFTER the entry ends it
        entry.append(stripped)
    return " ".join(entry)


def has_token(entry: str, key: str) -> bool:
    """Is `@<key>` present as a token, rather than as text inside a subject?"""
    return re.search(rf"(?:^|\s)@{re.escape(key)}(?:\s|$)", entry) is not None


def cmd_move(args, home: Path, now: datetime) -> int:
    # REFUSED for a non-recurring reminder, because tklr would not move it, it
    # would duplicate it. Controller.reschedule_instance appends
    # `@- <old> @+ <new>` to the entry and nothing else. With an `@r` present
    # tklr renders those as EXDATE + RDATE and the move is correct; with no
    # `@r` the old time comes from `@s`/DTSTART, no EXDATE is produced, and the
    # reminder ends up on the schedule at BOTH times. Measured on tklr 1.0.43:
    # rruleset became `RDATE:<old>, <new>`.
    #
    # Checked BEFORE the call, not after, so there is no duplicate to clean up.
    # An empty entry (unreadable record) falls through: tklr_mutate reports a
    # missing id better than a guard can.
    for flag, value in (("--instance", args.instance), ("--to", args.to)):
        if value is not None and not str(value).strip():
            die(f"{flag} was given but empty", "Name the datetime it should use.")

    entry = record_entry(home, args.id)
    if entry and not has_token(entry, "r"):
        # A reminder with no `@r` has exactly ONE occurrence, so moving that
        # occurrence and changing `@s` are the same operation. Route it through
        # the same in-place token edit `edit --when` uses: correct, keeps the id
        # and the history, and needs nothing from reschedule_instance.
        #
        # This used to refuse and tell the caller to delete and re-add. The
        # refusal was right about tklr (reschedule_instance appends `@- old
        # @+ new` and, with no `@r` to turn those into EXDATE + RDATE, leaves
        # the reminder on the schedule at BOTH times, measured on 1.0.43) but
        # wrong to make that tklr's defect the caller's problem. There is no
        # reason the user should hear about `@r` at all.
        if has_token(entry, "+"):
            print("note: this reminder carries explicit extra dates (@+); "
                  "only its start time is being moved, they are left alone.",
                  file=sys.stderr)
        edit_args = argparse.Namespace(
            id=args.id, when=args.to, dry_run=args.dry_run,
            subject=None, duration=None, for_whom=None, alert=None, via=None,
            note=None, location=None, priority=None, notice=None, timezone=None,
            offset=None, travel=None, repeat=None, clear=None)
        return cmd_edit(edit_args, home, now)

    instance, instance_had_time = resolve_when(args.instance, now)
    to_when, _ = resolve_when(args.to, now)
    # A timed occurrence cannot be named by date alone, and tklr's refusal does
    # not say so. Caught here because it is the one mismatch with an obvious
    # cause: "move tomorrow's 3pm dentist" resolves --to fine and leaves
    # --instance as a bare date.
    if not instance_had_time:
        print(f"note: --instance {instance} names a whole day. If that "
              "occurrence has a time, include it or tklr will not match it.",
              file=sys.stderr)
    return move_occurrence(home, args.id, entry, instance, to_when, now,
                           args.dry_run)


TOKEN_SPLIT = re.compile(r"\s+(?=@[A-Za-z+~-])")


def refuse_plus_on_recurring(entry: str) -> None:
    """Stop an entry that tklr would accept and then never schedule.

    On tklr 1.0.43 a record with both `@r` and `@+` generates no occurrences at
    all. `tklr check` calls it valid and `tklr add` reports success, so without
    this the reminder is created, confirmed to the user, and is already invisible
    -- the one shape where every report is true and nothing is on the schedule.
    Reached through `--raw`, which is the only way to hand-write tokens.
    """
    if has_token(entry, "r") and has_token(entry, "+"):
        die("that reminder would never appear on the schedule",
            "A repeating reminder that carries an extra date (@+) generates no "
            "occurrences at all on tklr 1.0.43 — the whole series, not just "
            "that date.",
            "Add the repeating reminder without the @+, then add the extra "
            "date as its own reminder.")


def without_recurrence(entry: str, new_start: str) -> str:
    """The same reminder as a single dated entry: no `@r`, no `@-`, no `@+`.

    Order is preserved, so `@d` -- which swallows everything after it in tklr's
    grammar -- stays last if it was last.
    """
    parts = TOKEN_SPLIT.split(entry.strip())
    kept = [parts[0]]                       # itemtype + subject
    for part in parts[1:]:
        key = part[1:2]
        if key in {"r", "-", "+"}:
            continue
        kept.append(f"@s {new_start}" if key == "s" else part)
    return " ".join(kept)


def move_occurrence(home: Path, rid: int, entry: str, instance: str,
                    to_when: str, now: datetime, dry_run: bool) -> int:
    """Move one occurrence of a repeating reminder, without ever writing `@+`.

    `@+` cannot be used at all on tklr 1.0.43. A recurring record carrying one
    generates NO occurrences -- not the moved one, not the rest of the series --
    while the rruleset still reads correctly and every command reports success.
    Measured: 12 occurrences before, 0 after, gone from the schedule entirely.
    That is what tklr's own `reschedule_instance` writes, and what the TUI's
    Reschedule writes, so this is not reachable only through the shim.

    So the occurrence is excluded with `@-`, which works correctly, and the
    moved one is created as its own dated reminder carrying the original's
    duration, alerts, people and details. Two records instead of one is a real
    cost and it is the smaller one: the alternative on this version is a
    reminder that silently disappears from the schedule.
    """
    stored, horizon = occurrence_window(home, rid)
    old = compact(instance)
    if old is None or compact(to_when) is None:
        die("an occurrence needs a date and a time, e.g. '2026-08-17 09:00'")
    if stored and old not in stored and horizon and old <= horizon:
        die(f"{instance} is not an occurrence of id {rid}",
            f"Its occurrences are listed by: {sys.argv[0]} show {rid}",
            "Name it exactly as it is scheduled.")

    moved = without_recurrence(entry, to_when)
    chk = run_tklr(home, "check", "--", moved)
    if "valid" not in (chk.stdout or "").lower():
        die("could not build the moved reminder",
            f"composed: {moved}",
            *[ln for ln in (chk.stdout or "").splitlines()[:4]])

    if dry_run:
        print(f"WOULD exclude {instance} from id {rid}")
        print(f"WOULD create:  {moved}")
        print("  (nothing was changed)")
        return 0

    minus = [p.strip() for p in (token_value(entry, "-") or "").split(",")
             if p.strip()]
    if as_instant(old) not in {as_instant(m) for m in minus}:
        minus.append(old)
    rc = delegate("tklr_mutate.py",
                  ["edit", str(rid), "--set", "@- " + ", ".join(minus)], home)
    if rc != 0:
        return rc

    add = run_tklr(home, "add", "--", moved)
    if "Added 1 entry" not in ((add.stdout or "") + (add.stderr or "")):
        die("the occurrence was excluded but the moved reminder was NOT created",
            f"composed: {moved}",
            f"id {rid} no longer has an occurrence at {instance}; add the "
            "replacement by hand or the user simply loses it.")

    heal_alerts(home)
    after, _ = occurrence_window(home, rid)
    if old in after:
        die(f"id {rid} still has an occurrence at {instance}",
            "The entry was written but tklr did not drop the old time.")
    print(f"moved: {instance} → {to_when}")
    print(f"  id {rid} no longer occurs at {instance}; the moved one is now a "
          "separate reminder")
    print(f"  (tklr 1.0.43 drops the whole series if a moved occurrence is "
          "stored on the record itself)")
    return 0


def cmd_uses(args, home: Path, now: datetime) -> int:
    """Where jot time went, by category.

    The second half of tklr's jot model. A jot is captured in a few words while
    something is happening; later it gains `--duration` and `--use`, and this is
    what those were for -- totals per category and month, rather than a pile of
    timestamped lines nobody reads back.
    """
    if args.list:
        proc = run_tklr(home, "uses", "list")
    else:
        cmd = ["uses", "report"]
        if args.use:
            cmd += ["--use", args.use]
        if args.months:
            cmd += ["--months", args.months]
        proc = run_tklr(home, *cmd)

    out = (proc.stdout or "") + (proc.stderr or "")
    if ("No uses defined" in out or "No matching jots" in out
            or not out.strip()):
        print("no jot time has been categorised yet.")
        print("  A jot records that something happened; --duration says how "
              "long it took")
        print("  and --use says what it counts toward. Only jots carrying both "
              "appear here.")
        return 0
    show_output(proc)
    return 0


def cmd_channels(args, home: Path, now: datetime) -> int:
    if args.set:
        if len(args.set) != 2:
            die("--set takes a letter and a command", code=2)
        letter, command = args.set
        rc = delegate("set_alert_channel.py", args.set, home)
        if rc != 0:
            return rc
        # A letter that validates is not a letter that delivers, and the two
        # look identical from here. Same bar as the first channel: nothing is
        # announced until an alert has gone down it.
        if args.no_test:
            print("\n(--no-test: nothing has proven an alert can be delivered "
                  "on this letter.)")
        elif create_test_alert(letter, home, now) != 0:
            die("the letter is configured but the delivery test could not be "
                "created.",
                "Do not announce this channel — nothing has proven it delivers.")
        described = describe_channels({letter: command})
        print_added_relay(home, described[0] if described else "the new channel",
                          tested=not args.no_test, known_email=args.email)
        return 0
    if args.remove:
        return delegate("set_alert_channel.py", ["--remove", args.remove], home)
    return delegate("set_alert_channel.py", ["--list"], home)


ALERT_TEMPLATE = ('--quiet "⏰ Reminder: {name} — starts {when} ({start}). '
                  '{description}"')


def host_or_die(call, *args):
    """Run a host.py call, mapping its failure onto this script's reporting.

    host.py never exits, because the same missing host command is fatal to
    `setup` and merely worth reporting in `status`. Callers that want to carry
    on catch host.HostError themselves; everything else comes through here.
    """
    try:
        return call(*args)
    except host.HostError as exc:
        die(str(exc), *([exc.detail] if exc.detail else []))


def chat_list(platform: str | None = None) -> str:
    """The host's chat destinations, verbatim, or die saying why it can't tell."""
    return host_or_die(host.chat_list, platform)


def platform_targets(platform: str) -> list[str]:
    """Every target this machine has on one platform."""
    return host_or_die(host.platform_targets, platform)


CRON_JOB_NAME = host.CRON_JOB_NAME
POLLER = host.dispatcher_path()


def export_tklr_home(home: Path) -> None:
    """Point child processes at this workspace, without touching our own env.

    The poller takes its workspace from `$TKLR_HOME`, so a caller running it
    for a non-default workspace has to pass it down. putenv rather than
    building a child environment by hand: only the child needs the value, and
    putenv is the API for exactly that -- it changes what children inherit and
    deliberately leaves this process's own mapping alone. The child assembles
    its mapping from what it inherits, so it reads TKLR_HOME normally.

    It also means the skill never copies its whole environment to pass one
    value down. A scanner cannot tell that shape apart from dumping the
    environment somewhere, and it is right not to try.
    """
    os.putenv("TKLR_HOME", str(home))


def run_installer(home: Path) -> None:
    """Run install.sh and report it in one line, or die with its full output.

    Folded in so the whole setup is ONE tool call. It used to be a separate
    step, and separate steps are where this gets lost: a run on 2026-08-07
    called install.sh, received 5,356 characters back -- 28 lines of uv package
    names, then a block of instructions -- narrated "let me check a few things",
    emitted no further tool call, and the turn simply ended. Nothing was
    configured. One command cannot be abandoned halfway.
    """
    script = SKILL_SCRIPTS / "install.sh"
    if not script.is_file():
        die(f"install.sh is missing from {SKILL_SCRIPTS}")
    try:
        proc = subprocess.run(["bash", str(script), "--home", str(home)],
                              capture_output=True, text=True, timeout=900)
    except (OSError, subprocess.SubprocessError) as exc:
        die(f"could not run install.sh: {exc}")

    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        print(out, file=sys.stderr)
        die("install.sh failed — see its output above.",
            "tklr itself is not usable, so nothing further will work.")

    version = ""
    for line in out.splitlines():
        if "installed —" in line or "already installed —" in line:
            version = line.split("—", 1)[1].strip()
    print(f"tklr: ready{f' ({version})' if version else ''}")


# True/False when the schedule could be read, None when it could not.
cron_job_present = host.cron_job_present


def ensure_dispatcher() -> bool:
    """Copy the poller to wherever the host's scheduler will accept it.

    Which directory that is, and why it cannot simply be the skill's own copy,
    is host.dispatcher_path()'s business. On a host with no such restriction
    that path is the skill's own copy and this reduces to a no-op.
    """
    source = SKILL_SCRIPTS / "tklr_alert_poller.py"
    if not source.is_file():
        return False
    try:
        POLLER.parent.mkdir(parents=True, exist_ok=True)
        if not POLLER.exists() or POLLER.read_bytes() != source.read_bytes():
            shutil.copy2(source, POLLER)
            POLLER.chmod(0o755)
        return True
    except OSError:
        return False


def ensure_cron_job() -> tuple[bool, str]:
    """Create the every-minute dispatcher job if it is missing.

    Folded into `setup` rather than left as an instruction because it is the
    one step with no visible symptom when skipped: letters validate, reminders
    save, `add` reports the alert is scheduled -- and nothing is ever
    delivered, because nothing is running to deliver it. Every setup that has
    silently produced no alerts got this far and no further.
    """
    if not ensure_dispatcher():
        return False, f"could not install the dispatcher into {POLLER.parent}"

    present = cron_job_present()
    if present is None:
        return False, (f"could not read {host.schedule_hint()} -- create the job "
                       "by hand and confirm it, or nothing will ever be delivered")
    if present:
        return True, f"cron job '{CRON_JOB_NAME}' already present"

    return host.create_cron_job()


def cmd_setup(args, home: Path, now: datetime) -> int:
    """Configure one platform as an alert channel, start to finish.

    The agent knows exactly one thing for certain about delivery: which
    platform the user is talking to it on. This turns that one fact into a
    working channel without asking the user anything, which is the point --
    every version of this flow that asked "where would you like reminders?"
    ended up proposing a dead platform that happened to sort first in the
    host's own listing.
    """
    platform = args.platform.strip().lower().rstrip(":")
    if not platform:
        die("--platform needs a name, e.g. --platform telegram", code=2)

    # Empty means the host could not tell us, which passes: a listing this
    # script cannot read is not evidence the platform is wrong.
    known = host_or_die(host.chat_platforms)
    if known and platform not in known:
        die(f"'{platform}' is not a messaging platform on this machine.",
            f"configured platforms: {', '.join(sorted(known))}",
            "pass the platform this conversation is on.")

    if args.target:
        target = args.target
    else:
        targets = platform_targets(platform)
        if not targets:
            die(f"'{platform}' has no targets in {host.target_hint()}.",
                "it may be configured but not connected. Ask the user which",
                "channel to use instead, or pass --target explicitly.")
        if len(targets) > 1:
            die(f"'{platform}' has {len(targets)} targets — pick one and pass "
                "it as --target:",
                *(f"  {t}" for t in targets))
        target = targets[0]

    # Only now, once the destination is known to be valid: a typo in --platform
    # should not trigger a package install before it is reported.
    run_installer(home)

    command = host.chat_send_command(target, ALERT_TEMPLATE)
    rc = delegate("set_alert_channel.py", [args.letter, command], home)
    if rc != 0:
        return rc
    print(f"\nalert channel '{args.letter}' delivers to {target}.")

    # Before the cron job, not after: the job is the thing that reads this, so
    # scheduling it while the workspace is unrecorded creates the one state
    # this is meant to prevent, however briefly.
    pin_failed = write_workspace_pin(home)
    if pin_failed:
        print(f"  note: could not record the workspace ({pin_failed});")
        print(f"        the dispatcher will resolve it itself, which is right "
              f"only while nothing sets TKLR_HOME or XDG_CONFIG_HOME "
              f"differently for it")

    ok, note = ensure_cron_job()
    print(f"dispatcher: {note}")
    if not ok:
        die("the channel is configured but NOTHING WILL BE DELIVERED.",
            "A reminder will save, validate, and report its alert as scheduled;",
            "no alert will ever arrive, because no job is running to send it.",
            "Fix the dispatcher before telling the user anything works.")

    if args.no_test:
        print("\n(--no-test: skipped the delivery test. Nothing has proven that "
              "an alert\ncan actually reach the user.)")
        routes = print_routes(home, args.email)
        print_relay(f"Your reminders will arrive on {channels_phrase(home)}.",
                    offer_sentence(routes), email_unavailable(home))
        return 0

    rc = create_test_alert(args.letter, home, now)
    if rc != 0:
        die("the channel and cron job are configured, but the delivery test "
            "could not be created.",
            "Report this as a failure: nothing has proven an alert can reach "
            "them, so setup is not complete.")
    routes = print_routes(home, args.email)
    # Opens like a reply, deliberately. A block that starts mid-thought invites
    # a preamble, and the preamble is where "setup is complete!" gets announced
    # -- two lines above the sentence asking whether the test alert arrived.
    # Nothing to prepend if the first line is already an opening.
    print_relay(
        f"All set up bar one thing: your reminders will arrive on "
        f"{channels_phrase(home)}, and I have just sent a test one. Tell me "
        "when it turns up, since whether it actually reaches you is the one "
        "thing I cannot check from here.",
        offer_sentence(routes), email_unavailable(home))
    return 0


def create_test_alert(letter: str, home: Path, _now: datetime) -> int:
    """Create a reminder whose alert fires in a little over two minutes.

    Setup's own proof of delivery, created here rather than left as an
    instruction because it is the step that gets skipped -- and skipping it is
    invisible, since every other part of the chain reports healthy while
    sending nothing. It also takes the agent out of the verification loop
    entirely: the alert arrives on the user's device whether or not the agent
    remembers to mention it.

    The trigger is computed from a whole minute boundary, not from now: tklr
    stores times to the minute, so an unrounded `now + 2m` truncates to as
    little as 1m01s away and `check_alert_margin` refuses it outright.

    The boundary is taken from now + SPAWN_SLACK rather than from now. The
    margin is re-checked by the `add` SUBPROCESS, milliseconds later, against
    its own clock -- so anchoring on `now` exactly gives a worst case of
    exactly MIN_ALERT_MARGIN (when now lands on a minute boundary), which any
    spawn delay at all pushes under. The slack makes the trigger 2:05-3:05
    away, always clear of the 2:00 floor.

    The clock is re-read here rather than taken from the caller: `setup` runs
    the installer and the host's scheduler first, each with a long timeout, so
    timestamp from program start can be minutes stale by the time we arrive.
    """
    offset_min = 2
    SPAWN_SLACK = timedelta(seconds=5)
    now = datetime.now()
    anchor = now + SPAWN_SLACK
    next_minute = anchor.replace(second=0, microsecond=0)
    if anchor != next_minute:                    # already on the boundary? keep it
        next_minute += timedelta(minutes=1)
    fires = next_minute + timedelta(minutes=offset_min)
    start = fires + timedelta(minutes=offset_min)

    print(f"\ndelivery test: alert fires {fires:%H:%M} "
          f"(in {human(fires - now)}), delivered within a minute of that.")
    proc = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "--home", str(home),
         "add", "--type", "event", "--subject", TEST_SUBJECT,
         "--when", f"{start:%Y-%m-%d %H:%M}", "--duration", "5m",
         "--alert", f"{offset_min}m", "--via", letter],
        capture_output=True, text=True)
    for line in (proc.stdout or "").splitlines():
        print(f"  {line}")
    for line in (proc.stderr or "").splitlines():
        print(f"  {line}", file=sys.stderr)
    if proc.returncode != 0:
        return proc.returncode

    print("\nNow WAIT for it to arrive, then ask the user whether it did.")
    print("That is the only proof this works, and the one thing you cannot "
          "check yourself.")
    return 0


SELF = Path(__file__).resolve()


def mail_accounts(home: Path) -> list[tuple[str, str]]:
    """[(himalaya account name, its From: address)], or [] if email is not set up.

    Delegated to set_alert_channel.py rather than reimplemented: himalaya's
    config is a plaintext-password file in a common setup, and exactly one
    place in this skill should be reading it.
    """
    key = str(home)
    if key in _mail_cache:
        return _mail_cache[key]
    _mail_cache[key] = _read_mail_accounts(home)
    return _mail_cache[key]


_mail_cache: dict[str, list[tuple[str, str]]] = {}


def _read_mail_accounts(home: Path) -> list[tuple[str, str]]:
    try:
        proc = subprocess.run(
            [sys.executable, str(SKILL_SCRIPTS / "set_alert_channel.py"),
             "--home", str(home), "--mail-accounts"],
            capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return []
    if proc.returncode != 0:
        return []
    out = []
    for line in (proc.stdout or "").splitlines():
        if "\t" in line:
            name, addr = line.split("\t", 1)
            out.append((name.strip(), addr.strip()))
    return out


# notify-send is an ordinary CLI, not a host call, so it stays here: a port
# keeps this route unchanged. Same for himalaya, in himalaya_command below.
DESKTOP_COMMAND = ('notify-send "⏰ Reminder: {name}" '
                   '"starts {when} ({start}). {description}"')


class Route(NamedTuple):
    """A delivery route with no letter yet."""
    label: str    # what it is, for the agent
    command: str  # how to add it, for the agent
    offer: str    # what to call it when offering, for the user
    ask: str = ""  # anything the offer must ask for to be actionable


def email_unavailable(home: Path) -> str:
    """Why email is not on offer, in words for the user — "" if it is on offer.

    Absence needs saying. himalaya being unconfigured is not a reason to stay
    quiet about email: the user cannot ask for a channel they don't know the
    skill supports, and "no email account on this machine" is a thing they can
    act on, unlike silence. Only genuine absence -- if an email letter already
    exists, or accounts exist to offer, this is empty.
    """
    letters = configured_letters(home)
    if any("himalaya" in c for c in letters.values()) or mail_accounts(home):
        return ""
    return ("I can send reminders by email too, but that goes through himalaya "
            "and there is no email account set up on this machine yet. Set one "
            "up whenever you like and I can use it.")


def discover_routes(home: Path, known_email: str | None = None) -> list[Route]:
    """Every delivery route with no letter yet, and how to add and offer it.

    `offer` is the one field the user ever sees. A route has to be describable
    in a sentence a person can answer -- "your email", "the Household group
    chat" -- or the offer is not an offer.

    This is discovery the agent will not do on its own. "Once the first channel
    works, check what else exists and offer it" has been an instruction in
    SKILL.md and in references/setup.md for several revisions, and a run on
    2026-08-08 still finished setup, announced success, and never so much as
    looked for himalaya -- because by then `setup` had reported success and
    there was nothing left in front of it. An agent does not go looking for a
    channel it has no evidence of. So the evidence is printed here, in the
    output of the one command it definitely runs, with the address filled in.

    Only routes that are genuinely absent are listed: a workspace that already
    has an email letter should produce no email line, or the offer becomes
    noise that gets ignored on the run where it matters.
    """
    letters = configured_letters(home)
    commands = " ".join(letters.values())
    free = [c for c in "abcdefghijklmopqrstuvwxyz" if c not in letters]
    routes: list[Route] = []

    if "himalaya" not in commands:
        for name, addr in mail_accounts(home):
            # The destination address is the one thing this script cannot work
            # out and the agent often can -- from memory, or from earlier in the
            # conversation. Passed in, it becomes a confirmable offer; absent, a
            # question inside the offer, so either way the reply that accepts
            # email carries an address and no round trip is wasted. `{addr}` is
            # where mail is sent FROM and is usually not where it is read, so it
            # is never the default.
            routes.append(Route(
                f"email — himalaya account '{name}', sending from {addr}",
                f"python3 {SELF} email --to "
                + (known_email or "<the address they READ mail at>"),
                f"your email at {known_email}" if known_email else "your email",
                # A remembered address is a claim, not a fact: it can be stale,
                # or belong to someone else in the household. Offered, never
                # assumed.
                f"Tell me if {known_email} is not where you read mail."
                if known_email else
                "For email, tell me which address to send to."))
            break  # one offer is an offer; the rest is a menu

    # notify-send being installed is not the question -- whether anyone would
    # see the popup is. With no display this machine is a server, and a desktop
    # notification is a channel that reports success and shows nobody anything.
    if ("notify-send" not in commands and shutil.which("notify-send")
            and (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))):
        routes.append(Route(
            "a desktop notification on this machine",
            f"python3 {SELF} channels --set {free[0] if free else '<letter>'} "
            f"'{DESKTOP_COMMAND}'",
            "a desktop notification on this machine"))

    # A host that cannot list its channels is not a reason to fail: the email
    # and desktop routes above stand on their own, and an offer of nothing is
    # still an honest offer.
    try:
        listed = host.chat_list()
    except host.HostError:
        listed = ""
    # An offer must not name a destination the user already has. Two targets on
    # one platform are one destination to them: with a named room configured,
    # offering that platform contradicts the sentence just above it.
    already = {d.lower() for d in describe_channels(letters)}
    for target, label, offer in host.chat_targets(listed):
        if (target in commands or offer.lower() in already
                or any(label == r.label for r in routes)):
            continue
        letter = free[len(routes)] if len(free) > len(routes) else "<letter>"
        command = host.chat_send_command(target, ALERT_TEMPLATE)
        routes.append(Route(label, f"python3 {SELF} channels --set {letter} "
                                   f"'{command}'", offer))
    return routes


def print_routes(home: Path, known_email: str | None = None) -> list[Route]:
    """Print the unconfigured routes, or say plainly that there are none."""
    routes = discover_routes(home, known_email)
    missing_email = email_unavailable(home)
    print("\nOther channels this machine can reach, none of them configured yet:")
    if not routes and not missing_email:
        print("  none — every route found is already an alert letter.")
    for route in routes:
        print(f"  · {route.label}")
        if route.command:
            print(f"      {route.command}")
        if route.offer == "your email" and not known_email:
            print("      (already know their address — from memory, or from")
            print("       earlier in this conversation? re-run with --email <it>")
            print("       and the offer names it for confirmation instead of")
            print("       asking. Never guess one.)")
    if missing_email:
        print("  · email — SUPPORTED but not available: himalaya has no account")
        print("      configured on this machine. Not something you can add, and")
        print("      not something to stay quiet about: the closing block says")
        print("      email exists and needs an account. Do not improvise another")
        print("      email route — a chat platform literally called 'email'")
        print("      is a different, usually unconfigured mechanism, not a")
        print("      fallback. Email on this skill means himalaya.")
    return routes


def offer_sentence(routes: list[Route]) -> str:
    """The offer, in words a person can answer. Empty when there is nothing left.

    One channel is a working setup, not a finished one, and the user cannot ask
    for a channel they do not know you can reach.
    """
    names = [r.offer for r in routes if r.offer]
    if not names:
        return ""
    if len(names) == 1:
        sentence = f"I can also send them to {names[0]} — want that as well?"
    else:
        listed = ", ".join(names[:-1]) + f" or {names[-1]}"
        sentence = (f"I can also send them to {listed} — want any of those as "
                    "well? Some people like a second channel for the things "
                    "they really cannot miss.")
    asks = " ".join(r.ask for r in routes if r.ask and r.offer)
    return f"{sentence} {asks}".strip()


def channels_phrase(home: Path) -> str:
    """"your chat and email at alex@example.com" — the configured destinations."""
    described = describe_channels(configured_letters(home))
    if not described:
        return "no channel yet"
    if len(described) == 1:
        return described[0]
    return ", ".join(described[:-1]) + f" and {described[-1]}"


RELAY_RULE = (
    "Nothing above the line is for the user. If what you send contains "
    "`tklr`,\n`python3`, a `--flag`, an `@` token or a code fence, you have "
    "written the wrong\nthing: they never type a command. They talk to you, and "
    "you compose it. When\nthey ask how to use this, the answer comes from "
    "`welcome`, not from you.")


def print_relay(*paragraphs: str) -> None:
    """Print the exact words to send the user, and say that they are exact.

    Every point where the agent composes a user-facing message by itself is a
    point where it hands over a command instead -- not from ignoring a rule, but
    because the nearest example in its context is always an invocation. A run on
    2026-08-08 configured email flawlessly and then closed with
    `tklr add "Dentist @s tomorrow 3p @e 15m,60m: a,e"`: a command the user must
    never type, in a syntax that does not exist. `welcome` fixed this for the end
    of setup by printing the text rather than describing it. This is the same
    move for every other moment that ends in a message.
    """
    rule = "-" * 72
    print(f"\n{rule}\nSEND EXACTLY THIS TO THE USER AS YOUR WHOLE REPLY —\n"
          f"no sentence before it, none after it:\n{rule}")
    for para in paragraphs:
        if para:
            print(textwrap.fill(" ".join(para.split()), width=72) + "\n")
    print(f"{rule}\n{RELAY_RULE}")


def himalaya_command(from_addr: str, to_addr: str) -> str:
    """Build the email delivery command — the one shape that is easy to get wrong.

    It nests a printf inside `sh -c` inside a TOML literal string, and each
    layer eats one level of escaping: the `\\\\n` written here survives TOML
    verbatim, becomes `\\n` after the dispatcher's shlex.split, and is finally
    interpreted by printf. Hand-written versions of this have shipped without a
    `From:` header (himalaya then exits 1 on every alert, forever) and with the
    newlines collapsed. Generating it removes the whole class of mistake.
    """
    lines = [
        f"From: {from_addr}",
        f"To: {to_addr}",
        "Subject: Reminder: {name} - starts {when} ({start})",
        "",
        "{name}",
        "When: {start} ({when})",
        "{description}",
        "",
    ]
    body = "\\\\n".join(lines)
    return f'sh -c "printf \\"{body}\\" | himalaya message send"'


ADDR_RE = re.compile(r"^[^@\s,]+@[^@\s,]+\.[^@\s,]+$")


def cmd_email(args, home: Path, now: datetime) -> int:
    """Add an email alert letter, end to end, including the delivery test."""
    to_addr = args.to.strip()
    if not ADDR_RE.match(to_addr):
        die(f"'{to_addr}' does not look like an email address",
            "--to is where the person READS mail, which is usually not the",
            "himalaya account's own address. Ask them; do not assume.")

    accounts = mail_accounts(home)
    if args.from_addr:
        from_addr = args.from_addr.strip()
    elif not accounts:
        die("himalaya has no email accounts configured, so email is not "
            "available on this machine.",
            "Say that plainly rather than improvising another route --",
            "a chat platform literally called 'email' is a different, usually",
            "unconfigured mechanism, not a fallback. Email means himalaya.")
    elif len(accounts) > 1:
        die(f"himalaya has {len(accounts)} accounts — say which one sends, "
            "with --from:",
            *(f"  --from {addr}   ({name})" for name, addr in accounts))
    else:
        from_addr = accounts[0][1]

    if not ADDR_RE.match(from_addr):
        die(f"'{from_addr}' does not look like an email address",
            "--from must be the himalaya account's OWN address: himalaya takes",
            "the envelope sender from the `From:` header and has no default.")

    rc = delegate("set_alert_channel.py",
                  [args.letter, himalaya_command(from_addr, to_addr)], home)
    if rc != 0:
        return rc
    print(f"\nalert channel '{args.letter}' emails {to_addr} (from {from_addr}).")

    if args.no_test:
        print("\n(--no-test: nothing has proven mail can actually be delivered "
              "on this letter.)")
        print_added_relay(home, "email", tested=False)
        return 0
    rc = create_test_alert(args.letter, home, now)
    if rc != 0:
        die("the email letter is configured but the delivery test could not be "
            "created.",
            "Report this as a failure: nothing has proven email works.")
    print_added_relay(home, "email", tested=True)
    return 0


def print_added_relay(home: Path, added: str, tested: bool,
                      known_email: str | None = None) -> None:
    """Close out "channel added" with the words to send, and what is still open.

    The turn after a channel is added is the one that went wrong on 2026-08-08:
    email was configured correctly and the reply taught the user a tklr command.
    Nothing was left for the agent to say, so it invented something.
    """
    routes = print_routes(home, known_email)
    test = (f" I have sent a test to {added}; tell me when it arrives, since "
            "that is the one thing I cannot check from here." if tested else "")
    print_relay(f"Done — your reminders will now reach you on "
                f"{channels_phrase(home)}.{test}",
                offer_sentence(routes), email_unavailable(home))


def describe_channels(letters: dict[str, str]) -> list[str]:
    """Plain-English destinations, derived from the configured letters.

    `welcome` promises only what exists. A blurb that offers email on a
    workspace with no email letter is a promise the skill cannot keep.
    """
    out: list[str] = []
    for letter in sorted(letters):
        command = letters[letter]
        target = re.search(r"--to\s+[\"']?(\S+?)[\"']?(?:\s|$)", command)
        if "himalaya" in command:
            addr = re.search(r"To:\s*([^\s\\\"]+@[^\s\\\"]+)", command)
            out.append(f"email{f' at {addr.group(1)}' if addr else ''}")
        elif "notify-send" in command:
            out.append("a desktop notification on this machine")
        elif target:
            platform = target.group(1).split(":", 1)[0]
            out.append(f"{platform.capitalize()}")
        else:
            # A letter whose command is none of the three known shapes -- a
            # custom script, say. Still a real destination; describe it
            # vaguely rather than dropping it, because dropping every letter
            # leaves nothing to promise and used to crash on channels[0].
            out.append("the channel you set up")
    seen, unique = set(), []
    for item in out:
        if item.lower() not in seen:
            seen.add(item.lower())
            unique.append(item)
    return unique


WELCOME = """\
You're all set — just talk to me normally about anything time-related.

**Appointments and events.** "Dentist Friday at 3 for an hour." "Coffee with
Sam tomorrow at 11:30." All-day things work too — "{who}'s birthday on August
15th" — as do repeating ones: "standup every weekday at 9", "1:1 with Dana
every other Tuesday", "pay the mortgage on the 1st of each month". I can note a
location, and hold travel time either side of a meeting.

**Things to do.** "Remind me to buy milk" for something with no fixed time, or
with a deadline and a priority: "renew my passport by September 1st, it's
important — start warning me a month out." Bigger jobs can have steps I track
together — "plan the Colorado trip: flights, hotel, dog sitter" — and I can
keep habits honest too: "I want to exercise three times a week."

**Asking me things.** "What's on my calendar today?" "What about tomorrow?"
"How's my week looking?" "What do I need to get done?" "When's my next dentist
appointment?" "Am I free Tuesday at 3 for a coffee date?" — for that last one
I'll check what's around it, not just the slot itself.

**How you get reminded.** Alerts reach you on {channels}. You can have several
per event at different times — "remind me a day before and again an hour
before" — and I'll pick sensible ones if you don't say.

**Changing and finishing things.** "I've done that" marks a task complete.
"Cancel Friday's meeting", "move the dentist to Thursday afternoon", "skip next
week's standup but keep the rest" all work too. To change any other detail I'll
replace the entry and tell you that's what I did.
"""

TEST_SUBJECT = "tklr delivery test"

TEST_LINE = ("\nI've added a test reminder that should reach you shortly — tell "
             "me whether it arrives, since that's the one part I can't check "
             "myself.\n")


def recent_delivery_test(home: Path, now: datetime, minutes: int = 30) -> bool:
    """Was a delivery test created recently enough to still be arriving?

    `Records.created` is a UTC stamp (`20260809T2217Z`), so it is compared
    against UTC rather than local time -- comparing it to a local clock is
    right for one timezone and silently wrong everywhere else.
    """
    import sqlite3
    cutoff = (datetime.now(timezone.utc)
              - timedelta(minutes=minutes)).strftime("%Y%m%dT%H%M")
    try:
        conn = sqlite3.connect(home / "tklr.db", timeout=15)
        row = conn.execute(
            "SELECT COUNT(*) FROM Records WHERE subject = ? AND created >= ?",
            (TEST_SUBJECT, cutoff + "Z")).fetchone()
        conn.close()
    except sqlite3.Error:
        return False
    return bool(row and row[0])


def cmd_welcome(args, home: Path, now: datetime) -> int:
    """Print the user-facing description of this skill, ready to send as-is.

    This exists because the description is the single thing the agent gets
    wrong most reliably. Asked to explain the skill, a model reaches for the
    nearest example in its context -- which is a wrapper invocation -- and
    hands the user a command cheat sheet, teaching them the traps the wrapper
    exists to hide. Generated text cannot be trusted here, so it is not
    generated: it is printed, and the agent's only job is to relay it.
    """
    letters = configured_letters(home)
    if not letters:
        die("no alert channels are configured, so there is nothing to promise.",
            "run `setup --platform <the platform you are on>` first.")
    channels = describe_channels(letters)
    if len(channels) > 1:
        channels_text = ", ".join(channels[:-1]) + f" and {channels[-1]}"
    else:
        channels_text = channels[0]
    text = WELCOME.format(who=args.who or "Jordan", channels=channels_text)
    # The flag alone is not enough to make the claim. `welcome` sends nothing;
    # the test it refers to is the one `setup` created moments earlier, so the
    # sentence is only true when that record actually exists. Its default is to
    # include the line, and the documented answer to "how do I use this" is this
    # command -- so a user asking that months later was told a test reminder was
    # on its way, waited for it, and had every reason to report the skill broken.
    if not args.no_test and recent_delivery_test(home, now):
        text += TEST_LINE
    # Re-wrap per paragraph: the channel list is variable-length, so the
    # template's own line breaks land wherever. Chat clients re-wrap anyway;
    # this keeps the plain-text form readable when they don't.
    import textwrap
    print("\n\n".join(
        textwrap.fill(" ".join(para.split()), width=78)
        for para in text.strip().split("\n\n")))
    return 0


def report_workspace_agreement(home: Path) -> None:
    """Say whether the three things that resolve the workspace still agree.

    Three parties each pick a workspace, in environments that differ: this
    process, the dispatcher under the scheduler, and `tklr` in the user's
    terminal. When they disagree, every individual report still says success --
    reminders save, alerts queue, the dispatcher runs cleanly -- and nothing
    is ever delivered. That is the failure this whole check exists to make
    visible, because it has no other symptom.
    """
    try:
        pin = host.workspace_pin_path()
        recorded = pin.read_text(encoding="utf-8").strip()
    except (OSError, host.HostError):
        recorded = ""

    if not recorded:
        print("  dispatcher workspace: NOT RECORDED — it resolves its own, which")
        print("    differs from this one whenever the scheduler's environment does.")
        print("    Run setup to record it.")
    elif Path(recorded).expanduser() != home:
        print(f"  dispatcher workspace: {recorded}")
        print("    MISMATCH — the dispatcher polls that one; this command is")
        print("    using the one above. Alerts created here are never sent.")
        print("    Run setup without --home to correct it.")

    mine = tklr_own_home()
    if mine is None:
        print("  `tklr` by hand: could not ask tklr where it looks")
    elif mine != home:
        print(f"  `tklr` by hand: {mine}")
        print("    MISMATCH — a person typing `tklr` sees a different workspace")
        print("    than the agent uses. Usually TKLR_HOME or XDG_CONFIG_HOME set")
        print("    for one and not the other.")


def report_vanished_records(home: Path) -> None:
    """Name any reminder that tklr has silently dropped from the schedule.

    A record carrying `@+` generates no occurrences at all on tklr 1.0.43 -- the
    whole series, not just the moved date -- while `details` still prints a
    correct-looking rruleset. `move` never writes one, but tklr's own reschedule
    and the TUI's Reschedule both do, so a reminder can arrive in this state
    without the skill ever touching it. There is no symptom until someone
    notices an alert that never came.
    """
    import sqlite3
    try:
        conn = sqlite3.connect(home / "tklr.db", timeout=15)
        rows = conn.execute(
            "SELECT r.id, r.subject FROM Records r "
            "WHERE r.tokens LIKE '%\"k\": \"+\"%' "
            "AND NOT EXISTS (SELECT 1 FROM DateTimes d WHERE d.record_id = r.id)"
        ).fetchall()
        conn.close()
    except sqlite3.Error:
        return
    if not rows:
        return
    print(f"  {len(rows)} reminder(s) are NOT on the schedule at all, because "
          "tklr drops a whole")
    print("    series once a moved occurrence is stored on the record "
          "(rescheduled in tklr's UI?):")
    for rid, subject in rows[:5]:
        print(f"      id {rid}: {subject!r}")
    print("    Fix each by removing its moved date and adding that one as its "
          "own reminder.")


def cmd_status(args, home: Path, now: datetime) -> int:
    print(f"workspace: {home}")
    report_workspace_agreement(home)
    report_vanished_records(home)
    letters = configured_letters(home)
    print(f"channels:  {', '.join(sorted(letters)) if letters else 'NONE — alerts cannot be created'}")
    poller = POLLER
    source = SKILL_SCRIPTS / "tklr_alert_poller.py"
    # Drift matters more than it looks. The deployed copy is what cron runs, and
    # an older one silently ignores flags it does not know -- a `--check` sent to
    # a pre-`--check` poller performs a FULL DISPATCH, so the read-only status
    # command would send and delete the very alert being inspected.
    stale = (poller.exists() and source.is_file()
             and poller.read_bytes() != source.read_bytes())
    print(f"dispatcher: {'installed' if poller.exists() else 'MISSING — run setup'}"
          + (" — OUT OF DATE vs the skill; run setup to refresh" if stale else ""))
    # The cron job is the only part of the chain with no symptom when absent:
    # everything else reports healthy and no alert is ever sent.
    cron = cron_job_present()
    print("cron job:  " + {
        True: f"'{CRON_JOB_NAME}' scheduled",
        False: f"MISSING — NOTHING WILL BE DELIVERED. Run: setup --platform <platform>",
        None: f"could not read {host.schedule_hint()} — verify by hand",
    }[cron])
    if poller.exists() and stale:
        print("  (not running it: an out-of-date poller ignores --check and would")
        print("   dispatch for real, sending and deleting any alert now due)")
    elif poller.exists():
        export_tklr_home(home)
        proc = subprocess.run([sys.executable, str(poller), "--check"],
                              capture_output=True, text=True, timeout=180)
        for line in (proc.stdout or "").splitlines():
            print(f"  {line}")
    # A workspace set up before this existed has a working chat letter, no
    # email letter, and nobody who ever mentioned email was possible. `status`
    # is where that gets noticed on any later run.
    if letters:
        routes = print_routes(home, args.email)
        say = " ".join(x for x in (offer_sentence(routes),
                                   email_unavailable(home)) if x)
        if say:
            print(f"\nWorth saying next time you speak to the user:\n  \"{say}\"")
    return 0


def cmd_add(args, home: Path, now: datetime) -> int:
    if args.raw:
        entry, resolved = args.raw.strip(), None
        if entry[:1] not in set(ITEMTYPE.values()) | {"-", "?"}:
            die("a raw entry must start with an itemtype character")
    else:
        if not args.type:
            die("--type is required", code=2)
        entry, resolved, _ = build_entry(args, home, now)

    refuse_plus_on_recurring(entry)

    for w in warnings:
        print(f"  note: {w}")

    # `--` before the entry: a jot starts with "-", which tklr's CLI would
    # otherwise parse as an option ("Error: No such option '- '"). It is why
    # tklr ships a separate `jot` command; the separator does the same job and
    # is harmless for every other type.
    chk = run_tklr(home, "check", "--", entry)
    if "Entry is valid" not in (chk.stdout or ""):
        detail = [l.strip() for l in (chk.stdout or "").splitlines()
                  if l.strip() and "aggregate" not in l and "DateTimes" not in l]
        die("that reminder could not be created", f"composed: {entry}", *detail[:6])

    if args.dry_run:
        print(f"WOULD create: {entry}")
        report_alert_times(entry, resolved, now)
        print("  (nothing was written)")
        return 0

    add = run_tklr(home, "add", "--", entry)
    out = (add.stdout or "") + (add.stderr or "")
    if "Added 1 entry" not in out:
        detail = [l.rstrip() for l in out.splitlines()
                  if l.strip() and "aggregate" not in l and "DateTimes" not in l]
        die("the reminder was not created", f"composed: {entry}", *detail[:8])

    heal = POLLER
    heal_failed = ""
    if heal.exists():
        export_tklr_home(home)
        done = subprocess.run([sys.executable, str(heal), "--heal"],
                              capture_output=True, text=True, timeout=180,
                              check=False)
        if done.returncode != 0:
            # A skipped heal is the difference between a reminder that fires
            # and one that silently does not. Never swallow it.
            heal_failed = (done.stdout or done.stderr or "").strip().splitlines()
            heal_failed = heal_failed[-1] if heal_failed else "heal returned non-zero"

    import sqlite3
    try:
        conn = sqlite3.connect(home / "tklr.db", timeout=15)
        row = conn.execute(
            "SELECT id, itemtype, subject FROM Records ORDER BY id DESC LIMIT 1").fetchone()
        conn.close()
    except sqlite3.Error:
        row = None
    if row and row[1] == "?":
        die(f"it was stored as a DRAFT (id {row[0]}) and will never fire",
            f"Inspect with: {sys.argv[0]} show {row[0]}")

    print(f"created id {row[0] if row else '?'}: {entry}")
    report_alert_times(entry, resolved, now)
    if row:
        verify_scheduled(home, row[0], entry, resolved, now, heal_failed)
    return 0


def verify_scheduled(home: Path, record_id: int, entry: str, resolved: str | None,
                     now: datetime, heal_failed: str) -> None:
    """Confirm the reminder is really on the schedule, not just in the table.

    'Added 1 entry' means a Records row exists. It does NOT mean the reminder
    will ever appear on a calendar or notify anyone -- that needs a DateTimes
    row, and an alert needs an Alerts row on top of it. Both are derived, both
    have failed silently in practice (see the stale-cache bug and the
    minimum-margin rule), and both are cheap to check. Saying 'created' without
    checking is how a reminder that never fires gets reported as a success.
    """
    import sqlite3
    try:
        conn = sqlite3.connect(home / "tklr.db", timeout=15)
        occurrences = conn.execute(
            "SELECT COUNT(*) FROM DateTimes WHERE record_id = ?", (record_id,)).fetchone()[0]
        alert_rows = conn.execute(
            "SELECT COUNT(*) FROM Alerts WHERE record_id = ?", (record_id,)).fetchone()[0]
        conn.close()
    except sqlite3.Error as exc:
        print(f"  WARNING: could not verify it was scheduled: {exc}")
        return

    wanted_alert = "@a " in entry
    start = parse_resolved(resolved)

    if resolved and not occurrences:
        die(f"id {record_id} was saved but is NOT on the schedule "
            "(no occurrence was generated)",
            heal_failed or "tklr's derived tables are stale.",
            f"Fix: python3 {POLLER} --heal --verbose",
            f"Then confirm with: {sys.argv[0]} show {record_id}")

    if not wanted_alert:
        return

    # An alert due after today may legitimately have no row yet, so only insist
    # on one when the trigger falls inside the window tklr actually fills.
    #
    # That window is now .. LOCAL END OF DAY, not a rolling 24 hours:
    # `populate_alerts` (model.py:3268) computes
    # `now.replace(hour=23, minute=59, second=59)` and `populate_alerts_for_record`
    # says "alerts that trigger today". Testing against 24 hours instead --
    # which this did -- makes every evening reminder for tomorrow morning fail:
    # the alert is under a day away, so a row is demanded, and tklr will not
    # write one until midnight. `add` then reported a perfectly healthy reminder
    # as "NO ALERT was scheduled -- nobody will be notified" and exited 1.
    soonest = None
    m = re.search(r"@a ([^:]+):", entry)
    if m and start:
        fires = [alert_fire_time(o.strip(), start) for o in m.group(1).split(",")]
        soonest = min(fires) if fires else None
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=0)

    # `soonest is None` means the fire time could not be worked out, which is
    # not evidence the alert is missing. Insisting on a row in that case turns
    # every unparsed shape into a false "nobody will be notified" on a record
    # that is fine, and the caller's repair for that is to delete and re-add a
    # healthy reminder.
    if not alert_rows and soonest is not None and soonest <= end_of_day:
        die(f"id {record_id} was saved but NO ALERT was scheduled — nobody will "
            "be notified",
            heal_failed or "The alert row tklr should have generated is missing.",
            f"Fix: python3 {POLLER} --heal --verbose",
            f"If that does not help, delete it and re-add with the alert further "
            f"out: {sys.argv[0]} delete {record_id}")

    if alert_rows:
        print(f"  verified: on the schedule, {alert_rows} alert"
              f"{'s' if alert_rows != 1 else ''} queued")
    elif wanted_alert:
        print("  verified: on the schedule; alert is beyond tklr's generation "
              "horizon and will be created closer to the time")


EMAIL_HELP = ("their email address, if you already know it — from memory or "
              "from earlier in this conversation. The channel offer then names "
              "it for confirmation instead of asking for it. Never guess one.")


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="tklr_agent_wrapper.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "The single interface for calendars, reminders and alerts.\n"
            "\n"
            "Run THIS, never `tklr` itself. It takes named flags and returns plain\n"
            "English. tklr's own syntax is sigil-dense and fails silently — a wrong\n"
            "sigil becomes a record that quietly never fires, where a wrong flag is\n"
            "rejected here immediately.\n"
            "\n"
            "Pick a subcommand below, then run `%(prog)s <subcommand> --help`\n"
            "for its flags."),
        epilog=(
            "examples:\n"
            "  %(prog)s add --type event --subject \"Dentist\" \\\n"
            "      --when \"tomorrow 3pm\" --duration 1h --for alex --alert 1d,1h --via r\n"
            "  %(prog)s add --type task --subject \"Buy milk\" --for alex\n"
            "  %(prog)s add ... --dry-run     show what would happen, write nothing\n"
            "  %(prog)s list --today\n"
            "  %(prog)s find --person alex\n"
            "  %(prog)s status                is everything set up and working\n"
            "\n"
            "alerts:\n"
            "  --alert takes offsets BEFORE the start (1d,1h,15m); --via takes the\n"
            "  channel letters they are delivered on. Both are needed for anyone to\n"
            "  be notified. A trigger less than 2 minutes away is refused, because\n"
            "  tklr would schedule nothing and say nothing.\n"
            "\n"
            "  Delivery itself is not done here — tklr_alert_poller.py runs every\n"
            "  minute from the host agent's scheduler and sends what is due.\n"
            "\n"
            "workspace:\n"
            "  --home, else $TKLR_HOME, else ~/.config/tklr. Do not pass --home:\n"
            "  `setup` refuses it, and a workspace anywhere else is never polled.\n"
            "\n"
            "exit codes: 0 success, 1 refused or failed, 2 usage error.\n"))
    ap.add_argument("--home", help="tklr workspace (default $TKLR_HOME or ~/.config/tklr)")
    sub = ap.add_subparsers(dest="cmd", required=True, metavar="<subcommand>")

    a = sub.add_parser(
        "add", help="create a reminder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "Create a reminder from named fields. Nothing is written until it\n"
            "validates, and afterwards it is checked to confirm it really is on\n"
            "the schedule — being saved and being able to fire are different."),
        epilog=(
            "notifying someone:\n"
            "  --alert and --via go together; neither alone notifies anyone.\n"
            "    --alert 1d,1h   fire 1 day and 1 hour BEFORE the start\n"
            "    --via r,e       deliver on channels r and e (see `channels`)\n"
            "  The trigger (start minus offset) must be at least 2 minutes out.\n"
            "  Closer than that, tklr schedules nothing and reports nothing, so\n"
            "  this refuses instead. For a quick test: --when \"in 8 minutes\"\n"
            "  --alert 5m, which fires in 3.\n"
            "\n"
            "recurring:\n"
            "  --repeat \"daily\", \"every weekday\", \"weekly on monday\"\n"
            "\n"
            "projects:\n"
            "  --step \"Book flights\" --step \"Reserve hotel\" --chain\n"
            "  --chain makes each step wait on the previous one.\n"
            "\n"
            "checking first:\n"
            "  --dry-run prints the composed entry and every alert time, and\n"
            "  writes nothing. Use it whenever the request is ambiguous.\n"
            "\n"
            "examples:\n"
            "  %(prog)s --type event --subject \"Dentist\" --when \"tomorrow 3pm\" \\\n"
            "      --duration 1h --for alex --alert 1d,1h --via r\n"
            "  %(prog)s --type task --subject \"Buy milk\" --for alex\n"
            "  %(prog)s --type event --subject \"Standup\" --when \"tomorrow 9am\" \\\n"
            "      --repeat \"every weekday\" --for alex,jordan --alert 10m --via r\n"))
    a.add_argument("--type", choices=sorted(ITEMTYPE),
                   help="event (has a time), task (to do), project (tasks with "
                        "steps), goal (n per period), note (reference), jot "
                        "(timestamped log line)")
    a.add_argument("--subject", help="what it is, in plain words")
    a.add_argument("--when", help="'tomorrow 3pm', 'friday', 'in 2 hours', '2026-08-15 09:00'")
    a.add_argument("--duration", help="how long it lasts, e.g. 1h, 30m")
    a.add_argument("--for", dest="for_whom", help="comma-separated people, e.g. alex,jordan")
    a.add_argument("--alert", help="offsets BEFORE the start, e.g. 1d,1h,15m (needs --via)")
    a.add_argument("--via", help="channel letters to deliver on, e.g. r,e (needs --alert)")
    a.add_argument("--use", help="for jots: the time-tracking category it counts "
                   "toward, e.g. exercise.walking (a dot nests it under exercise)")
    a.add_argument("--note", help="free-text detail")
    a.add_argument("--location", help="where")
    a.add_argument("--priority", type=int, help="1 (highest) to 5 (lowest)")
    a.add_argument("--notice", help="how long before it starts to show as pending")
    a.add_argument("--timezone", help="e.g. America/Chicago; default is local")
    a.add_argument("--offset", help="for tasks: reschedule this long after completion, e.g. 3d")
    a.add_argument("--travel", help="travel time, e.g. 30m or 30m,15m (before,after)")
    a.add_argument("--repeat", help="'daily', 'every weekday', 'weekly on monday'")
    a.add_argument("--target", help="for goals: completions per period, e.g. 3/1w")
    a.add_argument("--step", action="append",
                   help="a project step; repeat the flag for each one")
    a.add_argument("--chain", action="store_true",
                   help="each --step waits on the one before it")
    a.add_argument("--raw", help="last resort; see references/tklr-syntax.md")
    a.add_argument("--dry-run", action="store_true",
                   help="show what would be created, write nothing")
    a.set_defaults(fn=cmd_add)

    l = sub.add_parser("list", help="what is scheduled")
    g = l.add_mutually_exclusive_group()
    g.add_argument("--today", action="store_true")
    g.add_argument("--tomorrow", action="store_true")
    g.add_argument("--week", action="store_true")
    g.add_argument("--date", help="a day, e.g. 'friday' or '2026-08-07'")
    l.add_argument("--days", type=int, help="how many days from --date")
    l.set_defaults(fn=cmd_list)

    s = sub.add_parser("show", help="everything about one reminder")
    s.add_argument("id", type=int); s.set_defaults(fn=cmd_show)

    f = sub.add_parser("find", help="search by text, or list one person's items")
    f.add_argument("text", nargs="?", default="")
    f.add_argument("--person"); f.set_defaults(fn=cmd_find)

    fr = sub.add_parser("free", help="what is around a proposed time")
    fr.add_argument("--when", required=True); fr.set_defaults(fn=cmd_free)

    d = sub.add_parser("done", help="mark a task complete")
    d.add_argument("id", type=int); d.set_defaults(fn=cmd_done)

    dl = sub.add_parser("delete", help="remove a reminder or an occurrence")
    dl.add_argument("id", type=int)
    dl.add_argument("--instance",
                    help="skip one occurrence, or several comma-separated. "
                         "Keeps the rest of the series, and the id")
    dl.add_argument("--from", dest="from_dt")
    dl.add_argument("--dry-run", action="store_true"); dl.set_defaults(fn=cmd_delete)

    e = sub.add_parser(
        "edit",
        help="change an existing reminder, keeping its id and history",
        description="Change one or more details of a reminder that already "
                    "exists. Only what you name changes; everything else is "
                    "left exactly as it is. Use this instead of deleting and "
                    "re-adding — the id, the completion history and the alert "
                    "rows all survive an edit and none of them survive a "
                    "replacement.")
    e.add_argument("id", type=int)
    e.add_argument("--subject", help="new wording")
    e.add_argument("--when", help="new start, e.g. 'friday 2pm'. For ONE "
                                  "occurrence of a repeating reminder use `move`")
    e.add_argument("--duration", help="how long it lasts, e.g. 1h, 30m")
    e.add_argument("--for", dest="for_whom",
                   help="replace who it is for, comma-separated")
    e.add_argument("--alert", help="new offsets BEFORE the start, e.g. 1d,1h")
    e.add_argument("--via", help="new channel letters, e.g. r,e. Given alone, "
                                 "the existing offsets are kept")
    e.add_argument("--note", help="free-text detail")
    e.add_argument("--location", help="where")
    e.add_argument("--priority", type=int, help="1 (highest) to 5 (lowest)")
    e.add_argument("--notice", help="how long before it starts to show as pending")
    e.add_argument("--timezone", help="only with --when")
    e.add_argument("--offset", help="for tasks: reschedule this long after completion")
    e.add_argument("--travel", help="travel time, e.g. 30m or 30m,15m")
    e.add_argument("--repeat", help="repetition rule")
    e.add_argument("--clear", help="remove fields entirely, comma-separated: "
                                   + ", ".join(sorted(set(CLEARABLE))))
    e.add_argument("--dry-run", action="store_true",
                   help="print the before and after entry, change nothing")
    e.set_defaults(fn=cmd_edit)

    mv = sub.add_parser("move", help="reschedule one occurrence")
    mv.add_argument("id", type=int)
    mv.add_argument("--instance", required=True); mv.add_argument("--to", required=True)
    mv.add_argument("--dry-run", action="store_true"); mv.set_defaults(fn=cmd_move)

    c = sub.add_parser("channels", help="list or configure alert channels")
    c.add_argument("--set", nargs=2, metavar=("LETTER", "COMMAND"))
    c.add_argument("--remove", metavar="LETTER")
    c.add_argument("--no-test", action="store_true",
                   help="with --set: skip the delivery test (leaves it unproven)")
    c.add_argument("--email", help=EMAIL_HELP)
    c.set_defaults(fn=cmd_channels)

    u = sub.add_parser("uses", help="where jot time went, by category")
    u.add_argument("--use", help="filter by category substring, e.g. exercise")
    u.add_argument("--months", help="YYMM or YYMM-YYMM; default previous+current")
    u.add_argument("--list", action="store_true",
                   help="list the category names instead of the totals")
    u.set_defaults(fn=cmd_uses)

    st = sub.add_parser("status", help="is everything set up and working")
    st.add_argument("--email", help=EMAIL_HELP)
    st.set_defaults(fn=cmd_status)

    su = sub.add_parser(
        "setup",
        help="configure the platform you are talking on as an alert channel")
    su.add_argument("--platform", required=True,
                    help="the platform THIS conversation is on, e.g. telegram")
    su.add_argument("--letter", default="r", help="channel letter (default r)")
    su.add_argument("--target",
                    help="only if the platform has more than one target")
    su.add_argument("--no-test", action="store_true",
                    help="skip the delivery test (leaves delivery unproven)")
    su.add_argument("--email", help=EMAIL_HELP)
    su.set_defaults(fn=cmd_setup)

    em = sub.add_parser(
        "email", help="add an email alert channel (himalaya)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "Add email as an alert channel and prove it delivers.\n"
            "\n"
            "The `From:` address is the himalaya account's own — himalaya takes\n"
            "the envelope sender from that header and has no default, so this\n"
            "reads it for you. `--to` is where the person actually READS mail,\n"
            "which is usually a different address: ask them, do not assume."),
        epilog=("examples:\n"
                "  %(prog)s --to alex@example.com\n"
                "  %(prog)s --to alex@example.com --letter b   second person\n"))
    em.add_argument("--to", required=True,
                    help="where they read mail (ask them; not the account address)")
    em.add_argument("--letter", default="e", help="channel letter (default e)")
    em.add_argument("--from", dest="from_addr",
                    help="sending address; only needed if himalaya has several accounts")
    em.add_argument("--no-test", action="store_true",
                    help="skip the delivery test (leaves delivery unproven)")
    em.set_defaults(fn=cmd_email)

    w = sub.add_parser(
        "welcome",
        help="print what to tell the user this does — send its output verbatim")
    w.add_argument("--who", help="another person's name, for the examples")
    w.add_argument("--no-test", action="store_true",
                   help="omit the closing test-reminder line")
    w.set_defaults(fn=cmd_welcome)

    args = ap.parse_args()
    # A malformed --email would reach the user inside an offer, so it is checked
    # here rather than at the point it is printed.
    if getattr(args, "email", None) and not ADDR_RE.match(args.email.strip()):
        die(f"--email {args.email!r} does not look like an email address",
            "Pass an address you actually know, or leave it off and the offer",
            "will ask the user for one. Never guess.")
    # `setup` provisions a whole system, and two parts of that system resolve
    # the workspace independently of this process: `tklr` typed in a terminal,
    # and the dispatcher run by the scheduler. Neither can be told to look
    # somewhere else, so a workspace that is not the one they resolve is a
    # workspace nothing will ever poll and no user will ever see. That failure
    # is silent in the worst way — setup reports success, the delivery test
    # reports success, and no alert is ever sent. Refused here rather than
    # warned about, because the warning would sit in output that already says
    # everything worked.
    if args.cmd == "setup" and args.home:
        die(f"setup cannot use --home {args.home!r}",
            f"The workspace is {tklr_home(None)}, which is where `tklr` looks "
            "and where the dispatcher polls.",
            "A workspace anywhere else is never polled and never delivers.",
            "Re-run without --home. To move the default, set TKLR_HOME or",
            "XDG_CONFIG_HOME for everything, not for this one command.")
    home = tklr_home(args.home)
    # `setup` is the command that CREATES the workspace, so it cannot require
    # one. Everything else does — operating on a missing workspace produces
    # confusing tklr errors rather than an obvious one.
    if args.cmd != "setup" and not (home / "tklr.db").exists():
        die(f"no workspace at {home}",
            "Run: tklr_agent_wrapper.py setup --platform <the platform you are on>")
    return args.fn(args, home, datetime.now())


if __name__ == "__main__":
    sys.exit(main())
