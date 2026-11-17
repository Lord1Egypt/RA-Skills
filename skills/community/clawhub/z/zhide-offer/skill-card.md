## Description:

职得Offer校园求职助手调用职得Offer MCP接口查询校园招聘岗位和面试经验。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack-yang-ai](https://clawhub.ai/user/jack-yang-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially students and early-career job seekers, use this skill to search campus recruiting and internship roles, inspect job details, search interview experiences, and review interview rounds, questions, and answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recruiting searches, filters, job or interview IDs, quota checks, and the API key are sent to offer.yxzrkj.cn.

Mitigation: Install only if that data sharing is acceptable for the intended use.

Risk: A local config file can expose the API key if it is committed or shared.

Mitigation: Prefer the ZHIDE_OFFER_KEY environment variable and do not commit real API keys into repositories or shared skill directories.

## Reference(s):

- [职得Offer MCP API 文档](artifact/references/api.md)
- [ClawHub release page](https://clawhub.ai/jack-yang-ai/skills/zhide-offer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or terminal text with shell commands and API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ZHIDE_OFFER_KEY API key; requests may send recruiting searches, company and city filters, requested job or interview IDs, account quota checks, and the API key to offer.yxzrkj.cn.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
