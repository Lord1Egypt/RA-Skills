## Description: <br>
Discovers, inspects, and requests RedotPay services through the RedotPay CLI across media, model, data API, and commerce lookup categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turbo-wang](https://clawhub.ai/user/turbo-wang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search RedotPay service listings, inspect service details and pricing, and make confirmed paid service requests when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make wallet-backed paid requests through the RedotPay CLI. <br>
Mitigation: Require exact cost, currency, purpose, and explicit user confirmation before every paid request. <br>
Risk: Wallet login and request handling may involve sensitive credentials or payment metadata. <br>
Mitigation: Use a limited-balance account, avoid exposing tokens or wallet configuration, use verbose logging sparingly, and log out when finished. <br>
Risk: Unverified service calls may exceed the user's intended spend. <br>
Mitigation: Inspect service pricing before calling and set a spend cap with --max-spend or REDOTPAY_CLI_MAX_SPEND for chargeable requests. <br>


## Reference(s): <br>
- [RedotPay Wallet Skill Page](https://clawhub.ai/turbo-wang/redotpay-wallet) <br>
- [RedotPay CLI Installer](https://raw.githubusercontent.com/redotpay/redotpay-cli/v0.1.0/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and RedotPay CLI request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include service identifiers, endpoint details, pricing, confirmation prompts, login guidance, and request results.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
