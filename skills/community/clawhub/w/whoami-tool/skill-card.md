## Description: <br>
Prints the USER environment variable as a simple current-username check. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation authors use this skill for a quick username check in scripts and session logs. It should not be used for UID, GID, group membership, root detection, or access-control decisions unless the implementation is corrected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation advertises security-relevant identity checks that the included script does not implement. <br>
Mitigation: Use the skill only for a simple USER environment-variable print, or correct the implementation before relying on effective-user, UID, GID, group, JSON, or access-control behavior. <br>


## Reference(s): <br>
- [Whoami Tool on ClawHub](https://clawhub.ai/dinghaibin/whoami-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text username output with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included script prints the USER environment variable and does not implement the documented full identity, group, JSON, UID, or user-check options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
