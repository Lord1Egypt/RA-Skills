# ssh-lab — Remote Server SSH Workbench

> Structured SSH operations for managing remote GPU servers.
> Standardizes what's universal (GPU/disk/process), delegates interpretation to the LLM.

## When to Use

- User asks about GPU status, server health, remote processes
- Need to check if training is running, disk is full, GPU is idle
- Running commands on remote servers
- Tailing remote log files, listing checkpoints
- File transfer between local and remote (rsync)
- Comparing hosts side-by-side (GPU, disk, processes)
- Setting up alerts for GPU idle, disk full, process died
- Any mention of: `ssh-lab`, `gpu status`, `server status`, `nvidia-smi`, remote server

## Setup

```bash
cd /path/to/ssh-lab && npm run build
```

After building, use the CLI via any of:
```bash
ssh-lab status all          # if npm link'd or installed globally
npx ssh-lab status all      # via npx
node dist/cli.js status all # direct invocation
```

The CLI reads `~/.ssh/config` automatically — zero configuration needed for existing SSH hosts.

## Commands

### List hosts
```bash
ssh-lab hosts [--json]
```

### Server status (GPU + disk + process)
```bash
ssh-lab status [host|all] [--json] [--timeout ms] [--heartbeat] [--quiet]
```
Returns structured probe data: GPU utilization/VRAM/temp, disk usage, active processes.
Includes automatic alerts: GPU idle, disk full (>90%), high temp (>85°C).
`--heartbeat` gives compact one-liner output for agent integration. `--quiet` suppresses all-clear output (for cron).

### Run remote command
```bash
ssh-lab run <host|all> <command...> [--json] [--timeout ms]
```
Supports `all` for parallel execution across all hosts.

### Tail remote log
```bash
ssh-lab tail <host> <path> [-n lines] [--json]
```
Default: last 50 lines. Smart truncation at 50KB.

### List remote directory
```bash
ssh-lab ls <host> <path> [--sort time|size|name] [--json]
```
Lists files with size, date, permissions. Great for checkpoint directories.

### Disk usage
```bash
ssh-lab df <host|all> [path] [--json]
```
Shows disk usage for all filesystems. Optional path runs `du -sh` on a specific directory.

### File sync (rsync)
```bash
ssh-lab sync <host> <src> <dst> [--direction up|down] [--dry-run] [--exclude pat1,pat2]
```
Direction: `down` (remote→local, default), `up` (local→remote). Always use `--dry-run` first!

### Watch file (snapshot for polling)
```bash
ssh-lab watch <host> <path> [-n lines] [--prev-hash hash] [--json]
```
Captures file state + metadata. Returns `changed: true/false` when `--prev-hash` is provided.
Agent calls this repeatedly via cron/heartbeat — the tool itself is stateless.

### Compare hosts (side-by-side)
```bash
ssh-lab compare <host1> <host2> [--probes gpu,disk,process] [--json]
ssh-lab compare all [--probes gpu]
ssh-lab compare GMI4 GMI5 GMI6 --probes gpu,disk
```
Side-by-side comparison of GPU, disk, and process data across hosts.
Probes default to `gpu,disk,process`. Supports any number of hosts.
Uses bounded concurrency pool for parallel data collection.

### Doctor (diagnostics)
```bash
ssh-lab doctor <host> [--json] [--timeout ms]
```
Runs connectivity and health diagnostics on a host. Checks SSH reachability,
authentication, command execution, and basic system health.

### Alert management
```bash
# List configured rules
ssh-lab alert list [--json]

# Add a rule
ssh-lab alert add <kind> <host> [--threshold N] [--process-pattern regex]

# Remove a rule
ssh-lab alert remove <rule-id>

# Evaluate alerts against live status
ssh-lab alert check [host|all] [--json] [--quiet]
```

**Alert kinds**: `gpu_idle`, `disk_full`, `process_died`, `ssh_unreachable`, `oom_detected`, `high_temp`

**Examples**:
```bash
ssh-lab alert add disk_full all --threshold 90
ssh-lab alert add process_died GMI4 --process-pattern "torchrun|deepspeed"
ssh-lab alert check all --json
```

### Add custom host
```bash
ssh-lab add <name> <user@host> [--port N] [--tags a,b] [--notes "desc"]
```

## Output Modes

All commands support three output modes:
- **summary** (default): Human-readable text with formatting
- **json** (`--json` or `-j`): Structured JSON for programmatic use
- **raw** (`--raw` or `-r`): Raw command output only

## Timeout Tiers

Commands use per-type timeout defaults (user `--timeout` always overrides):
- **quick** (5s): `hosts`, `add`, `doctor` — connectivity checks
- **standard** (15s): `status`, `run`, `ls`, `df`, `alert`, `compare` — normal probes
- **stream** (30s): `tail`, `watch` — streaming/log tailing
- **transfer** (60s): `sync` — rsync bulk transfers

## Architecture

- **Probe system**: Pluggable probes (gpu, disk, process) collect structured data
- **SSH via child_process**: Uses native `ssh` — inherits user's config, keys, ProxyJump
- **ControlMaster reuse**: Persistent SSH connections via `/tmp/ssh-lab-%r@%h:%p` sockets; auto-cleanup detects stale sockets (`ssh -O check`), gracefully exits (`ssh -O exit`), then removes dead socket files before retry
- **Retry + error classification**: Transient failures retried with exponential backoff; errors classified (AUTH_FAILED/TIMEOUT/etc.) with hints
- **Tiered timeouts**: Per-command defaults — quick (5s) for doctor/add, standard (15s) for status/run/ls/df/compare/alert, stream (30s) for tail/watch, transfer (60s) for sync. `--timeout` always overrides
- **Parallel execution**: `status all` / `run all` queries all hosts concurrently via `withPool` (default: 5)
- **Alert system**: 6 built-in alert rules with configurable thresholds
- **Zero npm dependencies**: Only devDependencies (typescript, @types/node)
- **SSH config hosts use alias**: For hosts from `~/.ssh/config`, SSH alias is used directly so all ProxyJump/Match/Include rules are respected

## Heartbeat Integration

In HEARTBEAT.md:
```
- [ ] Run: ssh-lab status all --heartbeat
  Check for: GPU idle, disk >90%, processes died
- [ ] Run: ssh-lab alert check all --json
  Act on any critical firings
```

## Config

Custom hosts stored in `~/.config/ssh-lab/config.json` (auto-created, XDG-compliant).
SSH hosts from `~/.ssh/config` discovered automatically via `ssh -G`.
Override config path with `SSH_LAB_CONFIG` env var.
