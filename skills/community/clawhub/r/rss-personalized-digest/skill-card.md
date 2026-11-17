## Description:

每天自动抓取多源 RSS，根据关键词权重筛选内容并生成带点击追踪跳转的个性化摘要，点击反馈会用于调整后续推荐权重。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pasaidon](https://clawhub.ai/user/pasaidon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to produce personalized RSS digests from configured sources, add click-tracking redirect links, and tune keyword weights from observed clicks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes click-tracking data and controls through an unauthenticated public tunnel.

Mitigation: Make the public tunnel opt-in, keep administrative routes private or authenticated, and restrict access before using it with real users.

Risk: Click logs include raw IP addresses and target URLs.

Mitigation: Minimize, protect, and regularly clear logged click data; avoid collecting real-user traffic unless the logging behavior is disclosed and approved.

Risk: Redirect destinations are decoded from incoming paths and then used for HTTP redirects.

Mitigation: Validate redirect destinations against an allowlist or URL policy before redirecting.

Risk: The startup flow disables SSH host key checking for the public tunnel.

Mitigation: Restore SSH host verification and make tunnel configuration explicit and reversible.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/pasaidon/skills/rss-personalized-digest)
- [IT之家 RSS](https://www.ithome.com/rss/)
- [钛媒体 RSS](https://www.tmtpost.com/rss)
- [36kr feed](https://36kr.com/feed)
- [Highsnobiety feed](https://www.highsnobiety.com/feed/)
- [The Decoder feed](https://the-decoder.com/feed/)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown digest with redirect links, plus JSON configuration and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses keyword weights, click logs, RSS feed URLs, and redirect base URL configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
