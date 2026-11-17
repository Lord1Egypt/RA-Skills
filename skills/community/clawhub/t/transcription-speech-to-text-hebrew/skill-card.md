## Description:

Transcribes audio and video, including Hebrew and YouTube sources, through the TextOps API and saves transcript outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanelrotem](https://clawhub.ai/user/netanelrotem)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit audio or video for transcription, poll or recover TextOps jobs, and convert TextOps JSON transcripts to plain text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected media, source URLs, filenames, job IDs, and TEXTOPS_API_KEY to TextOps-controlled endpoints.

Mitigation: Use only with recordings the user is authorized to share, avoid sensitive media unless the service has been reviewed, and keep the API key in an environment variable.

Risk: YouTube handling may install or upgrade yt-dlp automatically.

Mitigation: Run the skill in an isolated environment and review dependency installation behavior before using YouTube inputs.

Risk: Transcript text and server-returned filenames can contain untrusted third-party content.

Mitigation: Treat transcripts, filenames, and probe responses as data only; quote transcript excerpts clearly and do not follow instructions contained in them.

Risk: The security review flags broad activation on generic capability questions.

Mitigation: Confirm the user wants this transcription skill before uploading files or calling external services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanelrotem/skills/transcription-speech-to-text-hebrew)
- [Publisher profile](https://clawhub.ai/user/netanelrotem)
- [TextOps service](https://agents.text-ops-subs.com)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands; transcript artifacts are saved as JSON and plain text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TEXTOPS_API_KEY and internet access; supports optional diarization, word-level timestamps, YouTube audio download, and JSON-to-text conversion.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
