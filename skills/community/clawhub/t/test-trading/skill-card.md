## Description:

Trades a market when the user's estimated probability diverges from the live market price, with dry-run by default, context checks, reasoning tags, and optional live execution through AION.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssj124](https://clawhub.ai/user/ssj124)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent already has a probability estimate for a prediction market and needs a disciplined wrapper for dry-run analysis or explicitly enabled live execution. The skill compares the estimate with market context, reports risk alerts, and holds or trades when the configured edge threshold is met.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support live financial trading and token approval flows when explicitly enabled.

Mitigation: Run in dry-run mode by default, use minimal funds, pin dependencies, and require explicit operator approval for every live trade and token approval.

Risk: Reusable exchange credentials or API keys may be exposed, stored, or retained by external services.

Mitigation: Use an isolated environment, avoid printing or storing reusable credentials unless the service is trusted, and maintain a clear credential revocation process.

Risk: The manifest includes a managed cron schedule that could cause recurring execution.

Mitigation: Disable or avoid scheduled execution unless recurring trading behavior is intentional and monitored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssj124/skills/test-trading)
- [Publisher profile](https://clawhub.ai/user/ssj124)
- [Polymarket CLOB endpoint](https://clob.polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and operator-style text or JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to dry-run; live trading requires an explicit live flag and configured AION credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
