#!/usr/bin/env python3
"""Systemd Unit Generator — generate, validate, and lint systemd unit files."""

import sys
import os
import re
import json
from dataclasses import dataclass, field
from typing import Optional


# ── Unit file generation ────────────────────────────────────────────

HARDENING_OPTIONS = {
    'ProtectSystem': 'strict',
    'ProtectHome': 'yes',
    'PrivateTmp': 'yes',
    'NoNewPrivileges': 'yes',
    'ProtectKernelTunables': 'yes',
    'ProtectKernelModules': 'yes',
    'ProtectControlGroups': 'yes',
    'RestrictNamespaces': 'yes',
    'RestrictRealtime': 'yes',
    'MemoryDenyWriteExecute': 'yes',
    'SystemCallArchitectures': 'native',
    'CapabilityBoundingSet': '',
}

PRESETS = {
    'nodejs': {
        'type': 'simple',
        'restart': 'on-failure',
        'restart_sec': '5',
        'after': 'network.target',
        'env': {'NODE_ENV': 'production'},
        'harden': True,
        'description': 'Node.js Application',
    },
    'python': {
        'type': 'simple',
        'restart': 'on-failure',
        'restart_sec': '5',
        'after': 'network.target',
        'harden': True,
        'description': 'Python Application',
    },
    'docker': {
        'type': 'simple',
        'restart': 'always',
        'restart_sec': '10',
        'after': 'docker.service',
        'wants': 'docker.service',
        'exec_stop': '/usr/bin/docker-compose down',
        'description': 'Docker Compose Service',
    },
    'golang': {
        'type': 'simple',
        'restart': 'on-failure',
        'restart_sec': '5',
        'after': 'network.target',
        'harden': True,
        'description': 'Go Application',
    },
    'cron': {
        'type': 'oneshot',
        'restart': 'no',
        'after': 'network.target',
        'timer': True,
        'description': 'Scheduled Task',
    },
}


def generate_service(opts: dict) -> str:
    lines = ['[Unit]']
    lines.append(f"Description={opts.get('description', opts.get('name', 'Service'))}")
    if opts.get('after'):
        lines.append(f"After={opts['after']}")
    if opts.get('wants'):
        lines.append(f"Wants={opts['wants']}")
    lines.append('')

    lines.append('[Service]')
    lines.append(f"Type={opts.get('type', 'simple')}")
    if opts.get('user'):
        lines.append(f"User={opts['user']}")
    if opts.get('group'):
        lines.append(f"Group={opts['group']}")
    if opts.get('workdir'):
        lines.append(f"WorkingDirectory={opts['workdir']}")

    # Environment
    envs = opts.get('env', {})
    if isinstance(envs, dict):
        for k, v in envs.items():
            lines.append(f"Environment={k}={v}")
    elif isinstance(envs, list):
        for e in envs:
            lines.append(f"Environment={e}")

    lines.append(f"ExecStart={opts.get('exec', '/usr/bin/echo hello')}")
    if opts.get('exec_stop'):
        lines.append(f"ExecStop={opts['exec_stop']}")
    if opts.get('exec_reload'):
        lines.append(f"ExecReload={opts['exec_reload']}")

    restart = opts.get('restart', 'on-failure')
    lines.append(f"Restart={restart}")
    if restart != 'no':
        lines.append(f"RestartSec={opts.get('restart_sec', '5')}")

    if opts.get('syslog_identifier'):
        lines.append(f"SyslogIdentifier={opts['syslog_identifier']}")
    else:
        lines.append(f"SyslogIdentifier={opts.get('name', 'service')}")

    lines.append('StandardOutput=journal')
    lines.append('StandardError=journal')

    # Hardening
    if opts.get('harden'):
        lines.append('')
        lines.append('# Security hardening')
        for key, val in HARDENING_OPTIONS.items():
            if val:
                lines.append(f"{key}={val}")
            else:
                lines.append(f"{key}=")
        if opts.get('workdir'):
            lines.append(f"ReadWritePaths={opts['workdir']}")

    # Resource limits
    if opts.get('memory_max'):
        lines.append(f"MemoryMax={opts['memory_max']}")
    if opts.get('cpu_quota'):
        lines.append(f"CPUQuota={opts['cpu_quota']}")

    lines.append('')
    lines.append('[Install]')
    lines.append('WantedBy=multi-user.target')
    lines.append('')

    return '\n'.join(lines)


