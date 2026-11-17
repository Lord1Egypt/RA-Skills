## Description:

Read and send emails from an existing Sendook inbox, including checking new mail, reading messages, replying to conversations, and sending new messages within message-only scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obaid](https://clawhub.ai/user/obaid)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to help an agent work with a pre-configured Sendook inbox for message listing, search, reading, replies, and outbound email. It is limited to message operations and does not support inbox, domain, webhook, or API-key management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and send mail from the configured Sendook inbox using normal inbox credentials.

Mitigation: Install it only for trusted agents and use a Sendook API key restricted to the intended inbox.

Risk: Outbound messages or attachments could expose unintended content if sent without review.

Mitigation: Review outbound messages and attachments before sending, and attach only files explicitly requested by the user from the current project scope.

Risk: The skill depends on the @sendook/node package for SDK-based usage.

Mitigation: Pin or lock the @sendook/node dependency where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/obaid/skills/sendook)
- [Sendook Skills Homepage](https://github.com/obaid/sendook-skills)
- [Sendook Node SDK](https://www.npmjs.com/package/@sendook/node)
- [Sendook Node SDK Source](https://github.com/getrupt/sendook)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with TypeScript, bash, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENDOOK_API_KEY and SENDOOK_INBOX_ID environment variables for agent use.]

## Skill Version(s):

1.1.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
