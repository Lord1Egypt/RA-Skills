## Description: <br>
Rain Classroom MCP connector for accessing class, teaching activity, and student data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[softwolves](https://clawhub.ai/user/softwolves) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators and teaching assistants with Rain Classroom access use this skill to query their account, teaching classes, classroom statistics, warning lists, lesson attendance and response data, grading workload, assignment completion, announcement reading, and lesson reservation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses YUKETANG_SECRET to authenticate to Rain Classroom. <br>
Mitigation: Treat YUKETANG_SECRET like a password, keep it out of shared logs and screenshots, and rotate it if it may have been exposed. <br>
Risk: The installer writes or suggests MCP configuration that connects to the Rain Classroom endpoint. <br>
Mitigation: Review the generated project MCP configuration after setup and install only if the endpoint and publisher are trusted. <br>
Risk: The shell installer can silently report installation duration through the configured MCP service. <br>
Mitigation: Review setup.sh before running it and remove or disable the claw_report call if silent installation reporting is not acceptable. <br>
Risk: The skill can access classroom, teaching activity, attendance, grading, assignment, announcement, and student warning data. <br>
Mitigation: Use it only from an authorized Rain Classroom account and avoid sharing returned student or classroom data beyond the intended audience. <br>


## Reference(s): <br>
- [ClawHub yuketang-incub listing](https://clawhub.ai/softwolves/yuketang-incub) <br>
- [Publisher profile: softwolves](https://clawhub.ai/user/softwolves) <br>
- [Rain Classroom secret setup](https://ykt-envning.rainclassroom.com/ai-workspace/open-claw-skill) <br>
- [Rain Classroom MCP endpoint](https://open-envning.rainclassroom.com/openapi/v1/mcp-server/sse) <br>
- [API references](artifact/references/api_references.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese-language Markdown and plain text responses, shell commands, and MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some tool results must preserve the original returned text, emoji, tables, links, and class statistics without rewriting.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
