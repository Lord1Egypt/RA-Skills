## Description:

TikTok机会雷达数据源（只读）：关键词搜索视频、博主公开作品和视频评论，并输出结构化 JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

TikTok creators, marketers, and research teams can search public videos, review a creator’s public posts, and inspect video comments to support topic discovery, competitor research, and audience feedback analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan is benign with medium confidence, but some components, including scripts, were only partially inspected.

Mitigation: Review the skill's scripts before use; the scan verdict is not a guarantee of safety.

Risk: Search terms and TikTok links are sent to the data service, and API usage may incur charges.

Mitigation: Use the service only when that data sharing is acceptable, and check the plan limits before requesting large result sets.

## Reference(s):

- [TikTok data service and access information](https://www.guaikei.com)
- [Parameter and output reference](references/options.md)
- [Common questions and environment setup](references/faq.md)
- [ClawHub skill page](https://clawhub.ai/guaikei/skills/tt-radar)

## Skill Output:

**Output Type(s):** [JSON, Analysis, API Calls]

**Output Format:** [Structured JSON containing TikTok search results, creator posts, or video comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data; requires GUAIKEI_API_TOKEN. Service usage may be charged and plan limits apply.]

## Skill Version(s):

1.1.3 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
