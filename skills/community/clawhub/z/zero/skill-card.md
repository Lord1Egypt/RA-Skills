## Description: <br>
Create ephemeral TiDB Cloud Zero databases for agent workflows in Technical Preview. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bosn](https://clawhub.ai/user/Bosn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to provision temporary TiDB Cloud Zero databases, capture connection details, and run smoke-test or bootstrap SQL for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill returns TiDB Cloud Zero connection details that include sensitive credentials. <br>
Mitigation: Keep saved JSON files and connection strings out of logs and source control, use restrictive file permissions, and delete credentials after use or expiration. <br>
Risk: The skill proposes curl and mysql commands that can create cloud resources or run SQL. <br>
Mitigation: Review commands before execution and confirm the target endpoint and SQL statements match the intended workflow. <br>
Risk: The documented API path is Technical Preview and may change. <br>
Mitigation: Confirm the endpoint and response shape before relying on the skill in repeatable workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Bosn/zero) <br>
- [TiDB Cloud Zero API endpoint](https://zero.tidbapi.com/v1alpha1/instances) <br>
- [TiDB SQL skill](https://skills.sh/pingcap/agent-rules/tidb-sql) <br>
- [PyTiDB skill](https://skills.sh/pingcap/agent-rules/pytidb) <br>
- [TiDB Cloud documentation](https://docs.pingcap.com/tidbcloud/) <br>
- [TiDB Cloud website](https://tidbcloud.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, SQL, JSON, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local JSON files containing temporary database credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
