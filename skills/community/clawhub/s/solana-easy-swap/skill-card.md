## Description: <br>
Swap Solana tokens from chat by preparing Jupiter quotes, signing with a configured keypair, submitting transactions, checking status, and returning receipts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[in-liberty420](https://clawhub.ai/user/in-liberty420) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to prepare, confirm, execute, and track Solana mainnet token swaps from an agent chat workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign and submit transactions that move real funds from the wallet configured by SOLANA_KEYPAIR_PATH. <br>
Mitigation: Use a dedicated low-balance wallet and install only when comfortable granting signing access to that keypair. <br>
Risk: Incorrect token mints, amounts, minimum received values, slippage, price impact, or destination addresses can produce unwanted swaps or transfers. <br>
Mitigation: Show the prepared swap summary and require explicit user confirmation before execution; re-confirm after any re-prepare. <br>
Risk: Jupiter and RPC providers can observe swap metadata. <br>
Mitigation: Inform users that swap requests are sent to external Solana infrastructure and avoid using the skill where that metadata exposure is unacceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/in-liberty420/solana-easy-swap) <br>
- [Publisher Profile](https://clawhub.ai/user/in-liberty420) <br>
- [Jupiter Swap API Endpoint](https://lite-api.jup.ag/swap/v1) <br>
- [Solscan Transaction URL Template](https://solscan.io/tx/{signature}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prepare, execute, status, and receipt commands return structured JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
