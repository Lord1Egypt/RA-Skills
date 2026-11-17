## Description:

Stock Research Team (Simplified) helps an agent produce concise stock reviews for A-share, Hong Kong, and U.S. equities by combining market data, recent news, mandatory regulatory-event checks, technical levels, risks, and action-oriented ratings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanteng](https://clawhub.ai/user/tanteng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to prepare quick stock research for A-share, Hong Kong, and U.S. markets, including current price context, support and resistance, regulatory or penalty news, core thesis, risks, and buy/hold/sell style operating guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock ratings and operating suggestions could be mistaken for guaranteed financial advice.

Mitigation: Treat the output as investment research support and confirm market data, news, suitability, and risk tolerance before acting.

Risk: Recent regulatory, penalty, or policy search results may be incomplete or stale.

Mitigation: Confirm the mandatory regulatory-news search results against current authoritative sources before relying on a rating.

Risk: The manual upgrade path includes a deletion command that can remove the wrong local skill directory if copied carelessly.

Mitigation: Run deletion commands only after confirming the target path is the intended old skill installation.

## Reference(s):

- [Changelog](references/changelog.md)
- [Market Rules](references/market-rules.md)
- [Rating Criteria](references/rating-criteria.md)
- [Technical Indicators](references/technical-indicators.md)
- [Published ClawHub Skill Page](https://clawhub.ai/tanteng/skills/tanteng-stock-research)
- [Upstream Stock Research Team](https://clawhub.ai/skills/stock-research-team)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown stock research report with concise bullets and action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes rating, operating guidance, key levels, core thesis, and risks with regulatory events listed first.]

## Skill Version(s):

4.0.0 (source: server release metadata and changelog, released 2026-07-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
