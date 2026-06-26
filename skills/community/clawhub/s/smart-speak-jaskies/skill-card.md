## Description: <br>
Smart Speak converts multilingual Vietnamese, Chinese/Pinyin, and English text segments into a merged MP3 using edge-tts voices and ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jaskies](https://clawhub.ai/user/Jaskies) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to generate multilingual lesson, announcement, or narration audio from structured text segments. It is intended for workflows that need native voices across Vietnamese, Chinese, and English in a single MP3 output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text sent for synthesis may include secrets, private business text, or personal data. <br>
Mitigation: Do not convert sensitive text unless the deployment accepts that text may be sent to the external TTS provider. <br>
Risk: The generated MP3 can overwrite the selected output path. <br>
Mitigation: Choose and review the output path before running the script. <br>
Risk: The script depends on a hard-coded edge-tts executable path that may not exist on the user's machine. <br>
Mitigation: Verify or update the edge-tts path before execution. <br>
Risk: The skill requires local ffmpeg and edge-tts installation from package sources. <br>
Mitigation: Install dependencies only from trusted package sources and verify they are available before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jaskies/smart-speak-jaskies) <br>
- [Publisher profile](https://clawhub.ai/user/Jaskies) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with JSON command arguments and MP3 file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, edge-tts, and ffmpeg; generated MP3 output may overwrite the selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
