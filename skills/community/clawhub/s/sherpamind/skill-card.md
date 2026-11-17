## Description:

SherpaMind helps agents answer SherpaDesk support-operations questions by using a local SherpaDesk backend plus OpenClaw query layer for ticket lookup, support-history retrieval, account/user/technician analysis, stale-ticket review, workload reporting, and open-ended questions about SherpaDesk data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kklouzal](https://clawhub.ai/user/kklouzal)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams and operators use SherpaMind to prepare, inspect, search, and summarize local SherpaDesk ticket history through OpenClaw. It is suited for questions about accounts, technicians, backlog, recurring issues, ticket status, support history, and retrieval-ready operational reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SherpaDesk API credentials may be sent to a configurable endpoint.

Mitigation: Use the official SherpaDesk API endpoint unless a custom endpoint is intentionally trusted.

Risk: Local artifacts may contain sensitive support data.

Mitigation: Keep .SherpaMind private to the intended user, avoid committing runtime state, and review public exports before sharing.

Risk: Background sync can continue collecting and refreshing support data after setup.

Mitigation: Enable the user-level service only when ongoing sync is desired, and otherwise use explicit one-shot commands.

## Reference(s):

- [SherpaMind homepage](https://github.com/kklouzal/SherpaMind)
- [ClawHub skill page](https://clawhub.ai/kklouzal/skills/sherpamind)
- [SherpaDesk API documentation](https://github.com/sherpadesk/api/wiki)
- [OpenClaw Query Model](references/openclaw-query-model.md)
- [Architecture](references/architecture.md)
- [Retrieval Architecture](references/retrieval-architecture.md)
- [Automation](references/automation.md)
- [Bootstrap / Onboarding](references/bootstrap-onboarding.md)
- [API Reference Notes](references/api-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus generated local Markdown and JSONL artifacts from the SherpaMind backend]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create workspace-local runtime state, SQLite data, logs, public inspection artifacts, vector exports, and an optional user-level systemd service when configured for live use.]

## Skill Version(s):

0.1.7 (source: server release evidence; artifact pyproject.toml lists 0.1.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
