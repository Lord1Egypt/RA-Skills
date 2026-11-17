## Description:

Automated test skill verifying skill creation, inspection, updating, and deletion via the ClawHub REST API lifecycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to verify the ClawHub skill lifecycle for a fixed ephemeral test skill, including publishing, inspecting, updating, and cleanup behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes real publish, update, inspect, and delete behavior for a fixed ephemeral ClawHub test skill.

Mitigation: Install or run it only in a ClawHub test context where lifecycle changes to the named ephemeral skill are acceptable.

Risk: Using production credentials could apply the described lifecycle operations to a live ClawHub account.

Mitigation: Use test credentials unless the operator intentionally wants those publish, update, inspect, and cleanup actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown prose describing REST API lifecycle operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.2.0 (source: server release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
