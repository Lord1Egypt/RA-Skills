#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///
"""
tmux-manager: Restore tmux sessions from a YAML config file.

Usage:
  tmux-manager (--all | -s SESSION [...] | --session-group GROUP [...] [--window-group GROUP [...]] | --window-group GROUP [...]) [--kill | --restart] [--dry-run] [--list] [--config FILE]
  tmux-manager --send-keys -s SESSION[:WINDOW] COMMAND
  tmux-manager --tail -s SESSION[:WINDOW]
  tmux-manager --validate [--config FILE]
  tmux-manager --list-groups [--config FILE]

  --all                  Target all sessions in the config
  --session-group GROUP  Target sessions by session_group (repeatable, comma-separated) — all windows created
  --window-group GROUP   Target sessions by window_group (repeatable, comma-separated) — only matching windows created
  -s SESSION             Target specific session(s) by name (repeatable)
  --kill                 Kill targeted sessions instead of creating them
  --restart              Kill then recreate targeted sessions
  --dry-run              Show what would happen without making any changes
  --list                 List targeted sessions and their status (no changes made)
  --send-keys COMMAND    Send a command to a single session or window
  --tail                 Stream live output from the active pane (Ctrl+C to stop)
  --validate             Validate the config file for errors
  --list-groups          List all session and window groups (no selector needed)
  --config FILE          Path to config file

  SESSION[:WINDOW]       For --tail, optionally target a specific window
                         e.g. my-session:claude

Native tmux equivalents (no wrapper needed):
  tmux kill-server                          # kill ALL tmux sessions
  tmux capture-pane -p -t SESSION[:WINDOW]  # snapshot active pane output

Examples:
  tmux-manager --all                                    # create all sessions
  tmux-manager --all --kill                             # kill all sessions in config
  tmux-manager --all --restart                          # restart all sessions
  tmux-manager --all --dry-run                          # preview what would be created
  tmux-manager --all --list                             # list status of all sessions
  tmux-manager --session-group work                     # create sessions in session-group 'work'
  tmux-manager --session-group work --restart           # restart sessions in session-group 'work'
  tmux-manager --session-group work --list              # list status of sessions in session-group 'work'
  tmux-manager --kill --session-group work              # kill all sessions in session-group 'work'
  tmux-manager --window-group dev                       # create sessions but only 'dev' windows
  tmux-manager --window-group dev --restart             # restart with only 'dev' windows
  tmux-manager --window-group claude,gemini             # multiple groups, comma-separated
  tmux-manager --window-group claude --window-group gemini  # equivalent, repeatable flag
  tmux-manager --session-group TargetTracer,N8N --window-group claude,gemini  # combined: scoped sessions + filtered windows
  tmux-manager -s my-session                            # create only my-session
  tmux-manager --kill -s my-session                     # kill only my-session
  tmux-manager --restart -s my-session                  # restart only my-session
  tmux-manager --send-keys -s my-session "cmd"               # send to active window
  tmux-manager --send-keys -s my-session:claude "cmd"        # send to specific window
  tmux-manager --tail -s my-session                     # stream live pane output
  tmux-manager --validate                               # validate config file
  tmux-manager --list-groups                            # list all session and window groups
  tmux-manager --all --config ~/my-sessions.yaml        # use a specific config

Default config: tmux-sessions.yaml (same directory as this script)

--- Config reference ---

sessions:
  - name: my-project
    session_group: work         # string, or list: [work, ai] — for --session-group targeting
    working_dir: ~/Projects/my-project
    focus: editor               # window to focus after creation (optional)
    pre_hook: "docker compose up -d"   # shell command run before session is created
    pre_hook_fail: abort        # abort|warn (default: warn) — abort stops session creation
    post_hook: "echo done"             # shell command run after session is created
    env:
      MY_VAR: value
    windows:
      - name: editor
        window_group: dev       # string, or list: [dev, ai] — for --window-group targeting
        command: "nvim"         # use command OR panes, not both
        working_dir: ~/Projects/my-project   # overrides session working_dir
        env:
          EDITOR: nvim
      - name: dev
        window_group: dev
        panes:                  # optional: split the window into panes
          - command: "npm run dev"
          - command: "tail -f logs/app.log"
        layout: even-horizontal # tiled | even-horizontal | even-vertical | main-horizontal | main-vertical
"""

