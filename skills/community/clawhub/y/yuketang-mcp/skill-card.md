## Description:

提供雨课堂账户和班级相关查询服务，包括用户ID、开班列表、班级数据、预警名单、今日授课及作业公告完成情况查询等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuetangop](https://clawhub.ai/user/xuetangop)

### License/Terms of Use:

MIT-0

## Use Case:

Educators and teaching staff use this skill to query YuKeTang/Rain Classroom account details, teaching classes, class statistics, warning lists, daily teaching activity, correction statistics, homework submissions, announcement reads, and lesson reservations through the YuKeTang MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires YUKETANG_SECRET, which grants access to Rain Classroom account data and class scheduling actions.

Mitigation: Treat YUKETANG_SECRET like a password, avoid pasting it into chats or logs, and install only when the YuKeTang/Rain Classroom MCP service is trusted.

Risk: The bundled installers run unpinned external npx code.

Mitigation: Review the installer before use and prefer a pinned setup path where available.

Risk: The shell installer sends an undisclosed install report.

Mitigation: Review telemetry behavior before running setup.sh and choose an installation path that matches organizational policy.

## Reference(s):

- [YuKeTang Secret setup](https://www.yuketang.cn/ai-workspace/open-claw-skill)
- [YuKeTang MCP SSE endpoint](https://open-ai.xuetangx.com/openapi/v1/mcp-server/sse)
- [YuKeTang MCP tool reference](references/api_references.md)
- [ClawHub skill page](https://clawhub.ai/xuetangop/skills/yuketang-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured text, command examples, and MCP configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP tool calls that return Rain Classroom account, class, attendance, warning, assignment, announcement, and lesson reservation data.]

## Skill Version(s):

1.0.326682 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
