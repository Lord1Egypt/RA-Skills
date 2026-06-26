## Description: <br>
Use when needing to query or update Yunxiao work items, comments, projects, or organization members from OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n-wen](https://clawhub.ai/user/n-wen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Yunxiao work items, projects, comments, organizations, and members from an OpenClaw workflow. It can also create comments on Yunxiao work items when the user provides a token and explicitly requests that action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create comments on shared Yunxiao work items. <br>
Mitigation: Require explicit user approval before running create_comment and review the target work item and comment content before submission. <br>
Risk: The CLI runs an external npm MCP server with the user's Yunxiao access token. <br>
Mitigation: Install only when the Alibaba Cloud DevOps MCP package is trusted and use a least-privilege Yunxiao token. <br>
Risk: Automatic organization resolution may use the first returned organization if YUNXIAO_ORG_ID is not set. <br>
Mitigation: Set YUNXIAO_ORG_ID explicitly or pass the organization ID on commands that support it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/n-wen/yunxiao-mcp) <br>
- [Alibaba Cloud Yunxiao](https://devops.aliyun.com) <br>
- [alibabacloud-devops-mcp-server](https://www.npmjs.com/package/alibabacloud-devops-mcp-server) <br>
- [Yunxiao OpenAPI documentation](https://help.aliyun.com/document_detail/261300.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Yunxiao work item, project, comment, organization, and member data returned by the MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
