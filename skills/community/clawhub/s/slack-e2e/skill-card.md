## Description:

Test Slack with Convex-leased user OAuth or QA bots; check credentials, exercise owned messages, prove Gateway behavior, and distinguish API evidence from real Slack client interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers and developers use this skill to validate Slack user OAuth access, run Slack and Gateway end-to-end scenarios, and distinguish API evidence from real Slack client behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial, so some referenced paths were unavailable for inspection and scan evidence is incomplete.

Mitigation: Review the unavailable paths and complete a full security scan before relying on the skill.

## Reference(s):

- [Slack chat.postMessage API](https://docs.slack.dev/reference/methods/chat.postMessage/)
- [Slack users.info API](https://docs.slack.dev/reference/methods/users.info/)
- [Slack chat.delete API](https://docs.slack.dev/reference/methods/chat.delete/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scenario-specific; test runs can write private JSON evidence and artifacts.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
