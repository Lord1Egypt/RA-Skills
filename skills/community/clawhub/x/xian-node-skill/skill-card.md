## Description:

Set up and manage Xian blockchain nodes for mainnet or testnet deployment, custom network creation, CometBFT configuration, and node monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[endogen](https://clawhub.ai/user/endogen)

### License/Terms of Use:


## Use Case:

Developers and node operators use this skill to deploy and manage Xian blockchain nodes, including joining mainnet or testnet, creating a custom network, configuring validator or service nodes, and checking sync status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validator private keys may be exposed if pasted into agent chats, shell histories, logs, or stdout-captured environments.

Mitigation: Avoid pasting private keys into prompts or commands, generate keys only in an isolated environment, disable stdout logging for key generation, and move secrets through approved secret-handling workflows.

Risk: Building or running upstream node software without review can introduce supply-chain or operational risk.

Mitigation: Pin and review upstream Xian and CometBFT-related code before building, and run the node in an isolated environment.

Risk: Wipe and reset commands can remove local blockchain data or configuration state.

Mitigation: Back up node configuration and required chain data before running wipe, reset, or rebuild workflows.

## Reference(s):

- [Genesis File Template](references/genesis-template.md)
- [Xian Stack](https://github.com/xian-network/xian-stack)
- [Xian Core](https://github.com/xian-network/xian-core)
- [Xian Python SDK](https://github.com/xian-network/xian-py)
- [CometBFT Documentation](https://docs.cometbft.com/)
- [Xian Project Site](https://xian.org)
- [ClawHub Skill Page](https://clawhub.ai/endogen/skills/xian-node-skill)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash, Python, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes node setup commands, monitoring commands, troubleshooting guidance, and helper scripts for validator key generation and node status checks.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