def generate_timer(opts: dict) -> str:
    lines = ['[Unit]']
    lines.append(f"Description=Timer for {opts.get('name', 'task')}")
    lines.append('')

    lines.append('[Timer]')
    oncalendar = opts.get('oncalendar', 'daily')
    lines.append(f"OnCalendar={oncalendar}")
    if opts.get('persistent', True):
        lines.append('Persistent=true')
    if opts.get('accuracy_sec'):
        lines.append(f"AccuracySec={opts['accuracy_sec']}")
    else:
        lines.append('AccuracySec=1min')
    if opts.get('randomized_delay'):
        lines.append(f"RandomizedDelaySec={opts['randomized_delay']}")

    service = opts.get('service', f"{opts.get('name', 'task')}.service")
    lines.append(f"Unit={service}")
    lines.append('')

    lines.append('[Install]')
    lines.append('WantedBy=timers.target')
    lines.append('')

    return '\n'.join(lines)


def generate_socket(opts: dict) -> str:
    lines = ['[Unit]']
    lines.append(f"Description=Socket for {opts.get('name', 'service')}")
    lines.append('')

    lines.append('[Socket]')
    listen = opts.get('listen_stream', '8080')
    if listen.startswith('/'):
        lines.append(f"ListenStream={listen}")
    elif ':' in str(listen):
        lines.append(f"ListenStream={listen}")
    else:
        lines.append(f"ListenStream=0.0.0.0:{listen}")

    if opts.get('accept'):
        lines.append('Accept=yes')
    lines.append('NoDelay=yes')
    lines.append('')

    lines.append('[Install]')
    lines.append('WantedBy=sockets.target')
    lines.append('')

    return '\n'.join(lines)


# ── Validation ──────────────────────────────────────────────────────

@dataclass
class ValidationIssue:
    severity: str  # error, warning, info
    message: str
    line: int = 0
    fix: str = ""


VALID_SECTIONS = {'Unit', 'Service', 'Timer', 'Socket', 'Mount', 'Automount',
                  'Path', 'Slice', 'Scope', 'Install'}

COMMON_SERVICE_KEYS = {
    'Type', 'ExecStart', 'ExecStop', 'ExecReload', 'ExecStartPre', 'ExecStartPost',
    'ExecStopPost', 'User', 'Group', 'WorkingDirectory', 'Environment', 'EnvironmentFile',
    'Restart', 'RestartSec', 'TimeoutStartSec', 'TimeoutStopSec', 'TimeoutSec',
    'WatchdogSec', 'PIDFile', 'BusName', 'NotifyAccess', 'Sockets',
    'StandardOutput', 'StandardError', 'StandardInput', 'SyslogIdentifier',
    'SyslogFacility', 'SyslogLevel', 'SyslogLevelPrefix',
    'KillMode', 'KillSignal', 'SendSIGHUP', 'SendSIGKILL',
    'SuccessExitStatus', 'RestartPreventExitStatus', 'RestartForceExitStatus',
    'RootDirectory', 'RootImage', 'MountAPIVFS',
    'ProtectSystem', 'ProtectHome', 'PrivateTmp', 'PrivateDevices', 'PrivateNetwork',
    'PrivateUsers', 'ProtectKernelTunables', 'ProtectKernelModules', 'ProtectControlGroups',
    'NoNewPrivileges', 'RestrictNamespaces', 'RestrictRealtime', 'RestrictSUIDSGID',
    'MemoryDenyWriteExecute', 'SystemCallArchitectures', 'SystemCallFilter',
    'CapabilityBoundingSet', 'AmbientCapabilities', 'SecureBits',
    'ReadWritePaths', 'ReadOnlyPaths', 'InaccessiblePaths', 'TemporaryFileSystem',
    'MemoryMax', 'MemoryHigh', 'CPUQuota', 'TasksMax', 'LimitNOFILE', 'LimitNPROC',
    'Nice', 'OOMScoreAdjust', 'IOSchedulingClass', 'IOSchedulingPriority',
    'RuntimeDirectory', 'StateDirectory', 'CacheDirectory', 'LogsDirectory',
    'ConfigurationDirectory', 'RuntimeDirectoryMode',
    'RemainAfterExit', 'GuessMainPID',
}

