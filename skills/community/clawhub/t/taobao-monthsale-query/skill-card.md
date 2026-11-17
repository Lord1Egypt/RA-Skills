## Description:

查询阿里平台（淘宝/天猫）商品月销量，支持商品ID或链接输入，返回月销量数据

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjcia](https://clawhub.ai/user/yjcia)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to check Taobao or Tmall item sales over the past 30 days by providing a product ID or product link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product IDs submitted for lookup are sent to EarlyData to retrieve sales data.

Mitigation: Use the skill only for product IDs or links that can be shared with EarlyData; avoid sending unrelated private information.

Risk: The skill is mainly documented and surfaced in Chinese, so non-Chinese users may see Chinese status and error messages.

Mitigation: Translate or summarize responses for non-Chinese users before using the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yjcia/skills/taobao-monthsale-query)
- [EarlyData month sale API endpoint](https://mi.earlydata.com/monthsale)

## Skill Output:

**Output Type(s):** [text, API calls, guidance]

**Output Format:** [Plain text response with the monthly sales result or a failure reason]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese status and error messages may be returned.]

## Skill Version(s):

1.1.5 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
