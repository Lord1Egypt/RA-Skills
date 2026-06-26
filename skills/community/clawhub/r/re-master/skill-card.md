## Description: <br>
Manage off-plan real estate investments with payment tracking, group buy equity, cash buffer simulation, investor sharing links, and ROI scenario modeling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Binkl69](https://clawhub.ai/user/Binkl69) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External investors, real estate agents, and developers use this skill to model Dubai off-plan property payment milestones, group buy ownership, admin cash buffer needs, and investor-facing reports. <br>

### Deployment Geography for Use: <br>
United Arab Emirates (Dubai) <br>

## Known Risks and Mitigations: <br>
Risk: Config files and generated reports can contain private financial details about investors, contributions, properties, and payment timing. <br>
Mitigation: Keep configs and reports private, scrub participant details before sharing, and share only investor-specific views when possible. <br>
Risk: Financial calculations or scenario outputs may be incorrect, incomplete, or misleading if inputs are stale or assumptions do not match the deal terms. <br>
Mitigation: Review outputs against source documents and current investment assumptions before using them for decisions or sharing them with investors. <br>
Risk: The included Python scripts execute local calculations from user-provided JSON configs. <br>
Mitigation: Run the scripts only with configs you trust and inspect unfamiliar configs before execution. <br>


## Reference(s): <br>
- [Dubai Off-Plan Real Estate Standards (2026)](references/dubai_standards.md) <br>
- [Equity Calculation Formulas](references/equity_formulas.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts emit JSON funding forecasts and equity percentages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Python scripts run locally against user-provided investment configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
