## Description:

Read-only code review covering architecture, defects, security, dependencies, and licenses, with findings combined into a review report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengfr](https://clawhub.ai/user/zengfr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review a codebase for architecture issues, defects, security concerns, dependency risks, and license concerns, then combine the findings into a review report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with medium confidence, citing review instructions that reportedly conflict with read-only assurances.

Mitigation: Review the referenced workflow and confirm its write boundaries before use.

Risk: The security guidance reports repeated package commands that may fetch unpinned code; the scan was partial because referenced files were missing.

Mitigation: Review the missing workflow files and package commands before installation or execution; the scan does not confirm their behavior.

## Reference(s):

- [Source repository](https://github.com/zengfr/AutoCoding/tree/main/docs/generated-skills/ultravibe-review)
- [ClawHub skill release](https://clawhub.ai/zengfr/skills/ultravibe-review)

## Skill Output:

**Output Type(s):** [Analysis, JSON]

**Output Format:** [JSON phase reports and an aggregated code review report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Phase reports cover architecture, defects, security, and dependencies; the final report combines review findings.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
