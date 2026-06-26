## Description: <br>
Interact with SiYuan notes via direct HTTP API for reading, writing, searching, and managing SiYuan blocks, documents, notebooks, attributes, assets, and SQL queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eloklam](https://clawhub.ai/user/eloklam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to interact with a SiYuan note database through authenticated local or trusted-server HTTP API calls. It supports note search and retrieval, markdown export, SELECT-only SQL queries, direct API calls, and guarded block insert, update, and delete operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses SIYUAN_TOKEN to make authenticated calls that can read and modify a SiYuan note database. <br>
Mitigation: Use a trusted SiYuan server, keep SIYUAN_BASE on localhost unless remote access is intentional, and scope operational review around any command that can write, delete, export, or run broad SQL. <br>
Risk: The raw call command can reach arbitrary SiYuan API paths except for explicitly blocked notebook-management endpoints. <br>
Mitigation: Avoid raw call unless the endpoint and request body are known, and require explicit confirmation before invoking non-read API paths. <br>
Risk: Search and SQL commands can expose note content to the agent. <br>
Mitigation: Run SELECT queries only for the minimum needed scope and review requested search terms, notebook IDs, and result limits before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eloklam/siyuan-agent) <br>
- [Publisher profile](https://clawhub.ai/user/eloklam) <br>
- [SiYuan](https://ld246.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIYUAN_TOKEN and optionally SIYUAN_BASE for the target SiYuan server.] <br>

## Skill Version(s): <br>
2.0.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
