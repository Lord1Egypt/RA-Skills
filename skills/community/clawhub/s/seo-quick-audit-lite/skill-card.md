## Description:

Offline on-page SEO audit of a local HTML file — title and meta description quality, canonical, robots meta, viewport, Open Graph tags, h1 structure, image alt coverage, lang/charset. Zero network access. Use when the user asks to check a page's SEO basics from saved HTML or a template file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site owners use this skill to check the core on-page SEO elements in a saved HTML page or template. It reports pass, warning, and failure results with concise suggestions for common issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reported installation behavior may conflict with the offline audit purpose and may use unpinned remote content.

Mitigation: Before installing, review the installation behavior and verify remote content before running it.

Risk: The security scan was incomplete, so its benign verdict does not establish that all behavior is safe.

Mitigation: Review the partially inspected files before installation and execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nenadzivotic/skills/seo-quick-audit-lite)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON audit report with pass/warn/fail checks and concise remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audits only the supplied local HTML file; read-only and offline. Results reflect common conventions, not search-engine guarantees.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
