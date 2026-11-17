## Description:

Provides ISO 14971 medical device risk management guidance for planning, hazard analysis, risk evaluation, risk control, residual risk assessment, and post-production monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayangai](https://clawhub.ai/user/ayangai)

### License/Terms of Use:

MIT-0

## Use Case:

Medical device quality, regulatory, and engineering teams use this skill to structure ISO 14971 risk management work across the product lifecycle, including risk plans, hazard analysis, FMEA/FTA/HAZOP method selection, risk controls, ALARP rationale, benefit-risk analysis, and post-market monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a boundary-case classification bug in FMEA RPN threshold handling.

Mitigation: Review and fix the threshold handling before relying on calculator output, or manually classify RPN values at 50 and 100 according to the organization's approved risk policy.

Risk: Medical-device risk documentation can be product-specific and safety-critical.

Mitigation: Have qualified quality, regulatory, or clinical reviewers validate generated risk plans, analyses, controls, residual-risk conclusions, and post-production triggers before using them as controlled documentation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ayangai/skills/risk-management-iso14971)
- [ISO 14971 Implementation Guide](artifact/references/iso14971-implementation-guide.md)
- [Risk Analysis Methods](artifact/references/risk-analysis-methods.md)
- [Risk Assessment Templates](artifact/references/riREDACTED-SECRET.md)
- [Risk Matrix Calculator](artifact/scripts/risk_matrix_calculator.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tables, reusable templates, shell command examples, and optional text or JSON calculator output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local ISO 14971-style risk matrix and FMEA RPN calculator behavior; evidence reports no hidden access or persistence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
