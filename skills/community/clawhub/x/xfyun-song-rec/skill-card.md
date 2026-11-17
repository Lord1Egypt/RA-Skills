## Description:

Recognize songs by singing or audio file using iFlytek's Query By ACRCloud technology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dzy-1026](https://clawhub.ai/user/dzy-1026)

### License/Terms of Use:


## Use Case:

External developers and automation users use this skill to identify music from an audio file for song discovery, karaoke, music search, audio content recognition, or similar workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload any readable file path selected for recognition to the external iFlytek API without validating that it is audio or limiting file size.

Mitigation: Use only audio files intentionally meant for iFlytek recognition, avoid sensitive or private recordings, and restrict inputs to an approved upload directory.

Risk: Untrusted prompts or workflows could choose an unintended local file path for recognition.

Mitigation: Do not let untrusted prompts control file paths; prefer a safer wrapper that rejects symlinks and non-regular files, validates audio type, and enforces a maximum size.

## Reference(s):

- [iFLYTEK Music Recognition API Documentation](https://www.xfyun.cn/doc/voiceservice/music_recognition/API.html)
- [ClawHub Skill Page](https://clawhub.ai/dzy-1026/skills/xfyun-song-rec)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON recognition result with song metadata, confidence, match details, and console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an audio file path and iFLYTEK API credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
