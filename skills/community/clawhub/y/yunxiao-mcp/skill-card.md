## Description:

Queries and updates Yunxiao work items, comments, projects, and organization members from OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n-wen](https://clawhub.ai/user/n-wen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and delivery teams use this skill to inspect Yunxiao project work, retrieve work item details and comments, create comments, and search organization members from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm MCP server with broad environment access.

Mitigation: Pin the MCP server dependency, pass only required environment variables, and avoid running it where unrelated secrets are present.

Risk: The create_comment command can post immediately to Yunxiao work items.

Mitigation: Require explicit user confirmation before create_comment and use a least-privileged Yunxiao token.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/n-wen/skills/yunxiao-mcp)
- [Yunxiao DevOps](https://devops.aliyun.com)
- [alibabacloud-devops-mcp-server](https://www.npmjs.com/package/alibabacloud-devops-mcp-server)
- [Yunxiao OpenAPI documentation](https://help.aliyun.com/document_detail/261300.html)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YUNXIAO_ACCESS_TOKEN and may use YUNXIAO_ORG_ID or auto-detected organization IDs.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
