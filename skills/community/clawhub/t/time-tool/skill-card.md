## Description: <br>
Measure execution time of commands. Use for performance benchmarking, script optimization, and timing analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to measure command execution time while benchmarking scripts, checking performance changes, or comparing command behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run user-specified local commands for timing, which may mutate files, expose secrets, or access sensitive accounts if unsafe commands are provided. <br>
Mitigation: Use it only in workspaces where command execution is acceptable, and time trusted commands that do not touch important files, secrets, or sensitive accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/time-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text timing output and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports elapsed time for a user-specified local command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
