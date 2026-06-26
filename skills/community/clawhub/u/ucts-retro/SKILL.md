---
name: ucts-retro
description: >
  Weekly engineering retrospective. What shipped, what broke, what to improve,
  with concrete action items. Works directly in OpenClaw — no Claude Code session needed.
tags: [ucts, retrospective, engineering, team]
---

# UCTS Retro

Weekly engineering retrospective. This is a structured conversation — guide the user through each section.

## Format

### 🚀 What Shipped?

List everything that shipped this week:
- Features, fixes, improvements
- PRs merged, deployments completed
- Documentation updated

For each item, note:
- Did it take longer than expected? Why?
- Any surprises during implementation?
- What would you do differently?

### 💥 What Broke?

List everything that went wrong:
- Bugs found in production
- Incidents, outages, reverts
- Build failures, flaky tests
- Missed deadlines

For each item:
- **Root cause** (not symptoms). Use /investigate methodology if needed.
- **Impact**: who was affected, for how long?
- **Was it preventable?** What guard would have caught it?

### 🔧 What to Improve?

Identify friction points:
- Process: what takes too long, what's manual that should be automated?
- Tooling: what's broken, slow, or missing?
- Knowledge: what did you have to learn the hard way?
- Communication: what was unclear or undocumented?

### ✅ Action Items

**Maximum 3.** More than 3 means none will get done.

Each action item must have:
- **Owner**: one person (not "the team")
- **Deadline**: specific date (not "soon")
- **Definition of done**: how do you know it's complete?

Bad: "Improve testing"
Good: "Add integration tests for the payment flow by Friday. Done = CI passes with payment tests."

Bad: "Look into performance"
Good: "Profile the /api/search endpoint, identify top bottleneck, open a PR with a fix by Wednesday."

## If Actions Require Code

Spawn a Claude Code session:
```
Load UCTS. Run /ucts guide <action item description>
```
