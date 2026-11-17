## Description:

Analyzes historical Chinese sports and welfare lottery data for supported games, including number statistics, omission analysis, trend summaries, recommendations, and prediction-history tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze lottery histories, summarize statistical patterns, generate entertainment-oriented recommendations, and record prediction outcomes for model-weight updates. Outputs should not be treated as betting, financial, or probability advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes an under-disclosed payment module with a hardcoded SkillPay bearer key and remote payment/account calls.

Mitigation: Review before installing; require the publisher to remove or rotate the embedded credential, document payment-service behavior, and ensure payment checks fail closed with explicit user control.

Risk: Lottery recommendations may be mistaken for betting advice even though the artifact states that lottery draws are independent random events.

Mitigation: Keep the gambling disclaimers visible, treat outputs as entertainment or data-analysis learning material, and do not use recommendations as betting, financial, or probability advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shenmeng/skills/shenmeng-lottery-predictor)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or text responses with statistical summaries, lottery-number recommendations, JSON-like analysis structures, and optional Python or shell snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local JSON configuration and prediction-history files under the skill data directory.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
