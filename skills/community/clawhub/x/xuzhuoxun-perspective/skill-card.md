## Description:

Provides a Chinese-language, stylized A-share market analysis framework based on Xu Zhuoxun's investment models, heuristics, cases, and trading psychology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinkpeace](https://clawhub.ai/user/thinkpeace)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer A-share market questions in Chinese with a structured investment-framework style covering market analysis, strategy, trading psychology, position sizing, trend judgment, fund flows, and risk discipline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the stylized first-person persona for the real fund manager speaking.

Mitigation: Disclose that outputs are AI-generated educational commentary and avoid representing responses as statements from the real person.

Risk: Action-oriented trading, stop-loss, or position-sizing guidance can be misconstrued as personalized financial advice.

Mitigation: Keep outputs educational, include clear risk warnings when trading guidance appears, and require users to make independent investment decisions.

Risk: Market commentary can become stale or misleading when timely A-share data is unavailable.

Mitigation: Use current, cited market data for time-sensitive claims, or state uncertainty and avoid definitive trade calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thinkpeace/skills/xuzhuoxun-perspective)
- [Publisher profile](https://clawhub.ai/user/thinkpeace)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Core mental models](artifact/references/models/01-odds-over-probability.md)
- [Spring theory](artifact/references/models/02-spring-theory.md)
- [Capital flow indicators](artifact/references/models/10-capital-flow-indicators.md)
- [Decision heuristics: loss-based sizing](artifact/references/heuristics/01-loss-based-sizing.md)
- [Decision heuristics: stop-loss discipline](artifact/references/heuristics/02-two-night-stop.md)
- [Trading psychology](artifact/references/psychology/00-index.md)
- [Historical cases](artifact/references/cases/00-index.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language Markdown prose with conclusion, reasons, evidence, and action steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include educational market commentary, risk warnings, and position-sizing or stop-loss guidance; should not provide personalized financial advice or individual stock buy/sell calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
