## Description:

Converts RSS or web articles into WeChat Official Account-compatible HTML and supports optional draft publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangbaixun](https://clawhub.ai/user/huangbaixun)

### License/Terms of Use:

MIT

## Use Case:

Developers and content operators use this skill to fetch RSS or article content, prepare article data, and generate WeChat Official Account-compatible HTML with configurable branding. It can also guide optional cover generation and draft publishing when those integrations are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches user-supplied URLs from the local machine.

Mitigation: Process only trusted URLs, add URL validation or allowlisting before use, and avoid internal or sensitive network targets.

Risk: Configured publishing paths may upload generated drafts to WeChat.

Mitigation: Require a manual approval step before publishing and use least-privilege or throwaway WeChat credentials.

Risk: Local configuration can contain WeChat credentials and publishing paths.

Mitigation: Keep config.local.sh private, do not commit it, and rotate credentials if the file is exposed.

Risk: Unattended daily automation can publish or prepare content without sufficient review.

Mitigation: Avoid unattended automation until an explicit review and approval gate is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangbaixun/skills/rss-to-wechat)
- [User Guide](artifact/references/USER_GUIDE.md)
- [HTML Template](artifact/references/html-template.md)
- [Config Example](artifact/references/config.example.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash snippets, generated article JSON paths, and WeChat-compatible HTML instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional integrations can generate a cover image or upload a generated article draft when configured.]

## Skill Version(s):

1.0.1 (source: evidence.release.version, target metadata, artifact/_meta.json, changelog released 2026-03-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
