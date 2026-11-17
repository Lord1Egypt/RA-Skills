## Description:

使用 EasyPost 自动填充或发布微博（Weibo）动态图文或视频。Use when 用户需要向微博发布图文或视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gybin02](https://clawhub.ai/user/gybin02)

### License/Terms of Use:

MIT-0

## Use Case:

People who manage a Weibo account can use this skill to prepare image or short-video posts in their logged-in browser session, review the filled post, and publish it when ready.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using --yes publishes immediately without the default manual review.

Mitigation: Use the default fill mode to inspect the account, text, and media before publication; use --yes only when immediate publication is intended.

Risk: The security review covers the skill instructions, not the external EasyPost program.

Mitigation: Use a trusted EasyPost installation.

## Reference(s):

- [Weibo](https://weibo.com)
- [ClawHub skill page](https://clawhub.ai/gybin02/skills/weibo-upload)

## Skill Output:

**Output Type(s):** [Configuration, Shell commands, Guidance]

**Output Format:** [JSON post payloads and shell commands with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports image posts with 1–9 images and short-video posts; post content may include Weibo topic tags.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
