## Description:

Transcribe audio files via UniCloud ASR (云知声语音识别, recorded audio → text) API from UniSound.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaiccee](https://clawhub.ai/user/aaiccee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to transcribe recorded audio files through the UniSound UniCloud ASR API, including finance and customer service recordings. It is intended for file-based transcription rather than realtime speech recognition, TTS, live captions, or voice conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that recordings and authentication metadata are sent over plaintext HTTP.

Mitigation: Use an authenticated HTTPS UniSound endpoint before processing sensitive, customer, financial, regulated, or production recordings.

Risk: The security review reports published shared UAT credentials.

Mitigation: Treat embedded UAT credentials as public test credentials, use unique credentials, and rotate them before production use.

Risk: The skill uploads audio to UniSound servers for cloud transcription.

Mitigation: Review data handling requirements and test only with non-sensitive data until endpoint and credential controls are approved.

Risk: The security guidance recommends review before installing or using the skill.

Mitigation: Install dependencies in an isolated environment and review the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaiccee/skills/u2-audio-file-transcriber)
- [UniSound UniCloud ASR endpoint](http://af-asr.uat.hivoice.cn)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, configuration, guidance]

**Output Format:** [Plain text transcript or JSON result, with optional saved output file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8+, network access, and UniSound API credentials; supports WAV, MP3, M4A, FLAC, and OGG files up to 2 hours or 100 MB.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
