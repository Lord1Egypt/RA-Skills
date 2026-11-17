## Description:

Searches X (Twitter) posts through the official Gecho Bridge MCP tools and retrieves known post details and replies for keyword monitoring, post research, author information, engagement signals, and reply analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research teams use this skill to route X keyword searches and known post URL lookups through Gecho Bridge, then summarize posts, authors, engagement signals, and representative replies. It can also guide setup and optionally save raw results as local JSON when a reliable directory is provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses a logged-in Chrome and X session and may read public or account-accessible X posts and replies.

Mitigation: Use a browser profile intended for research workflows and avoid sessions with access that should not be available to research tools.

Risk: Collected post and reply data may be saved locally as JSON.

Mitigation: Choose a deliberate save directory, review saved files before sharing, and remove data that should not be retained.

Risk: The skill depends on external Gecho MCP package and Chrome extension components.

Mitigation: Review the Gecho Bridge package and Chrome extension before installation or update, and keep MCP configuration explicit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/x-zh-cn)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho website](https://gecho.ai/)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON files]

**Output Format:** [Markdown guidance with inline shell commands, structured post summaries, and optional saved JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npx, Gecho Bridge MCP tools, the Gecho Chrome extension, and logged-in Gecho and X browser sessions.]

## Skill Version(s):

1.1.38 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
