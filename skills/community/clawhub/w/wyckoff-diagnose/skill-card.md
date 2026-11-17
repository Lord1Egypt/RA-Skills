## Description:

Wyckoff Diagnose analyzes Chinese A-share stock codes and produces stock diagnosis reports with Wyckoff phase, volume-profile levels, scores, ratings, and action suggestions for right-side trend and left-side accumulation views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxarch1980](https://clawhub.ai/user/dxarch1980)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate stock-analysis reports for six-digit Chinese A-share symbols, either one at a time or in batch. The reports summarize Wyckoff phase, volume-profile price levels, right-side trend and left-side accumulation scores, ratings, signals, and suggested actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-data requests may be routed through an undisclosed plaintext custom server with an embedded token.

Mitigation: Review the provider and endpoint before installation; prefer a version that documents providers, uses HTTPS, and loads credentials from user-controlled configuration.

Risk: Generated stock-analysis reports can be incorrect or misleading if market data is incomplete, stale, or unavailable.

Mitigation: Treat outputs as reference material rather than investment advice, and compare conclusions against authoritative market data before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxarch1980/skills/wyckoff-diagnose)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style plain text report with optional shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a six-digit Chinese A-share stock code or a batch file of stock codes and live market-data access.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
