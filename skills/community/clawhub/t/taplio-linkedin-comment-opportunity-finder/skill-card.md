## Description:

Find the LinkedIn posts the user should comment on today to earn visibility, followers, and inbound. Pulls live candidates from the Taplio engagement feeds (the personalized selection, a curated creator feed for their niche, or a keyword search), scores each post on recency, audience overlap, engagement velocity, and topic match, and returns a prioritized list with the right comment angle for each, ready to hand to the Smart Comment Writer. Use when the user wants to grow through engagement instead of, or on top of, posting. Requires the Taplio MCP to read the feeds, the post urns, and the user's niche settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porenes](https://clawhub.ai/user/porenes)

### License/Terms of Use:

MIT-0

## Use Case:

LinkedIn users who want to build visibility through thoughtful engagement use this skill to find and prioritize timely posts in their niche, with a suggested comment angle for each.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can queue LinkedIn likes as well as identify and rank comment opportunities.

Mitigation: Keep likes optional and queue one only after the user explicitly requests it for that post; make clear that queueing does not mean the like has been sent.

Risk: The security scan was partial because two local path-like references were unresolved; the benign verdict is not a guarantee of safety.

Mitigation: Review the unresolved references and inspect the skill before connecting Taplio or using the workflow.

## Reference(s):

- [ClawHub release](https://clawhub.ai/porenes/skills/taplio-linkedin-comment-opportunity-finder)
- [Taplio MCP](https://mcp.taplio.com)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Prioritized Markdown list of LinkedIn posts with scores, links, and comment angles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to the requested number of opportunities, based on live Taplio data; may return fewer when candidates are weak.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
