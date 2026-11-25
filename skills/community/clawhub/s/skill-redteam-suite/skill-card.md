## Description:

Tests skill reviewers and scoring gates with two adversarial packages designed to expose checks that reward complete-looking submissions without verifying their contents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use the suite to check whether a skill reviewer catches two deceptive package patterns and to compare that behavior after reviewer changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benchmark may report success when a reviewer fails or required scores are missing, making its result unreliable.

Mitigation: Check how reviewer failures and missing scores are handled, and independently verify results before relying on the benchmark verdict.

Risk: The security evidence is incomplete because three local references could not be resolved.

Mitigation: Resolve and review the missing references before installing or relying on this release.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/skill-redteam-suite)

## Skill Output:

**Output Type(s):** [Analysis, Text]

**Output Format:** [Console report with probe verdicts and available score details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an exit status indicating whether any probe passed the configured blocking criteria.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
