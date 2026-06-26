## Description: <br>
Search, read, and write RemNote notes and personal knowledge base content via `remnote-cli`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robert7](https://clawhub.ai/user/robert7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect, search, read, and manage RemNote knowledge base content from the command line. It supports note-taking, journaling, tags, tables, and structured navigation while requiring explicit user confirmation before writes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify RemNote content when mutating commands are used. <br>
Mitigation: Use read-only commands by default and require the exact phrase `confirm write` before creating, updating, replacing, tagging, or journaling notes. <br>
Risk: Troubleshooting may restart the RemNote MCP server or browser profile to reconnect the bridge. <br>
Mitigation: Check bridge status first, align server and plugin versions, and only perform recovery steps needed to restore connectivity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robert7/remnote) <br>
- [remnote-mcp-server](https://github.com/robert7/remnote-mcp-server) <br>
- [RemNote plugin marketplace install guide](https://github.com/robert7/remnote-mcp-bridge/blob/main/docs/guides/install-plugin-via-marketplace-beginner.md) <br>
- [RemNote CLI command reference](https://github.com/robert7/remnote-mcp-server/blob/main/docs/guides/remnote-cli-command-reference.md) <br>
- [Install remnote-mcp-server (npm)](https://www.npmjs.com/package/remnote-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read operations are the default; write operations require explicit confirmation.] <br>

## Skill Version(s): <br>
0.16.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
