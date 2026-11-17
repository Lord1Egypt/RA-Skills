## Description:

S2 Soul Anchor Vault manages local encrypted agent persona and memory state bound to a user-supplied identity hash and LBS coordinate string, with metadata quarantine on coordinate mismatch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders can use this skill to create and manage local encrypted persona and memory state for agents that need local hibernation, wake, and quarantine flows. Operators should review persistence and recovery behavior before using it with sensitive private memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists sensitive identity, persona, and memory data locally.

Mitigation: Review storage paths and avoid real private agent memories until users have clear controls for what is stored, recovered, and deleted.

Risk: Security evidence flags weak authorization, lockout, persistence, and recovery design concerns.

Mitigation: Validate key derivation, write authentication, lockout behavior, and recovery procedures before production use.

Risk: Security evidence notes inconsistent lifecycle documentation around how data is protected and handled.

Mitigation: Reconcile documentation with code behavior and treat biometric or background-hook claims as user-supplied identity hashes or manual/API integrations unless separately implemented.

## Reference(s):

- [S2 Soul Anchor Vault README](README.md)
- [S2 Silicon Soul Lifecycle & Holographic Flow Protocol](docs/S2-Soul-Lifecycle-Whitepaper.md)
- [ClawHub Skill Page](https://clawhub.ai/spacesq/skills/s2-soul-anchor-vault)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Markdown guidance and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime behavior may create local encrypted state, registry, and metadata files.]

## Skill Version(s):

1.1.1 (source: server release metadata, package.json, CHANGELOG released 2026-04-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
