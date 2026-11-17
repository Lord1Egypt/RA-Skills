# supervisor-config-gen — setup + full reference

## Install

Single script, no dependencies beyond bash. Default branch is `master` (no tags exist yet — pull from `master`, not a version tag).

Download and run from any directory:

```shell
wget -qO- https://raw.githubusercontent.com/psyb0t/supervisor-config-gen/master/supervisor-config-gen > supervisor-config-gen
chmod +x supervisor-config-gen
```

### Install for all users (requires root)

```shell
sudo mv supervisor-config-gen /usr/local/bin/
```

### Install for the current user only

```shell
mkdir -p ~/bin
mv supervisor-config-gen ~/bin/
```

Then make sure `$HOME/bin` is on `$PATH`:

```shell
echo $PATH | grep -q "$HOME/bin" && echo "already in PATH" || echo "not in PATH yet"
```

If not in `$PATH`, add it (bash: `~/.bashrc`, zsh: `~/.zshrc`):

```shell
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Prerequisites

- Bash shell on the machine running the script.
- The target app directory MUST contain a `run.sh` executable — the script hardcodes `command=<dir>/run.sh` into the generated config without checking it exists. If there's no `run.sh`, the generated config will reference a missing file and Supervisor will fail to start the program.

## Full input reference

**There are no CLI flags, positional args, or environment variables.** The script (`supervisor-config-gen`, a single bash file, no subcommands) takes zero input parameters. Every field in the generated config is derived from ambient invocation state:

| Config field | Derivation | Notes |
|---|---|---|
| `[program:<name>]` section name / `program_name` | `basename "$(pwd)"` | The name of the directory you're standing in when you run the script |
| `command` | `$(pwd)/run.sh` | Always assumes a `run.sh` in the current directory — no way to point at a different entrypoint |
| `directory` | `$(pwd)` | Absolute path of the current directory |
| `process_name` | `%(program_name)s` | Supervisor's own template var, passed through literally |
| `numprocs` | `1` | Hardcoded |
| `user` | `$(whoami)` | The OS user running the script becomes the Supervisor `user=` — no override |
| `stopsignal` | `TERM` | Hardcoded |
| `stopwaitsecs` | `10` | Hardcoded |
| `stopasgroup` | `true` | Hardcoded |
| `killasgroup` | `true` | Hardcoded |
| `autostart` | `true` | Hardcoded |
| `autorestart` | `true` | Hardcoded |
| `redirect_stderr` | `true` | Hardcoded |
| `redirect_stdout` | `true` | Hardcoded |
| `stdout_logfile` | `$HOME/logs/supervisord/%(program_name)s-out.log` | `$HOME` of the invoking user, NOT the app directory |
| `stdout_logfile_maxbytes` | `50MB` | Hardcoded |
| `stdout_logfile_backups` | `10` | Hardcoded |
| `stderr_logfile` | `$HOME/logs/supervisord/%(program_name)s-err.log` | Same `$HOME` base |
| `stderr_logfile_maxbytes` | `50MB` | Hardcoded |

No `stderr_logfile_backups` is set (only stdout gets an explicit backup count in the emitted config — matches the script's actual `heredoc`, don't add one that isn't there).

## Output location + overwrite behavior

- Output file: `<program_name>-supervisor.conf`, where `program_name` is the current directory's basename.
- Written to the **current working directory** (same directory the script is run from) — not to a Supervisor `conf.d` path, not to `/etc/supervisor/`. You move/symlink it into Supervisor's include path yourself.
- If a file with that name already exists, it is **silently overwritten** — the script does not prompt, back up, or diff. Re-running the tool in the same directory always regenerates from scratch.
- On success the script prints `Generated <program_name>-supervisor.conf` to stdout. On write failure (e.g. permission denied) the `Generated ...` line is skipped because the script chains write and echo with `&&`.

## Usage

```bash
cd <your-app-dir>   # must contain run.sh
supervisor-config-gen
# Generated <your-app-dir>-supervisor.conf
```
