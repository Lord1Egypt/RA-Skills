## Description: <br>
LLM-driven warehouse metadata governance that helps generate and review table and field comments using Hive or read-only MCP collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rickitsui](https://clawhub.ai/user/rickitsui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data platform engineers and warehouse governance teams use this skill to inspect schemas, infer concise Chinese field descriptions, review low-confidence suggestions, and persist approved metadata. In pyhive mode it can write approved comments back to Hive; in MCP mode it keeps results in SQLite. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read warehouse samples or view definitions that contain sensitive, regulated, or secret-bearing data. <br>
Mitigation: Run first in MCP or read-only mode, restrict scans with database and table scope, and avoid routing sensitive samples or view definitions to external LLM endpoints unless policy permits it. <br>
Risk: In pyhive mode, approved LLM-generated comments can be written back to Hive at scale. <br>
Mitigation: Set writeback.hive_comment=false for review runs, inspect generated comments before applying them, and start with a test database or table before enabling broader writeback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rickitsui/warehouse-meta) <br>
- [Architecture reference](references/architecture.md) <br>
- [Configuration template](references/config_template.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update SQLite metadata stores, generated comments, review queues, configuration files, and Hive comments depending on selected mode.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