import subprocess
import sys
import os

import yaml


def run(cmd, check=True):
    return subprocess.run(cmd, check=check)


def session_exists(name):
    result = subprocess.run(["tmux", "has-session", "-t", name],
                            capture_output=True, check=False)
    return result.returncode == 0


def tmux_new_session(name, window_name, working_dir):
    run(["tmux", "new-session", "-d", "-s", name, "-n", window_name, "-c", working_dir])


def tmux_new_window(session, window_name, working_dir):
    run(["tmux", "new-window", "-d", "-t", f"{session}:", "-n", window_name, "-c", working_dir])


def tmux_send_keys(target, command):
    run(["tmux", "send-keys", "-t", target, command, "Enter"])


def resolve_path(path):
    return os.path.expanduser(str(path)) if path else os.path.expanduser("~")


def run_hook(hook_cmd, label):
    print(f"      [hook:{label}] {hook_cmd}")
    result = subprocess.run(hook_cmd, shell=True)
    if result.returncode != 0:
        print(f"      [!] {label} hook exited with code {result.returncode}")
    return result.returncode


def create_session(name, session_cfg, dry_run=False):
    session_dir = resolve_path(session_cfg.get("working_dir", "~"))
    session_env = session_cfg.get("env", {})
    windows = session_cfg.get("windows", [])
    focus = session_cfg.get("focus")
    pre_hook = session_cfg.get("pre_hook")
    pre_hook_fail = session_cfg.get("pre_hook_fail", "warn")
    post_hook = session_cfg.get("post_hook")

    if windows:
        first_win = windows[0]
        remaining_wins = windows[1:]
    else:
        first_win = session_cfg
        remaining_wins = []

    first_win_name = first_win.get("name", "main")
    first_win_dir = resolve_path(first_win.get("working_dir", session_dir))

    if dry_run:
        print(f"  [dry] would create {name}:{first_win_name}  ({first_win_dir})")
        for win_cfg in remaining_wins:
            win_name = win_cfg.get("name", "window")
            win_dir = resolve_path(win_cfg.get("working_dir", session_dir))
            print(f"        would add window {name}:{win_name}  ({win_dir})")
            if win_cfg.get("panes"):
                for p in win_cfg["panes"]:
                    print(f"          pane: {p.get('command', '(shell)')}")
        if pre_hook:
            print(f"        would run pre_hook:  {pre_hook}")
        if post_hook:
            print(f"        would run post_hook: {post_hook}")
        return

    # Pre-hook
    if pre_hook:
        rc = run_hook(pre_hook, "pre")
        if rc != 0 and pre_hook_fail == "abort":
            print(f"  [!] pre_hook failed — aborting session '{name}'.")
            return False

    # Create the session with the first window
    tmux_new_session(name, first_win_name, first_win_dir)
    print(f"  [+] {name}:{first_win_name}  ({first_win_dir})")

    # Apply session-level env vars
    for key, val in session_env.items():
        subprocess.run(["tmux", "setenv", "-t", name, key, str(val)], check=True)

    # Handle first window panes or command
    _setup_window(name, first_win_name, first_win, session_dir)

    # Create remaining windows
    for win_cfg in remaining_wins:
        win_name = win_cfg.get("name", "window")
        win_dir = resolve_path(win_cfg.get("working_dir", session_dir))
        tmux_new_window(name, win_name, win_dir)
        print(f"      {name}:{win_name}  ({win_dir})")
        _setup_window(name, win_name, win_cfg, session_dir)

    # Focus a specific window if requested
    if focus:
        subprocess.run(["tmux", "select-window", "-t", f"{name}:{focus}"], check=False)

    # Post-hook
    if post_hook:
        run_hook(post_hook, "post")

    return True


