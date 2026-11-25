## Description:

Audit a website across technical SEO, security headers, performance, accessibility, and content quality, and produce a prioritized report where every finding is backed by measured evidence. Use this skill whenever the user asks to audit, review, check, scan, or "health check" a website or URL, asks why a site is slow, not ranking, insecure, or inaccessible, or wants a technical SEO, Core Web Vitals, security header, or WCAG review, even if they only mention one of these areas. Also use it to compare a site before and after changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kulung301](https://clawhub.ai/user/kulung301)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and technical reviewers use this skill to audit public websites for SEO, security headers, performance, accessibility, and content quality. It produces evidence-backed findings and prioritized fixes, and can compare a site before and after changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser and network access while inspecting websites could expose the audit host, including access to sensitive files or internal services.

Mitigation: Run in an isolated environment without sensitive files or access to internal services, and confirm host permissions before use.

Risk: The security analysis is partial because referenced output paths were unresolved.

Mitigation: Treat the scanner assessment as incomplete and review the skill and its permissions before installation.

## Reference(s):

- [SEO checks](artifact/references/seo.md)
- [Security checks](artifact/references/security.md)
- [Performance checks](artifact/references/performance.md)
- [Accessibility checks](artifact/references/accessibility.md)
- [Content quality checks](artifact/references/content.md)
- [ClawHub release page](https://clawhub.ai/kulung301/skills/website-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Prioritized website audit report in Markdown with evidence-backed findings and suggested next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include severity, confidence, observed evidence, impact, and a matching fix; the report states checks that were not performed.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
