## Description:

Automated social media manager that helps plan, write, schedule, and analyze content across X/Twitter, LinkedIn, Instagram, TikTok, Facebook, and Pinterest using Buffer or Postiz.

This skill is ready for commercial/non-commercial use.

## Publisher:

[batsirai](https://clawhub.ai/user/batsirai)

### License/Terms of Use:


## Use Case:

External users, marketers, founders, and developers use this skill to create social media calendars, draft platform-specific posts, schedule approved content, review basic analytics, and prepare engagement replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, queue, or schedule posts through connected social accounts.

Mitigation: Use draft mode by default, require explicit human approval before live publishing, and verify the target account, platform, content, and scheduled time before running posting commands.

Risk: Buffer, Postiz, and social OAuth credentials can grant access to post through user accounts.

Mitigation: Use test accounts or least-privilege keys where possible, store secrets outside shared files, rotate keys after evaluation, and avoid exposing .env files.

Risk: The self-hosted Postiz setup includes a curl-to-shell Docker installation pattern and depends on correct service URL configuration.

Mitigation: Review Docker's official installation guidance before running installer commands, prefer HTTPS Postiz URLs, and avoid remote HTTP Postiz endpoints.

Risk: Generated posts or engagement replies could be off-brand, misleading, or inappropriate for sensitive interactions.

Mitigation: Review drafts manually and route controversial topics, complaints, political content, or business inquiries to a human before posting or replying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/batsirai/skills/social-media-engine)
- [Publisher profile](https://clawhub.ai/user/batsirai)
- [Postiz documentation](https://docs.postiz.com)
- [Postiz GitHub repository](https://github.com/gitroomhq/postiz-app)
- [Buffer API settings](https://publish.buffer.com/settings/api)
- [Content calendar template](artifact/templates/content-calendar.md)
- [Buffer setup guide](artifact/tools/buffer-setup.md)
- [Postiz setup guide](artifact/tools/postiz-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, content tables, post drafts, setup guidance, and status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Buffer or Postiz APIs when configured with posting credentials and explicit scheduling inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
