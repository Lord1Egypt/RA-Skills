## Description: <br>
Use when interacting with a Trilium Notes server via the ETAPI REST API - creating, reading, updating, searching, or deleting notes, branches, attributes, attachments, day/week/month notes; obtaining auth tokens; or scripting Trilium operations from the shell. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanickxia](https://clawhub.ai/user/yanickxia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to script Trilium Notes ETAPI workflows, including note management, search, export, import, backups, authentication, and shell-based integration debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ETAPI authentication tokens can grant access to notes and may appear in shell history, logs, or shared command output. <br>
Mitigation: Treat ETAPI tokens like passwords, avoid sharing command logs containing tokens, and prefer environment variables or secret handling appropriate to the runtime. <br>
Risk: Generated API commands may delete notes, overwrite note content, import data, export private content, or trigger backups. <br>
Mitigation: Review destructive, import, export, overwrite, and backup commands before execution, and back up important notes before bulk changes. <br>
Risk: Deleting the last branch of a Trilium note also deletes the note. <br>
Mitigation: Check branch relationships before deleting branches, especially in cloned-note workflows. <br>


## Reference(s): <br>
- [Trilium ETAPI endpoint reference](api-reference.md) <br>
- [trilium-py Python client](https://github.com/Nriver/trilium-py) <br>
- [trilium-client Python package](https://pypi.org/project/trilium-client/) <br>
- [trilium-api TypeScript package](https://www.npmjs.com/package/trilium-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples commonly use curl, jq, ETAPI paths, and environment variables such as TRILIUM_URL and TRILIUM_TOKEN.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
