## Description: <br>
Access GitHub repository documentation and code through the gitmcp.io MCP service, including documentation retrieval, documentation search, code search, referenced URL fetching, and direct MCP tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[am-will](https://clawhub.ai/user/am-will) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to read GitHub repository documentation and code through GitMCP when answering repository questions or locating implementation details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make remote requests through gitmcp.io, including broad URL fetches and direct MCP tool calls. <br>
Mitigation: Prefer scoped fetch-docs, search-docs, and search-code commands; allow arbitrary URL fetching or direct MCP calls only after reviewing the target and trusting the remote service. <br>
Risk: Repository documentation or code retrieved from remote sources may be incomplete, stale, or misleading. <br>
Mitigation: Review retrieved content before using it for decisions or code changes, and cross-check important claims against trusted project sources when available. <br>


## Reference(s): <br>
- [Read GitHub ClawHub skill page](https://clawhub.ai/am-will/read-github) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands or JSON tool-call output when the CLI is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make remote requests through gitmcp.io and can expose broad URL fetching or direct MCP tool calls depending on command usage.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
