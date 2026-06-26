---
name: systemd-unit-generator
description: Generate, validate, and lint systemd unit files (.service, .timer, .socket, .mount) with hardening and best practices.
version: 1.0.0
---

# Systemd Unit Generator

Generate systemd service, timer, socket, and mount unit files with security hardening.

## Commands

### Generate a service unit
```bash
python3 scripts/systemd-unit-generator.py service --name myapp --exec "/usr/bin/node /app/server.js" --user www-data
```

### Generate a timer unit
```bash
python3 scripts/systemd-unit-generator.py timer --name backup --oncalendar "daily" --service backup.service
```

### Generate a socket unit
```bash
python3 scripts/systemd-unit-generator.py socket --name myapp --listen-stream 8080
```

### Validate an existing unit file
```bash
python3 scripts/systemd-unit-generator.py validate /etc/systemd/system/myapp.service
```

### Lint a unit for best practices
```bash
python3 scripts/systemd-unit-generator.py lint /etc/systemd/system/myapp.service
```

### Use a preset template
```bash
python3 scripts/systemd-unit-generator.py preset nodejs --name myapp --exec "/usr/bin/node /app/server.js"
python3 scripts/systemd-unit-generator.py preset python --name myapi --exec "/app/venv/bin/gunicorn app:app"
python3 scripts/systemd-unit-generator.py preset docker --name webapp --exec "docker-compose up"
```

## Options

- `--name NAME` — Service name (required for generate)
- `--exec CMD` — ExecStart command
- `--user USER` — Run as user
- `--group GROUP` — Run as group
- `--workdir DIR` — Working directory
- `--env KEY=VAL` — Environment variable (repeatable)
- `--restart POLICY` — Restart policy (on-failure, always, no)
- `--type TYPE` — Service type (simple, forking, oneshot, notify)
- `--harden` — Apply security hardening (sandbox, resource limits)
- `--description DESC` — Unit description
- `--after UNIT` — After dependency
- `--wants UNIT` — Wants dependency
- `--oncalendar EXPR` — Timer calendar expression
- `--listen-stream ADDR` — Socket listen address/port
- `--format text|json` — Output format (default: text)
- `--output FILE` — Write to file instead of stdout

## Presets
- `nodejs` — Node.js app with auto-restart, logging, hardening
- `python` — Python/Gunicorn app with venv support
- `docker` — Docker Compose service
- `golang` — Go binary with minimal dependencies
- `cron` — Oneshot + timer for cron-like scheduling

## Security Hardening (--harden)
Adds: ProtectSystem, ProtectHome, PrivateTmp, NoNewPrivileges, CapabilityBoundingSet, SystemCallFilter, RestrictNamespaces, RestrictRealtime, MemoryDenyWriteExecute, ReadWritePaths

## Exit Codes
- 0: Success
- 1: Validation errors found
- 2: Invalid arguments
