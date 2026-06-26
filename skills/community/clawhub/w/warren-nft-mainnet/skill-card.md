## Description: <br>
Deploy NFT collections permanently on MegaETH mainnet. Images are stored on-chain via SSTORE2, then published through WarrenContainer and WarrenLaunchedNFT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[planetai87](https://clawhub.ai/user/planetai87) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and NFT collection creators use this skill to prepare and execute MegaETH mainnet NFT collection deployments with on-chain image storage and Warren launchpad registration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a wallet private key to sign irreversible MegaETH mainnet transactions. <br>
Mitigation: Use a fresh wallet funded only with the ETH needed for deployment, prefer PRIVATE_KEY in the environment, and review all collection parameters before running commands. <br>
Risk: The deployment flow can auto-mint a prerequisite 0xRabbit.agent key and spend mainnet gas. <br>
Mitigation: Confirm the configured contract addresses, wallet balance, and Genesis access settings before executing the deployment script. <br>
Risk: Collection metadata is posted to the Warren registration API by default after deployment. <br>
Mitigation: Review the metadata before deployment and override or unset REGISTER_API when registration should not be attempted. <br>


## Reference(s): <br>
- [Warren](https://thewarren.app) <br>
- [MegaETH Mainnet RPC](https://mainnet.megaeth.com/rpc) <br>
- [MegaETH Blockscout Explorer](https://megaeth.blockscout.com) <br>
- [Warren Mint](https://thewarren.app/mint) <br>
- [ClawHub Skill Page](https://clawhub.ai/planetai87/warren-nft-mainnet) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment commands and configuration guidance for running a Node.js NFT deployment script.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
