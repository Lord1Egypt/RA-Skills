## Description:

Deep single-page SEO analysis covering on-page elements, content quality, technical meta tags, schema, images, and performance signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External site owners, marketers, and developers use this skill to audit a single URL for on-page SEO, content quality, technical metadata, schema markup, images, and performance-related signals. It returns prioritized issues, actionable recommendations, and schema suggestions for improving the page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording can cause a plain single-URL request to trigger an SEO audit.

Mitigation: Use the skill when SEO analysis is intended and confirm that the URL should be audited before relying on results.

Risk: Private or authenticated pages may expose rendered page content for review.

Mitigation: Avoid sending private or authenticated pages unless sharing rendered HTML with the agent is acceptable.

Risk: Core Web Vitals findings are reference signals from available HTML, not direct lab or field measurements.

Mitigation: Validate performance-sensitive recommendations with browser-rendered snapshots or dedicated performance tooling before implementation.

## Reference(s):

- [ClawHub seo-page skill page](https://clawhub.ai/asale-ai/skills/seo-page)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown report with a scorecard, prioritized issues, recommendations, and optional JSON-LD snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use optional DataForSEO tools when available; otherwise analyzes available page HTML and reports unreachable, authentication, or JavaScript-rendering limitations.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter metadata.version is 2.2.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
