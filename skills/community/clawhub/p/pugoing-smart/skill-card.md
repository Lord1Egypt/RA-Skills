## Description:

Provides common Pugoing central-control platform API calls for querying areas, hosts, and devices, and for controlling devices with natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[run02](https://clawhub.ai/user/run02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call common Pugoing smart-control APIs for area, host, and device discovery and natural-language device control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes an authenticated HTTP client that can leak the Pugoing API key if directed to untrusted destinations.

Mitigation: Use a tightly scoped Pugoing API key, avoid supplying full URLs or custom destinations, and prefer HTTPS except for trusted local loopback testing.

Risk: Natural-language control calls can affect physical devices.

Mitigation: Require explicit user confirmation before commands that change device state.

## Reference(s):

- [Pugoing Smart ClawHub release page](https://clawhub.ai/run02/skills/pugoing-smart)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API Calls, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PUGOING_API_KEY and optional PUGOING_BASE_URL and PUGOING_TIMEOUT environment variables.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
