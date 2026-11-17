## Description:

This skill answers broad A-share market hotspot questions by calling EastMoney's hotspot discovery service and returning a structured Markdown report covering market news, themes, and active stocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to ask general market-level questions such as today's hotspots, currently active stocks, or popular investment themes and receive a Markdown hotspot report. It is not intended for single-security diagnosis, fund diagnosis, quantitative modeling, or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends hotspot queries and the EM_API_KEY credential to EastMoney's service.

Mitigation: Install only if EastMoney is trusted with the API key and submitted queries; prefer a revocable key with limited scope where available.

Risk: Stock-market hotspot reports are time-sensitive and may be mistaken for investment advice.

Mitigation: Present reports as informational, keep risk notices visible, and return a clear error or uncertainty statement instead of fabricating content when the API fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/skills/stock-market-hotspot-discovery)
- [EastMoney Miaoxiang service](https://ai.eastmoney.com/mxClaw)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown report, optionally saved as a local .md file; errors are returned as short text messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY. The runtime prefers data.displayData from the EastMoney response and only saves a Markdown file when the API response contains valid report content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
