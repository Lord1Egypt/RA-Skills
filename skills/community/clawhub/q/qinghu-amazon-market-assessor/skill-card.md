## Description:

青虎AI 亚马逊细分市场评估：进入某个品类前先看大盘，分析市场容量与销售额、头部 Listing 与品牌垄断程度、价格带分布、卖家所属地结构、新品活跃度、需求趋势与退货率，并给出市场准入可行性结论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers, ecommerce operators, and market researchers use this skill to decide whether a specific Amazon category is worth entering. It guides agents through Qinghu market-data calls and produces a concise go/no-go recommendation with market size, competition, pricing, seller mix, demand trend, and risk evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires a Qinghu API token and may call paid Qinghu data tools.

Mitigation: Ask for user authorization before data calls, use only the documented token sources, and report actual Qinghu point consumption from the response envelope.

Risk: Commercially sensitive market research may be exported as table files or links for larger datasets.

Mitigation: Review generated exports before sharing, avoid exposing unnecessary raw records, and keep summaries concise when full data is not required.

Risk: Market-entry conclusions depend on third-party estimated Amazon category data and correct category-node selection.

Mitigation: Resolve category nodes through the documented product_node step, label metric scope clearly, and treat estimates as directional evidence rather than absolute truth.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/autoagc/skills/qinghu-amazon-market-assessor)
- [Qinghu MCP API Endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API Key Dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)
- [Qinghu Workflow Auth Check Endpoint](https://www.iqinghu.com/api/desktop/qh/workflow/page?pageNum=1&pageSize=5)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, shell/API call examples, and optional exported table files or links for larger datasets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should lead with a market-entry conclusion, include concise supporting metrics and risks, and export large record sets instead of pasting long tables into chat.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
