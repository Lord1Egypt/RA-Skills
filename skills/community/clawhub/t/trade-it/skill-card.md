## Description:

Trade stocks, options, and crypto on brokerages, including Robinhood, ETrade, Charles Schwab, Webull, Public, Tastytrade, Coinbase, and Kraken, via the Trade It API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deanmauro](https://clawhub.ai/user/deanmauro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent builders use this skill to connect agents to Trade It for brokerage-backed account reads, holdings and trade lookup, draft trade creation, hosted review flows, and confirmed trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access brokerage data and authenticated trading paths, including create calls that may place real orders for some users.

Mitigation: Use deliberately limited accounts or hosted review flows, avoid immediate-placement settings, summarize order details, and require explicit user confirmation before execution.

Risk: The helper includes an authenticated generic tool execution path.

Mitigation: Do not expose generic tool execution in normal use; prefer the named account, draft, execution, and session commands with validated parameters.

Risk: Brokerage credentials and access tokens are sensitive.

Mitigation: Do not print tokens, keep redaction enabled, and allow users to revoke access through their brokerage or Trade It connection controls.

## Reference(s):

- [Trade It Homepage](https://tradeit.app)
- [ClawHub Skill Page](https://clawhub.ai/deanmauro/skills/trade-it)
- [API Reference](references/api-reference.md)
- [Enums and Constants](references/enums.md)
- [Integration Patterns](references/integration-patterns.md)
- [Examples](references/examples.md)
- [Security](references/security.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell command guidance, with JSON request and response shapes when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a required TRADEIT_ACCESS_TOKEN and redacts sensitive-looking response fields by default.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