def _setup_window(session, win_name, win_cfg, session_dir):
    target = f"{session}:{win_name}"
    panes = win_cfg.get("panes", [])

    # Window-level env vars
    for key, val in win_cfg.get("env", {}).items():
        tmux_send_keys(target, f"export {key}={val!r}")

    if panes:
        # First pane uses the existing window pane
        first_pane = panes[0]
        if first_pane.get("command"):
            tmux_send_keys(f"{target}.0", first_pane["command"])

        # Split for remaining panes
        for pane_cfg in panes[1:]:
            pane_dir = resolve_path(pane_cfg.get("working_dir", session_dir))
            run(["tmux", "split-window", "-t", target, "-c", pane_dir])
            if pane_cfg.get("command"):
                tmux_send_keys(target, pane_cfg["command"])

        # Apply layout
        layout = win_cfg.get("layout", "even-horizontal")
        run(["tmux", "select-layout", "-t", target, layout])
    else:
        win_cmd = win_cfg.get("command")
        if win_cmd:
            tmux_send_keys(target, win_cmd)


def validate_config(config, config_path):
    errors = []
    warnings = []

    sessions = config.get("sessions", [])
    if not sessions:
        errors.append("No sessions defined.")

    seen_names = set()
    for i, s in enumerate(sessions):
        name = s.get("name")
        label = f"sessions[{i}]"

        if not name:
            errors.append(f"{label}: missing 'name' field.")
            continue

        label = f"session '{name}'"

        if name in seen_names:
            errors.append(f"{label}: duplicate session name.")
        seen_names.add(name)

        if s.get("group"):
            warnings.append(f"{label}: unknown field 'group' — did you mean 'session_group'?")

        for key in s:
            if key not in KNOWN_SESSION_KEYS:
                warnings.append(f"{label}: unknown field '{key}'.")

        working_dir = s.get("working_dir")
        if working_dir:
            resolved = resolve_path(working_dir)
            if not os.path.isdir(resolved):
                warnings.append(f"{label}: working_dir '{resolved}' does not exist.")

        pre_hook_fail = s.get("pre_hook_fail", "warn")
        if pre_hook_fail not in ("warn", "abort"):
            errors.append(f"{label}: pre_hook_fail must be 'warn' or 'abort', got '{pre_hook_fail}'.")

        windows = s.get("windows", [])
        win_names = [w.get("name") for w in windows if w.get("name")]

        focus = s.get("focus")
        if focus and windows and focus not in win_names:
            errors.append(f"{label}: focus '{focus}' does not match any window name.")

        seen_win_names = set()
        for j, w in enumerate(windows):
            win_name = w.get("name", f"window[{j}]")
            if win_name in seen_win_names:
                errors.append(f"{label}, window '{win_name}': duplicate window name.")
            seen_win_names.add(win_name)

            if w.get("command") and w.get("panes"):
                warnings.append(f"{label}, window '{win_name}': both 'command' and 'panes' set — 'command' will be ignored.")

            if w.get("group"):
                warnings.append(f"{label}, window '{win_name}': unknown field 'group' — did you mean 'window_group'?")

            for key in w:
                if key not in KNOWN_WINDOW_KEYS:
                    warnings.append(f"{label}, window '{win_name}': unknown field '{key}'.")

            win_dir = w.get("working_dir")
            if win_dir:
                resolved = resolve_path(win_dir)
                if not os.path.isdir(resolved):
                    warnings.append(f"{label}, window '{win_name}': working_dir '{resolved}' does not exist.")

    print(f"Config: {config_path}\n")
    if not errors and not warnings:
        print("  Config is valid. No issues found.")
        return True

    for e in errors:
        print(f"  [error]   {e}")
    for w in warnings:
        print(f"  [warning] {w}")

    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).")
    return len(errors) == 0


