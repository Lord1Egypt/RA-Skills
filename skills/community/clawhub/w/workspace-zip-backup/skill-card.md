## Description: <br>
Fast backup and restore guidance for OpenClaw workspace markdown files, preserving directory structure while excluding non-markdown content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roryyu](https://clawhub.ai/user/roryyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create lightweight zip backups of workspace markdown notes, skills, and memory files, then restore them during migration or recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The restore workflow can overwrite files somewhere other than the destination the user requested. <br>
Mitigation: Restore into an empty staging directory first, inspect the archive contents, and only then move reviewed files into the intended workspace. <br>
Risk: Backup zip files may contain private notes, skills, or memory data. <br>
Mitigation: Keep generated archives private, store them only in trusted locations, and review contents before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roryyu/workspace-zip-backup) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with bash script blocks and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local backup and restore instructions; no network services or API calls are described.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
