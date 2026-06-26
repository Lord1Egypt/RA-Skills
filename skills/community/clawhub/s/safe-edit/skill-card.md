## Description: <br>
Safe Edit helps agents back up important configuration files and schedule a timed rollback before making risky configuration changes across Linux, macOS, FreeBSD, and Windows-like shell environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ijevin](https://clawhub.ai/user/ijevin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and OpenClaw users use this skill before modifying configuration files so an agent can create a backup, schedule a 15-minute rollback, and cancel the rollback after the change is confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can schedule rollback actions that restore files later and may run with elevated host permissions. <br>
Mitigation: Use it only for explicit target file paths selected by the user, and verify the scheduled rollback restores only the intended backup. <br>
Risk: The helper may install or rely on the at scheduling package on some Linux or BSD systems. <br>
Mitigation: Review host package changes before installation and confirm the scheduler dependency is acceptable for the deployment environment. <br>
Risk: Forgetting to confirm or cancel a rollback can revert a valid configuration change after validation. <br>
Mitigation: After testing the edited configuration, run the documented confirm or cancel command to clear the pending rollback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ijevin/safe-edit) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference backup paths, rollback status, and confirmation or cancellation commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
