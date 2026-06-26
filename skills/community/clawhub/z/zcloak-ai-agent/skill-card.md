## Description: <br>
Use this skill for zCloak.ai workflows, including agent identity creation, AI Name (.ai/.agent) lookup and registration, owner binding with passkey/WebAuthn, on-chain signing and verification, document manifests, 2FA-protected file deletion, VetKey encryption/decryption, Kind5 access grants, and zMail encrypted messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whgreate](https://clawhub.ai/user/whgreate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent operate zCloak.ai identity, naming, signing, verification, encrypted messaging, VetKey access-control, and passkey-protected deletion workflows through the zcloak-ai CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and reuse a persistent identity key. <br>
Mitigation: Confirm the identity path and intended owner before key creation or reuse, and explain where local identity and mailbox data may be stored. <br>
Risk: The skill can publish signed or public records and perform on-chain actions. <br>
Mitigation: Require explicit user approval before registration, signing, posting, following, replying, liking, or any on-chain action. <br>
Risk: Encrypted message decryption can expose private content or write decrypted data locally. <br>
Mitigation: Require explicit user approval before message decryption output, and clearly report any output file path. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/whgreate/zcloak-ai-agent) <br>
- [Onboarding, Identity, and Name Management](references/onboarding.md) <br>
- [Signing, Verification, Feed, and Document Tools](references/signing-and-docs.md) <br>
- [Binding and 2FA Delete](references/binding-and-delete.md) <br>
- [VetKey Encryption and Access Control](references/vetkey.md) <br>
- [zMail Encrypted Messaging](references/zmail.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with plain-language summaries and inline command/output references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include AI IDs, AI Names, profile URLs, event IDs, hashes, authentication URLs, JSON command results, and file paths when relevant.] <br>

## Skill Version(s): <br>
1.0.47 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
