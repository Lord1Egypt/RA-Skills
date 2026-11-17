## Description:

Deploy NFT collections permanently on MegaETH mainnet with images stored on-chain via SSTORE2 and published through WarrenContainer and WarrenLaunchedNFT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[planetai87](https://clawhub.ai/user/planetai87)

### License/Terms of Use:

ISC

## Use Case:

External developers and NFT creators use this skill to deploy NFT collections on MegaETH mainnet, store collection images permanently on-chain, and obtain management and mint page links for the deployed collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses wallet signing authority on MegaETH mainnet, where transactions consume real funds and deployed content is permanent.

Mitigation: Use a dedicated low-balance deployment wallet, review collection settings before execution, and confirm gas funding intentionally.

Risk: A private key is required, and passing it as a command-line argument can expose it through shell or process history.

Mitigation: Prefer a controlled PRIVATE_KEY environment variable or secret-injection workflow, avoid --private-key, and rotate any key that may have been exposed.

Risk: The deployment flow can submit collection metadata and wallet/contract identifiers to the Warren registration API after on-chain deployment.

Mitigation: Review the REGISTER_API behavior before running and proceed only if off-chain registration of that metadata is acceptable.

Risk: The setup script installs npm dependencies without a pinned lockfile.

Mitigation: Review and pin dependencies in a lockfile before installation in controlled or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/planetai87/skills/warren-nft-mainnet)
- [Warren app](https://thewarren.app)
- [Declared source link](https://github.com/planetai87/warren-tools)
- [MegaETH Blockscout explorer](https://megaeth.blockscout.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON]

**Output Format:** [Markdown instructions with inline bash commands plus deployment status text and final JSON from the deployment script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, a funded MegaETH mainnet wallet, and PRIVATE_KEY for transaction signing.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata; artifact/package.json is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
