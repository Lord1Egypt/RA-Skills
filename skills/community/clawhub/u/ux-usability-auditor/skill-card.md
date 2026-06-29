## Description: <br>
Automated UX/usability audit for web applications that navigates target app pages with Playwright, captures screenshots and UI metadata, evaluates them against a configurable checklist, and supports Chinese and English usability standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[micorine](https://clawhub.ai/user/micorine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, QA teams, and product teams use this skill to inspect web application usability, accessibility, and UI consistency. It is suited for generating structured UX audit reports with screenshots, UI statistics, checklist findings, and prioritized issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The inspector logs into the configured target web application and can access pages available to that account. <br>
Mitigation: Use a dedicated low-privilege test account and limit the configured target to applications approved for audit. <br>
Risk: Generated screenshots, JSON inspection output, and Markdown reports may contain private application data. <br>
Mitigation: Store outputs in a controlled local directory, review them before sharing, and avoid committing reports or screenshots that contain sensitive data. <br>
Risk: Configuration files can contain target URLs and login credentials. <br>
Mitigation: Keep credentials out of shared config files when possible and remove or rotate any test credentials after the audit. <br>


## Reference(s): <br>
- [Default usability audit checklist](artifact/references/checklist-default.md) <br>
- [ClawHub skill page](https://clawhub.ai/micorine/ux-usability-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report, JSON inspection results, PNG screenshots, and configuration-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local inspection_results.json, usability_audit_report.md, screenshots, and report assets in the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
