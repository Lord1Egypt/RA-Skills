## Description:

Launch Solana tokens on Pump.fun via the SolPaw platform. 0.1 SOL one-time fee. Your wallet is the onchain creator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvcidpsyche](https://clawhub.ai/user/lvcidpsyche)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent operators use this skill to configure an OpenClaw agent to launch Solana tokens on Pump.fun through SolPaw, including registration, fee payment, metadata upload, and launch requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for wallet-key access and broad shell execution while performing real Solana token launches.

Mitigation: Use a dedicated low-balance wallet, never expose a primary wallet private key to the agent environment, and review proposed commands before execution.

Risk: Launches, fees, metadata uploads, initial buys, and related onchain actions are public and irreversible.

Mitigation: Require explicit user approval for token name, symbol, description, fee payment, endpoint, transaction details, and launch submission.

Risk: The security review notes that the implementation does not fully match its creator-control claims.

Mitigation: Align the implementation with the promised local creator flow, avoid SOLANA_PRIVATE_KEY where possible, and verify signing behavior before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvcidpsyche/skills/solpaw-skill-final)
- [SolPaw API Reference](artifact/references/api-docs.md)
- [SolPaw homepage](https://solpaw.fun)
- [SolPaw API info endpoint](https://api.solpaw.fun/api/v1/info)
- [Pump.fun](https://pump.fun)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown instructions with bash and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SOLPAW_API_KEY, SOLPAW_CREATOR_WALLET, SOLANA_PRIVATE_KEY, and curl.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
