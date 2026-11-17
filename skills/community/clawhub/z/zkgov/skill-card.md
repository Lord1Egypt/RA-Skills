## Description:

Anonymous governance on HashKey Chain using zero-knowledge proofs. Query proposals, check voter status, register, create proposals, vote anonymously with ZK proofs, and finalize outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockchain-oracle](https://clawhub.ai/user/blockchain-oracle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect HashKey Chain governance activity and participate in ZKGov proposals through MCP tools or CLI commands, including registration, anonymous voting with ZK proofs, and proposal finalization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install mutable npm packages for MCP or CLI execution.

Mitigation: Pin reviewed @zkgov package versions and install them only in a sandboxed agent environment.

Risk: Write operations use persistent wallet key material and can submit on-chain transactions.

Mitigation: Keep only testnet funds in the wallet, protect any configured private key, and require explicit user confirmation before register, create, vote, or finalize actions.

Risk: Governance actions may be irreversible once submitted to the testnet contract.

Mitigation: Review proposal IDs, vote choices, wallet status, gas balance, and transaction intent before executing write tools.

## Reference(s):

- [ClawHub ZKGov skill page](https://clawhub.ai/blockchain-oracle/skills/zkgov)
- [@zkgov/mcp npm package](https://www.npmjs.com/package/@zkgov/mcp)
- [@zkgov/cli npm package](https://www.npmjs.com/package/@zkgov/cli)
- [HashKey Chain testnet RPC](https://testnet.hsk.xyz)
- [HashKey Chain testnet explorer](https://testnet-explorer.hsk.xyz)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with MCP tool names, CLI commands, and JSON-oriented command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs CLI fallback calls to use --json for reliable agent parsing.]

## Skill Version(s):

0.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
