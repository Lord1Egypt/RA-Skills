#!/usr/bin/env python3
"""Fast, agent-free tklr alert dispatcher.

Run every minute by the Hermes cron scheduler with --no-agent. No LLM, no
agent loop, stdlib only. Prints NOTHING on success (Hermes treats empty
stdout as silent); prints only what a human needs to act on.

This mirrors what tklr's own UI does in `Controller.execute_due_alerts()` --
read due alerts, run each one's command, delete the row -- with a one-minute
window instead of the UI's hard-coded six seconds, because we poll from cron
rather than from a running event loop.

    every minute:
      1. `tklr alerts` -- makes tklr recompute today's Alerts rows
      2. reap rows that are more than MAX_LATE behind (see below)
      3. read rows whose trigger_datetime is now or earlier
      4. run each row's alert_command (shlex.split + subprocess, no shell)
      5. delete each row that was delivered
      6. append a line to the delivery log ($TKLR_ALERTS_LOG)

There is no routing table and no send ledger. Delivery is defined entirely by
the `[alerts]` section of the tklr workspace's config.toml: one lowercase
letter per (person, channel), whose command is the delivery. tklr renders
{name}, {when}, {start}, {time}, {location}, {description} into the stored
command, so the message text is config, not code.

Per-destination state is not needed either: tklr writes one Alerts row per
(offset x letter), so a row *is* a single delivery. Deleting the row it just
sent gives exact once-only semantics, and a failed row simply stays for the
next run while its siblings are already gone.

A retry is bounded by MAX_LATE (default 60 minutes, $TKLR_ALERTS_MAX_LATE to
change). Past that the row is reaped and reported once, never retried again.
Both halves of that matter. Without the reaper, a row whose command keeps
failing -- a channel letter that was removed, a send binary that is broken --
is retried every minute forever, spawning a subprocess each time and filling
the log. And without the *floor* on what counts as due, every alert missed
while this machine was off fires in a single burst when it comes back, which
for a day-long outage means a day of reminders at once. An alert an hour late
is not worth delivering; it is worth telling someone it was missed.

Two database accesses are deliberate workarounds for missing tklr commands,
and are the only ones in this skill:
  * DELETE a delivered row -- tklr has no CLI for `mark_alert_executed()`.
    Safe because populate_alerts() only regenerates rows with
    trigger_datetime >= now, so a past-due row is never recreated.
  * Read due rows, and clear two derived-state cache keys to work around
    tklr's stale-cache bug (see --heal).

Usage:
  tklr_alert_poller.py             dispatch due alerts
  tklr_alert_poller.py --heal      force tklr to rebuild derived tables first
  tklr_alert_poller.py --verbose   report what was seen even when nothing was
                                   due -- use this when verifying setup, because
                                   silence alone does NOT mean "delivered"
  tklr_alert_poller.py --check     REPORT ONLY. Sends nothing, deletes nothing,
                                   rebuilds nothing. This is what `status` runs,
                                   so inspecting a pending alert cannot consume
                                   it -- and so a passing check proves CRON
                                   delivered, not that the check itself did.
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import logging
import os
import shlex
import shutil
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Keep tklr's numpy import from spinning up one BLAS thread per core.
#
# `tklr/model.py` imports numpy at module scope, so every invocation pays for
# BLAS initialisation across the whole machine: measured 3.03 CPU-seconds per
# run unpinned versus 0.30 pinned, with no wall-clock difference either way
# (~0.35s both). Nothing on the alert path touches numpy, so it is pure waste
# -- and at once a minute it adds up to roughly 70 CPU-minutes a day, spent as
# short wide bursts across every core, which is exactly the shape that makes
# token latency stutter for the llama-server running on this box.
#
# Set here rather than in the cron job because Hermes cron jobs carry no env.
# Child processes inherit both these and the niceness below.
# putenv rather than assigning into this interpreter's environment mapping:
# only the children need these, and putenv is the API for precisely that -- it
# sets what children inherit and deliberately leaves our own mapping alone.
# Nothing in this file reads them back, so that costs nothing. It also keeps
# the skill from ever copying its whole environment to pass one value down,
# a shape a security scanner cannot tell apart from dumping it somewhere.
for _blas_var in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
):
    # getenv, not putenv unconditionally: an explicit setting from the caller
    # wins, matching the setdefault this replaced.
    if os.getenv(_blas_var) is None:
        os.putenv(_blas_var, "1")

try:
    os.nice(19)
except OSError:  # pragma: no cover - only if already at max niceness
    pass

def _default_tklr_home() -> Path:
    """Resolve the workspace the way tklr itself does.

    Mirrors tklr_env.TklrEnvironment._resolve_home: TKLR_HOME, then
    XDG_CONFIG_HOME/tklr, then ~/.config/tklr. Skipping the XDG step would
    point the dispatcher at a different database than tklr uses on any machine
    that sets it — alerts would be written in one workspace and polled in
    another.
    """
    env_home = os.environ.get("TKLR_HOME")
    if env_home:
        return Path(env_home).expanduser()
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg).expanduser() / "tklr"
    return Path.home() / ".config" / "tklr"


DEFAULT_TKLR_HOME = _default_tklr_home()

# Mirrors host.workspace_pin_path(). Spelled out rather than imported because
# this file is copied out of the skill directory on its own and arrives with no
# siblings -- see the note below about why it imports nothing from the skill.
PIN_PATH = (Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes")
            / "scripts" / "tklr-workspace-path")


def resolve_tklr_home() -> tuple[Path, str]:
    """The workspace to poll, and one word saying where that came from.

    Precedence, and the reasoning for it:

      1. $TKLR_HOME -- a caller that exports it means it. The wrapper does
         exactly this before running `--heal` against a workspace the user
         named, and the pin must not override a deliberate instruction.
      2. the pin -- written by setup. This is the branch cron takes, because
         cron exports nothing, and it is the whole reason the pin exists.
      3. the ambient default -- no pin yet (an install predating it, or a
         dispatcher deployed by hand). Preserves the old behaviour rather than
         refusing, since a missing pin is not evidence the workspace is wrong.

    Note there is no XDG branch here: steps 1 and 3 both go through
    `_default_tklr_home`, which already applies it.
    """
    if os.environ.get("TKLR_HOME"):
        return DEFAULT_TKLR_HOME, "TKLR_HOME"
    try:
        pinned = PIN_PATH.read_text(encoding="utf-8").strip()
    except OSError:
        pinned = ""
    if pinned:
        return Path(pinned).expanduser(), "pin"
    return DEFAULT_TKLR_HOME, "default"

# This file deliberately does NOT import host.py, unlike the rest of the skill:
# it is copied out of the skill directory to wherever the host's scheduler
# insists a script must live, and arrives there with no siblings. It needs no
# host call anyway -- it runs the shell command stored in the workspace and has
# no opinion about what that command is, which is exactly what makes the host
# swappable. The two host-shaped paths it does have are env-overridable, so a
# port sets the variables rather than editing this file.
HOST_LOG_DIR = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes") / "logs"
LOG_PATH = Path(os.environ.get("TKLR_ALERTS_LOG") or HOST_LOG_DIR / "tklr-alerts.log")

def lock_path_for(home: Path) -> Path:
    """One lock per workspace, not one lock for the whole machine.

    A single global lock meant `--heal` (which `tklr_agent_wrapper.py add` runs after
    every create) could lose a race to the every-minute cron dispatcher and
    silently skip healing, leaving a reminder with no alert while the user was
    told it had been created. Two different workspaces had no business
    excluding each other either.
    """
    override = os.environ.get("TKLR_ALERTS_LOCK")
    if override:
        return Path(override)
    try:
        key = str(home.resolve())
    except OSError:
        key = str(home)
    slug = hashlib.sha1(key.encode("utf-8")).hexdigest()[:8]
    return HOST_LOG_DIR / f".tklr-alerts.{slug}.lock"


# How long `--heal` waits for the dispatcher to finish before giving up.
# Healing only rebuilds derived tables, so waiting out a tick is always
# better than skipping the rebuild.
HEAL_LOCK_WAIT = 30.0

SEND_TIMEOUT = 45
TKLR_TIMEOUT = 60


def _max_late_minutes() -> int:
    """How far behind an alert may be and still be worth sending."""
    raw = os.environ.get("TKLR_ALERTS_MAX_LATE", "").strip()
    if not raw:
        return 60
    try:
        value = int(raw)
    except ValueError:
        return 60
    return value if value > 0 else 60


MAX_LATE = timedelta(minutes=_max_late_minutes())

problems: list[str] = []
log = logging.getLogger("tklr-alerts")


def setup_logging() -> None:
    """Append to LOG_PATH, matching the host's own log layout."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(LOG_PATH, maxBytes=1_000_000, backupCount=3)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    log.setLevel(logging.INFO)
    log.addHandler(handler)


