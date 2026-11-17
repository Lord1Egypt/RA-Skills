## Description:

Detects highlight moments in local livestream recordings and exports short clips using audio energy, scene changes, hybrid audio-video signals, audio-scene union, or ASR keyword density.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juzanxie-dev](https://clawhub.ai/user/juzanxie-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media operators use this skill to extract reusable highlight clips from local livestream recordings without manually reviewing and trimming the full video. It is suited for preparing short-form clips from moments with loud audio peaks, frequent visual transitions, or dense ASR commerce keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies may resolve to different package versions over time.

Mitigation: Install the skill in an isolated Python environment and pin or lock dependencies before production use.

Risk: Generated clips, segments.json, concat metadata, and merged_highlights.mp4 are written to the selected output directory and may overwrite prior generated outputs.

Mitigation: Use a dedicated output directory for each run and confirm it is safe to write before execution.

Risk: The highlight detector is heuristic and does not judge whether resulting clips are suitable for publication.

Mitigation: Review generated segments and final clips before redistribution or posting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/juzanxie-dev/skills/skill-live-highlight-slicer)
- [README](artifact/README.md)
- [Security Notes](artifact/SECURITY.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands; runtime outputs MP4 clips, segments.json metadata, and an optional merged MP4 file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local video input, ffmpeg, ffprobe, Python 3.9+, and the listed Python packages.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, clawhub.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
