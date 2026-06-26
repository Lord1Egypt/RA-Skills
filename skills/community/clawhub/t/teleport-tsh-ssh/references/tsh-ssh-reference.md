# tsh ssh reference (tbot identity oriented)

Source: https://goteleport.com/docs/reference/cli/tsh/#tsh-ssh

## Purpose

Use `tsh ssh` to open SSH sessions or run commands on Teleport-managed nodes using short-lived certs from a Machine ID identity file.

## Required pattern for this skill

Always include identity file explicitly, and include proxy when available:

```bash
tsh -i <identity-file> --proxy=<proxy> ssh <host>
tsh -i <identity-file> --proxy=<proxy> ssh <host> -- <command> [args...]
```

Default identity file path:

- `~/.openclaw/workspace/tbot/identity`

Proxy precedence:

1. `TELEPORT_PROXY` env var
2. `~/.openclaw/workspace/tbot/proxy` saved value
3. Prompt user, then save to proxy file

## Identity file format hints

A typical Teleport Machine ID identity bundle includes:

- PEM private key block (`BEGIN PRIVATE KEY`)
- OpenSSH user certificate line (`*-cert-v01@openssh.com ...`)
- One or more PEM certificates (`BEGIN CERTIFICATE`)
- Optional known_hosts / cert-authority lines

## Practical flags

- `-i, --identity`: select identity file (required by this skill)
- `-l, --login`: remote Unix user
- `--proxy`: explicit Teleport proxy
- `--debug`: verbose troubleshooting logs

## Related commands

```bash
tsh -i <identity-file> --proxy=<proxy> status
tsh -i <identity-file> --proxy=<proxy> ls
tsh -i <identity-file> --proxy=<proxy> scp <local_path> <host>:<remote_path>
tsh -i <identity-file> --proxy=<proxy> scp <host>:<remote_path> <local_path>
tsh clusters
```

## Error mapping

- `not logged in` / expired creds: Machine ID material stale; verify tbot refresh and file freshness.
- `access denied`: role/login mismatch or host policy mismatch.
- `node not found`: wrong host/cluster context.
- `bad permissions` / read failures: adjust file perms and ownership.

## Automation notes

- Prefer non-interactive execution for agent flows.
- Preserve stderr for useful Teleport diagnostics.
- Avoid `--insecure` unless explicitly requested.
