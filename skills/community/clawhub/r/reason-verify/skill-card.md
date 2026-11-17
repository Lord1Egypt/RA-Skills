## Description:

A Python-only reasoning verification helper that extracts claims, checks contradictions, evaluates coverage, and optionally grounds claims against provided facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to review reasoning outputs for contradictions, missing coverage, numeric conflicts, and optional fact grounding before relying on or revising an answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports under-disclosed self-evolving capability registration.

Mitigation: Review before installing and remove or disable scripts/learner.py unless self-evolving registration is intended.

Risk: The release evidence reports overbroad activation language.

Mitigation: Narrow the read_when trigger to explicit reasoning verification, self-checking, contradiction detection, or fact-grounding requests before automatic loading.

Risk: The verifier uses heuristic checks and may miss issues or assign confidence that should not be treated as proof.

Mitigation: Use the report as review guidance and verify critical conclusions against the provided source facts or independent evidence.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Structured JSON report with concise text diagnostics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted claims, issue findings, reliability scores, grounding ratios, verdicts, and revision suggestions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
