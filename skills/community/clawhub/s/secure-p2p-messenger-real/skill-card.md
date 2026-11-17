## Description:

Provides local shell commands for identity setup, contact management, and encrypted message exchange using OpenSSL-based key and message handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[puppetcat-fire](https://clawhub.ai/user/puppetcat-fire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators can use this skill to generate a local identity, manage contacts, and create or read encrypted message packages. It should be treated as experimental local tooling for non-sensitive workflows unless its security issues are resolved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release overstates important security guarantees and may mislead users about encryption, authentication, metadata protection, and key safety.

Mitigation: Treat it as experimental local tooling and do not use it for confidential material, credentials, legal documents, or agent-to-agent trust decisions until the documented security issues are corrected.

Risk: The security evidence says sender signatures, metadata authentication, contact ID validation, private-key storage, and documentation accuracy need correction before relying on it as a secure messenger.

Mitigation: Require security review and fixes for those areas before deployment in workflows that depend on message authenticity, privacy, or key safety.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/puppetcat-fire/skills/secure-p2p-messenger-real)
- [Publisher profile](https://clawhub.ai/user/puppetcat-fire)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell command guidance with JSON message packages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local files under the user's OpenClaw secure-p2p directory and requires bash, openssl, jq, and base64.]

## Skill Version(s):

1.0.14 (source: server release evidence, SKILL.md frontmatter, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
