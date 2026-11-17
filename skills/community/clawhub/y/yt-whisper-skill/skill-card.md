## Description:

Transcribes YouTube videos locally with Whisper on CUDA, archives URL/title-headed transcripts, and can produce structured AI summaries and compact research plans from input files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jagones84](https://clawhub.ai/user/jagones84)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and agent users use this skill to run local YouTube transcription workflows and turn transcripts or other documents into reusable summary and research-plan artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner can recursively delete MP4 files in the selected output directory.

Mitigation: Use a dedicated empty output directory for each run, and constrain cleanup to the per-run temp directory before using the skill on directories that may contain valuable media.

Risk: The installer creates a local virtual environment and copies runnable commands into user-level locations.

Mitigation: Review the installer before running it and confirm that creating .venv, ~/.local/bin/yt-transcribe, and ~/Transcriptions/Scripts/yt-transcribe.sh is acceptable in the target account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jagones84/skills/yt-whisper-skill)
- [OpenClaw documentation](https://docs.openclaw.ai/)
- [Artifact README](artifact/README.md)
- [Example transcript workflow](artifact/examples/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain-text transcripts and Markdown summary or research-plan files, with shell commands for setup and execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes transcripts under ~/Transcriptions/<Category>/ by default and may create *_AISUMMARY.md or *_AISEARCHPLAN.md companion files.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
