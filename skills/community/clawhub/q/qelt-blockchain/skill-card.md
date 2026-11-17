## Description:

Query and interact with the QELT blockchain (Chain ID 770) via JSON-RPC. Use when asked about blocks, transactions, wallet balances, smart contract calls, gas estimation, event logs, nonces, or raw transaction submission. Covers QELT Mainnet (770) and Testnet (771).

This skill is ready for commercial/non-commercial use.

## Publisher:

[prqelt](https://clawhub.ai/user/prqelt)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to query QELT mainnet or testnet state, inspect blocks and transactions, estimate gas, retrieve event logs, prepare MetaMask network configuration, and submit pre-signed raw transactions through JSON-RPC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A vulnerable event-log shell example can allow a malicious RPC response to become local Python execution.

Mitigation: Validate RPC results as expected hex data before conversion and avoid inserting RPC output directly into executable Python snippets.

Risk: Submitting a pre-signed mainnet transaction can irreversibly broadcast the user's intended action.

Mitigation: Confirm the network, destination, value, calldata, and user intent before any raw transaction submission.

Risk: Unbounded event-log requests can time out or be rate-limited.

Mitigation: Use bounded block ranges and page historical scans through the archive endpoint.

## Reference(s):

- [QELT Documentation](https://docs.qelt.ai)
- [QELT Network Reference](artifact/references/network.md)
- [QELT Block Explorer](https://qeltscan.ai)
- [QELT Mainnet RPC](https://mainnet.qelt.ai)
- [QELT Testnet RPC](https://testnet.qelt.ai)
- [ClawHub Skill Page](https://clawhub.ai/prqelt/skills/qelt-blockchain)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON-RPC curl commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for live JSON-RPC requests; transaction submission is limited to pre-signed raw transactions.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
