## Description:

Analyzes search engine results pages for a query by mapping SERP features, ranking patterns, search intent, AI Overviews, and snippet opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, SEO, and content teams use this skill to inspect a live or provided SERP, explain ranking patterns and intent, estimate ranking difficulty, and produce recommendations for competing on a target query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web and SERP content can be incomplete, stale, or misleading if treated as authoritative without evidence labels.

Mitigation: Label metrics as Measured, User-provided, or Estimated, cite live or provided SERP evidence for intent and difficulty claims, and mark unavailable metrics as N/A.

Risk: Reusable SEO research notes may preserve keyword priorities, competitor facts, or strategy decisions across sessions.

Mitigation: Review saved memory notes and remove sensitive or unwanted research summaries before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/serp-analysis)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Analysis Templates](artifact/references/analysis-templates.md)
- [SERP Feature Taxonomy](artifact/references/serp-feature-taxonomy.md)
- [Example Report](artifact/references/example-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown SERP brief with tables, evidence labels, recommendations, and optional shell commands for live SERP collection]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include durable research-summary guidance for memory/research/ when supported by the host environment.]

## Skill Version(s):

19.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
