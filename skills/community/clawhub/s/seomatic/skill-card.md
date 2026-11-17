## Description:

SEOmatic helps users analyze their website's search performance, audit SEO and AI visibility, research opportunities, and stage site improvements for approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minh42](https://clawhub.ai/user/minh42)

### License/Terms of Use:

MIT-0

## Use Case:

Website owners, marketers, and SEO teams use the skill to review Search Console performance, audit pages and AI visibility, research keywords and competitors, and prepare site changes for their approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running a mutable external CLI could execute unreviewed package changes.

Mitigation: Prefer a pinned or preinstalled SEOmatic binary and review the package before installation.

Risk: An API key with staging authority can access sensitive SEO data and prepare site changes.

Mitigation: Use the least-privileged key available, protect it from logs and output, and review each staged change in SEOmatic before approving it.

## Reference(s):

- [SEOmatic CLI documentation](https://seomatic.ai/developers/cli)
- [SEOmatic MCP documentation](https://seomatic.ai/developers/mcp)
- [SEOmatic skill release](https://clawhub.ai/minh42/skills/seomatic)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with SEO findings, recommendations, and review links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Metrics should include their source date ranges; staged changes require user approval before publication.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
