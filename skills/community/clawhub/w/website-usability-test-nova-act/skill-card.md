## Description:

AI-orchestrated usability testing using Amazon Nova Act to generate personas, run website workflow tests, interpret raw browser-automation results, and produce HTML usability reports with safety guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adityak6798](https://clawhub.ai/user/adityak6798)

### License/Terms of Use:

MIT

## Use Case:

Developers, QA teams, and product teams use this skill to run persona-based website usability tests for flows such as checkout, booking, signup, posting, navigation, and information discovery. It helps collect browser traces and raw Nova Act responses, then guides the agent to interpret goal achievement and generate a usability report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live browser automation can perform workflow actions on real websites.

Mitigation: Run only against authorized targets, prefer non-production or test environments, use test accounts, and preserve the documented stop-before-impact behavior for payment, posting, account creation, and final submissions.

Risk: Browser traces and reports may contain screenshots, page content, personal data, or sensitive account information.

Mitigation: Avoid real personal, payment, or account data; run in a sandbox or VM when testing untrusted sites; and review or delete generated traces and reports after use.

Risk: Generated HTML reports may be unsafe to open for untrusted page content until HTML escaping and CSP issues are fixed.

Mitigation: Open reports only from trusted test runs or in an isolated browser profile, and review report content before sharing.

Risk: Page summaries may be sent to an undeclared AI provider during testing.

Mitigation: Do not test pages containing confidential data unless provider data handling is approved, and disclose third-party AI processing expectations to stakeholders.

## Reference(s):

- [Nova Act Cookbook](artifact/references/nova-act-cookbook.md)
- [Persona Examples](artifact/references/persona-examples.md)
- [AWS Console](https://console.aws.amazon.com/)

## Skill Output:

**Output Type(s):** [Analysis, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON result interpretation, browser trace files, and HTML usability reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local Nova Act logs, adaptive test results JSON, and an HTML usability report in the working directory.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
