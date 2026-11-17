## Description:

Uses Tavily Search to retrieve gold market information across exchange, bank account gold, London precious metals, and retail gold price sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fmouseboy](https://clawhub.ai/user/fmouseboy)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and external users use this skill to gather current gold price, news, technical, and fundamental signals and produce neutral informational market commentary. It is intended for analysis support, not personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends gold-related search requests to Tavily using TAVILY_API_KEY.

Mitigation: Use it only where Tavily use is approved, provide the key through a scoped environment variable, and rotate or revoke the key if it is exposed.

Risk: Gold market commentary can be mistaken for personalized financial advice.

Mitigation: Present outputs as informational analysis only and require human review before making financial decisions.

Risk: Default Chinese-language output may not be suitable for every audience.

Mitigation: Translate or localize the report before sharing with users who need another language.

## Reference(s):

- [sudo-gold ClawHub Skill](https://clawhub.ai/fmouseboy/skills/sudo-gold)
- [Gold Technical Indicators Reference](artifact/references/technical-indicators.md)
- [Tavily Search API Endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Chinese-language console text or Markdown-style analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Tavily search results; output is informational market commentary and defaults to Chinese.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
