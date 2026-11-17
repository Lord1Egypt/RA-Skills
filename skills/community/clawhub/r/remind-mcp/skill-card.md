## Description:

Read Remind classes, chats, messages, and notification settings from the shell using a signed-in browser session and GraphQL queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve account, class, chat, message, and notification data from Remind in scripts or one-off shell workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell workflow can send messages to chats or classes and change notification delivery settings.

Mitigation: Require explicit approval of recipients and message text before sending, and approval before changing notification delivery; use a read-only workflow that rejects mutations when only reading.

Risk: The saved session contains authentication credentials for a Remind account.

Mitigation: Protect the session file like a password and delete it when it is no longer needed.

Risk: The external CLI, browser extension, and live Remind service were not audited as part of this release.

Mitigation: Review these dependencies before relying on them and limit captured credentials to the required Remind domain and headers.

## Reference(s):

- [GraphQL query examples](references/graphql-queries.md)
- [Remind GraphQL API](https://www.remind.com/graphql)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Remind account data as JSON or text, with Markdown guidance and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
