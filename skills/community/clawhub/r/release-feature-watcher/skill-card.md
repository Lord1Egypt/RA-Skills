## Description:

Use when the user wants to monitor a technical feature, bugfix, model/API update, changelog, release, package version, or PR and be notified only when a specific actionable condition is met.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abe238](https://clawhub.ai/user/abe238)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create quiet, self-cleaning watchers for technical releases, changelogs, packages, APIs, models, PRs, issues, and security fixes. It helps define actionable readiness conditions, baselines, schedules, success alerts, and cleanup behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled watchers can continue checking external technical sources after the original need has passed.

Mitigation: Use specific readiness conditions, review created job IDs and expiry dates, and remove watchers when they are no longer needed.

Risk: Watcher setup may write small local configuration files for recurring checks.

Mitigation: Review generated watcher configs before scheduling and keep them scoped to the requested source, condition, baseline, action, and cleanup rule.

## Reference(s):

- [Condition Patterns](artifact/references/condition-patterns.md)
- [Watcher Config Schema](artifact/templates/watcher-config.schema.json)
- [ClawHub Skill Page](https://clawhub.ai/abe238/skills/release-feature-watcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown watcher cards and alerts, JSON watcher configs, shell commands, and optional Python-based check output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quiet by default; success alerts include evidence, next action, and cleanup details.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
