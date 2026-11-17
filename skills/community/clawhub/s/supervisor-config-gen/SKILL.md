---
name: supervisor-config-gen
description: Bash tool that generates a Supervisor (supervisord) `[program:*]` config file from zero CLI flags — it derives everything from the current directory (program name = dirname, `command=<dir>/run.sh`, `directory=<dir>`, `user=$(whoami)`, logs under `$HOME/logs/supervisord/`) and writes `<dirname>-supervisor.conf` into that same directory, overwriting silently if present. Use when the user wants to generate a Supervisor program config for an app directory that has a `run.sh` entrypoint.
homepage: https://github.com/psyb0t/supervisor-config-gen
user-invocable: true
permissions:
  shell: bash script (runs `supervisor-config-gen` in the target app directory; no other commands executed)
  filesystem: writes a generated Supervisor `[program:*]` config file (`<dirname>-supervisor.conf`) to the current local directory; overwrites an existing file of that name without prompting
metadata:
  openclaw:
    emoji: "⚙️"
    requires:
      bins:
        - bash
---

# supervisor-config-gen — generate a Supervisor program config from a directory

supervisor-config-gen is a single bash script with **no flags, no args, no env vars**. Run it from inside an app directory and it emits a Supervisor `[program:x]` config for that app, inferring everything from the directory itself.

## Security & safety

- Generates a local plain-text config file. No network calls, no external services.
- The generated config controls **what Supervisor executes and as which user** — review the output before pointing supervisord at it, same as reviewing any generated shell/config artifact.
- It **overwrites** `<dirname>-supervisor.conf` in the current directory without prompting if one already exists. Don't run it in a directory where that file has manual edits you want to keep.
- The script does not sandbox or validate the target `run.sh` — it just references its path. Make sure `run.sh` is what you expect before Supervisor runs it.

## When to use

- The user wants a Supervisor program config for an app directory that has a `run.sh` entrypoint (a startup script Supervisor should manage).
- The user says "generate a supervisor config for this app" / "supervisorize this" / "make a supervisord conf".

## When NOT to use

- The app has no `run.sh` — the generated `command=` will point at a script that doesn't exist. Add/rename a `run.sh` entrypoint first, or hand-write the config.
- You need non-default supervisord settings (custom `numprocs`, environment vars, non-TERM stop signal, different log paths/rotation, etc.) — this tool has no flags to control those. Generate the base config, then hand-edit it.
- You need configs for multiple apps at once — the tool is single-directory, single-invocation.

## Inputs → output

There is nothing to pass in. The script derives every field from ambient state at run time:

| Field | Source |
|---|---|
| `program_name` (used in filename + `[program:x]`) | `basename $(pwd)` — the current directory's name |
| `command` | `$(pwd)/run.sh` — a `run.sh` is REQUIRED to exist in the current directory (the script doesn't check, it just hardcodes the path) |
| `directory` | `$(pwd)` |
| `user` | `$(whoami)` — the user invoking the script |
| `stdout_logfile` / `stderr_logfile` | `$HOME/logs/supervisord/<program_name>-{out,err}.log` |
| output path | `./<program_name>-supervisor.conf` (written in the current directory, overwritten if it exists) |

Everything else (`numprocs=1`, `stopsignal=TERM`, `stopwaitsecs=10`, `stopasgroup=true`, `killasgroup=true`, `autostart=true`, `autorestart=true`, `redirect_stderr=true`, `redirect_stdout=true`, 50MB log rotation with 10 backups on stdout) is fixed/hardcoded — not configurable via flags.

### Example invocation

Given an app directory `shitty-app/` containing `main.py` and `run.sh`:

```bash
cd shitty-app
supervisor-config-gen
# Generated shitty-app-supervisor.conf
```

Resulting `shitty-app-supervisor.conf` (paths reflect the actual invoking user/home/cwd):

```ini
[program:shitty-app]
command=/home/not-root/shitty-app/run.sh
directory=/home/not-root/shitty-app
process_name=%(program_name)s
numprocs=1
user=not-root

stopsignal=TERM
stopwaitsecs=10
stopasgroup=true

killasgroup=true

autostart=true
autorestart=true

redirect_stderr=true
redirect_stdout=true

stdout_logfile=/home/not-root/logs/supervisord/%(program_name)s-out.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=10
stderr_logfile=/home/not-root/logs/supervisord/%(program_name)s-err.log
stderr_logfile_maxbytes=50MB
```

For install steps and the full field reference, see `references/setup.md`.
