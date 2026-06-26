## Description: <br>
Query and interact with the QELT blockchain via JSON-RPC for blocks, transactions, wallet balances, smart contract calls, gas estimation, event logs, nonces, and pre-signed raw transaction submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PRQELT](https://clawhub.ai/user/PRQELT) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to query QELT Mainnet and Testnet state, inspect transactions and contracts, estimate gas, retrieve logs, and submit user-provided pre-signed raw transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A pre-signed transaction broadcast can execute irreversible mainnet activity if the network or transaction contents are not confirmed. <br>
Mitigation: Confirm mainnet versus testnet, recipient, contract call, value, and signed transaction contents before any raw transaction submission. <br>
Risk: Private keys or seed phrases could be exposed if a user provides signing material. <br>
Mitigation: Do not request, store, print, or transmit private keys or mnemonics; only accept pre-signed raw transaction hex. <br>
Risk: Live RPC requests may be rate-limited or unavailable, especially broad historical log queries. <br>
Mitigation: Use archive endpoints for historical or TRACE requests, bound log ranges, page scans, and apply backoff for 429 or 503 responses. <br>


## Reference(s): <br>
- [ClawHub QELT Blockchain release](https://clawhub.ai/PRQELT/qelt-blockchain) <br>
- [QELT documentation](https://docs.qelt.ai) <br>
- [QELT Network Reference](artifact/references/network.md) <br>
- [QELT block explorer](https://qeltscan.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON-RPC examples and curl command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and network access to QELT RPC endpoints; write operations require a pre-signed raw transaction.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
