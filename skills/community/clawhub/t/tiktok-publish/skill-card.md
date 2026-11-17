## Description:

Post to TikTok, upload TikTok videos, and publish TikTok video content through the MyBrandMetrics API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawbus](https://clawhub.ai/user/clawbus)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to publish TikTok videos from local files or remote URLs through MyBrandMetrics, check publish status, and prepare one-time scheduled posting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content publicly to TikTok through a connected account.

Mitigation: Confirm the TikTok account, source media, title, and privacy setting before publishing; use SELF_ONLY for test posts.

Risk: The skill sends an API key and may upload local files or submit remote URLs to MyBrandMetrics.

Mitigation: Use environment variables in shared environments, avoid committing real tokens, and verify the exact local file path or URL before publishing.

Risk: The documented Google Sheet scheduling workflow is not implemented by the included scripts.

Mitigation: Do not rely on scheduled posting unless the publisher supplies and explains the missing implementation.

## Reference(s):

- [Configuration](references/configuration.md)
- [Publishing Examples](references/publishing-examples.md)
- [ClawHub Skill Page](https://clawhub.ai/clawbus/skills/tiktok-publish)
- [ClawBus](https://www.clawbus.com/)
- [MyBrandMetrics](https://mybrandmetrics.com/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, JSON]

**Output Format:** [Markdown guidance with inline bash commands and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a MyBrandMetrics API key and may upload local video files or submit remote video URLs for TikTok publishing.]

## Skill Version(s):

1.1.18 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
