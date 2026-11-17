## Description:

Multi-platform social media posting service with automatic provider failover for Twitter/X, LinkedIn, Instagram, Facebook, TikTok, Threads, Bluesky, YouTube, and Pinterest, including per-user credential management, OAuth flow, media upload, scheduling, and post history tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external teams use this skill to guide agents through publishing, scheduling, and tracking social media posts across supported platforms with provider failover and account-level credential handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or schedule public social media posts.

Mitigation: Require confirmation of the provider account, platform list, post content, media, schedule, and credential source before any post is created or scheduled.

Risk: Global provider credentials may be used when a user has no personal credentials.

Mitigation: Disable global credential fallback for ordinary user-generated posts unless the workflow is explicitly a service-owned publishing flow.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/social-posting)
- [ClawHub publisher profile](https://clawhub.ai/user/phy041)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider API payload examples, environment variable guidance, database schema snippets, and posting workflow steps.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
