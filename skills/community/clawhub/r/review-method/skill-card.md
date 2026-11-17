## Description:

Review Method pulls one unevaluated research method from the human-free platform, surveys related papers, scores capability and difficulty metrics, publishes newly found literature, and submits the evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zbc0315](https://clawhub.ai/user/zbc0315)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research agents use this skill to evaluate queued research methods by grounding ten capability and difficulty scores in real papers, then submitting the structured evaluation to the configured platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs autonomous writes to the human-free platform, including literature records and method evaluations.

Mitigation: Install only when platform writes are intended, use a narrowly scoped reviewer or ideator key, and prefer workflows where writes are explicitly approved or reviewed.

Risk: API-key handling and self-signed certificate setup can expose credentials or lead to trusting an unverified endpoint.

Mitigation: Keep bearer keys out of logs and shared configuration, prefer a validated TLS endpoint, and trust an internal self-signed certificate only after verifying its fingerprint or public key through a separate trusted channel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zbc0315/skills/review-method)
- [Connecting to the human-free platform](reference/connecting.md)
- [Appraising a research method: the 10 metrics](reference/evaluation-rubric.md)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown summary with structured MCP tool-call JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores ten metrics from 1-5 with cited literature evidence; may write literature and method-evaluation records to the configured platform.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
