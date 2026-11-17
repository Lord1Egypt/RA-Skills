## Description:

Drafts structured Chinese weekly-review summaries from user-provided work logs, blockers, lessons learned, and next-week plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, managers, and individual contributors use this skill to turn weekly task notes into review-ready management and execution summaries. It is suited for weekly reports, meeting preparation, personal retrospectives, and planning workflows where missing facts should be marked for confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weekly review inputs may contain sensitive personal, project, or business information.

Mitigation: Provide only the notes intended for summarization and redact sensitive details before use.

Risk: Draft quality depends on the accuracy and completeness of user-provided logs.

Mitigation: Review the generated draft, confirm missing items, and keep uncertain items in the confirmation section.

Risk: The script's --output option writes to the path provided by the user.

Mitigation: Use stdout or --dry-run for review first, and check the destination path before writing files.

Risk: Additional audit modes exist in the script but are not the active configured workflow.

Mitigation: Leave audit modes disabled unless they receive separate review and clearer documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/weekly-review-pilot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown by default; JSON is available through the bundled script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script can print to stdout or write to a user-provided output path.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
