## Description: <br>
Execute read-only Snowflake SELECT queries with forbidden keyword blocking, row limits, timeouts, and structured JSON results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiagohubnerdataplatform](https://clawhub.ai/user/tiagohubnerdataplatform) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Data engineers and analytics agents use this skill to run governed read-only Snowflake SELECT queries and receive bounded JSON result sets with execution metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive Snowflake data could be exposed if the HTTP service is reachable by untrusted callers or uses a broad database role. <br>
Mitigation: Run the service on a trusted local interface, add endpoint access controls, and use a least-privilege Snowflake role limited to approved schemas and tables. <br>
Risk: Unpinned dependencies can change the runtime behavior of a database access service. <br>
Mitigation: Pin dependencies before using the skill with sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tiagohubnerdataplatform/snowflake) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls] <br>
**Output Format:** [Structured JSON object containing query_id, row_count, and results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Snowflake query metadata and rows; appends a row limit when the input SELECT query has no LIMIT clause.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
