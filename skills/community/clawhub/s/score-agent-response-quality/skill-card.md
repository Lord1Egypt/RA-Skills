## Description:

Scores an AI agent response 0-100 across six quality dimensions and returns targeted improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[operon](https://clawhub.ai/user/operon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, agent builders, and QA reviewers use this skill to evaluate a sample agent response for quality, monetization readiness, and actionable improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes vendor-specific monetization framing and Operon demand-pool claims.

Mitigation: Review monetization context separately and adjust expectations for the actual agent vertical and current advertiser availability.

Risk: Sample agent responses may contain personal or sensitive information.

Mitigation: Redact sensitive personal data before submitting a response for scoring.

Risk: The score is rubric-based and does not measure factual accuracy, RAG performance, latency, or hallucination rate.

Mitigation: Pair this review with domain-specific factuality, retrieval, latency, or hallucination evaluation when those qualities matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/operon/skills/score-agent-response-quality)
- [Operon homepage](https://operon.so)
- [Operon developer documentation](https://operon.so/developers?utm_source=skill-score-quality&utm_medium=skill&utm_campaign=skills-distribution)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with a score summary, dimension table, improvement list, and monetization context]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a normalized 0-100 score, six dimension notes, top three improvement suggestions, and monetization context.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
