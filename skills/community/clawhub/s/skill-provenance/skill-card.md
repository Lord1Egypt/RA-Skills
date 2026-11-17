## Description:

Version, validate, package, verify, recover, and hand off Agent Skill bundles across local folders, registries, platform uploads, and agent sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snapsynapse](https://clawhub.ai/user/snapsynapse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to preserve version identity, integrity, changelogs, bundle hashes, and deployment handoffs for multi-file Agent Skill bundles as they move across local folders, registries, uploads, and agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The no-plugin verification path asks users to download and run a shell wrapper from a mutable external URL.

Mitigation: Inspect the wrapper and verify it through a trusted checksum or signature before execution, or prefer reviewed local tooling or a pinned package source.

Risk: The skill can modify manifests, changelogs, hashes, validation records, and derived packages in directories selected by the user.

Mitigation: Review proposed diffs and validation output before publishing, installing, replacing source material, committing, or deploying generated artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snapsynapse/skills/skill-provenance)
- [Skill Provenance README](README.md)
- [Packaging and changelog reference](references/packaging-and-changelog.md)
- [Platform, ecosystem, and trust reference](references/platforms-and-trust.md)
- [Standalone verification and bootstrap reference](references/standalone-verification.md)
- [Public pre-install assistant guide](https://skillprovenance.dev/.well-known/assistant-guide.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured manifest or changelog snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or edit skill manifests, changelogs, bundle hashes, validation records, and derived package metadata in user-selected directories.]

## Skill Version(s):

6.3.0 (source: ClawHub release evidence and MANIFEST.yaml bundle_version, released 2026-09-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