VALID_RESTART = {'no', 'on-success', 'on-failure', 'on-abnormal', 'on-watchdog', 'on-abort', 'always'}
VALID_TYPE = {'simple', 'exec', 'forking', 'oneshot', 'dbus', 'notify', 'idle', 'notify-reload'}


def parse_unit_file(content: str) -> dict:
    """Parse a systemd unit file into sections."""
    sections = {}
    current = None
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#') or stripped.startswith(';'):
            continue
        m = re.match(r'^\[(\w+)\]$', stripped)
        if m:
            current = m.group(1)
            if current not in sections:
                sections[current] = []
            continue
        if current and '=' in stripped:
            key, _, value = stripped.partition('=')
            sections[current].append((key.strip(), value.strip(), i))
    return sections


def validate_unit(filepath: str) -> list:
    issues = []
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception as e:
        return [ValidationIssue('error', str(e))]

    sections = parse_unit_file(content)

    if not sections:
        issues.append(ValidationIssue('error', 'No sections found — not a valid unit file'))
        return issues

    # Check section names
    for sec in sections:
        if sec not in VALID_SECTIONS:
            issues.append(ValidationIssue('warning', f"Unknown section [{sec}]"))

    # Service-specific validation
    if 'Service' in sections:
        svc = {k: (v, ln) for k, v, ln in sections['Service']}

        # ExecStart required
        if 'ExecStart' not in svc:
            svc_type = svc.get('Type', ('simple', 0))[0]
            if svc_type != 'oneshot':
                issues.append(ValidationIssue('error', 'Missing ExecStart in [Service]'))

        # Type validation
        if 'Type' in svc:
            t, ln = svc['Type']
            if t not in VALID_TYPE:
                issues.append(ValidationIssue('error', f"Invalid Type={t}", ln,
                              f"Valid: {', '.join(sorted(VALID_TYPE))}"))

        # Restart validation
        if 'Restart' in svc:
            r, ln = svc['Restart']
            if r not in VALID_RESTART:
                issues.append(ValidationIssue('error', f"Invalid Restart={r}", ln,
                              f"Valid: {', '.join(sorted(VALID_RESTART))}"))

        # PIDFile with non-forking
        if 'PIDFile' in svc:
            t = svc.get('Type', ('simple', 0))[0]
            if t != 'forking':
                issues.append(ValidationIssue('warning',
                    f"PIDFile set but Type={t} — PIDFile is mainly for Type=forking",
                    svc['PIDFile'][1]))

    # Timer-specific validation
    if 'Timer' in sections:
        timer = {k: (v, ln) for k, v, ln in sections['Timer']}
        has_trigger = any(k in timer for k in
            ('OnCalendar', 'OnBootSec', 'OnStartupSec', 'OnUnitActiveSec',
             'OnUnitInactiveSec', 'OnActiveSec'))
        if not has_trigger:
            issues.append(ValidationIssue('error', 'Timer has no trigger (OnCalendar, OnBootSec, etc.)'))

    # Install section check
    if 'Install' not in sections:
        issues.append(ValidationIssue('info', 'No [Install] section — unit cannot be enabled'))

    return issues


# ── Lint ────────────────────────────────────────────────────────────

