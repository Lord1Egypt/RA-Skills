---
name: self-improving-security
description: "Captures vulnerabilities, misconfigurations, access control violations, compliance gaps, incident response patterns, and threat intelligence to enable continuous security improvement. Use when: (1) A CVE or vulnerability is discovered, (2) Secrets are exposed in logs or output, (3) Access control violations or unauthorized access attempts occur, (4) Compliance audit findings or gaps are identified, (5) Security misconfigurations are found in infrastructure or applications, (6) Incident response procedures are executed or improved, (7) Threat intelligence is gathered from advisories or pen test results."
---

# Self-Improving Security Skill

Log security learnings, incidents, and compliance findings to markdown files for continuous improvement. Security-specific entries track vulnerabilities, misconfigurations, access violations, and incident response outcomes. Mature patterns get promoted to security runbooks, hardening checklists, incident response playbooks, and compliance matrices.

## CRITICAL: Sensitive Data Redaction

**NEVER log actual secrets, credentials, tokens, private keys, API keys, passwords, connection strings, or PII in any learning or incident entry.** Always redact sensitive values before writing. Use placeholders:

| Sensitive Data | Redacted Form |
|----------------|---------------|
| API keys | `REDACTED_API_KEY` |
| Passwords | `REDACTED_PASSWORD` |
| Access tokens (JWT, bearer, session) | `REDACTED_TOKEN` |
| Private keys | `REDACTED_PRIVATE_KEY` |
| Connection strings | `REDACTED_CONNECTION_STRING` |
| PII (emails, SSNs) | `REDACTED_PII` |
| IP addresses (internal) | `REDACTED_INTERNAL_IP` |
| Certificate contents | `REDACTED_CERT` |

When logging an incident involving exposed secrets, describe *what kind* of secret was exposed, *where* it appeared, and *the remediation taken* — never the secret itself.

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Security Learnings\n\nVulnerabilities, misconfigurations, compliance gaps, and security insights.\n\n**Categories**: vulnerability | misconfiguration | access_violation | compliance_gap | incident_response | threat_intelligence\n**Areas**: authentication | authorization | encryption | network | endpoint | compliance | cloud\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/SECURITY_INCIDENTS.md ] || printf "# Security Incidents Log\n\nVulnerability discoveries, access violations, secrets exposure, and active security incidents.\n\n---\n" > .learnings/SECURITY_INCIDENTS.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Security Feature Requests\n\nSecurity capabilities and hardening improvements requested or identified.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

If you want automatic reminders or setup assistance, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

No credentials or access tokens are required by this skill.

## Quick Reference

| Situation | Action |
|-----------|--------|
| CVE found in dependency | Log to `.learnings/SECURITY_INCIDENTS.md` with category `vulnerability` |
| Secrets exposed in logs/output | Log to `.learnings/SECURITY_INCIDENTS.md` — **REDACT the secret first** |
| Access violation or unauthorized access | Log to `.learnings/SECURITY_INCIDENTS.md` with category `access_violation` |
| Misconfigured permissions/policies | Log to `.learnings/LEARNINGS.md` with category `misconfiguration` |
| Compliance audit failure | Log to `.learnings/LEARNINGS.md` with category `compliance_gap` |
| Incident response executed | Log to `.learnings/LEARNINGS.md` with category `incident_response` |
| Threat intelligence gathered | Log to `.learnings/LEARNINGS.md` with category `threat_intelligence` |
| Security feature needed | Log to `.learnings/FEATURE_REQUESTS.md` |
| Hardening improvement identified | Log to `.learnings/LEARNINGS.md` with category `misconfiguration` |
| SSL/TLS or certificate issue | Log to `.learnings/SECURITY_INCIDENTS.md` with area `encryption` |
| CORS misconfiguration | Log to `.learnings/LEARNINGS.md` with area `network` |
| Authentication bypass found | Log to `.learnings/SECURITY_INCIDENTS.md` with area `authentication` |
| Similar to existing entry | Link with `**See Also**`, consider priority bump |
| Broadly applicable security pattern | Promote to hardening checklist, runbook, or playbook |
| Proven incident workflow | Promote to `AGENTS.md` (OpenClaw workspace) |
| Security tool gotcha | Promote to `TOOLS.md` (OpenClaw workspace) |
| Security principles | Promote to `SOUL.md` (OpenClaw workspace) |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-security
```

**Manual:**
```bash
git clone https://github.com/jose-compu/self-improving-security.git ~/.openclaw/skills/self-improving-security
```

### Workspace Structure

OpenClaw injects these files into every session:

```
~/.openclaw/workspace/
├── AGENTS.md          # Incident response workflows, delegation patterns
├── SOUL.md            # Security principles, assume-breach mindset
├── TOOLS.md           # Security tool capabilities, scanner configs
├── MEMORY.md          # Long-term memory (main session only)
├── memory/            # Daily memory files
│   └── YYYY-MM-DD.md
└── .learnings/        # This skill's log files
    ├── LEARNINGS.md
    ├── SECURITY_INCIDENTS.md
    └── FEATURE_REQUESTS.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` — misconfigurations, compliance gaps, threat intelligence, best practices
- `SECURITY_INCIDENTS.md` — vulnerabilities, access violations, secrets exposure
- `FEATURE_REQUESTS.md` — security capabilities and hardening requests

### Promotion Targets

When security learnings prove broadly applicable, promote them:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Security principles | `SOUL.md` | "Assume breach, defense in depth" |
| Incident response workflows | `AGENTS.md` | "Rotate credentials before root cause analysis" |
| Security tool hardening | `TOOLS.md` | "Always pass --no-cache to docker build in CI" |
| Hardening checklist items | `HARDENING.md` | "Disable directory listing on all web servers" |
| Incident response steps | `PLAYBOOKS.md` | "Secrets exposure containment procedure" |
| Compliance requirements | `COMPLIANCE.md` | "GDPR data retention audit quarterly" |

### Optional: Enable Hook

For automatic reminders at session start:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-security
openclaw hooks enable self-improving-security
```

