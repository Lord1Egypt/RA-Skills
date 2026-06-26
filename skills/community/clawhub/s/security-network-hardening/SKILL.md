---
name: security-network-hardening
description: Audit and harden an OpenClaw host and its network exposure. Use for security checks, hardening, firewall setup, network exposure review, metrics endpoint restriction, OpenClaw gateway security fixes, or step-by-step remediation on a Linux host running OpenClaw.
---

# Security + Network Hardening

Audit first, then harden with explicit approval. Keep this file short; read the references when needed.

## Core rules

- Start read-only unless the user explicitly asks for fixes.
- Require confirmation before any state-changing action.
- Preserve current management access; do not break SSH/RDP/VNC.
- Prefer exact findings over generic advice.
- After workspace edits, commit them.

## Read-only baseline

Run:

```bash
uname -a
cat /etc/os-release
id
ss -ltnup 2>/dev/null || ss -ltnp 2>/dev/null
openclaw security audit --deep
openclaw update status
openclaw status --deep
```

If firewall state matters, also run:

```bash
ufw status verbose || true
firewall-cmd --state 2>/dev/null || true
nft list ruleset 2>/dev/null || true
```

## Priorities

Check for these first:
1. elevated wildcard access in `tools.elevated.allowFrom.*`
2. writable credentials directories
3. missing gateway auth rate limiting
4. broad or unclear listening ports
5. metrics endpoints exposed too widely
6. ineffective custom `gateway.nodes.denyCommands`
7. workspace skill symlink escapes

## Fix patterns

Read these only when relevant:
- UFW/firewall workflow: `references/ufw-playbook.md`
- OpenClaw config fixes: `references/openclaw-fix-patterns.md`

## Artifact generation

When the user wants generated files, create:
- `firewall-rules.md`
- `apply-firewall.sh`
- `scripts/rollback-firewall.sh`
- `scripts/verify-firewall.sh`

## Safe firewall order

1. Confirm allowed source subnet/IPs.
2. Add SSH rule first if SSH is in use.
3. Apply LAN-only and single-host rules.
4. Verify from expected clients.
5. Re-check `ufw status verbose` and `ss -ltnp`.

## Verification

After fixes, verify with:

```bash
openclaw security audit --deep
openclaw gateway status
python3 -m json.tool ~/.openclaw/openclaw.json >/dev/null
sudo ufw status verbose
ss -ltnp
```

Success means:
- no critical audit findings
- no warning audit findings when practical
- gateway reachable
- required ports reachable only from approved sources
