## Description:

This skill analyzes FinOps billing anomalies and cost changes, selecting relevant dimension, amount, or driver analysis based on the user's question and the current authorized identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT

## Use Case:

FinOps practitioners and cloud account users can use the skill to investigate billing increases or other cost changes, locate the products or dimensions behind an anomaly, and explain amount or usage and pricing drivers. It analyzes data through the current authorized identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is benign with medium confidence and notes that the skill's instruction scope, language constraint, and tool scope merit review; one component was only partially inspected.

Mitigation: Review the flagged constraints and tool scope for your environment, and inspect the partially reviewed component before installation.

## Reference(s):

- [Analysis State Protocol](artifact/references/analysis_state.md)
- [API Mapping](artifact/references/api_mapping.md)
- [RCA Orchestrator Design](artifact/references/rca_orchestrator_design.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Structured business explanation in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses tool-returned data for numeric conclusions; reports insufficient evidence or missing prerequisites when applicable.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
