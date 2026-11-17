## Description:

Transcribe audio files using Sber Salute Speech async API with Russian-first speech-to-text support for ru-RU, en-US, kk-KZ, ky-KG, and uz-UZ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chorus12](https://clawhub.ai/user/chorus12)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to transcribe permitted audio or video files through Sber Salute Speech and return a timestamped transcript plus saved result files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and audio are sent to Sber's service, and saved JSON/transcript files may contain sensitive content.

Mitigation: Use only media you are allowed to send to Sber, protect SALUTE_AUTH_DATA, and handle saved outputs as sensitive data.

Risk: SSL certificate checks are disabled by default.

Mitigation: Prefer a version that enables SSL verification or supports a trusted CA bundle before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chorus12/skills/salute-speech)
- [Sber developer studio](https://developers.sber.ru/studio/)
- [Salute Speech async recognition documentation](https://developers.sber.ru/docs/ru/salutespeech/rest/post-async-speech-recognition)
- [Salute Speech authentication documentation](https://developers.sber.ru/docs/ru/salutespeech/api/authentication)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance plus timestamped transcript text and raw JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sensitive transcript content; the skill requires uv and SALUTE_AUTH_DATA.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
