## Description: <br>
Deploy websites and files permanently on MegaETH mainnet using SSTORE2. Agents use their own wallet and pay gas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[planetai87](https://clawhub.ai/user/planetai87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to publish HTML, websites, and files as permanent on-chain content on MegaETH mainnet. It is intended for users who control the deployer wallet and accept mainnet gas costs and immutability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill signs real MegaETH mainnet transactions and spends gas from the configured wallet. <br>
Mitigation: Use a dedicated low-balance deployer wallet and inject PRIVATE_KEY through an environment variable or secret manager rather than command-line arguments. <br>
Risk: Published files are permanent on-chain content and cannot be taken back after deployment. <br>
Mitigation: Review the exact file or HTML content before deployment and do not publish secrets, private data, or content that should remain mutable. <br>
Risk: The skill can auto-mint an access NFT and deploy multiple chunks, increasing transaction activity. <br>
Mitigation: Confirm wallet balance, network settings, and intended content size before execution; keep CHUNK_SIZE and repeated deploy loops under operator control. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/planetai87/warren-deploy-mainnet) <br>
- [The Warren](https://thewarren.app) <br>
- [MegaETH Blockscout Explorer](https://megaeth.blockscout.com) <br>
- [MegaETH Mainnet RPC](https://mainnet.megaeth.com/rpc) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown instructions with bash commands and JSON deployment output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a PRIVATE_KEY for a funded MegaETH mainnet wallet.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
