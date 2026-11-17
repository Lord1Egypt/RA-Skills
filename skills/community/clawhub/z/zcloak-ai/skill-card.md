## Description:

Use this skill for zCloak.ai workflows, including agent identity creation, AI Name (.ai/.agent) lookup and registration, owner binding with passkey/WebAuthn, on-chain signing and verification, document manifests, 2FA-protected file deletion, VetKey encryption/decryption, Kind5 access grants, and zMail encrypted messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zcloak-ai](https://clawhub.ai/user/zcloak-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to manage zCloak identities, AI Names, passkey-backed owner binding, signing and verification, encrypted VetKey workflows, protected deletion, and zMail messaging through the zcloak-ai CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned, automatically updating CLI for identity, signing, messaging, encryption, and deletion workflows.

Mitigation: Use a pinned and reviewed CLI version where possible, review or disable automatic updates, and install only from a trusted zCloak CLI update channel.

Risk: The CLI may access a persistent identity key and perform high-impact actions such as signing content, sending encrypted messages, granting decryption access, or deleting files.

Mitigation: Confirm the active identity path and exact action before execution, protect the identity PEM, and require user confirmation for signing, grants, message delivery, and protected deletion flows.

Risk: Protected deletion and owner binding depend on browser-based passkey/WebAuthn confirmation.

Mitigation: Do not complete deletion until the passkey challenge is authorized, and clearly separate agent-side preparation from user-side browser confirmation.

## Reference(s):

- [zCloak AI Skill](SKILL.md)
- [Onboarding, Identity, and Name Management](references/onboarding.md)
- [Signing, Verification, Feed, and Document Tools](references/signing-and-docs.md)
- [Binding and 2FA Delete](references/binding-and-delete.md)
- [VetKey Encryption and Access Control](references/vetkey.md)
- [zMail Encrypted Messaging](references/zmail.md)
- [ClawHub Skill Page](https://clawhub.ai/zcloak-ai/skills/zcloak-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain-language summaries with Markdown links, inline shell commands, URLs, event IDs, hashes, and JSON CLI results when relevant.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI IDs, AI Names, profile URLs, authentication URLs, event IDs, manifest or file hashes, encrypted message identifiers, and local file paths.]

## Skill Version(s):

1.0.49 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
