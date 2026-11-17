## Description:

Generate, manage, and download SSL/TLS certificates with token-based verification and multi-domain support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps teams, security engineers, and automation platforms use Certificaty to automate SSL/TLS certificate ordering, domain verification, certificate generation, inventory review, and certificate or key downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes certificate inventory, domain, email, certificate issuance, and private-key download workflows.

Mitigation: Install only if the ToolWeb.in service is trusted for those assets and confirm authentication, authorization, tenant isolation, and proof-of-domain-control controls before using real domains.

Risk: Downloadable private keys can create high-impact exposure if key export is not tightly controlled.

Mitigation: Use tightly controlled private-key export and handling practices, and confirm audit logging is enabled for certificate and key operations.

## Reference(s):

- [Certificaty ClawHub Skill](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-certificaty)
- [Certificaty API Docs](https://api.toolweb.in:8164/docs)
- [Certificaty API Route](https://api.toolweb.in/tools/certificaty)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Files, Guidance]

**Output Format:** [JSON responses and downloadable certificate or key files, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes certificate metadata and PEM, CRT, or KEY file downloads when service endpoints are used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
