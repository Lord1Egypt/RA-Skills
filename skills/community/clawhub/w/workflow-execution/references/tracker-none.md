# Tracker Reference: None (Local Files)

How to use the workflow-execution skill without a project management system.

## When to use this

- Solo work where external tracking is overhead
- Quick tasks that don't need issue lifecycle
- Environments where no tracker is configured

## Create a plan file

Instead of a tracking issue, create a local markdown file:

```bash
mkdir -p plans/
cat > plans/my-task.md << 'EOF'
# Task: Your task title

## Goal
...

## Done Criteria
- [ ] ...

## Steps
1. ...
EOF
```

## Package context

Add sections to the same file or create companion files:

```
plans/
├── my-task.md          # Plan document
├── my-task-design.md   # Design document (when applicable)
└── my-task-context.md  # Context document (when applicable)
```

## Track progress

Update the plan file directly — check off done criteria, add notes:

```markdown
## Done Criteria
- [x] Tests pass
- [ ] PR merged
- [ ] Deployed

## Progress
- 2026-03-27: Completed implementation, tests passing. PR open.
```

## Hand off to executing agent

Include the plan file path in the spawn message:

```
Read the plan at plans/my-task.md, then implement it.
```

## Close

When done, either delete the plan file or move it to an archive:

```bash
mv plans/my-task.md plans/done/my-task.md
```

## Limitations

- No revision history (unless tracked in git)
- No multi-agent coordination (no checkout/conflict detection)
- No status lifecycle or notifications
- Consider upgrading to a real tracker if you find yourself managing multiple concurrent tasks
