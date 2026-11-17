## Description:

Helps identify when multiple attestation validators share training data, model architecture, organizational upstream, or similar reasoning traces, creating correlated blind spots that can make multi-validator attestation no stronger than a single validator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers, evaluators, and agent operators use this skill to assess whether multiple attestation validators provide independent judgment or share epistemic blind spots. It supports analysis from disclosed provenance, shared benchmark behavior, evasion transferability, and evaluation trace similarity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validator traces and provenance data may contain information users did not intend to submit for analysis.

Mitigation: Provide only validator traces, attestation results, and provenance details that are authorized for this analysis.

Risk: The evidence says the artifact is markdown-only but declares curl and python3 requirements that are not explained by the current instructions.

Mitigation: Review requested tool use before granting execution access and avoid enabling unnecessary tools for this skill.

Risk: Correlation scores can be misleading when baselines are poorly calibrated or validators converge on objectively correct reasoning.

Mitigation: Calibrate baselines on comparable edge cases and treat the result as correlation risk analysis, not proof of evasion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/validator-correlated-judgment)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown correlation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report may include provenance overlap assessment, similarity scores, evasion transferability estimates, effective independent validator count, a correlation verdict, and a detection method.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
