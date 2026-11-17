## Description:

Create 60s music videos from research articles using storyboard PDF, image/video/audio gen, and ffmpeg assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bunsdev](https://clawhub.ai/user/bunsdev)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and media producers use this skill to turn research articles into a structured storyboard, generated media assets, and a finished 60-second music video. The workflow is intended for resumable production runs with approval gates before paid or long-running provider work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research content, prompts, and generated assets may be sent to external image, video, and audio providers.

Mitigation: Avoid proprietary or sensitive source articles unless the selected providers are acceptable for that data.

Risk: Media generation can launch paid or long-running provider jobs.

Mitigation: Use the documented approval gates before provider selection, scene count, duration, and media generation.

Risk: Generated storyboards and media may overstate or distort scientific claims from the source article.

Mitigation: Preserve source notes and caveats in the storyboard and review prompts for research faithfulness before final generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bunsdev/skills/research-to-music-video-pipeline)
- [Storyboard template](artifact/templates/storyboard.md)
- [Run manifest schema](artifact/templates/manifest.schema.json)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON manifests, provider prompts, shell commands, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a storyboard PDF, prompt pack, manifest, generated scene assets, audio, and final MP4 when configured providers and approvals are available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
