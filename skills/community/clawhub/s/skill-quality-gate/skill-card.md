## Description:

This CLI checks nine skill-quality dimensions and reports per-dimension pass/fail results for review before marketplace submission or release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers preparing a skill, prompt, or agent configuration for marketplace submission or release can run the checker to review nine quality dimensions and its pass/fail report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker can return success even when one or more checks fail, so its overall status may not reliably block publication.

Mitigation: Treat it as an advisory checklist until failed checks reliably return a failing exit status; review the printed results before publishing.

Risk: File access does not enforce the promised boundary around the selected directory.

Mitigation: Use a dedicated secret scanner and review the selected target and its files before relying on the results.

## Reference(s):

- [Project Homepage](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [ClawHub Release Page](https://clawhub.ai/zhaoxinghua09-cell/skills/skill-quality-gate)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain-text report with per-dimension pass/fail results and an overall status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Printed to the current session; no output file is produced by default.]

## Skill Version(s):

1.0.10 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
