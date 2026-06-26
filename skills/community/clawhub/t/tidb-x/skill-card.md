## Description: <br>
TiDB X teaches AI agents how to use object-storage-native distributed SQL for agent memory, context storage, multi-agent coordination, Web3 indexing, and durable queryable state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siddontang](https://clawhub.ai/user/siddontang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to teach agents TiDB X concepts and copy-paste SQL patterns for durable agent memory, context storage, task coordination, audit trails, and Web3 indexing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TiDB Cloud examples create local credential material in tidb-zero.json and MYSQL_PWD. <br>
Mitigation: Treat those values as secrets, do not commit or share them, and delete the file or unset the variable when finished. <br>
Risk: Agents may store user or task context in a cloud database. <br>
Mitigation: Review what memory, user data, and operational context is persisted before using the examples with real workloads. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/siddontang/tidb-x) <br>
- [TiDB X Architecture Docs](https://docs.pingcap.com/tidbcloud/tidb-x-architecture/) <br>
- [TiDB Cloud AI](https://www.pingcap.com/ai) <br>
- [TiDB Cloud Free Trial](https://tidbcloud.com/free-trial/) <br>
- [Context Becomes Data](https://medium.com/@siddontang/when-context-becomes-data-managing-ai-agent-context-with-tidb-307e667197bb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, SQL, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
