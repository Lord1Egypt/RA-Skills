## Description:

Organizes screenshot-derived tasks, notes, priorities, missing information, archiving advice, and next steps into a reviewable structured brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn screenshot text summaries, context, and deadlines into task lists, notes, priorities, follow-up questions, archiving advice, and next actions. It is suited to post-screenshot organization, not OCR replacement or inventing screenshot content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshot-derived inputs may include personal, confidential, or otherwise sensitive content.

Mitigation: Provide only the files or text intended for review, and desensitize sensitive screenshot summaries before using the skill.

Risk: The bundled script contains dormant audit functions that are broader than the stated screenshot-to-task purpose.

Mitigation: Keep the bundled spec in structured_brief mode for normal use, and remove or document unused audit paths before broader deployment.

Risk: The skill does not replace OCR and should not invent screenshot content when inputs are incomplete.

Mitigation: Supply trusted OCR text or human-written screenshot summaries, and keep missing details in the confirmation section instead of filling gaps.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/screenshot-to-task)
- [README](artifact/README.md)
- [Structured Brief Spec](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Structured Markdown brief, with optional JSON wrapper when the local script is run with --format json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The normal output sections are task list, notes, priority, missing information, archiving advice, follow-up actions, confirmation items, and next step.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
