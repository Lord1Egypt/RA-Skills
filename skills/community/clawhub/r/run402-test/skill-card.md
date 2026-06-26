## Description: <br>
Test skill for Run402 — provision AI-native Postgres databases with REST API, auth, and row-level security using x402 micropayments on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MajorTal](https://clawhub.ai/user/MajorTal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to provision Run402 Postgres projects, create tables through the admin SQL endpoint, and query project data over REST. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an admin SQL endpoint with a service key, which can change or damage database state if pointed at the wrong project or SQL statement. <br>
Mitigation: Treat SERVICE_KEY as an admin secret, verify the project ID and SQL before execution, and use backups and explicit review before touching production or valuable data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may produce or rely on project identifiers, anonymous keys, service keys, and SQL statements that require review before use.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
