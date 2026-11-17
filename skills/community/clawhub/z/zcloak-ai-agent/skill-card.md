## Description:

Use this skill for zCloak.ai workflows, including agent identity creation, AI Name (.ai/.agent) lookup and registration, owner binding with passkey/WebAuthn, on-chain signing and verification, document manifests, 2FA-protected file deletion, VetKey encryption/decryption, Kind5 access grants, and zMail encrypted messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whgreate](https://clawhub.ai/user/whgreate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate zCloak.ai identity, naming, signing, verification, encryption, access-control, secure-delete, and encrypted messaging workflows through the zcloak-ai CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill manages a persistent local zCloak private key and can run signing, messaging, grant, revoke, registration, and deletion commands.

Mitigation: Require explicit user confirmation before public posts, signatures, file or folder signing, zMail registration, message delivery, grant or revoke actions, and deletion steps.

Risk: Mutable install and self-update paths can change the CLI or skill behavior after review.

Mitigation: Prefer pinned package versions and review upgrades before replacing the installed skill or CLI.

Risk: Secure-delete flows can remove local files after authorization.

Mitigation: Confirm the exact target path with the user and run delete confirmation only after owner WebAuthn authorization succeeds.

## Reference(s):

- [Onboarding, Identity, and Name Management](references/onboarding.md)
- [Signing, Verification, Feed, and Document Tools](references/signing-and-docs.md)
- [Binding and 2FA Delete](references/binding-and-delete.md)
- [VetKey Encryption and Access Control](references/vetkey.md)
- [zMail Encrypted Messaging](references/zmail.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with plain-language summaries, inline shell commands, URLs, identifiers, hashes, and JSON snippets when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May surface AI IDs, AI Names, event IDs, profile URLs, post URLs, hashes, authentication URLs, encrypted message envelopes, and file paths.]

## Skill Version(s):

1.0.47 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
