## Description:

Read and act on a RanklyBee SEO workspace - Google Search Console and Bing data, content, backlinks, link prospects and outreach, community leads, and AI visibility - through the RanklyBee MCP server or Public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dazhiyu0235](https://clawhub.ai/user/dazhiyu0235)

### License/Terms of Use:

MIT-0

## Use Case:

Website owners and SEO practitioners use the skill to review their own connected site's Google Search Console and Bing performance, content, backlinks, prospects, community leads, and AI visibility. They can also prepare content and outreach, with approval required before sending or publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The provider currently documents a preselected submission permission even though the skill describes read access as the default.

Mitigation: Review every consent checkbox and grant only needed permissions; keep approval prompts enabled for sending, posting, publishing, and other writes.

Risk: An API token or overly broad project access could expose account data.

Mitigation: Grant access only to the projects and permissions needed, and store tokens in the client's secret store or an environment variable rather than chat.

## Reference(s):

- [RanklyBee MCP setup guide](https://ranklybee.com/docs/mcp)
- [RanklyBee Public API reference](https://api.ranklybee.com/api/public/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Analysis]

**Output Format:** [Text or Markdown, including SEO analysis, summaries, and content or outreach drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are limited to the signed-in user's connected sites; sending, publishing, and other write actions require user approval.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
