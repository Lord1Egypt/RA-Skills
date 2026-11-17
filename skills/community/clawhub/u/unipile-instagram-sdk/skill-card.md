## Description:

Access Instagram messaging, profiles, posts, and interactions via Unipile's official Node.js SDK for automation and content management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohit21gojs](https://clawhub.ai/user/mohit21gojs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to read Instagram account, profile, post, chat, and message data through Unipile, and to perform write actions such as sending DMs, creating posts, commenting, and reacting when write permission is enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that write actions are enabled by default despite a read-only safety claim.

Mitigation: Set UNIPILE_PERMISSIONS=read before first use, and enable write or read,write only when posting, messaging, commenting, or reacting is required.

Risk: The skill uses credentials that can grant API-level access to connected Instagram accounts through Unipile.

Mitigation: Use a dedicated Instagram account or tightly scoped Unipile setup, monitor account activity, and rotate the access token if exposure is suspected.

Risk: An unintended Unipile endpoint could receive the access token.

Mitigation: Verify that UNIPILE_DSN is the intended Unipile HTTPS endpoint before running commands, and rotate the token if it may have been used with an untrusted endpoint.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohit21gojs/skills/unipile-instagram-sdk)
- [Unipile Node SDK Repository](https://github.com/unipile/unipile-node-sdk)
- [Unipile Provider Features Documentation](https://developer.unipile.com/docs/list-provider-features)
- [Unipile Dashboard](https://dashboard.unipile.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI read operations return JSON and write operations return status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UNIPILE_DSN and UNIPILE_ACCESS_TOKEN; UNIPILE_PERMISSIONS controls read and write operations.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
