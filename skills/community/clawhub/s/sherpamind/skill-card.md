## Description: <br>
SherpaMind helps agents query, retrieve, and analyze SherpaDesk ticket history, support operations, stale tickets, workload, accounts, users, technicians, and related operational reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kklouzal](https://clawhub.ai/user/kklouzal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support teams and operators use SherpaMind through an agent to inspect SherpaDesk ticket history, retrieve prior support context, analyze accounts or technician workload, and produce operational summaries grounded in local SherpaDesk data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SherpaMind can store SherpaDesk API credentials and broad ticket history in local plaintext workspace files. <br>
Mitigation: Install only in a trusted private workspace, restrict filesystem access, and avoid sharing doctor, bootstrap, database, log, or export output. <br>
Risk: Generated public Markdown and export files can contain sensitive support details derived from ticket history. <br>
Mitigation: Review `.SherpaMind/public` and export destinations before sharing, and keep customer, account, user, technician, and ticket details anonymized for public use. <br>
Risk: The optional user-level background service can keep syncing and enriching data unattended. <br>
Mitigation: Enable the service only when unattended operation is intended, verify status with doctor and service-status commands, and use one-shot service runs when continuous sync is not needed. <br>
Risk: Issue reporting can publish operational details outside the workspace. <br>
Mitigation: Require explicit operator approval before opening or updating GitHub issues and scrub any reproduction details for public safety. <br>


## Reference(s): <br>
- [SherpaMind homepage](https://github.com/kklouzal/SherpaMind) <br>
- [SherpaDesk API documentation](https://github.com/sherpadesk/api/wiki) <br>
- [OpenClaw query model](references/openclaw-query-model.md) <br>
- [Retrieval architecture](references/retrieval-architecture.md) <br>
- [Bootstrap onboarding](references/bootstrap-onboarding.md) <br>
- [Automation](references/automation.md) <br>
- [API reference notes](references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, Analysis] <br>
**Output Format:** [Markdown with inline shell commands and concise analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on local SherpaDesk-derived SQLite data, generated Markdown artifacts, and retrieval indexes when configured.] <br>

## Skill Version(s): <br>
0.1.7 (source: ClawHub release metadata; pyproject.toml reports 0.1.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
