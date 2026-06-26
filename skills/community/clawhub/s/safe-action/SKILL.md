---
name: safe-action
description: Before any destructive or irreversible action, run a safety pre-flight — check risks, reversibility, and timing.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🛡️"
    homepage: https://agentutil.net
    always: false
---

# safe-action

Measure twice, cut once. Before taking destructive, irreversible, or high-stakes actions, this skill runs a three-part safety pre-flight: risk assessment, reversibility check, and timing awareness.

Combines three AgentUtil services — think (safety checklists), undo (reversibility intelligence), and context (situational timing) — into a single decision workflow.

## When to Activate

Use this skill before:

- **Deleting** anything — repositories, databases, user accounts, files, branches, DNS records
- **Deploying** to production — code releases, infrastructure changes, migrations
- **Mass operations** — bulk updates, batch deletes, sending to many recipients
- **Permission changes** — revoking access, changing roles, modifying security settings
- **Infrastructure changes** — scaling down, terminating instances, modifying load balancers
- **Financial actions** — processing refunds, transferring funds, modifying billing

**Do NOT use for:** read-only operations, local development changes, or actions the user has explicitly marked as low-risk.

## Workflow

### Step 1: Safety checklist (think)

Get a pre-flight checklist for the action type.

**MCP (preferred):** If `@agentutil/think-mcp` is available:
```
think_check({ action: "database_migration", description: "Drop column users.email in production" })
```

**HTTP fallback:**
```bash
curl -X POST https://think.agentutil.net/v1/check \
  -H "Content-Type: application/json" \
  -d '{"action": "database_migration", "description": "Drop column users.email in production"}'
```

Note the `risk_level` and any `critical` severity items in the checklist.

### Step 2: Reversibility check (undo)

Assess whether the action can be undone and find safer alternatives.

**MCP (preferred):** If `@agentutil/undo-mcp` is available:
```
undo_check({ platform: "GitHub", resource: "repository", action: "delete" })
```

**HTTP fallback:**
```bash
curl -X POST https://undo.agentutil.net/v1/check \
  -H "Content-Type: application/json" \
  -d '{"platform": "GitHub", "resource": "repository", "action": "delete"}'
```

Check `reversibility_level` and `safer_alternatives`.

### Step 3: Timing check (context)

Verify this is a good time — not a holiday, after-hours, or during a known outage.

**MCP (preferred):** If `@agentutil/context-mcp` is available:
```
context_check({ action: "deploy", timezone: "America/New_York", platform: "github" })
```

**HTTP fallback:**
```bash
curl -X POST https://context.agentutil.net/v1/check \
  -H "Content-Type: application/json" \
  -d '{"action": "deploy", "timezone": "America/New_York", "platform": "github"}'
```

Check `risk_level` and any holidays or business events.

### Step 4: Synthesize and decide

Combine results into a clear recommendation:

| Scenario | Action |
|----------|--------|
| All three return low risk | Proceed. Briefly note key checklist items completed. |
| Think returns `high` risk | Pause. Present the critical checklist items to the user. Ask for explicit confirmation. |
| Undo shows `irreversible` | Warn clearly: "This action cannot be undone." Present any `safer_alternatives` (e.g., archive instead of delete). |
| Undo shows `time_limited` | Warn: "This can only be undone within [recovery_window]." |
| Context returns `high` risk | Warn about timing: "It's [holiday/after-hours/during known incident]. Consider waiting." |
| Multiple services flag risk | Present all findings together. Recommend the safest path. Do NOT proceed without explicit user approval. |

### Presentation format

When reporting findings to the user, use this structure:

```
**Pre-flight check for [action]:**

Safety: [risk_level] — [summary of critical items]
Reversibility: [reversibility_level] — [recovery_mechanism or "no recovery"]
Timing: [risk_level] — [summary or "all clear"]

[Recommendation: proceed / proceed with caution / suggest alternative / strongly advise against]
```

## Data Handling

This skill sends action descriptions, platform names, and timezone identifiers to three external APIs. No user-generated content (documents, messages, credentials) is transmitted — only structured action metadata.

## Pricing

Each sub-check costs $0.001-$0.003 via x402 (USDC on Base). A full pre-flight (all three checks) costs ~$0.004-$0.008. Free tiers available for exploration:
- think: GET /v1/actions (free)
- undo: GET /v1/platforms (free)
- context: GET /v1/calendar (free)

## Privacy

No authentication required for free endpoints. No personal data collected. Rate limiting uses IP hashing only. Action descriptions are not stored beyond immediate processing.
