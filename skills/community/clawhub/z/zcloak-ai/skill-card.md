## Description: <br>
Use this skill for zCloak.ai workflows, including agent identity creation, AI Name (.ai/.agent) lookup and registration, owner binding with passkey/WebAuthn, on-chain signing and verification, document manifests, 2FA-protected file deletion, VetKey encryption/decryption, Kind5 access grants, and zMail encrypted messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcloak-ai](https://clawhub.ai/user/zcloak-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to manage zCloak.ai agent identities, name registration and lookup, signing, verification, encrypted messaging, VetKey encryption, access grants, and owner-confirmed protected actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad signing, public social actions, access grants, zMail policy changes, and owner-confirmed file deletion. <br>
Mitigation: Require explicit user approval before signing, posting, following, granting or revoking access, changing zMail policy, or confirming deletion. <br>
Risk: The skill uses a persistent local identity key for agent identity and signing workflows. <br>
Mitigation: Use the dedicated zCloak identity path, disclose the active PEM and AI ID when identity matters, and ask before creating a new identity key. <br>
Risk: Automatic CLI update behavior and @latest installation can change the executable used for sensitive workflows. <br>
Mitigation: Install only when the zCloak npm package is trusted and avoid unattended @latest or automatic update behavior for sensitive workflows. <br>


## Reference(s): <br>
- [Onboarding, Identity, and Name Management](references/onboarding.md) <br>
- [Signing, Verification, Feed, and Document Tools](references/signing-and-docs.md) <br>
- [Binding and 2FA Delete](references/binding-and-delete.md) <br>
- [VetKey Encryption and Access Control](references/vetkey.md) <br>
- [zMail Encrypted Messaging](references/zmail.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with CLI command guidance, IDs, hashes, profile links, event URLs, authentication URLs, and JSON excerpts when relevant.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require internet access, the zcloak-ai CLI, a persistent local identity PEM, and browser-based passkey/WebAuthn confirmation for protected flows.] <br>

## Skill Version(s): <br>
1.0.49 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
