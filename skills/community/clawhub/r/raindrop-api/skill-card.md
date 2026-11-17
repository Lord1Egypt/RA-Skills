## Description:

Build, debug, and explain integrations with Raindrop.io, including OAuth 2 authorization, bearer-token REST API calls, collections and raindrops CRUD flows, tags and highlights, import or export and backups, and MCP server setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangcheng](https://clawhub.ai/user/huangcheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to design, debug, and explain Raindrop.io REST API and MCP integrations for bookmark management, OAuth authentication, imports, exports, backups, tags, highlights, and collections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access tokens and client secrets can expose private Raindrop.io bookmark data if shared or stored insecurely.

Mitigation: Treat credentials as sensitive, request them only when live API calls are needed, and avoid placing tokens or client secrets in generated code, logs, or shared files.

Risk: Bulk update, delete, export, and backup workflows can modify or expose large amounts of private bookmark data.

Mitigation: Review proposed bulk operations before execution and store downloaded exports or backups carefully.

Risk: Raindrop.io API usage can be disrupted by rate limits or by workflows that conflict with published service terms.

Mitigation: Respect usage terms, avoid abusive polling or rate-limit evasion, and handle 429 responses with backoff using live rate-limit headers.

## Reference(s):

- [Raindrop.io Reference](references/raindrop-reference.md)
- [Raindrop.io Developer Docs](https://developer.raindrop.io/)
- [Raindrop.io REST API v1](https://api.raindrop.io/rest/v1)
- [Raindrop.io MCP Endpoint](https://api.raindrop.io/rest/v2/ai/mcp)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code, API examples, configuration guidance, and shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include REST request examples, OAuth setup steps, MCP client setup guidance, and cautions for tokens, bulk edits, exports, and backups.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
