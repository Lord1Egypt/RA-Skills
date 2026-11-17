## Description:

Veroq provides verified AI intelligence for markets, assets, sentiment, economic data, web content, and claim fact-checking through OpenClaw commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnytarrr](https://clawhub.ai/user/johnnytarrr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to request sourced market intelligence, fact-check claims, retrieve live prices and indicators, analyze portfolios, and generate briefs or reports from VEROQ data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts, private URLs, research questions, portfolio holdings, or trading strategies may be sent to api.veroq.ai.

Mitigation: Review the skill before installation, avoid confidential inputs unless this data flow is acceptable, and disclose the external API dependency to users.

Risk: Trading, market, forecast, and portfolio outputs may be incomplete, stale, or mistaken for financial advice.

Mitigation: Treat outputs as decision support only, verify important claims and numbers against authoritative sources, and require human review before financial decisions.

Risk: The optional self-hosted Docker path depends on an external container image.

Mitigation: Use the self-hosted option only after pinning and verifying the image digest and reviewing the deployment configuration.

## Reference(s):

- [ClawHub Veroq skill page](https://clawhub.ai/johnnytarrr/skills/veroq)
- [VeroQ](https://veroq.ai)
- [VeroQ OpenClaw integration](https://veroq.ai/integrations/openclaw)
- [VeroQ API Reference](https://veroq.ai/api-reference)
- [VeroQ Developers](https://veroq.ai/developers)
- [veroq-mcp npm package](https://www.npmjs.com/package/veroq-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text and Markdown command responses with summaries, evidence, verdicts, confidence scores, market metrics, alerts, and report links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include live or generated intelligence, third-party API results, source or evidence lists, confidence values, and trading-related signals; outputs should be reviewed before financial or other high-impact use.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
