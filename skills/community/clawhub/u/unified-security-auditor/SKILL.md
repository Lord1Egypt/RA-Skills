---
name: unified-security
description: Unified application security skill for Coding Agent systems like OpenCode. Use when reviewing or writing code that touches authentication, authorization, user input, payments, database access, secrets, deployment, dependencies, or AI/agent workflows. Includes OWASP Top 10 (2025), ASVS 5.0 highlights, agentic AI security, vibe-coded pitfalls, insecure defaults detection, supply chain risk signals, and CI/CD agent action hardening.
license: CC-BY-SA-4.0
metadata:
  sources:
    - name: claude-code-owasp
      url: https://github.com/agamm/claude-code-owasp
      license: MIT
    - name: trailofbits/skills
      url: https://github.com/trailofbits/skills
      license: CC-BY-SA-4.0
    - name: vibe-security-skill
      url: https://github.com/raroque/vibe-security-skill
      license: MIT
    - name: VibeSec-Skill
      url: https://github.com/BehiSecc/VibeSec-Skill
      license: Apache-2.0
---

# Unified Security Skill

## Mission
Audit and harden codebases against real-world security failures, especially those introduced by fast AI-assisted development. Prioritize exploitable issues and provide concrete fixes.

## Use When
- Reviewing code for security vulnerabilities
- Implementing authentication, authorization, sessions, or access control
- Handling user input, file uploads, or external data
- Working with secrets, API keys, cryptography, or tokens
- Implementing payments, billing, or webhooks
- Configuring databases, RLS, or security rules
- Integrating AI/LLM services or agent tools
- Designing CI/CD workflows that invoke AI agents
- Evaluating dependency and supply chain risk

## Core Principles
1. Never trust the client. Validate all critical data server-side.
2. Defense in depth. Combine multiple controls.
3. Fail closed. Missing config should disable access, not weaken it.
4. Least privilege. Reduce access scope everywhere.
5. Validate inputs and encode outputs for the render context.

## Audit Workflow (adapt to stack)
1. Secrets and environment variables
2. Database access control (RLS, rules, auth guards)
3. Authentication and authorization
4. Rate limiting and abuse prevention
5. Payments and webhook validation
6. Input validation and injection risks
7. XSS, output encoding, CSP, and headers
8. CSRF and session protections
9. AI/LLM integration safety
10. Deployment configuration and prod hardening
11. Insecure defaults (fail-open config)
12. Supply chain risk signals
13. CI/CD agent action hardening

## Immediate-Flag Patterns (Critical/High)
- Secrets or service-role keys exposed client-side
- Client-controlled price, role, or access flags
- Disabled or overly permissive database rules
- Missing auth on privileged routes or APIs
- Hardcoded default credentials or weak crypto
- Unverified webhooks or signature bypasses
- Fail-open config that enables insecure operation

## OWASP Top 10 (2025) Quick Map
- A01 Broken Access Control: verify ownership and deny by default
- A02 Security Misconfiguration: harden defaults, disable unused features
- A03 Supply Chain Failures: lock versions and review dependencies
- A04 Cryptographic Failures: use modern algorithms and key management
- A05 Injection: parameterize queries, validate input
- A06 Insecure Design: threat model, rate limit, design controls
- A07 Auth Failures: MFA, secure sessions, breached-password checks
- A08 Integrity Failures: verify artifacts, use SRI, avoid unsafe deserialization
- A09 Logging Failures: log security events with alerting
- A10 Exception Handling: fail closed, hide internals, log context

## ASVS 5.0 Highlights
- Level 1: 12+ char passwords, auth rate limits, HTTPS everywhere
- Level 2: MFA for sensitive ops, encryption at rest, security logging
- Level 3: HSMs, formal threat modeling, pen test validation

## Agentic AI Security (OWASP 2026) Summary
- ASI01 Goal hijack: isolate and validate inputs
- ASI02 Tool misuse: restrict tools and verify I/O
- ASI03 Privilege abuse: short-lived scoped tokens
- ASI04 Supply chain: verify plugins and MCP servers
- ASI05 Code execution: sandbox, review, approvals
- ASI06 Memory poisoning: segment and validate context
- ASI07 Agent comms: authenticate and encrypt
- ASI08 Cascading failures: circuit breakers, isolation
- ASI09 Trust exploitation: verify high-risk outputs
- ASI10 Rogue agents: monitoring and kill switches

## Insecure Defaults Detection
- Fail-open is critical: `SECRET = env.get('KEY') or 'default'`
- Fail-secure is acceptable: `SECRET = env['KEY']` (crashes if missing)
- Ignore test fixtures, templates, and docs
- Verify runtime behavior before reporting

## Supply Chain Risk Signals
Flag dependencies with one or more of:
- Single maintainer or anonymous owner
- Unmaintained or archived status
- Low popularity compared to peers
- High-risk features (FFI, deserialization, code exec)
- History of critical CVEs
- No security contact or disclosure process

## CI/CD Agent Actions Hardening
When workflows invoke AI agents, treat all event data as attacker-controlled.

Common AI action references:
- `anthropics/claude-code-action`
- `google-github-actions/run-gemini-cli`
- `openai/codex-action`
- `actions/ai-inference`

High-risk patterns:
- `pull_request_target` or `issue_comment` with untrusted input
- Prompt fields populated via `env:` intermediaries
- Eval of AI output (`eval`, `exec`, `$()`)
- Dangerous sandbox configs (`danger-full-access`, `--yolo`)
- Wildcard allowlists (`allow-users: "*"`)

Safe defaults:
- Restrict triggers to trusted contexts
- Strip or escape untrusted inputs before prompts
- Lock down tools and file access
- Use least-privileged tokens and permissions
- Require human approval for sensitive actions

## Output Format
Organize findings by severity: Critical, High, Medium, Low.
For each issue:
- File and line(s)
- Vulnerability name
- Concrete impact
- Before/after fix

End with a prioritized summary and remediation order.

## When Generating Code
Use the same checks proactively. Prefer secure patterns by default and note tradeoffs in comments when you must relax controls.

## When Generating a Security Audit Report
Save into the folder/project where this skill was executed as a markdown file with todays date

### Final Report Format

```
## Security Audit Report
**Target:** <files/component>
**Date:** <today>
**Auditor:** <ask the user for a name> OR skip and use "Automated Security Skill"

### Executive Summary
<2-3 sentences: overall risk posture, most critical issues>

### Findings

#### [CRITICAL/HIGH/MEDIUM/LOW] <Title>
- **Location:** file:line
- **Impact:** ...
- **Reproduction:** ...
- **Fix:**
  ```diff
  - vulnerable code
  + secure code
  ```

#### Recommendations
<Prioritized action items>

#### Clean Checks
<Domains with no findings>

## Attribution and License
This skill is a curated, adapted work derived from:
- https://github.com/raroque/vibe-security-skill (MIT)
- https://github.com/BehiSecc/VibeSec-Skill (Apache-2.0)
- https://github.com/agamm/claude-code-owasp (MIT)
- https://github.com/trailofbits/skills (CC-BY-SA-4.0)

This unified skill is licensed under CC-BY-SA-4.0 to satisfy ShareAlike requirements.
