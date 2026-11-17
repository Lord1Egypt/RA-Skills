## Description:

Writer Perspective Distiller guides an agent through a human-confirmed process for distilling a writer's fiction, nonfiction, biographical context, and selected passages into a callable writing-perspective skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinadu-ai](https://clawhub.ai/user/tinadu-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, writers, editors, and brand-voice builders use this skill to create a source-grounded perspective SKILL.md for writing or rewriting in a carefully analyzed authorial posture. The workflow is intended for human-supervised style distillation, with confirmation checkpoints before finalizing beliefs and blacklist guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated author-specific skills may contain private writing samples, organizational voice guidance, or copyrighted source material.

Mitigation: Review the generated SKILL.md before loading or sharing it, and remove private or copyrighted material that should not be included.

Risk: The skill can produce misleading style guidance if an agent relies on surface voice instead of confirmed source evidence.

Mitigation: Use the required human checkpoints for belief candidates and blacklist sharpening before finalizing the perspective skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tinadu-ai/skills/writer-perspective-distiller)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown SKILL.md draft with structured analysis and checkpoint prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local author-perspective skill after required human checkpoints and a user-judged quality gate.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
