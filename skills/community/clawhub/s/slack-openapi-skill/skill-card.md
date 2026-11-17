## Description:

Operate Slack Web API through UXC with a curated OpenAPI schema, bearer-token auth, and messaging-core guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure bearer-token access and operate a focused Slack messaging workflow through UXC, including auth validation, channel inspection, conversation and thread reads, message posting, reactions, and limited Socket Mode event intake.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Slack through user-provided tokens and may expose workspace content if credentials are over-scoped.

Mitigation: Prefer least-privilege bot tokens, avoid user tokens unless a workflow explicitly requires them, and review Slack app scopes before use.

Risk: The skill can post messages and add reactions in Slack.

Mitigation: Confirm every write action before execution and validate channel, thread, and message content before sending.

Risk: The documented default schema link points to a mutable GitHub main-branch URL.

Mitigation: Use a pinned or local OpenAPI schema when integrity and repeatability matter.

Risk: Socket Mode event capture can persist raw Slack event data locally.

Mitigation: Treat NDJSON sinks as sensitive Slack history, restrict file permissions, and use a short retention policy.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Curated Slack Web API OpenAPI Schema](references/slack-web.openapi.json)
- [Slack Web API Documentation](https://docs.slack.dev/apis/web-api)
- [Slack chat.postMessage](https://docs.slack.dev/reference/methods/chat.postMessage)
- [Slack conversations.history](https://docs.slack.dev/reference/methods/conversations.history)
- [Slack conversations.replies](https://docs.slack.dev/reference/methods/conversations.replies/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may lead an agent to make Slack Web API calls through UXC when the user provides credentials and confirms write actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
