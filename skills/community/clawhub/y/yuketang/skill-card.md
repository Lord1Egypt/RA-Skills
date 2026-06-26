## Description: <br>
Provides Rain Classroom account and teaching-class query workflows, including user IDs, class lists, class statistics, warning lists, today's teaching activity, lesson reservation, and assignment or notice completion status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuetangop](https://clawhub.ai/user/xuetangop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External educators and teaching staff use this skill to query Rain Classroom account, class, attendance, warning, correction, assignment, and notice data through the configured MCP service. It can also guide lesson reservation after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Rain Classroom account access through YUKETANG_SECRET. <br>
Mitigation: Treat the secret like a password, set it only through a secure local mechanism, and rotate it if exposed. <br>
Risk: The skill includes lesson-reservation capability that can affect teaching schedules. <br>
Mitigation: Review reservation details with the user and require explicit confirmation before invoking scheduling tools. <br>
Risk: Setup may run dynamic npx tooling and the shell setup sends a silent post-install report. <br>
Mitigation: Review setup scripts before use and disable or avoid reporting steps if they are not acceptable for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xuetangop/yuketang) <br>
- [Rain Classroom Secret Setup](https://www.yuketang.cn/ai-workspace/open-claw-skill) <br>
- [Rain Classroom MCP Endpoint](https://open-ai.xuetangx.com/openapi/v1/mcp-server/sse) <br>
- [API References](references/api_references.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured lists, tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool responses should preserve returned emoji, original wording, and table headers when displayed.] <br>

## Skill Version(s): <br>
1.0.327853 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
