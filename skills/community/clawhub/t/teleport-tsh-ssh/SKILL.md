---
name: teleport-tsh-ssh
description: Use Teleport tsh CLI with a Machine ID (tbot) identity file to SSH into Teleport-managed hosts or run remote commands through Teleport access controls. Trigger when asked to connect to a Teleport host, execute commands on Teleport nodes, or troubleshoot tsh access using a local tbot-refreshed identity. Complements the teleport-tbot-bootstrap skill for creating and persisting the local Machine ID identity source.
---

# teleport-tsh-ssh

Use this skill to access Teleport SSH nodes via `tsh` with an explicit identity file (`-i`) and persistent proxy selection.

Pair this with `teleport-tbot-bootstrap` to set up and persist the local Machine ID identity source.

## Compatibility

Tested against Teleport/tsh/tbot **18.7.0**.

## Identity policy (required)

Always pass `-i <identity-file>` to `tsh` commands.

Default identity path:

- `~/.openclaw/workspace/tbot/identity`

If the default does not exist, discover a workspace identity file and use the best match.

## Identity discovery fallback

When default identity is missing, search within workspace for candidate files named like:

- `identity`
- `*.identity`
- `tbot/identity`

Validate candidate format before use. A valid Teleport Machine ID identity file typically contains multiple blocks, such as:

- `-----BEGIN PRIVATE KEY-----`
- an OpenSSH user cert line (`*-cert-v01@openssh.com ...`)
- one or more `-----BEGIN CERTIFICATE-----` blocks

Pick the most likely current file (prefer paths under `tbot/`, then newest mtime).

## Security notes

- Never commit identity files, bot state directories, tokens, or registration secrets.
- Prefer explicit paths and least-privilege role mappings for automation identities.

## Known limitations (v1.0.0)

- Focuses on Teleport SSH node access (`tsh ssh`, `tsh ls`, `tsh scp`).
- Does not cover Teleport app/db/kubernetes access workflows.

## Proxy resolution (required)

Resolve proxy in this order:

1. If `TELEPORT_PROXY` is set, use it.
2. Else, read saved proxy from `~/.openclaw/workspace/tbot/proxy` (single-line text file) if present.
3. Else, prompt user for Teleport proxy address, then save it to `~/.openclaw/workspace/tbot/proxy` for future runs.

Always include proxy in commands when resolved:

- `tsh -i <identity> --proxy=<proxy> ...`

## Quick workflow

1. Confirm `tsh` is installed.
2. Resolve identity file path (default first, then fallback discovery).
3. If no valid identity file is found, prompt user to provide the identity file path.
4. Resolve proxy (`TELEPORT_PROXY` first, then saved proxy file, then prompt-and-save).
5. Check auth status when useful: `tsh -i <identity> --proxy=<proxy> status`.
6. Discover hosts if needed: `tsh -i <identity> --proxy=<proxy> ls`.
7. Connect/run command with explicit identity:
   - `tsh -i <identity> --proxy=<proxy> ssh <host>`
   - `tsh -i <identity> --proxy=<proxy> ssh <host> -- <command> [args...]`
8. Return concise result + actionable error details.

## Command patterns

- Interactive shell:
  - `tsh -i <identity> --proxy=<proxy> ssh <host>`
- Remote command execution:
  - `tsh -i <identity> --proxy=<proxy> ssh <host> -- <command> [args...]`
- Set remote login user:
  - `tsh -i <identity> --proxy=<proxy> ssh <login>@<host>`
  - or `tsh -i <identity> --proxy=<proxy> ssh --login=<login> <host>`
- List available nodes:
  - `tsh -i <identity> --proxy=<proxy> ls`

If user asks what nodes are available, run `tsh ls` with identity+proxy and report back.

Prefer non-interactive form when user asks for command output.

## File copy with Teleport SCP

Use `tsh scp` with identity+proxy for file transfer. Syntax mirrors OpenSSH `scp`.

- Local → remote:
  - `tsh -i <identity> --proxy=<proxy> scp <local_path> <host>:<remote_path>`
- Remote → local:
  - `tsh -i <identity> --proxy=<proxy> scp <host>:<remote_path> <local_path>`

## Troubleshooting checklist

- `tsh: command not found` → install Teleport client.
- Identity file missing/unreadable → resolve fallback file; if none found, ask user for path.
- Missing proxy → ask user for proxy, save to `~/.openclaw/workspace/tbot/proxy`, retry.
- `not logged in` / cert expired → refresh Machine ID output (tbot service health).
- `access denied` → role/login mismatch; verify host and identity origin.
- `host not found` → verify with `tsh -i <identity> --proxy=<proxy> ls` and cluster/proxy context.

## Clawhub listing copy

### Clawhub short description

Use `tsh` with explicit Machine ID identity (`-i`) for Teleport SSH, remote commands, node listing, and `tsh scp`.

### Companion skill

Use with `teleport-tbot-bootstrap` to create and persist the local Machine ID identity source.

### Clawhub long description

Standardize Teleport server access with identity-first command patterns.
Enforce explicit identity usage, resolve proxy consistently, support host discovery, command execution, and file transfer with practical troubleshooting guidance.

## References

- `references/tsh-ssh-reference.md`
- https://goteleport.com/docs/reference/cli/tsh/#tsh-ssh
