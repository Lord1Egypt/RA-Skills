## Description: <br>
One-command disk cleanup for macOS and Linux: trash, caches, temp files, old kernels, snap revisions, Homebrew, Docker, and Xcode artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camopel](https://clawhub.ai/user/camopel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and power users use this skill to inspect and reclaim disk space on macOS or Linux systems by running a cleanup script with dry-run and selective skip options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup script can delete broad user and system data, including caches, trash, logs, Docker artifacts, Xcode build data, package caches, snap revisions, and old kernels. <br>
Mitigation: Run with --dry-run first, review the listed actions, and use --yes only after confirming the cleanup targets are acceptable. <br>
Risk: Some cleanup actions may remove data that is useful for rollback, rebuilding, debugging, or local development workflows. <br>
Mitigation: Use skip flags such as --skip-docker, --skip-kernels, --skip-brew, and --skip-snap for areas that matter to the current workflow or recovery plan. <br>
Risk: The release evidence notes that the skill overstates how safe and reversible the cleanup is. <br>
Mitigation: Treat cleanup as potentially destructive, keep backups for important local work, and avoid running it on systems where cache or archive removal has not been reviewed. <br>


## Reference(s): <br>
- [Storage Cleanup on ClawHub](https://clawhub.ai/camopel/storage-cleanup) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, guidance] <br>
**Output Format:** [Markdown with bash commands and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script reports cleanup targets, dry-run actions, and disk space before and after cleanup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
