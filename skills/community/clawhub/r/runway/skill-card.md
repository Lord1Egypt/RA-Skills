## Description:

Prompt and direct Runway generative-video workflows for controlled camera moves, character consistency, edit-grade video edits, consent checks, disclosure planning, and human assembly of short clips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brand teams, agencies, and production operators use this skill to choose Runway when shot control, consistent references, or video-to-video edits matter. It helps an agent produce SHOT-style Runway briefs and route the work through human review, audio/caption assembly, consent checks, disclosure, and publishing handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated media workflows can mishandle likeness consent, AI disclosure, or publishing approval.

Mitigation: Review every workflow for consent, disclosure, and publishing approval before producing or releasing media.

Risk: API examples or operational notes may involve Runway credentials.

Mitigation: Keep Runway keys in server-side secrets or a secret manager; do not expose them in client code or generated content.

Risk: Runway clips require human assembly and review, so incomplete output could be mistaken for publish-ready media.

Mitigation: Treat skill output as production guidance and require human editing, audio/caption assembly, and final approval before publication.

## Reference(s):

- [ClawHub Runway skill page](https://clawhub.ai/social-media-skills/skills/runway)
- [The SHOT framework](artifact/references/the-shot-framework.md)
- [Control recipes](artifact/references/control-recipes.md)
- [Runway 2026 capabilities](artifact/references/runway-2026-capabilities.md)
- [Scope, consent, and tools layer](artifact/references/scope-and-tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with structured SHOT briefs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model, reference, assembly, consent, and disclosure notes; no executable output.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
