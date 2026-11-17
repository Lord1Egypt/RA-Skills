## Description:

Automated test skill that verifies skill lifecycle operations including publish, inspect, update, and delete via the ClawHub REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to verify the ClawHub skill lifecycle by exercising creation, inspection, version update, and deletion behavior for a dedicated test skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lifecycle tests can update or delete ClawHub skill records if pointed at the wrong target.

Mitigation: Run only in a test context with least-privilege ClawHub credentials and confirm the target slug before any update or deletion step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/tosr-test-skill-1778050466)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands]

**Output Format:** [Markdown with REST endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
