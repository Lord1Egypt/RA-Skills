## Description:

Analyze data with `toxicity-structure-alert` using a reproducible workflow, explicit validation, and structured outputs for review-ready interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and scientific reviewers use this skill to screen molecular SMILES inputs for known toxic structural alerts, risk levels, and follow-up recommendations. It supports bounded, reviewable toxicity triage and should not replace comprehensive toxicology assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Toxicity alerts are screening guidance and may include false positives or false negatives.

Mitigation: Use results as triage input only and confirm with full toxicology review, validated assays, or complementary ADMET tools.

Risk: The workflow depends on molecular structure input quality and RDKit availability; invalid SMILES or degraded matching can reduce result reliability.

Mitigation: Validate SMILES inputs, run the documented smoke check in an isolated environment, and prefer reviewed or pinned dependencies.

## Reference(s):

- [Toxicity Structure Alert on ClawHub](https://clawhub.ai/aipoch-ai/skills/toxicity-structure-alert)
- [Runtime Checklist](references/runtime_checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text or JSON toxicity alert reports with risk scores, matched alerts, recommendations, and executable command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports basic, standard, and full detail levels; high-risk findings may produce a non-zero command exit code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
