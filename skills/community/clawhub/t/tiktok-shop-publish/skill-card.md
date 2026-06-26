## Description: <br>
Automates TikTok Shop operations, including product management, order processing, sales analytics, video publishing, and marketing workflow support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
TikTok Shop sellers, operators, and ecommerce teams use this skill to manage listings, process orders, review sales data, publish videos, and coordinate shop workflows from command-line driven automation. <br>

### Deployment Geography for Use: <br>
US, UK, Southeast Asia, and Indonesia <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles TikTok Shop credentials, session cookies, and shop data. <br>
Mitigation: Use mock mode first, avoid personal session cookies, provide least-privilege TikTok credentials, and inspect local configuration file permissions before using real accounts. <br>
Risk: Order fulfillment, refunds, inventory changes, pricing changes, and video publishing can affect live commerce operations. <br>
Mitigation: Enable these actions only after confirming approval controls, command scope, and expected shop impact. <br>
Risk: Feishu synchronization can move customer, order, product, and analytics data outside the shop environment. <br>
Mitigation: Use least-privilege Feishu credentials and confirm exactly what data leaves the local environment before enabling sync. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lvjunjie-byte/tiktok-shop-publish) <br>
- [TikTok Shop Seller Center](https://seller.tiktok.com/) <br>
- [TikTok Shop Partner Documentation](https://partner.tiktokshop.com/) <br>
- [TikTok Marketing API](https://business-api.tiktok.com/) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [ClawHub TikTok Shop Documentation](https://docs.clawhub.com/tiktok-shop) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Markdown, Guidance] <br>
**Output Format:** [Command-line output, configuration snippets, and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May act on shop, order, product, customer, video, analytics, and Feishu data depending on configured credentials and enabled commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, clawhub.json, README badge, and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
