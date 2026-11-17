## Description:

Guides OpenClaw agents to read X account context and draft posts, replies, quotes, and threads for explicit approval before publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[princebansal](https://clawhub.ai/user/princebansal)

### License/Terms of Use:

MIT

## Use Case:

People managing personal X accounts use this skill with the OpenClaw X plugin to check account context and prepare posts, replies, quotes, and threads for review before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect or unreviewed draft could be published to a live public account.

Mitigation: Show and review the exact draft, then require explicit user approval before publishing.

Risk: A post or media upload could use the wrong account, and media uploads are immediate external actions.

Mitigation: Confirm the selected account before publishing, keep drafts tied to that account, and upload only a user-authorized file.

## Reference(s):

- [X Management on ClawHub](https://clawhub.ai/princebansal/skills/x-management)
- [Companion OpenClaw X plugin](https://clawhub.ai/princebansal/plugins/openclaw-plugin-x)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Draft post text and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishing requires explicit approval; the companion plugin is needed for X account access.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