See `references/openclaw-integration.md` for complete details.

---

## Generic Setup (Other Agents)

For Claude Code, Codex, Copilot, or other agents, create `.learnings/` in the project or workspace root:

```bash
mkdir -p .learnings
```

Create the files inline using the headers shown above. Avoid reading templates from the current repo or workspace unless you explicitly trust that path.

### Add reference to agent files

Add to AGENTS.md, CLAUDE.md, or `.github/copilot-instructions.md`:

#### Security Self-Improvement Workflow

When security issues or findings occur:
1. Log to `.learnings/SECURITY_INCIDENTS.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
2. **ALWAYS redact secrets before logging**
3. Review and promote broadly applicable findings to:
   - `CLAUDE.md` - security conventions and constraints
   - `AGENTS.md` - incident response workflows
   - `.github/copilot-instructions.md` - security context for Copilot

## Logging Format

### Learning Entry

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: authentication | authorization | encryption | network | endpoint | compliance | cloud
**CVSS**: N/A or score (e.g., 7.5)

### Summary
One-line description of the security finding or learning

### Details
Full context: what was found, the security impact, affected systems, root cause

### Remediation
Specific fix, hardening step, or compensating control

### Metadata
- Source: cve_advisory | pen_test | audit | user_feedback | incident | scan
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- CVE: CVE-YYYY-NNNNN (if applicable)
- CWE: CWE-XXX (if applicable)
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: harden.input_validation | comply.gdpr_consent (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

### Security Incident Entry

Append to `.learnings/SECURITY_INCIDENTS.md`:

```markdown
## [SEC-YYYYMMDD-XXX] incident_type

**Logged**: ISO-8601 timestamp
**Priority**: critical | high | medium | low
**Status**: pending
**Area**: authentication | authorization | encryption | network | endpoint | compliance | cloud
**Severity**: critical | high | medium | low
**CVSS**: score or N/A

### Summary
Brief description of the security incident

### Incident Details
```
Sanitized error output, log excerpt, or finding description.
NEVER include actual secrets, tokens, keys, or PII here.
```

### Impact Assessment
- Affected systems/services
- Data at risk (type, not content)
- Blast radius estimate

### Containment & Remediation
- Immediate containment steps taken
- Root cause (if known)
- Long-term remediation plan

### Timeline
- **Detected**: ISO-8601
- **Contained**: ISO-8601 (if applicable)
- **Resolved**: ISO-8601 (if applicable)

### Metadata
- CVE: CVE-YYYY-NNNNN (if applicable)
- CWE: CWE-XXX (if applicable)
- Attack Vector: network | adjacent | local | physical
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: SEC-20250110-001 (if related)

---
```

### Feature Request Entry

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: authentication | authorization | encryption | network | endpoint | compliance | cloud

### Requested Capability
What security capability is needed

### Security Justification
Why this capability matters — what risk it mitigates, what compliance requirement it satisfies

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built, what security controls it enables

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name
- Compliance: SOC2 | GDPR | HIPAA | PCI-DSS | ISO27001 (if applicable)

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `SEC` (security incident), `FEAT` (feature request)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20250415-001`, `SEC-20250415-A3F`, `FEAT-20250415-002`

## Resolving Entries

