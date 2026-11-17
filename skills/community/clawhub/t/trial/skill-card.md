## Description:

Send and receive KAS cryptocurrency. Check balances, send payments, generate wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manyfestation](https://clawhub.ai/user/manyfestation)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to operate a Kaspa command-line wallet, including balance checks, fee estimates, payment URI generation, wallet generation, and KAS transfers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wallet can move real KAS funds and the security verdict is suspicious due to weak safeguards.

Mitigation: Review the skill before installation or real-funds use, start on testnet or with small balances, and require manual out-of-band confirmation for every send.

Risk: Wallet mnemonics or private keys may be exposed through shell environments or agent-visible logs.

Mitigation: Avoid production secrets in shell environment variables or logs, and rotate credentials if exposure is suspected.

Risk: The wallet depends on an unpinned kaspa package and configurable RPC endpoints.

Mitigation: Pin and review the kaspa dependency before handling valuable wallets, and use only trusted wss:// RPC endpoints.

## Reference(s):

- [Kaspa Mainnet Transaction Explorer](https://explorer.kaspa.org/txs/{txid})
- [Kaspa Testnet Transaction Explorer](https://explorer-tn10.kaspa.org/txs/{txid})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return structured JSON and exit code 0 for success or 1 for errors.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
