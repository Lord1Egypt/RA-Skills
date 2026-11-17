## Description:

This skill uses a technical-analysis framework distilled from public Chinese-language content by “来自股市的猩猩” to analyze A-share indices, market style, sector behavior, key levels, scenarios, and risk-aware market commentary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujiosk](https://clawhub.ai/user/wujiosk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market-analysis agents use this skill to draft Chinese-language A-share technical analysis, including morning, midday, closing, weekend strategy, and technical review formats. It is intended for general market commentary with explicit safeguards against impersonation, fabricated market data, certain-return claims, and personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be misused as personalized financial advice or treated as a promise of market outcomes.

Mitigation: Keep outputs framed as general technical analysis, include uncertainty and risk disclaimers, and avoid specific buy or sell instructions or guaranteed-return language.

Risk: A-share analysis is time-sensitive and can become misleading if based on stale or fabricated prices, volumes, or index levels.

Mitigation: Use current, verified market data and state the analysis timestamp and data cutoff before producing conclusions.

Risk: Style imitation could be mistaken for the original creator's own view or authorization.

Mitigation: State that outputs are based on a public-content style summary, do not speak as the creator, and do not claim private access or endorsement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wujiosk/skills/zhiyu)
- [Source Map and Identity Boundaries](artifact/references/source-map.md)
- [Method and Style Summary](artifact/references/method-and-style.md)
- [Corpus Findings](artifact/references/corpus-findings.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured Chinese-language prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include key levels, scenario trees, market observations, posture guidance, and risk disclaimers; requires current verified market data for time-sensitive analysis.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
