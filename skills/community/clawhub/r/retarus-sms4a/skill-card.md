## Description:

Send SMS jobs and check SMS delivery status through the Retarus SMS for Applications REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeggerd](https://clawhub.ai/user/aeggerd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create or validate Retarus SMS4A job payloads, send SMS messages, and retrieve per-recipient delivery status for Retarus job IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retarus account credentials may be exposed if operators pass passwords directly on the command line or store secret files without protection.

Mitigation: Prefer secret-store backed environment injection or a protected secret file, and avoid command-line passwords except for local testing.

Risk: Agents with this skill can send SMS messages and read delivery reports through the configured Retarus account, which may create billing or permissions exposure.

Mitigation: Install only for agents that need SMS access, use account permissions aligned with authorized users, apply billing limits, and run dry-run checks before sending.

Risk: Status lookups can miss delivery reports if they rely only on the DNS-balanced eu endpoint.

Mitigation: Use the documented status workflow that queries both de2 and de1, with the preferred datacenter only controlling the first lookup target.

## Reference(s):

- [Retarus SMS4A Reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit dry-run request plans, job IDs, datacenter attempts, recipient reports, API responses, and structured error details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
