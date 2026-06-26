## Description: <br>
爆款选题发现虾 monitors trend lists across Weibo, Douyin, Zhihu, Baidu, Bilibili, and related platforms, filters topics against an account profile, analyzes viral-content patterns, and produces actionable content-topic recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, content marketers, and agent users use this skill to find current high-potential topics, match them to an account niche, draft structured topic cards, and optionally save selected ideas to a Feishu topic database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Platform cookies used for Douyin or Xiaohongshu access can grant account access if pasted or hardcoded carelessly. <br>
Mitigation: Prefer unauthenticated sources where available, and only use cookies after reviewing what account access they provide. <br>
Risk: Saving recommendations to Feishu may expose planning data or create records in the wrong workspace. <br>
Mitigation: Require explicit user confirmation before creating Feishu tables or writing records, and confirm the destination table and fields first. <br>
Risk: Live trend data can be incomplete, stale, rate-limited, or blocked by platform anti-scraping changes. <br>
Mitigation: Treat fetched hotlists as time-sensitive inputs, handle 403 or 429 responses as retrieval failures, and avoid relying on a single platform source. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/viral-topic-finder-claw) <br>
- [Platform Hotlist API Guide](references/platform-hotlist-api.md) <br>
- [Viral Content Analysis Model](references/viral-content-analysis.md) <br>
- [Account Keyword Library](references/account-keywords.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with structured topic cards and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch live trend data from supported platforms and may optionally prepare Feishu table records when requested by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