def tklr_exe() -> str:
    return shutil.which("tklr") or str(Path.home() / ".local" / "bin" / "tklr")


def run_tklr(home: Path, *args: str) -> bool:
    try:
        subprocess.run(
            [tklr_exe(), "--home", str(home), *args],
            capture_output=True,
            timeout=TKLR_TIMEOUT,
            check=False,
        )
        return True
    except (OSError, subprocess.SubprocessError) as exc:
        problems.append(f"could not run `tklr {' '.join(args)}`: {exc}")
        log.error("tklr %s failed: %s", " ".join(args), exc)
        return False


# ---------------------------------------------------------------------------
# derived-table refresh (and the stale-cache workaround)
# ---------------------------------------------------------------------------

def needs_healing(db_path: Path) -> bool:
    """Detect tklr's stale derived-state bug.

    tklr rebuilds DateTimes/Alerts only when a version string derived from
    max(Records.modified) changes. That column has minute resolution, so
    reminders saved in the same clock minute as the previous rebuild leave the
    key unchanged and never get a DateTimes row -- which means no alerts, and
    absence from days/weeks/agenda. A scheduled reminder that has alerts but
    no DateTimes row is the fingerprint.

    `Records.alerts` holds a JSON list, and tklr writes the literal string
    '[]' for a record with no alerts at all. Testing `!= ''` counted that as
    "has alerts", so a single ordinary undated task -- which can never have a
    DateTimes row -- matched the fingerprint and pinned healing ON for every
    run, forever. That is not a cosmetic waste: the rebuild it triggers
    destroys any alert sitting in the minute it came due (see dispatch order
    in main), so one stray task silently stopped every alert on the machine.
    Parse the JSON and require a non-empty list.
    """
    try:
        conn = sqlite3.connect(db_path, timeout=15)
        rows = conn.execute(
            """
            SELECT R.alerts FROM Records R
            LEFT JOIN DateTimes D ON D.record_id = R.id
            WHERE R.alerts IS NOT NULL AND R.alerts != ''
              AND R.itemtype NOT IN ('?', 'x')
              AND D.record_id IS NULL
            """
        ).fetchall()
        conn.close()
    except sqlite3.Error:
        return False

    for (raw,) in rows:
        try:
            parsed = json.loads(raw)
        except (TypeError, ValueError):
            # Unparseable is not evidence of an alert; treat it as none rather
            # than pinning healing on because of one malformed row.
            continue
        if isinstance(parsed, list) and parsed:
            return True
        if isinstance(parsed, str) and parsed.strip():
            return True
    return False


