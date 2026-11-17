## Description:

Convert a syllabus, exam scope, or course notes into a revision calendar with spaced review, mock tests, and weak-point loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Students, educators, and learning-support agents use this skill to convert syllabus or exam-scope material into actionable revision plans, topic effort tables, mock test schedules, and next-step checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled helper script creates only a basic topic/date CSV and does not implement the full spaced-review or mock-test workflow described by the skill.

Mitigation: Review generated plans and treat script output as a first-pass draft before relying on it for study scheduling.

Risk: Study materials can contain sensitive personal or academic information.

Mitigation: Use explicit input files and avoid pointing the helper script at sensitive files unless needed for the planning task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/study-revision-planner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional CSV files and local Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a local python3 helper script to create a basic topic/date CSV; generated plans should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
