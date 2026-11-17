## Description:

Predicts World Cup match outcomes and generates China Sports Lottery strategy analysis using Elo ratings, injury and weather factors, Polymarket calibration, and Beijing Time schedule handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deloyong](https://clawhub.ai/user/deloyong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze World Cup matches, compare model probabilities with market odds, and produce lottery strategy guidance for lawful China Sports Lottery analysis. Outputs should be treated as decision-support analysis, not guaranteed predictions or betting advice.

### Deployment Geography for Use:

Global, with China Sports Lottery features intended only where lawful.

## Known Risks and Mitigations:

Risk: The ClawHub security summary flags under-disclosed self-modification and broad packaging behavior.

Mitigation: Review or remove the auto_evolution modules before installation, and run evolve, tune, or apply commands only in an isolated worktree that does not contain secrets or unrelated files.

Risk: The security guidance calls out an exposed API key.

Mitigation: Treat the key as compromised if it belongs to you, rotate it, and replace embedded credentials with user-supplied secrets.

Risk: The skill can load local .pkl model files.

Mitigation: Load model files only from trusted sources and avoid accepting model artifacts from untrusted users.

Risk: Lottery and expected-value outputs may be mistaken for guaranteed betting outcomes.

Mitigation: Present outputs as analytical estimates, preserve the skill's gambling-risk disclaimers, and confirm local legal requirements before use.

## Reference(s):

- [yyWorldCup ClawHub Skill Page](https://clawhub.ai/deloyong/skills/yy-world-cup)
- [Comprehensive Data Model v3.1](docs/MODEL_v3.1.md)
- [Polymarket API Documentation](https://docs.polymarket.com/cn/api-reference/introduction)
- [balldontlie FIFA World Cup API](https://api.balldontlie.io/fifa/worldcup/v1/)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; generated prediction and strategy reports may be returned as plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external sports, weather, and market data APIs and may write local cache, model, or auto-evolution files when those modules are used.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
