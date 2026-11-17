## Description:

Workflow Cache queries a cloud registry for reusable browser automation workflows before model inference and can contribute successful session traces back to the registry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ainclaw](https://clawhub.ai/user/ainclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to reduce repeated browser-automation inference by replaying cached workflows when a matching pattern exists. It is also used to compile successful session traces into reusable Lobster workflows for later reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud lookups and auto-contribution can send session-derived workflow data to a remote service.

Mitigation: Use only in low-sensitivity environments unless cloud lookups and auto-contribution are governed by approval, endpoint, and workflow-verification controls; disable auto_contribute or the skill when data sharing is not approved.

Risk: Cloud-supplied workflows may be replayed in an active browser session without clear user approval or strong trust controls.

Mitigation: Require review or approval for returned workflows before execution, keep workflow validation enabled, and fall back to normal agent behavior when validation or execution fails.

## Reference(s):

- [Workflow Cache ClawHub Release](https://clawhub.ai/ainclaw/skills/workflow-cache)
- [ainclaw Publisher Profile](https://clawhub.ai/user/ainclaw)
- [Workflow Cache Homepage](https://clawhub.ai/workflow-cache)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Text responses with executable workflow steps and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform cloud lookup, replay cached browser workflows, and contribute sanitized successful workflow patterns when enabled.]

## Skill Version(s):

1.0.3 (source: evidence release, package.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
