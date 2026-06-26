## Description: <br>
查询客流数据，输出JSON，适合直接导入 Bitable 或其它数据可视化工具 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z1chengge](https://clawhub.ai/user/z1chengge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users and developers use this skill to query passenger-flow data for a specified date range from a configured SQL Server database and return JSON for Bitable or other visualization workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to a configured SQL Server and may return business passenger-flow data. <br>
Mitigation: Install only for the intended database, configure credentials through protected environment variables, and avoid sharing prompts or logs that may contain returned business data. <br>
Risk: Database credentials with broad privileges could expose more data than the passenger-flow query requires. <br>
Mitigation: Use a dedicated read-only or stored-procedure-limited database account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/z1chengge/python-ysddata-keliu) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON-like text containing status, columns, and rows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SQL Server connection settings from protected environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
