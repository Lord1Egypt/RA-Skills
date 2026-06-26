## Description: <br>
金刚罩 is an OpenClaw system guardian skill for configuration validation, backup-backed safe restarts, health patrols, resource cleanup, and failure recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RealHossie](https://clawhub.ai/user/RealHossie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to maintain OpenClaw installations by checking configuration safety, restarting the gateway with rollback protection, auditing changes, and cleaning old local data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete local session, backup, log, and temporary data during automated maintenance. <br>
Mitigation: Review the retention constants and run health patrol manually before enabling scheduled cleanup. <br>
Risk: Backups may create additional plaintext copies of configuration or secret-bearing files. <br>
Mitigation: Secure ~/.openclaw/backups and ~/.openclaw/data/system-guardian, and avoid inline secrets in openclaw.json where possible. <br>
Risk: The skill has restart and rollback authority over an OpenClaw gateway. <br>
Mitigation: Install only when automated OpenClaw maintenance is desired, and review restart behavior before using cron automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RealHossie/system-guardian) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local backup, audit, baseline, and cleanup outputs under the user's OpenClaw directories when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence release version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
