## Description: <br>
context-mode is an MCP server that saves 98% of your context window by sandboxing tool outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1yihui](https://clawhub.ai/user/1yihui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route large file reads, shell outputs, web fetches, and indexed retrieval through a context-management MCP server so agent sessions can conserve context window space and recover information after compaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes broad local shell, file-reading, indexing, and web-fetching activity through an MCP server. <br>
Mitigation: Use it only in trusted workspaces, pin and verify the npm package, and configure deny rules for secrets and destructive commands before enabling the server. <br>
Risk: Persistent SQLite/FTS indexing may retain sensitive local content if private logs, credentials, or restricted documents are indexed. <br>
Mitigation: Exclude sensitive paths from indexing, avoid indexing credential-bearing files, and confirm the process for purging stored index data. <br>


## Reference(s): <br>
- [YiHui CONTEXT MODE on ClawHub](https://clawhub.ai/1yihui/yihui-context-mode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and terse agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to use MCP tools for local command execution, file indexing, web fetching, BM25 search, and SQLite/FTS-backed session continuity.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
