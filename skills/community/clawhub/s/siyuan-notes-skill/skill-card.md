## Description: <br>
A SiYuan notes integration that helps an agent search, read, edit, organize, and query a user's notes through the SiYuan API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanxing-6](https://clawhub.ai/user/fanxing-6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an assistant to a SiYuan workspace for note search, document reading, controlled editing, document organization, and SQL-backed note queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read notes from a SiYuan workspace, exposing private workspace content to the agent session. <br>
Mitigation: Install only for workspaces the agent is allowed to access and use the least-privileged local token available. <br>
Risk: When write mode is enabled, commands can edit, delete, move, replace sections, or apply patches to notes. <br>
Mitigation: Keep SIYUAN_ENABLE_WRITE=false unless edits are intended, and review document or block IDs before write, delete, move, replace-section, or apply-patch operations. <br>
Risk: Token-in-query authentication can expose credentials through URLs or logs. <br>
Mitigation: Avoid token-in-query mode unless required by the environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fanxing-6/siyuan-notes-skill) <br>
- [SiYuan](https://b3log.org/siyuan/) <br>
- [Command Reference](docs/command-reference.md) <br>
- [Patchable Markdown Format](docs/pmf-spec.md) <br>
- [SiYuan SQL Reference](docs/sql-reference.md) <br>
- [Error Recovery](docs/Error-Recovery.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands, JavaScript snippets, and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read commands may return formatted notes or Markdown; write commands can return JSON status from the SiYuan API.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
