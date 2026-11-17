#!/usr/bin/env python3
"""Add, change, or list tklr alert channel letters — safely.

Editing the `[alerts]` section by hand has three traps. This script handles all
of them so callers never have to:

  1. The section normally exists but holds only comments, so a naive
     "append after [alerts]" or "create the section" both go wrong.
  2. An apostrophe anywhere in a command makes tklr rewrite the file as invalid
     TOML, and the command after that discards the whole section — the channel
     silently disappears two tklr runs later.
  3. Whether the letter survived can only be established by running tklr twice
     and re-reading the file, because erasure takes two runs.

Usage
  set_alert_channel.py --list
  set_alert_channel.py --mail-accounts        # himalaya account -> From: address
  set_alert_channel.py r '<any shell command that sends a message>'
  set_alert_channel.py --remove r
  set_alert_channel.py --home ~/.config/tklr r '<command>'

A letter's value is a plain shell command, so the channel can be anything this
machine can send with. The only host-specific part is validating a chat target
against what the machine can reach, which goes through host.py.

Exit codes: 0 ok, 1 rejected/failed, 2 usage error.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import host

RESERVED = {"n"}  # built-in: bell + notification popup


def die(msg: str, code: int = 1) -> "NoReturn":  # type: ignore[valid-type]
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def warn(msg: str) -> None:
    """Flag something that will still work but probably isn't what was meant."""
    print(f"warning: {msg}", file=sys.stderr)


def default_home() -> Path:
    """Resolve the workspace the way tklr itself does: TKLR_HOME, then
    XDG_CONFIG_HOME/tklr, then ~/.config/tklr."""
    env_home = os.environ.get("TKLR_HOME")
    if env_home:
        return Path(env_home).expanduser()
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg).expanduser() / "tklr"
    return Path.home() / ".config" / "tklr"


