## Description: <br>
Create, list, and roll back incremental snapshots of OpenClaw configurations and memory with optional automatic backups and retention policies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaceli](https://clawhub.ai/user/chaceli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create manual or automatic restore points before configuration and memory changes, inspect available snapshots, and roll back full or partial state when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Snapshots may contain sensitive material such as API keys, credentials, environment variables, skills, configuration, memory, or private workspace files. <br>
Mitigation: Review snapshot contents and storage location before use; prefer a version that excludes secrets by default or provides real encrypted storage and explicit file previews. <br>
Risk: Rollback operations can overwrite current OpenClaw configuration or memory state. <br>
Mitigation: Use the preview and confirmation flow before restoring, and create a fresh rollback point before applying changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chaceli/time-machine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, JSON configuration snippets, and plain-text status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled scripts can create, list, delete, and restore snapshot files under the user's OpenClaw directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
