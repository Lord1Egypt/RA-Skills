## Description: <br>
Provides TikTok Shop store automation for product management, order handling, data analysis, video publishing, marketing operations, and Feishu synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators and developers use this skill to configure and run TikTok Shop workflows such as product import, inventory sync, order fulfillment, reporting, video publishing, and Feishu order synchronization. <br>

### Deployment Geography for Use: <br>
US, UK, Southeast Asia, and Indonesia <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect live TikTok Shop operations such as fulfillment, refunds, video publishing, stock updates, and recurring automation. <br>
Mitigation: Use mock mode first and require human approval before enabling actions that modify store state or publish content. <br>
Risk: The skill may handle account credentials, session cookies, and customer order data with local plaintext storage risk. <br>
Mitigation: Do not provide production credentials unless local storage controls are acceptable, and restrict file access to the operating-system user that runs the skill. <br>
Risk: Feishu synchronization can send order and customer data to the wrong destination if webhook, app token, or table ID values are incorrect. <br>
Mitigation: Verify all Feishu webhook and table destinations with test data before syncing real orders or customer records. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lvjunjie-byte/tiktok-shop-automation) <br>
- [TikTok Shop Seller Center](https://seller.tiktok.com/) <br>
- [TikTok Shop Partner API](https://partner.tiktokshop.com/) <br>
- [TikTok Marketing API](https://business-api.tiktok.com/) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and command-line guidance with JSON/YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate reports, exported data files, product/order updates, Feishu records, and TikTok Shop automation commands depending on the selected workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, clawhub.json, README badge, changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
