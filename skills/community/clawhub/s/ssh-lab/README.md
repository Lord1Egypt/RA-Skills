# ssh-lab

Remote server SSH workbench for managing GPU training servers. Provides structured data collection (GPU/disk/process probes), declarative alerting, and side-by-side comparison — all through a zero-dependency CLI.

Built for AI agents: structured JSON output, semantic exit codes, heartbeat mode for cron/polling.

## Install

```bash
git clone <repo-url> && cd ssh-lab
npm install && npm run build
```

Requires: Node.js 18+, native `ssh` client.

## Quick Start

```bash
# List all SSH hosts (reads ~/.ssh/config automatically)
ssh-lab hosts

# GPU/disk/process status for all servers
ssh-lab status all

# Run a command on a specific server
ssh-lab run GMI4 "nvidia-smi"

# Compare two servers side-by-side
ssh-lab compare GMI4 GMI5

# Check if a server is healthy
ssh-lab doctor GMI4

# Set up alerts
ssh-lab alert add gpu_idle all
ssh-lab alert add process_died GMI4 --process-pattern "train.py"
ssh-lab alert add disk_full all --threshold 85

# Check alerts (exit code: 0=ok, 1=warn, 2=critical)
ssh-lab alert check all --quiet
```

## Commands

| Command | Description |
|---------|-------------|
| `hosts` | List all configured servers |
| `status [host\|all]` | GPU + disk + process overview |
| `run <host\|all> <cmd>` | Execute command on remote host(s) |
| `tail <host> <path>` | Tail a remote log file |
| `ls <host> <path>` | List remote directory |
| `df <host\|all> [path]` | Disk usage details |
| `sync <host> <src> <dst>` | rsync file transfer |
| `watch <host> <path>` | Snapshot file state for polling |
| `compare <hosts\|all>` | Side-by-side host comparison |
| `doctor <host>` | Connectivity & health diagnostics |
| `alert add\|list\|check\|remove` | Declarative alert rules |
| `add <name> <user@host>` | Add a custom host |

## Output Modes

All commands support `--json`, `--raw`, or default summary output.

```bash
ssh-lab status GMI4 --json    # Structured JSON
ssh-lab status all --raw      # Raw probe output
ssh-lab status all             # Human-readable summary
```

## Alert Types

| Type | Detects |
|------|---------|
| `gpu_idle` | GPUs idle but VRAM loaded |
| `disk_full` | Disk usage above threshold |
| `process_died` | Expected process not running |
| `ssh_unreachable` | Host not reachable |
| `oom_detected` | OOM events in dmesg |
| `high_temp` | GPU temperature too high |

## Architecture

- **Zero npm runtime dependencies** — only TypeScript + @types/node as devDeps
- **Probe system** — pluggable probes (gpu, disk, process) parse remote command output into structured data
- **SSH ControlMaster** — persistent connections with auto-cleanup
- **Retry + backoff** — transient SSH failures retried automatically
- **Error classification** — AUTH_FAILED / TIMEOUT / HOST_UNREACHABLE / etc. with hints
- **Parallel execution** — `status all`, `run all`, `compare` query hosts concurrently

## Agent Integration

ssh-lab is designed to be called by AI agents:

- `--json` for structured data consumption
- `--heartbeat` / `--quiet` for cron/polling (only output on problems)
- Semantic exit codes (0=ok, 1=warn, 2=critical)
- Stateless design — no daemon, agent drives the schedule

## Config

- SSH hosts: auto-discovered from `~/.ssh/config` via `ssh -G`
- Custom hosts: `~/.config/ssh-lab/config.json` (XDG-compliant)
- Alert rules: `~/.ssh-lab/alerts.json`
- Override config path: `SSH_LAB_CONFIG` env var

## License

MIT
