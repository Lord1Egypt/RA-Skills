## Description:

OpenClaw Task Manager records, tracks, and manages assigned assistant tasks, including task type, status, invoked functions, permission needs, dependencies, and task statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quenfly](https://clawhub.ai/user/quenfly)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to keep a persistent Markdown task log, update task status, query tasks, and recalculate summary statistics for ongoing or one-time work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic persistent task logging can store secrets, credentials, private plans, client details, or other sensitive task content in TASKS.md.

Mitigation: Install only when persistent task logging is desired, avoid recording sensitive details, and review the contents and location of TASKS.md before sharing or retaining it.

Risk: The skill uses broad triggers and little user control, which can create more task records than expected.

Mitigation: Review or change the configured storage path and operational expectations before enabling the skill in routine workflows.

Risk: The statistics updater modifies a task file and is described by security evidence as needing hardening before use on important files.

Mitigation: Inspect the script and test it on a copy of TASKS.md before running it against important task logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quenfly/skills/task-manager-easy)
- [Source skill documentation](artifact/SKILL.md)
- [Release description](artifact/RELEASE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown task records with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes or updates a persistent TASKS.md file; the included Node.js script recalculates task summary counts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
