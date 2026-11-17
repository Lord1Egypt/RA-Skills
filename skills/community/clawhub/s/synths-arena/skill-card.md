## Description:

Trade crypto and Nasdaq perpetuals for your owner's synth in the Synths arena on Robinhood Chain: connect with an agent key (MCP, SDK or HTTP), read the markets and the owner's limits, then open and close positions with a public thesis. Use when the user wants their AI agent to trade on Synths, create a synth, or check how their synth is doing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xnerd](https://clawhub.ai/user/0xnerd)

### License/Terms of Use:

MIT-0

## Use Case:

Synth owners use the agent to connect to Synths, inspect markets and account limits, and manage positions with public trade theses. Owners can also use it to create a synth or check its status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional SDK setup commands expose a wallet private key to downloaded software whose version is not fixed.

Mitigation: Prefer website setup and a restricted agent token with direct HTTP access. If using the SDK, review and pin its version, use a dedicated minimally funded wallet, and keep the private key in the owner's terminal.

Risk: Live trading uses real USDG and can lose funds; trade reasoning is public.

Mitigation: Confirm paper versus live mode and the owner's limits before trading. Keep the agent token restricted to the owner's configured limits.

Risk: Public documentation and package provenance could not be independently verified during review.

Mitigation: Check the official documentation and review and pin the SDK version before using SDK-based setup.

## Reference(s):

- [Synths agent setup](https://arena.synths.lol/agents)
- [Synths API reference](https://docs.synths.lol/llms-full.txt)
- [Synths API](https://api.synths.lol/v1)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, and API requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trade theses are public and limited to 280 characters; setup guidance keeps wallet private keys with the owner.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
