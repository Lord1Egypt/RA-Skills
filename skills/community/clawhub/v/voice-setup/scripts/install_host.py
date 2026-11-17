#!/usr/bin/env python3
"""
install_host.py - wire the active voice into Claude Code, and unwire it.

A Claude Code plugin ships `output-styles/` and `hooks/hooks.json` at its root
and the host discovers both when the plugin is enabled, so **a plugin install
needs nothing from this script**. It exists for the other install paths the
README documents: a symlink into `~/.claude/skills/`, a loose-skill checkout,
anything where there is no plugin for the host to read those directories from.
There, the only way to reach the same two features is to write into the user's
own configuration, which is what everything below is careful about.

    install_host.py --status
    install_host.py --install --dry-run
    install_host.py --install
    install_host.py --uninstall

What `--install` writes, at `--scope user` (the default):

    ~/.claude/output-styles/rabbit-<voice>.md   generated from the active voice
    ~/.claude/output-styles/rabbit-writes.md    the static baseline
    ~/.claude/settings.json                     hooks, and `outputStyle`
    ~/.claude/rabbit-writes-host.json           the record of the three above

`--scope project` writes the same tree under `.claude/` in the working
directory instead.

**The sidecar is the whole uninstall story.** It records every path written,
the hash each file had when this script wrote it, every hook command added, and
the previous value of `outputStyle`. `--uninstall` reads it and removes exactly
that: it restores the old `outputStyle` rather than deleting the key, it drops
only hook entries naming this plugin's runner, and it refuses to delete a style
file whose hash has moved, because somebody's edits to their own style file are
theirs. Without a sidecar it falls back to matching on the runner path and
prints what it matched before touching anything.

**It never rewrites a settings file it could not parse**, and it copies the
file to `settings.json.rabbit-bak` before the first edit either way. A JSON
round-trip reformats the whole document, which is a real cost and the reason
for the backup.

Claude Code only. Output styles and this hook schema are that host's, and the
rest of this plugin serves Codex through the same manifests. On a machine with
no `~/.claude` this reports what it found and writes nothing.

Stdlib only, 3.9+.
"""

import argparse
import hashlib
import json
import os
import shutil
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)
# skills/rabbit-reads/scripts/_bootstrap.py answers to the same bare name and
# can already be cached in sys.modules from an earlier import in the same
# process (a combined pytest run, for one). check_notes.py carries this same
# guard for the same reason.
if ("_bootstrap" in sys.modules
        and getattr(sys.modules["_bootstrap"], "__file__", None)
        != os.path.join(_SCRIPT_DIR, "_bootstrap.py")):
    del sys.modules["_bootstrap"]
from _bootstrap import (HERE, ENGINE_DIR, cli_error,  # noqa: E402
                        voices_mod)

sys.path.insert(0, os.path.join(ENGINE_DIR, "scripts"))
from rwlib import outputstyle  # noqa: E402

def _first_existing(*candidates):
    """The first path that is there, or the first candidate for the error.

    Two layouts have to work. In a checkout the engine is a sibling skill, and
    in a packaged bundle its files are vendored beside this script, which is
    the same reason `_bootstrap` searches two directories for `rwlib`. Falling
    back to the first candidate rather than to None keeps the error message
    naming the path somebody would look for.
    """
    for path in candidates:
        if path and os.path.exists(path):
            return path
    return candidates[0]


# The runner the hook entries point at. `claude_hook.py` is in
# SHARED_ENGINE_FILES, so a bundle carries it beside this script's own
# directory rather than under a sibling skill that is not there.
HOOK_RUNNER = _first_existing(
    os.path.join(ENGINE_DIR, "scripts", "claude_hook.py"),
    os.path.join(HERE, "claude_hook.py"))

# The static baseline style lives at the plugin root, which only exists in a
# full checkout. A bundle installs the generated voice style alone, and
# `plan_install` already skips this file when it is missing.
BASELINE_STYLE = _first_existing(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))),
                 "output-styles", "rabbit-writes.md"),
    os.path.join(os.path.dirname(HERE), "output-styles", "rabbit-writes.md"))

