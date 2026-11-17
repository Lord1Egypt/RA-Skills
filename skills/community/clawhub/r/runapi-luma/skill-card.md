## Description:

Query historical Luma tasks with the RunAPI CLI for one-off status lookup; this model is retired and cannot create new tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other RunAPI users can check the status of existing Luma task IDs without submitting new tasks for this retired model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating a new Luma task fails because the model is retired.

Mitigation: Only check existing task IDs; do not retry creation or substitute another model automatically.

Risk: Installing the RunAPI CLI and handling its API key introduce external software and credential exposure.

Mitigation: Install the CLI only if needed, and use environment authentication or saved CLI configuration carefully.

## Reference(s):

- [Luma model overview](https://runapi.ai/models/luma.md)
- [Luma provider overview](https://runapi.ai/providers/luma.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [Luma SDK integration](https://github.com/runapi-ai/luma-sdk)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status lookup requires an existing task ID; new Luma task creation is not supported.]

## Skill Version(s):

0.3.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
