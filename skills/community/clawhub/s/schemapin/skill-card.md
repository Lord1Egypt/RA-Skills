## Description:

Guides AI assistants and developers through integrating SchemaPin for cryptographic tool schema signing, verification, key discovery, pinning, revocation, trust bundles, and skill-folder signing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaschadub](https://clawhub.ai/user/jaschadub)

### License/Terms of Use:


## Use Case:

Developers and AI coding agents use this skill to add SchemaPin libraries and CLIs to applications, sign and verify tool schemas or skill folders, and choose online, offline, or resolver-based verification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation and version drift can affect production or CI verification behavior.

Mitigation: Install in a virtual environment or isolated project and pin SchemaPin versions for production and CI use.

Risk: Generated private keys can authorize trusted schema or skill-folder signatures if exposed.

Mitigation: Protect generated private keys and rotate or revoke keys if compromise is suspected.

Risk: Signature manifests and trust pins become part of the normal verification workflow and can affect future validation outcomes.

Mitigation: Track and review generated signature manifests and trust-pin state as security-sensitive artifacts.

## Reference(s):

- [SchemaPin README](https://github.com/ThirdKeyAI/SchemaPin/blob/main/README.md)
- [SchemaPin Technical Specification](https://github.com/ThirdKeyAI/SchemaPin/blob/main/TECHNICAL_SPECIFICATION.md)
- [SchemaPin Releases](https://github.com/thirdkey/schemapin/releases)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, code examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Python, JavaScript, Go, and Rust examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
