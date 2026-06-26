## Description: <br>
Display directory structure as an indented tree for visualizing folder hierarchies and project structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect local project or folder structure as an indented directory tree. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool prints file and folder names from the path it is given, including hidden names. <br>
Mitigation: Run it only on directories whose names can be disclosed, and review output before sharing it. <br>
Risk: Some documented command-line options do not match the implemented script flags. <br>
Mitigation: Check the script-supported flags or run a local test before relying on documented examples in automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/tree-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text directory tree, with Markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script reads a local path and prints directory and file names; some documented command-line options do not match the implemented script flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