def invalidate_derived_state(db_path: Path) -> None:
    """Drop tklr's derived-state cache keys so the next command rebuilds them.

    WORKAROUND: tklr exposes no way to force a rebuild. These two rows are a
    cache tklr recreates on its next command, not user data.
    """
    try:
        conn = sqlite3.connect(db_path, timeout=15)
        with conn:
            conn.execute("DELETE FROM DerivedState WHERE key IN ('datetimes', 'alerts')")
        conn.close()
        log.info("cleared stale derived-state cache keys")
    except sqlite3.Error as exc:
        problems.append(f"could not clear tklr derived state: {exc}")


def refresh_alerts(home: Path, db_path: Path, force: bool) -> None:
    """Have tklr recompute today's alerts, healing stale derived state."""
    if force:
        invalidate_derived_state(db_path)
        run_tklr(home, "alerts")
        return

    run_tklr(home, "alerts")
    if needs_healing(db_path):
        invalidate_derived_state(db_path)
        run_tklr(home, "alerts")


# ---------------------------------------------------------------------------
# dispatch
# ---------------------------------------------------------------------------

def _stamp(moment: datetime) -> str:
    """A trigger_datetime comparison key: local-naive, minute resolution."""
    return moment.strftime("%Y%m%d%H%M")


# tklr writes trigger_datetime as 'YYYYMMDDTHHMM', but its schema comment
# allows 'YYYYMMDDTHHMMSS'. Truncating to 12 characters makes every comparison
# the same width -- string ordering on mixed widths would put a row with
# seconds on the wrong side of the cutoff.
_TRIGGER_KEY = "substr(replace(trigger_datetime, 'T', ''), 1, 12)"


def reap_stale_alerts(conn: sqlite3.Connection, floor: datetime) -> list[sqlite3.Row]:
    """Discard alerts too far past due to be worth sending, and say which.

    An alert only lands here after failing every retry for MAX_LATE, or
    because nothing was polling when it came due. Either way it is now
    misleading rather than useful, and left in place it would be retried for
    as long as the row exists. Returns the reaped rows so the caller can
    report them -- exactly once, since they are gone afterwards.
    """
    stale = conn.execute(
        f"""
        SELECT alert_id, record_id, record_name, trigger_datetime,
               start_datetime, alert_name, alert_command
        FROM Alerts
        WHERE {_TRIGGER_KEY} < ?
        ORDER BY trigger_datetime, record_id, alert_name
        """,
        (_stamp(floor),),
    ).fetchall()

    if stale:
        with conn:
            conn.execute(
                f"DELETE FROM Alerts WHERE {_TRIGGER_KEY} < ?", (_stamp(floor),)
            )
    return stale


