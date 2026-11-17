## Description:

青虎AI Shopee 爆款截流跟卖：按站点和类目拉 Shopee 商品榜单，批量查商品详情与趋势快照，分析爆款和飙升款的价格带与销量结构，判断同款跟卖还是差异化截流，并接 1688 以图搜款快速采集同款货源。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace operators and analysts use this skill to investigate Shopee hot products by site and category, compare ranking, detail, trend, keyword, price-distribution, and sourcing signals, and decide whether to follow, intercept with differentiation, watch, or drop candidate products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may call Qinghu data APIs that consume Qinghu points.

Mitigation: Confirm tool use and expected cost before calls, and report actual point consumption from the API response envelope.

Risk: The skill can use Qinghu API tokens from user input or environment variables.

Mitigation: Confirm token use with the user, keep tokens out of outputs and exports, and use only the documented Authorization header.

Risk: Large Shopee result sets may be written to local export files.

Mitigation: Tell the user where exports are written and avoid copying large raw datasets into chat.

Risk: Product-following recommendations can miss brand authorization, patent, import, or site-specific compliance constraints.

Mitigation: Present follow/intercept/drop guidance as market analysis and direct the user to verify legal and marketplace compliance before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-shopee-hot-intercept)
- [Qinghu API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, files, guidance]

**Output Format:** [Markdown summaries with structured product analysis, optional local spreadsheet exports, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large result sets are expected to be exported as local files; conclusions should include site, accounting date, period, and sample-size context.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
