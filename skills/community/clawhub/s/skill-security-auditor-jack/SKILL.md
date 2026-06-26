---
name: skill-security-auditor
description: "Audit third-party or custom skills for permission risk, unsafe commands, and integration safety. Use before: installing a new skill, enabling external scripts or repos, granting broad permissions, recurring security review. Triggered when any skill is about to be adopted into the OpenClaw system."
---

# Skill Security Auditor

Audit skills for supply-chain, privilege, and automation risk before adoption.

## Input

Required:
- `skill_manifest` — the skill's SKILL.md or metadata
- `source_location` — where the skill comes from (clawhub, git, local, unknown)
- `required_permissions` — what permissions the skill requests
- `shell_commands` — any shell/CLI commands referenced by the skill
- `env_usage` — environment variables the skill reads or writes
- `install_steps` — how the skill is installed / what it runs on install

## Output Schema

```
risk_level: "low" | "medium" | "high" | "critical"

suspicious_actions: {
  action: string
  location: string
  severity: "warning" | "critical"
  description: string
  recommendation: string
}[]

over_privileged_points: {
  permission: string
  why_needed: string | null
  why_excessive: string
  recommendation: string
}[]

install_recommendation: "approve" | "approve_with_sandbox" | "reject" | "manual_review"

sandbox_recommendation: {
  recommended: boolean
  isolation_level: "none" | "process" | "network" | "full"
  reasons: string[]
} | null

audit_summary: string    # one paragraph honest summary
```

## Risk Levels

| Level | Criteria |
|-------|----------|
| low | Minimal permissions, no shell, no env secrets, known source |
| medium | Some filesystem access or env usage, known source |
| high | Shell commands, broad permissions, or unknown source |
| critical | Opaque install scripts, secret access, eval/exec patterns |

## Suspicious Actions to Flag

- `eval`, `exec`, `Function()` — code execution
- `curl` / `wget` with pipe to shell — remote code download
- `chmod +x` / `sudo` — privilege escalation
- Reading `~/.ssh`, `/etc/passwd`, environment secrets
- Network calls to unknown hosts
- Base64-encoded or obfuscated commands
- Install scripts that fetch from unknown URLs

## Over-Privileged Points to Flag

- Filesystem access beyond the skill's stated scope
- Broad `read` permissions on entire directories
- `write` access to system paths
- Environment variables containing tokens/keys
- Network access not strictly needed for stated function

## Source Trust Levels

| Source | Trust |
|--------|-------|
| ClawHub verified | medium (review anyway) |
| Known git repo | medium |
| Local skill | high |
| Unknown URL | low |
| Copy-pasted code | very low |

## Rules

1. **Never default-approve high-privilege skills.** Burden of proof is on the skill, not the auditor.
2. **Flag remote install scripts and opaque shell chains.** If you can't see what runs, flag it.
3. **Flag access to secrets, env vars, filesystem, or network where not strictly needed.**
4. **Recommend isolation for untrusted skills.** Better safe than sorry.

## Failure Handling

If source trust cannot be established:
- Default to `risk_level = "high"` minimum
- Recommend `reject` or `manual_review`
- Do not fabricate a clean audit
- Explicitly state what could not be verified
