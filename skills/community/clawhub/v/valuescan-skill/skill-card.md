## Description:

ValueScan Skill helps agents query cryptocurrency market data, including token search, candlesticks, major fund-flow analysis, on-chain data, sentiment, and market indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[valuescan-io](https://clawhub.ai/user/valuescan-io)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to access ValueScan cryptocurrency data for market monitoring, token analysis, fund-flow review, on-chain activity checks, and API-backed research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included SDK can attach signed API credentials to a non-ValueScan URL if a caller passes an absolute path.

Mitigation: Harden SDK usage so signed headers are only sent to https://api.valuescan.io/api/open/v1 paths.

Risk: Broad market-analysis prompts may trigger paid ValueScan API requests.

Mitigation: Confirm intended endpoints, account credit impact, and user authorization before making broad or repeated calls.

Risk: Outputs are financial data signals and may be mistaken for guaranteed trading advice.

Mitigation: Treat results as informational signals and require independent review before investment or trading decisions.

## Reference(s):

- [ValueScan Homepage](https://www.valuescan.ai)
- [ValueScan API Documentation](https://claw.valuescan.io)
- [ValueScan Developer Portal](https://www.valuescan.ai/dev-portal/home/)
- [ValueScan Skill on ClawHub](https://clawhub.ai/valuescan-io/skills/valuescan-skill)
- [API Reference Files](references/)
- [Signing SDK README](script/sdk/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request examples, JSON response interpretation, and optional JavaScript signing code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated ValueScan API calls that consume account credits.]

## Skill Version(s):

1.0.7 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
