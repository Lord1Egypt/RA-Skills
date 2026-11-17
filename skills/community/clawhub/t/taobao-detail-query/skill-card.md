## Description:

查询阿里平台（淘宝/天猫）商品详情，支持商品ID或链接输入，返回详情数据

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjcia](https://clawhub.ai/user/yjcia)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up Taobao/Tmall product details from a product ID or product link and return the result in Markdown. It is useful for product inspection workflows that need item details such as title, price, sales, images, SKU, and shop information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product IDs are sent to EarlyData over HTTPS.

Mitigation: Query only product IDs or links that are appropriate to share with the third-party API provider.

Risk: Responses and errors are primarily in Chinese.

Mitigation: Use this skill where Chinese-language output is acceptable, or translate the result before relying on it.

Risk: The third-party API can return missing-product, rate-limit, network, or malformed-response errors.

Mitigation: Surface the returned failure reason to the user and verify important product information before acting on it.

## Reference(s):

- [API Reference](references/api_reference.md)
- [EarlyData Detail API Endpoint](https://mi.earlydata.com/detail)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown-formatted text containing product detail data or Chinese error messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a Taobao/Tmall item ID and API version 6.0; no credentials are requested by the artifact.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
