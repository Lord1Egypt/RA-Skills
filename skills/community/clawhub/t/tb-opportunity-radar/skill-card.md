## Description:

给定一个淘宝或天猫商品链接，比较三个不同店铺的商品、买家评价及小红书需求，生成新品差异化机会分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatmind](https://clawhub.ai/user/fatmind)

### License/Terms of Use:

MIT-0

## Use Case:

电商运营和选品人员用它对比淘宝、天猫竞品的卖点、销量与买家反馈，并结合小红书评论寻找新品机会。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scraped browser-session data may be sent to an LLM endpoint selected through WC3_LLM_ENDPOINT.

Mitigation: Use only a trusted local LLM pipeline and leave WC3_LLM_ENDPOINT unset or strictly control its value.

Risk: The skill uses a logged-in Chrome Taobao/Tmall session and saves raw reviews and derived analysis locally.

Mitigation: Review the skill before installing, use a trusted local browser relay, and choose a non-shared, non-synced output directory for sensitive data.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/fatmind/skills/tb-opportunity-radar)

## Skill Output:

**Output Type(s):** [Analysis, Files]

**Output Format:** [HTML report with supporting JSON, JSONL and Markdown files; JSON run summary on stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compares up to three products; reports partial results if valid comparison products are unavailable.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