SIDECAR_NAME = "rabbit-writes-host.json"
SIDECAR_VERSION = 1
BACKUP_SUFFIX = ".rabbit-bak"

# One entry per hook this script installs. The event and matcher have to match
# `hooks/hooks.json` at the plugin root, because the two are the same feature
# reaching two install paths, and a user who moves from one to the other should
# not get different behaviour.
HOOK_SPECS = (
    {"event": "SessionStart", "matcher": None, "timeout": 15},
    {"event": "PreToolUse", "matcher": "Bash", "timeout": 25},
    {"event": "PostToolUse", "matcher": "Write|Edit", "timeout": 30},
)

# A list of commands, not a block: cli_error iterates this, so a string here
# prints one character per line.
EXAMPLES = [
    "python3 install_host.py --status",
    "python3 install_host.py --install --dry-run",
    "python3 install_host.py --install",
    "python3 install_host.py --install --scope project",
    "python3 install_host.py --uninstall",
]


# --------------------------------------------------------------------------
# Where things live


def _home_dir():
    """The user's home directory, honoring `$HOME` even on Windows.

    `os.path.expanduser("~")` on Windows prefers `USERPROFILE`, then falls
    back to `HOMEDRIVE`+`HOMEPATH`, and only reaches `HOME` if neither of
    those is set. A CI runner has `HOMEDRIVE`/`HOMEPATH` set for the real
    account, so `tests/test_install_host.py` popping just `USERPROFILE` and
    setting `HOME` to a throwaway directory was silently landing every write
    in the real `~/.claude` on Windows instead.
    """
    return os.environ.get("HOME") or os.path.expanduser("~")


def scope_root(scope):
    if scope == "project":
        return os.path.join(os.getcwd(), ".claude")
    return os.path.join(_home_dir(), ".claude")


def hook_command():
    return 'python3 "%s"' % HOOK_RUNNER


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _changed_since_written(path, record):
    """Whether a file this script wrote no longer matches its recorded hash.

    A file it cannot even read as UTF-8 (a hand edit that changed the
    encoding, not just the text) is changed by definition: `_sha(_read(...))`
    would otherwise raise `UnicodeDecodeError` and crash `--status` and
    `--uninstall` instead of reporting or protecting the edit.
    """
    try:
        return _sha(_read(path)) != record.get("sha256")
    except (OSError, UnicodeDecodeError):
        return True


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp.%d" % os.getpid()
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.replace(tmp, path)


# --------------------------------------------------------------------------
# The settings file


def load_settings(path):
    """(dict, error). An unparseable file is an error and never a fresh dict.

    Overwriting a settings file this script could not read would discard
    whatever the user has in it, and "it was broken already" is not a defence
    when the backup is written from the same read.
    """
    if not os.path.exists(path):
        return {}, None
    try:
        text = _read(path)
    except OSError as exc:
        return None, str(exc)
    if not text.strip():
        return {}, None
    try:
        data = json.loads(text)
    except ValueError as exc:
        return None, "%s is not valid JSON: %s" % (path, exc)
    if not isinstance(data, dict):
        return None, "%s does not hold a JSON object" % path
    return data, None


def backup_settings(path):
    if not os.path.exists(path):
        return None
    dest = path + BACKUP_SUFFIX
    shutil.copy2(path, dest)
    return dest


def add_hooks(settings, command):
    """Add this plugin's hook entries. Returns the count actually added."""
    hooks = settings.setdefault("hooks", {})
    added = 0
    for spec in HOOK_SPECS:
        groups = hooks.setdefault(spec["event"], [])
        if not isinstance(groups, list):
            continue
        if _find_group(groups, command) is not None:
            continue                    # already installed, so this is a no-op
        entry = {"hooks": [{"type": "command", "command": command,
                            "timeout": spec["timeout"]}]}
        if spec["matcher"]:
            entry["matcher"] = spec["matcher"]
        groups.append(entry)
        added += 1
    return added


