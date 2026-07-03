## Description: <br>
查询搜索和获取博物馆的开放藏品数据 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to list Met Museum departments, search open collection objects, and retrieve details for a specific object ID. The skill requires a XiaoBenYang API key and routes requests through that third-party MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests for Met Museum collection data are routed through the XiaoBenYang third-party MCP service instead of directly to a public Met endpoint. <br>
Mitigation: Install only if the user trusts XiaoBenYang and is comfortable sending museum lookup requests and parameters through that service. <br>
Risk: The skill stores the XiaoBenYang API key in a local plaintext .env file. <br>
Mitigation: Use a limited-scope key if available, protect the workspace, avoid committing .env, and rotate the key if the workspace is shared or exposed. <br>
Risk: The published description focuses on open collection lookup while the security evidence flags a third-party API dependency. <br>
Mitigation: Review the setup requirements and upstream service dependency before use, especially in environments with strict data-routing or credential-storage policies. <br>


## Reference(s): <br>
- [XiaoBenYang](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP API](https://mcp.xiaobenyang.com) <br>
- [ClawHub skill page](https://clawhub.ai/alinklab/skills/the-met) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, JSON] <br>
**Output Format:** [Markdown summaries derived from JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns list, search, and object-detail data from the upstream service; requires a local API key before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
