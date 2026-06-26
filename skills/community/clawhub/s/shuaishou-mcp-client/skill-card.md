## Description: <br>
Connects an agent to the Shuaishou HTYD MCP server through a Streamable HTTP client so it can list and call shop workflow tools, including login, product collection, claim, and Temu publishing tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wang-jie-ss](https://clawhub.ai/user/wang-jie-ss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, shop operators, and automation developers use this skill to connect an agent to Shuaishou shop workflows for collecting product links, claiming products into shop drafts, and publishing or tracking Temu listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish products to live shops through Shuaishou and Temu workflows. <br>
Mitigation: Require human confirmation of the product URL, target shop, platform, and publish action before running collect_and_publish, publish_and_track, publish_temu, or raw MCP calls. <br>
Risk: Authorization may be stored locally for reuse. <br>
Mitigation: Use a dedicated low-privilege MCP key and protect or remove ~/.htyd-mcp-client-streamable.json after use. <br>
Risk: Broad MCP tool access can perform actions beyond simple listing or status checks. <br>
Mitigation: Review requested tool names and arguments before execution, especially login, claim, publish, and generic raw tool calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wang-jie-ss/shuaishou-mcp-client) <br>
- [Shuaishou MCP endpoint](https://dz.shuaishou.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke live MCP tools that affect shop drafts and Temu publishing workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
