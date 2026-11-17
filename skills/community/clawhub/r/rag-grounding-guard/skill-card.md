## Description:

Compares terms in RAG answer claims with supplied retrieved text and flags low-overlap claims for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use the skill to review whether claims in a RAG answer share terms with supplied retrieved sources, then inspect low-coverage claims and citations before relying on the answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Word overlap can give unsupported claims a high coverage score, and a matching term does not establish that a source entails a claim or that a citation is correct.

Mitigation: Review each claim against its source passage and check citations independently. Use the score as a triage aid, not as an automatic release or safety gate.

Risk: The checker does not enforce the documented file-access boundary, so supplied paths may reach files outside the intended project area.

Mitigation: Run it in a filesystem sandbox with explicitly approved, non-sensitive inputs, and verify that the host enforces the intended access limits.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/rag-grounding-guard)
- [LGD theory](https://github.com/zhaoxinghua09-cell/LGD)
- [Formal paper](https://doi.org/10.5281/zenodo.22456647)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Plain-text report with a coverage rate and covered or low-coverage claims]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses word overlap as a rough aid; manually verify factual support and citations.]

## Skill Version(s):

1.0.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
