## Description:

Compress OpenClaw session context safely with backups and restore steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juanbastias](https://clawhub.ai/user/juanbastias)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage long OpenClaw agent sessions by backing up current context, preserving active work, compressing stale context, and checking that restore steps remain available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups, summaries, or persistent context updates can preserve the wrong information or omit active decisions.

Mitigation: Review proposed context changes before they are written and verify that names, numbers, decisions, blockers, and open tasks remain intact.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with checklist-style workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose backups or updates to persistent context files for user review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
