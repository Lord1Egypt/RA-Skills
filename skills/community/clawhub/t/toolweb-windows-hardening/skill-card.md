## Description:

Professional Windows Security Configuration Generator for automated hardening policy creation and deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams, system administrators, compliance professionals, and developers use this skill to generate Windows security hardening configurations from selected policy options and retrieve available hardening categories for planning or automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated hardening files and request metadata are sent to a third-party API.

Mitigation: Avoid sensitive internal identifiers unless necessary and review the provider's privacy and retention terms before use.

Risk: Generated Windows hardening policies may affect production or remotely managed systems.

Mitigation: Review and test generated policies in a staging environment before applying them to production systems.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-windows-hardening)
- [API Docs](https://api.mkkpro.com:8125/docs)
- [Kong Route](https://api.mkkpro.com/hardening/windows)
- [ToolWeb](https://toolweb.in)

## Skill Output:

**Output Type(s):** [API Calls, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated hardening configurations may include download URLs and request metadata from a third-party API.]

## Skill Version(s):

1.0.0 (source: release evidence and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
