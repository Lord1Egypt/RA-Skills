## Description: <br>
Buy products from Amazon and eBay using USDC on Solana through SP3ND's autonomous x402 payment flow across 22 Amazon marketplaces, 8 eBay marketplaces, and 200+ shipping countries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kent-x1](https://clawhub.ai/user/kent-x1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to let an agent create carts, place orders, pay with USDC on Solana through x402, and track Amazon or eBay fulfillment through SP3ND. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can spend real USDC once its wallet is funded. <br>
Mitigation: Use a dedicated wallet, fund only the amount intended for autonomous purchases, monitor the balance, and add an operator approval or spend-limit gate before payment. <br>
Risk: The wallet file contains private key material that can authorize spending. <br>
Mitigation: Store `.wallet.json` with owner-only permissions, keep it out of logs and version control, and use it only for payment signing and credential-regeneration signatures. <br>
Risk: Order placement sends shipping address, phone, and contact email to SP3ND and fulfillment providers. <br>
Mitigation: Send only information required for fulfillment and use the skill only when sharing those details with the service and marketplace providers is acceptable. <br>
Risk: Using a marketplace URL that does not match the shipping country can cause failed orders, wrong pricing, or undeliverable items. <br>
Mitigation: Validate Amazon and eBay marketplace TLDs against the destination country before creating carts or orders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kent-x1/sp3nd) <br>
- [SP3ND website](https://sp3nd.shop) <br>
- [SP3ND API documentation](https://sp3nd.shop/partner-api/docs) <br>
- [SP3ND web skill file](https://sp3nd.shop/skill.md) <br>
- [SP3ND A2A agent card](https://sp3nd.shop/.well-known/agent-card.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown instructions with HTTP, JSON, JavaScript, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SP3ND API credentials, a funded dedicated Solana wallet, and network access to SP3ND, PayAI, and Solana RPC endpoints.] <br>

## Skill Version(s): <br>
1.6.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
