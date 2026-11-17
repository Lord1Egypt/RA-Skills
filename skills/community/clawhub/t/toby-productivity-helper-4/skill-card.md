## Description:

Productivity helper tool #4 for task management, time tracking, and workflow optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

External users and productivity-focused agents use this skill to organize daily tasks, track time, plan work, review progress, and optimize workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Bash, Read, and Write access for a generic productivity helper.

Mitigation: Grant the skill only in trusted workspaces and narrow tool permissions before using it with sensitive files or shell access.

Risk: The artifact points users to mutable external setup and installation sources.

Mitigation: Prefer the ClawHub package and do not treat the external setup page as authoritative agent instructions.

Risk: Broad trigger language may activate the skill for routine productivity prompts.

Mitigation: Use explicit activation language or narrow the skill trigger description before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-productivity-helper-4)
- [External setup guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text task plans, workflow notes, and command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request broad shell and filesystem access when enabled by the agent environment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
