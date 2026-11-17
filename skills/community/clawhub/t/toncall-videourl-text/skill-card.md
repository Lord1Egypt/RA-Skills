## Description:

Transcribes accessible video URLs by downloading the video, extracting audio with ffmpeg, uploading the audio to Volcengine TOS, and using Volcengine speech recognition to return text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juysoft](https://clawhub.ai/user/juysoft)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and operators use this skill to turn an accessible video URL into a plain text transcript for review, summarization, or copy extraction. It is intended for media the user is allowed to process and requires user-provided Volcengine TOS and speech-recognition credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads arbitrary video URLs and sends extracted audio to Volcengine cloud services.

Mitigation: Use it only with media the user is permitted to process, avoid private or sensitive media, and restrict network egress to expected services.

Risk: Processing untrusted URLs can expose the runtime to oversized downloads, long-running jobs, or unexpected network destinations.

Mitigation: Run the skill in a sandbox and add URL allowlisting plus size and runtime limits before accepting arbitrary user-submitted URLs.

Risk: Temporary audio is uploaded to TOS and cleanup can fail.

Mitigation: Use scoped credentials, private storage policies, short-lived objects where possible, and monitor cleanup failures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juysoft/skills/toncall-videourl-text)
- [FFmpeg download](https://ffmpeg.org/download.html)
- [Volcengine ASR submit endpoint](https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit)
- [Volcengine ASR query endpoint](https://openspeech.bytedance.com/api/v3/auc/bigmodel/query)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text transcription with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves transcription files under texts/ and attempts to remove local temporary media files and the uploaded TOS temporary object after processing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
