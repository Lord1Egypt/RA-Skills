## Description: <br>
Whoami Tool Check helps an agent inspect local user identity and account context for access checks and audit workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security reviewers use this skill to confirm the current local account identity and support access-audit checks before security-sensitive work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local identity and audit output can expose usernames, groups, home paths, shells, and sudo status. <br>
Mitigation: Run the skill only in trusted sessions and avoid sharing raw audit output publicly. <br>
Risk: The included executable behavior is minimal and may not provide every documented audit option in every environment. <br>
Mitigation: Confirm available command options in the installed environment before relying on role, sudo, capability, user lookup, or JSON audit results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/whoami-tool-check) <br>
- [Publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text or structured JSON for local identity and access audit results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally and reports account identity or audit context without network output.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
