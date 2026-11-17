## Description:

Manage Trello boards, lists, cards, comments, labels, checklists, and project workflows via the Trello API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Trello project workflows from chat, including boards, lists, cards, comments, labels, checklists, members, Power-Ups, and webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires users to enable an external plugin and rely on a hosted service with Trello OAuth access.

Mitigation: Review ClawLink and the plugin before installation, confirm Trello OAuth scopes during authorization, and revoke Trello access when no longer needed.

Risk: Destructive Trello actions can affect boards, organizations, cards, webhooks, members, labels, lists, comments, checklists, attachments, and Power-Ups.

Mitigation: Require explicit user review before write operations, especially deletion, archiving, member changes, bulk changes, and webhook changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/trello-projects)
- [Trello API Documentation](https://developer.atlassian.com/cloud/trello/)
- [Trello REST API Reference](https://developer.atlassian.com/cloud/trello/rest/)
- [Trello Power-Ups](https://trello.com/power-ups)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=trello-projects)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown with inline bash code blocks and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected Trello OAuth account through ClawLink before Trello tool calls can run.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
