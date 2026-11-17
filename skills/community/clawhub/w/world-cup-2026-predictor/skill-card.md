## Description:

Bilingual football forecasting skill for pre-kickoff alerts, post-match review, and controlled model evolution from multi-book odds, market movement, Asian handicap, totals, BTTS, exact score, qualification, lineup, and news evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youjunzhao](https://clawhub.ai/user/youjunzhao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to produce disciplined English or Chinese football match forecasts, rolling pre-kickoff updates, and post-match reviews from timestamped market and news evidence. It also supports local calibration and controlled profile evolution after sufficient verified completed matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Football forecasts can be mistaken or interpreted as certainty.

Mitigation: Present probabilities as evidence-quality assessments, avoid guarantees or profit claims, and abstain when source coverage, freshness, or match context is insufficient.

Risk: Forecast and review commands can create local ledgers that mix match inputs with other local data.

Mitigation: Use a dedicated data directory for this skill, or use no-record options when local forecast or review records should not be written.

Risk: Promotion or rollback commands can change the local active model profile.

Mitigation: Run promote or rollback only as an intentional operator action after reviewing the completed-match evidence, metrics, and profile audit records.

Risk: Ambiguous odds formats, duplicated aggregator data, stale prices, or insufficient independent bookmakers can produce misleading forecasts.

Mitigation: Require declared odds formats, timestamps, underlying bookmaker identity, source deduplication, and the minimum independent-bookmaker threshold before treating a forecast as actionable.

## Reference(s):

- [Consensus Model](references/consensus-model.md)
- [Market Rules](references/market-rules.md)
- [Odds Formats](references/odds-formats.md)
- [Post-Match Review And Controlled Evolution](references/postmatch-evolution.md)
- [Source Policy](references/source-policy.md)
- [ClawHub Skill Page](https://clawhub.ai/youjunzhao/skills/world-cup-2026-predictor)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with optional JSON outputs from bundled Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the user's language, labels non-actionable forecasts, and may write local JSONL forecast or review records unless disabled with no-record options.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
