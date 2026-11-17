## Description:

Automate YouTube video editing workflow: Download -> Transcribe (Whisper) -> Analyze (GPT-4) -> High-Quality Thumbnail (Korean & Character Consistency).

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeong-wooseok](https://clawhub.ai/user/jeong-wooseok)

### License/Terms of Use:


## Use Case:

External creators and developers use this skill to turn YouTube URLs or local videos into edited content packages with subtitles, Korean SEO metadata, and thumbnail assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs unpinned dependencies and invokes local subprocesses for video and optional image generation.

Mitigation: Review before installing and run only in an isolated project directory.

Risk: The optional image-generation path can expose NANO_BANANA_KEY through a child-process command line.

Mitigation: Avoid enabling the optional image-generation path until key handling is fixed and prefer environment-based secret passing to child processes.

Risk: The skill can invoke an installed nano-banana-pro skill and read user-provided avatar or font paths.

Mitigation: Review nano-banana-pro separately and avoid untrusted avatar filenames or paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jeong-wooseok/skills/youtube-editor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Generated files and console guidance, including SRT subtitles, transcript text, Markdown metadata, HTML thumbnail markup, and PNG thumbnail assets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENAI_API_KEY, FFmpeg, and optional NANO_BANANA_KEY for image generation.]

## Skill Version(s):

1.0.14 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
