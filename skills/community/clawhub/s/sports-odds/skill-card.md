## Description:

Get live sports betting odds and compare lines across sportsbooks. Supports NFL, NBA, MLB, NHL, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianalloway](https://clawhub.ai/user/ianalloway)

### License/Terms of Use:

MIT-0

## Use Case:

Sports fans, analysts, and developers use the skill to retrieve current odds for supported sports and compare moneyline, spread, and totals markets across sportsbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key is included in request URLs and could appear in shared logs.

Mitigation: Use your own Odds API key and keep expanded request URLs out of shared logs.

Risk: Repeated requests can consume the API request allowance.

Mitigation: Cache responses and monitor the API usage headers.

## Reference(s):

- [The Odds API](https://the-odds-api.com/)
- [sports-odds on ClawHub](https://clawhub.ai/ianalloway/skills/sports-odds)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [Sports odds data and cross-book comparisons as JSON or concise text, with shell command examples in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live results depend on the selected sport, region, market, and API availability.]

## Skill Version(s):

0.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
