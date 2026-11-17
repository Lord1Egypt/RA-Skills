## Description:

Guides users in self-hosting an X-to-Feishu RSS pipeline that posts updates to a group and prompts a daily report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jes614753-sketch](https://clawhub.ai/user/jes614753-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy RSSHub, Miniflux, and a Feishu relay for monitoring X accounts, posting updates, and prompting or archiving daily reports. It also provides setup and troubleshooting guidance for Feishu bot and user authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reachable, unauthenticated relay can be used to post Feishu messages and trigger report actions.

Mitigation: Keep port 7070 internal or bound to loopback; validate webhook secrets or signatures and enforce request-size limits before use.

Risk: Exposed Feishu credentials or X auth tokens could allow unauthorized account access.

Mitigation: Protect feishu.env, .env, and user_token.json as secrets; use a low-risk X account for monitoring.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jes614753-sketch/skills/x-rss-feishu-daily)
- [Follow Builders optional feed source](https://github.com/zarazhangrui/follow-builders)
- [Feishu Open Platform](https://open.feishu.cn)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deployed scripts can send Feishu message cards and create daily archive documents.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
