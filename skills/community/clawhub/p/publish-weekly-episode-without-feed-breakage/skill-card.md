## Description:

Keeps this week's podcast episode from breaking distribution by guiding an agent through live checks of a deployed public podcast RSS feed, recent enclosures, artwork, and bounded media samples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powmcp](https://clawhub.ai/user/powmcp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, podcast operators, and developers use this skill after publishing an episode to check the deployed public RSS feed and related assets before directories ingest the update. It helps produce a bounded handoff that separates measured feed evidence from unassessed items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation commands can fetch current third-party code.

Mitigation: Use pinned or reviewed installation sources in sensitive environments.

Risk: Live checks send podcast feed or media URLs to the PowMCP service.

Mitigation: Use public podcast URLs and avoid private feeds or secret-bearing URLs unless the service is approved for that data.

Risk: A clean run covers only the selected recent-episode window, fetched assets, and bounded media sample.

Mitigation: Report skipped or unavailable checks as unassessed, and rerun the same check after feed or asset fixes.

## Reference(s):

- [Podcast Feed Check Reference](references/podcast-feed-check.md)
- [Podcast Feed Check App](https://powmcp.com/apps/podcast-feed-check/)
- [Podcast Feed Check MCP Endpoint](https://powmcp.com/podcast-feed-check/mcp)
- [Apple Feed Validation](https://podcasters.apple.com/support/829-validate-your-podcast)
- [Podcast Validation Error Reference](https://correctfeed.com/help/podcast-feed-validation-errors/)
- [ClawHub Skill Page](https://clawhub.ai/powmcp/skills/publish-weekly-episode-without-feed-breakage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown checklist, reports, setup commands, and bounded operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include verbatim measured evidence returned by the Podcast Feed Check MCP service; does not independently certify directory acceptance or uninspected episodes.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
