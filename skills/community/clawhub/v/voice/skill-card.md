## Description: <br>
Convert text to speech using Microsoft Edge's TTS engine with customizable voices, direct playback, and automatic temporary file cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaov1976](https://clawhub.ai/user/zhaov1976) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to convert text into spoken audio, play generated or existing audio files, list available voices, and clean up temporary audio files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided text and options are used to build shell commands. <br>
Mitigation: Install only from a trusted publisher, avoid untrusted text or options, and prefer updating command execution to safe argument-array execution before broader use. <br>
Risk: Spoken text is processed by Microsoft Edge TTS. <br>
Mitigation: Do not pass secrets, credentials, private messages, or other sensitive content to the skill. <br>
Risk: Playback paths and temporary audio cleanup behavior need review. <br>
Mitigation: Constrain playback to expected audio locations and verify cleanup timing before using the skill in shared or sensitive environments. <br>
Risk: Runtime dependencies are not fully pinned in the artifact evidence. <br>
Mitigation: Pin and review dependencies before deployment. <br>


## Reference(s): <br>
- [ClawHub Voice release page](https://clawhub.ai/zhaov1976/voice) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands] <br>
**Output Format:** [JSON-like status objects with media file paths, audio playback results, and voice lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary audio files and invoke local playback or dependency installation commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact package.json and CHANGELOG report 1.1.0, artifact skill.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