def lint_unit(filepath: str) -> list:
    issues = validate_unit(filepath)

    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception:
        return issues

    sections = parse_unit_file(content)

    if 'Service' in sections:
        svc = {k: (v, ln) for k, v, ln in sections['Service']}

        # No hardening
        hardening_keys = {'ProtectSystem', 'ProtectHome', 'PrivateTmp', 'NoNewPrivileges',
                          'CapabilityBoundingSet', 'SystemCallFilter', 'RestrictNamespaces'}
        found_hardening = hardening_keys.intersection(svc.keys())
        if not found_hardening:
            issues.append(ValidationIssue('warning',
                'No security hardening directives — consider adding ProtectSystem, NoNewPrivileges, etc.',
                fix='Use --harden flag when generating'))

        # No Description
        if 'Unit' in sections:
            unit = {k: (v, ln) for k, v, ln in sections['Unit']}
            if 'Description' not in unit:
                issues.append(ValidationIssue('info', 'No Description in [Unit]'))

        # Restart without RestartSec
        if 'Restart' in svc and svc['Restart'][0] not in ('no',):
            if 'RestartSec' not in svc:
                issues.append(ValidationIssue('info',
                    'Restart set but no RestartSec — default is 100ms, may cause rapid restarts',
                    fix='Add RestartSec=5 or appropriate value'))

        # ExecStart with relative path
        if 'ExecStart' in svc:
            cmd = svc['ExecStart'][0]
            # Strip exec prefixes
            clean_cmd = re.sub(r'^[-+!@:]*', '', cmd).strip()
            if clean_cmd and not clean_cmd.startswith('/') and not clean_cmd.startswith('$'):
                issues.append(ValidationIssue('warning',
                    f"ExecStart uses relative path: {clean_cmd[:50]} — should be absolute",
                    svc['ExecStart'][1],
                    'Use full path like /usr/bin/...'))

        # Running as root without hardening
        if 'User' not in svc and not found_hardening:
            issues.append(ValidationIssue('warning',
                'Service runs as root with no hardening — consider adding User= and security options'))

        # StandardOutput/StandardError check
        if 'StandardOutput' not in svc and 'StandardError' not in svc:
            issues.append(ValidationIssue('info',
                'No StandardOutput/StandardError — defaults to journal, which is fine'))

    return issues


# ── Output formatting ───────────────────────────────────────────────

def format_text_output(content: str, is_unit=True) -> str:
    return content


def format_json_output(issues: list) -> str:
    return json.dumps([{
        'severity': i.severity,
        'message': i.message,
        'line': i.line,
        'fix': i.fix
    } for i in issues], indent=2)


def format_issues_text(issues: list, filepath: str) -> str:
    if not issues:
        return f"✅ {filepath}: No issues found"

    lines = [f"\n📄 {filepath}", "─" * 60]
    for i in issues:
        icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}[i.severity]
        loc = f"line {i.line}" if i.line else "global"
        lines.append(f"  {icon} [{i.severity.upper()}] {i.message}")
        if i.fix:
            lines.append(f"     Fix: {i.fix}")

    errors = sum(1 for i in issues if i.severity == 'error')
    warnings = sum(1 for i in issues if i.severity == 'warning')
    infos = sum(1 for i in issues if i.severity == 'info')
    lines.append(f"\n  {errors} errors, {warnings} warnings, {infos} info")
    return '\n'.join(lines)


