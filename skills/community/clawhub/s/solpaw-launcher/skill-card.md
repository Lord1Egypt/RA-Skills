## Description:

Launch Solana tokens on Pump.fun via the SolPaw platform. 0.1 SOL one-time fee. Your wallet is the onchain creator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvcidpsyche](https://clawhub.ai/user/lvcidpsyche)

### License/Terms of Use:

MIT

## Use Case:

External developers and OpenClaw agent operators use this skill to launch Solana tokens on Pump.fun through SolPaw after confirming token details, funding a dedicated wallet, and supplying the required API key and wallet configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to configure SOLANA_PRIVATE_KEY for a paid Solana token launch.

Mitigation: Use only a dedicated low-balance launch wallet, never provide a main wallet private key, and keep secrets in environment variables rather than code or chat.

Risk: The security evidence says the skill claims local signing while the shipped code uses a server-signed launch path.

Mitigation: Treat installation as sensitive until the publisher clarifies server-signed versus local-signing behavior, and require explicit human confirmation for every fee payment and token launch.

Risk: Raw exec dispatch can run commands that make authenticated API requests and trigger paid onchain actions.

Mitigation: Review the skill before deployment, restrict invocation to explicit user requests, and confirm token name, symbol, description, and fee payment before execution.

## Reference(s):

- [SolPaw API Reference](artifact/references/api-docs.md)
- [SolPaw Website](https://solpaw.fun)
- [SolPaw API Base URL](https://api.solpaw.fun/api/v1)
- [ClawHub Skill Listing](https://clawhub.ai/lvcidpsyche/skills/solpaw-launcher)
- [Pump.fun](https://pump.fun)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript, JSON, YAML, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include launch status, token mint addresses, Pump.fun URLs, Solscan URLs, and API error messages.]

## Skill Version(s):

3.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
