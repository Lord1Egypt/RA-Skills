## Description:

Manages Todoist tasks, projects, sections, labels, comments, completed-task reports, activity logs, ID migration, project templates, and sync workflows through Todoist API v1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:

MIT

## Use Case:

Developers, agents, and Todoist power users use this skill to inspect, capture, organize, bulk-update, and report on Todoist work through a non-interactive CLI with JSON output and dry-run controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Todoist token can be sent to a caller-chosen API base URL if --base-url is overridden.

Mitigation: Use environment-based token injection, keep --base-url at the official Todoist HTTPS API, and remove or allowlist --base-url before broader deployment.

Risk: Bulk, raw, sync, or destructive operations can change many Todoist objects.

Mitigation: Start with read-only commands, resolve names to IDs, require --dry-run previews, and execute only with explicit --confirm after user review.

Risk: Large paginated API responses can exceed an agent's working context or obscure relevant results.

Mitigation: Use --limit, --max-items, cursors, and --output FILE for large payloads.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tristanmanchester/skills/todoist-api-skill)
- [Todoist API v1 endpoint](https://api.todoist.com/api/v1)
- [Command reference](references/REFERENCE.md)
- [Recipes](references/RECIPES.md)
- [Gotchas](references/GOTCHAS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON or summary output from the Todoist CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI defaults to structured JSON envelopes, supports summary output, and can write full results to a file for large responses.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
