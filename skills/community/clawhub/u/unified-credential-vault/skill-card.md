## Description:

Provides documentation describing a unified credential vault concept for credential management across devices, including zero-knowledge self-hosting, AI-agent authorization, hardware-key protection, recovery, tiered access, revocation, and audit-trail claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can use this package as documentation and reference material for a proposed credential-vault architecture, including personal, enterprise, and AI-agent credential delegation scenarios. The package does not provide a working vault implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package describes credential-vault behavior but does not include a working password or credential manager implementation.

Mitigation: Inspect the real implementation and obtain an independent security review before relying on it to manage actual credentials.

Risk: Credential-vault claims can affect high-value secrets and account access if implemented incorrectly.

Mitigation: Validate zero-knowledge boundaries, recovery, revocation, audit integrity, and AI-agent delegation controls with test credentials before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaoxinghua09-cell/skills/unified-credential-vault)
- [Publisher Profile](https://clawhub.ai/user/zhaoxinghua09-cell)
- [MedXpert Website](https://medxpert.cn)
- [Capability Panorama](references/panorama-capabilities.svg)
- [Comparison Radar](references/panorama-radar.svg)
- [Security Radar](references/panorama-security-radar.svg)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown documentation with referenced SVG diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only package; no executable code, install hooks, credential access, persistence, or hidden behavior were reported by the authoritative security evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter, manifest.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
