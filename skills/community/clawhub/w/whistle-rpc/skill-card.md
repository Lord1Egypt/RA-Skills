## Description:

Production Solana RPC for AI agents with unlimited JSON-RPC, WebSocket access, DEX data, historical APIs, and a 1 SOL/month on-chain subscription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dylanport](https://clawhub.ai/user/dylanport)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Whistle RPC to connect AI agents to Solana JSON-RPC, WebSocket subscriptions, DEX market data, historical transaction APIs, and paid subscription management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm CLI execution could introduce supply-chain risk.

Mitigation: Pin and verify the npm CLI package before running subscription commands.

Risk: API keys placed in URLs can leak through logs, browser history, or monitoring systems.

Mitigation: Prefer the documented X-API-Key or Authorization header options instead of query parameters.

Risk: Subscription and renewal flows require real SOL payments on mainnet.

Mitigation: Require explicit human confirmation of amount and recipient before signing, and use a dedicated low-value wallet.

## Reference(s):

- [Whistle RPC ClawHub listing](https://clawhub.ai/dylanport/skills/whistle-rpc)
- [Whistle website](https://whistle.ninja)
- [Whistle RPC NPM CLI](https://npmjs.com/package/whistle-rpc)
- [Whistle tools manifest](https://whistle.ninja/tools.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with endpoint, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint URLs, API-key placement options, subscription status checks, and human-confirmation guidance for Solana payments.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter says 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
