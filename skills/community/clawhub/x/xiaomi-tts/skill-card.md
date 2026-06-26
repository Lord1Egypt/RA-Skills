## Description: <br>
把文字转成语音。可以发语音、念给我听、唱歌、用方言或夹子音说话，支持各种情绪和风格。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangalexhy](https://clawhub.ai/user/zhangalexhy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert supplied text into expressive MiMo TTS speech with selectable voices, styles, emotions, roles, dialects, and output handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to Xiaomi/MiMo's remote TTS API. <br>
Mitigation: Do not submit secrets, private notes, or confidential prompts unless that sharing is acceptable; prefer a limited API key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangalexhy/xiaomi-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Audio files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the bundled script returns WAV audio or writes a .wav file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MIMO_API_KEY value supplied by environment variable, config file, or command-line option.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
