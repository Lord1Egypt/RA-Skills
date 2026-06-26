## Description: <br>
AI-native lending service for autonomous agents to request loans, repay with USDC on Base, and check credit scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsoft-latam](https://clawhub.ai/user/rsoft-latam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to interact with RSoft Agentic Bank: checking rates and creditworthiness, requesting Base Sepolia USDC loans, repaying through the payment skill, and confirming repayment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The repayment flow asks the agent to send USDC to an address returned by RSoft's API. <br>
Mitigation: Use a dedicated testnet wallet with limited funds and review the returned pay_to address and repayment_amount before authorizing payment. <br>
Risk: Wallet addresses, request IDs, and transaction hashes are sent to RSoft's API, and retention or sharing practices are not explained in the evidence. <br>
Mitigation: Review RSoft's data practices before using the service with sensitive identifiers or operational wallets. <br>
Risk: The skill depends on a separately installed payment skill and a funded Base Sepolia wallet. <br>
Mitigation: Verify the payment skill separately and keep only the funds needed for the intended testnet workflow in the wallet. <br>


## Reference(s): <br>
- [RSoft Agentic Bank Homepage](https://rsoft-agentic-bank.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/rsoft-latam/rsoft-agentic-bank) <br>
- [BaseScan Sepolia Explorer](https://sepolia.basescan.org/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown instructions with shell command examples and REST API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and a payment skill wallet configured for Base Sepolia.] <br>

## Skill Version(s): <br>
1.7.0 (source: release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
