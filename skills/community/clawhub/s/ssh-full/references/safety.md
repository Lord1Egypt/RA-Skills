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

- **Default is strict: `StrictHostKeyChecking=yes`.** Unknown hosts are rejected — the user must explicitly verify and accept the host key before connecting.
- `yes`: **default and only safe option** for most deployments. Requires the host key to be in `~/.ssh/known_hosts`.
- `no`: **do not use** unless the user explicitly understands and accepts the man-in-the-middle risk. Required only for ephemeral environments where host keys change frequently.
- Existing ssh config policy wins if you do not pass `--host-key-checking`, but the script's default is `yes` (strict) when no config entry exists.
- **`accept-new` has been removed.** It was a security antipattern — auto-trusting unknown hosts on first contact without fingerprint verification.

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
- **Stale temp key cleanup:** If `ssh-keys.sh restore` is interrupted by `kill -9`, temp key files at `/dev/shm/ssh-vault-*` or `/tmp/ssh-vault-*` may persist. Run `ssh-keys.sh cleanup` to list them and `ssh-keys.sh cleanup --force` to shred and remove.

## Sudo password handling

When `sudo` is required but `NOPASSWD` is not configured on the server:
- Store the sudo password in Vaultwarden as `sudo-<name>/sudo_password` (plain text field).
- Use `--sudo --sudo-pass-vault <name>` — the script resolves the password in RAM and pipes it to `sudo -S` via stdin.
- **Exposure is minimized, not eliminated:** the password never appears in chat, JSON stdout, `ps aux` argv, or on disk. However, it briefly exists in the shell's memory (`SUDO_PASS` variable) and the stdin pipe buffer. A core dump or `/proc/<pid>/environ` could theoretically expose it if the process is inspected at the right instant. For maximum safety, prefer `NOPASSWD` in sudoers.
- `--sudo` requires `--confirm-dangerous` for explicit user approval.

## stdout/stderr contract

All scripts follow a strict output contract for security and parseability:

| Stream | Content | Format |
|--------|---------|--------|
| **stdout** | Pure JSON result | `{"success": bool, "exit_code": int, "stdout": "...", "stderr": "...", ...}` |
| **stderr** | Status messages (vault, warnings, progress) | Free text |

- **Never** parse stdout without going through JSON — vault status messages on stdout indicate an outdated `ssh-keys.sh`.
- The `"command"` field in JSON always shows the **original** user command, even when wrapped with sudo/base64 internally.
- The `"sudo": true` field indicates privileged execution.
