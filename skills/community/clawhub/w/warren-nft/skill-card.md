## Description:

Deploy NFT collections permanently on MegaETH blockchain with images stored on-chain via SSTORE2, supporting collection creation, royalties, minting, and management pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[planetai87](https://clawhub.ai/user/planetai87)

### License/Terms of Use:


## Use Case:

Developers and NFT creators use this skill to deploy on-chain NFT collections to the MegaETH testnet from an image folder or generated SVG artwork, then obtain contract, management, and mint page outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses wallet signing authority to deploy contracts and store NFT assets on-chain.

Mitigation: Use a dedicated testnet wallet with limited funds and verify all transaction details before signing.

Risk: The deployment script includes embedded contract bytecode and default treasury and registration endpoints.

Mitigation: Review the default TREASURY_ADDRESS and REGISTER_API settings, and treat the bytecode as unaudited unless matching source and build verification are provided.

Risk: Private keys may be supplied through the environment or command-line arguments.

Mitigation: Prefer environment or wallet tooling that avoids shell history exposure, and do not reuse wallets containing valuable assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/planetai87/skills/warren-nft)
- [MegaWarren homepage](https://megawarren.xyz)
- [MegaETH faucet](https://docs.megaeth.com/faucet)
- [MegaETH testnet explorer](https://megaeth-testnet-v2.blockscout.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and deployment result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces transaction-facing deployment instructions and reports NFT contract address, container ID, image count, management URL, and mint URL after execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
