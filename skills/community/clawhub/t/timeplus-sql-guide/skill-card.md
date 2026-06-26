## Description: <br>
Write and execute Timeplus streaming SQL for real-time analytics, including stream creation, streaming queries, materialized views, ingestion, sinks, UDFs, random streams, and full SQL syntax. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gangtao](https://clawhub.ai/user/gangtao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to compose, inspect, and run Timeplus streaming SQL for real-time analytics workflows. It supports common operational tasks such as creating streams, querying historical or live data, ingesting events, building materialized views, sending data to sinks, and defining UDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL or commands can make persistent database changes, including CREATE, DROP, INSERT, DELETE, UDF creation, package installation, sink creation, and webhook or connector actions. <br>
Mitigation: Review every generated command before execution and require explicit approval before running commands that modify data, install packages, create UDFs, create sinks, or transmit data outside Timeplus. <br>
Risk: The skill requires Timeplus credentials and can connect to live Timeplus environments. <br>
Mitigation: Use scoped, low-privilege credentials with trusted Timeplus environments and avoid hardcoding credentials in SQL or command text. <br>
Risk: Commands may send data over HTTP interfaces or to external services. <br>
Mitigation: Prefer HTTPS or a protected local network and review webhook, sink, and external connector targets before use. <br>


## Reference(s): <br>
- [Timeplus Documentation](https://docs.timeplus.com) <br>
- [Timeplus Proton GitHub Repository](https://github.com/timeplus-io/proton) <br>
- [Timeplus SQL Guide on ClawHub](https://clawhub.ai/gangtao/timeplus-sql-guide) <br>
- [Getting Data Into Timeplus](references/INGESTION.md) <br>
- [Transformations](references/TRANSFORMATIONS.md) <br>
- [Sending Data Out of Timeplus](references/SINKS.md) <br>
- [SQL Reference](references/SQL_REFERENCE.md) <br>
- [Random Streams](references/RANDOM_STREAMS.md) <br>
- [UDFs](references/UDFS.md) <br>
- [Python Table Functions](references/Python_TABLE_FUNCTION.md) <br>
- [EMIT Clauses and UDAF Emit Control](references/EMIT_AND_UDAF.md) <br>
- [Scheduled Tasks](references/TASK.md) <br>
- [Real-time Alerts in Timeplus](references/ALERT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include curl commands that use TIMEPLUS_HOST, TIMEPLUS_USER, and TIMEPLUS_PASSWORD.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
