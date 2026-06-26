## Description: <br>
Smart Restart Protection helps restart OpenClaw Gateway safely with rate limits, lock checks, configuration backups, and status recovery checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackytianjp](https://clawhub.ai/user/jackytianjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators managing OpenClaw Gateway use this skill to inspect restart protection status, run guarded restarts, and reset protection state during emergencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can restart the local OpenClaw Gateway and touches local OpenClaw configuration, session, and workspace state. <br>
Mitigation: Install only when Gateway restart control is intended, review the shell scripts before use, and run them in an environment where local OpenClaw state changes are acceptable. <br>
Risk: Copied OpenClaw configuration backups may contain sensitive local configuration data. <br>
Mitigation: Treat backup files as sensitive, restrict local file permissions, and clean up old backups according to operational policy. <br>
Risk: Documented force, no-backup, or rollback behavior may not be reliable in every environment. <br>
Mitigation: Verify those behaviors directly in the target environment before depending on them for recovery or emergency operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackytianjp/smart-restart-protection) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with inline shell commands, JavaScript snippets, and status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local OpenClaw Gateway commands and read or write local OpenClaw restart state, backups, logs, sessions, and workspace files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
