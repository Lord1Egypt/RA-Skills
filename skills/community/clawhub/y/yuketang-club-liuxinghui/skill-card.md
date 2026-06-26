## Description: <br>
Connects agents to Rain Classroom MCP tools so teachers can query account, class, teaching activity, warning, homework, exam, and announcement data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[softwolves](https://clawhub.ai/user/softwolves) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers and education-support agents use this skill to configure Rain Classroom MCP access and retrieve structured teaching, class, assignment, announcement, warning, and lesson-reservation information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a personal Rain Classroom secret and may expose teacher, class, and student data through a remote MCP endpoint. <br>
Mitigation: Install only when authorized for the relevant Rain Classroom data, keep the bearer value in YUKETANG_SECRET, and avoid committing MCP configuration files containing secrets. <br>
Risk: The shell installer can configure persistent remote MCP access and includes under-disclosed setup behavior. <br>
Mitigation: Prefer manual MCP configuration when possible, review installer behavior before execution, and remove or review the silent setup.sh claw_report call before running the shell installer. <br>


## Reference(s): <br>
- [Rain Classroom MCP Tool Reference](artifact/references/api_references.md) <br>
- [Rain Classroom Secret Setup](https://ykt-env-example.rainclassroom.com/ai-workspace/open-claw-skill) <br>
- [Rain Classroom MCP Endpoint](https://open-envning.rainclassroom.com/openapi/v1/mcp-server/sse) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands and structured tool-call instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool results should be structured as lists, preserve returned emoji and original wording, and avoid inventing course data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
