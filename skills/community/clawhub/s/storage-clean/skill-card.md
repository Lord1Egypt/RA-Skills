## Description: <br>
Analyzes disk usage across Windows, macOS, and Linux, generates an interactive HTML report, and proposes tiered cleanup commands without automatically deleting files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inventory local disk usage, identify large files and development artifacts, and decide which cleanup commands to review and run manually. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated inventory reports can expose local usernames, hostnames, and file paths. <br>
Mitigation: Keep reports local by default, and sanitize sensitive paths or host details before sharing them. <br>
Risk: Generated cleanup commands and the optional cleaner script can remove files, including irreversible deletion paths. <br>
Mitigation: Review every target path before execution, prefer recycle-bin or trash actions, and keep backups for important data. <br>
Risk: The server security review marked the release suspicious because broad local inventory and deletion tooling are not fully scoped by the safety language. <br>
Mitigation: Install only in environments where broad local scanning is acceptable and restrict use to trusted users who understand the cleanup commands. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/bettermen/storage-clean) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; scanner output includes JSON data and an interactive HTML report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and psutil; generated reports may contain local usernames, hostnames, and file paths.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
