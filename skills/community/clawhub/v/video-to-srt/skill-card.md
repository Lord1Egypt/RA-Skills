## Description:

Generate timecoded SRT subtitles from local video or audio files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sallyxie2026](https://clawhub.ai/user/sallyxie2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to transcribe local video or audio into timecoded SRT subtitle files for editing tools and subtitle workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may create a local virtual environment, cache model files, and download Python or model dependencies.

Mitigation: Install only in environments where local dependency installation and model caching are acceptable.

Risk: Using --copy-next-to-input may replace an existing .srt file beside the source media.

Mitigation: Use explicit output directories and avoid --copy-next-to-input when an adjacent subtitle file should not be overwritten.

Risk: The default language is Chinese, which may reduce accuracy for other or mixed-language media.

Mitigation: Use --language auto or set the correct language for non-Chinese or mixed-language audio.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated SRT subtitle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local subtitle files and reports the subtitle path, detected language, and cue count.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
