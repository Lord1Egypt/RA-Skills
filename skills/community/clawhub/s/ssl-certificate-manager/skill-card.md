## Description:

Automate SSL certificate generation and management with DNS challenge validation and certificate provisioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security professionals, DevOps teams, and developers use this skill to create DNS challenges, request SSL/TLS certificate issuance, download certificate files, and debug DNS validation for managed domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Certificate issuance and download workflows can affect production TLS assets and may expose private key material.

Mitigation: Use the external certificate service only when trusted, verify per-domain authorization before issuance, restrict downloads to required files, and never log, share, or commit private.key content.

Risk: The published OpenAPI contract does not document access controls or private-key handling requirements.

Mitigation: Require human review of authentication, authorization, and key custody controls before allowing autonomous agents to issue or download certificates.

Risk: Incorrect DNS challenge configuration can cause failed issuance or operational delays.

Mitigation: Use the staging option and DNS debug endpoint before production issuance when validating new domains or automation changes.

## Reference(s):

- [SSL Certificate Manager API Route](https://api.mkkpro.com/security/ssl-certificate-manager)
- [SSL Certificate Manager API Docs](https://api.mkkpro.com:8044/docs)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return certificate file contents from download endpoints; private.key output must be treated as secret material.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
