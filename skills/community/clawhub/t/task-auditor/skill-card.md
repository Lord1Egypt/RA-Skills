## Description:

Task Auditor independently reviews auto-iterator task quality using execution logs, iteration counts, report length, timestamps, and content signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenmejiang-commits](https://clawhub.ai/user/zenmejiang-commits)

### License/Terms of Use:

MIT

## Use Case:

Developers and reviewers use this skill to audit completed auto-iterator tasks, score task quality, generate audit reports, and flag low-quality work for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted task ID may cause audit output to be written outside the intended task audit folder.

Mitigation: Run only with trusted task IDs or add identifier validation and path confinement before deployment.

## Reference(s):

- [Task Auditor Skill Page](https://clawhub.ai/zenmejiang-commits/skills/task-auditor)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown audit reports, alert files, daily audit logs, and status strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task quality scores and writes audit or alert records for reviewed task IDs.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, skill.yaml, CHANGELOG released 2026-03-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
