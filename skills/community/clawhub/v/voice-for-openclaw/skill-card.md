## Description: <br>
MiniMax TTS Plus generates speech from text with selectable agent voices and can produce local audio files or voice-message outputs for Telegram and Feishu workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vshen009](https://clawhub.ai/user/vshen009) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to synthesize text into voice output, choose per-agent voices, and generate or deliver audio through local files, Telegram, or Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to MiniMax. <br>
Mitigation: Avoid sending secrets, regulated content, or other sensitive text unless that use is intentional and approved. <br>
Risk: Generated audio can be posted to Telegram or Feishu when delivery credentials and targets are configured. <br>
Mitigation: Use generate-only mode for local output and configure channel credentials only for intended recipients. <br>
Risk: API and messaging credentials are required for full operation. <br>
Mitigation: Store credentials in a private .env file or environment variables and do not publish filled credential files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vshen009/voice-for-openclaw) <br>
- [MiniMax Speech T2A API documentation](https://platform.minimax.io/docs/api-reference/speech-t2a-http) <br>
- [MiniMax developer portal](https://platform.minimax.io) <br>
- [Telegram BotFather](https://t.me/BotFather) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration, Guidance] <br>
**Output Format:** [Shell commands and JSON status messages that point to generated MP3 or OGG/Opus audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, ffmpeg, requests, and MINIMAX_API_KEY; Telegram delivery requires TELEGRAM_BOT_TOKEN and TELEGRAM_TARGET.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
