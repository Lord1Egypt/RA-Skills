## Description: <br>
Reverses text input character by character for text analysis, palindrome checks, and data format conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and text-processing users use this skill to reverse input text for quick analysis, palindrome checks, and simple data transformation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged script reverses the full stdin stream, while the skill description says each line is reversed independently. <br>
Mitigation: Test representative multi-line input before relying on line-by-line semantics. <br>
Risk: The skill documentation shows file arguments, but the packaged script reads stdin directly. <br>
Mitigation: Pipe file contents to the command or confirm an installed wrapper handles file arguments before use. <br>
Risk: Server security guidance notes that related maintainer-oriented workflows may use broad filesystem access. <br>
Mitigation: Review helper commands before execution and use narrower execution settings where available. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads stdin when invoked as a command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