def _find_group(groups, command):
    for i, group in enumerate(groups):
        if not isinstance(group, dict):
            continue
        for hook in group.get("hooks", []):
            if isinstance(hook, dict) and hook.get("command") == command:
                return i
    return None


def remove_hooks(settings, command):
    """Drop only the entries naming this command, then prune what is empty.

    Pruning matters. A `PostToolUse` key left holding an empty list, or a
    matcher group whose `hooks` list is now empty, is residue that reads as a
    configured hook to anybody opening the file later.
    """
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        return 0
    removed = 0
    for event in list(hooks):
        groups = hooks.get(event)
        if not isinstance(groups, list):
            continue
        kept_groups = []
        for group in groups:
            if not isinstance(group, dict):
                kept_groups.append(group)
                continue
            entries = group.get("hooks")
            if not isinstance(entries, list):
                kept_groups.append(group)
                continue
            kept = [h for h in entries
                    if not (isinstance(h, dict) and h.get("command") == command)]
            removed += len(entries) - len(kept)
            if not kept:
                continue                # the whole group was ours
            group["hooks"] = kept
            kept_groups.append(group)
        if kept_groups:
            hooks[event] = kept_groups
        else:
            del hooks[event]
    if not hooks:
        settings.pop("hooks", None)
    return removed


# --------------------------------------------------------------------------
# The sidecar


def sidecar_path(scope):
    return os.path.join(scope_root(scope), SIDECAR_NAME)


def read_sidecar(scope):
    path = sidecar_path(scope)
    if not os.path.exists(path):
        return None
    try:
        data = json.loads(_read(path))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


# --------------------------------------------------------------------------
# The generated style


def active_style(voices_dir=None):
    """(voice_name, rendered_text) for the active profile, or (None, None)."""
    rules_path, name, _note = voices_mod.resolve(voices_dir=voices_dir)
    if not rules_path or not name:
        return None, None
    rules = voices_mod.load(rules_path, voices_dir=voices_dir)
    profile_md = ""
    md_path = os.path.join(os.path.dirname(rules_path), name + ".md")
    if os.path.exists(md_path):
        profile_md = _read(md_path)
    return name, outputstyle.render(rules, profile_md, voice_name=name)


# --------------------------------------------------------------------------
# Commands


def plan_install(scope):
    """[(path, text)] this install would write, plus the voice name."""
    root = scope_root(scope)
    styles_dir = os.path.join(root, "output-styles")
    files = []

    voice, rendered = active_style()
    if voice:
        files.append((os.path.join(styles_dir,
                                   outputstyle.style_filename(voice)), rendered))
    if os.path.exists(BASELINE_STYLE):
        files.append((os.path.join(styles_dir, "rabbit-writes.md"),
                      _read(BASELINE_STYLE)))
    return voice, files


def do_status(args):
    root = scope_root(args.scope)
    print("host:      Claude Code" if os.path.isdir(root)
          else "host:      no %s, so nothing is installed here" % root)
    print("scope:     %s (%s)" % (args.scope, root))

    rules_path, name, note = voices_mod.resolve()
    if rules_path and name:
        print("voice:     %s" % name)
    else:
        print("voice:     none active")
        if note:
            print("           %s" % note)

    print("runner:    %s" % ("found" if os.path.exists(HOOK_RUNNER) else
                             "MISSING at %s" % HOOK_RUNNER))

    side = read_sidecar(args.scope)
    if not side:
        settings, _err = load_settings(os.path.join(root, "settings.json"))
        hook_count = _count_hooks(settings or {}, hook_command())
        if hook_count:
            print("installed: partially (no %s, but %d hook entry(s) naming "
                  "this plugin's runner are in settings.json). Generated "
                  "output-style files cannot be identified without that "
                  "record; check %s by hand."
                  % (SIDECAR_NAME, hook_count,
                     os.path.join(root, "output-styles")))
        else:
            print("installed: no (no %s)" % SIDECAR_NAME)
        return 0
    print("installed: yes")
    for record in side.get("files", []):
        path = record.get("path", "")
        state = "ok"
        if not os.path.exists(path):
            state = "gone"
        elif _changed_since_written(path, record):
            state = "edited by hand"
        print("           %s (%s)" % (path, state))
    if side.get("hook_command"):
        print("           hook: %s" % side["hook_command"])
    print("           previous outputStyle: %r"
          % side.get("previous_output_style"))
    return 0


