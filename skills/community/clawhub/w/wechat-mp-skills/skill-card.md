## Description:

Helps an agent prepare WeChat Official Account articles by selecting a theme, processing Markdown or generated content, uploading images, and saving drafts through the WeChat API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rookiebug1216](https://clawhub.ai/user/rookiebug1216)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn article content, local Markdown files, or generated topics into WeChat Official Account drafts with selected formatting templates and uploaded image assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file uploads can expose unintended files when article Markdown or image paths are not trusted.

Mitigation: Use a dedicated content directory, inspect Markdown before upload, and validate local file paths before running the publishing workflow.

Risk: Fetching arbitrary image URLs can reach untrusted or sensitive network locations.

Mitigation: Restrict accepted image URLs to trusted hosts and validate URLs before enabling network image uploads.

Risk: WeChat access tokens or credentials may be exposed through command-line arguments or logs.

Mitigation: Use environment variables or encrypted configuration, avoid passing secrets on the command line, and patch token logging before sensitive use.

Risk: A compromised or overprivileged WeChat account increases the blast radius of publishing mistakes.

Mitigation: Use a dedicated low-privilege WeChat account and rotate AppSecret values regularly.

## Reference(s):

- [WeChat Get Access Token API](https://developers.weixin.qq.com/doc/subscription/api/base/api_getaccesstoken.html)
- [WeChat Upload Image API](https://developers.weixin.qq.com/doc/subscription/api/material/permanent/api_uploadimage.html)
- [ClawHub skill page](https://clawhub.ai/rookiebug1216/skills/wechat-mp-skills)
- [ClawHub publisher profile](https://clawhub.ai/user/rookiebug1216)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI-oriented guidance with generated article content, configuration examples, and API operation results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce draft metadata or JSON-style command results when invoking the bundled CLI.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter says 1.1.0 and pyproject.toml says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
