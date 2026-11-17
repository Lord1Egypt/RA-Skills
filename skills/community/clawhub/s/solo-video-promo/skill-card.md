## Description:

Generate promo video plan with 30-45s script, shot-by-shot storyboard, and optional Remotion/Montage-tool config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortunto2](https://clawhub.ai/user/fortunto2)

### License/Terms of Use:

MIT

## Use Case:

Developers, product builders, and content teams use this skill to turn project context into a concise short-form promo video plan with a script, storyboard, asset checklist, and optional Remotion or Montage configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or overwrite docs/video-promo.md in the target repository.

Mitigation: Review the generated docs/video-promo.md diff before committing, especially when an existing promo plan is already present.

Risk: Generated scripts, storyboards, and tooling configuration may not accurately reflect the product or available assets.

Mitigation: Confirm the project details, asset checklist, and selected Remotion, Montage, FFmpeg, or manual editing path before production use.

## Reference(s):

- [Video Promo skill page](https://clawhub.ai/fortunto2/skills/solo-video-promo)
- [fortunto2 publisher profile](https://clawhub.ai/user/fortunto2)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown plan written to docs/video-promo.md with script, storyboard, asset checklist, and optional tooling configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Remotion, Montage-tool, FFmpeg, or manual editing guidance based on detected project tooling.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
