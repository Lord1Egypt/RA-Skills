## Description:

SERP-based semantic topic clustering for SEO content architecture that expands keywords, groups them by search-result overlap, designs hub-and-spoke content plans, and generates interactive cluster visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External SEO practitioners, content strategists, and developers use this skill to plan SERP-overlap topic clusters, design pillar-and-spoke content architecture, create internal linking matrices, and produce briefs or execution outputs for SEO programs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or rewrite content and planning files in a working content directory.

Mitigation: Run it in a controlled workspace and inspect file diffs before publishing or merging generated content.

Risk: Generated cluster maps may be unsafe when built from untrusted imported plans because the release security summary flags an HTML injection risk.

Mitigation: Use trusted inputs for cluster data, validate generated maps before opening or hosting them, and avoid publishing maps from unreviewed imported plans.

## Reference(s):

- [SERP Overlap Methodology](references/serp-overlap-methodology.md)
- [Hub-and-Spoke Content Architecture](references/hub-spoke-architecture.md)
- [Execution Workflow](references/execution-workflow.md)
- [claude-blog integration](https://github.com/AgriciDaniel/claude-blog)
- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/seo-cluster)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and HTML files with concise agent guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes cluster-plan.json, cluster-plan.md, cluster-map.html, optional cluster-briefs, and cluster-scorecard.md in the active workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
