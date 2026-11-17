## Description:

Manage TickTick tasks and projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halr9000](https://clawhub.ai/user/halr9000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to TickTick so it can list, create, edit, complete, and abandon tasks and manage project configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent OAuth credentials grant the skill read/write access to TickTick tasks.

Mitigation: Install only if this access is acceptable, keep the credential store protected, and prefer a setup flow that receives the OAuth client secret interactively or through a protected channel.

Risk: Task-changing commands can edit, complete, abandon, or batch-abandon remote TickTick tasks without an additional confirmation step.

Mitigation: Review task IDs from machine-readable task output before issuing modifying commands, and require human approval before automated bulk changes.

## Reference(s):

- [ClawHub Ticktick skill page](https://clawhub.ai/halr9000/skills/ticktick-enhanced)
- [TickTick Open API endpoint](https://api.ticktick.com/open/v1)
- [TickTick OAuth endpoint](https://ticktick.com/oauth)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, YAML, shell commands, configuration, guidance]

**Output Format:** [Plain text, rich text, JSON, or YAML depending on command options.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify remote TickTick tasks through create, edit, complete, abandon, and batch-abandon commands.]

## Skill Version(s):

0.2.0 (source: ClawHub release evidence; artifact package.json reports 0.1.0 and _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
