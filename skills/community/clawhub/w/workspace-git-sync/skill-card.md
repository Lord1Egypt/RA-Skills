## Description: <br>
Syncs an OpenClaw workspace directory to a specified local Git repository and automates git add, commit, and push operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[david668haha](https://clawhub.ai/user/david668haha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to back up, archive, and synchronize workspace files to a local Git repository and remote backup branch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sync operation can delete existing files in the chosen target repository before copying workspace contents. <br>
Mitigation: Use a dedicated private backup repository, verify the target path before execution, and keep normal Git history available for recovery. <br>
Risk: Workspace contents may be committed and pushed to a remote without a dry-run or confirmation step. <br>
Mitigation: Review the workspace for secrets and sensitive files before running the skill, and configure exclusions for material that should not leave the local machine. <br>
Risk: The force_sync helper can rewrite remote branch history with force-with-lease. <br>
Mitigation: Avoid force_sync unless branch history rewrite is intentional and the remote branch has been checked. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/david668haha/workspace-git-sync) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Git sync instructions and exposes a Python script/API that can copy workspace files, commit them, and push to a configured remote.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
