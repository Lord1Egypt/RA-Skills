## Description:

Use when a user asks to create a presentation, slide deck, PPT, or PPTX from a query and optional files, or to resume an existing SenseNova presentation task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

People creating or continuing a presentation task use this entry skill to organize source materials, gather evidence when appropriate, and route the work through a selected presentation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default external research may expose confidential details from presentation attachments in search queries.

Mitigation: For confidential presentations, require supplied materials only and prohibit external searches; otherwise approve sanitized search terms before searching.

Risk: Linked local images, companion skills, dependencies, and retained document extracts can introduce content or privacy concerns.

Mitigation: Review linked images and companion skills, use reviewed dependency versions, and remove retained extracts when they are no longer needed.

## Reference(s):

- [ClawHub sn-ppt-entry release](https://clawhub.ai/sensenova-skills/skills/sn-ppt-entry)

## Skill Output:

**Output Type(s):** [HTML presentations, PPTX presentations, Markdown outlines, JSON task files]

**Output Format:** [HTML and PPTX presentation files, with Markdown and JSON workflow artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presentation output follows the selected static, dynamic, or creative mode.]

## Skill Version(s):

2026.10.29 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
