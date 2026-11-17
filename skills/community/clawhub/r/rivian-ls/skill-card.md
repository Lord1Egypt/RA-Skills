## Description:

Access Rivian vehicle telemetry, including battery, range, charge state, locks, doors, tires, cabin temperature, and location, using the rivian-ls CLI tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfrederiksen](https://clawhub.ai/user/pfrederiksen)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and automation builders use this skill to retrieve Rivian vehicle status, security, charging, tire, location, and dashboard data through an authenticated rivian-ls CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unofficial Rivian API and a third-party CLI that may break or change without notice.

Mitigation: Pin and verify the CLI release, test after Rivian or rivian-ls changes, and handle API failures gracefully.

Risk: Authentication and the credential cache can provide access to sensitive vehicle telemetry, including location.

Mitigation: Avoid passwords and OTPs in shell history or long-lived environment variables, restrict credential-cache permissions, and remove credentials when no longer needed.

Risk: Dashboard, cron, or JSON outputs can expose vehicle status and location.

Mitigation: Restrict access to generated endpoints and logs, and avoid publishing telemetry outputs.

## Reference(s):

- [Rivian Ls ClawHub skill page](https://clawhub.ai/pfrederiksen/skills/rivian-ls)
- [rivian-ls CLI upstream project](https://github.com/pfrederiksen/rivian-ls)
- [rivian-ls JSON Field Reference](references/api-fields.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON or text command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an installed and authenticated rivian-ls CLI; the bundled script can emit text or JSON telemetry summaries.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
