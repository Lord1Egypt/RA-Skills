## Description: <br>
Home Reno Estimator helps agents estimate residential renovation costs from floor area, finish level, and city, then produce a structured budget report with line-item ranges, uncertainty notes, and data-source context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External homeowners, renovation planners, and agents use this skill to create fast residential renovation budget estimates for Chinese cities from area, finish grade, and location. The result is useful for early budget planning, contractor comparison, and identifying cost uncertainty before obtaining formal quotes. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The package includes marketing, payment, sharing, and unrelated business-guidance material beyond the core estimator. <br>
Mitigation: Install only when that collateral is desired; otherwise review the package contents and use only the estimator workflow. <br>
Risk: Users may disclose sensitive renovation details, budgets, contractor documents, contact details, or report screenshots while using or sharing outputs. <br>
Mitigation: Avoid posting exact addresses, contact details, budgets, contractor documents, or report screenshots publicly. <br>
Risk: Payment, sharing, referral, or off-platform messaging instructions may influence user behavior outside the estimator task. <br>
Mitigation: Treat those instructions as optional and require explicit user consent before taking any payment, sharing, referral, or off-platform messaging action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nic-yuan/vertical-home-reno-estimator) <br>
- [Data sources](references/data-sources.md) <br>
- [Renovation price data](references/price-data-2024.md) <br>
- [Sample output](SAMPLE-OUTPUT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown report with tabular cost ranges, caveats, next-step guidance, and JSON estimator data from a local Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and three user inputs: area, renovation grade, and city; estimates are advisory ranges rather than binding quotes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
