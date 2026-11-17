## Description:

Provides a client and local engine for producing deterministic video from simulated world state, with frame hashes and a signed render manifest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nohn3043-arch](https://clawhub.ai/user/nohn3043-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the client to request renders from a compatible service or run the bundled engine locally, then inspect the resulting video and reproducibility artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A render service may overwrite local files, and the optional server may grant ordinary users administrative powers.

Mitigation: Use an isolated local demo until download containment and server authorization are fixed; keep the optional server private and avoid using its account system for real assets.

Risk: The client may hand a bill to an external payment capability, whose code and optional integrations are not verified by this evidence.

Mitigation: Review the payment dependency separately and require explicit control of payment approval.

Risk: A signature alone does not establish authorship or verify the rendered pixels.

Mitigation: Treat signatures as demonstration checks and use full pixel replay for verification.

## Reference(s):

- [API protocol](references/api.md)
- [Determinism and verification](references/determinism.md)
- [Shot-file format](references/shot-files.md)
- [ClawHub release page](https://clawhub.ai/nohn3043-arch/skills/second-reality-video)
- [Publisher profile](https://clawhub.ai/user/nohn3043-arch)

## Skill Output:

**Output Type(s):** [Video files, JSON and JSONL artifacts, Hashes, Text reports]

**Output Format:** [MP4 video, JSON/JSONL manifests and frame records, SHA-256 hashes, and text audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Frame hashes support pixel-level checks; MP4 container hashes are corroborative only.]

## Skill Version(s):

1.1.0 (source: artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
