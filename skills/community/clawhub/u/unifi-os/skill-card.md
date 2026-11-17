## Description:

Read-only access to UniFi Network data for device inventory, network configuration, client information, alerts, health status, firmware status, and topology export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbojer](https://clawhub.ai/user/mbojer)

### License/Terms of Use:

MIT-0

## Use Case:

Network administrators and operations engineers use this skill to inspect UniFi Network sites, troubleshoot client and device issues, review alerts and health, and generate topology documentation without making configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local cache and topology exports can store sensitive UniFi network data such as clients, topology, alerts, IP addresses, MAC addresses, and network configuration.

Mitigation: Install only on trusted administrator machines, protect ~/.clawdbot/cache/unifi, periodically clear cached data when no longer needed, and restrict generated topology documents to trusted recipients.

Risk: UniFi API credentials can expose administrative network data if the key or configuration file is mishandled.

Mitigation: Use a narrowly scoped read-only UniFi API key, configure only an HTTPS UniFi URL, store credentials with restrictive file permissions, and rotate the key if exposure is suspected.

Risk: Raw output and client-history lookups may reveal more network detail than needed for a troubleshooting task.

Mitigation: Prefer the default stripped output, use --json or --raw only when specific fields are required, and avoid sharing client-history or raw API records outside trusted operations workflows.

## Reference(s):

- [UniFi API Endpoint Reference](references/endpoints.md)
- [ClawHub skill page](https://clawhub.ai/mbojer/skills/unifi-os)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands; script outputs are text, JSON, or topology Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only UniFi API calls and local caching; raw outputs, topology exports, and client history can contain sensitive network records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
