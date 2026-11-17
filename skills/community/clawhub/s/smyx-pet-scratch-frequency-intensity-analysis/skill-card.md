## Description:

Analyzes cat scratch-post videos to estimate scratching frequency, session duration, and relative intensity, returning structured behavioral observations without diagnosing disease or prescribing behavior changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and caretakers use this skill to summarize scratching frequency, session duration, and relative intensity from cat scratch-post videos. It provides behavioral observations and history reports for monitoring, not veterinary diagnoses or behavior-correction advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked this release suspicious over unresolved account and identity handling, history retrieval, and video processing behavior; this is not a finding of malicious intent.

Mitigation: Follow the scanner guidance and avoid installation until the author explains account creation, identity and token storage, history-listing behavior, and why export-only mode can still analyze video.

Risk: Relative intensity estimates can vary with camera angle and distance, and behavioral observations do not establish a health diagnosis.

Mitigation: Present results as approximate observations only; do not use them as a disease diagnosis or behavior-correction plan.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pet-scratch-frequency-intensity-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured JSON observations and Markdown summaries or history tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Intensity estimates are relative and can be affected by camera angle and distance; results are not veterinary diagnoses.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
