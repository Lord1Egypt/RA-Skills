## Description: <br>
唯品会（vip.com）图片搜索商品技能。当用户想通过图片搜索相似商品时触发，包括但不限于：以图搜图、拍照搜商品、图片搜索、找同款等。返回商品名称、价格、品牌、图片、链接等结构化信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vip](https://clawhub.ai/user/vip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can provide a local product image to search Vipshop for visually similar goods, then review structured product names, brands, prices, images, links, and pagination results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses stored Vipshop login tokens and can generate signed account-linked product URLs. <br>
Mitigation: Review before installing, assume searches use the logged-in Vipshop session, and avoid sharing generated product links or transcripts. <br>
Risk: Local images are uploaded to Vipshop services for image search. <br>
Mitigation: Use only images the user is comfortable uploading to Vipshop and confirm intent before searching sensitive or private images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vip/vipshop-img-product) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, markdown, text] <br>
**Output Format:** [Markdown tables and concise text generated from JSON script output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local image path, Vipshop login state, and optional pagination token for follow-up result pages.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
