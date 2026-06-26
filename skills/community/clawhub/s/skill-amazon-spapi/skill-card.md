## Description: <br>
Amazon SP-API skill for OpenClaw agents. Fetch orders, check FBA inventory, manage listings and pricing. Works with any marketplace and seller account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External sellers, operators, and developers use this skill to let an OpenClaw agent fetch Amazon orders, inspect FBA inventory, and read or update listing prices through Amazon SP-API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live Amazon seller-account access, including access to order data and listing price updates. <br>
Mitigation: Use least-privileged SP-API credentials, keep amazon-sp-api.json out of shared or synced folders, and require human approval before listing updates. <br>
Risk: Listing price updates can cause unintended commercial impact if an agent sends the wrong SKU, price, or marketplace. <br>
Mitigation: Run listing updates behind a wrapper with dry-run behavior, SKU allowlists, marketplace checks, and price limits. <br>
Risk: The skill depends on the external amazon-sp-api npm package and live Amazon SP-API behavior. <br>
Mitigation: Review and pin the npm dependency version before deployment, and monitor Amazon SP-API errors and rate limits during use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-amazon-spapi) <br>
- [Amazon SP-API marketplace IDs](https://developer-docs.amazon.com/sp-api/docs/marketplace-ids) <br>
- [Amazon Seller Central Develop Apps](https://sellercentral.amazon.com/apps/develop) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, API calls] <br>
**Output Format:** [CLI text and optional JSON files from Node.js scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, the amazon-sp-api package, and an amazon-sp-api.json credential file or AMAZON_SPAPI_PATH.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
