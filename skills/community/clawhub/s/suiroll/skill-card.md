## Description: <br>
Provably fair giveaway tool for AI agents on Sui with VRF and Moltbook auth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abdhilabs](https://clawhub.ai/user/abdhilabs) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers, community operators, and agents use SUIROLL to create, enter, draw, list, and verify Sui-based giveaways with Moltbook-backed participant authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can sign and submit Sui blockchain transactions, including actions that may involve real funds. <br>
Mitigation: Use testnet first, use a dedicated low-value wallet, and verify the network, package ID, registry ID, prize amount, gas budget, and transaction target before signing. <br>
Risk: Moltbook API credentials may be retained locally in plaintext. <br>
Mitigation: Avoid entering secrets in shared or recorded terminals and delete ~/.config/suiroll/moltbook-session.json after use if the retained API key is not needed. <br>


## Reference(s): <br>
- [SUIROLL ClawHub release](https://clawhub.ai/abdhilabs/suiroll) <br>
- [Sui documentation](https://docs.sui.io) <br>
- [Sui testnet faucet guide](https://docs.sui.io/guides/developer/faucet) <br>
- [Move Book](https://move-book.com) <br>
- [Sui Explorer](https://explorer.sui.io) <br>
- [Moltbook developer API keys](https://www.moltbook.com/developers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce blockchain transaction digests, lottery object IDs, verification summaries, and setup guidance for Sui and Moltbook credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
