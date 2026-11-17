## Description:

Generates hardened pfSense firewall configurations based on specified security options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External network administrators, security engineers, DevSecOps teams, and MSSPs use this skill to request hardened pfSense firewall configuration objects from a hosted API for review and deployment planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated firewall configuration may be incomplete, unsuitable for the target environment, or disruptive if applied directly.

Mitigation: Review and test generated configuration in a non-production environment before deployment, and keep a backup and recovery path.

Risk: Requests to the hosted API may expose sensitive firewall details or operational context.

Mitigation: Do not send secrets or sensitive firewall information unless the provider is trusted and the data handling requirements are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-pfsense-hardening)
- [pfSense hardening API route](https://api.mkkpro.com/hardening/pfsense)
- [pfSense hardening API docs](https://api.mkkpro.com:8131/docs)
- [ToolWeb](https://toolweb.in)
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/)

## Skill Output:

**Output Type(s):** [API Calls, Configuration, JSON, Guidance]

**Output Format:** [JSON configuration objects and markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hosted API wrapper; generated firewall configurations should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
