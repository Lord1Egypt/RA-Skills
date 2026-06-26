## Description: <br>
Build, debug, and explain integrations with Raindrop.io, including OAuth 2 authorization, bearer-token REST API calls, collections and raindrops CRUD flows, tags and highlights, import or export and backups, and MCP server setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangcheng](https://clawhub.ai/user/huangcheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build, debug, or explain Raindrop.io REST API and MCP integrations for bookmark collections, raindrops, tags, highlights, imports, exports, backups, and client setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An authorized agent can read or change Raindrop.io bookmark data during live use. <br>
Mitigation: Provide only least-privilege credentials through a secure mechanism when possible, and revoke tokens or MCP access when the task is finished. <br>
Risk: Bulk delete, move, merge, export, backup, or sharing operations can affect many bookmarks or expose bookmark data. <br>
Mitigation: Review those operations before execution and confirm the target collection, scope, and sharing settings. <br>
Risk: High-volume requests can trigger Raindrop.io rate limits. <br>
Mitigation: Use documented rate-limit headers and backoff behavior, especially after HTTP 429 responses. <br>


## Reference(s): <br>
- [Raindrop.io Reference](references/raindrop-reference.md) <br>
- [Raindrop.io Developer Docs](https://developer.raindrop.io/) <br>
- [Raindrop.io REST API](https://api.raindrop.io/rest/v1) <br>
- [Raindrop.io MCP Endpoint](https://api.raindrop.io/rest/v2/ai/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code, API examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OAuth, REST, MCP setup, and rate-limit handling guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
