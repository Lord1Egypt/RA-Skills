## Description:

Professional FortiGate security configuration generator based on CIS Benchmark standards for enterprise firewall hardening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams, network architects, managed security service providers, infrastructure-as-code practitioners, and compliance professionals use this skill to generate standardized FortiGate firewall hardening configurations aligned with CIS Benchmark-style controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated firewall configuration changes may be incorrect, incomplete, or unsuitable for a specific FortiGate deployment.

Mitigation: Review generated diffs, test changes outside production, and maintain rollback and out-of-band management access before applying them.

Risk: Hardening options and request metadata are sent to a third-party API.

Mitigation: Use the skill only when that data sharing is acceptable and avoid sending unnecessary real user identifiers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-fortigate-hardening)
- [FortiGate Hardening API Docs](https://api.mkkpro.com:8135/docs)
- [FortiGate Hardening API Route](https://api.mkkpro.com/hardening/fortigate)
- [ToolWeb](https://toolweb.in)

## Skill Output:

**Output Type(s):** [configuration, guidance]

**Output Format:** [JSON API responses containing hardening options, generated FortiGate configuration objects, and download URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The API accepts hardening options plus request metadata such as session ID, optional user ID, and timestamp.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
