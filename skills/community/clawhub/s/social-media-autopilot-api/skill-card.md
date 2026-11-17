## Description:

Use SocialEcho OpenAPI for explicit team/account/content queries and user-authorized TikTok Shop sync or cross-platform publishing. Requires a user-provided Team API Key and confirmation before live writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socialecho-net](https://clawhub.ai/user/socialecho-net)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media operations teams use this skill to query SocialEcho team, account, content, report, upload, Reddit, Pinterest, and TikTok Shop APIs, and to prepare or execute user-confirmed publishing and product sync workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A powerful SocialEcho Team API key may be exposed if placed directly in shell commands, logs, or shared scripts.

Mitigation: Use a least-privilege Team API key, avoid printing or persisting the key, and rotate any key that may have been logged.

Risk: Publishing content or syncing TikTok Shop products can make live external changes.

Mitigation: Require a dry-run preview, exact account confirmation, and fresh user authorization before adding execution flags for each write action.

Risk: Unexpected API destinations could expose data or credentials.

Mitigation: Restrict API calls to the SocialEcho production host or the development host only when the user explicitly targets development.

## Reference(s):

- [Social media autopilot ClawHub page](https://clawhub.ai/socialecho-net/skills/social-media-autopilot-api)
- [SocialEcho app](https://app.socialecho.net/)
- [SocialEcho production API](https://api.socialecho.net)
- [SocialEcho development API](https://api-dev.socialecho.net)
- [OpenAPI specification](artifact/openapi.json)
- [Platform publish limits: copy, media, and formats](artifact/platform-publish-limits_en.md)
- [Platform publish limits: Chinese reference](artifact/platform-publish-limits_cn.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce dry-run previews for publishing and TikTok Shop sync actions before live execution.]

## Skill Version(s):

2.1.1 (source: server release evidence, package.json, openapi.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
