## Description:

Cryptographically sign and verify AgentSkill directories with Ed25519 so recipients can verify integrity and authorship with a trusted public key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to create Ed25519 signing keys, sign AgentSkill directories, and verify whether a signed skill remains unchanged and matches a trusted public key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The verifier can read outside the target skill through symlinks.

Mitigation: Use the skill only on trusted or pre-inspected skill directories, and avoid verifying packages that contain symlinks.

Risk: A passing signature may exclude dependency or virtualenv content.

Mitigation: Do not treat signature verification as proof that excluded runtime content is unchanged; inspect or pin excluded dependencies separately.

Risk: Self-verification proves integrity against the embedded key but not author identity.

Mitigation: Use trust verification with a public key obtained through a known-good channel before relying on authorship claims.

## Reference(s):

- [Skill Sign on ClawHub](https://clawhub.ai/songhonglei/skills/skill-sign)
- [RFC 8032: Edwards-Curve Digital Signature Algorithm](https://www.rfc-editor.org/rfc/rfc8032.txt)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, JSON]

**Output Format:** [Command-line text plus generated key files and sign.key JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python scripts and writes signing material under the user's skill-sign configuration directory.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md Version field)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
