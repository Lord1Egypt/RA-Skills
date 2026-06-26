---
name: repo-agent-brief
description: Generate concise, safety-aware repository orientation briefs with @builtbyecho/repo-agent-brief/agent-brief before coding-agent work, reviews, handoffs, PR analysis, unfamiliar repo edits, diff-aware branch handoffs, or when an agent needs stack/commands/context/risk signals before changing files.
---

# Repo Agent Brief Skill

Use `@builtbyecho/repo-agent-brief` to orient an agent before it edits or reviews a repository. It finds high-signal context files, infers stack/commands, builds a compact repo map, and flags obvious secret/risky-instruction patterns.

## Default workflow

From the repository root:

```bash
npx @builtbyecho/repo-agent-brief . > AGENT_BRIEF.md
sed -n '1,220p' AGENT_BRIEF.md
```

For in-progress branches:

```bash
npx @builtbyecho/repo-agent-brief . --diff origin/main > AGENT_HANDOFF.md
sed -n '1,260p' AGENT_HANDOFF.md
```

For machine-readable automation:

```bash
npx @builtbyecho/repo-agent-brief . --format json > agent-brief.json
```

For durable handoffs:

```bash
npx @builtbyecho/repo-agent-brief . --diff HEAD --bundle
sed -n '1,220p' .agent-brief/brief.md
sed -n '1,160p' .agent-brief/verification.md
```

## When to use

- First pass in an unfamiliar repo.
- Before delegating to a coding agent.
- PR/branch handoff where changed files matter.
- Safety preflight before touching CI, migrations, deploy scripts, auth, or config.

## Safety

- This is not a full secret scanner. Use Gitleaks/TruffleHog for full audits.
- If high-risk patterns are found, inspect before proceeding.
- Use `--fail-on-high-risk` in CI or strict agent workflows.
- Generated briefs may include snippets from repo context files; avoid posting publicly without review.

## Useful commands

```bash
npx @builtbyecho/repo-agent-brief .
npx @builtbyecho/repo-agent-brief . --diff HEAD
npx @builtbyecho/repo-agent-brief . --diff HEAD --bundle
npx @builtbyecho/repo-agent-brief . --diff origin/main --fail-on-high-risk
npx @builtbyecho/repo-agent-brief . --no-snippets
```
