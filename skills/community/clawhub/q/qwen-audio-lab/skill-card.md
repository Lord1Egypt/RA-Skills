## Description: <br>
Hybrid text-to-speech, reusable voice cloning, and narrated audio generation for macOS plus Aliyun Qwen. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aliyx](https://clawhub.ai/user/aliyx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content creators, and agents use this skill to convert text, text files, and PPT speaker notes into narrated audio. It supports local macOS speech for simple playback and Aliyun Qwen for downloadable audio, reusable cloned voices, and prompt-designed voices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud synthesis and voice cloning can send text and reference audio to Aliyun DashScope. <br>
Mitigation: Use mac-say for local-only speech, and use Qwen features only when cloud processing is acceptable. <br>
Risk: Voice cloning can create reusable voices from supplied recordings. <br>
Mitigation: Clone a voice only when the user has appropriate consent, especially for third-party voices. <br>
Risk: Remembered voices are stored locally for reuse. <br>
Mitigation: Review, delete, or relocate remembered voice state when reusable voice records should not be retained. <br>
Risk: Qwen commands require a DashScope API key. <br>
Mitigation: Limit the API key where possible and avoid exposing it in shared logs, prompts, or shell history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aliyx/qwen-audio-lab) <br>
- [Aliyun DashScope API endpoint](https://dashscope.aliyuncs.com/api/v1) <br>
- [Aliyun DashScope international API endpoint](https://dashscope-intl.aliyuncs.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON responses, and generated audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate WAV or MP3 audio files and local remembered-voice state when commands are executed.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
