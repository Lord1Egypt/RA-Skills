#!/usr/bin/env python3
"""
Space Duck — Daemon supervisor for telegram_listener.py + workspace_bridge.py

INTENT: Make the listener (and optionally the bridge) survive host reboots
        so the MC consent UX stays "🟢 online" without manual intervention.
CALLS:  None directly. Generates + loads OS-native service units:
          - macOS: ~/Library/LaunchAgents/com.spaceduck.<svc>.plist + launchctl
          - linux: ~/.config/systemd/user/spaceduck-<svc>.service + systemctl --user
        Falls back to a clear error on other platforms — no silent install.
AUTH:   None — runs locally. Reads the same ~/.space-duck/config.json that
        the listener uses; supervision uses no platform endpoints.

Why this exists
---------------
Pre-0.3.8 the canonical setup was `nohup python3 telegram_listener.py
--owner-approval &`. Dies with the terminal. After reboot, owner has to
remember to restart by hand. Result: consent UX silently regresses, MC
flips to "🟡 offline", every bridge-control tap stalls.

What "supervision" means
------------------------
  - Auto-start on user login (laptop wake) or boot (Linux server).
  - Restart on crash. Cap at 5 restarts/15min to avoid crashloop.
  - Logs go to ~/.space-duck/logs/<svc>.log + .stderr.
  - One unit per service: "listener" (default) and "bridge" (optional).

CLI
---
    python3 install_service.py listener install
    python3 install_service.py listener status
    python3 install_service.py listener uninstall
    python3 install_service.py listener restart

    python3 install_service.py bridge install --workspace ~/.openclaw/workspace
    python3 install_service.py bridge status
    python3 install_service.py bridge uninstall

Exit codes
----------
    0 — success
    1 — runtime error (e.g. missing config, command failed)
    2 — unsupported platform
"""
import argparse
import os
import platform
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

HOME = Path.home()
SD_DIR = HOME / '.space-duck'
LOG_DIR = SD_DIR / 'logs'
SCRIPT_DIR = Path(__file__).resolve().parent
LISTENER_PATH = SCRIPT_DIR / 'telegram_listener.py'
BRIDGE_PATH = SCRIPT_DIR / 'workspace_bridge.py'

DARWIN_LAUNCHAGENTS = HOME / 'Library' / 'LaunchAgents'
LINUX_SYSTEMD_USER = HOME / '.config' / 'systemd' / 'user'

PYTHON = shutil.which('python3') or '/usr/bin/python3'


# ─────────────────────────── platform detection ─────────────────────────────

def _platform():
    p = platform.system().lower()
    if p == 'darwin':
        return 'darwin'
    if p == 'linux':
        return 'linux'
    return p  # other (windows, etc.) — unsupported


# ─────────────────────────── unit-file generation ───────────────────────────

def _darwin_label(svc):
    return f'com.spaceduck.{svc}'


def _darwin_plist(svc, exec_argv, logfile, errfile):
    label = _darwin_label(svc)
    args_xml = '\n'.join(f'    <string>{a}</string>' for a in exec_argv)
    return textwrap.dedent(f'''\
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
          "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
          <key>Label</key><string>{label}</string>
          <key>ProgramArguments</key><array>
        {args_xml}
          </array>
          <key>RunAtLoad</key><true/>
          <key>KeepAlive</key>
          <dict>
            <key>SuccessfulExit</key><false/>
          </dict>
          <key>ThrottleInterval</key><integer>30</integer>
          <key>StandardOutPath</key><string>{logfile}</string>
          <key>StandardErrorPath</key><string>{errfile}</string>
          <key>EnvironmentVariables</key>
          <dict>
            <key>PATH</key><string>/usr/local/bin:/usr/bin:/bin</string>
          </dict>
        </dict>
        </plist>
        ''')


def _linux_unit(svc, exec_argv, logfile, errfile):
    cmd = ' '.join(exec_argv)
    return textwrap.dedent(f'''\
        [Unit]
        Description=Space Duck {svc} (owner-approval consent UX)
        After=network-online.target

        [Service]
        Type=simple
        ExecStart={cmd}
        Restart=on-failure
        RestartSec=5
        StartLimitInterval=900
        StartLimitBurst=5
        StandardOutput=append:{logfile}
        StandardError=append:{errfile}

        [Install]
        WantedBy=default.target
        ''')


# ─────────────────────────── svc registry ───────────────────────────────────

def _listener_argv(args):
    argv = [PYTHON, str(LISTENER_PATH), '--owner-approval']
    if args.no_pulse: argv.append('--no-pulse')
    if args.strict_consent: argv.append('--strict-consent')
    if args.verbose: argv.append('--verbose')
    return argv


def _bridge_argv(args):
    argv = [PYTHON, str(BRIDGE_PATH), 'run']
    if args.workspace:
        argv += ['--workspace', str(Path(args.workspace).expanduser())]
    if args.bind:
        argv += ['--bind', args.bind]
    return argv


SERVICES = {
    'listener': {
        'argv_fn': _listener_argv,
        'log_name': 'listener',
    },
    'bridge': {
        'argv_fn': _bridge_argv,
        'log_name': 'bridge',
    },
}


# ─────────────────────────── install / uninstall / status ───────────────────

def _unit_path(svc, plat):
    if plat == 'darwin':
        return DARWIN_LAUNCHAGENTS / f'{_darwin_label(svc)}.plist'
    if plat == 'linux':
        return LINUX_SYSTEMD_USER / f'spaceduck-{svc}.service'
    return None


