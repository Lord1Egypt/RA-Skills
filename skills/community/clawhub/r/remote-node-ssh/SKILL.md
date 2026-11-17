---
name: remote-node-ssh
description: Run commands and transfer files between an OpenClaw Gateway (VPS) and a paired local node, using the node protocol when connected and least-privilege SSH when not. Covers transport selection, exec allowlists and approvals, file transfer with rsync preview, reconnect and reapproval recovery. Assumes the node is already paired via the hybrid-gateway skill.
metadata:
  openclaw:
    requires:
      bins:
        - ssh
        - scp
        - rsync
        - openclaw
    homepage: https://github.com/jkfaris94/remote-node-ssh
license: MIT
---

# Remote Node Exec

Run commands on a paired OpenClaw node from the Gateway. Node protocol when connected, SSH when not. Setup and the security contract live in [`hybrid-gateway`](https://github.com/jkfaris94/hybrid-gateway); this skill assumes Steps 1 to 5 there already pass.

## Required tools

On the Gateway: `openclaw`, `ssh`, `scp`, `rsync`. On the node: the OpenClaw node host service (paired) and, for the fallback only, an SSH server with a dedicated non-root user and key-only login.

## One-time SSH setup (after hybrid-gateway Steps 1 to 5 pass)

On the node: create a dedicated non-root user for the Gateway, allow key-only login for it, keep sshd on the Tailscale interface. On the Gateway:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_node -N ""
ssh-copy-id -i ~/.ssh/id_node.pub <node-user>@<node-tailscale-ip>   # compare the host-key fingerprint with the node's own `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub`
```

Add to `~/.ssh/config` on the Gateway:

```
Host <node-alias>
  HostName <node-tailscale-ip>
  User <node-user>
  IdentityFile ~/.ssh/id_node
  IdentitiesOnly yes
```

Never set `StrictHostKeyChecking no`, never reuse a personal key, never give the node user sudo. Test: `ssh <node-alias> -- true`.

## Which transport

| Need | Transport |
|---|---|
| Run an allowlisted command | `exec host=node` (node protocol) |
| Full login shell (brew, nvm, pyenv) | SSH |
| Transfer files | SSH (`scp` / `rsync`) |
| Node disconnected | SSH |
| Long-running task | not by default; see Constraints |

## Node protocol

Routes through the Gateway; no SSH keys involved. The node enforces its own allowlist (`security=allowlist, ask=on-miss`): an unlisted command raises an approval instead of running.

```tool
exec host=node command="/usr/bin/uname -a"
```

Use absolute paths. The node's PATH is fixed at service start (`openclaw nodes describe --node <name>` prints it), so package-manager tools need their full path:

```tool
exec host=node command="/opt/homebrew/bin/python3 --version"
```

Manage the allowlist from the Gateway, one binary per pattern, never a shell:

```bash
openclaw approvals get --node "<node-name>"
openclaw approvals allowlist add --agent main --node "<node-name>" "/opt/homebrew/bin/ollama"
openclaw approvals pending
```

Direct probe without an agent turn:

```bash
openclaw nodes invoke --node "<node-name>" --command system.which --params '{"bins":["node"]}' --json
```

## SSH fallback

Use the alias from the setup section. Test with a harmless command first:

```bash
ssh <node-alias> -- true
ssh <node-alias> "source ~/.profile 2>/dev/null; node --version"
```

Anything with JSON, quotes, or `$` goes in a script, not inline (zsh and bash quote differently):

```bash
ssh <node-alias> bash -s < job.sh
```

## File transfer (SSH only)

```bash
scp file.txt <node-alias>:/tmp/
scp <node-alias>:/tmp/result.txt ./
rsync -avn ./data/ <node-alias>:~/data/     # preview
rsync -av  ./data/ <node-alias>:~/data/     # apply after reading the preview
```

No `--delete` by default. Never disable host-key checking to make a transfer work.

## Check node status

```bash
openclaw nodes status
openclaw nodes describe --node "<node-name>"   # caps, commands, PATH, pending reapproval
```

## Disconnect recovery

1. `openclaw nodes status` on the Gateway.
2. If `paired · disconnected`: `ssh <node-alias> -- true`. Reachable means the node service died or the machine slept; unreachable means the route (Tailscale, Wi-Fi, power).
3. Reachable: `ssh <node-alias> "openclaw node restart"` (LaunchAgent on macOS, systemd user unit on Linux), then `openclaw nodes status`.
4. `reapproval pending` after an upgrade: `openclaw nodes describe` shows the new commands. Existing caps still work. Approve the exact id with `openclaw nodes approve <request-id>` only if the workflow needs the new surface.
5. `403 Proxy client attribution is required`: the Gateway's `gateway.trustedProxies` is wider than its real proxies. Follow the hybrid-gateway Step 1 guidance: keep only the same-host Serve proxy (`127.0.0.1`) and any reverse proxy you actually run, and never the Tailscale range.

## Constraints

- Node protocol: no file transfer, no TTY, fixed PATH, allowlist enforced on the node.
- SSH: needs a private route (Tailscale, LAN, VPN) and the least-privilege account from setup. Do not widen it to root or a shared key.
- Long tasks: detached or background work on the node is not the default. When a task outlives the invoke timeout, run it under an explicitly approved, supervised workflow with a named owner and a way to stop it; do not leave unattended processes behind.

## Tested with

OpenClaw 2026.9.3 Gateway (Ubuntu 24.04) and macOS 26 node.
