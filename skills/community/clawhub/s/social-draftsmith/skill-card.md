## Description:

Social Draftsmith drafts, rewrites, adapts, and publishes approval-first social media posts across Facebook, X, Reddit, and manual LinkedIn-ready packages from ideas, links, announcements, images, long-form text, or sourced context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[normandmickey](https://clawhub.ai/user/normandmickey)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social-media operators use this skill to turn rough ideas, sourced context, links, announcements, and images into platform-specific social post drafts, approval packages, and optional credential-backed publishing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use social-media credentials for live posting workflows.

Mitigation: Only provide credentials in environments intended for publishing, use dry-run first, and review the selected platform account or subreddit before approving a live post.

Risk: A draft or image package could be published publicly before the user has verified the exact copy and asset.

Mitigation: Require explicit approval after the final platform, text, image plan, and concrete image path are locked.

Risk: Thin source material can lead to misleading, overly confident, or legally risky public copy.

Mitigation: Ground factual or sensitive posts in reputable source context and flag defamatory, misleading, aggressive, or deceptive wording before publication.

## Reference(s):

- [ClawHub skill listing: Social Draftsmith](https://clawhub.ai/normandmickey/skills/social-draftsmith)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown drafting packages with optional shell commands and JSON dry-run or publish results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Approval-first workflow; live publishing requires platform credentials and explicit approval.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
