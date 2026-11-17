## Description:

Automates end-to-end testing of skill lifecycle operations, including create, inspect, update, and delete, through the ClawHub REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release operators use this skill to validate ClawHub skill lifecycle behavior for a temporary test skill. It is intended for authorized test contexts where create, inspect, update, and delete operations are expected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The described API actions can mutate live ClawHub skill records, including deletion.

Mitigation: Use only in an authorized ClawHub test context and keep operations scoped to the declared test slug.

Risk: Running lifecycle cleanup against production or user-owned skills could remove data unintentionally.

Mitigation: Confirm the target slug before update or delete actions and avoid cleanup outside the intended ephemeral test skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/tosr-test-skill-1778050405)

## Skill Output:

**Output Type(s):** [Guidance, API workflow descriptions]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes live lifecycle operations for a declared ephemeral ClawHub test skill.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
