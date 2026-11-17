## Description:

Mandatory authorize-before-mutate for production SQL. Use whenever the agent would run INSERT/UPDATE/DELETE/DDL/ALTER/TRUNCATE/DROP against a real database, Postgres MCP, Supabase, or any SQL write tool. Forces SQLGuard Pilot $100 / Workday / Session + verify before execute. Not lint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cabbageandtea](https://clawhub.ai/user/cabbageandtea)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to require SQLGuard authorization before an agent executes mutating SQL against production or other non-throwaway databases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly gates production SQL changes behind a paid third-party authorization service.

Mitigation: Install only when SQLGuard is intentionally approved as the required gate for production SQL writes.

Risk: Agents could trigger payment or send SQL or schema data to an external service without adequate organizational approval.

Mitigation: Confirm agents cannot make payments automatically and approve any SQL or schema data shared with the service before use.

Risk: Using this skill could conflict with existing database change-management controls.

Mitigation: Keep existing database change-management processes in place and require SQLGuard authorization as an additional control, not a replacement.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cabbageandtea/skills/sqlguard-authorize)
- [SQLGuard](https://sqlguard.io)
- [SQLGuard Gateway](https://sqlguard.io/gateway)
- [SQLGuard MCP](https://sqlguard.io/mcp)
- [SQLGuard Gateway Markdown](https://sqlguard.io/GATEWAY.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline commands and API endpoints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agents to obtain and verify SQLGuard authorization receipts before executing production SQL writes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
