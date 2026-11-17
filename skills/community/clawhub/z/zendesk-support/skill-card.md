## Description:

Manage Zendesk support tickets, users, organizations, macros, and helpdesk workflows via the Zendesk REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams and developers use this skill to manage Zendesk tickets, users, organizations, macros, and helpdesk workflows from an agent session through ClawLink-authenticated Zendesk tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected Zendesk account access can expose or affect support data within the permissions granted during OAuth.

Mitigation: Review Zendesk OAuth permissions before connecting, use an account with appropriate scope, and revoke the connection when it is no longer needed.

Risk: Write, destructive, and bulk operations can create, update, or delete Zendesk records.

Mitigation: Use the preview and confirmation flow for every write or destructive action, and review target resources and intended effects before execution.

Risk: The integration depends on trust in ClawLink and the ClawHub plugin source for credential handling.

Mitigation: Install only if the user trusts ClawLink and the plugin source with Zendesk account access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/zendesk-support)
- [Zendesk REST API Docs](https://developer.zendesk.com/api-reference/)
- [Zendesk Ticketing API Reference](https://developer.zendesk.com/api-reference/ticketing/introduction/)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to discover live Zendesk tools, preview write actions, and require user confirmation before create, update, delete, or bulk operations.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
