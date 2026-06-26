---
name: remote-node-ssh
description: >
  Run commands and transfer files between an OpenClaw gateway (VPS) and a paired local node
  via node protocol or SSH fallback. Covers transport selection, common exec patterns, file
  transfer, and disconnect recovery. Assumes the node is already paired. For setup, see
  `hybrid-gateway`.
requires:
  - ssh
  - scp
  - rsync
  - openclaw
homepage: https://github.com/kanso-agent/remote-node-ssh
license: MIT
---

# Remote Node Exec

Run commands on a paired OpenClaw node from your gateway. Node protocol when connected, SSH when not.

> **Setup:** Node must be paired first. See [`hybrid-gateway`](https://clawhub.ai/skills/hybrid-gateway).

## Required Tools

This skill expects the following on your gateway machine:
- `ssh`, `scp`, `rsync` — standard SSH tooling for fallback transport and file transfer
- `openclaw` CLI — for node protocol commands and node status checks

Your remote node needs an SSH server running and an OpenClaw node agent paired to your gateway.

## When to Use What

| Need | Transport |
|------|-----------|
| Run a command | `exec host=node` (node protocol) |
| Full shell env (brew, nvm, pyenv) | SSH with shell rc sourcing |
| Transfer files | SSH (`scp` / `rsync`) |
| Node disconnected | SSH |
| Long-running task | SSH + `nohup` or `tmux` |

## Node Protocol

Fastest path. Routes through the gateway — no SSH keys needed.

```tool
exec host=node command="uname -a"
```

**Caveat:** Minimal PATH. Use full binary paths for package-manager-installed tools:

```tool
exec host=node command="/opt/homebrew/bin/python3 --version"
```

## SSH Fallback

Use your SSH config alias (the hostname or alias you configured in your SSH config for the node).

```bash
ssh <node-alias> "whoami"
```

With full shell environment:

```bash
ssh <node-alias> "source ~/.profile 2>/dev/null; node --version"
```

## File Transfer (SSH only)

```bash
# To node
scp file.txt <node-alias>:/tmp/

# From node
scp <node-alias>:/tmp/result.txt ./

# Sync a directory
rsync -avz ./data/ <node-alias>:~/data/
```

## Check Node Status

```bash
openclaw nodes status
```

## Disconnect Recovery

1. Check: `openclaw nodes status`
2. If disconnected, verify the node is reachable via SSH: `ssh <node-alias> "echo ok"`
3. If reachable, restart the OpenClaw node service on the remote machine using its service manager
4. Verify: `openclaw nodes status`

## Constraints

- Node protocol: no file transfer, no TTY/interactive sessions, minimal PATH
- SSH: requires network reachability (LAN, Tailscale, or VPN)
- Long tasks: use SSH + `nohup`/`tmux` to avoid timeouts
