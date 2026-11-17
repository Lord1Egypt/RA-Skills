## Description:

Deterministic web/data extraction via the ToolSnap MCP server — exact parsing instead of LLM summarization, at near-zero context cost. Use before loading any external URL, PDF, CSV/JSON, feed, or sitemap into context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icosaedro-git](https://clawhub.ai/user/icosaedro-git)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use ToolSnap's MCP tools to extract targeted text or structured data from web pages, documents, feeds, and datasets before bringing it into an agent's context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote skill updates or memory snippets could introduce unreviewed instructions.

Mitigation: Review skill updates before installing and inspect memory snippets before saving them.

Risk: Authentication headers or private content sent to the remote service may expose sensitive information; paid tools can spend wallet funds.

Mitigation: Send sensitive data only when the service is trusted; use a dedicated wallet with a small balance and set a spending limit.

## Reference(s):

- [ToolSnap ClawHub release](https://clawhub.ai/icosaedro-git/skills/toolsnap)
- [ToolSnap MCP server](https://mcp.toolsnap.app/mcp)
- [Canonical ToolSnap skill instructions](https://mcp.toolsnap.app/SKILL.md)
- [ToolSnap paid tools and pay-proxy documentation](https://github.com/ToolSnap-app/toolsnap-mcp#paid-tools--connect-through-the-pay-proxy)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV, HTML]

**Output Format:** [Tool-dependent extracted text or structured data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic extraction; optional paid tools can incur per-call charges.]

## Skill Version(s):

1.1.0 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
