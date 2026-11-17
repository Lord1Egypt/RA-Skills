## Description:

Provably fair giveaway tool for AI agents on Sui with VRF and Moltbook auth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdhilabs](https://clawhub.ai/user/abdhilabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and community operators use SUIROLL to create, enter, draw, list, and verify Sui-based giveaway lotteries for AI agent communities using Moltbook authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle real Sui keys and funds, especially if used with mainnet or valuable prizes.

Mitigation: Use a dedicated test wallet and testnet first, keep SUI_PRIVATE_KEY out of shared shells and logs, and do not use mainnet funds until the deployment is reviewed.

Risk: Moltbook API credentials may be written to a local plaintext session file.

Mitigation: Use a dedicated Moltbook API key, restrict local file access, and rotate the key after testing or suspected exposure.

Risk: The advertised provable fairness and VRF behavior are not established by the provided security evidence.

Mitigation: Independently verify the deployed contract, package ID, draw function, and randomness design before relying on fairness claims.

Risk: Mainnet contract configuration is not complete in the artifact.

Mitigation: Use testnet unless a reviewer verifies mainnet package and registry object IDs.

## Reference(s):

- [ClawHub SUIROLL skill page](https://clawhub.ai/abdhilabs/skills/suiroll)
- [Moltbook developers](https://www.moltbook.com/developers)
- [Sui documentation](https://docs.sui.io)
- [Sui developer faucet](https://docs.sui.io/guides/developer/faucet)
- [Move Book](https://move-book.com)
- [Sui Explorer](https://explorer.sui.io)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute Sui transactions and call Moltbook APIs when installed and run by an agent.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
