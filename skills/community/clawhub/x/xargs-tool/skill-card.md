## Description: <br>
Build and execute command lines from standard input for batch argument processing, parallel execution, argument substitution, and delimiter control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to construct and run repeated local command invocations from piped input, such as processing file lists or applying one command to many arguments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local batch commands, including file deletion or modification commands. <br>
Mitigation: Require explicit human review before executing destructive or file-modifying commands, and run only commands the user intentionally approved. <br>
Risk: The documentation advertises dry-run and interactive options that the included script does not implement. <br>
Mitigation: Do not rely on documented dry-run or interactive safeguards unless the implementation is fixed and revalidated. <br>


## Reference(s): <br>
- [Xargs Tool release page](https://clawhub.ai/dinghaibin/xargs-tool) <br>
- [dinghaibin publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local subprocesses when used through the included script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
