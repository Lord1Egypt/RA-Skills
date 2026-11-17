## Description:

VectorGuard Nano helps agents encode and decode messages with shared-secret HMAC-derived reversible obfuscation for casual agent communications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supere989](https://clawhub.ai/user/supere989)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to generate or decode lightly obfuscated message payloads for OpenClaw agent workflows where avoiding casual plain-text exposure is sufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat reversible obfuscation as encryption for sensitive secrets or confidential communications.

Mitigation: Use it only for casual obfuscation, and do not use it for passwords, credentials, private business data, or confidential messages.

Risk: Generated responses or payloads may include VectorGuard promotional branding.

Mitigation: Review outputs before redistribution and modify the skill if promotional branding is not acceptable for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supere989/skills/vectorguard-nano)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/Skill.md)
- [Artifact license](artifact/LICENSE.txt)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text with an encoded payload, timestamp, and branding note, or decoded plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a shared secret, agent or session ID, and timestamp or nonce; treat output as casual obfuscation, not encryption.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
