## Description: <br>
This skill provides comprehensive guidance and tools for conducting pharmacoeconomic evaluations including cost-effectiveness analysis (CEA), cost-utility analysis (CUA), cost-benefit analysis (CBA), sensitivity analysis, and decision-analytic model construction (Markov, decision tree, DES, PSM). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tlb1201](https://clawhub.ai/user/tlb1201) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan pharmacoeconomic evaluations, calculate ICERs and QALYs, run deterministic or probabilistic sensitivity analyses, and structure decision-analytic models for HTA, reimbursement, pricing, or health economics research. <br>

### Deployment Geography for Use: <br>
Global; outputs include China-specific defaults and should be adapted to the target jurisdiction and payer context. <br>

## Known Risks and Mitigations: <br>
Risk: China-specific defaults or thresholds may be misapplied to another jurisdiction, payer, or policy context. <br>
Mitigation: Confirm the target jurisdiction, payer perspective, thresholds, discount rates, and utility sources with qualified health economics experts before relying on results. <br>
Risk: Local pharmacoeconomic calculations can produce misleading decision support when assumptions, parameter sources, or model structure are incomplete. <br>
Mitigation: Document all input sources, validate model assumptions, run sensitivity analyses, and review conclusions with qualified health economics experts. <br>
Risk: The release evidence includes purchase and crypto capability tags that are not needed for the documented local analysis workflow. <br>
Mitigation: Run the skill in an isolated Python environment and do not grant purchase, payment, wallet, or crypto capabilities. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tlb1201/skill-pharmacoeconomic-evaluation) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown guidance with Python code examples and local calculation results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on user-supplied clinical, cost, utility, threshold, and jurisdiction assumptions.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
