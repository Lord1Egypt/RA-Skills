## Description: <br>
Automatically sync local skills to ClawHub and GitHub by detecting new or modified skills, publishing to ClawHub, committing to GitHub, and maintaining sync status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use Skill Sync to automate publishing and repository synchronization for their own ClawHub skills. It scans configured skill directories, identifies release candidates, publishes updates, commits changes, and records sync status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically publish to ClawHub and push Git commits with weak review controls. <br>
Mitigation: Disable unattended cron or automatic publishing until a review step and explicit confirmation are configured. <br>
Risk: Unsafe shell command construction may allow skill metadata to affect command execution. <br>
Mitigation: Audit and fix command construction before use; restrict synchronized skills to a narrow allowlist. <br>
Risk: Automated repository synchronization may publish sensitive local content if repositories are not reviewed. <br>
Mitigation: Audit synchronized repositories for secrets and generated files before enabling auto-commit, auto-push, or publishing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sunnyhot/skill-sync) <br>
- [Publisher Profile](https://clawhub.ai/user/sunnyhot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown reports, console logs, JSON status files, and shell command execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish to ClawHub, commit and push Git repositories, and update local status and log files when configured to run.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
