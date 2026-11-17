## Description:

Generate complete YouTube videos from a single prompt - script, voiceover, stock footage, captions, thumbnail. Self-contained, no external modules. 100% free tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayank8290](https://clawhub.ai/user/mayank8290)

### License/Terms of Use:


## Use Case:

Creators, marketers, and developers use this skill to turn a topic prompt into a YouTube-ready video package with script, voiceover, stock footage, captions, thumbnail, and metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom output name can make generated files land outside the advertised video output folder.

Mitigation: Use simple directory names for custom output values, run the skill in an isolated environment, and review output paths before execution.

Risk: The skill uses a Pexels API key and leaves generated media files on disk under the user's account.

Mitigation: Use a Pexels-only key, avoid sensitive topics or secrets in prompts, and review or clean generated files after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mayank8290/skills/youtube-factory)
- [Pexels API](https://pexels.com/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated local video project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg, edge-tts, and PEXELS_API_KEY; produces local script, audio, video, thumbnail, and metadata files.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
