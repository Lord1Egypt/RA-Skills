## Description:

Periodically audit all workspace skills, learnings, memory, and configuration files to recommend refactoring, new skill ideas, and workflow improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omaression](https://clawhub.ai/user/omaression)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace maintainers use this skill to review agent skills, memory, learnings, and configuration for stale content, overlap, workflow gaps, and concrete improvement opportunities. It produces advisory recommendations that can guide refactors, new skill ideas, and configuration updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can repeatedly read sensitive workspace files, including skills, memory, learnings, and configuration.

Mitigation: Run it manually or in dry-run mode first, narrow the watched file scope, and redact secrets or personal data before enabling recurring audits.

Risk: Audit findings may be sent to external model services and Telegram without per-run approval.

Mitigation: Require explicit approval before Telegram delivery or cron scheduling, and review generated recommendations before sharing them outside the workspace.

Risk: Recommendations may be incorrect or may propose changes that are not worth applying.

Mitigation: Treat outputs as advisory, review diffs before implementation, and require user approval before any workspace edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omaression/skills/skill-enhancer)
- [ClawHub publisher profile](https://clawhub.ai/user/omaression)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown recommendations, JSON audit files, JSON recommendation files, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory recommendations; helper scripts can write local JSON state and format Telegram messages.]

## Skill Version(s):

1.0.0-alpha (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
