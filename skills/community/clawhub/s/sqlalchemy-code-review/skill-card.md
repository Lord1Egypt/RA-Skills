## Description: <br>
Reviews SQLAlchemy code for session management, relationships, N+1 queries, and migration patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill to review SQLAlchemy 2.0 application code and Alembic migrations for session lifecycle, relationship loading, query style, and migration safety issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review findings may be incorrect or misleading if the agent reports SQLAlchemy issues without reading the relevant source or migration file. <br>
Mitigation: The skill requires findings to be anchored to file and line evidence and directs the agent to withdraw, downgrade, or rephrase claims when the evidence does not support them. <br>
Risk: Using this skill may cause the agent to inspect application source code and database migration files. <br>
Mitigation: Use it only where the agent is allowed to read the target repository, and do not provide secrets or unrelated sensitive files as review input. <br>


## Reference(s): <br>
- [Sessions](references/sessions.md) <br>
- [Relationships](references/relationships.md) <br>
- [Queries](references/queries.md) <br>
- [Migrations](references/migrations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review guidance with file and line references when findings are reported] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no executable code or hidden access requests were reported by the security scan.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
