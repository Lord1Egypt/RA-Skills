## Description: <br>
Backs up OpenClaw workspace configuration, scripts, memory files, and skill metadata to a configurable GitHub repository with token sanitization support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mayueanyou](https://clawhub.ai/user/mayueanyou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create repeatable backups of workspace configuration, automation scripts, memory logs, and skill metadata in a private GitHub repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may send OpenClaw workspace state, including memory and profile-style files, to the configured GitHub repository. <br>
Mitigation: Use a private repository at minimum, review the exact backup file list before running, and exclude or encrypt sensitive notes where appropriate. <br>
Risk: The skill performs remote git writes and supports force-push behavior. <br>
Mitigation: Run dry-run mode first and avoid force-push unless overwriting remote history is intended. <br>
Risk: Token sanitization is scoped to known configuration fields and may not cover credentials embedded in free-form files. <br>
Mitigation: Review MEMORY.md, SOUL.md, USER.md, logs, scripts, and other free-form files before backup, and remove secrets that are outside the sanitizer's covered fields. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mayueanyou/self-backup) <br>
- [GitHub CLI](https://cli.github.com/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on configuring a GitHub backup repository, running setup and backup scripts, and restoring backed-up files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
