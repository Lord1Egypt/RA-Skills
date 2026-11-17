## Description:

Video Transition helps agents generate Python guidance and ffmpeg-based workflows for applying xfade transitions, merging video clips, and adding fade effects to local media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[systiger](https://clawhub.ai/user/systiger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video automation users use this skill to create or adapt Python and ffmpeg commands for combining local video clips with transition effects and batch fade processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security scan marks the release suspicious because the fallback video merge path handles temporary files and paths unsafely.

Mitigation: Run only on trusted local media in a controlled output folder until the fallback concat path uses secure temporary files, escapes or rejects unsafe path characters, and validates transition and duration inputs.

## Reference(s):

- [Video Transition ClawHub Page](https://clawhub.ai/systiger/skills/video-transition)
- [systiger ClawHub Profile](https://clawhub.ai/user/systiger)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs assume local ffmpeg and ffprobe availability and trusted local media paths.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
