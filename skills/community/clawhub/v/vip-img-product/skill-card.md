## Description: <br>
唯品会（vip.com）图片搜索商品技能，当用户想通过图片搜索相似商品时触发，包括以图搜图、拍照搜商品、图片搜索、找同款等，并返回商品名称、价格、品牌、图片、链接等结构化信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vip](https://clawhub.ai/user/vip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to upload a local product image and search Vipshop for visually similar products or same-item matches. The agent can return product names, brands, pricing, images, product links, and pagination details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses saved Vipshop login state and may expose authenticated product links derived from account material. <br>
Mitigation: Install only if the publisher is trusted, avoid sharing or logging generated product links, and prefer normal product URLs when possible. <br>
Risk: The workflow uploads user-provided images to Vipshop services for image search. <br>
Mitigation: Request explicit user consent before upload and avoid using sensitive or private images. <br>
Risk: Raw backend data or token-derived links may be included in agent-visible results. <br>
Mitigation: Review outputs before sharing and redact raw backend data or authentication-derived links from logs and public reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vip/vip-img-product) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON script output and Markdown table with product images and product-name links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local image path, Vipshop login state, and network access; supports pageToken-based pagination with up to 10 products per page.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