def read_alerts(config: Path) -> dict[str, str]:
    try:
        data = tomllib.loads(config.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        die(f"{config} is not valid TOML ({exc}).\n"
            f"       tklr may have corrupted it — see the apostrophe bug. "
            f"Fix or delete the bad line, then retry.")
    except OSError as exc:
        die(f"cannot read {config}: {exc}")
    alerts = data.get("alerts")
    return dict(alerts) if isinstance(alerts, dict) else {}


def section_bounds(lines: list[str]) -> tuple[int, int] | tuple[None, None]:
    """Return (header_index, end_index) of the [alerts] table, or (None, None)."""
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "[alerts]":
            start = i
            break
    if start is None:
        return None, None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if re.match(r"^\s*\[", lines[i]):
            end = i
            break
    return start, end


def back_up_once(config: Path) -> None:
    """Keep the config as it was before this skill first touched it.

    Written once and never overwritten, so it holds the user's own file rather
    than the state left by the previous run of this script. Someone who already
    used tklr arrives with a config they tuned by hand, and every alert letter
    is an edit to it; a first-touch copy is what makes that reversible.

    Best effort: a config that cannot be copied is not a reason to refuse to
    configure a channel, so this warns and continues.
    """
    backup = config.with_name(config.name + ".before-tklr-reminders")
    if backup.exists() or not config.exists():
        return
    try:
        shutil.copy2(config, backup)
        print(f"  saved your original config to {backup.name}")
    except OSError as exc:
        warn(f"could not back up {config.name} ({exc}); continuing")


def write_letter(config: Path, letter: str, command: str | None) -> None:
    """Insert/replace/remove one letter inside [alerts], preserving everything else."""
    back_up_once(config)
    text = config.read_text(encoding="utf-8")
    lines = text.splitlines()

    start, end = section_bounds(lines)
    if start is None:
        # No [alerts] table at all — append one at the end.
        lines += ["", "[alerts]"]
        start, end = len(lines) - 1, len(lines)

    body = lines[start + 1:end]
    pattern = re.compile(rf"^\s*{re.escape(letter)}\s*=")
    body = [ln for ln in body if not pattern.match(ln)]

    if command is not None:
        # Single-quoted literal string: what tklr itself emits, so it round-trips
        # byte-for-byte and no "Updated ... with missing defaults" rewrite occurs.
        entry = f"{letter} = '{command}'"
        # Place new entries directly after the header, above the comment block,
        # so they are the first thing a human sees.
        body.insert(0, entry)

    new_lines = lines[:start + 1] + body + lines[end:]
    new_text = "\n".join(new_lines).rstrip("\n") + "\n"

    # Never write a file tklr cannot parse.
    try:
        tomllib.loads(new_text)
    except tomllib.TOMLDecodeError as exc:
        die(f"refusing to write — the result would not be valid TOML ({exc})")

    tmp = config.with_suffix(config.suffix + ".tmp")
    tmp.write_text(new_text, encoding="utf-8")
    tmp.replace(config)


def run_tklr(home: Path, *args: str) -> subprocess.CompletedProcess[str] | None:
    exe = shutil.which("tklr") or str(Path.home() / ".local" / "bin" / "tklr")
    try:
        return subprocess.run(
            [exe, "--home", str(home), *args],
            capture_output=True, text=True, timeout=90,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"warning: could not run tklr ({exc})", file=sys.stderr)
        return None


def verify_round_trip(home: Path, config: Path, expect: set[str]) -> bool:
    """tklr rewrites config.toml on load; erasure takes two runs, so run twice."""
    run_tklr(home, "agenda")
    run_tklr(home, "agenda")
    still = set(read_alerts(config))
    missing = expect - still
    if missing:
        print(f"  FAILED: {', '.join(sorted(missing))} vanished after tklr rewrote "
              f"the config — almost certainly an apostrophe in the command.",
              file=sys.stderr)
        return False
    return True


def mail_accounts() -> list[tuple[str, str]]:
    """Return [(account_name, from_address)] for each himalaya account.

    `himalaya account list --json` gives the account NAME only -- neither it nor
    `account check` reveals the address, and the `From:` header a delivery command
    needs must be the account's own address. The address lives solely in
    himalaya's config.

    That config also holds credentials, so this reads it here, once, and emits
    nothing but addresses. Do not have an agent parse that file directly: it is a
    plaintext-password file in a common setup, and a stray dump leaks the lot.

    Key names vary by auth mechanism (`sasl.plain.authcid`, `login`, or a
    top-level `email`), so rather than hardcoding one path this walks the
    account's subtree and takes the first address-shaped value, preferring
    explicitly-named keys. Skips anything that smells like a secret.
    """
    cfg = Path.home() / ".config" / "himalaya" / "config.toml"
    if not cfg.is_file():
        return []
    try:
        data = tomllib.loads(cfg.read_text(encoding="utf-8"))
    except (tomllib.TOMLDecodeError, OSError):
        return []
    accounts = data.get("accounts")
    if not isinstance(accounts, dict):
        return []

    SECRET = ("pass", "secret", "token", "key", "cmd")
    PREFERRED = ("email", "authcid", "login", "user", "from")

    def find(node, depth=0):
        """Yield (key_rank, value) for address-shaped strings under *node*."""
        if depth > 6 or not isinstance(node, dict):
            return
        for k, v in node.items():
            kl = str(k).lower()
            if any(s in kl for s in SECRET):
                continue
            if isinstance(v, str) and "@" in v and " " not in v.strip():
                rank = PREFERRED.index(kl) if kl in PREFERRED else len(PREFERRED)
                yield rank, v.strip()
            elif isinstance(v, dict):
                yield from find(v, depth + 1)

    out = []
    for name, acct in accounts.items():
        hits = sorted(find(acct))
        if hits:
            out.append((str(name), hits[0][1]))
    return out


def check_mail_headers(command: str) -> None:
    """Refuse a himalaya command with no `From:` header.

    himalaya takes the envelope sender from the message's `From:` header and has
    no fallback: without one it exits 1 with "No `From:` header found in raw
    message" and sends nothing, so every alert on the letter fails for the life
    of the reminder. This skill shipped exactly that command for months, because
    a letter can be created and validated without an email ever being sent.
    """
    if "himalaya" not in command:
        return
    if re.search(r"(?i)\bFrom:", command):
        return
    die("this himalaya command has no `From:` header.\n"
        "       himalaya takes the envelope sender from `From:` and has no\n"
        "       default -- it would exit 1 with \"No `From:` header found in raw\n"
        "       message\" every time, so the alert would never be delivered.\n"
        "       Add it as the first header, set to the himalaya account's own\n"
        "       address (`himalaya account list --json` names the accounts):\n"
        "         printf \"From: account@example.com\\\\nTo: them@example.com\\\\n...\"")


# The complete set tklr substitutes. Anything else in braces survives into the
# delivered message as literal text -- `{message}` reached a user verbatim.
KNOWN_PLACEHOLDERS = frozenset(
    {"name", "when", "start", "time", "location", "description"}
)

# Braces that are part of shell/printf syntax rather than a tklr placeholder.
_BRACE_RE = re.compile(r"\{([^{}]*)\}")


def check_placeholders(command: str) -> None:
    """Refuse a message template containing a placeholder tklr will not fill.

    Same failure class as an unreachable target, and just as permanent: tklr
    substitutes only the six names it knows, leaves every other `{...}` alone,
    and the dispatcher counts the send as a success. A letter written with
    `{message}` delivered "Test Alert: {message}" to a real user and would have
    kept doing it for the life of the letter.

    Also warns -- does not refuse -- when the template carries no time at all.
    An alert that names the event but never says when it starts reads as an
    assistant announcing an upcoming reminder rather than being one.
    """
    unknown = sorted(
        {
            m.group(1)
            for m in _BRACE_RE.finditer(command)
            # `{}`, `{1}` and `${VAR}`-ish forms are shell, not placeholders
            if m.group(1).isidentifier()
            and m.group(1) not in KNOWN_PLACEHOLDERS
            # `${VAR}` is a shell expansion, not a tklr placeholder
            and not (m.start() and command[m.start() - 1] == "$")
        }
    )
    if unknown:
        die("unknown placeholder(s) in the message: "
            + ", ".join("{%s}" % u for u in unknown) + "\n"
            "       tklr substitutes only {name}, {when}, {start}, {time},\n"
            "       {location} and {description}. Anything else is delivered to\n"
            "       the user as literal text, on every alert, for the life of\n"
            "       this letter -- and the send still reports success, so it is\n"
            "       never noticed. Copy a message shape from\n"
            "       templates/alerts-config-example.toml and change only the\n"
            "       target.")

    if "{time}" in command:
        warn("{time} renders minutes as garbage when `ampm = false` "
             "(\"Sunday at 22 o 4 hours\"). Prefer {start}.")

    if not ({"{when}", "{start}", "{time}"} & set(re.findall(r"\{\w+\}", command))):
        warn("this message says nothing about when the event starts. Without a "
             "time it reads as an announcement of an upcoming reminder rather "
             "than the reminder itself. The shipped shape is "
             "\"Reminder: {name} - starts {when} ({start})\".")


def check_send_target(command: str) -> None:
    """Refuse a chat target that does not exist on this machine.

    A host that reports success for a destination it cannot actually reach
    makes a made-up target a perfect black hole: the dispatcher sees success,
    deletes the alert row, logs "sent", and the message reaches nobody. The
    only moment this is catchable is now, against the list of real targets.

    Only `--to <platform>:<id>` is checked, and only when the host's listing
    can be read -- an unreachable listing must not block setup.

    The listing itself comes from host.py. Nothing about which agent provides
    it belongs here.
    """
    m = re.search(r"--to\s+(\S+)", command)
    if not m:
        return
    target = m.group(1).strip("\"'")

    try:
        listed = host.chat_list()
    except host.HostError:
        return
    if not listed.strip():
        return

    available = host.chat_target_ids(listed)
    platforms = host.chat_platforms(listed)

    # The platform is a closed set and always checkable. Getting it wrong -- an
    # account or provider name where a platform belongs -- would otherwise be
    # written into config.toml unchallenged, and every alert on that letter
    # fails for the life of the reminder.
    platform = target.split(":", 1)[0].lower() if ":" in target else target.lower()
    if platforms and platform not in platforms:
        die(f"'{platform}' is not a messaging platform on this machine.\n"
            f"       Configured platforms: {', '.join(sorted(platforms))}\n"
            "       A target is `<platform>:<id>`, or a bare platform name for its\n"
            "       home channel -- never an account or provider name. Take one\n"
            f"       from {host.target_hint()}.")

    if ":" not in target or not available:
        return  # bare platform name means the home channel; nothing more to check

    ident = target.split(":", 1)[1].split("/")[0]

    # Only chat ids are enumerable, and they are the ones that fail silently.
    # Email addresses and phone numbers are open-ended -- `--list` cannot know
    # every address you might mail -- so checking them against it would reject
    # perfectly good targets.
    if "@" in ident or ident.startswith("+"):
        return

    if any(ident and ident in cand for cand in available):
        return

    die(f"'{target}' is not one of this machine's messaging targets.\n"
        "       A send to a room that does not exist can report success, so\n"
        "       nothing would ever tell you the alerts went nowhere.\n"
        f"       Copy a target verbatim from {host.target_hint()}:\n"
        + "\n".join(f"         {c}" for c in available))


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("letter", nargs="?", help="one lowercase letter a-z")
    ap.add_argument("command", nargs="?", help="the delivery command")
    ap.add_argument("--home", default=None, help="tklr workspace (default $TKLR_HOME or ~/.config/tklr)")
    ap.add_argument("--list", action="store_true", help="show configured letters and exit")
    ap.add_argument("--mail-accounts", action="store_true",
                    help="print 'account<TAB>address' per himalaya account (the From: address)")
    ap.add_argument("--remove", metavar="LETTER", help="delete a letter")
    args = ap.parse_args()

    home = Path(args.home).expanduser() if args.home else default_home()
    config = home / "config.toml"
    if not config.exists():
        die(f"no config at {config}",
            "Run: tklr_agent_wrapper.py setup --platform <the platform you are on>")

    if args.mail_accounts:
        found = mail_accounts()
        if not found:
            print("no himalaya email accounts found")
            return 1
        for name, addr in found:
            print(f"{name}\t{addr}")
        return 0

    if args.list:
        alerts = read_alerts(config)
        if not alerts:
            print("no alert channels configured")
            return 0
        for k in sorted(alerts):
            print(f"{k} = {alerts[k]}")
        return 0

    if args.remove:
        letter = args.remove
        if letter not in read_alerts(config):
            die(f"letter '{letter}' is not configured")
        write_letter(config, letter, None)
        print(f"removed '{letter}'")
        return 0

    if not args.letter or args.command is None:
        ap.print_usage(sys.stderr)
        die("give a letter and a command, or use --list / --remove", 2)

    letter, command = args.letter, args.command

    # --- validation, in the order most likely to catch a mistake -----------
    if not re.fullmatch(r"[a-z]", letter):
        die(f"'{letter}' is not a single lowercase letter. tklr enforces a-z "
            f"(is_lowercase_letter); multi-character names are rejected.")
    if letter in RESERVED:
        die(f"'{letter}' is built into tklr (bell + popup) — pick another letter")
    if "'" in command:
        die("the command contains an apostrophe.\n"
            "       tklr re-emits every value in SINGLE quotes when it rewrites\n"
            "       config.toml, so an apostrophe produces invalid TOML and the\n"
            "       next run deletes the whole [alerts] section.\n"
            "       Reword it: \"It is time\", not \"It's time\".")
    if not command.strip():
        die("the command is empty")
    if command.strip() in {"true", ":", "/bin/true", "echo", "cat"}:
        die(f"'{command.strip()}' is a no-op. The dispatcher would treat the alert as\n"
            "       delivered and delete it, so the reminder would reach nobody.\n"
            "       Use a real delivery command.")
    check_send_target(command)
    check_mail_headers(command)
    check_placeholders(command)

    existing = read_alerts(config)
    verb = "updated" if letter in existing else "added"
    write_letter(config, letter, command)

    # --- prove it actually took ------------------------------------------
    alerts = read_alerts(config)
    if alerts.get(letter) != command:
        die("the letter did not land in the file as written")

    if not verify_round_trip(home, config, {letter}):
        return 1

    probe = f"* Probe @s 2099-08-05 3p @a 1h: {letter}"
    res = run_tklr(home, "check", probe)
    if res is not None and "Entry is valid" not in (res.stdout or ""):
        detail = (res.stdout or res.stderr or "").strip().splitlines()
        print(f"  WARNING: tklr will not accept '@a 1h: {letter}' — "
              f"{detail[-1] if detail else 'no output'}", file=sys.stderr)
        return 1

    print(f"{verb} '{letter}' and verified it:")
    print(f"  survives tklr rewriting config.toml")
    print(f"  '@a 1h: {letter}' validates")
    print(f"  configured letters: {', '.join(sorted(read_alerts(config)))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
