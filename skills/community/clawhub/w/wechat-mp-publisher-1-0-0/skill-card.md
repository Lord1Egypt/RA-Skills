## Description:

Publishes articles to WeChat Official Accounts through the WeChat API using configured AppID, AppSecret, IP whitelist, and access token management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saaaa1aaaas](https://clawhub.ai/user/saaaa1aaaas)

### License/Terms of Use:

MIT

## Use Case:

Developers and WeChat Official Account operators use this skill to configure WeChat credentials, fetch access tokens, and publish Markdown or text articles from a Node.js CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat credentials or access tokens may be exposed through example secrets, command output, or an unprotected .env file.

Mitigation: Replace example secrets with placeholders, rotate any AppSecret that may have been published, avoid printing tokens, and add explicit .env protection such as .gitignore guidance.

Risk: Publishable HTML may be unsafe if generated content is saved or submitted without sanitization.

Mitigation: Sanitize generated HTML before saving or publishing and review article content before submission.

Risk: Flagged npm dependencies may contain known security issues.

Mitigation: Update the flagged npm dependencies before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/saaaa1aaaas/skills/wechat-mp-publisher-1-0-0)
- [Publisher profile](https://clawhub.ai/user/saaaa1aaaas)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, HTML]

**Output Format:** [Markdown guidance with CLI commands, status text, and optional saved HTML output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WeChat AppID and AppSecret environment variables and may publish content through WeChat API calls.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact/package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
