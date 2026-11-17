## Description:

Evaluate e-commerce pages with evidence-first SEO findings that distinguish verified issues, likely signals, editorial opportunities, unavailable checks, and appendix items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ecom-agent-tools](https://clawhub.ai/user/ecom-agent-tools)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and SEO practitioners use this skill to evaluate e-commerce URLs or local HTML with evidence-labeled technical, editorial, unavailable, and appendix findings. It is intended to produce a structured review and action plan without inventing ranking, traffic, index, analytics, or merchant data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to browse target or competitor pages, inspect local HTML, or review private SEO, analytics, Search Console, merchant, feed, or commerce data.

Mitigation: Provide only targets and private data that the user is authorized to use for the SEO review, and avoid supplying unnecessary sensitive business data.

Risk: SEO conclusions can be misleading when required evidence such as field Core Web Vitals, index status, feed consistency, analytics, or merchant data is unavailable.

Mitigation: Keep unsupported checks in the UNAVAILABLE section and avoid claiming rankings, traffic, conversions, index status, field performance, feed consistency, or business impact without suitable evidence.

## Reference(s):

- [SEO Evaluator homepage](https://ecomagenttools.com)
- [ClawHub skill page](https://clawhub.ai/ecom-agent-tools/skills/seo-evaluator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with evidence labels, findings, unavailable checks, appendix items, passed checks, and a checkbox action plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are grouped as VERIFIED, LIKELY, EDITORIAL, UNAVAILABLE, or APPENDIX; the skill avoids universal scores or grades.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata; artifact frontmatter describes SEO Evaluator prompt version 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
