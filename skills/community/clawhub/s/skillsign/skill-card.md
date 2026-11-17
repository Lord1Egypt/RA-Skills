## Description:

Sign and verify agent skill folders with ed25519 keys, detect tampering, manage trusted authors, track provenance chains, and revoke signing keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felmonon](https://clawhub.ai/user/felmonon)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to create local signing keys, sign skill folders, verify whether files changed after signing, manage trusted public keys, inspect signatures, and review signing chains before running or publishing skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification can wrongly mark attacker-controlled signatures or provenance as trusted.

Mitigation: Treat verification results as an experimental local integrity signal; derive signer fingerprints from verified public keys and compare trust against actual public keys before using it to approve skills.

Risk: Provenance chain entries may not be cryptographically authenticated enough to serve as a trusted-author gate.

Mitigation: Use provenance chains as informational context unless each chain entry is cryptographically authenticated by a verified key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/felmonon/skills/skillsign)
- [Publisher profile](https://clawhub.ai/user/felmonon)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with command-line output and generated local key, signature, manifest, trust, chain, and revocation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local filesystem artifacts under .skillsig/ and ~/.skillsign/ when commands are run.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
