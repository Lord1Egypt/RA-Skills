## Description: <br>
High-performance audio library with text-to-speech (TTS) and speech-to-text (STT). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DarkNoah](https://clawhub.ai/user/DarkNoah) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Qwen Audio to create reusable voice profiles, synthesize speech, clone voices with supplied reference audio, and transcribe audio into text or subtitle files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install dependencies during use and may download models or packages. <br>
Mitigation: Review before installing, use an isolated Python or uv environment, and avoid running it where automatic package changes are unacceptable. <br>
Risk: Voice cloning can be misused when reference recordings are used without consent. <br>
Mitigation: Only use voice cloning with recordings you own or have explicit permission to use. <br>
Risk: Stored voice profiles can contain sensitive local audio and transcript data. <br>
Mitigation: Treat saved voice profiles as sensitive local data and restrict access to the skill directory. <br>


## Reference(s): <br>
- [Environment checklist](references/env-check-list.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Audio files, Subtitle files, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON command results plus WAV audio, plain text transcripts, and ASS/SRT subtitle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Voice profiles are stored as local files and generated outputs are written to user-specified paths.] <br>

## Skill Version(s): <br>
0.0.6 (source: release evidence; artifact frontmatter 0.0.4 and pyproject.toml 0.1.0 differ) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
