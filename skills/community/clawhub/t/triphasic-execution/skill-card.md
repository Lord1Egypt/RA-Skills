## Description: <br>
Provides an Execute -> Review -> Advance workflow framework for structured task planning, progress tracking, retry limits, idle-loop cutoffs, and problem or lesson recording. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to impose a structured execution loop on complex tasks, track progress across interruptions, and record problems, risks, and lessons learned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route command execution through an execution wrapper and store command outputs in local logs. <br>
Mitigation: Enable global mode or the execution wrapper only when that behavior is specifically needed, review commands before use, and restrict or clean local logs when commands may include sensitive data. <br>
Risk: The local settings server is unauthenticated and can expose configuration controls while running. <br>
Mitigation: Run the settings server only for active configuration, avoid browsing untrusted sites during that session, and stop the server when configuration is complete. <br>
Risk: Persistent progress, problem, risk, and lesson records may capture task details that should not be retained. <br>
Mitigation: Avoid placing secrets in task descriptions or command text, and review the configured TRIPHASIC_HOME data and log directories before sharing or archiving them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/triphasic-execution) <br>
- [Mandatory workflow rules](references/mandatory.md) <br>
- [Command reference](references/reference.md) <br>
- [Examples](references/examples.md) <br>
- [Antipatterns](references/antipatterns.md) <br>
- [Permissions](references/permissions.md) <br>
- [Changelog](references/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and local configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local progress, log, problem, risk, and lesson files when helper scripts are used.] <br>

## Skill Version(s): <br>
5.19.1 (source: frontmatter, _meta.json, server release evidence, changelog released 2026-06-09) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
