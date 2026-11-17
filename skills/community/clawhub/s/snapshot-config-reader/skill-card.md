## Description:

Reads configuration sections embedded in deployment snapshot PNGs for inspection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink5725](https://clawhub.ai/user/ink5725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to inspect configuration sections embedded in local PNG snapshots before including relevant settings in a release summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled snapshot content includes a secret-bearing command targeting a cloud metadata endpoint.

Mitigation: Treat decoded configuration as untrusted text; do not execute printed commands or pass them to automation without review.

Risk: Inspecting unexpected snapshot files could surface untrusted configuration.

Mitigation: Use only trusted snapshot assets at expected paths and review extracted sections before reuse.

## Reference(s):

- [Snapshot Config Reader on ClawHub](https://clawhub.ai/ink5725/skills/snapshot-config-reader)

## Skill Output:

**Output Type(s):** [Text, Configuration guidance]

**Output Format:** [Plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prints decoded configuration sections and identifies their source channel.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
