## Description:

Fact-check and attribution-check social media content (tweets, LinkedIn posts, blog excerpts). Verifies claims, checks attribution, and flags inaccuracies before publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Content, marketing, and social teams use this skill before publication to check claims and attribution in tweets, LinkedIn posts, and short blog excerpts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated accuracy reports could still contain mistakes or uncertain findings that affect publication decisions.

Mitigation: Review the generated report before publication and resolve inaccurate, unverifiable, or high-priority attribution items manually.

Risk: The workflow is scoped to social content and short blog excerpts, not deep technical fact-checking.

Mitigation: Use a deeper fact-checking workflow for long-form or highly technical content.

Risk: The skill text includes internal role and approval-flow names that may not match every deployment.

Mitigation: Adapt routing labels and approval handoffs to the deploying team's process before relying on them operationally.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local accuracy report with claim checks, attribution flags, verdicts, and recommended edits.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
