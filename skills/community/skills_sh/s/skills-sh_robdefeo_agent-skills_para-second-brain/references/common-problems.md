# Common Problems and Troubleshooting

## Quick Triage

1. Is this item actionable now? If yes, it probably belongs in Projects.
2. Is this an ongoing responsibility? If yes, it belongs in Areas.
3. Is this reference material with no active deadline? If yes, it belongs in Resources.

## Frequent Pain Points

### "Everything looks like a project"

Use the completion test: if it never ends, it is an Area, not a Project.

### "My inbox keeps growing"

Schedule a weekly 15-minute inbox pass and process to zero using the three-question method.

### "Too many tiny folders"

Do not create a folder unless the topic is recurring, distinct, and likely to accumulate material.

### "I cannot find what to archive"

Review `10_PROJECTS/Completed/` and projects with completion markers in `AGENTS.md`, then move closed work to `40_ARCHIVE/Projects/`.

### "Project notes keep leaking into Areas"

If filename matches an active project name, file it under that project first.

## Validation Guidance

Use `scripts/validate.sh` when users ask for system health checks.

Examples:

- Full check: `scripts/validate.sh ~/second-brain`
- Only stale projects: `scripts/validate.sh ~/second-brain --stale`
- Only structure: `scripts/validate.sh ~/second-brain --structure`

Interpret report severities:

- CRITICAL: broken structure or missing required project metadata
- WARNING: stale projects and archive candidates
- INFO: orphaned files or filing suggestions

## Error Cases

- Invalid path: user should pass a valid directory; script exits non-zero with stderr message.
- Missing required folder structure: create folders using commands suggested in the report.
- No findings: system is healthy; continue monthly maintenance.
