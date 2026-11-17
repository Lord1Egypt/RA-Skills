## Description:

Segments long-form videos with an SRT transcript into 3-6 self-contained short clips and per-clip subtitles for downstream post-production.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianshuo](https://clawhub.ai/user/jianshuo)

### License/Terms of Use:

MIT-0

## Use Case:

Video producers and agent operators use this skill to select transcript-aligned topic boundaries, create segments.json, cut clips, extract frames, and slice per-clip subtitles for short-video publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packaged post-production behavior extends beyond the stated cut-and-crop segmentation purpose.

Mitigation: Install only when cover generation, subtitle burn-in, and intro-prepending are expected; otherwise review or remove those scripts before use.

Risk: External image-provider use may send video frames, titles, or prompts outside the local environment.

Mitigation: Require explicit user approval before invoking image generation and avoid sending sensitive media or transcript content to external providers.

Risk: ffmpeg and dependency trust assumptions can affect execution safety and output integrity.

Mitigation: Run in isolated project directories, use trusted pinned dependencies, and avoid shared temporary ffmpeg binaries.

## Reference(s):

- [segments_schema.json](artifact/references/segments_schema.json)
- [example_segments.json](artifact/references/example_segments.json)
- [platform_sizes.md](artifact/references/platform_sizes.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown instructions with JSON configuration and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When executed, the workflow produces segments.json plus per-segment clip, subtitle, and frame files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
