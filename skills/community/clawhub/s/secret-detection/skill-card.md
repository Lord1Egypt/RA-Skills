## Description: <br>
Git hook to detect secrets before commit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Derick001](https://clawhub.ai/user/Derick001) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install a local Git pre-commit scanner that checks staged files or explicit paths for common credentials before commit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the hook can replace an existing pre-commit hook. <br>
Mitigation: Check whether the repository already has a pre-commit hook and back it up before installation. <br>
Risk: Detected credentials can be printed into local output or logs. <br>
Mitigation: Avoid shared terminals, CI logs, and agent transcripts unless output is redacted; rotate any real secret that appears in scanner output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Derick001/secret-detection) <br>
- [Publisher profile](https://clawhub.ai/user/Derick001) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and scanner output as text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scanner can return a non-zero exit code when secrets are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
