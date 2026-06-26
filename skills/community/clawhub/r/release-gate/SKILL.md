---
name: release-gate
description: Prevents bad deploys by enforcing structured sign-off before any irreversible action. Configurable checklist with named reviewers (Dev, QA, Legal, Product). Blocks execution until all required gates pass and logs every decision. Use before systemctl restarts, file deploys, database migrations, public launches, or any action that is hard to undo.
---

# Release Gate

A lightweight, configurable deployment gate for AI agents. Enforces structured sign-off before irreversible actions — no deploy without explicit checklist completion.

## When to Use This Skill

Read this skill before any action that is:
- **Hard to reverse** — systemctl restart, DB migration, file deploy, data deletion
- **Customer-facing** — public launches, website updates, pricing changes
- **High-stakes** — payments, emails to real users, legal documents going live
- **Team-coordinated** — requiring multiple agents or humans to align first

## Quick Start

```
Before deploying: run through the release gate checklist.
Block if any item is unchecked. Log the result either way.
```

### Minimal Gate (single reviewer)

```
## Release Gate — [Feature Name]

### Dev Sign-Off
- [ ] Code is tested and working
- [ ] No regressions in existing functionality
- [ ] Secrets and credentials are not hardcoded

### Final Check
- [ ] All boxes above are checked
- [ ] Deployer: [name/agent]

If any box is unchecked: BLOCK. Fix first, then re-run.
```

### Full Gate (multi-role)

```
## Release Gate — [Feature Name]
Date: YYYY-MM-DD
Deployer: [agent or human name]

### Dev Sign-Off
- [ ] Feature built and tested end-to-end
- [ ] No existing routes/endpoints broken
- [ ] DB migrations are safe and additive (no destructive schema changes)
- [ ] Security review: auth, input validation, IDOR, rate limiting

### Product / Copy Sign-Off
- [ ] Feature is represented on the website/UI
- [ ] Copy accurately describes what the code does
- [ ] No website copy for features that don't exist yet in code
- [ ] Pricing is consistent across all pages/surfaces

### Legal / Compliance Sign-Off (if applicable)
- [ ] Privacy policy covers this feature
- [ ] Regulatory requirements checked (TCPA, GDPR, COPPA, etc.)
- [ ] Any third-party terms reviewed

### Final Check
- [ ] All roles above are aligned
- [ ] No open blockers
- [ ] Log entry written to deployments.log

If any box is unchecked: BLOCK THE DEPLOY. Align first.
```

## Roles — Customize for Your Team

| Role | Responsibility |
|------|---------------|
| Dev | Code quality, tests, security |
| Product | UI/copy matches code, pricing consistency |
| Legal | Compliance, terms, privacy |
| QA | Regression testing, edge cases |
| Finance | Pricing, billing, refund policies |

Define only the roles relevant to your project. A solo dev only needs Dev + Final Check.

## Configuring Your Gate

Copy the template that fits your project into your workspace as `DEPLOY_GATE.md` (or inline it in your project's AGENTS.md). Customize the checklist items and role names.

### Example: SaaS Startup

```markdown
# Deploy Gate — MyApp

## Roles
- Dev: code, security, DB
- Product: copy, pricing, UI
- Legal: privacy, compliance

## Trigger On
- systemctl restart myapp
- Changes to app.py, models.py, templates/
- Any update to landing_page.html
- Pricing changes

## Gate Checklist
### Dev
- [ ] Tested locally + staging
- [ ] DB migration safe (additive only)
- [ ] No hardcoded secrets

### Product
- [ ] Website matches new feature
- [ ] Pricing pages updated if needed

### Orchestrator
- [ ] Dev + Product aligned
- [ ] Log entry written

## Log File
/opt/myapp/logs/deployments.log
```

## Logging

Every gate run — pass or block — must be logged.

### Log Format

```
[2026-03-30 04:00 UTC] DEPLOY: Add Stripe checkout
  Feature: Stripe payment integration v1
  Dev: PASS | Product: PASS | Legal: PASS
  Deployer: [agent or human]
  Result: APPROVED — systemctl restart myapp executed
```

```
[2026-03-30 04:00 UTC] BLOCKED: Add Stripe checkout
  Feature: Stripe payment integration v1
  Dev: PASS | Product: BLOCKED (pricing page not updated)
  Deployer: [agent or human]
  Result: BLOCKED — deploy held until Product role updates pricing page
```

### Python logging helper

```python
from scripts.release_gate import log_gate_decision

log_gate_decision(
    log_file="/opt/myapp/logs/deployments.log",
    feature="Stripe checkout v1",
    roles={"Dev": "PASS", "Product": "PASS", "Legal": "PASS"},
    result="APPROVED",
    deployer="[your agent or name]",
    notes="systemctl restart myapp"
)
```

## Hard Rules

1. **Any unchecked box = BLOCK.** Do not deploy with open items.
2. **No "I'll fix it after the deploy."** Fix first. Gate second. Deploy third.
3. **Log every decision** — pass and block. The log is the audit trail.
4. **Gate applies to rollbacks too.** A rollback is still a deploy.
5. **If you're unsure whether something needs a gate: it does.**

## Anti-Patterns to Avoid

❌ "It's just a small change" — small changes break prod  
❌ "I'll update the copy after" — website must match code on deploy  
❌ Skipping Legal row for features that touch user data  
❌ Not logging blocks — partial logs hide patterns  
❌ Running the gate mentally without writing it down  

## Integration With Agent Workflows

### Pre-deploy hook pattern

```python
# In your agent task, before any deploy command:
gate_passed = run_release_gate(
    feature="Add subscription billing",
    required_roles=["Dev", "Product"],
    checklist={
        "Dev": ["tests pass", "no hardcoded secrets", "migration safe"],
        "Product": ["pricing page updated", "copy accurate"],
    }
)
if not gate_passed:
    raise RuntimeError("Release gate not cleared. Blocking deploy.")
```

### With deploy-gate skill

If your project already uses the `deploy-gate` skill, this skill provides the underlying pattern and logging utilities. `deploy-gate` is a project-specific instantiation of `release-gate`.

## What This Skill Does NOT Do

- Does NOT enforce blocking at runtime — there is no code that physically prevents a deploy. The gate works because the agent is instructed to treat it as a hard rule.
- Does NOT detect if the gate was bypassed — if an agent skips the checklist, nothing will catch it automatically. The log is your only audit trail.
- Does NOT handle concurrent approvals — if two agents approve simultaneously, last-write-wins on the log. For multi-agent teams, serialize gate runs.
- Does NOT recover from failed logging — if the log write fails, the deploy decision is unrecorded. Always verify the log entry was written before proceeding.

This is a structured convention enforced by agent instruction, not a runtime enforcement system. That is intentional — the same model used in professional engineering workflows (PR checklists, DORA gates, SOC2 change management). The discipline is the mechanism.

## References

- OWASP Secure Deployment Checklist: https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/
- 12-Factor App deployment: https://12factor.net/
