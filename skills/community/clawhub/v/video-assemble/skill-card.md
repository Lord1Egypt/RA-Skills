## Description:

Assembles a final narrated video from source footage and timed voiceover, mixing original audio, producing subtitles, and optionally normalizing loudness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT-0

## Use Case:

Video editors and developers use this skill to turn source footage and prepared narration timings into a mixed, subtitled recap video with delivery quality records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media processing can create or delete files in selected work and output directories and overwrite existing recap outputs.

Mitigation: Review output paths and back up existing files before running; use a fresh work directory for strict adoption workflows.

Risk: JianYing export or media bundling can write additional files to the selected destination.

Mitigation: Review the export destination before enabling draft export or bundling.

## Reference(s):

- [ClawHub release](https://clawhub.ai/worldwonderer/skills/video-assemble)
- [Audio modes](artifact/references/audio-modes.md)
- [Subtitle tracks](artifact/references/subtitle-track.md)
- [JianYing template attribution](artifact/references/jianying/SOURCE.md)

## Skill Output:

**Output Type(s):** [Shell commands, Video files, Subtitle files, JSON metadata]

**Output Format:** [MP4 video, SRT/ASS subtitles, and JSON timeline and quality records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional JianYing draft export and subtitle burn-in.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
