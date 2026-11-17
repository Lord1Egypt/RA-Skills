## Description:

Audits web UI for WCAG 2.1 Level AA and produces accessibility findings, conformance guidance, and a remediation backlog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicolas-m-design](https://clawhub.ai/user/nicolas-m-design)

### License/Terms of Use:


## Use Case:

Developers, designers, QA teams, and accessibility reviewers use this skill to audit web UI flows against WCAG 2.1 Level A and AA, distinguish confirmed implementation issues from design-time risks, and prepare remediation work with acceptance criteria and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional automation script can run a local browser against user-provided URLs.

Mitigation: Use trusted target URLs, avoid attacker-supplied URL lists, and avoid scanning from privileged internal networks unless that access is intended.

Risk: Optional npm dependencies are required for axe and Playwright scanning.

Mitigation: Review and pin playwright and @axe-core/playwright dependencies before installing them in the audit environment.

Risk: Automated axe output is only a baseline and can miss manual WCAG issues.

Mitigation: Treat automated results as supporting evidence and complete the skill's keyboard, visual, reflow, forms, semantics, and status-message review steps before reporting findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicolas-m-design/skills/wcag-21-aa-web-ui-audit)
- [UI Component Checklists](docs/ui-component-checklists.md)
- [WCAG 2.1 Level A + AA Success Criteria](docs/wcag21-aa-success-criteria.md)
- [Audit Report Template](templates/audit-report-template.md)
- [Finding Template](templates/finding-template.md)
- [Remediation Backlog Template](templates/remediation-backlog-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown audit reports and remediation backlog content, with optional JSON and Markdown axe baseline files when the local Playwright script is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional automation path writes outputs/axe-results.json and outputs/axe-summary.md; manual WCAG review remains required for conformance guidance.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
