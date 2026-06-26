## Description: <br>
查询阿里平台（淘宝/天猫）商品详情，支持商品ID或链接输入，返回详情数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yjcia](https://clawhub.ai/user/yjcia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up Taobao or Tmall product details from a product ID or product link. The skill is useful when a workflow needs item title, price, sales, images, SKU, shop, or related product attributes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product IDs are sent to the EarlyData API for lookup. <br>
Mitigation: Use the skill only when sharing Taobao/Tmall product IDs with EarlyData is acceptable for the workflow. <br>
Risk: Responses are unnormalized third-party API output and may depend on provider availability or data handling. <br>
Mitigation: Review returned product details before using them in downstream decisions, and handle lookup failures or unavailable data gracefully. <br>


## Reference(s): <br>
- [API Reference](references/api_reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yjcia/taobao-detail-query) <br>
- [Publisher Profile](https://clawhub.ai/user/yjcia) <br>
- [EarlyData Detail API Endpoint](https://mi.earlydata.com/detail) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls] <br>
**Output Format:** [Markdown-formatted text containing product detail data or an error message.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Taobao/Tmall product ID or product link; sends the product ID to EarlyData for lookup.] <br>

## Skill Version(s): <br>
1.0.5 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
