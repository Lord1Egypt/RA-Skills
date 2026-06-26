## Description: <br>
Key lifecycle management with Volcengine KMS. Use when users need key creation, rotation policies, encryption/decryption workflows, or key permission troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to plan and execute Volcengine KMS key lifecycle, cryptographic operation, rotation, and permission troubleshooting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: KMS operations can create, rotate, decrypt with, sign with, or change access to sensitive keys. <br>
Mitigation: Use least-privilege IAM credentials limited to intended projects and keys, and require explicit confirmation before creating keys, decrypting data, signing, rotating keys, or changing key policies. <br>
Risk: Plaintext secrets or cryptographic material could be exposed in logs or responses during key workflows. <br>
Mitigation: Do not expose plaintext secrets in logs, and return only the minimum operation result, key metadata, and audit hints needed for the task. <br>


## Reference(s): <br>
- [sources.md](references/sources.md) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/volcengine-security-kms) <br>
- [Publisher profile](https://clawhub.ai/user/cinience) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include key metadata, operation results, audit hints, and least-privilege permission checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
