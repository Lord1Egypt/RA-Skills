## Description: <br>
Generates speech with the MiniMax API, converts it to OPUS by default, and sends the audio to a Feishu/Lark user with lark-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to turn provided text into spoken audio and deliver it as a Feishu/Lark voice message or transferable MP3 file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text is sent to MiniMax and generated audio is delivered to the configured Feishu/Lark recipient. <br>
Mitigation: Use only with content and recipients approved for those services, and verify the MiniMax API key and Feishu/Lark user ID before running. <br>
Risk: Generated audio files may remain in /tmp or the working directory after delivery. <br>
Mitigation: Delete temporary and local audio files when they are no longer needed. <br>
Risk: Incorrect Feishu/Lark identity or audio settings can send to the wrong context or produce unusable voice messages. <br>
Mitigation: Use the documented bot identity and OPUS settings, then confirm delivery in the intended Feishu/Lark conversation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuchenggong19851114-design/voice-minimax) <br>
- [MiniMax TTS API endpoint](https://api.minimaxi.com/v1/t2a_v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and Python command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MiniMax API key, ffmpeg, lark-cli, and a Feishu/Lark user ID; writes temporary and local audio files before sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
