## Description:

Downloads YouTube videos, extracts word-level subtitle timing, translates English subtitles to Chinese, and burns the translated subtitles into H.264 MP4 video with PIL-based antialiased rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryso](https://clawhub.ai/user/terryso)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, video localization operators, and external agent users use this skill to create Chinese-subtitled local MP4 files from YouTube videos. It supports subtitle extraction, translation batching, preview generation, and final subtitle burn-in for upload-ready video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path includes an unverified remote installer for uv.

Mitigation: Use a trusted package manager or a pinned, verified uv artifact before running the workflow.

Risk: Runtime dependencies are not fully pinned, which can affect reproducibility.

Mitigation: Run the scripts in a locked environment and pin Pillow and other execution dependencies.

Risk: The workflow downloads and processes external video content and may use a local proxy-switch command.

Mitigation: Run it in a limited working directory and inspect any proxy command before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and JSON subtitle file formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces subtitle segment JSON, translated subtitle JSON templates, preview MP4 files, and final burned-subtitle MP4 files when executed with the required local tools.]

## Skill Version(s):

1.1.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
