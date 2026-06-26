# Setup Checklist for Auto Skill Routing

## 1) AGENTS.md pre-task hook

Add near your non-trivial task checklist:

```markdown
Before non-trivial work, run:
`python skills/skill-auto-router/scripts/skill_router.py --task "<current task>"`
Then load only the top 1-3 matching skills.
```

## 2) HEARTBEAT.md daily hook

Add:

```markdown
Daily skill-router audit:
`python skills/skill-auto-router/scripts/skill_router.py --daily`
If weak descriptions are found, queue a cleanup task.
```

## 3) Publishing checklist

- Validate behavior with at least 3 real tasks
- Ensure skill descriptions are not placeholders
- Package skill:

```bash
python <openclaw-skill-creator>/scripts/package_skill.py <path-to-skill-folder>
```

- Upload resulting `.skill` file to ClawHub from your browser account
