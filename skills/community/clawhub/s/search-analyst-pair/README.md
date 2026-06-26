# search-analyst-pair

ClawHub submission bundle for a deterministic `/hunt` multi-agent workflow.

## What it does

It enforces a strict handoff chain:

`Search -> Analyst -> Main synthesis`

This avoids free-form routing and keeps outputs consistent for review and execution.

## What you get

After installation, each `/hunt` run is structured into the same reviewable output:

---
🔍 Search Findings  
[sources, raw findings]

📊 Analyst Assessment  
[key points, risks, recommendation]

🎯 Main Conclusion  
[final answer, action plan]
---

## Who is this for

- Anyone running self-hosted OpenClaw who needs reliable research output
- Teams that want traceable, reviewable AI research
- Users tired of ad-hoc agent responses

## One-line pitch

Stop asking your agent to research and hope for the best.  
`/hunt` gives you a fixed three-step brief every time.

## Source implementation

Runtime workflow assets are maintained here:

- `/Users/lihaochen/openclaw/workspace/workflows/search_analyst_pair/`

This submission package contains the registry-facing docs:

- `SKILL.md` (required by ClawHub)
- `README.md`

## Dependency notes

- Requires OpenClaw gateway auth token.
- Requires `main`, `search`, `analyst` agents to be configured.
- Requires agent-to-agent permissions and subagent allowlists.

## Suggested publish command

```bash
clawhub publish /Users/lihaochen/openclaw/workspace/clawhub-submission/search-analyst-pair \
  --slug search-analyst-pair \
  --name "Search Analyst Pair" \
  --version 1.0.0 \
  --tags latest \
  --changelog "Initial release: deterministic /hunt 3-hop workflow"
```
