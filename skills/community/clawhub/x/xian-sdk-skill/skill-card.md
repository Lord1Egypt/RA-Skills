## Description:

Build applications on the Xian blockchain using the xian-py Python SDK for wallets, transactions, smart contracts, state queries, token transfers, and sync or async workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[endogen](https://clawhub.ai/user/endogen)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build Xian blockchain applications that manage wallets, query state, send transactions, deploy and validate smart contracts, and implement sync or async SDK workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet examples involve private keys and mnemonics that could be exposed if copied into logs, transcripts, or shared code.

Mitigation: Treat private keys and mnemonics as secrets, avoid printing them, do not copy the shown private key, and keep examples in a dedicated environment.

Risk: Transaction, swap, and contract deployment examples can create irreversible blockchain effects when run against a live network.

Mitigation: Run examples on a local or test network first, and explicitly confirm recipient, amount, contract, and fees before using a live network.

## Reference(s):

- [Xian Contract Patterns](references/contract-patterns.md)
- [xian-py GitHub](https://github.com/xian-network/xian-py)
- [Xian Standard Contracts](https://github.com/xian-network/xian-standard-contracts)
- [Xian Project Site](https://xian.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No generated files are required by the skill itself.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
