## Description: <br>
A ClawHub skill installer that helps agents search for skills, install single skills, and batch install multiple skills with retry logic and version management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to search ClawHub and install one or more skills into a local skills directory. It is intended for normal ClawHub release usage, but installation should be reviewed because it modifies local skill files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can overwrite local skills. <br>
Mitigation: Use it only in a disposable or backed-up skills environment and confirm the hard-coded skills path before execution. <br>
Risk: The installer can run unsafe shell commands from user-provided input. <br>
Mitigation: Pass only simple, trusted skill names and review commands before executing them. <br>
Risk: Downloaded skill archives are not safely verified by this package. <br>
Mitigation: Prefer an official scoped installer flow when possible, and review and scan installed skills before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunnyhot/sunnyhot-skill-installer) <br>
- [Publisher profile](https://clawhub.ai/user/sunnyhot) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download, extract, overwrite, and install skill files when the generated shell commands are executed.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
