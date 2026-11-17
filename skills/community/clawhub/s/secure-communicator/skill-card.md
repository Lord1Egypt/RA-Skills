## Description:

Encrypts and decrypts text or files with the Pieter Theijssen triple-layer XOR cipher and V1 Base64 output format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theijssenp](https://clawhub.ai/user/theijssenp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to generate key files and run text or file encryption and decryption compatible with the Theijssen cipher workflow. Review is required before using it for sensitive secrets because the security evidence flags the custom cipher claims as overstated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The custom triple-layer XOR cipher may not provide the protection implied by the skill's sensitive-communication claims.

Mitigation: Do not rely on this skill for high-value secrets; prefer a standard authenticated-encryption tool for sensitive communications.

Risk: Plaintext passed with the --text option can be captured in shell history or process metadata.

Mitigation: Avoid command-line plaintext for sensitive data; use safer input handling or clear shell history according to local policy.

Risk: The --output option writes to the requested path and may overwrite an existing file.

Mitigation: Choose output paths deliberately and check for existing files before running encryption, decryption, or key generation commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/theijssenp/skills/secure-communicator)
- [Theijssen encode_decode compatibility reference](https://github.com/theijssenp/encode_decode)
- [Theijssen message_coder_decoder compatibility reference](https://github.com/theijssenp/message_coder_decoder)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Guidance]

**Output Format:** [Plain text, file output, and Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and openssl binaries according to ClawHub metadata.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
