## Description:

AI-powered cloud service mapping and provider recommendation across Azure, AWS, and Google Cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud architects, DevOps teams, and organizations use this skill to analyze workload requirements and compare service recommendations across AWS, Azure, and Google Cloud for migration or multi-cloud planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workload descriptions and metadata fields can expose sensitive architecture, business, customer, credential, or tracking details to an external API.

Mitigation: Review the provider's privacy and retention terms before use, and avoid sending secrets, internal hostnames, customer data, credentials, or highly confidential architecture details.

Risk: Cloud provider recommendations may be incomplete or misaligned with organization-specific constraints, compliance needs, or current pricing.

Mitigation: Treat recommendations as decision support and validate them with cloud architects, security reviewers, and current provider documentation before migration or procurement decisions.

## Reference(s):

- [OpenAPI specification](artifact/openapi.json)
- [API Docs](https://api.toolweb.in:8171/docs)
- [Kong Route](https://api.toolweb.in/security/servicemapper)
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-cloud-service-mapper-decision-advisor)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [Markdown with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workload summaries, cloud service recommendations, confidence scores, decision factors, and migration insights.]

## Skill Version(s):

1.0.0 (source: server release evidence and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
