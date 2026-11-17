## Description:

This skill helps agents convert text into MP3 speech audio through the hosted tts.102465.xyz API with selectable providers, voices, emotions, speech rate, and pitch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengwm64](https://clawhub.ai/user/fengwm64)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn supplied text into spoken MP3 audio for narration, read-aloud workflows, and voiceover drafts. The skill guides provider, voice, style, rate, and pitch selection before calling the hosted TTS API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for synthesis is transmitted to the third-party service tts.102465.xyz.

Mitigation: Do not send passwords, API keys, confidential scripts, private business data, regulated personal data, or other sensitive content.

Risk: GET requests can expose synthesized text in URLs, browser history, server logs, or shared links.

Mitigation: Prefer POST requests for generated audio, especially for longer or less public text.

Risk: Generated MP3 files can retain sensitive spoken content after the task is complete.

Mitigation: Delete generated MP3 files when they are no longer needed.

## Reference(s):

- [ClawHub TTS Skill](https://clawhub.ai/fengwm64/skills/tts-api)
- [Hosted TTS API](https://tts.102465.xyz)
- [Generate Speech Endpoint](https://tts.102465.xyz/api/tts)
- [Azure Voices Endpoint](https://tts.102465.xyz/api/voices?provider=azure)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl examples and MP3 audio output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce MP3 files from text sent to a third-party hosted TTS service.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