KNOWN_SESSION_KEYS = {
    "name", "session_group", "working_dir", "focus",
    "pre_hook", "pre_hook_fail", "post_hook", "env", "windows", "command",
    "group",  # legacy — caught by specific warning
}
KNOWN_WINDOW_KEYS = {
    "name", "window_group", "working_dir", "command", "panes", "layout", "env",
    "group",  # legacy — caught by specific warning
}


def normalize_group(val):
    """Return val as a set — handles string, list, or None."""
    if not val:
        return set()
    if isinstance(val, list):
        return set(val)
    return {str(val)}


def filter_by_window_group(sessions, window_groups):
    """Return session configs filtered to only include windows in the given window_group(s)."""
    filtered = []
    for s in sessions:
        windows = s.get("windows", [])
        matching = [w for w in windows if normalize_group(w.get("window_group")) & window_groups]
        if not matching:
            continue
        modified = dict(s)
        modified["windows"] = matching
        filtered.append(modified)
    return filtered


def list_sessions(sessions, config_path):
    print(f"Config: {config_path}\n")
    rows = []
    for s in sessions:
        name = s.get("name", "")
        group = ", ".join(sorted(normalize_group(s.get("session_group")))) or "-"
        working_dir = resolve_path(s.get("working_dir", "~"))
        windows = s.get("windows", [])
        window_names = ", ".join(w.get("name", "?") for w in windows) if windows else name
        status = "running" if session_exists(name) else "stopped"
        rows.append((name, group, status, window_names, working_dir))

    col_headers = ("SESSION", "GROUP", "STATUS", "WINDOWS", "WORKING DIR")
    col_widths = [len(h) for h in col_headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(val))

    fmt = "  ".join(f"{{:<{w}}}" for w in col_widths)
    separator = "  ".join("-" * w for w in col_widths)
    print(fmt.format(*col_headers))
    print(separator)
    for row in rows:
        print(fmt.format(*row))
    print()


def list_groups(sessions, config_path):
    print(f"Config: {config_path}\n")

    session_groups = {}
    for s in sessions:
        for g in normalize_group(s.get("session_group")):
            session_groups.setdefault(g, []).append(s.get("name", "?"))
    ungrouped_sessions = [s.get("name", "?") for s in sessions if not normalize_group(s.get("session_group"))]

    window_groups = {}
    for s in sessions:
        for w in s.get("windows", []):
            for g in normalize_group(w.get("window_group")):
                label = f"{s.get('name', '?')}:{w.get('name', '?')}"
                window_groups.setdefault(g, []).append(label)

    print("Session groups (--session-group):")
    if session_groups:
        for g, names in sorted(session_groups.items()):
            print(f"  {g}  ({', '.join(names)})")
    else:
        print("  (none defined)")
    if ungrouped_sessions:
        print(f"  (ungrouped)  ({', '.join(ungrouped_sessions)})")

    print("\nWindow groups (--window-group):")
    if window_groups:
        for g, labels in sorted(window_groups.items()):
            print(f"  {g}  ({', '.join(labels)})")
    else:
        print("  (none defined)")
    print()


def restart_sessions(sessions, config_path, dry_run=False):
    print(f"Config: {config_path}\n")
    if not dry_run:
        subprocess.run(["tmux", "start-server"], check=True)
    for session_cfg in sessions:
        name = session_cfg.get("name")
        if not name:
            continue
        if dry_run:
            print(f"  [dry] would kill and recreate: {name}")
        else:
            if session_exists(name):
                subprocess.run(["tmux", "kill-session", "-t", name], check=True)
                print(f"  [-] {name} (killed)")
            create_session(name, session_cfg, dry_run=False)
    print(f"\nDone: {len(sessions)} restarted.")


