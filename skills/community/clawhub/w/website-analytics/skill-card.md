## Description:

Google Analytics (GA4) for AI agents - traffic stats, sources, campaigns, referrals, landing pages, events, and conversion funnels across all your websites from one CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoanndefay](https://clawhub.ai/user/yoanndefay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and site owners use this skill to let agents inspect read-only GA4 traffic, source, campaign, referral, landing page, event, user, and funnel data from the fleets CLI or MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run unpinned npm packages that could change after review.

Mitigation: Review the fleets npm packages and publisher before installing, pin exact versions for fleets and fleets-mcp where possible, and run them with only the analytics credentials and environment variables they need.

## Reference(s):

- [fleets CLI](https://fleets.run)
- [ClawHub Skill Page](https://clawhub.ai/yoanndefay/skills/website-analytics)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing guidance for read-only analytics commands that can return JSON or CSV through the underlying fleets tools.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
