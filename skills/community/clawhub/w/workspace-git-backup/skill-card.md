## Description: <br>
Sets up automatic scheduled backups of an OpenClaw workspace or another directory to GitHub or GitLab on macOS or Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cooperun](https://clawhub.ai/user/Cooperun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure recurring Git-based backups for a workspace or directory, create or connect a remote repository, and manage scheduled backup jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring automation can commit and push all non-ignored files from the selected directory to a remote Git host. <br>
Mitigation: Before enabling scheduling, verify the Git remote, repository privacy, authenticated account, and ignore rules; run one manual backup and inspect the commit. <br>
Risk: An incorrect backup path or repository configuration can expose unintended workspace, secret, or personal files. <br>
Mitigation: Choose the backup directory deliberately and exclude sensitive files before running Git add, commit, or push operations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install scheduled tasks and create or modify Git configuration, log files, and backup scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
