## Description:

Extract transcript or subtitles from a local video file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feiskyer](https://clawhub.ai/user/feiskyer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use this skill to turn local video files into readable transcripts, extracting embedded subtitles when present and using speech-to-text transcription when subtitles are absent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: When embedded subtitles are absent, audio may be sent to OpenAI or Azure OpenAI for transcription.

Mitigation: Use the API fallback only for videos whose audio is approved for external processing, and configure credentials in ~/.transcribe_video.env with restricted permissions.

Risk: Same-name .wav or .txt files beside the selected video may be deleted or overwritten by the bundled transcription script.

Mitigation: Check for existing same-name files before running the script, back up important files, or run the skill in a working copy of the video directory.

Risk: Unpinned Python dependencies can change behavior across environments.

Mitigation: Install dependencies in a virtual environment and prefer pinned versions for repeatable use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated text transcript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a transcript text file next to the source video and may create temporary audio during API transcription.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
