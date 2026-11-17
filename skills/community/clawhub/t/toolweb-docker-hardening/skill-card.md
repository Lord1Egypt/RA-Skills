## Description:

Professional Docker security configuration generator aligned with CIS Benchmark v1.8.0 standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, security teams, and infrastructure architects use this skill to request Docker hardening options and generate hardened Dockerfiles, Docker Compose manifests, security policy documents, compliance scores, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests are sent to an external provider API and may include Docker hardening choices plus session metadata.

Mitigation: Use only when comfortable sharing those request details with the provider, and avoid sending secrets, private hostnames, internal topology, or account identifiers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-docker-hardening)
- [OpenAPI Specification](artifact/openapi.json)
- [Docker Hardening API Docs](https://api.mkkpro.com:8136/docs)
- [Docker Hardening API Route](https://api.mkkpro.com/hardening/docker)
- [ToolWeb](https://toolweb.in)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JSON responses containing generated file contents, applied policy lists, compliance scores, timestamps, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API-backed output may include Dockerfile, docker-compose, and security policy content.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