def kill_sessions(sessions, config_path, dry_run=False):
    print(f"Config: {config_path}\n")
    killed = []
    skipped = []
    for session_cfg in sessions:
        name = session_cfg.get("name")
        if not name:
            continue
        if session_exists(name):
            if dry_run:
                print(f"  [dry] would kill: {name}")
            else:
                subprocess.run(["tmux", "kill-session", "-t", name], check=True)
                print(f"  [-] {name} (killed)")
            killed.append(name)
        else:
            print(f"  [~] {name} (not running, skipping)")
            skipped.append(name)
    action = "would kill" if dry_run else "killed"
    print(f"\nDone: {len(killed)} {action}, {len(skipped)} skipped.")


def tail_pane(target):
    """Stream live output from a pane via pipe-pane + tail -f."""
    import tempfile

    session_name = target.split(":")[0]
    if not session_exists(session_name):
        sys.exit(f"Error: session '{session_name}' is not running.")

    log_file = os.path.join(tempfile.gettempdir(), f"tmux-tail-{target.replace(':', '-')}.log")

    # Start piping pane output to log file
    subprocess.run(
        ["tmux", "pipe-pane", "-t", target, f"cat >> {log_file}"],
        check=True
    )
    print(f"Tailing output from '{target}'  (Ctrl+C to stop)\n{'-' * 50}")

    try:
        subprocess.run(["tail", "-f", log_file])
    except KeyboardInterrupt:
        pass
    finally:
        # Stop piping
        subprocess.run(["tmux", "pipe-pane", "-t", target], check=False)
        try:
            os.unlink(log_file)
        except OSError:
            pass
        print(f"\nStopped tailing '{target}'.")


