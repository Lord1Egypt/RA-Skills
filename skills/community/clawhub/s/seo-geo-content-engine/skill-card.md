## Description:

Turns keywords into SEO and GEO content packages with keyword research, SERP analysis, article drafting, FAQ schema, and AI-ready output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geo-seo](https://clawhub.ai/user/geo-seo)

### License/Terms of Use:

MIT-0

## Use Case:

External SEO teams, SaaS teams, agencies, and content operators use this skill to turn a target keyword into a repeatable search- and AI-answer-ready content package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional keyword tracker access may expose private planning data if a private sheet URL is provided.

Mitigation: Use read-only or public tracker URLs and provide private sheet URLs only when the agent is intended to read that tracker.

Risk: Optional live SERP lookup can send search terms to a configured search provider.

Mitigation: Use the SERP API only when configured intentionally, or provide approved SERP exports and pasted search-result snapshots instead.

Risk: Generated SEO articles, metadata, and FAQ schema may contain claims or structured data that need editorial review before publishing.

Mitigation: Review factual claims, citations, keyword usage, and schema validity before publication.

Risk: Broad keyword prompts could activate the content workflow unintentionally.

Mitigation: Use explicit prompts such as "write article:" or "create SEO content for" when invoking the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geo-seo/skills/seo-geo-content-engine)
- [Project homepage from metadata](https://github.com/GEO-SEO/seo-geo-content-engine)
- [Schema.org](https://schema.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown content package with SEO metadata, long-form article text, FAQ schema code, and a GEO-optimized version.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The default article target is 1500-2000 words and the workflow can use optional SERP API output or user-provided SERP snapshots.]

## Skill Version(s):

1.0.4 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
