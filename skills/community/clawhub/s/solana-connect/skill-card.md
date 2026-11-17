## Description:

OpenClaw Solana Connect is a toolkit for AI agents to generate Solana wallets, read balances and transaction history, inspect token accounts, and prepare or send SOL transfers with configurable limits and dry-run support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seenfinity](https://clawhub.ai/user/seenfinity)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent builders use this skill to let OpenClaw agents query Solana account data and construct SOL transfer flows. It is most appropriate when dry-run simulation, transaction limits, trusted RPC configuration, and human review are kept in place before any live fund movement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move real SOL when dryRun is disabled.

Mitigation: Keep dryRun enabled by default, test with simulation first, and require explicit human approval before enabling live transfers.

Risk: Private-key and approval safeguards are weaker than the documentation claims.

Mitigation: Use only an isolated, trusted runtime and prefer a hardware wallet, custody service, or external signer instead of passing funded wallet private keys through an agent-facing API.

Risk: skipConfirmation can bypass the intended approval flow for live transfers.

Mitigation: Avoid skipConfirmation for live transfers and set conservative MAX_SOL_PER_TX and HUMAN_CONFIRMATION_THRESHOLD values.

Risk: A malicious or unreliable RPC endpoint can affect transaction data or submission behavior.

Mitigation: Configure SOLANA_RPC_URL to a trusted RPC endpoint and verify network selection before allowing live transactions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/seenfinity/skills/solana-connect)

## Skill Output:

**Output Type(s):** [Code, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and JSON-like result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SOLANA_RPC_URL, MAX_SOL_PER_TX, MAX_TOKENS_PER_TX, and HUMAN_CONFIRMATION_THRESHOLD environment configuration.]

## Skill Version(s):

3.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
