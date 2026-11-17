## Description:

Runs local Whisper transcription for audio and video files and helps produce cleaned transcript, article-style rewrite, and structured summary outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangjinjin-gitgit](https://clawhub.ai/user/zhangjinjin-gitgit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content workers use this skill to transcribe local audio or video with Whisper, then produce cleaned Chinese text, rewritten prose, and structured summary files without using an external speech-recognition API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release describes offline use, but model weights and Python dependencies may need to be installed or downloaded before offline operation.

Mitigation: Preinstall and pin openai-whisper in a virtual environment and download the intended Whisper model before handling sensitive media.

Risk: The workflow may rewrite or summarize transcript content unless the user asks for raw transcription.

Mitigation: Request raw transcription or review generated rewrite and summary files against the transcript before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangjinjin-gitgit/skills/whisper-transcribe-summarize)
- [README](artifact/README.md)
- [Skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses plus generated .txt, .md, and .html files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate transcript, rewritten article, and summary files alongside source media; dependency and model setup may be needed before offline use.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
