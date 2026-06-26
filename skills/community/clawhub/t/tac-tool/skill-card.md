## Description: <br>
Concatenate and display files in reverse line order (last line first). Use for viewing log files from newest entries and reversing file content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to view local text files in reverse line order, especially logs where recent entries are most useful first. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can display local file contents to the agent. <br>
Mitigation: Use it only with files the user is comfortable allowing the agent to read and display. <br>
Risk: The implementation appears more limited than the examples and may handle only one filename or fail without an argument. <br>
Mitigation: Prefer a single explicit filename and review behavior before relying on multi-file or stdin workflows. <br>


## Reference(s): <br>
- [Tac Tool on ClawHub](https://clawhub.ai/dinghaibin/tac-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain text file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Displays local file lines in reverse order; implementation evidence indicates it handles one filename and may not behave correctly with no argument.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
