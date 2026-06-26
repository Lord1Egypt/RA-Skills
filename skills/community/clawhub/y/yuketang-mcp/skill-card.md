## Description: <br>
Provides Rain Classroom account and class query services, including user ID, teaching class lists, class statistics, warning lists, today's teaching activity, homework completion, and announcement-read status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuetangop](https://clawhub.ai/user/xuetangop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External educators and teaching staff use this skill to connect an agent to Rain Classroom/XuetangX MCP tools for account lookup, class analytics, teaching-day summaries, class reservation, and homework or announcement status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires YUKETANG_SECRET and connects to the Rain Classroom/XuetangX MCP endpoint, which can expose account and class data to the configured service. <br>
Mitigation: Install only if the endpoint is trusted, keep YUKETANG_SECRET protected, rotate it if exposed, and remove the MCP configuration when access is no longer needed. <br>
Risk: The setup flow has under-disclosed install-reporting behavior. <br>
Mitigation: Review setup.sh before running it and confirm that the install-reporting call is acceptable in the target environment. <br>
Risk: Class reservation actions can affect scheduled teaching activity. <br>
Mitigation: Approve class reservations only after checking the class, time, title, duration, and meeting type. <br>


## Reference(s): <br>
- [ClawHub yuketang-mcp release page](https://clawhub.ai/xuetangop/yuketang-mcp) <br>
- [Rain Classroom Secret setup page](https://www.yuketang.cn/ai-workspace/open-claw-skill) <br>
- [Rain Classroom/XuetangX MCP endpoint](https://open-ai.xuetangx.com/openapi/v1/mcp-server/sse) <br>
- [API references](references/api_references.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and structured tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on live Rain Classroom/XuetangX MCP responses and require YUKETANG_SECRET for authenticated use.] <br>

## Skill Version(s): <br>
1.0.326682 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
