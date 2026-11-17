## Description:

Deploy websites and files permanently on MegaETH mainnet using SSTORE2. Agents use their own wallet and pay gas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[planetai87](https://clawhub.ai/user/planetai87)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to deploy HTML or file content as permanent on-chain assets on MegaETH mainnet. It supports direct HTML strings, files, and stdin input, then returns deployment identifiers and a Warren viewer URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill signs real MegaETH mainnet transactions with a wallet private key, and those transactions are irreversible.

Mitigation: Use a dedicated low-balance deployment wallet, review the target network and content before execution, and expect all gas and minting costs to be paid from that wallet.

Risk: Passing private keys directly as command-line arguments or leaving them in the shell environment can expose credentials.

Mitigation: Prefer the PRIVATE_KEY environment variable over the --private-key argument, avoid pasting real keys into shell history, and unset sensitive variables after deployment.

Risk: Website or file content deployed by this skill is public, permanent, and immutable on mainnet.

Mitigation: Deploy only content that is ready for permanent publication and verify that it contains no secrets, private data, or material that may need later removal.

Risk: Dependency installation and deployment from the same shell can expose wallet credentials to local tooling.

Mitigation: Run setup in a clean environment without PRIVATE_KEY set, then set the deployment key only for the deployment command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/planetai87/skills/warren-deploy-mainnet)
- [Warren homepage](https://thewarren.app)
- [Warren source repository](https://github.com/planetai87/warren-tools)
- [MegaETH Blockscout explorer](https://megaeth.blockscout.com)
- [Warren mint page](https://thewarren.app/mint)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown instructions with bash commands and JSON deployment output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deployment output includes tokenId, rootChunk, depth, and a Warren viewer URL.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
