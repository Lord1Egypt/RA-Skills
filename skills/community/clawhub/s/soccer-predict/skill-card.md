## Description:

Soccer Predict is a football match betting prediction skill that gathers Titan007 match data, applies a five-step quantitative framework, and produces betting recommendations, expected value analysis, predicted scores, and post-match review outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superluigi0309](https://clawhub.ai/user/superluigi0309)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts can use this skill to collect football match data, calculate odds-derived probabilities, compare model predictions, and review post-match outcomes. It is intended for uncertain analytical guidance around football betting markets, not as guaranteed financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce football betting recommendations that may be mistaken for certain or financial advice.

Mitigation: Treat outputs as uncertain analysis, require independent review before any real-money wagering, and avoid automated action on recommendations.

Risk: Post-match review can write persistent football prediction memory files across sessions.

Mitigation: Confirm before allowing memory writes and periodically inspect or delete football prediction memory files.

Risk: The README install example uses an unpinned installer command.

Mitigation: Use a pinned or verified installer command and review package source before installation.

## Reference(s):

- [Soccer Predict on ClawHub](https://clawhub.ai/superluigi0309/skills/soccer-predict)
- [Data Collection Guide](references/data-collection.md)
- [Prediction Framework](references/prediction-framework.md)
- [Post-Match Review & Learning Framework](references/review-framework.md)
- [Titan007 Match Analysis Source](https://zq.titan007.com/)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, html, guidance]

**Output Format:** [Concise text summaries or detailed Markdown/HTML reports with odds tables, probability estimates, EV values, betting recommendations, predicted scores, and post-match review notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write cross-session football prediction memory files during post-match review and learning.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
