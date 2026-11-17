## Description:

Create, edit, and visually verify durable teaching diagrams for study notes and technical explanations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[illustrated-paper-guide](https://clawhub.ai/user/illustrated-paper-guide)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, researchers, and note authors use this skill to create editable diagrams for mechanisms, pathways, causal chains, timelines, comparisons, spatial layouts, and technical explanations, then embed and visually verify them in context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may edit nearby note text and add image files when invoked.

Mitigation: Review proposed note edits and generated assets before accepting them, especially in shared or published notes.

Risk: Broad triggers can cause accidental invocation on ambiguous requests such as general model comparisons.

Mitigation: Confirm that a visual teaching diagram is desired before using the skill on ambiguous comparison or explanation requests.

Risk: Diagram output can introduce misleading visual claims, clipping, overlap, contrast issues, or broken rendering.

Mitigation: Render and visually inspect at least one output, checking text, arrows, margins, contrast, links, and consistency with the accompanying explanation.

## Reference(s):

- [Teaching Diagram Maker listing](https://clawhub.ai/illustrated-paper-guide/skills/teaching-diagram-maker)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, shell commands, guidance]

**Output Format:** [Markdown guidance with editable diagram files and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local note text and image assets, especially SVG diagrams, and should report where assets were saved, embedded, rendered, and inspected.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
