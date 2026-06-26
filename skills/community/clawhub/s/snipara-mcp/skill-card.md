## Description: <br>
Snipara MCP connects agents to Snipara documentation search, multi-repository querying, and persistent memory tools for faster codebase answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alopez3006](https://clawhub.ai/user/alopez3006) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to query indexed project documentation, search across repositories, recall saved preferences, and retrieve focused context before answering codebase questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, session context, memories, and uploaded document contents may be sent to Snipara. <br>
Mitigation: Use scoped credentials, avoid secrets or regulated data, and install only when remote processing by Snipara is acceptable. <br>
Risk: Persistent memory can retain sensitive preferences, decisions, or project context across sessions. <br>
Mitigation: Do not store secrets in memory, and periodically review or delete saved memories. <br>
Risk: Bulk sync, deletion, summary deletion, memory deletion, and swarm state tools can modify or remove remote project data or coordination state. <br>
Mitigation: Confirm the target project and operation scope before use, keep destructive sync options disabled unless intended, and restrict credentials to the minimum required access. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/alopez3006/snipara-mcp) <br>
- [Snipara documentation](https://docs.snipara.com) <br>
- [Snipara MCP PyPI package](https://pypi.org/project/snipara-mcp/) <br>
- [Snipara dashboard](https://snipara.com/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON tool examples, inline shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return remote documentation context, saved memories, project settings, search results, and multi-agent coordination state through Snipara tools.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
