## Description: <br>
Automatically scans an OpenClaw workspace and maintains a WORKSPACE_INDEX.md with directory purposes, running status, memory references, and search keywords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Harukaon](https://clawhub.ai/user/Harukaon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to keep a concise directory-level inventory of a workspace, including what each directory is for, whether it appears active, and which memory files or keywords help locate related context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated workspace index may contain private project names, memory references, ports, container IDs, and cleanup or status notes. <br>
Mitigation: Install only in workspaces you are comfortable indexing, and review WORKSPACE_INDEX.md before committing or sharing it. <br>
Risk: Daily HEARTBEAT maintenance can update the index on a recurring basis. <br>
Mitigation: Enable daily maintenance only when recurring automatic updates are desired, and periodically inspect the generated changes. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/Harukaon/workspace-indexer) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown file named WORKSPACE_INDEX.md with directory-level descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include project names, memory references, running service details, ports, container IDs, and cleanup or status notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
