## Description:

A cross-session, cross-project workflow that has agents read project state at the start, record progress while working, and leave a handoff anchor at the end.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to keep project progress, tasks, and decisions consistent across work sessions and agents, then hand off a clear next step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project progress, tasks, decisions, and logs may contain information that should not be shared.

Mitigation: Review generated project records before sharing or archiving them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yottameta/skills/yotta-workflow)
- [Project homepage](https://github.com/YottaMeta/yotta-workflow)
- [Path model](references/path-model.md)
- [FAQ](references/faq.md)
- [Walkthroughs](references/walkthroughs.md)
- [Exception playbook](references/exception-playbook.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files, Shell commands]

**Output Format:** [Markdown guidance, project-state files, and handoff text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-scoped .workflow state files and a handoff anchor.]

## Skill Version(s):

0.4.5 (source: frontmatter, package.json, changelog released 2026-11-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
