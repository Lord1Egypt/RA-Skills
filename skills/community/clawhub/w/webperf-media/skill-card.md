## Description:

Webperf Media helps agents audit images, videos, and SVGs in Chrome DevTools and produce media performance recommendations for LCP, CLS, lazy loading, formats, priority hints, and asset sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nucliweb](https://clawhub.ai/user/nucliweb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and performance engineers use this skill to inspect page media through Chrome DevTools and identify optimizations for image loading, video setup, SVG bitmap usage, and Core Web Vitals impact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects media URLs, DOM attributes, and performance resource metadata on the active browser page.

Mitigation: Run it only on pages selected for audit and avoid sensitive logged-in pages unless that page data can be reviewed by the agent.

Risk: Cross-skill follow-up audits can expand the scope of browser diagnostics beyond the initial media check.

Mitigation: Review proposed follow-up audits before allowing additional browser-page analysis.

## Reference(s):

- [Snippet Descriptions](references/snippets.md)
- [Script Return Value Schema](references/schema.md)
- [Webperf Snippets Repository](https://github.com/nucliweb/webperf-snippets)
- [Webperf Media ClawHub Page](https://clawhub.ai/nucliweb/skills/webperf-media)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown guidance with Chrome DevTools JavaScript snippets and structured audit findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces recommendations from page media diagnostics; does not persist or modify page state.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