When an issue is fixed or mitigated, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 or #42
- **Remediation Applied**: Brief description of fix or compensating control
- **Verified By**: pen test | scan | manual review
```

Other status values:
- `in_progress` - Actively being investigated or remediated
- `wont_fix` - Risk accepted (add justification in Resolution notes)
- `promoted` - Elevated to hardening checklist, runbook, or playbook
- `promoted_to_skill` - Extracted as a reusable skill

## Promoting to Security Documentation

When a finding is broadly applicable, promote it to permanent security documentation.

### When to Promote

- Finding applies across multiple services/environments
- Pattern should be part of standard hardening
- Prevents recurring security issues
- Documents compliance requirements
- Defines incident response procedures

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| `CLAUDE.md` | Security constraints, banned patterns, safe defaults |
| `AGENTS.md` | Incident response workflows, security scan automation |
| `.github/copilot-instructions.md` | Security coding standards for Copilot |
| `SOUL.md` | Security mindset: assume breach, defense in depth, least privilege |
| `TOOLS.md` | Security scanner configs, tool-specific hardening |
| `HARDENING.md` | Infrastructure and application hardening checklist |
| `PLAYBOOKS.md` | Incident response playbooks |
| `COMPLIANCE.md` | Compliance matrices and audit evidence |

### How to Promote

1. **Distill** the finding into a concise security rule or control
2. **Add** to appropriate section in target file (create file if needed)
3. **Update** original entry:
   - Change `**Status**: pending` → `**Status**: promoted`
   - Add `**Promoted**: HARDENING.md` (or whichever target)

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: SEC-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Recurring security issues often indicate:
   - Missing hardening baseline (→ promote to HARDENING.md)
   - Missing automation (→ add scanner or pre-commit hook)
   - Architectural weakness (→ create security architecture ticket)
   - Compliance gap (→ update compliance matrix)

## Detection Triggers

Automatically log when you notice:

**Vulnerability Indicators** (→ security incident):
- `CVE-` prefix in output or advisories
- `CRITICAL` or `HIGH` severity in scan results
- `vulnerability` or `exploit` in dependency audit output
- SQL injection, XSS, CSRF patterns in code review

**Secrets Exposure** (→ security incident, **REDACT IMMEDIATELY**):
- API keys, tokens, passwords in logs or output
- Private keys or certificates in plaintext
- Connection strings with embedded credentials
- `.env` files with secrets committed to git

**Access Control Issues** (→ security incident):
- `Permission denied` in unexpected contexts
- `403 Forbidden` or `401 Unauthorized` errors
- Authentication failures or bypass attempts
- Privilege escalation indicators

**Infrastructure Signals** (→ learning):
- `SSL` or `TLS` handshake failures
- `certificate expired` or `certificate verify failed`
- `CORS` policy violations or misconfigurations
- Open ports or exposed services in scan results
- `insecure` flag usage in tools or configs

**Compliance Signals** (→ learning):
- Audit exception or finding
- Missing logging or monitoring
- Data retention policy violations
- Missing consent mechanisms

**Feature Requests** (→ feature request):
- "We need secret scanning..."
- "Can we automate compliance checks..."
- "Is there a way to detect..."
- "We should add MFA for..."

## Priority Guidelines

| Priority | When to Use |
|----------|-------------|
| `critical` | Active exploitation, data breach, secrets exposed in production, zero-day |
| `high` | Known CVE unpatched, secrets in CI/CD logs, missing auth on public endpoint |
| `medium` | Misconfiguration with compensating controls, compliance gap with workaround |
| `low` | Hardening improvement, defense-in-depth enhancement, informational finding |

## Area Tags

Use to filter findings by security domain:

| Area | Scope |
|------|-------|
| `authentication` | Login, MFA, session management, credential storage |
| `authorization` | RBAC, ABAC, permission models, access policies |
| `encryption` | TLS/SSL, at-rest encryption, key management, certificates |
| `network` | Firewalls, CORS, DNS, load balancers, ingress/egress |
| `endpoint` | API security, input validation, rate limiting, WAF |
| `compliance` | SOC2, GDPR, HIPAA, PCI-DSS, ISO 27001, audit trails |
| `cloud` | IAM policies, S3 buckets, security groups, KMS, cloud posture |

## Security-Specific Best Practices

1. **Always redact** — never log actual secrets, credentials, tokens, or PII
2. **Assume breach** — treat every finding as if an attacker already has access
3. **Defense in depth** — one control failing should not mean total compromise
4. **Least privilege** — document the minimum permissions needed, not the maximum
5. **Log immediately** — security context degrades fast; capture details now
6. **Include CVSS/CWE** — standardized scoring enables consistent prioritization
7. **Document blast radius** — who and what is affected if this is exploited
8. **Track remediation timeline** — time-to-fix is a key security metric
9. **Link related entries** — attack chains often span multiple findings
10. **Promote aggressively** — proven security patterns belong in hardening checklists

## Periodic Review

Review `.learnings/` at natural breakpoints:

### When to Review
- Before deploying to production
- After security incidents
- Before compliance audits
- After dependency updates
- Weekly during active development
- After pen test or vulnerability scan results

### Quick Status Check
```bash
# Count pending security items
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# List pending critical/high items
grep -B5 "Priority\*\*: critical\|Priority\*\*: high" .learnings/*.md | grep "^## \["

# Find findings for a specific area
grep -l "Area\*\*: authentication" .learnings/*.md

# List all CVEs referenced
grep -h "CVE:" .learnings/*.md | sort -u
```

## Hook Integration

Enable automatic reminders through agent hooks. This is **opt-in**.

### Conservative Mode (Recommended)
- Default to manual logging (no hooks); if reminders are useful, enable `UserPromptSubmit` with `scripts/activator.sh` only.
- Enable `PostToolUse` (`scripts/error-detector.sh`) only in trusted environments when you explicitly want command-output pattern checks.

### Quick Setup (Claude Code / Codex)

Create `.claude/settings.json` in your project:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-security/scripts/activator.sh"
      }]
    }]
  }
}
```

### Advanced Setup (With Security Error Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-security/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-security/scripts/error-detector.sh"
      }]
    }]
  }
}
```

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate security findings |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Detects security-relevant patterns in output |

See `references/hooks-setup.md` for detailed configuration and troubleshooting.

## Automatic Skill Extraction

When a security learning is valuable enough to become a reusable skill, extract it.

### Skill Extraction Criteria

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Has `See Also` links to 2+ similar findings |
| **Verified** | Status is `resolved` with confirmed remediation |
| **Non-obvious** | Required investigation or specialized knowledge |
| **Broadly applicable** | Not environment-specific; useful across projects |
| **User-flagged** | User says "save this as a security skill" |

### Extraction Workflow

1. **Identify candidate**: Finding meets extraction criteria
2. **Run helper** (or create manually):
   ```bash
   ./skills/self-improving-security/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-security/scripts/extract-skill.sh skill-name
   ```
3. **Customize SKILL.md**: Fill in template with finding content
4. **Update entry**: Set status to `promoted_to_skill`, add `Skill-Path`
5. **Verify**: Ensure no secrets or sensitive data leaked into the skill

### Extraction Detection Triggers

**In conversation:**
- "Save this security pattern"
- "This vulnerability keeps appearing"
- "Add this to our hardening checklist"
- "Remember this incident response step"

**In entries:**
- Multiple `See Also` links (recurring vulnerability pattern)
- Critical priority + resolved status
- Category: `incident_response` with documented procedure
- Compliance finding with reusable remediation

## Gitignore Options

**Keep learnings local** (recommended for security):
```gitignore
.learnings/
```

Security findings may contain sensitive context. Default to local-only.

**Track learnings in repo** (team-wide, sanitized):
Only if all entries are confirmed free of secrets, credentials, and PII.

## Multi-Agent Support

### Claude Code
**Activation**: Hooks (UserPromptSubmit, PostToolUse)
**Setup**: `.claude/settings.json` with hook configuration
**Detection**: Automatic via hook scripts

### Codex CLI
**Activation**: Hooks (same pattern as Claude Code)
**Setup**: `.codex/settings.json` with hook configuration

### GitHub Copilot
**Activation**: Manual (no hook support)
**Setup**: Add security self-improvement guidance to `.github/copilot-instructions.md`

### OpenClaw
**Activation**: Workspace injection + inter-agent messaging
**Setup**: See "OpenClaw Setup" section above

### Agent-Agnostic Guidance

Regardless of agent, apply security self-improvement when you:

1. **Discover a vulnerability** — in dependencies, code, or configuration
2. **Find exposed secrets** — in logs, output, repos, or CI pipelines
3. **Identify access issues** — unauthorized access, privilege escalation, broken auth
4. **Note compliance gaps** — missing controls, audit failures, policy violations
5. **Improve incident response** — better containment, faster detection, clearer procedures
6. **Gather threat intelligence** — new attack vectors, advisory patterns, pen test results

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/security/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: security
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (security)
Only trigger this skill automatically for security signals such as:
- `cve-|vulnerability|exploit|secret|token|credential|key leaked`
- `auth bypass|privilege escalation|tls|ssl|cors misconfiguration`
- explicit security intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/security/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
