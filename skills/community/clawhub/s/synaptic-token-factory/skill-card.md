## Description:

Deploy, mint, and trade autonomous SRC-20 tokens on SynapticChain Layer-1 in a single command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synaptics-lab](https://clawhub.ai/user/synaptics-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create and operate SRC-20 tokens on SynapticChain, including deployment, minting, transfers, approvals, and trading-related workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may perform real SynapticChain deploy, mint, or trade operations without clear confirmation safeguards.

Mitigation: Require explicit user confirmation before deploy, mint, or trade actions, and verify the intended network and wallet before execution.

Risk: Token operations can create financial or operational exposure through wallet use and on-chain state changes.

Mitigation: Use isolated wallets, limited balances, and spending limits where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/synaptics-lab/skills/synaptic-token-factory)
- [SynapticChain RPC endpoint](https://nodes.synapticchain.xyz/rpc)
- [SynapticChain block explorer](https://explorer.synapticchain.xyz)
- [SynapticChain Telegram](https://t.me/synapse402)

## Skill Output:

**Output Type(s):** [shell commands, guidance, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in real blockchain operations when commands are executed by an agent or operator.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
