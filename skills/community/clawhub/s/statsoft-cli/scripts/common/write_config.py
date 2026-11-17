#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Centralized fail-closed config persistence gate for statsoft-cli.

This is the SINGLE confirmation gate for every persistent write performed by
the statsoft-cli setup scripts. It is invoked by the per-tool setup_*.sh /
setup_*.py scripts after they have *detected* a tool and built the desired
config document.

Contract
--------
  argv[1] : absolute/relative path of the target config.json
  argv[2] : (optional) path to a temp file containing the desired config as JSON
            If argv[2] is omitted, the JSON is read from stdin.
  --consent : (optional) explicit, caller-supplied opt-in token. Callers pass
            this flag (instead of mutating the shared STATSOFT_AUTO_WRITE
            environment variable) to convey that the user already approved
            persistence for THIS invocation. This keeps authorization scoped to
            the child process and prevents a setup script from self-granting
            write permission by polluting the process environment.

Behaviour (fail-closed by default)
----------------------------------
  * Detection-only is the DEFAULT. Nothing is written unless an explicit
    opt-in is present.
  * Persist only when ONE of:
      - --consent flag passed on the command line (explicit caller opt-in)
      - STATSOFT_AUTO_WRITE=1            (non-interactive / agent contexts)
      - STATSOFT_CONFIRM=1 AND the session is interactive (a real TTY) AND the
        user answers 'y' at the prompt
  * This gate is the ONLY component that writes config.json. Callers MUST NOT
    set STATSOFT_AUTO_WRITE themselves; they pass --consent instead so the
    authorization decision is explicit and process-local.
  * When persisting: a timestamped backup (config.json.bak.yyyymmdd_hhmmss)
    is taken first, then the new file is written atomically via os.replace.
  * The caller is NEVER blocked: detection-only exits 0.

This module deliberately imports everything it needs and uses only variables
it defines itself, so it cannot suffer from the "undefined name" failures that
plagued the previous inline blocks.
"""
import os
import sys
import json
import shutil
import datetime


def _read_json(arg_path, from_stdin):
    if arg_path:
        try:
            with open(arg_path, "r", encoding="utf-8-sig") as fh:
                return fh.read()
        except Exception as exc:  # pragma: no cover - defensive
            sys.stderr.write("write_config.py: cannot read JSON file %s: %s\n" % (arg_path, exc))
            return None
    if from_stdin:
        return sys.stdin.read()
    return None


def main():
    # Explicit, caller-supplied consent (scoped to this child process only).
    # Callers pass --consent instead of mutating the shared STATSOFT_AUTO_WRITE
    # environment variable, so a setup script cannot self-grant authorization.
    consent_arg = "--consent" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--consent"]

    if len(args) < 1:
        sys.stderr.write("usage: write_config.py <config_path> [<json_file>] [--consent]\n")
        return 2

    target_path = args[0]

    # Single-path enforcement (SDI-1 / SDI-4): the ONLY acceptable write target
    # is the canonical config.json at the skill root. Compute it from this
    # file's location: scripts/common/write_config.py -> skill root = ../../
    # Any caller-supplied path that does not resolve to this canonical path is
    # rejected outright, so a buggy or malicious wrapper cannot redirect writes
    # to an arbitrary location or turn this helper into a generic file writer.
    _self_dir = os.path.dirname(os.path.abspath(__file__))
    # Skill root config.json (scripts/common -> ../..), AND the live windows-only
    # runtime config (scripts/common -> ../windows-only). Both live inside the skill
    # directory, so neither expands the writable surface; they only let the existing
    # windows-only setup_*.ps1 writers (which resolve "..\config.json" to
    # scripts/windows-only/config.json) reach their actual target instead of being
    # rejected. Pre-existing scripts/common scripts themselves persist to root.
    canonical_cfg = os.path.normpath(os.path.join(_self_dir, "..", "..", "config.json"))
    canonical_cfg_win = os.path.normpath(os.path.join(_self_dir, "..", "windows-only", "config.json"))
    target_abs = os.path.normpath(os.path.abspath(target_path))
    if target_abs != canonical_cfg and target_abs != canonical_cfg_win:
        sys.stderr.write(
            "write_config.py: target path rejected — persistence is restricted to the "
            "canonical config.json locations (%s or %s). Got: %s\n" % (canonical_cfg, canonical_cfg_win, target_path)
        )
        return 2
    json_src = _read_json(args[1] if len(args) > 1 else None,
                          from_stdin=(len(args) < 2))

    if not json_src or not json_src.strip():
        sys.stderr.write("write_config.py: empty config payload; nothing to persist.\n")
        return 2

    try:
        data = json.loads(json_src)
    except Exception as exc:
        sys.stderr.write("write_config.py: invalid JSON payload: %s\n" % exc)
        return 2

    auto_write = os.environ.get("STATSOFT_AUTO_WRITE") == "1"
    confirm_env = os.environ.get("STATSOFT_CONFIRM") == "1"

    go = False
    if consent_arg or auto_write:
        # Explicit caller-supplied consent (this invocation) OR an externally
        # set opt-in flag. The caller itself never sets STATSOFT_AUTO_WRITE.
        go = True
    elif confirm_env and sys.stdin.isatty():
        try:
            sys.stdout.write("Persist detected config to config.json? (y/N) ")
            sys.stdout.flush()
            ans = sys.stdin.readline().strip().lower()
            go = ans in ("y", "yes")
        except Exception:
            go = False

    if not go:
        print("Detection-only: config.json NOT modified. "
              "Set STATSOFT_AUTO_WRITE=1 to persist, or STATSOFT_CONFIRM=1 for an interactive prompt.")
        return 0

    # Only now — when actually persisting — create the parent directory, so that
    # detection-only mode never touches the filesystem (SDI-4 fix).
    parent_dir = os.path.dirname(os.path.abspath(target_path))
    if parent_dir and not os.path.isdir(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    # Persist with timestamped backup + atomic replace.
    if os.path.exists(target_path):
        bak = target_path + ".bak." + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(target_path, bak)
        print("Config backed up to: " + bak)

    tmp = target_path + ".tmp." + str(os.getpid())
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    os.replace(tmp, target_path)
    print("Config written to: " + target_path)

    # Dual-canonical mirror (B5 hardening): keep the sibling canonical config in
    # sync so readers (e.g. windows-only/statsoft-r.ps1, which resolves
    # "..\config.json") never see a stale copy after a write to the other one.
    for sib in (canonical_cfg, canonical_cfg_win):
        if sib != target_abs and os.path.exists(sib):
            sib_bak = sib + ".bak." + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy2(sib, sib_bak)
            sib_tmp = sib + ".tmp." + str(os.getpid())
            with open(sib_tmp, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2, ensure_ascii=False)
            os.replace(sib_tmp, sib)
            print("Config mirrored to: " + sib)
    return 0


if __name__ == "__main__":
    sys.exit(main())