# ── Main ────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print("Usage: systemd-unit-generator.py <command> [options]")
        print("\nCommands:")
        print("  service    Generate a .service unit file")
        print("  timer      Generate a .timer unit file")
        print("  socket     Generate a .socket unit file")
        print("  validate   Validate an existing unit file")
        print("  lint       Lint a unit file for best practices")
        print("  preset     Generate from a preset template")
        print("\nPresets: nodejs, python, docker, golang, cron")
        print("\nOptions:")
        print("  --name NAME          Service name")
        print("  --exec CMD           ExecStart command")
        print("  --user USER          Run as user")
        print("  --group GROUP        Run as group")
        print("  --workdir DIR        Working directory")
        print("  --env KEY=VAL        Environment variable (repeatable)")
        print("  --restart POLICY     Restart policy")
        print("  --type TYPE          Service type")
        print("  --harden             Apply security hardening")
        print("  --description DESC   Unit description")
        print("  --after UNIT         After dependency")
        print("  --wants UNIT         Wants dependency")
        print("  --oncalendar EXPR    Timer calendar expression")
        print("  --listen-stream ADDR Socket listen address")
        print("  --format text|json   Output format")
        print("  --output FILE        Write to file")
        sys.exit(0)

    command = args[0]

    # Parse options
    opts = {'env': {}}
    i = 1
    positional = None

    while i < len(args):
        a = args[i]
        if a == '--name' and i + 1 < len(args):
            opts['name'] = args[i + 1]; i += 2
        elif a == '--exec' and i + 1 < len(args):
            opts['exec'] = args[i + 1]; i += 2
        elif a == '--user' and i + 1 < len(args):
            opts['user'] = args[i + 1]; i += 2
        elif a == '--group' and i + 1 < len(args):
            opts['group'] = args[i + 1]; i += 2
        elif a == '--workdir' and i + 1 < len(args):
            opts['workdir'] = args[i + 1]; i += 2
        elif a == '--env' and i + 1 < len(args):
            k, _, v = args[i + 1].partition('=')
            opts['env'][k] = v; i += 2
        elif a == '--restart' and i + 1 < len(args):
            opts['restart'] = args[i + 1]; i += 2
        elif a == '--type' and i + 1 < len(args):
            opts['type'] = args[i + 1]; i += 2
        elif a == '--harden':
            opts['harden'] = True; i += 1
        elif a == '--description' and i + 1 < len(args):
            opts['description'] = args[i + 1]; i += 2
        elif a == '--after' and i + 1 < len(args):
            opts['after'] = args[i + 1]; i += 2
        elif a == '--wants' and i + 1 < len(args):
            opts['wants'] = args[i + 1]; i += 2
        elif a == '--oncalendar' and i + 1 < len(args):
            opts['oncalendar'] = args[i + 1]; i += 2
        elif a == '--listen-stream' and i + 1 < len(args):
            opts['listen_stream'] = args[i + 1]; i += 2
        elif a == '--service' and i + 1 < len(args):
            opts['service'] = args[i + 1]; i += 2
        elif a == '--format' and i + 1 < len(args):
            opts['format'] = args[i + 1]; i += 2
        elif a == '--output' and i + 1 < len(args):
            opts['output'] = args[i + 1]; i += 2
        elif a == '--memory-max' and i + 1 < len(args):
            opts['memory_max'] = args[i + 1]; i += 2
        elif a == '--cpu-quota' and i + 1 < len(args):
            opts['cpu_quota'] = args[i + 1]; i += 2
        elif not a.startswith('--'):
            positional = a; i += 1
        else:
            i += 1

    fmt = opts.get('format', 'text')

    if command == 'service':
        output = generate_service(opts)
        if opts.get('output'):
            with open(opts['output'], 'w') as f:
                f.write(output)
            print(f"✅ Written to {opts['output']}")
        else:
            print(output)

    elif command == 'timer':
        output = generate_timer(opts)
        if opts.get('output'):
            with open(opts['output'], 'w') as f:
                f.write(output)
            print(f"✅ Written to {opts['output']}")
        else:
            print(output)

    elif command == 'socket':
        output = generate_socket(opts)
        if opts.get('output'):
            with open(opts['output'], 'w') as f:
                f.write(output)
            print(f"✅ Written to {opts['output']}")
        else:
            print(output)

    elif command == 'preset':
        preset_name = positional
        if not preset_name:
            print("Error: preset name required")
            print(f"Available: {', '.join(PRESETS.keys())}")
            sys.exit(2)
        if preset_name not in PRESETS:
            print(f"Unknown preset: {preset_name}")
            print(f"Available: {', '.join(PRESETS.keys())}")
            sys.exit(2)

        preset = PRESETS[preset_name].copy()
        # Merge user opts over preset
        for k, v in opts.items():
            if v and k != 'format' and k != 'output':
                preset[k] = v

        output = generate_service(preset)
        if preset.get('timer'):
            output += '\n# ── Timer unit ──\n\n'
            output += generate_timer(preset)

        if opts.get('output'):
            with open(opts['output'], 'w') as f:
                f.write(output)
            print(f"✅ Written to {opts['output']}")
        else:
            print(output)

    elif command == 'validate':
        filepath = positional
        if not filepath:
            print("Error: file path required")
            sys.exit(2)
        issues = validate_unit(filepath)
        if fmt == 'json':
            print(format_json_output(issues))
        else:
            print(format_issues_text(issues, filepath))
        if any(i.severity == 'error' for i in issues):
            sys.exit(1)

    elif command == 'lint':
        filepath = positional
        if not filepath:
            print("Error: file path required")
            sys.exit(2)
        issues = lint_unit(filepath)
        if fmt == 'json':
            print(format_json_output(issues))
        else:
            print(format_issues_text(issues, filepath))
        if any(i.severity == 'error' for i in issues):
            sys.exit(1)

    else:
        print(f"Unknown command: {command}")
        sys.exit(2)


if __name__ == '__main__':
    main()
