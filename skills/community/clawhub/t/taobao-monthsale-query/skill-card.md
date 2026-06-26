## Description: <br>
查询阿里平台（淘宝/天猫）商品月销量，支持商品ID或链接输入，返回月销量数据 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yjcia](https://clawhub.ai/user/yjcia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users provide a Taobao or Tmall item ID or product URL to retrieve the item's reported sales for the past 30 days. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Taobao or Tmall item IDs are sent to EarlyData for sales lookup. <br>
Mitigation: Use the skill only when sending item IDs to EarlyData is acceptable for the user's workflow. <br>
Risk: Lookup results depend on a third-party API and network availability. <br>
Mitigation: Surface timeout, rate-limit, invalid-link, and unavailable-item failures clearly and retry later when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yjcia/taobao-monthsale-query) <br>
- [EarlyData month-sale API endpoint](https://mi.earlydata.com/monthsale) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text response with the month-sales value or a concise failure reason.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Taobao or Tmall item ID or URL; sends the item ID to the EarlyData API for lookup.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
