## Description: <br>
Yoast SEO operating playbook for WordPress delivery. Covers Yoast Free vs Yoast Premium capability boundaries, editor workflows, safe optimization QA, and when to use WordPress REST vs wp-admin for SEO tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebastiangansca](https://clawhub.ai/user/sebastiangansca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External WordPress site owners, editors, marketers, and developers use this skill to plan, review, and execute Yoast-aware on-page SEO work. It helps produce tier-accurate title, meta description, heading, schema, readability, and internal-linking guidance for WordPress content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports a suspicious security verdict for behavior involving broad sandbox access and possible diff sharing through fallback reviewer CLIs. <br>
Mitigation: Install only after trusting the publisher; run review helpers without full-access automation where possible and disable fallback reviewers when code diffs should stay local. <br>
Risk: SEO recommendations can become inaccurate if the site's Yoast Free or Premium tier is assumed incorrectly. <br>
Mitigation: Confirm Yoast activation and Premium licensing before using feature-dependent recommendations; default to Free-safe guidance when tier status is unknown. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sebastiangansca/yoast-seo-playbook) <br>
- [Free vs Premium Matrix](references/free-vs-premium-matrix.md) <br>
- [Core Yoast Workflows](references/core-workflows.md) <br>
- [Yoast SEO QA Checklist](references/qa-checklist.md) <br>
- [Validated Sources](references/sources.md) <br>
- [Yoast Developer API Overview](https://developer.yoast.com/customization/apis/overview/) <br>
- [Yoast REST API](https://developer.yoast.com/customization/apis/rest-api/) <br>
- [Yoast Metadata API](https://developer.yoast.com/customization/apis/metadata-api/) <br>
- [Yoast Analysis Overview](https://developer.yoast.com/features/analysis/overview/) <br>
- [Yoast SEO Titles Specification](https://developer.yoast.com/features/seo-tags/titles/functional-specification/) <br>
- [Yoast SEO Descriptions Specification](https://developer.yoast.com/features/seo-tags/descriptions/functional-specification/) <br>
- [Yoast XML Sitemaps Specification](https://developer.yoast.com/features/xml-sitemaps/functional-specification/) <br>
- [Yoast Schema for Yoast SEO](https://developer.yoast.com/features/schema/plugins/yoast-seo/) <br>
- [Yoast Schema for Yoast SEO Premium](https://developer.yoast.com/features/schema/plugins/yoast-seo-premium/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with concise editor-ready recommendations and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
