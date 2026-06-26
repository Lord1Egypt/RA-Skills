## Description: <br>
SchemaPin guides agents and developers through cryptographic signing and verification of tool schemas and skill folders using ECDSA P-256, SHA-256, TOFU key pinning, and well-known key discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaschadub](https://clawhub.ai/user/jaschadub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to add schema and skill-folder integrity checks to agent tooling across Python, JavaScript, Go, and Rust. It is most useful when integrating signature generation, verification, key discovery, revocation checks, trust bundles, and TOFU pinning into deployment or registry workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TOFU pinning trusts the first accepted key for a domain, so accepting the wrong initial key can preserve a compromised trust state. <br>
Mitigation: Confirm the package source, publisher, and expected domain before first pinning, and use verified trust bundles or pre-fetched discovery data where practical. <br>
Risk: Following the examples may install packages or fetch public keys from external registries and endpoints. <br>
Mitigation: Pin dependency versions where practical and verify the SchemaPin packages and GitHub project match the publisher the user intends to trust. <br>


## Reference(s): <br>
- [ClawHub SchemaPin listing](https://clawhub.ai/jaschadub/schemapin) <br>
- [SchemaPin README](https://github.com/ThirdKeyAI/SchemaPin/blob/main/README.md) <br>
- [SchemaPin Technical Specification](https://github.com/ThirdKeyAI/SchemaPin/blob/main/TECHNICAL_SPECIFICATION.md) <br>
- [SchemaPin releases](https://github.com/thirdkey/schemapin/releases) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides language-specific examples and implementation guidance; does not execute package installs itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
