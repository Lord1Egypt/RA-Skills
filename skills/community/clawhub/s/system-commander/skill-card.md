## Description: <br>
Converts user tasks into Linux or Python command suggestions for file processing, data extraction, text manipulation, and related system-level work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nelohenriq](https://clawhub.ai/user/nelohenriq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical users use this skill to select efficient shell or Python commands for file processing, data extraction, text manipulation, and command-oriented automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested commands may modify files or install packages if run without review. <br>
Mitigation: Inspect commands before execution, verify paths, prefer dry runs and backups, and take extra care with sed -i, mv, xargs, and apt-get. <br>
Risk: Command suggestions may be unsuitable for sensitive or privileged operations. <br>
Mitigation: Use separate review before applying generated commands to sensitive data, privileged environments, or high-impact systems. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/nelohenriq/system-commander) <br>
- [Publisher Profile](https://clawhub.ai/user/nelohenriq) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include brief explanations, expected output examples, alternatives, dry-run commands, and package installation notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
