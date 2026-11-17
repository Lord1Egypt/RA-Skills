## Description:

Interact with a UseMemos instance to create, search, list, comment on, and attach files to memos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minstn](https://clawhub.ai/user/minstn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to operate a self-hosted UseMemos instance from an agent workflow, including creating and finding memos, uploading attachments, and managing memo comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens and private memo data can be exposed if USEMEMOS_URL uses plaintext HTTP or if the .env file is shared.

Mitigation: Use HTTPS for USEMEMOS_URL, keep the .env file private, and rotate or revoke USEMEMOS_TOKEN if exposure is suspected.

Risk: The skill can mutate remote memo data by creating memos, uploading and linking attachments, adding comments, and deleting comments.

Mitigation: Review proposed create, upload, link, comment, and delete actions before execution, especially on shared or production UseMemos instances.

Risk: Long-lived access tokens increase impact if the token is leaked.

Mitigation: Prefer expiring tokens with the narrowest practical account access instead of non-expiring tokens.

## Reference(s):

- [UseMemos API Reference](references/api.md)
- [UseMemos](https://usememos.com)
- [ClawHub Skill Page](https://clawhub.ai/minstn/skills/usememos-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a UseMemos base URL and bearer token from USEMEMOS_URL and USEMEMOS_TOKEN.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
