## Description:

United States federal income tax filing assistant for US citizens, resident aliens, and nonresident aliens that guides users through filer-type routing, form selection, amount calculations, IRS PDF form filling, and validation for federal returns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[irreel](https://clawhub.ai/user/irreel)

### License/Terms of Use:


## Use Case:

External users use this skill to prepare US federal income tax returns across citizen, resident alien, and nonresident alien workflows. It helps gather source-document facts, route income to federal forms and schedules, fill IRS PDFs with pypdf, and cross-check completed returns before filing.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill handles sensitive tax information, and the security summary advises avoiding unnecessary identifiers.

Mitigation: Collect only the tax facts needed for the requested workflow, avoid full SSNs or unnecessary personal identifiers, and confirm with the user before processing tax documents.

Risk: Generated tax calculations or filled forms may be incorrect or incomplete.

Mitigation: Manually verify all generated forms and cross-form totals against source documents before filing or submitting them.

Risk: The security summary notes a recommendation to install Python packages at the system level.

Mitigation: Install dependencies only in an isolated virtual environment with pinned versions before using PDF tooling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/irreel/skills/tax-filing)
- [Common Schedules](references/common-schedules.md)
- [Filing Status Decision Tree](references/filing-status.md)
- [IRS Form Field-to-Line Mappings](references/form-field-maps.md)
- [Form Routing](references/form-routing.md)
- [pypdf PDF Recovery Procedures](references/pypdf-recovery.md)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce filled IRS PDF update instructions and validation checklists; generated tax forms require manual verification before filing.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
