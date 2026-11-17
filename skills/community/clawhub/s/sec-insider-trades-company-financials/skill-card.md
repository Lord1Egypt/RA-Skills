## Description:

SEC filings, insider trades, company financials, and recent market-wide filings for AI agents working with US-listed companies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colinhughes2121](https://clawhub.ai/user/colinhughes2121)

### License/Terms of Use:

MIT-0

## Use Case:

External agents, developers, and financial research workflows use this skill to retrieve SEC EDGAR profiles, insider transactions, 8-K events, headline financials, recent form filings, and SEC 360 summaries for equity research and due diligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes paid per-call HTTPS requests using x402 and USDC.

Mitigation: Confirm the payment model before installation and configure wallet or agent spending limits where available.

Risk: SEC and financial data may influence research, diligence, or trading decisions.

Mitigation: Treat returned data as research input, verify material decisions against authoritative filings, and avoid fully automated trading actions based only on this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colinhughes2121/skills/sec-insider-trades-company-financials)
- [GoCreative API endpoint](https://api.gocreativeai.com)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [JSON API responses with concise agent-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid HTTPS GET calls using x402 USDC payments; no API key or signup is described.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
