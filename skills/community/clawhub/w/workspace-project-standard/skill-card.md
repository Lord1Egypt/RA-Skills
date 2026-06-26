## Description: <br>
Project workspace setup and documentation standard for OpenClaw agents that enforces a three-layer documentation system and self-contained project structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnshyo](https://clawhub.ai/user/lnshyo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill when starting a new project, organizing an existing workspace, or creating project documentation. It guides agents to keep project code, temporary files, and documentation in predictable locations and to maintain MEMORY.md plus per-project docs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace organization guidance may move or reclassify files in ways that affect a project layout. <br>
Mitigation: Review the scaffold script, resulting diffs, and root-file moves before accepting changes; keep the workspace under version control. <br>
Risk: Project documentation templates include credential reference sections that could be misused to record secrets directly. <br>
Mitigation: Document only secret names, vault paths, or environment variable references, and avoid writing actual credential values into project docs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lnshyo/workspace-project-standard) <br>
- [Project documentation template](assets/project-template.md) <br>
- [Links and paths template](assets/links-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline PowerShell commands and project documentation templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API calls or credential values are required; credentials should be documented only as secret names or vault/environment references.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
