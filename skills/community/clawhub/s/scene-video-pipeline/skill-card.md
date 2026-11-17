## Description:

Produce modular scene-based videos from slide deck source and per-scene narration audio (text manifest + Kokoro). Includes Playwright slide rendering, per-scene clip generation, and final stitch via editable order file for easy reordering/splicing without full rerender.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content production agents use this skill to turn slide decks and narration manifests into modular narrated scene clips and a stitched final video. It supports reorder, splice, insert, and single-scene content fixes without rerendering the entire video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A narration manifest with unsafe audio_file paths can write or delete files outside the expected project folder.

Mitigation: Review manifests before use and restrict audio_file values to safe .mp3 filenames under the expected tts/audio directory.

Risk: The skill executes local shell scripts that generate and overwrite media artifacts.

Mitigation: Run it only in trusted project directories after reviewing the planned module path, order file, and generated output paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/scene-video-pipeline)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and directory contracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local video production with ffmpeg, ffprobe, node, and a Kokoro Python environment; generated project artifacts include narration audio, per-scene MP4 clips, scene-order text, and a stitched MP4.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
