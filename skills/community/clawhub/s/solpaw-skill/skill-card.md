## Description:

Launch Solana tokens on Pump.fun via the SolPaw platform. 0.1 SOL one-time fee. Your wallet is the onchain creator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvcidpsyche](https://clawhub.ai/user/lvcidpsyche)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use this skill to prepare and execute Solana token launches on Pump.fun through SolPaw, including API registration, fee payment, metadata/image handling, transaction signing, and launch submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a real fund-moving token launch workflow and requests high-impact wallet/private-key authority.

Mitigation: Use only a dedicated low-balance wallet, never provide a main-wallet private key, and manually confirm every fee payment and signed transaction.

Risk: Server security evidence reports inconsistent token-creator claims around the launch path.

Mitigation: Verify that the actual launch path preserves the intended wallet as the on-chain creator before paying the 0.1 SOL fee.

Risk: Launch fees and token creation actions may be irreversible after execution.

Mitigation: Confirm the token name, symbol, description, recipient wallet, and all fee amounts before initiating payment or submitting a signed transaction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvcidpsyche/skills/solpaw-skill)
- [SolPaw homepage](https://solpaw.fun)
- [SolPaw API reference](references/api-docs.md)
- [SolPaw API info](https://api.solpaw.fun/api/v1/info)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration]

**Output Format:** [Markdown with inline bash, TypeScript, JSON, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include token launch details such as mint address, transaction signature, Pump.fun URL, Solscan URL, fee details, or error messages.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
