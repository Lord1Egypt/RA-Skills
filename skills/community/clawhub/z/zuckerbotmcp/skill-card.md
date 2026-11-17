## Description:

ZuckerBot lets agents create, launch, monitor, and manage Facebook and Instagram ad campaigns through the Meta Ads API using the ZuckerBot MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crumbedsausage](https://clawhub.ai/user/crumbedsausage)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to plan Meta ad campaigns, generate creatives, launch or pause campaigns, run A/B tests, inspect performance metrics, research markets and competitors, and sync confirmed conversion events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect live advertising spend through campaign launches, resumes, budget changes, and A/B test launches.

Mitigation: Manually confirm every campaign launch, resume, and budget change before execution.

Risk: The skill relies on ZuckerBot API credentials and Meta OAuth permissions managed through a third-party service.

Mitigation: Install only if the publisher and ZuckerBot service are trusted, review granted Meta permissions, and keep the ability to revoke both the API key and Meta authorization.

Risk: Conversion-data uploads can influence Meta optimization and may involve sensitive business events.

Mitigation: Confirm conversion data and the target campaign before syncing conversion events.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crumbedsausage/skills/zuckerbotmcp)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown and structured tool-call results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include campaign strategies, budget recommendations, ad creative concepts, campaign IDs, status confirmations, performance metrics, market research, competitor analysis, review intelligence, and conversion-sync confirmations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
