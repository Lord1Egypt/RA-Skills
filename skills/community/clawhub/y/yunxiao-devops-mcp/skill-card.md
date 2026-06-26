## Description: <br>
Yunxiao DevOps MCP lets agents operate Alibaba Cloud Yunxiao over MCP SSE for project management, work items, pipelines, code repositories, deployment workflows, and more than 165 tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonasgao](https://clawhub.ai/user/jonasgao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and agents use this skill to discover Yunxiao MCP tools, inspect their schemas, and call them for project, work item, pipeline, repository, and deployment operations. It is intended for environments where a human has deployed and authorized the Yunxiao MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate powerful Yunxiao cloud, repository, pipeline, file, and deployment workflows through MCP tools. <br>
Mitigation: Require explicit human confirmation before create, update, file, pipeline, or deployment actions. <br>
Risk: Yunxiao access depends on Alibaba Cloud RAM credentials that may be stored in deployment environment configuration. <br>
Mitigation: Use least-privileged RAM credentials and prefer short-lived or managed secrets over plaintext .env files. <br>
Risk: An exposed MCP server could allow unintended access to Yunxiao DevOps resources. <br>
Mitigation: Restrict the MCP server to localhost or a trusted network and verify the Docker image before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jonasgao/yunxiao-devops-mcp) <br>
- [Yunxiao official documentation](https://help.aliyun.com/zh/yunxiao/) <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>
- [MCP server deployment guide](artifact/DEPLOY.md) <br>
- [Yunxiao MCP SSE client README](artifact/client/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tool listings, JSON schemas and tool results, shell commands, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or later and a reachable Yunxiao MCP SSE server; tool calls may read or modify Yunxiao resources depending on the selected MCP tool and credentials.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
