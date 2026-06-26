## Description: <br>
Persistent, consensus-validated memory for AI agents via SAGE MCP server, enabling agents to recall past context, reflect on completed tasks, and maintain continuity across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l33tdawg](https://clawhub.ai/user/l33tdawg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill with a locally installed SAGE MCP server to give AI agents persistent, locally stored memory across conversations. It supports memory recall, per-turn observation storage, task reflection, and deletion of retained memories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can retain conversation summaries, task outcomes, user preferences, or other sensitive details across sessions. <br>
Mitigation: Decide before installation whether persistent memory is appropriate, avoid storing secrets or regulated data, and review or delete ~/.sage/data/sage.db when retention is no longer wanted. <br>
Risk: The skill depends on local SAGE MCP server behavior and generated MCP configuration. <br>
Mitigation: Install SAGE locally, inspect the generated .mcp.json for localhost-only tool configuration, and use the dashboard or API to view, edit, or delete retained memories. <br>


## Reference(s): <br>
- [SAGE Documentation](https://l33tdawg.github.io/sage/) <br>
- [SAGE Repository](https://github.com/l33tdawg/sage) <br>
- [SAGE Releases](https://github.com/l33tdawg/sage/releases) <br>
- [ClawHub Skill Page](https://clawhub.ai/l33tdawg/sage-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with MCP tool names and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides an agent to use local SAGE MCP tools and local SQLite-backed memory; it does not automatically capture raw conversation transcripts according to the artifact disclosure.] <br>

## Skill Version(s): <br>
5.0.2 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
