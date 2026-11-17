## Description:

Shadow AI Monitor generates HTML dashboards for tracking employee AI tool usage, data exposure risks, and PIPEDA compliance, with demo data generation, interactive drill-downs, and PDF export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techcodecrafter](https://clawhub.ai/user/techcodecrafter)

### License/Terms of Use:

MIT

## Use Case:

Security, compliance, legal, and executive teams use this skill to generate dashboards that summarize employee AI tool usage, sensitive data exposure patterns, and PIPEDA compliance gaps. Consultants and sales teams can also use its demo data generator to present AI governance scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated JSON and HTML reports may contain sensitive employee monitoring records.

Mitigation: Restrict access to generated outputs, use approved telemetry sources, and obtain appropriate workplace notice or legal review before use with real organizational data.

Risk: Dashboard output protections are weak for untrusted or unsanitized input data.

Mitigation: Review and sanitize source data before generating or opening reports, especially when using real monitoring records.

Risk: The generated dashboard loads Chart.js from an external CDN.

Mitigation: Bundle Chart.js locally or approve the CDN dependency before deploying reports in restricted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/techcodecrafter/skills/shadow-ai-monitor)
- [Chart.js CDN dependency](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [Files, JSON, HTML, Shell commands, Guidance]

**Output Format:** [Generated JSON data and standalone HTML dashboard, plus Markdown usage guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated dashboard can be opened in a browser and exported to PDF through browser print; Chart.js is loaded from jsDelivr unless bundled locally.]

## Skill Version(s):

1.0.0 (source: package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
