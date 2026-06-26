## Description: <br>
Isolated Kali Linux sandbox for running pentest tools and risky commands safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c0ffeeOverdose](https://clawhub.ai/user/c0ffeeOverdose) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security practitioners and developers use this skill to run authorized penetration-testing tools and risky shell commands inside an isolated Kali Linux sandbox instead of on the host. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad shell execution and offensive security tools can be misused or run against unauthorized systems. <br>
Mitigation: Use only for systems you own or are explicitly authorized to test, and review each command before execution. <br>
Risk: Sandbox isolation may not protect the host if network or filesystem boundaries are weak. <br>
Mitigation: Verify the sandbox's network and filesystem boundaries before installing or running commands, and reset or stop the sandbox when behavior is unexpected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/c0ffeeOverdose/prts-sandbox) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, and jq; command results may include stdout, stderr, or JSON status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