def main():
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print(__doc__)
        sys.exit(0)

    kill_mode = "--kill" in args
    all_mode = "--all" in args
    list_mode = "--list" in args
    list_groups_mode = "--list-groups" in args
    restart_mode = "--restart" in args
    dry_run = "--dry-run" in args
    validate_mode = "--validate" in args
    send_keys_mode = "--send-keys" in args
    tail_mode = "--tail" in args
    args = [a for a in args if a not in ("--kill", "--all", "--list", "--list-groups",
            "--restart", "--dry-run", "--validate", "--send-keys", "--tail")]

    if kill_mode and restart_mode:
        sys.exit("Error: --kill and --restart are mutually exclusive.")

    # --tail and --send-keys take a raw SESSION[:WINDOW] target from -s
    if tail_mode or send_keys_mode:
        # Pull the raw -s value (may include :window suffix)
        raw_target = None
        send_command = None
        clean_args = []
        i = 0
        while i < len(args):
            if args[i] == "-s":
                if i + 1 >= len(args):
                    sys.exit("Error: -s requires a session target.")
                if raw_target is not None:
                    sys.exit("Error: --tail/--send-keys only support a single -s target.")
                raw_target = args[i + 1]
                i += 2
            elif send_keys_mode and send_command is None and not args[i].startswith("-"):
                send_command = args[i]
                i += 1
            else:
                clean_args.append(args[i])
                i += 1
        args = clean_args
        if not raw_target:
            sys.exit("Error: --tail/--send-keys require -s SESSION[:WINDOW].")
        if send_keys_mode:
            if not send_command:
                sys.exit("Error: --send-keys requires a command string.")
            session_name = raw_target.split(":")[0]
            if not session_exists(session_name):
                sys.exit(f"Error: session '{session_name}' is not running.")
            tmux_send_keys(raw_target, send_command)
            print(f"  [>] {raw_target}: sent '{send_command}'")
        else:
            tail_pane(raw_target)
        return

    # Parse -s SESSION, --session-group GROUP, --window-group GROUP, --config FILE
    filter_sessions = []
    filter_session_groups = []
    filter_window_groups = []
    config_override = None
    i = 0
    while i < len(args):
        if args[i] == "-s":
            if i + 1 >= len(args):
                sys.exit("Error: -s requires a session name argument.")
            filter_sessions.append(args[i + 1])
            i += 2
        elif args[i] == "--session-group":
            if i + 1 >= len(args):
                sys.exit("Error: --session-group requires a group name argument.")
            filter_session_groups.extend(g.strip() for g in args[i + 1].split(","))
            i += 2
        elif args[i] == "--window-group":
            if i + 1 >= len(args):
                sys.exit("Error: --window-group requires a group name argument.")
            filter_window_groups.extend(g.strip() for g in args[i + 1].split(","))
            i += 2
        elif args[i] == "--config":
            if i + 1 >= len(args):
                sys.exit("Error: --config requires a file path argument.")
            config_override = args[i + 1]
            i += 2
        else:
            sys.exit(f"Error: unexpected argument '{args[i]}'.")

    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = (config_override if config_override
                   else os.path.join(script_dir, "tmux-sessions.yaml"))

    if not os.path.exists(config_path):
        sys.exit(f"Config file not found: {config_path}")

    with open(config_path) as f:
        config = yaml.safe_load(f)

    if validate_mode:
        ok = validate_config(config, config_path)
        sys.exit(0 if ok else 1)

    if list_groups_mode:
        list_groups(config.get("sessions", []), config_path)
        return

    sessions = config.get("sessions", [])
    if not sessions:
        sys.exit("No sessions defined in config.")

    if not any([all_mode, filter_sessions, filter_session_groups, filter_window_groups]):
        sys.exit("Error: specify --all, --session-group GROUP, --window-group GROUP, or -s SESSION.")
    if all_mode and any([filter_sessions, filter_session_groups, filter_window_groups]):
        sys.exit("Error: --all cannot be combined with other selectors.")
    if filter_sessions and any([all_mode, filter_session_groups, filter_window_groups]):
        sys.exit("Error: -s cannot be combined with other selectors.")

    # Filter sessions by name or session-group (mutually exclusive with each other)
    if filter_sessions:
        unknown = [s for s in filter_sessions if s not in {c.get("name") for c in sessions}]
        if unknown:
            sys.exit(f"Error: unknown session(s): {', '.join(unknown)}")
        sessions = [c for c in sessions if c.get("name") in filter_sessions]
    elif filter_session_groups:
        known = {g for c in sessions for g in normalize_group(c.get("session_group"))}
        unknown = [g for g in filter_session_groups if g not in known]
        if unknown:
            sys.exit(f"Error: unknown session-group(s): {', '.join(unknown)}")
        target = set(filter_session_groups)
        sessions = [c for c in sessions if normalize_group(c.get("session_group")) & target]

    # Apply window-group filter on top of whatever sessions remain
    if filter_window_groups:
        sessions = filter_by_window_group(sessions, set(filter_window_groups))
        if not sessions:
            sys.exit(f"Error: no sessions found with window-group(s): {', '.join(filter_window_groups)}")

    if list_mode:
        list_sessions(sessions, config_path)
        return

    if restart_mode:
        restart_sessions(sessions, config_path, dry_run=dry_run)
        return

    if kill_mode:
        kill_sessions(sessions, config_path, dry_run=dry_run)
        return

    # Create mode
    if not dry_run:
        subprocess.run(["tmux", "start-server"], check=True)

    created = []
    skipped = []

    print(f"Config: {config_path}\n")

    for session_cfg in sessions:
        name = session_cfg.get("name")
        if not name:
            print("  [!] Skipping session with no name.")
            continue

        if not dry_run and session_exists(name):
            print(f"  [~] {name} (already exists, skipping)")
            skipped.append(name)
            continue

        if create_session(name, session_cfg, dry_run=dry_run):
            created.append(name)

    action = "would create" if dry_run else "created"
    print(f"\nDone: {len(created)} {action}, {len(skipped)} skipped.")
    if created and not dry_run:
        print(f"Sessions: {', '.join(created)}")


if __name__ == "__main__":
    main()
