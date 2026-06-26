## Description: <br>
Install, wire, and verify the 699pic enterprise MCP server from the st699pic/st-ent-mcp repository for OpenClaw, Claude, Codex, or other local MCP clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[st699pic](https://clawhub.ai/user/st699pic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit, install, configure, and smoke-test a local stdio MCP server for the 699pic enterprise OpenAPI service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install workflow clones and runs external MCP server code. <br>
Mitigation: Verify the repository identity, inspect README.md, package.json, and mcp/server.js, and use an isolated container or VM when audit confidence is incomplete. <br>
Risk: The MCP registration may keep SERVICE_API_KEY available to future local agent sessions. <br>
Mitigation: Use a dedicated least-privilege API key, prefer project-scoped registration, and remove or rotate the key when the integration is no longer needed. <br>
Risk: Incorrect service endpoint or credential configuration can send requests to the wrong 699pic enterprise API environment. <br>
Mitigation: Confirm SERVICE_API_BASE_URL and SERVICE_API_KEY before smoke testing, then verify registration with tools/list or one real MCP call. <br>


## Reference(s): <br>
- [st-ent-mcp repository notes](artifact/references/repo.md) <br>
- [st-ent-mcp GitHub repository](https://github.com/st699pic/st-ent-mcp) <br>
- [ClawHub skill page](https://clawhub.ai/st699pic/st-ent-skills-install) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes audit steps, environment variable requirements, MCP registration guidance, and smoke-test commands.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