def fetch_due_alerts(
    conn: sqlite3.Connection, now: datetime, floor: datetime
) -> list[sqlite3.Row]:
    """Alerts whose trigger has arrived, and is not older than MAX_LATE.

    Never future ones. Read directly because no CLI command exposes this:
    tklr's get_alerts_for_window() filters `trigger_datetime BETWEEN now AND
    window_end`, so `tklr alerts` reports only alerts still in the future.
    """
    return conn.execute(
        f"""
        SELECT alert_id, record_id, record_name, trigger_datetime,
               start_datetime, alert_name, alert_command
        FROM Alerts
        WHERE {_TRIGGER_KEY} <= ? AND {_TRIGGER_KEY} >= ?
        ORDER BY trigger_datetime, record_id, alert_name
        """,
        (_stamp(now), _stamp(floor)),
    ).fetchall()


def delete_alert(conn: sqlite3.Connection, row: sqlite3.Row) -> None:
    """Remove a delivered alert -- tklr's own `mark_alert_executed()`, by hand.

    Keyed on the columns of tklr's unique index rather than alert_id, because
    `tklr alerts --format json` reports alert_id as null.
    """
    with conn:
        conn.execute(
            """
            DELETE FROM Alerts
            WHERE record_id = ? AND start_datetime = ?
              AND alert_name = ? AND COALESCE(trigger_datetime, '') = ?
            """,
            (
                row["record_id"],
                row["start_datetime"],
                row["alert_name"],
                row["trigger_datetime"] or "",
            ),
        )


def deliver(row: sqlite3.Row) -> tuple[bool, bool, str]:
    """Run one alert's command.

    Returns (delivered, retryable, detail). A command that cannot be parsed is
    not retryable -- it will fail identically every minute -- so the caller
    drops it after reporting rather than looping forever.
    """
    command = (row["alert_command"] or "").strip()
    if not command:
        return False, False, "alert has no command (is its letter defined in [alerts]?)"

    try:
        argv = shlex.split(command)
    except ValueError as exc:
        return False, False, (
            f"command could not be parsed ({exc}) -- an unbalanced quote, often "
            f'a \'"\' in the subject or details: {command}'
        )
    if not argv:
        return False, False, f"command is empty after parsing: {command}"

    resolved = shutil.which(argv[0])
    if resolved:
        argv[0] = resolved

    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=SEND_TIMEOUT)
    except FileNotFoundError:
        return False, False, f"command not found: {argv[0]}"
    except subprocess.TimeoutExpired:
        return False, True, f"{argv[0]} timed out after {SEND_TIMEOUT}s"
    except OSError as exc:
        return False, True, f"{argv[0]} failed: {exc}"

    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()
        return False, True, (
            f"{argv[0]} exited {proc.returncode}: {tail[-1] if tail else 'no output'}"
        )
    return True, False, ""


