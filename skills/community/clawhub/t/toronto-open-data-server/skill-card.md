## Description: <br>
Provides agent tools for discovering and querying Toronto open-data datasets, including dataset search, schema inspection, record queries, dataset statistics, and CSV previews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to explore Toronto open-data datasets, inspect schemas, retrieve sample records, and preview CSV-backed data through agent tool calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents itself as Toronto open-data access while routing requests and the XBY API key through a third-party Xiaobenyang service. <br>
Mitigation: Install only if third-party routing and API-key handling are acceptable; prefer a version that calls Toronto CKAN directly or clearly documents proxy, retention, and deletion behavior. <br>
Risk: The skill persists the XBY API key in a local .env file. <br>
Mitigation: Use a scoped or revocable key where possible, avoid shared working directories, and delete the local .env entry when the skill is no longer needed. <br>


## Reference(s): <br>
- [XiaoBenYang API key service](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown summaries of JSON tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool calls return success, raw, and message fields; CSV previews are bounded by a max_lines parameter.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
