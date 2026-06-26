## Description: <br>
Audit web UI for WCAG 2.1 Level AA and produce a remediation backlog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicolas-m-design](https://clawhub.ai/user/nicolas-m-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, QA teams, and accessibility reviewers use this skill to scope WCAG 2.1 Level A and AA web UI audits, find accessibility gaps, and turn findings into an engineering remediation backlog. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional scanner can be pointed at arbitrary user-provided URLs. <br>
Mitigation: Run it only against sites the user owns or is authorized to test. <br>
Risk: Generated accessibility reports and axe output can include DOM snippets from private or authenticated pages. <br>
Mitigation: Protect generated reports as sensitive project artifacts and avoid sharing them outside the authorized review group. <br>
Risk: Automated axe results are only a baseline and may miss manual WCAG conformance issues. <br>
Mitigation: Use the manual keyboard, visual, zoom/reflow, forms, semantics, ARIA, and status-message checks before making conformance decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nicolas-m-design/wcag-21-aa-web-ui-audit) <br>
- [WCAG 2.1 Level A + AA Success Criteria](docs/wcag21-aa-success-criteria.md) <br>
- [UI Component Checklists](docs/ui-component-checklists.md) <br>
- [Audit Report Template](templates/audit-report-template.md) <br>
- [Finding Template](templates/finding-template.md) <br>
- [Remediation Backlog Template](templates/remediation-backlog-template.md) <br>
- [Optional axe + Playwright runner](scripts/run_axe_playwright.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown audit reports and remediation backlogs, with optional JSON and Markdown axe baseline outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses explicit scope assumptions, WCAG success-criteria mapping, severity labels, acceptance criteria, and verification steps; optional automation writes outputs/axe-results.json and outputs/axe-summary.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
