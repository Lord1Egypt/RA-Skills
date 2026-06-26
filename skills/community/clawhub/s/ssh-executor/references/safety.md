# SSH Executor Safety Notes

## Default posture

- **Read-only first.** Start with inspection commands (`hostname`, `uptime`, `df -h`, `journalctl -n 100`, `docker ps`).
- **Explicit confirmation before any mutation.** State-changing commands require the user to see and approve the exact command before `--confirm-dangerous` is passed.
- **Least-privilege SSH accounts.** Use a dedicated read-only or low-privilege SSH account for inspection when available. Only escalate to a privileged account for authorized mutation.
- The script's dangerous-command heuristic (`is_dangerous_command`) is a **best-effort pattern check**, not a guarantee. It can produce both false positives and (more critically) false negatives. An empty check does not mean the command is safe.
- Prefer SSH aliases and existing `~/.ssh/config` entries.
- Prefer private keys over passwords.
- Keep timeouts short unless the user clearly expects a long-running command.
- Let ssh config resolve host, user, port, and identity file when an alias already exists.

## Host-key policy

- Existing ssh config policy wins if you do not pass `--host-key-checking`.
- `yes`: best for known sensitive hosts with preloaded host keys.
- `accept-new`: acceptable for first contact on low-risk hosts when the user asked to connect.
- `no`: avoid unless the user explicitly understands the risk.

## Commands that always need confirmation

Ask the user before running any command that:
- modifies files, permissions, or ownership (`rm`, `mv`, `chmod`, `chown`, `tee`, `dd`, `truncate`, `sed -i`)
- restarts, stops, or disables services (`systemctl restart|stop|disable`, `service`, `initctl`)
- installs, removes, or upgrades packages (`apt`, `apt-get`, `dnf`, `yum`, `apk`, `pacman`, `dpkg`, `rpm`)
- reboots or shuts down the host (`reboot`, `shutdown`, `poweroff`)
- uses `sudo`
- deletes, rotates, or truncates data (`truncate`, `dd`, logrotate actions)
- changes containers, databases, firewalls, or network state (`docker rm|down|kill`, `kubectl delete`, `iptables`, `ufw`, `firewall-cmd`, `ip link set`, `ip addr add|del`, `nmcli`)
- writes to disk or pipes output to a file (`>`, `>>`, `| tee`, `dd`)
- executes code on the remote host that was not explicitly reviewed (`curl | bash`, `wget -O- | sh`, `eval`, `source`)

**When in doubt, treat the command as dangerous and ask for confirmation.**

The script returns a guardrail error (exit code 99) for commands matching the heuristic unless `--confirm-dangerous` is present.

## Credential hygiene

- **Use dedicated least-privilege SSH keys** for remote inspection. Create a separate key/alias with read-only permissions instead of reusing a full-access key.
- **Do not paste private keys or passwords into chat** under any circumstance.
- The script's JSON output intentionally **omits key paths, SSH config paths, and resolved identity file paths** to avoid leaking credential metadata to logs, chat, or memory files.
- If an SSH alias resolves to a privileged account by default, configure a separate alias for inspection or explicitly pass `--user` with a low-privilege user.
