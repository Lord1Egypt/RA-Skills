## Description: <br>
Randomly shuffle lines of text input for random sampling, data randomization, and selection tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to randomize text lines for sampling, data randomization, and selection tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local helper can read files available to the agent. <br>
Mitigation: Review file paths before execution and avoid using it with sensitive files or sensitive piped input. <br>
Risk: The current artifact has a stdin-handling bug and the documented -n, -i, -r, and -e options are not reliable. <br>
Mitigation: Use explicit non-sensitive input files for simple full-line shuffling, and do not rely on the documented sampling options until the implementation is fixed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dinghaibin/shuf-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and plain text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces shuffled line-oriented text; documented options include sampling modes, but evidence notes some options are not reliable in the current artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
