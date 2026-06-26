## Description: <br>
Amazon SP-API skill for OpenClaw agents. Fetch orders, check FBA inventory, manage listings and pricing. Works with any marketplace and seller account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and seller-operations teams use this skill to let OpenClaw agents retrieve Amazon orders, inspect FBA inventory, and manage listing data or prices through Amazon SP-API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use sensitive Amazon SP-API seller credentials. <br>
Mitigation: Use least-privilege credentials, protect the credential file, and only install the skill for agents that are intended to access Amazon seller-account data. <br>
Risk: Listing updates can change live SKU prices without a built-in confirmation or dry-run safeguard. <br>
Mitigation: Require manual approval of SKU, marketplace, current price, new price, and currency before running listing updates. <br>
Risk: The skill depends on an npm package for Amazon SP-API access. <br>
Mitigation: Pin and review the npm dependency before deployment. <br>


## Reference(s): <br>
- [Amazon SP-API Marketplace IDs](https://developer-docs.amazon.com/sp-api/docs/marketplace-ids) <br>
- [ClawHub release page](https://clawhub.ai/Zero2Ai-hub/skill-spapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; scripts can print text or JSON results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and Amazon SP-API credentials supplied through a local configuration file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
