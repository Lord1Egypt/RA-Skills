## Description:

Visualizes local AI agent memory files as a five-layer recursive memory network with an interactive D3.js force-directed graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidadong2359](https://clawhub.ai/user/weidadong2359)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to inspect local agent memory files such as MEMORY.md, memory/*.md, .issues/*.md, and SOUL.md as an interactive memory graph with layers, weights, connections, filters, and summary statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default launch can expose private agent memory through a public unauthenticated Cloudflare Tunnel link.

Mitigation: Use local-only mode for sensitive workspaces and share a public tunnel only when anyone with the link may view the graph.

Risk: The visualizer scans local memory files, including SOUL.md when present, which may contain sensitive user or agent context.

Mitigation: Set RMN_WORKSPACE to a deliberately scoped directory containing only files intended for visualization.

Risk: The local data endpoint allows wildcard cross-origin access.

Mitigation: Run on a trusted local machine and avoid exposing the service beyond localhost unless access controls are added.

## Reference(s):

- [RMN Visualizer ClawHub listing](https://clawhub.ai/weidadong2359/skills/rmn-visualizer)
- [Cloudflare Tunnel downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)
- [D3.js](https://d3js.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with a URL and optional shell commands; interactive graph data is served as JSON to a browser visualization.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+; Cloudflare Tunnel is optional for public sharing; RMN_WORKSPACE and RMN_PORT configure workspace scope and port.]

## Skill Version(s):

1.1.2 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
