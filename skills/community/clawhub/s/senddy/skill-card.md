## Description:

Create and manage private stablecoin wallets using Senddy's zero-knowledge protocol on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattt21](https://clawhub.ai/user/mattt21)

### License/Terms of Use:

MIT

## Use Case:

Developers building payment agents, bots, and server-side apps use this skill to configure and operate private USDC wallets, transfers, withdrawals, transaction history, and persistent Senddy agent processes on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples include live fund-moving controls for private USDC transfers and withdrawals.

Mitigation: Use small test amounts first, add explicit confirmations and transfer limits, and review every integration before allowing production funds.

Risk: The agent seed controls wallet access and is shown as an environment-provided secret.

Mitigation: Store AGENT_SEED_HEX in real secret storage, restrict access to the runtime, and treat the seed like a private key.

Risk: The persistent daemon pattern can expose wallet operations if its HTTP interface is reachable by untrusted callers.

Mitigation: Bind the daemon only to a tightly controlled local channel, add authentication before wider exposure, and avoid exposing it beyond trusted hosts.

Risk: Copied examples may rely on unpinned dependencies or incomplete operational safeguards.

Mitigation: Pin dependencies, add request validation and error handling, and run security review before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mattt21/skills/senddy)
- [Senddy homepage](https://senddy.com)
- [Senddy support issues](https://github.com/senddy/senddy/issues)
- [Senddy Node API Reference](artifact/reference.md)
- [Senddy Node Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment variable requirements for SENDDY_API_KEY and AGENT_SEED_HEX.]

## Skill Version(s):

0.1.1 (source: evidence.release.version and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
