## Description:

Get UK (London Stock Exchange, LSE) market data via FinanceAgent on OneKey Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query London Stock Exchange market data for one or more LSE ticker symbols through the OneKey Gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install and example commands create supply-chain risk through the OneKey Gateway package and command resolution.

Mitigation: Install only if the OneKey Gateway and @aiagenta2z npm package publisher are trusted; prefer a pinned, local install over global npm installation or npx auto-resolution.

Risk: The example HTTP command can expose the OneKey Gateway API key in verbose curl output, logs, or shell history.

Mitigation: Remove curl verbose mode before using a real key, avoid logging secrets, and rotate the key if it may have been captured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/uk-stock-market-lse)
- [OneKey Gateway agent router endpoint](https://agent.deepnlp.org/agent_router)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with shell commands and JSON request/response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a OneKey Gateway API key; returned market data fields depend on the upstream data source.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
