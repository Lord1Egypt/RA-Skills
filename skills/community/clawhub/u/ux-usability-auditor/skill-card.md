## Description:

Automates UX/usability audits for web applications by using Playwright to navigate pages, capture screenshots and UI metadata, and generate checklist-based reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[micorine](https://clawhub.ai/user/micorine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA teams, and product teams use this skill to inspect web application usability, accessibility signals, and UI consistency. It helps generate structured audit evidence and reports from authenticated application flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic page discovery can navigate beyond the intended target application.

Mitigation: Run only against systems you are authorized to test and prefer a vetted page list or same-origin URL filtering before using auto-discovery on untrusted applications.

Risk: Screenshots, inspection results, and reports can contain sensitive authenticated application content.

Mitigation: Use a test account with minimal permissions, set a controlled output directory, and handle generated artifacts as sensitive.

Risk: The skill requires login credentials in configuration to inspect authenticated flows.

Mitigation: Avoid production secrets where possible and use scoped test credentials that can be rotated after the audit.

## Reference(s):

- [Default Usability Audit Checklist](artifact/references/checklist-default.md)
- [ClawHub Skill Page](https://clawhub.ai/micorine/skills/ux-usability-auditor)
- [Publisher Profile](https://clawhub.ai/user/micorine)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown audit report, JSON inspection results, PNG screenshots, and command/configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configurable target URL, login selectors, page list, checklist path, output directory, screenshot directory, and headless mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