def do_install(args):
    root = scope_root(args.scope)
    settings_path = os.path.join(root, "settings.json")

    if not os.path.exists(HOOK_RUNNER):
        print(cli_error.format_file_error(
            "install_host.py", HOOK_RUNNER, "hook runner",
            expected_type="path to claude_hook.py in the rabbit-writes skill",
            details="The hooks this installs point at that file, and a "
                    "settings entry naming a path that does not exist is a "
                    "hook the host reports as failing on every event.",
            examples=EXAMPLES), file=sys.stderr)
        return 2

    settings, err = load_settings(settings_path)
    if err:
        print(cli_error.format_file_error(
            "install_host.py", settings_path, "--scope %s" % args.scope,
            expected_type="readable JSON object",
            details="%s Fix or move that file first. This script will not "
                    "overwrite a settings file it could not read." % err,
            examples=EXAMPLES), file=sys.stderr)
        return 2

    voice, files = plan_install(args.scope)
    command = hook_command()

    print("scope:  %s" % root)
    print("voice:  %s" % (voice or "none active, baseline style only"))
    for path, _text in files:
        print("write:  %s" % path)
    print("hooks:  %s" % command)
    for spec in HOOK_SPECS:
        already = _find_group(
            (settings.get("hooks") or {}).get(spec["event"], []) or [],
            command) is not None
        print("        %s%s%s" % (spec["event"],
                                  " (%s)" % spec["matcher"] if spec["matcher"] else "",
                                  "  already installed" if already else ""))
    style_pick = (outputstyle.style_name(voice) if voice else "Rabbit Writes")
    print("set:    outputStyle = %r (was %r)"
          % (style_pick, settings.get("outputStyle")))
    print("record: %s" % sidecar_path(args.scope))

    if args.dry_run:
        print("")
        print("--dry-run, so nothing was written. Run again without it to apply.")
        return 0

    backup = backup_settings(settings_path)
    written = []
    for path, text in files:
        _write(path, text)
        written.append({"path": path, "sha256": _sha(text)})

    previous = settings.get("outputStyle")
    add_hooks(settings, command)
    settings["outputStyle"] = style_pick
    _write(settings_path, json.dumps(settings, indent=2) + "\n")

    side = read_sidecar(args.scope) or {}
    _write(sidecar_path(args.scope), json.dumps({
        "version": SIDECAR_VERSION,
        "scope": args.scope,
        "files": written,
        "hook_command": command,
        "settings_path": settings_path,
        "settings_backup": backup,
        # A second install must not record the style it set the first time as
        # "what was there before", which would make uninstall a no-op.
        "previous_output_style": side.get("previous_output_style", previous)
        if side else previous,
    }, indent=2) + "\n")

    print("")
    print("installed. Output styles load at session start, so run /clear or "
          "start a new session, then pick %r under Output style in /config."
          % style_pick)
    if backup:
        print("settings backed up to %s" % backup)
    return 0


