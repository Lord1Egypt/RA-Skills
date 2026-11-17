## Description:

Search Experience Optimization (SXO) analyzes Google SERPs backwards to detect page-type mismatches, derive user stories from intent signals, score pages from multiple persona perspectives, and recommend improvements or wireframe changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External SEO practitioners, content teams, and developers use this skill to compare a target page against current SERP expectations, identify search-intent and page-type gaps, and prioritize concrete SXO improvements. It can also generate persona scoring and IST/SOLL wireframe guidance when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses target URLs and search-result data needed for SEO analysis.

Mitigation: Use it only with URLs and keywords the user is authorized to analyze, and avoid submitting sensitive or private page data.

Risk: DataForSEO integration can incur API costs when those tools are available.

Mitigation: Review the cost estimate and obtain approval before approving any DataForSEO API usage.

Risk: SERP-derived recommendations may be incomplete when search results are sparse or available data is limited.

Mitigation: Review the stated limitations and validate recommendations before changing production content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/seo-sxo)
- [Page Type Taxonomy for SERP Classification](references/page-type-taxonomy.md)
- [Persona-Based Scoring Methodology](references/persona-scoring.md)
- [User Story Framework: SERP Signals to User Intent](references/user-story-framework.md)
- [Wireframe Templates: IST/SOLL Patterns](references/wireframe-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown analysis, scored tables, prioritized recommendations, and optional semantic HTML wireframe outlines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include source-signal notes, explicit limitations, and cost review before optional DataForSEO API usage.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
