## Description: <br>
TikTok 数据查询与工具助手。覆盖视频详情、用户数据、搜索、广告、创作者工具、电商等模块。含部分交互触发和协议工具接口（已标注）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing analysts, creator teams, and developers use this skill to query TikTok video, user, search, ad, creator, shop, and analytics data through the MaxHub API and summarize results in English or Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive MaxHub API keys and TikTok cookies may be transmitted to a third-party service. <br>
Mitigation: Install only when the user trusts MaxHub/aconfig.cn, use test-account cookies where possible, avoid primary-account cookies, and rotate or revoke cookies after use. <br>
Risk: Protocol utility endpoints for signatures, fingerprints, tokens, and device registration may raise platform terms or client-emulation concerns. <br>
Mitigation: Require explicit user approval before using these endpoints and review the relevant platform terms before deployment. <br>
Risk: Endpoints involving likes, follows, comments, view boosting, or account interactions can create higher misuse risk. <br>
Mitigation: Do not run these endpoints automatically; require explicit user intent and keep deployment controls focused on permitted data-analysis use cases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/new-ironman/tiktok-aggregate-scraper) <br>
- [MaxHub API service](https://www.aconfig.cn) <br>
- [README](README.md) <br>
- [Video API reference](references/api-video.md) <br>
- [User API reference](references/api-user.md) <br>
- [Search API reference](references/api-search.md) <br>
- [Ads and analytics API reference](references/api-ads-analytics.md) <br>
- [Parameter mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English and Chinese responses; API credentials should not be echoed.] <br>

## Skill Version(s): <br>
3.7.1 (source: server release metadata, frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
