## Description: <br>
Salesclaw provides a pharmaceutical sales ontology database, MySQL-backed knowledge base, and SQL/query tools for NL2SQL-style sales analytics and attribution analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gptplusplus](https://clawhub.ai/user/gptplusplus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and sales analytics teams use Salesclaw to initialize and query a MySQL ontology for pharmaceutical sales, reuse documented SQL templates, and run attribution workflows for prescriptions, expenses, territory coverage, representatives, hospitals, and compliance alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may silently read and write OpenClaw memory with sensitive business context. <br>
Mitigation: Disable or patch memory read/write paths unless cross-session sharing is intended, access-controlled, and reviewed for sensitive data. <br>
Risk: Database initialization can rebuild or drop the Salesclaw database when forced. <br>
Mitigation: Use a disposable or least-privilege MySQL account, test against non-production databases, and avoid force initialization outside controlled test environments. <br>
Risk: Queries and outputs may expose sales, hospital, doctor, representative, or compliance data. <br>
Mitigation: Run only against approved datasets, limit database credentials to the required scope, and review generated SQL and result handling before use with real data. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/gptplusplus/salesclaw) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [Knowledge index](artifact/knowledge/index.md) <br>
- [Knowledge operation log](artifact/knowledge/log.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON-like tool responses, SQL snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MySQL access and may read or write OpenClaw memory depending on the invoked tool.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release evidence, created 2026-05-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
