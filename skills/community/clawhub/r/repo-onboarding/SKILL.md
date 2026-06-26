---
name: repo-onboarding
description: Onboard a coding repository with both technical architecture intake and execution governance. Use when starting in a new/existing repo and you need: (1) architecture snapshot + dependency analysis, (2) run/build/test bootstrap map, and (3) ROADMAP + feature KANBAN workflow setup for multi-agent execution.
---

# Repo Onboarding

Combine `senior-architect` (technical intake) + `repo-kanban-pm` (execution governance).

## Workflow

1. **Technical intake (architecture + dependencies)**
2. **Execution system install (ROADMAP + KANBAN + bug inbox)**
3. **Onboarding report for handoff**

---

## Step 1 — Technical intake

Run from target repo root:

```bash
# 1) architecture assessment
python /home/broedkrummen/.openclaw/workspace-cody/skills/senior-architect/scripts/project_architect.py . --output json > docs/pm/architecture-assessment.json

# 2) dependency analysis
python /home/broedkrummen/.openclaw/workspace-cody/skills/senior-architect/scripts/dependency_analyzer.py . --output json > docs/pm/dependency-analysis.json

# 3) architecture diagram (mermaid)
python /home/broedkrummen/.openclaw/workspace-cody/skills/senior-architect/scripts/architecture_diagram_generator.py . --format mermaid -o docs/pm/architecture-diagram.md
```

If scripts fail, continue with manual fallback:
- identify stack (`package.json`, `pyproject.toml`, `go.mod`, etc.)
- capture run/build/test commands
- summarize folder structure and core boundaries in `docs/pm/ONBOARDING.md`

---

## Step 2 — Install execution governance

```bash
bash /home/broedkrummen/.openclaw/workspace-cody/skills/repo-kanban-pm/scripts/init_repo_pm.sh "$(pwd)"
```

Optional daily PM audit:

```bash
bash /home/broedkrummen/.openclaw/workspace-cody/skills/repo-kanban-pm/scripts/add_daily_pm_cron.sh "$(pwd)" --agent cody --tz UTC --time 09:30
```

---

## Step 3 — Create onboarding report

Create `docs/pm/ONBOARDING.md` using `references/onboarding-template.md`.
Must include:
- architecture summary
- dependency risks / circular deps
- run/build/test matrix
- env/config prerequisites
- initial roadmap/kanban status
- first recommended feature slice

---

## Exit criteria

Complete only when all are true:
- `docs/pm/architecture-assessment.json` exists (or manual equivalent documented)
- `docs/pm/dependency-analysis.json` exists (or manual equivalent documented)
- `docs/roadmap/ROADMAP.md` exists
- at least one `docs/features/<feature>/KANBAN.md` exists
- `docs/pm/ONBOARDING.md` exists and is actionable

## Notes

- Do not duplicate existing PM systems if repo already has one.
- If an equivalent workflow already exists, integrate with existing conventions and only fill gaps.
- Keep onboarding concise and executable by another agent in <10 minutes.
