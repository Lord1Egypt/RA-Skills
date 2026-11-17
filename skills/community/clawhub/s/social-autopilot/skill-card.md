## Description:

Social Autopilot generates and publishes platform-optimized social posts, X threads, Instagram Reels, YouTube Shorts, and Meta/Facebook posts from a user-provided content database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[humsafarprabhu-cmyk](https://clawhub.ai/user/humsafarprabhu-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and developers use this skill to automate social content generation and publishing across configured X, Instagram, YouTube, and Meta accounts. It is best suited for users who can review content and manage platform API credentials before scheduled posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish to multiple public social accounts from short commands, including a generic all-platform posting flow.

Mitigation: Use test accounts first, avoid broad posting triggers until configured, and review generated content before publishing.

Risk: The skill requires account tokens and OAuth credentials for X, Instagram, Meta, YouTube, and Cloudflare R2.

Mitigation: Limit API scopes, keep secrets outside shared project files, store YouTube tokens with restrictive permissions, and rotate credentials after testing.

Risk: Video rendering and posting workflows may run with access to production publishing credentials.

Mitigation: Run rendering in an isolated environment without production credentials and connect posting credentials only for the final reviewed workflow.

Risk: Unpinned installers or dependencies could change behavior after installation.

Mitigation: Pin installer and dependency versions before production use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/humsafarprabhu-cmyk/skills/social-autopilot)
- [Project homepage listed in artifact metadata](https://github.com/abhinawtech/social-autopilot)
- [Support link listed in artifact metadata](https://github.com/abhinawtech/social-autopilot/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with command phrases, configuration values, generated post text, and generated media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate API calls to configured social platforms and Cloudflare R2 when posting workflows are run.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
