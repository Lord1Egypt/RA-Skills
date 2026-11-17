## Description:

Helps agents route complex tasks through a Three Departments and Six Ministries multi-agent workflow for planning, review, dispatch, execution, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[743834110](https://clawhub.ai/user/743834110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when a non-trivial task benefits from explicit task triage, planning, independent review, coordinated execution, and a concise final report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can create local session notes in the current project.

Mitigation: Confirm the intended working directory and session path before execution.

Risk: The workflow may coordinate multiple sub-agent tasks for larger work.

Mitigation: Confirm task scope and review the plan before allowing execution.

Risk: The artifact text uses both court-session and .court-session naming.

Mitigation: Clarify the expected session directory name before relying on generated records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/743834110/skills/san-sheng-liu-bu)
- [ClawHub publisher profile](https://clawhub.ai/user/743834110)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with task plans, review notes, execution summaries, and local session files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local workflow records under a court session directory during task execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
