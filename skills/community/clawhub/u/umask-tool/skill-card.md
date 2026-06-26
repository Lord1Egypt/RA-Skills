## Description: <br>
Set or display file creation permission mask. Use for controlling default file permissions on new files and directories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect or intentionally change the default file creation permission mask when configuring permissions for newly created files and directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The utility can silently change file-permission behavior while documentation presents display of the current mask as a normal use. <br>
Mitigation: Review before installing or invoking; use explicit show and set modes, validate any requested mask, and confirm whether changes affect only a subprocess or a longer-lived agent environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/umask-tool) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with bash command examples and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No structured output; security evidence notes that display-style use may still affect file-permission behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
