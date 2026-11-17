## Description:

Automated test skill that verifies the full skill lifecycle--publish, inspect, update, and delete--via the ClawHub REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to exercise ClawHub publish, inspect, update, and delete lifecycle behavior against the real API for an ephemeral test skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create, update, or delete a test skill through the real ClawHub API.

Mitigation: Run it only with intended test credentials and verify the slug is the expected ephemeral test skill before deletion.

Risk: The packaged metadata description is a placeholder, which can obscure that this is a lifecycle test.

Mitigation: Treat the release as a ClawHub lifecycle validation artifact and rely on the server summary and artifact body for its actual purpose.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/tosr-test-pub-update-1787627907)

## Skill Output:

**Output Type(s):** [Guidance, API Calls]

**Output Format:** [Markdown guidance describing ClawHub lifecycle API operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May exercise publish, inspect, update, and delete behavior against the real ClawHub API.]

## Skill Version(s):

0.2.0 (source: server release metadata and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
