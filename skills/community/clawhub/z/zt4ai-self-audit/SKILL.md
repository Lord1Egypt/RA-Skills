---
name: zt4ai-self-audit
description: >
  Zero Trust security audit for AI agent workspaces, skills, and configurations.
  Based on Microsoft's Zero Trust for AI (ZT4AI) framework and the "Caging the
  Agents" research (arXiv:2603.17419). Audits installed skills for prompt injection
  risk, credential exposure, excessive privilege, behavioral manipulation, and
  integrity drift. Use when: performing a security audit of agent skills, reviewing
  newly installed skills from ClawHub or other sources, checking for prompt injection
  vectors in workspace files, auditing agent permissions and trust boundaries,
  verifying skill file integrity against a baseline, or hardening an agent's
  security posture. Triggers on: "audit my skills", "security check", "ZT4AI",
  "zero trust audit", "check skill integrity", "am I secure", "harden my agent",
  "review my trust boundaries".
---

# ZT4AI Self-Audit

Audit your agent's skills, workspace, and configuration against Zero Trust for AI principles.

## Background

AI agents process instructions and data as indistinguishable tokens in a context window. This means:
- Skill files loaded into context can inject behavioral instructions
- Workspace files (SOUL.md, AGENTS.md) are both operating instructions AND attack surface
- External inputs (web content, emails, ClawHub skills) can contain prompt injection
- Credentials in plaintext config files have no access scoping or rotation

This skill applies three frameworks:
1. **Microsoft ZT4AI** — Verify explicitly, least privilege, assume breach
2. **"Caging the Agents"** (arXiv:2603.17419) — Four-layer defense: workload isolation, credential proxy, network egress, prompt integrity
3. **OWASP Agentic AI Top 10** — Trust boundary violations, privilege escalation, resource exhaustion

## Audit Process

### Step 1: Inventory Skills

Scan all three skill locations:
```bash
echo "=== System ===" && ls /usr/lib/node_modules/openclaw/skills/ 2>/dev/null
echo "=== User ===" && ls ~/.openclaw/skills/ 2>/dev/null
echo "=== Workspace ===" && ls ~/.openclaw/workspace/skills/ 2>/dev/null
```

### Step 2: Classify Each Skill

Assign every skill to a risk category using the classification guide in `references/risk-classification.md`.

Categories:
- **Behavioral modifiers** (🔴 highest risk) — Skills that change how you think, override safety instincts, or inject decision-making patterns into your context
- **Credential handlers** (🟡 elevated risk) — Skills that read, write, or transmit API keys, tokens, passwords
- **System modifiers** (🟡 elevated risk) — Skills that write to config files, modify system state, or execute with elevated privileges
- **Tool wrappers** (🟢 standard risk) — Skills that wrap external tools with well-scoped inputs/outputs
- **Read-only** (🟢 low risk) — Skills that only read data and produce reports

### Step 3: Audit Each Skill Against ZT4AI Principles

For each skill, evaluate against the checklist in `references/audit-checklist.md`.

Quick reference — the three questions:
1. **Verify explicitly**: Does this skill verify identity/authorization before acting? Does it distinguish owner from non-owner input?
2. **Least privilege**: Does this skill request only the access it needs? Could its scope be narrowed?
3. **Assume breach**: If this skill were compromised (poisoned update, prompt injection in its files), what's the worst outcome? How would you detect it?

### Step 4: Check Scripts and Executables

Find all executable code in skills:
```bash
find ~/.openclaw/skills/ ~/.openclaw/workspace/skills/ \
  -type f \( -name "*.sh" -o -name "*.py" -o -name "*.js" \) \
  2>/dev/null | sort
```

For each script, check:
- Does it access credentials? (`grep -li "API_KEY\|SECRET\|TOKEN\|PASSWORD" <file>`)
- Does it make network calls? (`grep -li "curl\|wget\|requests\|fetch\|http" <file>`)
- Does it write to system config? (`grep -li "openclaw.json\|\.env\|/etc/" <file>`)
- Does it execute arbitrary input? (`grep -li "eval\|exec\|subprocess\|system(" <file>`)

### Step 5: Generate Integrity Baseline

Create SHA256 checksums of all skill files for future drift detection:
```bash
find ~/.openclaw/skills/ ~/.openclaw/workspace/skills/ \
  -type f \( -name "*.md" -o -name "*.sh" -o -name "*.py" -o -name "*.js" -o -name "*.json" \) \
  -exec sha256sum {} \; | sort -k2 > memory/skill-integrity-baseline.md
```

To verify against an existing baseline:
```bash
sha256sum -c memory/skill-integrity-baseline.md 2>&1 | grep -v ": OK$"
```

Any output indicates modified files — investigate before trusting.

### Step 6: Assess Workspace File Security

Check the self-modification surface:
- Can the agent modify its own SOUL.md / AGENTS.md? (Yes by default — flag it)
- Are memory files loaded into context? (Yes — they're instruction vectors)
- Is MEMORY.md loaded in non-owner contexts? (Should NOT be — data leak risk)
- Are there credentials in workspace files? (`grep -rli "api_key\|password\|secret" ~/.openclaw/workspace/`)

### Step 7: Check Network Egress

Assess outbound network restrictions:
```bash
# Check for firewall rules
iptables -L OUTPUT -n 2>/dev/null || echo "No iptables access"
ufw status 2>/dev/null || echo "No UFW"

# Check what the agent can reach
curl -s -o /dev/null -w "%{http_code}" https://httpbin.org/get --max-time 5
```

If the agent has unrestricted outbound access, flag as a security gap — a compromised agent could exfiltrate data to any destination.

### Step 8: Produce Report

Generate a structured report using the template in `references/report-template.md`. Include:
- Risk classification for each skill
- Specific findings with severity ratings
- Recommended remediations with priority
- Action tier assignments (see references/action-tiers.md)

Save report to `memory/zt4ai-audit-YYYY-MM-DD.md`.

## Ongoing Monitoring

After the initial audit:
1. **Re-verify integrity** after any skill install/update (`sha256sum -c` against baseline)
2. **Re-audit behavioral skills** whenever they're updated — these are the highest risk
3. **Update baseline** after intentional skill modifications
4. **Schedule periodic audits** via cron (monthly recommended)

## References

- `references/risk-classification.md` — Detailed classification criteria with examples
- `references/audit-checklist.md` — Per-skill audit checklist
- `references/action-tiers.md` — Graduated trust model for agent actions
- `references/report-template.md` — Audit report template
