## Description:

Converts local audio files to text with AI summaries, recording key points, and speaker diarization through Tinrec's cloud transcription API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinrec-com](https://clawhub.ai/user/tinrec-com)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to transcribe local audio files through Tinrec, then retrieve transcripts, summaries, chapters, to-dos, recommendations, and speaker-labeled output for meetings, interviews, and recordings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected recordings and resulting transcripts may be sent to Tinrec's cloud service.

Mitigation: Use only when policy permits cloud processing of the audio and transcript content, and avoid confidential or regulated recordings unless approved.

Risk: API keys can be provided through a local file, command-line argument, or environment variable.

Mitigation: Protect the API key file and avoid exposing keys in shell history, logs, or shared workspaces.

Risk: The CLI accepts a custom base URL for network requests.

Mitigation: Use the default Tinrec endpoint unless the alternate endpoint is fully trusted and controlled.

## Reference(s):

- [Audio2Text ClawHub skill page](https://clawhub.ai/tinrec-com/skills/tinrec-audio2text)
- [Tinrec API keys](https://tinrec.com/api-keys)
- [Tinrec API endpoint](https://api.tinrec.com/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON transcription results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include transcripts, summaries, chapters, to-dos, recommendations, and speaker data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
