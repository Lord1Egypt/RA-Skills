## Description: <br>
Professional lease contract review for Taiwan rental agreements, including residential, commercial or storefront, and parking space leases, with clause checks for illegality, unfairness, and risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsaitepiao-alt](https://clawhub.ai/user/tsaitepiao-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, tenants, landlords, and property professionals use this skill to review Taiwan lease agreements before signing, compare clauses against residential, commercial, and parking lease references, and generate a structured Markdown review report from lease-clause JSON. <br>

### Deployment Geography for Use: <br>
Taiwan <br>

## Known Risks and Mitigations: <br>
Risk: Lease review inputs may contain names, addresses, financial terms, or other sensitive contract details. <br>
Mitigation: Use explicit local input and output paths, limit access to generated reports, and avoid sharing lease files with agents or services that are not approved for that data. <br>
Risk: The skill provides lease-review assistance and may not reflect every fact, jurisdictional nuance, or legal update relevant to a specific dispute. <br>
Mitigation: Review the generated report before relying on it and consult a qualified Taiwan legal professional for legal decisions or contested lease terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tsaitepiao-alt/taiwan-lease-review) <br>
- [Lease review report format](assets/review-report.md) <br>
- [Residential lease mandatory items](references/mandatory-items.md) <br>
- [Illegal lease clauses](references/illegal-clauses.md) <br>
- [Taiwan rental law summary](references/rental-law.md) <br>
- [Clause risk levels](references/risk-levels.md) <br>
- [Commercial lease considerations](references/commercial-lease.md) <br>
- [Parking lease considerations](references/parking-lease.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and optional generated Markdown report from structured JSON input] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included local script requires python3 and reads an input JSON path plus an output Markdown path.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
