## Description:

Generates natural Chinese daily, weekly, monthly, and annual work reports from keywords or casual notes while reusing prior local reports for rollups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuwu2495](https://clawhub.ai/user/jiuwu2495)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and team contributors use this skill to turn terse work notes into readable Chinese work reports. It supports daily reports and rollups into weekly, monthly, and annual summaries using prior local reports when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads prior reports from .workbuddy/reports/ to build higher-level summaries, which can reuse sensitive business or personnel details stored there.

Mitigation: Review drafts before approving saves, and avoid storing highly sensitive details unless that reuse is intended.

Risk: Broad trigger wording can cause casual work notes to be treated as report input.

Mitigation: Confirm the inferred report type and generated content before approving any saved report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiuwu2495/skills/work-report-pro)
- [Publisher profile](https://clawhub.ai/user/jiuwu2495)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown work report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save approved reports under .workbuddy/reports/ for later daily, weekly, monthly, and annual rollups.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
