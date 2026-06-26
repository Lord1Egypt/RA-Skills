## Description: <br>
Persistent memory for OpenClaw agents via the Qoris MCP server, with explicit save and recall tools for cross-session context and no automatic data capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qoris-ai](https://clawhub.ai/user/qoris-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, teams, and external users use this skill to give OpenClaw agents explicit, cross-session memory backed by Qoris workspace storage, semantic search, and versioned records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected memory content is sent to the hosted Qoris service for the configured workspace. <br>
Mitigation: Install only when the provider, retention policy, access controls, and workspace sharing model are approved for the data being stored. <br>
Risk: The skill requires QORIS_API_KEY, which grants access to the configured memory workspace. <br>
Mitigation: Protect the API key as a sensitive credential, use restricted workspaces where appropriate, and rotate the key if exposure is suspected. <br>
Risk: Shared persistent memory can expose stored information to other holders of the workspace credentials. <br>
Mitigation: Do not store secrets, regulated data, or sensitive customer or personal information unless organizational controls explicitly allow it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qoris-ai/qoris-memory-mcp) <br>
- [Qoris homepage](https://qoris.ai) <br>
- [Qoris Memory documentation](https://docs.qoris.ai/memory) <br>
- [Qoris dashboard](https://qoris.ai/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell and JSON configuration examples; memory tool responses are text or structured MCP results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QORIS_API_KEY and QORIS_WORKSPACE_ID. Memory content is sent only through explicit memory tool calls to the configured Qoris workspace.] <br>

## Skill Version(s): <br>
1.0.5 (source: server evidence release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
