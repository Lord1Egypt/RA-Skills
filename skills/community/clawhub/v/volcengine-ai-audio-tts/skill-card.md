## Description:

Generates text-to-speech output through Volcengine audio services with voice, language, and format controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to convert text into speech, choose voice and language settings, set audio format parameters, and troubleshoot Volcengine TTS requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TTS requests may transmit user-provided text to Volcengine.

Mitigation: Avoid sending confidential text unless the Volcengine account, region, retention, and privacy terms meet the deployment requirements.

## Reference(s):

- [Sources](references/sources.md)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance, Files]

**Output Format:** [Markdown with an audio URL or path and reproducible TTS parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include duration and file size when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