def do_uninstall(args):
    root = scope_root(args.scope)
    settings_path = os.path.join(root, "settings.json")
    side = read_sidecar(args.scope)
    command = (side or {}).get("hook_command") or hook_command()

    if side is None:
        print("no %s, so falling back to matching the runner path. That "
              "fallback only identifies the hook command: any generated "
              "output-style files cannot be identified without the record "
              "and will be left in place. Remove them by hand from %s if "
              "you want them gone."
              % (SIDECAR_NAME, os.path.join(root, "output-styles")))

    settings, err = load_settings(settings_path)
    if err:
        print(cli_error.format_file_error(
            "install_host.py", settings_path, "--scope %s" % args.scope,
            expected_type="readable JSON object",
            details="%s Nothing was removed." % err,
            examples=EXAMPLES), file=sys.stderr)
        return 2

    edited = []
    for record in (side or {}).get("files", []):
        path = record.get("path")
        if not path or not os.path.exists(path):
            continue
        if _changed_since_written(path, record):
            edited.append(path)

    if edited and not args.force:
        print(cli_error.format_llm_error(
            "install_host.py",
            "Refused: %d file(s) written by --install have been edited since: "
            "%s. Those edits are yours and removing them is not this script's "
            "call. Pass --force to delete them anyway, or delete them by hand "
            "and run --uninstall again."
            % (len(edited), ", ".join(edited)),
            examples=EXAMPLES), file=sys.stderr)
        return 2

    print("scope:  %s" % root)
    removed_files = []
    for record in (side or {}).get("files", []):
        path = record.get("path")
        if path and os.path.exists(path):
            print("delete: %s" % path)
            removed_files.append(path)
    hook_count = _count_hooks(settings, command)
    print("hooks:  %d entry(s) naming %s" % (hook_count, command))
    previous = (side or {}).get("previous_output_style")
    print("set:    outputStyle -> %r" % previous)

    if args.dry_run:
        print("")
        print("--dry-run, so nothing was removed.")
        return 0

    backup_settings(settings_path)
    for path in removed_files:
        os.unlink(path)
        # An empty output-styles/ left behind reads as an install to anybody
        # who opens the directory later. Only ours, and only if it is empty.
        parent = os.path.dirname(path)
        if os.path.basename(parent) == "output-styles" and not os.listdir(parent):
            os.rmdir(parent)
    remove_hooks(settings, command)
    if previous is None:
        settings.pop("outputStyle", None)
    else:
        settings["outputStyle"] = previous
    if settings:
        _write(settings_path, json.dumps(settings, indent=2) + "\n")
    elif os.path.exists(settings_path):
        os.unlink(settings_path)
    if os.path.exists(sidecar_path(args.scope)):
        os.unlink(sidecar_path(args.scope))

    print("")
    if side is None:
        print("hooks and outputStyle removed. Output style files were left "
              "in place (see above). The change takes effect in a new "
              "session.")
    else:
        print("removed. The change takes effect in a new session.")
    return 0


def _count_hooks(settings, command):
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        return 0
    n = 0
    for groups in hooks.values():
        if not isinstance(groups, list):
            continue
        for group in groups:
            if not isinstance(group, dict):
                continue
            for hook in group.get("hooks", []) or []:
                if isinstance(hook, dict) and hook.get("command") == command:
                    n += 1
    return n


def main(argv=None):
    ap = cli_error.LLMArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        examples=EXAMPLES)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--status", action="store_true",
                      help="what is installed, where, and whether anything "
                           "has been edited since")
    mode.add_argument("--install", action="store_true",
                      help="write the output styles, add the hooks, and "
                           "record what was written")
    mode.add_argument("--uninstall", action="store_true",
                      help="remove exactly what --install wrote")
    ap.add_argument("--scope", choices=("user", "project"), default="user",
                    help="user writes ~/.claude, project writes .claude in "
                         "the working directory")
    ap.add_argument("--dry-run", action="store_true",
                    help="print every write and touch nothing")
    ap.add_argument("--force", action="store_true",
                    help="on --uninstall, delete style files that have been "
                         "edited since they were written")
    args = ap.parse_args(argv)

    if args.status:
        return do_status(args)
    if args.install:
        return do_install(args)
    return do_uninstall(args)


if __name__ == "__main__":
    sys.exit(main())
