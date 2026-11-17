## Description:

Analyzes images or videos of visible plant roots in transparent pots or seedling boxes to report root health, potential problems, and care suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Gardeners and greenhouse operators can assess visible roots in images or videos, review a health score and care suggestions, and retrieve past cloud reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plant-root images or media URLs are sent to the LifeEmergence cloud service for analysis.

Mitigation: Use only media you are authorized to share; review the provider and its retention practices before uploading.

Risk: The skill silently creates or reuses an account-linked identity, stores tokens locally, and accesses cloud history and reports.

Mitigation: Review local token storage and cloud history access before use, particularly in shared workspaces.

## Reference(s):

- [API documentation](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured analysis report or Markdown table of historical reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Health score (0–100), vitality grade, care suggestions, and report links when available.]

## Skill Version(s):

1.0.13 (source: server-resolved ClawHub release; artifact frontmatter states 1.0.18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
