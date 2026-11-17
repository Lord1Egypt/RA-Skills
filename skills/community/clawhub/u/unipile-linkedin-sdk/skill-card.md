## Description:

LinkedIn integration via Unipile's official Node.js SDK for messaging, InMail, profile lookup, connection management, post creation, and content interaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohit21gojs](https://clawhub.ai/user/mohit21gojs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect agents to LinkedIn through Unipile for account discovery, profile and post retrieval, messaging, invitations, reactions, comments, and post creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform write-capable LinkedIn actions such as sending messages, creating posts, invitations, comments, and reactions.

Mitigation: Set UNIPILE_PERMISSIONS=read by default, enable write only for a specific task, and return to read-only mode after the task.

Risk: A Unipile access token can perform actions on the user's behalf.

Mitigation: Store the token in environment variables or a secrets manager, avoid workspace files, and rotate or revoke it if it may have been exposed.

Risk: Using an untrusted or incorrect Unipile DSN could send credentials or account activity to the wrong endpoint.

Mitigation: Verify UNIPILE_DSN comes from the Unipile dashboard and uses HTTPS before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohit21gojs/skills/unipile-linkedin-sdk)
- [Unipile API documentation](https://developer.unipile.com/docs/list-provider-features)
- [Unipile dashboard](https://dashboard.unipile.com)
- [Unipile Node SDK repository](https://github.com/unipile/unipile-node-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and JSON API responses from the included CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UNIPILE_DSN and UNIPILE_ACCESS_TOKEN; UNIPILE_PERMISSIONS controls read and write operations.]

## Skill Version(s):

1.5.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
