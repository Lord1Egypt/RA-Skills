## Description:

Manages work todo items, including adding, viewing, completing, deleting, progress tracking, deadline grouping, and completion assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liumeixin](https://clawhub.ai/user/liumeixin)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and individual users use this skill to maintain work todo items in a local JSON file, track project status and progress, and generate daily work summaries grouped by due-date urgency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill modifies and can delete records in a local shared todo JSON file.

Mitigation: Keep another copy of important work-tracking data and confirm destructive actions before the agent updates or deletes todo records.

Risk: Todo IDs are timestamp-derived and are not collision-resistant.

Mitigation: Confirm the exact target item by ID plus task details before completing, updating, or deleting records, especially when multiple tasks are created close together.

Risk: Date parsing and completion assessment affect deadline grouping and delay labels.

Mitigation: Ask the user to confirm ambiguous due dates or completion dates before recording them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liumeixin/skills/work-todo)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown task summaries, status/progress updates, and JSON todo records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores todo data in a local shared JSON file and formats daily summaries by deadline category.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and _meta.json list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