def _ensure_dirs():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    DARWIN_LAUNCHAGENTS.mkdir(parents=True, exist_ok=True)
    LINUX_SYSTEMD_USER.mkdir(parents=True, exist_ok=True)


def cmd_install(args):
    svc = args.service
    if svc not in SERVICES:
        print(f'error: unknown service {svc!r}', file=sys.stderr); return 1
    plat = _platform()
    if plat not in ('darwin', 'linux'):
        print(f'error: unsupported platform {plat!r} — install manually',
              file=sys.stderr); return 2
    _ensure_dirs()
    cfg = SERVICES[svc]
    argv = cfg['argv_fn'](args)
    logfile = str(LOG_DIR / f'{cfg["log_name"]}.log')
    errfile = str(LOG_DIR / f'{cfg["log_name"]}.stderr')
    unit_path = _unit_path(svc, plat)
    if plat == 'darwin':
        body = _darwin_plist(svc, argv, logfile, errfile)
    else:
        body = _linux_unit(svc, argv, logfile, errfile)
    unit_path.write_text(body)
    print(f'[install] wrote {unit_path}')
    # Load + start.
    if plat == 'darwin':
        label = _darwin_label(svc)
        # bootout first (idempotent uninstall) then bootstrap.
        subprocess.run(['launchctl', 'bootout', f'gui/{os.getuid()}/{label}'],
                       capture_output=True)
        r = subprocess.run(['launchctl', 'bootstrap', f'gui/{os.getuid()}',
                            str(unit_path)], capture_output=True, text=True)
        if r.returncode != 0:
            print(f'[install] launchctl bootstrap failed: {r.stderr}',
                  file=sys.stderr); return 1
        subprocess.run(['launchctl', 'enable', f'gui/{os.getuid()}/{label}'],
                       capture_output=True)
        print(f'[install] launchctl loaded {label} (RunAtLoad + KeepAlive)')
    else:
        subprocess.run(['systemctl', '--user', 'daemon-reload'],
                       capture_output=True)
        r = subprocess.run(['systemctl', '--user', 'enable', '--now',
                            f'spaceduck-{svc}.service'],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f'[install] systemctl enable --now failed: {r.stderr}',
                  file=sys.stderr); return 1
        print(f'[install] systemd-user spaceduck-{svc}.service enabled + '
              'started')
    print(f'[install] logs: {logfile} / {errfile}')
    return 0


def cmd_uninstall(args):
    svc = args.service
    plat = _platform()
    unit_path = _unit_path(svc, plat)
    if unit_path is None:
        print(f'unsupported platform {plat!r}', file=sys.stderr); return 2
    if plat == 'darwin':
        label = _darwin_label(svc)
        subprocess.run(['launchctl', 'bootout', f'gui/{os.getuid()}/{label}'],
                       capture_output=True)
    else:
        subprocess.run(['systemctl', '--user', 'disable', '--now',
                        f'spaceduck-{svc}.service'], capture_output=True)
    if unit_path.exists():
        unit_path.unlink()
        print(f'[uninstall] removed {unit_path}')
    else:
        print(f'[uninstall] no unit at {unit_path} — nothing to do')
    return 0


def cmd_status(args):
    svc = args.service
    plat = _platform()
    unit_path = _unit_path(svc, plat)
    print(f'platform = {plat}')
    print(f'unit_path = {unit_path}')
    print(f'unit_present = {unit_path.exists() if unit_path else False}')
    if plat == 'darwin':
        label = _darwin_label(svc)
        r = subprocess.run(['launchctl', 'print',
                            f'gui/{os.getuid()}/{label}'],
                           capture_output=True, text=True)
        if r.returncode == 0:
            for line in r.stdout.splitlines():
                if any(k in line for k in ('state', 'pid', 'last exit')):
                    print(f'  {line.strip()}')
        else:
            print('  (not loaded)')
    elif plat == 'linux':
        r = subprocess.run(['systemctl', '--user', 'status',
                            f'spaceduck-{svc}.service'],
                           capture_output=True, text=True)
        print(r.stdout[:600] or r.stderr[:600])
    print(f'logs: {LOG_DIR / (SERVICES[svc]["log_name"] + ".log")}')
    return 0


def cmd_restart(args):
    cmd_uninstall(args)
    return cmd_install(args)


# ─────────────────────────── CLI plumbing ───────────────────────────────────

def main(argv=None):
    ap = argparse.ArgumentParser(prog='install_service',
        description='Install/manage Space Duck daemons via launchd/systemd.')
    ap.add_argument('service', choices=list(SERVICES.keys()),
                    help='which daemon')
    ap.add_argument('action', choices=['install', 'uninstall', 'status',
                                       'restart'])
    # Listener flags (forwarded into the unit's ExecStart):
    ap.add_argument('--no-pulse', action='store_true',
                    help='listener: disable self-pulse')
    ap.add_argument('--strict-consent', action='store_true',
                    help='listener: require tap for read-only actions too')
    ap.add_argument('--verbose', action='store_true',
                    help='listener: verbose stderr logging')
    # Bridge flags:
    ap.add_argument('--workspace', help='bridge: workspace dir')
    ap.add_argument('--bind', default='0.0.0.0:8086',
                    help='bridge: bind addr')
    args = ap.parse_args(argv)
    dispatch = {
        'install': cmd_install, 'uninstall': cmd_uninstall,
        'status': cmd_status, 'restart': cmd_restart,
    }
    return dispatch[args.action](args)


if __name__ == '__main__':
    sys.exit(main())
