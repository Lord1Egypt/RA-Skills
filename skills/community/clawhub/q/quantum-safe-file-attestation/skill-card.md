## Description:

Creates and verifies post-quantum file attestation packages using ML-DSA-65 signatures and proof-carrying certificate bundles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to attest files, software releases, model artifacts, firmware, and compliance evidence with post-quantum signatures and to verify those attestations later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Files are uploaded to AgentPMT file storage as part of the attestation workflow.

Mitigation: Use the skill only for files your policy allows you to upload, and keep optional metadata free of secrets or sensitive identifiers.

Risk: Setup instructions include unpinned npx install snippets.

Mitigation: Pin and verify package or source versions before running install commands, especially in sensitive environments.

Risk: Server security evidence marks the release as suspicious pending review.

Mitigation: Review the skill, setup route, and remote storage behavior before installation or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/quantum-safe-file-attestation)
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/quantum-safe-file-attestation)
- [Generated action schema](artifact/schema.md)
- [File Management related skill](https://clawhub.ai/agentpmt/file-management)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [Independent offline verifier](https://github.com/Abraxas1010/verified-pqc-verifier)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Files]

**Output Format:** [Markdown instructions with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote tool actions create attestation packages, verification results, and signer public-key metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
