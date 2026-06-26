## Description: <br>
Use when a game, interactive story, or virtual world needs reusable NPC voice behavior, including fixed voice identity, catchphrases, relationship-aware dialogue, player voice intake through AudioClaw ASR, task briefings, narration, and event announcements synthesized with AudioClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kikidouloveme79](https://clawhub.ai/user/kikidouloveme79) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Game developers, narrative designers, and agent builders use this skill to create reusable NPC voice behavior, transcribe player speech, generate relationship-aware NPC lines, synthesize voice assets, and optionally send generated audio to Feishu for review or playtesting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Player speech, dialogue text, generated audio, and related metadata may be sent to AudioClaw/SenseAudio services and, when enabled, Feishu. <br>
Mitigation: Require explicit per-session opt-in before external delivery, confirm the Feishu destination chat, and define retention rules for transcripts and generated files. <br>
Risk: Sticky NPC voice mode can repeatedly send generated voice content after a session enters voice delivery mode. <br>
Mitigation: Keep external delivery disabled by default or reconfirm it for ongoing sessions, and provide a clear text-only fallback. <br>
Risk: The workflow depends on local credentials and injected API tokens for ASR, TTS, and Feishu delivery. <br>
Mitigation: Store credentials securely, avoid logging secrets or generated sensitive content, and rotate or revoke keys used during playtests. <br>


## Reference(s): <br>
- [NPC Voice Design](references/npc_voice_design.md) <br>
- [AudioClaw ASR Player Loop](references/asr_player_loop.md) <br>
- [AudioClaw ASR transcription endpoint](https://api.senseaudio.cn/v1/audio/transcriptions) <br>
- [AudioClaw TTS endpoint](https://api.senseaudio.cn/v1/t2a_v2) <br>
- [Feishu message API endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, audio files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; JSON transcripts, manifests, replies, and delivery summaries; MP3 audio files and optional Feishu audio messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call AudioClaw/SenseAudio ASR and TTS services and Feishu; writes generated transcripts, scene manifests, voice synthesis summaries, and audio files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
