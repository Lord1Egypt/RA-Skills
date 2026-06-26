## Description: <br>
Automatically extracts sequential skill, tool, or function calls from a conversation and stitches them into a configurable, exception-handled Python workflow program. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugpoor](https://clawhub.ai/user/ugpoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to convert repeated chat-driven workflows into reusable Python programs with configurable parameters, output routing, and exception handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes conversation-derived Python and local outputs with weak review and destination controls. <br>
Mitigation: Review generated Python, output paths, API URLs, generated .py files, and task logs before execution. <br>
Risk: Conversation content may contain secrets or private data that could be written into generated code, files, logs, or API destinations. <br>
Mitigation: Use the skill only on trusted conversations and avoid workflows containing secrets or private data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ugpoor/skill-fix-workflow) <br>
- [Skill Documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Files, Configuration] <br>
**Output Format:** [Python files and structured status dictionaries with human-facing instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated workflows may write local files, task logs, API output settings, or HTML based on the selected output mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
