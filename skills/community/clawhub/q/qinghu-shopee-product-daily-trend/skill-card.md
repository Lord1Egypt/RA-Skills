## Description:

按 Shopee 商品 ID 查询最长 720 天的每日价格、销量、GMV、评分、点赞和评论趋势。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商分析人员和卖家使用此技能查看指定 Shopee 商品在选定站点和日期范围内的每日表现，评估价格与销量趋势。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may install or upgrade Node and qhkit on the host.

Mitigation: Prefer a preinstalled, pinned qhkit version; review any installation or upgrade before allowing it.

Risk: The skill may store a Qinghu API token locally.

Mitigation: Use a scoped or disposable API key and approve credential setup before use.

Risk: Qinghu data calls may consume paid credits, including on some failures.

Mitigation: Check the estimate and confirm expected charges before paid calls; review actual credits afterward.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-product-daily-trend)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [青虎 API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise prose with key metrics and optional spreadsheet file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies site, period and sample size; reports credits consumed for paid calls.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
