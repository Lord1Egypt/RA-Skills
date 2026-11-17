## Description:

通过多维证据矩阵评估靶点药物并支持立项判断。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Biotech, pharma, university, and BD users use this skill to evaluate a target or target-indication opportunity through genetics, mechanism, clinical, competition, patent, and safety evidence for Go/Watch/Niche Go/No-Go triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs may be mistaken for clinical, investment, or legal advice.

Mitigation: Use the skill only for early R&D or BD decision support and route clinical, investment, and FTO conclusions to qualified reviewers.

Risk: Target, indication, or strategy inputs may be confidential.

Mitigation: Submit sensitive plans only when the configured pharma and patent MCP services are approved for that data.

Risk: Sparse evidence can lead to overconfident triage decisions.

Mitigation: Follow the artifact guardrail to emit Insufficient Evidence rather than a forced Go/No-Go decision when major evidence dimensions are missing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/target-drug-evidence-evaluation)
- [Scoring Rubric](references/scoring-rubric.md)
- [MCP Tool Map](references/mcp-tool-map.md)
- [Output Templates](references/output-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown with an executive verdict, scorecard, evidence matrix, and next actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires evidence-backed scoring; returns Insufficient Evidence when more than three dimensions lack usable data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
