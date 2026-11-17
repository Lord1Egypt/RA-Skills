## Description:

VitaVault iOS app integration - sync Apple Health data directly to your AI agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandons7](https://clawhub.ai/user/brandons7)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users and developers use this skill to connect VitaVault iOS Apple Health exports or sync snapshots to an OpenClaw agent, then query, summarize, and prepare health briefings from locally stored data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health data could be exposed if the webhook is published publicly or run without strong authentication.

Mitigation: Require a strong bearer token, bind to localhost by default, expose only through trusted HTTPS infrastructure, and avoid automatic public publishing.

Risk: Persistent host changes can make the webhook survive reboots and keep receiving health data longer than intended.

Mitigation: Require explicit user approval before installing a service, document how to stop and remove it, and set private file permissions for stored snapshots.

Risk: Stored Apple Health snapshots may accumulate sensitive records on disk.

Mitigation: Use retention and deletion controls, validate dates and request sizes, and keep the data directory access restricted.

Risk: Cloud API querying can send credentials or health data to infrastructure outside the local machine.

Mitigation: Use only trusted private API endpoints and keep cloud API credentials separate from the webhook sync token.

## Reference(s):

- [VitaVault Data Types](references/data-types.md)
- [VitaVault Export Schema](references/schema.md)
- [VitaVault Website](https://vitavault.io)
- [VitaVault Developers](https://vitavault.io/developers/)
- [ClawHub Skill Page](https://clawhub.ai/brandons7/skills/vitavault)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands, plain-text summaries, and JSON health data outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read local health-data JSON files under the user's home directory when the included scripts are run.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
