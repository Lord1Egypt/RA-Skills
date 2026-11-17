## Description:

Generates CIS v1.8.0 compliant Azure Kubernetes Service (AKS) configurations for security hardening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevSecOps engineers, cloud architects, and security teams use this skill to generate CIS v1.8.0-aligned AKS hardening configurations, compliance scores, warnings, and recommendations from selected hardening options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends AKS hardening requests to a third-party API.

Mitigation: Send only the hardening options needed for generation and avoid real personal identifiers unless required.

Risk: Generated hardening guidance may be used in production or regulated environments.

Mitigation: Review the provider's trust, pricing, and data-handling practices before production use.

## Reference(s):

- [API Docs](https://api.mkkpro.com:8149/docs)
- [Kong Route](https://api.mkkpro.com/hardening/azure-aks)
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-azure-aks-hardening)

## Skill Output:

**Output Type(s):** [configuration, guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes generated AKS hardening settings, compliance score, warnings, recommendations, CIS version, and generation timestamp.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
