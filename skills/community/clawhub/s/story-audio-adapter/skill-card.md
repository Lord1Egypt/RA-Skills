## Description: <br>
Converts structured `[role]text` story or script input into a multi-role narrated audio work by analyzing characters, matching them to voices, synthesizing segments with SenseAudio TTS, and returning a media reference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XinHao-96](https://clawhub.ai/user/XinHao-96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn tagged novels, stories, or scripts into multi-character audio for Feishu/OpenClaw delivery. It is intended for stories where narration and dialogue roles are clearly marked or can default to narration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically installs an unpinned Python dependency at runtime. <br>
Mitigation: Review before installation; run in a virtual environment and preinstall a pinned requests dependency, or ask the maintainer to remove runtime pip installation. <br>
Risk: Story text is sent to SenseAudio for synthesis and saved in local output files. <br>
Mitigation: Use a scoped SenseAudio API key and synthesize only content that is acceptable to send to SenseAudio and store locally. <br>


## Reference(s): <br>
- [Role Analysis Prompt](references/role_analysis_prompt.md) <br>
- [Voice Library](references/voice_library.json) <br>
- [SenseAudio API Base](https://api.senseaudio.cn) <br>
- [ClawHub Skill Page](https://clawhub.ai/XinHao-96/story-audio-adapter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Files, Media reference] <br>
**Output Format:** [Markdown response with JSON analysis, local file paths, WAV audio artifacts, and a MEDIA:./... reference] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY; saves segment audio, metadata, and a combined WAV output under the workspace outputs directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
