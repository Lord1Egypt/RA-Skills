## Description: <br>
Return exit code 0 indicating success. Use as a no-op command that always succeeds in scripts and conditional expressions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation maintainers use this skill when they need a command that always exits successfully for shell scripts, conditionals, loops, or placeholder branches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Always-success behavior can mask failed checks or accidentally keep automation running. <br>
Mitigation: Use it only where a no-op success command is intentional, and keep surrounding checks explicit. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands] <br>
**Output Format:** [Process exit status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No stdout; exits with status 0.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
