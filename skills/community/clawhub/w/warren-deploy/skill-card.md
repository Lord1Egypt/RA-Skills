## Description:

Deploy websites and files permanently on MegaETH blockchain. AI agents stress test the network by deploying HTML on-chain using SSTORE2 bytecode storage. Agents pay their own gas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[planetai87](https://clawhub.ai/user/planetai87)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to deploy HTML or file content to the MegaETH testnet, producing permanent on-chain website records and URLs for Warren stress-test workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can sign wallet transactions for public, immutable on-chain deployments.

Mitigation: Use a brand-new disposable testnet wallet with no real assets or reused keys, and require explicit confirmation for every deployment.

Risk: Passing private keys on the command line can expose wallet credentials through shell history or process inspection.

Mitigation: Prefer the PRIVATE_KEY environment variable over the --private-key option, and keep the wallet limited to disposable testnet funds.

Risk: The setup script installs an npm dependency before deployment.

Mitigation: Review the ethers dependency and run setup in a controlled skill directory before allowing deployments.

Risk: Deployments spend gas and published content cannot be deleted.

Mitigation: Review content, size, and gas expectations before execution, and fund the wallet only with testnet ETH needed for the intended deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/planetai87/skills/warren-deploy)
- [Warren homepage](https://megawarren.xyz)
- [MegaETH faucet documentation](https://docs.megaeth.com/faucet)
- [MegaETH testnet explorer](https://megaeth-testnet-v2.blockscout.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, URLs, Guidance]

**Output Format:** [Markdown instructions with bash examples and JSON deployment results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, ethers.js, a disposable MegaETH testnet wallet, testnet ETH, and explicit operator review before spending gas.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
