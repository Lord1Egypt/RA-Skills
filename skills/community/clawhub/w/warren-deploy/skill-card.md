## Description: <br>
Deploy websites and files permanently on MegaETH blockchain. AI agents stress test the network by deploying HTML on-chain using SSTORE2 bytecode storage. Agents pay their own gas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[planetai87](https://clawhub.ai/user/planetai87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to deploy HTML, files, and simple website content to the MegaETH testnet as permanent public on-chain records for Warren stress-test workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment flow handles a wallet private key. <br>
Mitigation: Use a fresh burner MegaETH testnet wallet only, never a valuable or mainnet wallet key, and prefer a temporary PRIVATE_KEY environment variable over passing the key as a command-line argument. <br>
Risk: Deployed content becomes public and effectively permanent on-chain. <br>
Mitigation: Deploy only content that is safe to publish permanently and review files before submitting them to the deployment script. <br>
Risk: The setup flow installs npm dependencies. <br>
Mitigation: Run setup in an isolated folder and review the dependency install before using the deploy script. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/planetai87/warren-deploy) <br>
- [Warren homepage](https://megawarren.xyz) <br>
- [MegaETH testnet faucet](https://docs.megaeth.com/faucet) <br>
- [MegaETH testnet explorer](https://megaeth-testnet-v2.blockscout.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON deployment results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment instructions and a transaction result containing tokenId, rootChunk, depth, and a Warren loader URL.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
