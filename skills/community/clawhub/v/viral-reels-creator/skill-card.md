## Description:

Full-featured ffmpeg-based skill for creating and editing vertical short-form videos for Instagram Reels, TikTok, YouTube Shorts, and related platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yash-kavaiya](https://clawhub.ai/user/yash-kavaiya)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and developers use this skill to plan, assemble, caption, style, beat-sync, and export short-form vertical videos for major social platforms. It can guide agents through ffmpeg commands, helper scripts, and platform-specific export settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated ffmpeg commands and command-building examples may be unsafe when used with untrusted or unusual filenames.

Mitigation: Review commands before execution, quote paths carefully, avoid untrusted filenames, and use safe output names without slashes or traversal.

Risk: The batch export flow is overwrite-prone because it uses ffmpeg overwrite behavior for generated outputs.

Mitigation: Run exports in a dedicated output directory, inspect output names before execution, and keep backups of source and prior output files.

Risk: The installation guidance includes broad system-level package and pip installs.

Mitigation: Install and run the skill in an isolated container or virtual environment with reviewed, pinned dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yash-kavaiya/skills/viral-reels-creator)
- [Platform Specs Reference](artifact/references/platform-specs.md)
- [Viral Hooks & Content Strategy Reference](artifact/references/viral-hooks.md)
- [Beat-Synced Editing Reference](artifact/references/beat-sync.md)
- [Caption Templates Reference](artifact/references/caption-templates.md)
- [Animations Reference](artifact/references/animations.md)
- [Color Grading & Filters Reference](artifact/references/color-grading.md)
- [Transitions Reference](artifact/references/transitions.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, ffmpeg filter snippets, JSON analysis outputs, and generated video files when commands are executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact targets MP4 vertical-video outputs and platform-specific export variants.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
