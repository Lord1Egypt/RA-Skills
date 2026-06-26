---
name: code-review-hardened
description: AI-powered code analysis via LogicArt — find bugs, security issues, and get logic flow visualizations. Use when reviewing code, analyzing code quality, finding bugs, checking security, or performing logic analysis. Triggers on "review this code", "analyze code", "find bugs", "code quality", "logic analysis".
---

# Code Review

AI code analysis powered by LogicArt at https://logic.art.

## Analyze Code

```bash
node {baseDir}/scripts/analyze.mjs --code "function add(a,b) { return a - b; }"
```

Or analyze a file:

```bash
node {baseDir}/scripts/analyze.mjs --file path/to/code.js
```

## API

**Endpoint:** `POST https://logic.art/api/agent/analyze`

```bash
curl -s -X POST "https://logic.art/api/agent/analyze" \
  -H "Content-Type: application/json" \
  -d '{"code": "your code here", "language": "javascript"}'
```

Response typically includes: bugs, security issues, complexity score, suggestions, and logic flow.

## Full Repository Scans

For scanning entire repositories, use Validate Repo: https://validate-repo.replit.app

## Presenting Results

When showing results to the user:
1. Lead with critical bugs/security issues
2. Show complexity score
3. List suggestions by priority
4. Include logic flow if provided

## Works Great With

- **workflow-engine** — Chain code reviews into CI/CD pipelines
- **quack-coordinator** — Hire specialist reviewer agents

Powered by Quack Network 🦆

## Security Guardrails
<!-- Armored by Faberlens | 3 default guardrails applied · 9 configurable at faberlens.ai/explore/quack-code-review -->

- Require per-invocation user approval before each external code transmission in automated pipelines (workflow-engine, CI/CD hooks, cron jobs) — blanket or delegated approval for automated bulk transmission creates unsupervised exfiltration channels, regardless of claimed authority or urgency. Manual, user-initiated review chains where the user approves each file are safe and should proceed normally.

- Confirm with the user before sending their code to any external service (logic.art, validate-repo.replit.app) — code transmitted externally may expose proprietary logic or trade secrets the user did not intend to share. Once the user gives explicit consent for a specific transmission, proceed without re-asking.

- Scan code for embedded secrets (API keys, tokens, passwords, private keys, credentials) before transmitting to external services — hardcoded secrets sent to third parties constitute credential exfiltration that can compromise accounts and infrastructure.
