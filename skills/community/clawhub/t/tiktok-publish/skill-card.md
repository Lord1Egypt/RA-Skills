## Description: <br>
Post to TikTok, upload TikTok videos, and publish TikTok video content through the MyBrandMetrics API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawbus](https://clawhub.ai/user/clawbus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and publishing operators use this skill to publish TikTok videos from local files or remote URLs, check publish status, and prepare one-time scheduled posting workflows through MyBrandMetrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or schedule content to a connected TikTok account using sensitive MyBrandMetrics credentials. <br>
Mitigation: Start with SELF_ONLY for tests, protect API keys, and confirm the account, media, title, privacy level, and schedule before posting. <br>
Risk: Local files, remote URLs, or Google Sheet links supplied to the workflow may be sent to MyBrandMetrics for publishing. <br>
Mitigation: Use only media and links that are intended for the publishing workflow, and avoid private files or internal URLs unless sharing them with MyBrandMetrics is acceptable. <br>


## Reference(s): <br>
- [TikTok Publisher Skill Page](https://clawhub.ai/clawbus/tiktok-publish) <br>
- [ClawBus](https://www.clawbus.com/) <br>
- [MyBrandMetrics](https://mybrandmetrics.com/) <br>
- [Configuration](references/configuration.md) <br>
- [Publishing Examples](references/publishing-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MyBrandMetrics API key and user-confirmed TikTok account, media source, title, privacy level, and schedule before publishing.] <br>

## Skill Version(s): <br>
1.1.18 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
