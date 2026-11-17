## Description:

Web Regression Testing turns natural-language test requests into browser-driven regression checks with planned steps, assertions, screenshots, and Markdown reports in Chinese or English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kastol](https://clawhub.ai/user/kastol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and web delivery reviewers use this skill to plan and execute authorized web UI, regression, smoke, and acceptance tests from natural-language descriptions and produce reviewable reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can act on live login, checkout, and admin workflows.

Mitigation: Use only authorized sites, prefer staging or sandbox accounts, and avoid real checkout or admin mutations unless explicitly intended.

Risk: Screenshots and generated reports may contain credentials, personal data, order details, or internal system information.

Mitigation: Redact screenshots and reports before sharing or storing them outside the test context.

Risk: The documented browser setup includes unsafe command guidance for some environments.

Mitigation: Pin and verify agent-browser before installation and do not run --no-sandbox on sensitive or untrusted sites.

## Reference(s):

- [Assertion Catalog](references/assertion-catalog.md)
- [Report Template](references/report-template.md)
- [Run Guide](references/run-guide.md)
- [Admin Console Flow](references/admin-console-flow.md)
- [Windows Edge Fallback](references/windows-edge-fallback.md)
- [Example Run](references/example-run.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with test steps, assertion results, defect summaries, screenshot references, and inline shell commands when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses and reports follow the user's input language; browser observations and screenshots may be included when automation is available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
