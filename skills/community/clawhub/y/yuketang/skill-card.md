## Description:

Provides Rain Classroom account and class query services, including user ID, teaching class lists, class data, warning lists, today's teaching status, assignments, announcements, and completion status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuetangop](https://clawhub.ai/user/xuetangop)

### License/Terms of Use:

MIT-0

## Use Case:

External educators and teaching staff use this skill to query Rain Classroom account identity, teaching classes, class analytics, warning lists, current-day teaching status, lesson reservations, grading workload, assignments, and announcement status through a configured MCP endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires YUKETANG_SECRET, which should be treated like a password.

Mitigation: Keep the secret out of shared logs and shell history, rotate it if exposed, and configure it only in trusted environments.

Risk: The security summary flags undisclosed silent install reporting and recommends reviewing setup.sh before use.

Mitigation: Review the installer before execution and prefer an installer path that makes reporting opt-in.

Risk: The configured MCP endpoint can access Rain Classroom teaching and class data for the authenticated user.

Mitigation: Install only when the user trusts the Rain Classroom MCP endpoint and grants access from an account intended for this use.

## Reference(s):

- [Rain Classroom MCP Tool Reference](references/api_references.md)
- [Rain Classroom Secret Setup](https://www.yuketang.cn/ai-workspace/open-claw-skill)
- [Rain Classroom MCP Endpoint](https://open-ai.xuetangx.com/openapi/v1/mcp-server/sse)
- [ClawHub yuketang Skill Page](https://clawhub.ai/xuetangop/skills/yuketang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured tool-call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP configuration snippets, environment-variable setup steps, and structured Rain Classroom query results.]

## Skill Version(s):

1.0.327853 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
