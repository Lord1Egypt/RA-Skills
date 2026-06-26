## Description: <br>
Quick system test to verify OpenClaw environment. Simple command execution with output validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GustavoZiaugra](https://clawhub.ai/user/GustavoZiaugra) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to verify that an OpenClaw environment can run Python, inspect the working directory, access files, and execute basic system commands for debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local command execution can run unintended commands or expose local system details. <br>
Mitigation: Use the skill only in a non-sensitive workspace and review commands before execution. <br>
Risk: Environment-dump commands may disclose local configuration or secrets. <br>
Mitigation: Avoid environment-inspection commands and do not allow untrusted users or prompts to choose custom commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/GustavoZiaugra/quick-test) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text with command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local environment details from command output.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
