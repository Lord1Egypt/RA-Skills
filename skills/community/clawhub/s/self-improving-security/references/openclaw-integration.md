# OpenClaw Security Integration

Complete setup and usage guide for integrating the security self-improvement skill with OpenClaw.

## Overview

OpenClaw uses workspace-based prompt injection combined with event-driven hooks. Security context is injected from workspace files at session start, and hooks trigger on lifecycle events to remind the agent about security finding capture.

## Workspace Structure

```
~/.openclaw/
├── workspace/                   # Working directory
│   ├── AGENTS.md               # Incident response workflows, security automation
│   ├── SOUL.md                 # Security principles, assume-breach mindset
│   ├── TOOLS.md                # Security tool configs, scanner gotchas
│   ├── HARDENING.md            # Infrastructure and application hardening checklist
│   ├── PLAYBOOKS.md            # Incident response playbooks
│   ├── COMPLIANCE.md           # Compliance matrices and audit evidence
│   ├── MEMORY.md               # Long-term memory (main session only)
│   └── .learnings/             # Security finding logs
│       ├── LEARNINGS.md
│       ├── SECURITY_INCIDENTS.md
│       └── FEATURE_REQUESTS.md
├── skills/                      # Installed skills
│   └── self-improving-security/
│       └── SKILL.md
└── hooks/                       # Custom hooks
    └── self-improving-security/
        ├── HOOK.md
        └── handler.ts
```

## Quick Setup

### 1. Install the Skill

```bash
clawdhub install self-improving-security
```

Or copy manually:

```bash
cp -r self-improving-security ~/.openclaw/skills/
```

### 2. Install the Hook (Optional)

Copy the hook to OpenClaw's hooks directory:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-security
```

Enable the hook:

```bash
openclaw hooks enable self-improving-security
```

### 3. Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Or copy from `assets/`:

```bash
cp assets/LEARNINGS.md ~/.openclaw/workspace/.learnings/
cp assets/ERRORS.md ~/.openclaw/workspace/.learnings/SECURITY_INCIDENTS.md
cp assets/FEATURE_REQUESTS.md ~/.openclaw/workspace/.learnings/
```

## Injected Prompt Files

### AGENTS.md (Security Workflows)

Purpose: Incident response workflows and security automation patterns.

```markdown
# Security Agent Coordination

## Incident Response Workflow
1. Detect: Identify the security finding or incident
2. Triage: Assess severity, blast radius, and urgency
3. Contain: Apply immediate containment measures
4. Remediate: Fix the root cause
5. Verify: Confirm remediation is effective
6. Document: Log to .learnings/ with full context

## Delegation Rules
- Use explore agent for vulnerability pattern searches across codebase
- Spawn sub-agents for parallel security scans
- Use sessions_send to share critical findings across sessions
```

### SOUL.md (Security Principles)

Purpose: Security mindset and principles.

```markdown
# Security Principles

## Core Mindset
- Assume breach: act as if attackers already have access
- Defense in depth: never rely on a single control
- Least privilege: grant minimum permissions needed
- Zero trust: verify explicitly, never trust implicitly

## Handling Sensitive Data
- NEVER log actual secrets, credentials, tokens, or PII
- Always use REDACTED_* placeholders
- Describe the type and location, not the content
- When in doubt, redact more rather than less
```

### TOOLS.md (Security Tools)

Purpose: Security tool capabilities, scanner configurations, and integration gotchas.

```markdown
# Security Tools

## Dependency Scanning
- `npm audit` / `pnpm audit` for Node.js dependencies
- `safety check` for Python dependencies
- `trivy` for container image scanning

## Secret Scanning
- `gitleaks` for git history scanning
- `trufflehog` for deep secret detection
- GitHub Secret Scanning for repository-level alerts

## Static Analysis
- `semgrep` for pattern-based code scanning
- `bandit` for Python security linting
- `eslint-plugin-security` for JavaScript/TypeScript
```

## Security-Specific Promotion Decision Tree

```
Is the finding a one-off or broadly applicable?
├── One-off → Keep in .learnings/
└── Broadly applicable →
    ├── Security principle or mindset? → SOUL.md
    ├── Incident response procedure? → PLAYBOOKS.md
    ├── Infrastructure hardening? → HARDENING.md
    ├── Compliance requirement? → COMPLIANCE.md
    ├── Tool configuration or gotcha? → TOOLS.md
    └── Workflow or automation? → AGENTS.md
```

## Inter-Agent Communication

OpenClaw provides tools for cross-session sharing of security findings.

Use these only when cross-session sharing is explicitly needed and the environment is trusted. **Never forward raw secrets, credentials, or unredacted sensitive data.**

### sessions_send (Security Alerts)

Send critical security findings to other sessions:
```
sessions_send(sessionKey="session-id", message="SECURITY: Expired JWT bypass found in admin middleware. See SEC-20250415-002.")
```

Prefer sending a concise finding summary plus entry ID rather than raw details.

### sessions_spawn (Security Scans)

Spawn background agents for security tasks:
```
sessions_spawn(task="Run dependency audit and report CVEs with CVSS >= 7.0", label="security-scan")
```

## OpenClaw-Specific Detection Triggers

| Trigger | Action |
|---------|--------|
| Dependency audit finds CVEs | Log to SECURITY_INCIDENTS.md with CVE details |
| Tool reports misconfiguration | Log to LEARNINGS.md with misconfiguration category |
| Session detects secret in output | Log to SECURITY_INCIDENTS.md, REDACT immediately |
| Cross-session security alert | Evaluate and log locally if applicable |
| Compliance check failure | Log to LEARNINGS.md with compliance_gap category |

## Available Hook Events

| Event | When It Fires |
|-------|---------------|
| `agent:bootstrap` | Before workspace files inject |
| `command:new` | When `/new` command issued |
| `command:reset` | When `/reset` command issued |
| `command:stop` | When `/stop` command issued |
| `gateway:startup` | When gateway starts |

## Verification

Check hook is registered:

```bash
openclaw hooks list
```

Check skill is loaded:

```bash
openclaw status
```

## Troubleshooting

### Hook not firing

1. Ensure hooks enabled in config
2. Restart gateway after config changes
3. Check gateway logs for errors

### Learnings not persisting

1. Verify `.learnings/` directory exists
2. Check file permissions
3. Ensure workspace path is configured correctly

### Skill not loading

1. Check skill is in skills directory
2. Verify SKILL.md has correct frontmatter
3. Run `openclaw status` to see loaded skills
