## Description:

Verify regular or extended-stable OpenClaw releases against the exact publication surfaces, workflow identities, package provenance, smoke tests, and live Gateway behavior expected for that release track.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw developers and release maintainers use this skill to determine whether a regular or extended-stable release has been published and verified across the surfaces required for its track. It summarizes evidence, smoke-test results, caveats, and cleanup in a concise release report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags possible changes to live release distribution during verification as potentially beyond the stated purpose; its assessment has medium confidence and partial coverage.

Mitigation: Review any release-distribution action before execution and consider whether the skill is trusted when publishing credentials are available.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/hillstreet-ph/skills/verify-release)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Markdown release verification summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Organizes findings by release track and publication evidence, with yes/no status, caveats, and cleanup notes; does not print secrets.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
