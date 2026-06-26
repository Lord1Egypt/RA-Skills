## Description: <br>
ReSoul resets an OpenClaw workspace's persona/bootstrap state by fetching the official BOOTSTRAP.md and archiving SOUL.md, USER.md, and IDENTITY.md after explicit second confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tacitlab](https://clawhub.ai/user/tacitlab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill when they intentionally want to reset persona/bootstrap state, restore the upstream bootstrap template, and start the next fresh session from a clean identity setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the reset changes workspace bootstrap state by replacing BOOTSTRAP.md and moving existing SOUL.md, USER.md, and IDENTITY.md out of the workspace root. <br>
Mitigation: Require explicit second confirmation, verify the workspace path before execution, and archive identity files into .trash before removing them from the root. <br>
Risk: The fetched upstream bootstrap is intended for a fresh workspace and may not match an existing workspace's current expectations. <br>
Mitigation: Fetch the template successfully before archiving existing files, then review the restored BOOTSTRAP.md before relying on it in an existing workspace. <br>


## Reference(s): <br>
- [Official OpenClaw BOOTSTRAP.md template](https://raw.githubusercontent.com/openclaw/openclaw/main/docs/reference/templates/BOOTSTRAP.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text] <br>
**Output Format:** [Markdown with inline bash commands and a brief status report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write BOOTSTRAP.md and archive SOUL.md, USER.md, and IDENTITY.md when executed with explicit confirmation.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
