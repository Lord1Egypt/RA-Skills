## Description:

Turns speech from supported video links into a Chinese transcript with timestamps and a plain-text version.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luo4507](https://clawhub.ai/user/luo4507)

### License/Terms of Use:

MIT

## Use Case:

People using an agent to transcribe speech from supported video links into Chinese text, with a timestamped transcript and a plain-text copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video links may be fetched or opened in a headless browser without a separate confirmation.

Mitigation: Review the link and obtain consent before fetching or using browser fallback.

Risk: Media downloads disable TLS certificate verification.

Mitigation: Prefer a version that validates certificates; avoid untrusted links until corrected.

Risk: Video and audio processing may expose private content or leave temporary media in the execution environment.

Mitigation: Process sensitive videos only in a controlled environment and check that temporary files are removed.

Risk: Unpinned dependencies can change between installations.

Mitigation: Review and pin dependency versions before installation.

## Reference(s):

- [Video to Text (ZH) on ClawHub](https://clawhub.ai/luo4507/skills/video-to-text-zh)
- [Skill format reference](https://github.com/anthropics/skills)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Chinese plain text with timestamps, plus JSON metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes timestamped and plain-text transcripts; speech recognition may require review for names and specialized terms.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
