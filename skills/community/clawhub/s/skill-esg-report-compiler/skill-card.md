## Description:

Helps agents compile ESG reports by collecting and structuring company ESG data, mapping it to GRI and TCFD reference material, validating metric completeness, generating visualizations, and exporting PDF or HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Sustainability, reporting, and operations teams use this skill to prepare ESG disclosure materials from company-provided CSV, Excel, or JSON data. It supports report drafting and completeness checks, but its validation output should not be treated as formal GRI, TCFD, legal, or assurance advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML report export can embed untrusted ESG input without escaping, creating a report-viewing security risk.

Mitigation: Prefer PDF output for untrusted data, or sanitize and escape all text before HTML export; avoid hosting generated HTML on trusted domains.

Risk: The validation output is a basic completeness and range check, not formal GRI or TCFD compliance assurance.

Mitigation: Use the validation report as a drafting aid and have ESG, legal, or assurance specialists review final disclosures before publication.

## Reference(s):

- [Source repository](https://github.com/duding-engicool/skill-esg-report-compiler)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-esg-report-compiler)
- [GRI standards reference](references/gri_standards.md)
- [TCFD framework reference](references/tcfd_framework.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON, PNG, PDF, or HTML artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided ESG data and local Python dependencies such as pandas, matplotlib, and reportlab.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
