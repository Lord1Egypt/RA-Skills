## Description:

After sn-ppt-entry prepares a presentation task, this skill turns the query, user materials, and completed research into a single editable outline.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Presentation agents use this skill after task setup to synthesize the user's goal, supplied materials, and completed research into a coherent, editable slide outline for a downstream presentation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Revisions overwrite the existing outline and update task state.

Mitigation: Review the current outline and task inputs before revising, then confirm the updated outline before downstream slide production.

Risk: An outline may blur conflicts between user requests, source materials, external evidence, and inference.

Mitigation: Check claims against the supplied materials and completed research, and keep those evidence categories clearly distinguished.

## Reference(s):

- [sn-ppt-story on ClawHub](https://clawhub.ai/sensenova-skills/skills/sn-ppt-story)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Editable Markdown outline (outline.md)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one outline for downstream slide production; does not create slides or conduct new research.]

## Skill Version(s):

2026.10.29 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
