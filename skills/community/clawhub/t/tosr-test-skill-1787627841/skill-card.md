## Description:

Automated integration test skill for verifying ClawHub skill lifecycle operations, including creation, update, inspection, and deletion via the ClawHub API.

This skill is for research and development only.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill in controlled test environments to verify ClawHub skill lifecycle behavior across publish, inspect, update, and delete flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes publish, update, and delete operations against the real ClawHub API.

Mitigation: Use it only for ClawHub lifecycle tests in a sandbox or test account, and confirm the fixed test slug before allowing API operations.

## Reference(s):

- [TOSR Test Skill on ClawHub](https://clawhub.ai/yinwuzhe/skills/tosr-test-skill-1787627841)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown with REST endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe publish, inspect, update, and delete lifecycle operations for a fixed test skill slug.]

## Skill Version(s):

0.2.0 (source: server release metadata and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
