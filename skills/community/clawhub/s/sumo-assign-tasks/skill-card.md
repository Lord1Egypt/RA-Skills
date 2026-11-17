## Description:

Switches the Sumo task assignment method among sessions_spawn, clawteam, and SumoSubAgent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sumo0221](https://clawhub.ai/user/sumo0221)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Sumo workflow users use this skill to check and switch the backend used for assigning tasks to subagents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists the selected assignment method to a documented local OpenClaw memory path that is hard-coded for a Windows user profile.

Mitigation: Review or adapt the path before relying on persistence outside that profile or operating environment.

Risk: The skill changes which backend is used for assigning tasks to subagents.

Mitigation: Use the status command to confirm the active method after switching and before starting dependent workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sumo0221/skills/sumo-assign-tasks)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and plain text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the selected assignment method to a local OpenClaw memory JSON file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
