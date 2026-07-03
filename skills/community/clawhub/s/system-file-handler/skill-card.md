## Description: <br>
System File Handler lets an agent list directories, read and write files, create directories, delete files, and move files through MCP stdio filesystem operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgwventrue](https://clawhub.ai/user/lgwventrue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to let an agent perform local filesystem operations in a configured workspace, including directory listing, file reads and writes, directory creation, deletion, and moves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write, delete, and move real local files, and the security evidence says these powers are not clearly scoped or guarded. <br>
Mitigation: Use the skill only in a constrained workspace, keep backups, and require explicit confirmation before destructive write, delete, or move requests. <br>
Risk: The skill depends on locally built binaries and an absolute MCP command path. <br>
Mitigation: Install binaries only from trusted source material, verify the configured command path before use, and avoid granting broader filesystem access than the task requires. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lgwventrue/system-file-handler) <br>
- [go-fs-mcp Homepage](https://github.com/go-fs-mcp/go-fs-mcp) <br>
- [go-fs-mcp Operations Guide](https://github.com/go-fs-mcp/go-fs-mcp/blob/main/docs/OPERATIONS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files] <br>
**Output Format:** [JSON operation results containing tool names and result text; file contents or directory listings may be returned as text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can modify or remove local files when write, delete, or move operations are requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
