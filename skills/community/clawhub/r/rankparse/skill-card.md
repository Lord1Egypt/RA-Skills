## Description:

Fetch SEO data such as backlinks, domain authority, technology stack, page metadata, and competitor overlap for domains and URLs through the RankParse API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhibavishi](https://clawhub.ai/user/abhibavishi)

### License/Terms of Use:

MIT-0

## Use Case:

SEO practitioners, marketers, developers, and agents use this skill to research competitors, audit backlink profiles, inspect site metadata and technology, and build link outreach lists with RankParse data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SEO lookups are sent to the external RankParse service.

Mitigation: Use the skill only for domains or URLs that are approved to query through RankParse.

Risk: The RankParse API key could be exposed if copied into shared files.

Mitigation: Store RANKPARSE_API_KEY in an environment variable or secret manager and avoid hardcoding it in repository files.

Risk: RankParse API calls may consume paid credits.

Mitigation: Confirm the intended workflow and query scope before running multi-step audits or competitor research.

## Reference(s):

- [RankParse SEO API on ClawHub](https://clawhub.ai/abhibavishi/skills/rankparse)
- [RankParse Signup](https://rankparse.com/signup)
- [RankParse MCP Server](https://mcp.rankparse.com/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, API Calls]

**Output Format:** [Markdown with JSON configuration and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RANKPARSE_API_KEY; RankParse lookups may consume paid credits and send queried domains or URLs to the service.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
