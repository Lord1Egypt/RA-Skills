## Description:

Publishes a prepared Markdown article, cover image, and title to a WeChat Official Account draft box through a user-controlled WeChat Cloud relay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shinchen6](https://clawhub.ai/user/shinchen6)

### License/Terms of Use:

MIT

## Use Case:

Developers and content operators use this skill to turn finished Markdown articles into WeChat-ready HTML, upload cover and body images through a configured relay, and create or delete WeChat Official Account drafts. It is intended for users who control the relay service and can review content before real publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted article can cause readable local files outside the article folder to be uploaded as images.

Mitigation: Review Markdown from untrusted sources before running with --real, and run the skill from a restricted workspace containing only intended article assets.

Risk: Relay credentials and unpublished content can be sent over insecure or untrusted relay URLs.

Mitigation: Use an HTTPS relay that you control, configure it with a strong relay key, and inject secrets through environment variables or local config rather than hardcoding them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/shinchen6/skills/wechat-draft-publisher-cloud)
- [Companion WeChat draft relay](https://github.com/shinchen6/wechat-draft-relay)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and a publish_result.json status file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to dry-run; real publishing or draft deletion requires --real and a configured relay URL and key.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
