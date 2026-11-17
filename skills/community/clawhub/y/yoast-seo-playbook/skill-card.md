## Description:

Yoast SEO operating playbook for WordPress delivery. Covers Yoast Free vs Yoast Premium capability boundaries, editor workflows, safe optimization QA, and when to use WordPress REST vs wp-admin for SEO tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebastiangansca](https://clawhub.ai/user/sebastiangansca)

### License/Terms of Use:

MIT-0

## Use Case:

External WordPress editors, SEO operators, and developers use this skill to plan, review, and execute Yoast-aware on-page SEO work. It helps produce editor-ready titles, meta descriptions, heading notes, internal-link recommendations, QA checks, and tier-safe Free versus Premium guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defaults to Italian-first SEO copy for a Rilvo audience unless the user asks otherwise.

Mitigation: Confirm target language, audience, and brand voice before applying generated SEO copy to a live WordPress site.

Risk: Yoast Premium-only recommendations may be unavailable when Premium status is unknown or inactive.

Mitigation: Confirm Yoast SEO and Yoast SEO Premium state before proposing feature-dependent actions, and default to Free-safe guidance when uncertain.

Risk: Guidance for live WordPress edits could be applied through a separate content tool without review.

Mitigation: Review title, meta description, headings, canonical and robots behavior, and publish recommendation before making live content changes.

## Reference(s):

- [Core Yoast Workflows](references/core-workflows.md)
- [Yoast SEO Free vs Premium Matrix](references/free-vs-premium-matrix.md)
- [Yoast SEO QA Checklist](references/qa-checklist.md)
- [Skill Sources](references/sources.md)
- [Yoast Developer API Overview](https://developer.yoast.com/customization/apis/overview/)
- [Yoast REST API](https://developer.yoast.com/customization/apis/rest-api/)
- [Yoast Metadata API](https://developer.yoast.com/customization/apis/metadata-api/)
- [Yoast Analysis Features](https://developer.yoast.com/features/analysis/overview/)
- [Yoast SEO Titles Functional Specification](https://developer.yoast.com/features/seo-tags/titles/functional-specification/)
- [Yoast Meta Descriptions Functional Specification](https://developer.yoast.com/features/seo-tags/descriptions/functional-specification/)
- [Yoast Meta Robots Functional Specification](https://developer.yoast.com/features/seo-tags/meta-robots/functional-specification/)
- [Yoast XML Sitemaps Functional Specification](https://developer.yoast.com/features/xml-sitemaps/functional-specification/)
- [Yoast Schema for Yoast SEO](https://developer.yoast.com/features/schema/plugins/yoast-seo/)
- [Yoast Schema for Yoast SEO Premium](https://developer.yoast.com/features/schema/plugins/yoast-seo-premium/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with editor-ready SEO field text, checklist items, workflow notes, and tier assumptions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, credential handling, persistence, or live WordPress changes are performed by the skill itself.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
