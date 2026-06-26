## Description: <br>
Manage Things 3 tasks through Things Cloud using the maintained things-cloud-sdk CLI and MCP server, with dry-run safety for agent writes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pdurlej](https://clawhub.ai/user/pdurlej) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to inspect Things 3 tasks and safely create, edit, or complete tasks through Things Cloud using MCP tools or CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent access to Things Cloud can expose or modify personal task data. <br>
Mitigation: Install only if comfortable granting the agent access; prefer THINGS_TOKEN over THINGS_PASSWORD and keep credentials out of repositories and skill files. <br>
Risk: Write operations could unintentionally change user-visible Things tasks. <br>
Mitigation: Use the documented dry-run preview, summarize planned changes, and require explicit confirmation before running non-dry-run writes. <br>


## Reference(s): <br>
- [Things Cloud SDK homepage](https://github.com/pdurlej/things-cloud-sdk) <br>
- [ClawHub skill page](https://clawhub.ai/pdurlej/things-cloud) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses dry-run previews for writes, asks for explicit confirmation before real task changes, and keeps raw command output as JSON.] <br>

## Skill Version(s): <br>
0.1.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
