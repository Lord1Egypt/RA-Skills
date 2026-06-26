## Description: <br>
Queries 1688 cross-border product details through the AlphaShop API using product IDs extracted from product URLs or provided directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve structured 1688 product data such as title, price, images, specifications, and supplier information for a URL, product ID, or comma-separated batch of IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AlphaShop credentials are required to query product details. <br>
Mitigation: Use a dedicated AlphaShop API key where possible and configure credentials only through the supported OpenClaw skill configuration. <br>
Risk: Queried product IDs are sent to AlphaShop and API calls may consume paid credits. <br>
Mitigation: Query only intended product IDs, monitor AlphaShop balance, and stop the workflow if AlphaShop reports insufficient balance. <br>
Risk: The Python dependencies are specified as version ranges. <br>
Mitigation: Review or pin dependency versions before running the skill in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/query-1688-product-detail) <br>
- [AlphaShop API key management](https://www.alphashop.cn/seller-center/apikey-management) <br>
- [AlphaShop API credits](https://www.alphashop.cn/seller-center/home/api-list) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses and concise command/configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AlphaShop API credentials and sends queried product IDs to AlphaShop.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
