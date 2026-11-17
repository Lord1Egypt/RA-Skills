## Description:

Checks Google Search Console URL Inspection data to find indexing issues, explain them, review sitemaps, and stage fixes for approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minh42](https://clawhub.ai/user/minh42)

### License/Terms of Use:

MIT-0

## Use Case:

Site owners and SEO practitioners use the skill to understand why important pages are or are not indexed by Google. It summarizes Search Console inspection and sitemap data in plain language and can stage proposed fixes for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One local reference could not be resolved, so the security review is incomplete.

Mitigation: Review the unresolved reference and decide whether it matters before installing; a benign scan is not a guarantee of safety.

Risk: Staged indexing fixes can change site content or configuration, and incorrect changes could affect search visibility.

Mitigation: Review each target and rationale before approval; require explicit user sign-off for destructive noindex or redirect changes.

## Reference(s):

- [SEOmatic](https://app.seomatic.ai)
- [ClawHub release](https://clawhub.ai/minh42/skills/seomatic-indexing-check)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Plain-language indexing report with proposed fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include page statuses, sitemap findings, and staged tasks awaiting user approval.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
