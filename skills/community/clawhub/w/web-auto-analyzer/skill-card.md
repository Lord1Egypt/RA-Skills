## Description:

Automatically analyze websites for performance metrics and audit issues using Lighthouse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj-hao](https://clawhub.ai/user/lj-hao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run local Lighthouse audits for website performance, accessibility, SEO, and best-practice issues, then receive prioritized findings and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auditing arbitrary, authenticated, localhost, private-network, or cloud-metadata URLs can expose sensitive URL paths or reach internal services from the local browser environment.

Mitigation: Use isolated browser environments for sensitive targets and avoid authenticated, localhost, private-network, or cloud-metadata URLs unless explicitly approved.

Risk: Generated JSON and HTML Lighthouse reports can contain URL structure and audit details that may be sensitive when shared.

Mitigation: Review reports before sharing, redact sensitive paths or findings, and ask before saving analysis details for historical tracking.

Risk: Setup and troubleshooting guidance includes commands that can install packages, modify package metadata, or affect local processes.

Mitigation: Review installation, package.json overwrite, sudo, apt-key, and process-kill commands before running them in important environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lj-hao/skills/web-auto-analyzer)
- [Project homepage](https://github.com/user/chrome-devtools-auto-analyzer)
- [Quick Start](artifact/quick-start.md)
- [Setup Guide](artifact/setup.md)
- [Performance Metrics Reference](artifact/metrics-reference.md)
- [Audit Checklist](artifact/audit-checklist.md)
- [Troubleshooting](artifact/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables, inline shell commands, code examples, and references to JSON and HTML Lighthouse reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save local JSON and HTML audit reports under a results or user-selected output directory after running Lighthouse.]

## Skill Version(s):

1.1.1 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
