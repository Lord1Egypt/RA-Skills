## Description: <br>
Connects an agent to the Windows Quicker automation tool so it can read, search, match, and execute Quicker actions from CSV or SQLite data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awamwang](https://clawhub.ai/user/awamwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to let an agent find, summarize, and invoke local Quicker workflows on Windows. It is intended for workflows where the user has configured Quicker action data sources and wants natural-language matching before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can invoke local or remote Quicker actions from an agent workflow. <br>
Mitigation: Require explicit user confirmation before action execution, especially when a match is ambiguous or below the configured confidence threshold. <br>
Risk: Configuration may enable remote Quicker execution or expose sensitive local paths. <br>
Mitigation: Avoid configuring push_user or push_code unless remote execution is intentionally required, and protect config.json as a sensitive local configuration file. <br>
Risk: The skill can read configured action databases or CSV files and export action data. <br>
Mitigation: Limit configured paths to the intended Quicker data sources and review export destinations before writing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/awamwang/quicker-connector) <br>
- [Quicker website](https://getquicker.net/) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with Python and shell command examples, plus JSON for exported action lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read configured CSV or SQLite action data, write config or exported JSON files, and invoke QuickerStarter.exe on Windows.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter, package.json, changelog, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
