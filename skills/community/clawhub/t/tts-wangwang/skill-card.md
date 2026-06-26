## Description: <br>
将输入文字通过 tts.wangwangit.com 转换为多种语音风格的 MP3 音频文件，并返回给用户。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinsuso](https://clawhub.ai/user/yinsuso) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user wants supplied text read aloud and returned as an audio file. It supports selecting voice, speed, pitch, and speaking style for text-to-speech generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided text is sent to an external TTS endpoint. <br>
Mitigation: Do not submit passwords, confidential business material, private records, or regulated data unless the endpoint has been independently vetted. <br>
Risk: Very long text may exceed the documented single-request character limit. <br>
Mitigation: Split text over 10,000 characters into smaller requests before generating audio. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinsuso/tts-wangwang) <br>
- [Publisher profile](https://clawhub.ai/user/yinsuso) <br>
- [TTS API endpoint](https://tts.wangwangit.com/v1/audio/speech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown with inline JSON, bash, and Python examples; generated audio is saved as an MP3 file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends user-provided text to tts.wangwangit.com and writes generated audio to a local file path such as /tmp/tts_output.mp3.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