def main() -> int:
    force_heal = "--heal" in sys.argv[1:]
    verbose = "--verbose" in sys.argv[1:] or "-v" in sys.argv[1:]
    # --check: report only. Sends nothing, deletes nothing, rebuilds nothing.
    #
    # `status` used to call this script with --verbose, which performs a FULL
    # dispatch -- so the one command whose name promises to be read-only was
    # delivering due alerts and deleting their rows. Anyone inspecting a
    # pending test alert consumed it by looking at it, and the delivery it
    # proved was its own, not cron's.
    check_only = "--check" in sys.argv[1:]
    if check_only:
        force_heal = False
        verbose = True
    home, home_source = resolve_tklr_home()
    db_path = home / "tklr.db"

    setup_logging()

    if not db_path.exists():
        # Naming the source matters more than naming the path: "no database at
        # ~/.config/tklr" reads like the workspace was never created, when the
        # actual fault is usually that this run resolved a different workspace
        # than the one setup configured.
        print(f"tklr alerts: no tklr database at {db_path} (workspace from: {home_source})")
        if home_source != "pin":
            print("  setup records the workspace it configured; this run did not use it.")
            print(f"  expected the recorded path in {PIN_PATH}")
        return 1

    # One dispatcher at a time per workspace; a slow send must not cause a
    # double send. A plain dispatch run bails immediately when another is
    # already going -- the next minute will do. A --heal run instead waits,
    # because its caller is blocked on the answer and a skipped heal is a
    # reminder that silently never fires.
    lock_file = lock_path_for(home)
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    lock_fd = open(lock_file, "w", encoding="utf-8")
    deadline = time.monotonic() + (HEAL_LOCK_WAIT if force_heal else 0.0)
    while True:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except OSError:
            if time.monotonic() >= deadline:
                if force_heal:
                    # Never silent: the caller must be able to tell a heal
                    # that ran from one that did not.
                    print(
                        "tklr alerts: could not heal — another run held the "
                        f"lock for {HEAL_LOCK_WAIT:.0f}s ({lock_file})"
                    )
                    log.error("heal skipped: lock held for %ss", HEAL_LOCK_WAIT)
                    lock_fd.close()
                    return 1
                lock_fd.close()
                return 0  # previous run still going
            time.sleep(0.25)

    try:
        # ORDER MATTERS: read and send what is due BEFORE asking tklr to
        # regenerate anything.
        #
        # Regenerating clears a record's alert rows and re-creates only the
        # ones still in the FUTURE. An alert sitting in the very minute it came
        # due is therefore deleted and not restored -- so running the rebuild
        # first destroyed exactly the row this run was about to deliver.
        # Measured: row present at 22:11:04, gone the instant the rebuild ran.
        #
        # This used to be survivable because the rebuild only happened when
        # tklr's gate opened. Once needs_healing() got stuck ON, it happened
        # every minute and nothing was ever delivered again. Both halves are
        # fixed, but the ordering is the one that makes it impossible rather
        # than unlikely: dispatch reads a table nothing else is touching.
        #
        # Nothing is lost by generating afterwards. A trigger has to be in the
        # future to be generated at all, so by the time it is due its row was
        # written by an earlier run.
        conn = sqlite3.connect(db_path, timeout=15)
        conn.row_factory = sqlite3.Row

        now = datetime.now()
        floor = now - MAX_LATE

        for row in ([] if check_only else reap_stale_alerts(conn, floor)):
            label = f"{row['record_name']} [{row['alert_name']}]"
            when = row["trigger_datetime"]
            log.error("gave up on %s: due %s, more than %s late", label, when, MAX_LATE)
            problems.append(
                f"{label}: never delivered — it came due at {when}, "
                f"more than {MAX_LATE} ago (given up on)"
            )

        due = fetch_due_alerts(conn, now, floor)

        sent = 0
        for row in ([] if check_only else due):
            label = f"{row['record_name']} [{row['alert_name']}]"
            delivered, retryable, detail = deliver(row)

            if delivered:
                delete_alert(conn, row)
                sent += 1
                log.info("sent %s: %s", label, row["alert_command"])
            elif retryable:
                log.warning("deferred %s: %s", label, detail)
                problems.append(
                    f"{label}: {detail} (will retry until it is {MAX_LATE} past due)"
                )
            else:
                delete_alert(conn, row)
                log.error("dropped %s: %s", label, detail)
                problems.append(f"{label}: {detail} (dropped)")

        if sent:
            log.info("dispatched %d alert(s)", sent)

        # Only now: let tklr materialise rows for triggers still ahead of us.
        # Everything due has already been sent and deleted, so a rebuild has
        # nothing left to destroy.
        if not check_only:
            refresh_alerts(home, db_path, force_heal)

        # Silence on success. Speak up only when a human should know.
        if problems:
            print("\n".join(["tklr alerts:"] + [f"  - {p}" for p in problems]))
        elif verbose:
            # Verifying setup? Then silence must not be mistaken for delivery.
            # Report positively, including the "nothing was due" case, and say
            # why nothing was due if the workspace simply has no alerts.
            queued = conn.execute("SELECT COUNT(*) FROM Alerts").fetchone()[0]
            if check_only and due:
                print(f"tklr alerts: {len(due)} due RIGHT NOW and not yet sent "
                      f"(--check sent nothing). Cron should deliver within a "
                      f"minute; if it does not, the cron job is not running.")
            print(
                f"tklr alerts: {len(due)} due, {sent} sent, "
                f"{queued} still queued for later today"
            )
            if not due and not queued:
                print(
                    "  Nothing was due AND nothing is queued. If you expected a "
                    "test alert, the reminder probably has no alerts at all — "
                    "check it is not a draft ('?') and that its @a letter is "
                    "defined in the [alerts] section of config.toml."
                )
        conn.close()
        return 0
    finally:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
        finally:
            lock_fd.close()


if __name__ == "__main__":
    sys.exit(main())
