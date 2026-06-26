## Description: <br>
Deploy NFT collections permanently on MegaETH blockchain with on-chain image storage via SSTORE2, royalties, minting, and management pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[planetai87](https://clawhub.ai/user/planetai87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and NFT creators use this skill to set up and run a Node.js workflow that deploys MegaETH testnet NFT collections from image folders or generated SVG art. It helps configure collection metadata, minting limits, pricing, royalties, and post-deployment management links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks for wallet-signing authority and can spend testnet funds or deploy contracts from the configured wallet. <br>
Mitigation: Use only a fresh MegaETH testnet wallet with no mainnet funds or valuable assets, and avoid passing private keys inline or through command history. <br>
Risk: Deployed images, metadata, contract addresses, and wallet addresses are public and difficult to undo once written on-chain. <br>
Mitigation: Review all images, collection names, supply limits, prices, royalties, and wallet settings before running the deployment command. <br>
Risk: The security evidence flags the skill as suspicious because irreversible blockchain actions have limited guardrails. <br>
Mitigation: Review the skill before installing and execute it only in the intended MegaETH testnet environment. <br>


## Reference(s): <br>
- [MegaWarren homepage](https://megawarren.xyz) <br>
- [MegaETH faucet documentation](https://docs.megaeth.com/faucet) <br>
- [MegaETH testnet explorer](https://megaeth-testnet-v2.blockscout.com) <br>
- [ClawHub skill page](https://clawhub.ai/planetai87/warren-nft) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JavaScript CLI usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce blockchain transaction details, NFT contract addresses, container IDs, image counts, and MegaWarren management or mint page links after execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
