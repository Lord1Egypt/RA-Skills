## Description:

Analyze Zhihu hot trends & community dynamics; generate high-engagement answer strategies and first drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and content strategists use this skill to evaluate Zhihu domains, identify topic opportunities, generate answer strategy briefs and markdown drafts, and plan publishing timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mock analytics or fallback engagement metrics may be mistaken for current Zhihu data.

Mitigation: Treat recommendations as strategy templates unless verified Zhihu data is supplied, and confirm trend metrics before relying on them.

Risk: Generated drafts can contain unsupported personal experience, research claims, or statistics.

Mitigation: Replace unsupported claims with verified facts, real experience, and cited evidence before publishing.

Risk: Medical, legal, financial, or otherwise regulated topics may produce misleading or noncompliant publishing advice.

Mitigation: Apply qualified domain review, add appropriate disclaimers, and avoid publishing regulated advice without verification.

Risk: Creator style samples may lead to overly close imitation.

Mitigation: Use samples only for high-level structure and tone guidance, then review drafts for originality before publication.

## Reference(s):

- [Engagement Patterns Reference](references/engagement_patterns.json)
- [Topic Templates Reference](references/topic_templates.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [CLI text tables, markdown drafts, and JSON objects matching artifact/schemas/output.schema.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs use mock or fallback analytics unless replaced with verified Zhihu data; draft claims require human fact-checking before publication.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
