## Description: <br>
Helps identify when multiple attestation validators share training data, model architecture, organizational upstream, or reasoning patterns that create correlated blind spots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and agent operators use this skill to assess whether multiple attestation validators provide independent judgment or share epistemic blind spots. It supports provenance, behavioral, evasion-transferability, and evaluation-trace correlation analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validator reports, provenance details, and evaluation traces may reveal internal review methods or security assumptions. <br>
Mitigation: Use only materials the operator is authorized to share and redact sensitive review details before analysis. <br>
Risk: Correlation findings can be misleading when provenance is incomplete or trace and behavioral baselines are not calibrated. <br>
Mitigation: Treat the report as decision support and review conclusions against available provenance, test design, and case difficulty before changing attestation policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/validator-correlated-judgment) <br>
- [Skill source artifact](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown correlation report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include provenance overlap, model and fine-tuning similarity, behavioral correlation, trace similarity, evasion transferability, effective independent validator count, verdict, and detection method.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
