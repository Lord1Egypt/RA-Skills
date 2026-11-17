## Description:

Automates a VFX media production workflow that parses requirements, creates optimized prompts, generates concept images, gates video creation on user confirmation, and writes an execution report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, technical artists, and game or VFX teams use this skill to turn a VFX request into structured prompts, concept image batches, optional confirmed video generation, and an execution report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically generate concept images and write output files when a matching VFX-material request triggers it.

Mitigation: Confirm that the user wants media generation before invoking the workflow; users who only want advice should state that clearly.

Risk: Video generation may create unintended media or consume additional generation resources if started accidentally.

Mitigation: Keep the documented video confirmation gate in place and require an explicit user selection before any video-generation step.

Risk: Generated VFX concepts or reports may not match the user's artistic intent or production constraints.

Mitigation: Review generated images, prompts, and the final report before using outputs in a production asset pipeline.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tianheihei002/skills/yq-vfx-pipeline-automation)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown report, optimized prompts, generated media files, and concise workflow status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May organize outputs under /workspace/vfx-output by date, with images, videos, prompts, and report files.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release evidence, and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
