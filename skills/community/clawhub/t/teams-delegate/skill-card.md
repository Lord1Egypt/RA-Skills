## Description:

Delegates Microsoft Teams inbox management to an AI agent for message summaries, priority filtering, context-aware reply drafting, and Teams responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[takeovernat](https://clawhub.ai/user/takeovernat)

### License/Terms of Use:


## Use Case:

Employees and their agents use this skill to review Teams chats, summarize pending conversations, classify messages by priority, draft replies, and send Teams messages when explicitly approved or configured for auto-reply.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can monitor and send workplace Teams messages through broad Microsoft Graph permissions.

Mitigation: Install only when this access is acceptable, reduce Graph permissions to the minimum needed, and require explicit approval before every sent reply.

Risk: The local token cache can retain access to Teams data.

Mitigation: Protect the local token cache and revoke or rotate access regularly.

Risk: Unattended auto-replies could send unexpected or inappropriate messages.

Mitigation: Prefer draft-only operation and avoid cron or heartbeat auto-replies unless scope and stop conditions are tightly controlled.

## Reference(s):

- [Graph API Reference](references/graph-api.md)
- [Microsoft Graph API](https://graph.microsoft.com/v1.0)
- [Azure Portal](https://portal.azure.com)
- [ClawHub Skill Page](https://clawhub.ai/takeovernat/skills/teams-delegate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read Teams messages, summarize inbox state, and send replies through Microsoft Graph after local authentication.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
